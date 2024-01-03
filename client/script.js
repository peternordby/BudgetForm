const setToCurrentDate = () => {
    document.getElementById('date').valueAsDate = new Date();
}

const generateJSON = (form, password) => {
    const data = new FormData(form)
    const value = { ...Object.fromEntries(data.entries()), password: password }
    const json = JSON.stringify(value)
    return json
}

const setPassword = () => {
    const password = prompt("Skriv inn passordet")
    localStorage.setItem('password', password)
}

const COLORS = {
    DEFAULT: '#BABECC',
    SUCCESS: '#169123',
    ERROR: '#911616'
}

const setBackgroundColor = (color) => {
    const root = document.querySelector(':root')
    root.style.setProperty('--color-shadow', color)
}


window.addEventListener('submit', async (event) => {
    event.preventDefault()

    const submitButton = document.getElementById('submit')
    const submitText = document.getElementById('submit-text')
    const spinner = document.getElementById('spinner')

    submitButton.disabled = true
    submitText.style.display = 'none'
    spinner.style.display = 'block'


    // Retrieve password from local storage
    let password = localStorage.getItem('password')

    // If password is not set, ask for it
    while (password === null) {
        setPassword()
        password = localStorage.getItem('password')
    }

    const json = generateJSON(event.target, password)
    const url = 'https://server-wine-eta.vercel.app/addRow'


    try {
        const response = await fetch(url, {
            method: 'POST',
            body: json,
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const result = await response
        if (result.status === 200) {
            setBackgroundColor(COLORS.SUCCESS)
        }
        setTimeout(() => {
            setBackgroundColor(COLORS.DEFAULT)
            event.target.reset()
            setToCurrentDate()
        }, 1000)
    }
    catch (error) {
        console.error('Error:', error)
        setBackgroundColor(COLORS.ERROR)
        localStorage.removeItem('password')
        setTimeout(() => setBackgroundColor(COLORS.DEFAULT), 1000)
    }
    finally {
        submitButton.disabled = false
        submitText.style.display = 'block'
        spinner.style.display = 'none'
    }
})

setToCurrentDate()