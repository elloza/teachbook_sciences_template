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

    // 3. Fix Sidebar Toggle ID mismatch (Theme regression)
    const primaryCheckbox = document.getElementById('pst-primary-sidebar-checkbox');
    const secondaryCheckbox = document.getElementById('pst-secondary-sidebar-checkbox');

    document.querySelectorAll('label.sidebar-toggle').forEach(label => {
        const forAttr = label.getAttribute('for');
        if ((forAttr === '__primary' || label.classList.contains('primary-toggle')) && primaryCheckbox) {
            console.log("TeachBook: Fixing primary toggle label.");
            label.setAttribute('for', primaryCheckbox.id);
            // Stronger listener to override any theme-level event blocking
            label.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log("TeachBook: Direct toggle click handled.");
                if (primaryCheckbox) {
                    primaryCheckbox.checked = !primaryCheckbox.checked;
                    primaryCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        } else if ((forAttr === '__secondary' || label.classList.contains('secondary-toggle')) && secondaryCheckbox) {
            console.log("TeachBook: Fixing secondary toggle label.");
            label.setAttribute('for', secondaryCheckbox.id);
            label.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log("TeachBook: Secondary toggle click handled.");
                if (secondaryCheckbox) {
                    secondaryCheckbox.checked = !secondaryCheckbox.checked;
                    secondaryCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        }
    });
});

function injectLanguageSwitcher(languages, rootPath) {
    // In our standalone build structure:
    // /index.html (redirect)
    // /es/intro.html
    // /en/intro.html

    // We want to link to ../{code}/intro.html

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
        // Link to the relative sibling directory
        const targetUrl = `../${l.code}/intro.html`;
        return `
                    <li>
                        <a href="${targetUrl}" class="dropdown-item ${l.code === currentLangCode ? 'active' : ''}">
                            ${l.name}
                        </a>
                    </li>
                `}).join('')}
            </ul>
        </div>
    `;

    const header = document.querySelector(".article-header-buttons");
    if (header) {
        const div = document.createElement("div");
        div.innerHTML = dropdownHtml.trim();
        const switcherElement = div.firstChild;
        header.prepend(switcherElement);

        // Dropdown handled by CSS hover for better consistency
        // btn.onclick = (e) => { ... }
    }
}

function injectPDFButton(rootPath) {
    const sidebar = document.querySelector(".bd-sidebar-primary");
    if (sidebar) {
        if (document.getElementById("custom-pdf-btn")) return;

        // Detect current language from path
        let lang = window.location.pathname.includes("/en/") ? "en" : "es";

        // In standalone build, _static is at the root of the language folder
        // So from any page, the relative path to _static is stored in rootPath (DOCUMENTATION_OPTIONS.URL_ROOT)
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
