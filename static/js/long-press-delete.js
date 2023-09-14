
function handleDelete() {
    const deleteButton = document.getElementById("delete-button");
    const countdownText = document.getElementById("delete-button-text");

    if (deleteButton && countdownText) {
        let countdown = 3;
        let timer;

        function resetCountdown() {
            clearInterval(timer);
            countdownText.textContent = "Delete";
            countdown = 3;
        }

        function startCountdown() {
            timer = setInterval(function() {
                countdownText.textContent = `Deleting in ${countdown}...`;
                countdown--;

                if (countdown < 0) {
                    clearInterval(timer);
                    countdownText.textContent = `Success`;
                    countdown = 3;
                    htmx.trigger("#deleteEvent", "deleteConfirmed");
                }
            }, 1000);
        }

        deleteButton.addEventListener("mousedown", function() {
            countdownText.textContent = `Hold to confirm`;
            startCountdown();
        });

        deleteButton.addEventListener("mouseup", resetCountdown);
        deleteButton.addEventListener("mouseleave", resetCountdown);
    }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function() {
    handleDelete();
});

document.addEventListener("htmx:afterSettle", function() {
    handleDelete();
});

// Initialize for modal
if (document.getElementById('gemstoneModal')) {
    document.addEventListener("htmx:afterSettle", function() {
        initializeImagePreview();
    });
}
