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

    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(selectedFiles) {
        for (let file of selectedFiles) {
            if (file.type === "application/pdf") {
                files.push(file);
                displayFile(file);
            }
        }
        updateButtonState();
    }

    function displayFile(file) {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        tile.setAttribute('draggable', true);

        const icon = document.createElement('i');
        icon.classList.add('fa-regular', 'fa-file-pdf');
        icon.setAttribute('id', 'fa');

        const fileNameText = document.createTextNode(file.name);

        tile.appendChild(icon);
        tile.appendChild(fileNameText);

        tile.addEventListener('dragstart', () => tile.classList.add('dragging'));
        tile.addEventListener('dragend', () => {
            tile.classList.remove('dragging');
            updateFinalOrder();
        });

        pdfOrderingDiv.appendChild(tile);
        initDragAndDrop();
        belowStuff.classList.remove('hidden');
    }

    function initDragAndDrop() {
        const tiles = pdfOrderingDiv.querySelectorAll('.tile');

        tiles.forEach(tile => {
            tile.addEventListener('dragover', (e) => {
                e.preventDefault();
                const draggingTile = document.querySelector('.dragging');
                const closestTile = getClosestTile(e.clientY);

                if (closestTile) {
                    closestTile.classList.add('over');
                    closestTile.parentNode.insertBefore(draggingTile, closestTile);
                }
            });

            tile.addEventListener('dragleave', () => {
                tile.classList.remove('over');
            });
        });
    }

    function getClosestTile(mouseY) {
        const tiles = [...pdfOrderingDiv.querySelectorAll('.tile')];
        return tiles.reduce((closest, tile) => {
            const tileRect = tile.getBoundingClientRect();
            const offset = mouseY - tileRect.top - tileRect.height / 2;

            if (offset < 0 && offset > closest.offset) { return { tile, offset }; }
            else { return closest; }
        }, { offset: Number.NEGATIVE_INFINITY }).tile;
    }

    function updateButtonState() {
        if (files.length <= 1) { convertButton.disabled = true; }
        else { convertButton.disabled = false; }
    }

    function updateFinalOrder() {
        finalOrder = [...pdfOrderingDiv.querySelectorAll('.tile')].map(tile => tile.textContent.trim());
        console.log('Final order:', finalOrder);
    }

    function doMetadata() {
        return {
            "operation": "merge",
            "file name": files.map(file => file.name),
            "operationSpecificInfo": {
                "order": finalOrder
            }
        };
    }

    convertButton.addEventListener('click', uploadFiles);

    function uploadFiles() {
        const fD = new FormData();
        
        files.forEach(file => fD.append('file', file));
        fD.append('metadata', JSON.stringify(doMetadata()));
    
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
