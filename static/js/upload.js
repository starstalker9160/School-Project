document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileSelect = document.getElementById('fileSelect');
    const fileElem = document.getElementById('fileElem');
    const bigBoiButton = document.getElementById('big-boi');
    const inputFields = document.querySelectorAll('.inputFeilds');
    
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
        regexOut = window.location.href.match(/[^\/]+$/)[0]

        vals = [];
        inputFields.forEach(div => {
            const inputValue = div.querySelector('input').value;
            vals.push(inputValue);
        });

        var metadata;

        switch (regexOut) {
            case "split":
                metadata = {
                    "operation": "split",
                    "file name": fileName,
                    "operationSpecificInfo": {
                        "splitOnPage": vals[0]
                    }
                }
            case "from-pdf":
                metadata = {
                    "operation": "from-pdf",
                    "file name": fileName,
                    "operationSpecificInfo": {}
                }
            case "from-docx":
                metadata = {
                    "operation": "from-docx",
                    "file name": fileName,
                    "operationSpecificInfo": {}
                }
        }

        return metadata;
    }

    function uploadFile(file) {
        const fD = new FormData();
        fD.append('file', file);

        const metadata = doMetadata(file.name);

        fD.append('metadata', JSON.stringify(metadata));

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
