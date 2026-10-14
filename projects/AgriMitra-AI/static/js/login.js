// ------------------------------
// TRANSLATIONS
// ------------------------------

const lang = {

en:{
title:"AgriMitra AI",
tagline:"Multilingual Smart Farming Assistant",
userid:"Enter User ID",
password:"Enter Password",
login:"LOGIN",
forgot:"Forgot Password?",
register:"Register",
invalid:"Invalid User ID or Password"
},

kn:{
title:"ಆಗ್ರಿಮಿತ್ರ AI",
tagline:"ಬಹುಭಾಷಾ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",
userid:"ಬಳಕೆದಾರರ ಗುರುತು",
password:"ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ",
login:"ಲಾಗಿನ್",
forgot:"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
register:"ನೋಂದಣಿ",
invalid:"ತಪ್ಪಾದ ಬಳಕೆದಾರರ ಗುರುತು ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್"
},

hi:{
title:"एग्रीमित्र AI",
tagline:"बहुभाषी स्मार्ट कृषि सहायक",
userid:"यूज़र आईडी दर्ज करें",
password:"पासवर्ड दर्ज करें",
login:"लॉगिन",
forgot:"पासवर्ड भूल गए?",
register:"रजिस्टर",
invalid:"गलत यूज़र आईडी या पासवर्ड"
},

te:{
title:"అగ్రిమిత్ర AI",
tagline:"బహుభాషా స్మార్ట్ వ్యవసాయ సహాయకుడు",
userid:"యూజర్ ఐడి నమోదు చేయండి",
password:"పాస్‌వర్డ్ నమోదు చేయండి",
login:"లాగిన్",
forgot:"పాస్‌వర్డ్ మర్చిపోయారా?",
register:"నమోదు",
invalid:"తప్పు యూజర్ ఐడి లేదా పాస్‌వర్డ్"
},

ta:{
title:"அக்ரிமித்ரா AI",
tagline:"பன்மொழி ஸ்மார்ட் வேளாண் உதவியாளர்",
userid:"பயனர் ஐடியை உள்ளிடவும்",
password:"கடவுச்சொல்லை உள்ளிடவும்",
login:"உள்நுழை",
forgot:"கடவுச்சொல் மறந்துவிட்டதா?",
register:"பதிவு செய்யவும்",
invalid:"தவறான பயனர் ஐடி அல்லது கடவுச்சொல்"
}

};

// ------------------------------
// LANGUAGE CHANGE
// ------------------------------

const language = document.getElementById("language");

language.addEventListener("change", function () {
    const l = lang[this.value] || lang.en;
    document.getElementById("title").innerHTML = l.title;
    document.getElementById("tagline").innerHTML = l.tagline;
    document.getElementById("userid").placeholder = l.userid;
    document.getElementById("password").placeholder = l.password;
    document.getElementById("loginBtn").innerHTML = l.login;
    document.getElementById("forgot").innerHTML = l.forgot;
    document.getElementById("register").innerHTML = l.register;
    localStorage.setItem("language", this.value);
});

// ------------------------------
// LOAD SAVED / SELECTED LANGUAGE
// ------------------------------

window.onload = function () {
    let saved = localStorage.getItem("language");
    const urlLang = new URLSearchParams(window.location.search).get("lang");
    if (urlLang) saved = urlLang;
    if (saved && lang[saved]) {
        language.value = saved;
        language.dispatchEvent(new Event("change"));
    }
};

// ------------------------------
// PASSWORD SHOW/HIDE
// ------------------------------

const eye = document.getElementById("eye");
const password = document.getElementById("password");

eye.onclick = function () {
    if (password.type === "password") {
        password.type = "text";
        eye.classList.replace("fa-eye", "fa-eye-slash");
    } else {
        password.type = "password";
        eye.classList.replace("fa-eye-slash", "fa-eye");
    }
};

// ------------------------------
// LOGIN (authenticates with the backend)
// ------------------------------

async function login() {
    const id = document.getElementById("userid").value;
    const pass = document.getElementById("password").value;
    const current = lang[language.value] || lang.en;
    const error = document.getElementById("error");

    if (!id || !pass) {
        error.innerHTML = current.invalid;
        return;
    }

    const btn = document.getElementById("loginBtn");
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner" aria-hidden="true"></span>' + current.login;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                userid: id,
                password: pass,
                language: language.value
            })
        });
        const data = await response.json();

        if (data.success) {
            localStorage.setItem("agri_language", language.value);
            window.location.href = "/dashboard";
        } else {
            error.innerHTML = current.invalid;
        }
    } catch (err) {
        console.error(err);
        error.innerHTML = "Unable to connect to the server.";
    } finally {
        btn.disabled = false;
        btn.innerHTML = current.login;
    }
}
