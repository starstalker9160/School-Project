document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-elem');
    const fileSelectButton = document.getElementById('file-select');
    const convertButton = document.getElementById('convert-button');
    const pdfOrderingDiv = document.getElementById('pdf-ordering');
    const belowStuff = document.querySelector('.belowStuff');

    let files = [];
    let finalOrder = [];

    fileSelectButton.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

    dropArea.addEventListener('dragover', (e) => e.preventDefault());
    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
    });

    const handleFiles = (selectedFiles) => {
        Array.from(selectedFiles).forEach(file => {
            if (file.type === "application/pdf") {
                files.push(file);
                displayFile(file);
            }
        });
        updateButtonState();
    };

    const displayFile = (file) => {
        const tile = createTile(file);
        pdfOrderingDiv.appendChild(tile);
        initDragAndDrop();
        belowStuff.classList.remove('hidden');
    };

    const createTile = (file) => {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        tile.setAttribute('draggable', true);

        const icon = document.createElement('i');
        icon.classList.add('fa-regular', 'fa-file-pdf');

        tile.appendChild(icon);
        tile.appendChild(document.createTextNode(file.name));

        tile.addEventListener('dragstart', () => tile.classList.add('dragging'));
        tile.addEventListener('dragend', () => {
            tile.classList.remove('dragging');
            updateFinalOrder();
        });

        return tile;
    };

    const initDragAndDrop = () => {
        const tiles = pdfOrderingDiv.querySelectorAll('.tile');

        tiles.forEach(tile => {
            tile.addEventListener('dragover', (e) => {
                e.preventDefault();
                const draggingTile = document.querySelector('.dragging');
                const closestTile = getClosestTile(e.clientY);

                if (closestTile) {
                    closestTile.parentNode.insertBefore(draggingTile, closestTile);
                }
            });
        });
    };

    const getClosestTile = (mouseY) => {
        return [...pdfOrderingDiv.querySelectorAll('.tile')].reduce((closest, tile) => {
            const offset = mouseY - tile.getBoundingClientRect().top - tile.offsetHeight / 2;
            return offset < 0 && offset > closest.offset ? { tile, offset } : closest;
        }, { offset: Number.NEGATIVE_INFINITY }).tile;
    };

    const updateButtonState = () => {
        convertButton.disabled = files.length <= 1;
    };

    const updateFinalOrder = () => {
        finalOrder = [...pdfOrderingDiv.querySelectorAll('.tile')].map(tile => tile.textContent.trim());
    };

    const doMetadata = () => ({
        operation: "merge",
        "file name": files.map(file => file.name),
        operationSpecificInfo: { order: finalOrder }
    });

    convertButton.addEventListener('click', () => {
        const formData = new FormData();

        files.forEach(file => formData.append('file', file));
        formData.append('metadata', JSON.stringify(doMetadata()));

        fetch('/upload', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => alert(data.error || data.message))
            .catch(error => console.error('Error:', error));
    });
});
