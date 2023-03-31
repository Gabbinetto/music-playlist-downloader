const button = document.getElementById('download-button');
const urlInput = document.getElementById('url-input')
button.onclick = () => {

    // const id = urlInput.value.replace('https://www.youtube.com/playlist?list=', '')

    console.log(urlInput.value)

    if (urlInput.value.replace(" ", "") == "") {
        return
    }

    window.location.href = 'download?url=' + encodeURIComponent(urlInput.value)
}