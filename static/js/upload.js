document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileSelect = document.getElementById('file-select');
    const fileElem = document.getElementById('file-elem');
    const convertButton = document.getElementById('convert-button');
    const inputFields = document.querySelectorAll('.inputFields');
    const docFileName = document.getElementById('doc-file-name');
    const pdfFileName = document.getElementById('pdf-file-name');

    const operation = window.location.href.match(/[^\/]+$/)[0];

    let selectedFile = null;

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('hover');
    });

    dropArea.addEventListener('dragleave', () => { dropArea.classList.remove('hover'); });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('hover');
        const files = event.dataTransfer.files;
        if (files.length) {
            selectedFile = files[0];

            performJSOperation();
        }
    });

    fileSelect.addEventListener('click', () => fileElem.click());

    fileElem.addEventListener('change', () => {
        if (fileElem.files.length) {
            selectedFile = fileElem.files[0];

            performJSOperation();
        }
    });

    convertButton.addEventListener('click', () => {
        if (selectedFile) { uploadFile(selectedFile); }
        else { alert("Please select a file first!"); }
    });

    function performJSOperation() {
        switch (operation) {
            case "split":
                split(selectedFile.name)
        }
    }

    function split(filename) {
        document.getElementById('split-swap-one').classList.toggle('hidden');
        document.getElementById('split-swap-two').classList.toggle('hidden');
        document.getElementById('split-page-input').classList.toggle('hidden');
        document.getElementById('pdf-file-name').innerHTML = filename;
        document.getElementById('output-pdf-file-one-name').innerHTML = filename.replace(/\.[^/.]+$/, "") + "_part_1.pdf"
        document.getElementById('output-pdf-file-two-name').innerHTML = filename.replace(/\.[^/.]+$/, "") + "_part_2.pdf"
    }

    function doMetadata(fileName) {
        var vals = [];
        inputFields.forEach(div => {
            const inputValue = div.querySelector('input').value;
            vals.push(inputValue);
        });

        var metadata;

        switch (operation) {
            case "split":
                metadata = {
                    "operation": "split",
                    "file name": fileName,
                    "operationSpecificInfo": {
                        "splitOnPage": vals[0]
                    }
                };
                vals = [];
                break;
        }
        return metadata;
    }

    function uploadFile(file) {
        const fD = new FormData();
        fD.append('file', file);
        fD.append('metadata', JSON.stringify(doMetadata(file.name)));

        fetch('/upload', {
            method: 'POST',
            body: fD,
        })
            .then(response => {
                const contentType = response.headers.get('Content-Type');

                if (response.ok && contentType && contentType.includes('application/json')) {
                    return response.json();
                } else if (response.ok && contentType) {
                    const url = new URL(response.url);
                    const errorMessage = url.searchParams.get('error_message');
                    const color = url.searchParams.get('color');
                    window.location.href = `/error?error_message=${encodeURIComponent(errorMessage)}&color=${encodeURIComponent(color)}`;
                    return Promise.reject('Redirecting to error page');
                } else {
                    return Promise.reject('Unexpected response type');
                }
            })
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});
