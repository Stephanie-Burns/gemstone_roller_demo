document.addEventListener("DOMContentLoaded", function() {
    function initializeImagePreview() {
        const input = document.querySelector('input[type=file]');
        const label = document.querySelector('.gemstone-file-label');
        const uploadIcon = document.querySelector('#upload-icon'); // Modified selector
        // const labelText = document.querySelector('#label-text');  // Modified selector

        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Remove or hide existing icon and text
                    if (uploadIcon) uploadIcon.style.display = 'none';
                    // if (labelText) labelText.style.display = 'none'; // Modified reference

                    // Remove existing preview image if any
                    const existingImg = document.getElementById('image-preview');
                    if (existingImg) existingImg.remove();

                    // Create and add the new preview image
                    const img = document.createElement('img');
                    img.setAttribute('id', 'image-preview');
                    img.setAttribute('src', e.target.result);
                    img.style.width = '60px';
                    img.style.height = '60px';
                    label.appendChild(img);
                }
                reader.readAsDataURL(file);
            }
        });
    }
    initializeImagePreview();
});
