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

    /* 
    // 3. Fix Sidebar Toggle ID mismatch (Theme regression) - EXPERIMENTAL
    // Removing custom interference to let the theme handle events natively.
    /*
    const primaryCheckbox = document.getElementById('pst-primary-sidebar-checkbox');
    const secondaryCheckbox = document.getElementById('pst-secondary-sidebar-checkbox');

    document.querySelectorAll('label.sidebar-toggle').forEach(label => {
        const forAttr = label.getAttribute('for');

        // Fix for Primary Sidebar (Left)
        if ((forAttr === '__primary' || label.classList.contains('primary-toggle')) && primaryCheckbox) {
            if (label.getAttribute('for') !== primaryCheckbox.id) {
                console.log("TeachBook: Fixing primary toggle label.");
                label.setAttribute('for', primaryCheckbox.id);
            }
        }
        // Fix for Secondary Sidebar (Right)
        else if ((forAttr === '__secondary' || label.classList.contains('secondary-toggle')) && secondaryCheckbox) {
            if (label.getAttribute('for') !== secondaryCheckbox.id) {
                console.log("TeachBook: Fixing secondary toggle label.");
                label.setAttribute('for', secondaryCheckbox.id);
            }
        }
    });
    */
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
