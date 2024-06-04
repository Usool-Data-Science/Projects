$(document).ready(function () {
    var pdfjsLib = window['pdfjs-dist/build/pdf'];

    // Set the workerSrc property
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://mozilla.github.io/pdf.js/build/pdf.worker.js';

    $("#uploadForm").on("submit", function (e) {
        e.preventDefault();
        var file = document.getElementById('pdfFile').files[0];
        if (file && file.type === 'application/pdf') {
            var fileReader = new FileReader();
            fileReader.onload = function () {
                var typedarray = new Uint8Array(this.result);

                pdfjsLib.getDocument(typedarray).promise.then(function (pdf) {
                    // Get first page
                    pdf.getPage(1).then(function (page) {
                        var scale = 1.5;
                        var viewport = page.getViewport({ scale: scale });

                        // Prepare canvas using PDF page dimensions
                        var canvas = document.getElementById('pdfCanvas');
                        var context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        // Render PDF page into canvas context
                        var renderContext = {
                            canvasContext: context,
                            viewport: viewport
                        };
                        page.render(renderContext);
                    });
                });
            };
            fileReader.readAsArrayBuffer(file);
            $("#pdfPreview").show();
        } else {
            alert("Please select a valid PDF file.");
        }
    });
});
