
function initializeImagePreview() {
    const input = document.querySelector('input[type=file]');
    const label = document.querySelector('.gemstone-file-label');
    const uploadIcon = document.querySelector('#upload-icon');

    if (!input || !label || !uploadIcon) {
        return; // Exit early if any of the elements don't exist
    }

    input.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadIcon.style.display = 'none';

                const existingImg = document.getElementById('image-preview');
                if (existingImg) existingImg.remove();

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

// Initialize on page load
document.addEventListener("DOMContentLoaded", function() {
    initializeImagePreview();
});

document.addEventListener("htmx:afterSettle", function() {
    initializeImagePreview();
});

// Initialize for modal
if (document.getElementById('gemstoneModal')) {
    document.addEventListener("htmx:afterSettle", function() {
        initializeImagePreview();
    });
}
