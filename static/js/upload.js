document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileSelect = document.getElementById('fileSelect');
    const fileElem = document.getElementById('fileElem');

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('hover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('hover');
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('hover');
        const files = event.dataTransfer.files;
        if (files.length) {
            uploadFile(files[0]);
        }
    });

    fileSelect.addEventListener('click', () => fileElem.click());

    fileElem.addEventListener('change', () => {
        if (fileElem.files.length) {
            uploadFile(fileElem.files[0]);
        }
    });

    function uploadFile(file) {
        if (file.type !== 'application/pdf') {
            alert('Please upload a valid PDF file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        const metadata = {
            "operation": "split",  // chat please fix this
            "file name": file.name
        };

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
