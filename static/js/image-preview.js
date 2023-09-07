
function initializeImagePreview() {
    const input = document.querySelector('input[type=file]');
    input.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Hide the old image
                const oldImg = document.getElementById('old-image-preview');
                if (oldImg) {
                    oldImg.style.display = 'none';
                }

                // Get the preview element and set its source to the selected image
                const img = document.getElementById('image-preview');
                img.src = e.target.result;
                img.style.display = 'block';  // Make the image visible
            }
            reader.readAsDataURL(file);
        }
    });
}