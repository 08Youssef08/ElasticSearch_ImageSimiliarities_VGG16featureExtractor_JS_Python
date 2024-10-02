const dropZone = document.getElementById("drop_zone");
const output = document.getElementById("output");

dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropZone.classList.add("highlight");
});

dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("highlight");
});

dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropZone.classList.remove("highlight");

    const files = e.dataTransfer.files;
    if (files.length) {
        const file = files[0];
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64Image = event.target.result.split(",")[1]; // Extract base64
                dropZone.style.backgroundImage = `url(${event.target.result})`; // Set drop zone background
                dropZone.style.color = 'transparent'; // Hide the text

                output.innerHTML = "Image uploaded. Extracting features...";

                // Send the Base64 image to the Python backend for feature extraction
                fetch('/extract_features', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ image: base64Image })
                })
                .then(response => response.json())
                .then(data => {
                    output.innerHTML = `Extracted Features: ${JSON.stringify(data.features)}`;
                    
                    // Now that features are extracted, use them to search for similar images
                    return fetch('/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ features: data.features })  // Use extracted features here
                    });
                })
                .then(response => response.json())
                .then(similarImages => {
                    // Clear only image display, keep the drop zone
                    const gridContainer = document.createElement('div');
                    gridContainer.classList.add('grid-container');

                    // Iterate through the similar images and display them in the grid
                    similarImages.forEach(img => {
                        const imgPath = `./static/images/${img.relative_path}`;
                        const imgElement = document.createElement('img');
                        imgElement.src = imgPath;
                        imgElement.alt = `Image ID: ${img.image_id}`;
                        imgElement.classList.add('grid-item');

                        gridContainer.appendChild(imgElement);
                    });

                    // Clear old grid content, append new grid
                    output.innerHTML = "";  // Clear previous results but not the drop zone
                    output.appendChild(gridContainer);
                    
                    console.log('Similar images:', similarImages);
                })
                .catch(error => {
                    output.innerHTML = `Error: ${error}`;
                    console.error('Error:', error);
                });

            };
            reader.readAsDataURL(file);  // Convert image to Base64
        } else {
            output.innerHTML = "Please drop an image file.";
        }
    }
});
