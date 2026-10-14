// ------------------------------
// SPLASH SCREEN - auto redirect to login
// ------------------------------

let redirectDone = false;

function goToLogin() {
    if (redirectDone) return;
    redirectDone = true;

    const savedLang = localStorage.getItem("language") || "en";
    window.location.href = "/login?lang=" + savedLang;
}

window.addEventListener("load", function () {
    setTimeout(goToLogin, 3000);
});

// Click anywhere also continues
document.addEventListener("click", goToLogin);
