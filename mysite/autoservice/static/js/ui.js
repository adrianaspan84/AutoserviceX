document.addEventListener("DOMContentLoaded", function () {
    // Bootstrap toasts
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.map(function (toastEl) {
        const t = new bootstrap.Toast(toastEl, {delay: 4000});
        t.show();
    });

    // Burger meniu
    const burger = document.getElementById("navBurger");
    const navLinks = document.getElementById("navLinks");
    if (burger && navLinks) {
        burger.addEventListener("click", () => {
            navLinks.classList.toggle("nav-open");
        });
    }

    // Dark / Light režimas
    const rootHtml = document.documentElement;
    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    const savedTheme = localStorage.getItem("theme") || "dark";
    setTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const current = rootHtml.getAttribute("data-theme") === "dark" ? "light" : "dark";
            setTheme(current);
            localStorage.setItem("theme", current);
        });
    }

    function setTheme(mode) {
        rootHtml.setAttribute("data-theme", mode);
        if (themeIcon) {
            if (mode === "dark") {
                themeIcon.classList.remove("fa-sun");
                themeIcon.classList.add("fa-moon");
            } else {
                themeIcon.classList.remove("fa-moon");
                themeIcon.classList.add("fa-sun");
            }
        }
    }
});
