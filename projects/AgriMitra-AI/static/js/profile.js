/* =============================================
   AGRIMITRA AI - PROFILE PAGE
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("profileForm");
    const errorBox = document.getElementById("errorBox");
    const savedBox = document.getElementById("savedBox");

    const serverLang = (typeof getSavedLanguage === "function") ? getSavedLanguage() : "en";
    document.getElementById("prefLanguage").value = serverLang;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        errorBox.classList.add("hidden");
        savedBox.classList.add("hidden");

        const payload = {
            phone: document.getElementById("phone").value,
            language: document.getElementById("prefLanguage").value
        };

        try {
            const resp = await fetch("/api/profile", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();

            if (!data.success) {
                errorBox.textContent = data.message || "Update failed.";
                errorBox.classList.remove("hidden");
                return;
            }

            localStorage.setItem("agri_language", payload.language);
            applySidebarLanguage(payload.language);
            const topbarSel = document.querySelector(".top-right #language");
            if (topbarSel) topbarSel.value = payload.language;
            savedBox.textContent = data.message;
            savedBox.classList.remove("hidden");
        } catch (err) {
            console.error(err);
            errorBox.textContent = "Unable to connect to the server.";
            errorBox.classList.remove("hidden");
        }
    });

    const PAGE_STRINGS = {
        pageTitle: "Profile",
        pageSubtitle: "Your account information.",
        formTitle: "Profile",
        lblFullname: "Full Name",
        lblUserid: "User ID",
        lblEmail: "Email",
        lblPhone: "Phone Number",
        phonePh: "Enter phone number",
        lblLanguage: "Preferred Language",
        save: "Save Changes"
    };

    function applyPageLanguage(lang) {
        return NLP.translate(Object.keys(PAGE_STRINGS).map(function (k) { return PAGE_STRINGS[k]; }), lang)
            .then(function (out) {
                const t = {};
                Object.keys(PAGE_STRINGS).forEach(function (k, i) { t[k] = out[i]; });
                const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
                set("pageTitle", t.pageTitle);
                set("pageSubtitle", t.pageSubtitle);
                set("formTitle", t.formTitle);
                set("lblFullname", t.lblFullname);
                set("lblUserid", t.lblUserid);
                set("lblEmail", t.lblEmail);
                set("lblPhone", t.lblPhone);
                set("lblLanguage", t.lblLanguage);
                document.getElementById("phone").placeholder = t.phonePh;
                document.getElementById("saveBtn").querySelector("span").textContent = t.save;
            });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    applyPageLanguage(getSavedLanguage());
});
