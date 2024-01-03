const setToCurrentDate = () => {
    document.getElementById('date').valueAsDate = new Date();
}

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
    const result = await response
    if (result.status === 200) {
        alert("Det ble lagt til i regnskapet!")
    }
    form.reset()
    setToCurrentDate()
})

setToCurrentDate()