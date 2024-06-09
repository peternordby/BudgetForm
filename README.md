# BudgetForm

Web application for remotely accessing a budget and expense sheet in Google Drive 📊

## Client

The website is built using HTML, CSS, and JavaScript. It implements neumorphic design for the form. The website is hosted using GitHub Pages and submits the form data via a POST request to the server.

## Server

The server is hosted with Vercel. It is built with Flask and accepts POST requests from the client. The data is validated before it is inserted into the sheet using the Google Spreadsheets API with Google Credentials.
