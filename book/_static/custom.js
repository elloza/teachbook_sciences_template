// Custom UI Injection (Language Switcher + PDF Button)
document.addEventListener("DOMContentLoaded", function () {
    const TEACHBOOK_VERSION = "3.0";
    if (window.TEACHBOOK_LOADED_VERSION === TEACHBOOK_VERSION) return;
    window.TEACHBOOK_LOADED_VERSION = TEACHBOOK_VERSION;

    console.log(`TeachBook v${TEACHBOOK_VERSION}: Loading UI components...`);

    // 1. Fetch Languages
    const rootPath = (typeof DOCUMENTATION_OPTIONS !== 'undefined' && DOCUMENTATION_OPTIONS.URL_ROOT) ? DOCUMENTATION_OPTIONS.URL_ROOT : './';

    const tryFetch = (path) => fetch(path).then(res => {
        if (!res.ok) throw new Error("Not found: " + path);
        return res.json();
    });

    // Try multiple paths to find languages.json:
    // 1. Via Sphinx URL_ROOT (works in most builds)
    // 2. Parent _static (for multi-language builds where page is in /es/ or /en/)
    // 3. Same-level _static (fallback)
    tryFetch(rootPath + '_static/languages.json')
        .catch(() => tryFetch('../_static/languages.json'))
        .catch(() => tryFetch('_static/languages.json'))
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

    // 3. Robust Sidebar Toggle (Manual Handler with Polling)
    // The theme's native behavior is unreliable due to ID mismatches.
    // We implement a manual toggle to guarantee functionality.
    // POLLING: We run this check multiple times to catch elements rendered late by theme JS.

    function applySidebarFix() {
        const primaryCheckbox = document.getElementById('pst-primary-sidebar-checkbox');
        // Find toggles that haven't been fixed yet
        const primaryToggles = document.querySelectorAll('label[for="__primary"]:not([data-fixed]), .primary-toggle:not([data-fixed])');

        primaryToggles.forEach(toggle => {
            console.log("TeachBook: Applying fix to primary toggle", toggle);

            primaryToggles.forEach(toggle => {
                console.log("TeachBook: Attaching desktop fix to primary toggle", toggle);

                // Mark as fixed
                toggle.setAttribute('data-fixed', 'true');

                // Do NOT remove 'for' or clone node. Let native/theme behavior persist.
                // Just ADD our listener for the desktop class toggle.
                toggle.addEventListener('click', (e) => {
                    // Do NOT prevent default or stop propagation.
                    // Let the theme handle the mobile logic.

                    // Toggle custom class for desktop support
                    // We typically only care about this on desktop, but toggling the class
                    // is harmless on mobile because our CSS is media-queried.
                    document.documentElement.classList.toggle('teachbook-sidebar-hidden');
                    console.log("TeachBook: Toggled 'teachbook-sidebar-hidden'");
                });
            });
        });

        // Secondary sidebar (if needed, same logic)
        const secondaryCheckbox = document.getElementById('pst-secondary-sidebar-checkbox');
        const secondaryToggles = document.querySelectorAll('label[for="__secondary"]:not([data-fixed]), .secondary-toggle:not([data-fixed])');

        secondaryToggles.forEach(toggle => {
            console.log("TeachBook: Applying fix to secondary toggle", toggle);
            secondaryToggles.forEach(toggle => {
                console.log("TeachBook: Attaching fix to secondary toggle", toggle);
                toggle.setAttribute('data-fixed', 'true');
                // Do NOT clone or strip. Just add listener if we needed custom logic.
                // Currently we don't need custom logic for secondary, as it usually works fine?
                // But if we wanted to be safe, we could add logic here.

                // For now, removing the cloneNode is the most important part to restore mobile.
            });
        });
    }

    // Run immediately
    applySidebarFix();

    // Re-run periodically to catch late-loading elements
    const intervalId = setInterval(applySidebarFix, 500);

    // Stop polling after 5 seconds to save resources
    setTimeout(() => clearInterval(intervalId), 5000);
});

function injectLanguageSwitcher(languages, rootPath) {
    const path = window.location.pathname;
    let currentLangCode = "es";
    languages.forEach(lang => {
        if (path.includes(`/${lang.code}/`)) currentLangCode = lang.code;
    });

    const dropdownHtml = `
        <div class="teachbook-lang-container">
            <button class="btn btn-sm teachbook-lang-btn dropdown-toggle" 
                    type="button" 
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    title="Change Language / Cambiar Idioma">
                <i class="fa-solid fa-language"></i>
                <span class="lang-text">${currentLangCode.toUpperCase()}</span>
            </button>
            <ul class="teachbook-lang-dropdown">
                ${languages.map(l => {
        // Use Sphinx's calculated root path to ensure we always get back to the project root
        // regardless of current depth.
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
