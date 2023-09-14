function handleDelete() {
    const deleteButton = document.getElementById("delete-button");
    const countdownText = document.getElementById("delete-button-text");
    let countdown = 3;
    let timer;

    function startCountdown() {
        timer = setInterval(function() {
            countdownText.textContent = `Deleting in ${countdown}...`;
            countdown--;

            if (countdown < 0) {
                clearInterval(timer);
                countdownText.textContent = `Success`;
                countdown = 3;  // Reset the countdown, no need to manually trigger here
            }
        }, 1000);
    }

    deleteButton.addEventListener("mousedown", function() {
        countdownText.textContent = `Hold to confirm`;
        startCountdown();
    });

    deleteButton.addEventListener("mouseup", function() {
        clearInterval(timer);
        countdownText.textContent = "Delete";
        countdown = 3; // Reset the countdown
    });
}

document.addEventListener("DOMContentLoaded", function() {
    handleDelete();
});
