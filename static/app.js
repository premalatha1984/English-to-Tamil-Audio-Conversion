

document.getElementById("uploadForm").addEventListener("submit", async (event) => {
  
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        displayResponse(data);
    } catch (error) {
        console.error("Error:", error);
    }
});

function displayResponse(data) {
    const responseDiv = document.getElementById("response");
    responseDiv.innerHTML = `
        <p>File Uploaded: ${data.filename}</p>
        <p>Transcription: ${data.transcription}</p>
    `;
}
