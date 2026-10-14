/* =============================================
   AGRIMITRA AI - HISTORY PAGE
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const table = document.getElementById("historyTable");
    const body = document.getElementById("historyBody");
    const emptyState = document.getElementById("emptyState");
    const loadingText = document.getElementById("loadingText");

    const PAGE_STRINGS = {
        pageTitle: "Prediction History",
        pageSubtitle: "Your past crop and fertilizer recommendations.",
        thTime: "Date & Time",
        thCrop: "Crop",
        thFert: "Fertilizer",
        thLang: "Language",
        empty: "No predictions yet. Use the Crop or Fertilizer pages to get your first recommendation.",
        emptyCta: "Go to Crop Recommendation"
    };

    const LANG_NAMES = ["English", "Kannada", "Hindi", "Telugu", "Tamil"];
    const LANG_CODES = ["en", "kn", "hi", "te", "ta"];

    async function loadHistory() {
        try {
            const resp = await fetch("/api/history");
            const data = await resp.json();

            loadingText.classList.add("hidden");

            if (!data.success || !data.history.length) {
                showEmpty();
                return;
            }

            renderTable(data.history);
        } catch (err) {
            console.error(err);
            loadingText.innerHTML = '<p style="color:var(--c-error-dark);margin:0;">Unable to load history.</p>';
            loadingText.classList.remove("hidden");
        }
    }

    function showEmpty() {
        emptyState.classList.remove("hidden");
        applyPageLanguage(getSavedLanguage());
    }

    function renderTable(items) {
        lastItems = items;
        table.classList.remove("hidden");
        body.innerHTML = "";
        const lang = getSavedLanguage();

        const names = [];
        const nameIndex = {};
        items.forEach(function (item) {
            [item.predicted_crop, item.recommended_fertilizer].forEach(function (n) {
                if (n && nameIndex[n] === undefined) {
                    nameIndex[n] = names.length;
                    names.push(n);
                }
            });
        });

        NLP.translate(names.concat(LANG_NAMES), lang).then(function (translated) {
            const translatedNames = {};
            names.forEach(function (n, i) { translatedNames[n] = translated[i]; });
            const langNames = translated.slice(names.length);

            for (const item of items) {
                const tr = document.createElement("tr");

                const tdTime = document.createElement("td");
                tdTime.textContent = item.created_at;
                tr.appendChild(tdTime);

                const tdCrop = document.createElement("td");
                if (item.predicted_crop) {
                    const badge = document.createElement("span");
                    badge.className = "badge";
                    badge.textContent = translatedNames[item.predicted_crop] +
                        (item.crop_confidence != null ? " (" + Math.round(item.crop_confidence * 100) + "%)" : "");
                    tdCrop.appendChild(badge);
                } else {
                    tdCrop.textContent = "-";
                }
                tr.appendChild(tdCrop);

                const tdFert = document.createElement("td");
                if (item.recommended_fertilizer) {
                    const badge = document.createElement("span");
                    badge.className = "badge fert";
                    badge.textContent = translatedNames[item.recommended_fertilizer] +
                        (item.fertilizer_confidence != null ? " (" + Math.round(item.fertilizer_confidence * 100) + "%)" : "");
                    tdFert.appendChild(badge);
                } else {
                    tdFert.textContent = "-";
                }
                tr.appendChild(tdFert);

                const idx = LANG_CODES.indexOf(item.language);
                const tdLang = document.createElement("td");
                tdLang.textContent = idx >= 0 ? langNames[idx] : item.language;
                tr.appendChild(tdLang);

                body.appendChild(tr);
            }
        });
    }

    function applyPageLanguage(lang) {
        return NLP.applyTo(lang, PAGE_STRINGS).then(function () {
            if (lastItems && !table.classList.contains("hidden")) {
                renderTable(lastItems);
            }
        });
    }

    let lastItems = null;

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    loadHistory();

    applyPageLanguage(getSavedLanguage());
});
