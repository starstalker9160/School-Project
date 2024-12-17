document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileSelect = document.getElementById('file-select');
    const fileElem = document.getElementById('file-elem');
    const convertButton = document.getElementById('convert-button');
    const inputFields = document.querySelectorAll('.inputFields');
    const fromDocxSwapOne = document.getElementById('from-docx-swap-one');
    const fromDocxSwapTwo = document.getElementById('from-docx-swap-two');
    const docFileName = document.getElementById('doc-file-name');
    const pdfFileName = document.getElementById('pdf-file-name');
    const toDocxSwapOne = document.getElementById('to-docx-swap-one');
    const toDocxSwapTwo = document.getElementById('to-docx-swap-two');

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
        if (files.length) { selectedFile = files[0]; }
    });

    fileSelect.addEventListener('click', () => fileElem.click());

    fileElem.addEventListener('change', () => {
        if (fileElem.files.length) { selectedFile = fileElem.files[0]; }
    });

    bigBoiButton.addEventListener('click', () => {
        if (selectedFile) { uploadFile(selectedFile); }
        else { alert("Please select a file first!"); }
    });

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

            case "from-pdf":
                metadata = {
                    "operation": "from-pdf",
                    "file name": fileName,
                    "operationSpecificInfo": {}
                };
                break;

            case "from-docx":
                metadata = {
                    "operation": "from-docx",
                    "file name": fileName,
                    "operationSpecificInfo": {}
                };
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
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
