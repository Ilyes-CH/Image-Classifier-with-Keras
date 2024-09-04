function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function () {
        const output = document.getElementById('image-preview');
        output.src = reader.result;
        output.style.display = 'block';
    };
    console.log(event.target.files)
    reader.readAsDataURL(event.target.files[0]);
}

document.getElementById('upload-form').onsubmit = function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/uploader', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('prediction').innerText = `${data.prediction} with probability ${data.probability}%`;
            document.getElementById('result').style.display = 'block';
            document.getElementById('progressBar').style.display = 'block'

            document.getElementById('progressBar').innerHTML = `  <div
          class="progress-bar gradient-bar" 
          role="progressbar"
          aria-valuenow="${data.probability}"
          aria-valuemin="0"
          aria-valuemax="${data.probability}"
          style="width: ${data.probability}%;"
        >
         ${data.probability}
        </div>`
        })
        .catch(error => {
            console.error('Error:', error);
        });
};