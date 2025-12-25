import json
import os
from typing import Any, Dict, Iterable

from dotenv import load_dotenv
from flask import Flask, make_response, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

app = Flask(__name__)

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
REQUIRED_FIELDS = {"password", "date", "amount", "description", "category", "tag"}


def _add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, POST"
    return response


@app.after_request
def apply_cors_headers(response):
    return _add_cors_headers(response)


def _error_response(message: str, status: int):
    response = make_response(message, status)
    return _add_cors_headers(response)


def _get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


def _sanitize_text(value: Any) -> str:
    # Prevent spreadsheet formula injection
    text = "" if value is None else str(value).strip()
    if text.startswith(("=", "+", "-", "@")):
        text = f"'{text}"
    return text


def _parse_amount(raw_amount: Any) -> float:
    try:
        return float(raw_amount)
    except (TypeError, ValueError) as exc:
        raise ValueError("Amount must be numeric") from exc


def _validate_payload(data: Dict[str, Any]) -> Iterable[str]:
    return [field for field in REQUIRED_FIELDS if data.get(field) is None]


def _get_sheets_service():
    # Env var contains the *full* JSON content of the service account key
    raw = _get_required_env("GOOGLE_CREDS")

    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("GOOGLE_CREDS is not valid JSON") from exc

    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPE)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


@app.route("/")
def index():
    return "Submit POST requests to /addRow"


@app.route("/addRow", methods=["POST", "OPTIONS"])
def add_row():
    if request.method == "OPTIONS":
        return _add_cors_headers(make_response("Success", 200))

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return _error_response(
            "Bad Request\nExpected JSON with password, date, amount, description, category, and tag",
            400,
        )

    missing_fields = _validate_payload(data)
    if missing_fields:
        return _error_response(
            f"Bad Request\nMissing required fields: {', '.join(sorted(missing_fields))}",
            400,
        )

    try:
        expected_password = _get_required_env("PASSWORD")
        spreadsheet_id = _get_required_env("SPREADSHEET_ID")
    except RuntimeError:
        return _error_response("Server misconfigured", 500)

    if data.get("password") != expected_password:
        return _error_response("Unauthorized", 401)

    try:
        amount = _parse_amount(data["amount"])
    except ValueError as exc:
        return _error_response(f"Bad Request\n{exc}", 400)

    transaction_date = _sanitize_text(data["date"])
    description = _sanitize_text(data["description"])
    category = _sanitize_text(data["category"])
    tag = _sanitize_text(data["tag"])

    # Append: date, date, amount, description, category, tag
    values = [[transaction_date, transaction_date, amount, description, category, tag]]

    try:
        service = _get_sheets_service()
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="Utgifter!A:F",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()
    except HttpError:
        return _error_response("Upstream service unavailable", 502)
    except Exception:
        return _error_response("Server error", 500)

    return _add_cors_headers(make_response("Success", 200))
