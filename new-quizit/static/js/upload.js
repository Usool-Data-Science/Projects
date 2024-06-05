// First select all the drop zone input on the page.
// Track back to select the (closest) drop zone element of that specific input
// When dragged over, add the drop-zone--over class
// for each of [dragleave, dragend], remove the drop-zone--over class.

// NOW LETS DO THE MAIN WORK.
// First prevent default behavior for the dragover and drop event
// CHECK IF USER USES THE CLICK EVENT INSTEAD OF DRAG/DROP///////
// Add the click event listener to the dropzone, then let the inputElement be clicked
// if the click results in a change in the inputElement and it has a file,
// Then update the thumbnail with that file
// CHECK IF USER USES DRAG AND DROP///////////
// Then check if there is at least one file in the event.dataTransfer.files
// If there is, then assign that file into the inputElement.file
// Then update the thumbnail
// Also remove the drop-zone--over class since we are done with the dropping.

// NOW LETS DECLARE THE THUMBNAIL CLASS
// prototype the thumbnail element to accept the drop-zone--Element and the file
// Clear the space for our thumbnail by removing the prompt if it still exist there.
// query the thumbnail element if it exist otherwise declare it afresh and append it to the dropzone element.
// Add label to the thumbnailelement

// NOW LETS SHOW THE IMAGE FOR THE THUMBNAIL USING FILE READER
// Check if the file type starts with image/, then use the filereader to read it asynchronously.
// then set the background image of the thumbnail to that image.
// Otherwise show nothing in the background.

// Alternative thumbnails
let pdfLogo = new Image();
let htmlLogo = new Image();
let wordDocLogo = new Image();

pdfLogo.src = "static/img/thumbnails/pdf logo.png";
htmlLogo.src = "static/img/thumbnails/html logo.png";
wordDocLogo.src = "static/img/thumbnails/word_doc_logo.png";

// Ensure the images are loaded before attaching event listeners
pdfLogo.onload = htmlLogo.onload = wordDocLogo.onload = function () {
    document.querySelectorAll(".drop_zone__input").forEach((inputElement) => {
        const dropZoneElement = inputElement.closest(".drop_zone");

        dropZoneElement.addEventListener("click", (e) => {
            inputElement.click();
        });

        inputElement.addEventListener("change", (e) => {
            if (inputElement.files.length) {
                updateThumbnail(dropZoneElement, inputElement.files[0]);
                handleFileUpload(inputElement.files[0]);
            }
        });

        // Change the border style
        dropZoneElement.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZoneElement.classList.add("drop_zone--over");
        });

        ["dragleave", "dragend"].forEach((type) => {
            dropZoneElement.addEventListener(type, (e) => {
                dropZoneElement.classList.remove("drop_zone--over");
            });
        });

        dropZoneElement.addEventListener("drop", (e) => {
            e.preventDefault();

            if (e.dataTransfer.files.length) {
                inputElement.files = e.dataTransfer.files;
                updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
                handleFileUpload(e.dataTransfer.files[0]);
            }

            dropZoneElement.classList.remove("drop_zone--over");
        });
    });
};

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop_zone__thumb");

    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop_zone__prompt")) {
        dropZoneElement.querySelector(".drop_zone__prompt").remove();
    }

    // First time - there is no thumbnail element, so let's create it
    if (!thumbnailElement) {
        thumbnailElement = document.createElement("div");
        thumbnailElement.classList.add("drop_zone__thumb");
        dropZoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        };
    } else if (file.type === "application/pdf") {
        thumbnailElement.style.backgroundImage = `url('${pdfLogo.src}')`;
    } else if (file.type.includes("officedocument")) {
        thumbnailElement.style.backgroundImage = `url('${wordDocLogo.src}')`;
    } else if (file.type === "text/html") {
        thumbnailElement.style.backgroundImage = `url('${htmlLogo.src}')`;
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}

function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('myFile', file);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Assuming the server doesn't need to send a response body for the file preview
            // Just preview the file uploaded using its URL object
            const previewSection = document.querySelector(".previewer");
            const pdfUrl = URL.createObjectURL(file);
            previewSection.innerHTML = `<iframe src="${pdfUrl}" width="100%" height="500px"></iframe>`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
