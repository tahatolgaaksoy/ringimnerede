document.addEventListener('DOMContentLoaded', (event) => {
    const popup = document.getElementById("popup");
    const popupButton = document.getElementById("popupButton");
    const closeButton = document.getElementsByClassName("close")[0];

    popupButton.onclick = function() {
        popup.style.display = "block";
    }

    closeButton.onclick = function() {
        popup.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == popup) {
            popup.style.display = "none";
        }
    }
});
