/* =============================================
   AGRIMITRA AI - NLP TRANSLATION HELPER
   Every UI string and domain term is machine
   translated by the server's NLP engine
   (/translate). No manual translations are
   hardcoded anywhere in the frontend.

   Results are cached in memory + localStorage so
   repeat language switches are instant.
   ============================================= */

const NLP = (function () {
    const KEY_SEP = "\u0001";
    const STORE_KEY = "agri_nlp_cache";

    let cache = {};
    let inflight = {};
    let saving = false;

    function loadStore() {
        try {
            const raw = localStorage.getItem(STORE_KEY);
            if (raw) cache = JSON.parse(raw) || {};
        } catch (e) {
            cache = {};
        }
    }

    function saveStore() {
        if (saving) return;
        saving = true;
        setTimeout(function () {
            saving = false;
            try {
                localStorage.setItem(STORE_KEY, JSON.stringify(cache));
            } catch (e) {
                // storage full or unavailable - keep in-memory cache only
            }
        }, 0);
    }

    function cacheKey(lang, text) {
        return lang + KEY_SEP + text;
    }

    function getCached(lang, text) {
        return cache[cacheKey(lang, text)];
    }

    function setCached(lang, text, value) {
        cache[cacheKey(lang, text)] = value;
        saveStore();
    }

    function translate(texts, lang) {
        const single = !Array.isArray(texts);
        const list = single ? [String(texts)] : texts.slice();

        if (lang === "en" || !lang) {
            return Promise.resolve(single ? list[0] : list);
        }

        const out = [];
        const missing = [];

        list.forEach(function (t, i) {
            const cached = getCached(lang, t);
            if (cached !== undefined) {
                out[i] = cached;
            } else {
                missing.push({ t: t, i: i });
            }
        });

        if (!missing.length) {
            return Promise.resolve(single ? out[0] : out);
        }

        const finish = function (translated) {
            missing.forEach(function (m, idx) {
                const val = (translated[idx] != null && String(translated[idx]).trim() !== "")
                    ? String(translated[idx])
                    : m.t;
                setCached(lang, m.t, val);
                out[m.i] = val;
            });
            return single ? out[0] : out;
        };

        const doFetch = function () {
            return fetch("/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    texts: missing.map(function (m) { return m.t; }),
                    language: lang
                })
            })
                .then(function (resp) { return resp.json(); })
                .then(function (data) {
                    return (data && Array.isArray(data.translations)) ? data.translations : [];
                })
                .catch(function () {
                    return missing.map(function (m) { return m.t; });
                });
        };

        // Coalesce concurrent requests for the same language into one fetch.
        const pending = inflight[lang];
        if (pending) {
            return pending.then(function () {
                // some of our texts may already be translated by that request
                const stillMissing = [];
                missing.forEach(function (m) {
                    const c = getCached(lang, m.t);
                    if (c !== undefined) out[m.i] = c;
                    else stillMissing.push(m);
                });
                if (!stillMissing.length) {
                    return single ? out[0] : out;
                }
                return doFetch().then(function (translated) {
                    stillMissing.forEach(function (m, idx) {
                        const val = (translated[idx] != null && String(translated[idx]).trim() !== "")
                            ? String(translated[idx])
                            : m.t;
                        setCached(lang, m.t, val);
                        out[m.i] = val;
                    });
                    return single ? out[0] : out;
                });
            });
        }

        const p = doFetch().then(finish).then(function (result) {
            delete inflight[lang];
            return result;
        });
        inflight[lang] = p;
        return p;
    }

    /* Translate a mapping { elementId: englishText } and set the text of each element.
       Cached strings apply immediately; the rest fill in when the API responds. */
    function applyTo(lang, mapping) {
        const ids = Object.keys(mapping);
        ids.forEach(function (id) {
            const cached = getCached(lang, mapping[id]);
            if (cached !== undefined) {
                const el = document.getElementById(id);
                if (el) el.textContent = cached;
            }
        });
        return translate(ids.map(function (id) { return mapping[id]; }), lang)
            .then(function (translated) {
                ids.forEach(function (id, i) {
                    const el = document.getElementById(id);
                    if (el) el.textContent = translated[i];
                });
            });
    }

    /* Translate the text of every <option> in a <select>.
       The original English text is kept in data-en so re-translation always
       starts from English (never from a previously translated string). */
    function localizeOptions(lang, selectEl) {
        if (!selectEl || !selectEl.options) return Promise.resolve();
        const options = Array.prototype.slice.call(selectEl.options);
        const texts = options.map(function (o) {
            if (!o.hasAttribute("data-en")) {
                o.setAttribute("data-en", o.textContent);
            }
            return o.getAttribute("data-en");
        });
        return translate(texts, lang).then(function (translated) {
            options.forEach(function (o, i) { o.textContent = translated[i]; });
        });
    }

    loadStore();
    return { translate: translate, applyTo: applyTo, localizeOptions: localizeOptions };
})();
