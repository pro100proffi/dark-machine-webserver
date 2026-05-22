document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(function (link) {
        const href = link.getAttribute("href");

        if (href === "/" && currentPath === "/") {
            link.classList.add("active");
        } else if (href !== "/" && currentPath === href) {
            link.classList.add("active");
        }
    });

    startCountdown();
    loadCgiBlock();
});

function startCountdown() {
    const targetDate = new Date("2026-06-06T00:00:00").getTime();

    const daysElement = document.getElementById("days");
    const hoursElement = document.getElementById("hours");
    const minutesElement = document.getElementById("minutes");
    const secondsElement = document.getElementById("seconds");

    if (!daysElement || !hoursElement || !minutesElement || !secondsElement) {
        return;
    }

    function updateCountdown() {
        const now = new Date().getTime();
        const difference = targetDate - now;

        if (difference <= 0) {
            daysElement.textContent = "00";
            hoursElement.textContent = "00";
            minutesElement.textContent = "00";
            secondsElement.textContent = "00";
            return;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor(
            (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        const minutes = Math.floor(
            (difference % (1000 * 60 * 60)) / (1000 * 60)
        );
        const seconds = Math.floor(
            (difference % (1000 * 60)) / 1000
        );

        daysElement.textContent = String(days).padStart(2, "0");
        hoursElement.textContent = String(hours).padStart(2, "0");
        minutesElement.textContent = String(minutes).padStart(2, "0");
        secondsElement.textContent = String(seconds).padStart(2, "0");
    }

    updateCountdown();

    setInterval(updateCountdown, 1000);
}

function loadCgiBlock() {
    const cgiContent = document.getElementById("cgi-content");

    if (!cgiContent) {
        return;
    }

    fetch("/cgi-bin/countdown_info.py")
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Ошибка загрузки CGI");
            }

            return response.text();
        })
        .then(function (html) {
            cgiContent.innerHTML = html;
            cgiContent.classList.remove("cgi-loading");
        })
        .catch(function () {
            cgiContent.innerHTML = "Не удалось загрузить CGI-блок.";
            cgiContent.classList.add("cgi-error");
        });
}