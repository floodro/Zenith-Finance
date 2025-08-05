setTimeout(function() {
        var messages = document.getElementById("messages");
        if (messages) {
            messages.style.transition = "opacity 1s ease-out";
            messages.style.opacity = "0";
            setTimeout(function() {
                messages.style.display = "none";
            }, 1000);
        }
    }, 3000);