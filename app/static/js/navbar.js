document.addEventListener("DOMContentLoaded", () => {
    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach((item) => {
        const link = item.querySelector(".nav-link");
        const dropdown = item.querySelector(".dropdown");

        // Toggle dropdown on click for mobile
        link.addEventListener("click", (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                dropdown.style.display =
                    dropdown.style.display === "block" ? "none" : "block";
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".nav-item") && window.innerWidth <= 768) {
            document.querySelectorAll(".dropdown").forEach((dropdown) => {
                dropdown.style.display = "none";
            });
        }
    });
});