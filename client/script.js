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


window.addEventListener('submit', async (event) => {
    event.preventDefault()

    // Retrieve password from local storage
    let password = localStorage.getItem('password')

    // If password is not set, ask for it
    if (!password) {
        setPassword()
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
            alert("Det ble lagt til i regnskapet!")
        }
        event.target.reset()
        setToCurrentDate()
    }
    catch (error) {
        console.error('Error:', error)
        localStorage.removeItem('password')
    }
})

setToCurrentDate()