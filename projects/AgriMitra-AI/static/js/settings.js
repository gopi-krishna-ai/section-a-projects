/* =============================================
   AGRIMITRA AI - SETTINGS PAGE
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("settingsForm");
    const errorBox = document.getElementById("errorBox");
    const savedBox = document.getElementById("savedBox");

    const serverLang = (typeof getSavedLanguage === "function") ? getSavedLanguage() : "en";
    document.getElementById("prefLanguage").value = serverLang;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        errorBox.classList.add("hidden");
        savedBox.classList.add("hidden");

        const payload = {
            language: document.getElementById("prefLanguage").value,
            current_password: document.getElementById("current_password").value,
            new_password: document.getElementById("new_password").value
        };

        if (payload.new_password && payload.new_password.length < 6) {
            errorBox.textContent = "New password must contain at least 6 characters.";
            errorBox.classList.remove("hidden");
            return;
        }

        try {
            const resp = await fetch("/api/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();

            if (!data.success) {
                errorBox.textContent = data.message || "Save failed.";
                errorBox.classList.remove("hidden");
                return;
            }

            localStorage.setItem("agri_language", payload.language);
            applySidebarLanguage(payload.language);
            const topbarSel = document.querySelector(".top-right #language");
            if (topbarSel) topbarSel.value = payload.language;
            document.getElementById("current_password").value = "";
            document.getElementById("new_password").value = "";
            savedBox.textContent = data.message;
            savedBox.classList.remove("hidden");
        } catch (err) {
            console.error(err);
            errorBox.textContent = "Unable to connect to the server.";
            errorBox.classList.remove("hidden");
        }
    });

    const PAGE_STRINGS = {
        pageTitle: "Settings",
        pageSubtitle: "Language and password preferences.",
        formTitle: "Settings",
        lblLanguage: "Preferred Language",
        pwSectionTitle: "Change Password",
        lblCurrent: "Current Password",
        lblNew: "New Password",
        leaveBlank: "Leave the password fields empty to keep your current password.",
        currentPasswordPh: "Enter current password",
        newPasswordPh: "Enter new password (min 6 characters)",
        save: "Save Settings"
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
                set("lblLanguage", t.lblLanguage);
                set("pwSectionTitle", t.pwSectionTitle);
                set("lblCurrent", t.lblCurrent);
                set("lblNew", t.lblNew);
                set("leaveBlank", t.leaveBlank);
                document.getElementById("current_password").placeholder = t.currentPasswordPh;
                document.getElementById("new_password").placeholder = t.newPasswordPh;
                document.getElementById("saveBtn").querySelector("span").textContent = t.save;
            });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    applyPageLanguage(getSavedLanguage());
});
