const button = document.getElementById("download-button");
const urlInput = document.getElementById("url-input");
const interface = document.getElementById("interface");
const thankyou = document.getElementById("thankyou");


button.onclick = download
urlInput.onkeyup = (key) => {if (key == "Enter") download()};
    

function download() {

    // const id = urlInput.value.replace("https://www.youtube.com/playlist?list=", "")

    console.log(urlInput.value)

    if (urlInput.value.replace(" ", "") == "") {
        return
    }

    // Hide the interface and show the thank you content
    interface.style.visibility = "hidden";
    interface.style.position = "absolute";
    thankyou.style.visibility = "visible";


    // Go to download
    window.location.href = "download?url=" + encodeURIComponent(urlInput.value)
}