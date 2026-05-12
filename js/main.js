// =========================
// NAVBAR SCROLL EFFECT
// =========================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    navbar.classList.toggle(
        "navbar-scrolled",
        window.scrollY > 50
    );

});

// =========================
// SCROLL TO TOP BUTTON
// =========================

const scrollTopBtn =
    document.getElementById("scrollTopBtn");

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        scrollTopBtn.style.display = "block";

    }

    else {

        scrollTopBtn.style.display = "none";

    }

});

scrollTopBtn.addEventListener("click", () => {

    window.scrollTo({

        top: 0,
        behavior: "smooth"

    });

});

// =========================
// WEBSITE LOADED
// =========================

console.log("CampusFind Loaded Successfully");