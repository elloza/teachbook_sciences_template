// Custom UI Injection (Language Switcher + PDF Button)
document.addEventListener("DOMContentLoaded", function () {
    const TEACHBOOK_VERSION = "3.0";
    if (window.TEACHBOOK_LOADED_VERSION === TEACHBOOK_VERSION) return;
    window.TEACHBOOK_LOADED_VERSION = TEACHBOOK_VERSION;

    console.log(`TeachBook v${TEACHBOOK_VERSION}: Loading UI components...`);

    // 1. Fetch Languages
    const rootPath = (typeof DOCUMENTATION_OPTIONS !== 'undefined' && DOCUMENTATION_OPTIONS.URL_ROOT) ? DOCUMENTATION_OPTIONS.URL_ROOT : './';

    const tryFetch = (path) => fetch(path).then(res => {
        if (!res.ok) throw new Error("Not found");
        return res.json();
    });

    // Try relative to current page first (for local dev), then root (for prod)
    tryFetch(rootPath + '_static/languages.json')
        .catch(() => tryFetch('_static/languages.json')) // fallback for root-level access or different build structs
        .then(languages => {
            if (languages.length > 1) {
                injectLanguageSwitcher(languages, rootPath);
            } else {
                console.log("TeachBook: Single language detected. Hiding switcher.");
            }
        })
        .catch(err => {
            console.log("TeachBook: Language switcher disabled (missing languages.json).");
        });

    // 2. Inject PDF Button (Always, if configured)
    injectPDFButton(rootPath);

    // 3. Robust Sidebar Toggle (Manual Handler)
    // The theme's native behavior is unreliable due to ID mismatches.
    // We implement a manual toggle to guarantee functionality.
    const primaryCheckbox = document.getElementById('pst-primary-sidebar-checkbox');

    // Find all primary toggles (desktop header icon + mobile overlay if any)
    const primaryToggles = document.querySelectorAll('label[for="__primary"], .primary-toggle');

    primaryToggles.forEach(toggle => {
        // Remove 'for' attribute to prevent browser's native confused behavior
        toggle.removeAttribute('for');

        // Clone element to strip existing listeners (if any theme listeners are causing issues)
        const newToggle = toggle.cloneNode(true);
        toggle.parentNode.replaceChild(newToggle, toggle);

        newToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            if (primaryCheckbox) {
                primaryCheckbox.checked = !primaryCheckbox.checked;
                // Dispatch change event to trigger CSS/Theme reactions
                primaryCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                console.log("TeachBook: Primary sidebar toggled manually. State:", primaryCheckbox.checked);
            }
        });
    });

    // Secondary sidebar (if needed, same logic)
    const secondaryCheckbox = document.getElementById('pst-secondary-sidebar-checkbox');
    const secondaryToggles = document.querySelectorAll('label[for="__secondary"], .secondary-toggle');

    secondaryToggles.forEach(toggle => {
        toggle.removeAttribute('for');
        // Clone to strip listeners
        const newToggle = toggle.cloneNode(true);
        toggle.parentNode.replaceChild(newToggle, toggle);

        newToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (secondaryCheckbox) {
                secondaryCheckbox.checked = !secondaryCheckbox.checked;
                secondaryCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    });
});

function injectLanguageSwitcher(languages, rootPath) {
    const path = window.location.pathname;
    let currentLangCode = "es";
    languages.forEach(lang => {
        if (path.includes(`/${lang.code}/`)) currentLangCode = lang.code;
    });

    const dropdownHtml = `
        <div class="teachbook-lang-container">
            <button class="btn btn-sm teachbook-lang-btn" 
                    type="button" 
                    title="Change Language / Cambiar Idioma">
                <i class="fa-solid fa-language"></i>
                <span class="lang-text">${currentLangCode.toUpperCase()}</span>
            </button>
            <ul class="teachbook-lang-dropdown">
                ${languages.map(l => {
        // Use Sphinx's calculated root path to ensure we always get back to the project root
        // regardless of current depth.
        const targetUrl = rootPath + `${l.code}/intro.html`;

        return `
                    <li>
                        <a href="${targetUrl}" class="dropdown-item ${l.code === currentLangCode ? 'active' : ''}">
                            ${l.name}
                        </a>
                    </li>
                    `;
    }).join('')}
            </ul>
        </div>
    `;

    const header = document.querySelector(".article-header-buttons");
    if (header) {
        const div = document.createElement("div");
        div.innerHTML = dropdownHtml.trim();
        const switcherElement = div.firstChild;
        header.prepend(switcherElement);
    }
}

function injectPDFButton(rootPath) {
    const sidebar = document.querySelector(".bd-sidebar-primary");
    if (sidebar) {
        if (document.getElementById("custom-pdf-btn")) return;

        // Detect current language from path
        let lang = window.location.pathname.includes("/en/") ? "en" : "es";

        // In standalone build, _static is at the root of the language folder
        const pdfFilename = `teachbook_${lang}.pdf`;
        const pdfUrl = rootPath + `_static/${pdfFilename}`;

        const langStrings = {
            "es": { "text": "Libro Completo (PDF)", "title": "Descargar PDF completo" },
            "en": { "text": "Complete Book (PDF)", "title": "Download complete PDF" }
        };
        const strings = langStrings[lang] || langStrings["en"];

        const btnHtml = `
            <div class="sidebar-footer-pdf">
                <div class="custom-sidebar-pdf-container">
                    <a href="${pdfUrl}" id="custom-pdf-btn" class="btn btn-sm" download title="${strings.title}">
                        <i class="fa-solid fa-file-pdf"></i>
                        <span>${strings.text}</span>
                    </a>
                </div>
            </div>
        `;

        const div = document.createElement("div");
        div.innerHTML = btnHtml.trim();
        sidebar.appendChild(div.firstChild);
    }
}
