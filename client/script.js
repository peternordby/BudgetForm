document.getElementById('date').valueAsDate = new Date();

window.addEventListener('submit', async (event) => {
    event.preventDefault()
    const form = event.target
    const data = new FormData(form)
    const value = Object.fromEntries(data.entries())
    const json = JSON.stringify(value)
    const url = form.action
    console.log("json:", json)
    console.log("url:", url)

    const response = await fetch(url, {
        method: 'POST',
        body: json,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    const result = await response.json()
    console.log("result:", result)
    form.reset()
    form.elements[0].focus()
})