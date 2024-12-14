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
        if (files.length) {
            selectedFile = files[0];
        }
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
        vals = [];
        inputFields.forEach(div => {
            const inputValue = div.querySelector('input').value;
            vals.push(inputValue);
        });

        var metadata;

        if (window.location.href.replace(/^http:\/\/127\.0\.0\.1:8080\//, '') == "split") {
            metadata = {
                "operation": "split",
                "file name": fileName,
                "operationSpecificInfo": {
                    "splitOnPage": vals[0]
                }
            }
        }

        return metadata;
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // const metadata = {
        //     "operation": window.location.href.replace(/^http:\/\/127\.0\.0\.1:8080\//, ''),
        //     "file name": file.name,
        //     "operationSpecificInfo": {}
        // };

        const metadata = doMetadata(file.name);

        formData.append('metadata', JSON.stringify(metadata));

        fetch('/upload', {
            method: 'POST',
            body: formData,
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
