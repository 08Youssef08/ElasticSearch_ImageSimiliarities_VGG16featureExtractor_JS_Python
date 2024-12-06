const dropZone = document.getElementById("drop_zone");
const output = document.getElementById("output");
let topK=5;
document.getElementById("TopkButt").addEventListener('keydown', function (event) {
    if (event.key === 'Enter') { 
        const inputVal = document.getElementById("TopkButt").value;

        if (inputVal && !isNaN(inputVal)) {
            topK = parseInt(inputVal, 10); 
            console.log('Number of results set to:', topK);
        } else {
            console.error('Invalid input. Using default topK value.');
            topK = 5; 
        }
    }
});
let selectedMetric = "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0";  // Default metric 

//listeners to buttons to capture the selected metric
document.getElementById('cosineBtn').addEventListener('click', function() {
    selectedMetric = "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0";
});
document.getElementById('l1Btn').addEventListener('click', function() {
    selectedMetric = "1 / (1 + l1norm(params.query_vector, 'image_embedding'))";
});
document.getElementById('euclideanBtn').addEventListener('click', function() {
    selectedMetric = "1 / (1 + l2norm(params.query_vector, 'image_embedding'))";
});
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
                    
                    // using features to search for similar images
                    return fetch('/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ features: data.features,
                            metric: selectedMetric,
                            topK : topK
                         }) 
                    });
                })
                .then(response => response.json())
                .then(similarImages => {
                    // image display
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

                    // Clear old grid 
                    output.innerHTML = "";  // Clear previous results but not the drop zone
                    output.appendChild(gridContainer);
                    
                    console.log('Similar images:', similarImages);
                })
                .catch(error => {
                    output.innerHTML = `Error: ${error}`;
                    console.error('Error:', error);
                });

            };
            reader.readAsDataURL(file); 
        } else {
            output.innerHTML = "Please drop an image file.";
        }
    }
});
