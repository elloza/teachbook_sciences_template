// Custom Sidebar Buttons Injection (PDF + Dynamic Languages)
document.addEventListener("DOMContentLoaded", function () {
    // Nuclear Option: Global Flag to prevent multiple executions
    if (window.TEACHBOOK_LOADED_VERSION) {
        console.log("TeachBook: Script version " + window.TEACHBOOK_LOADED_VERSION + " already ran. Skipping.");
        return;
    }
    window.TEACHBOOK_LOADED_VERSION = "2.1"; // Updated version

    console.log("TeachBook v2.1: Loading...");

    // 0. Prevent duplicate injection (Idempotency check)
    // We use a unique ID on the wrapper to ensure we can find and remove the whole block consistently.
    const WRAPPER_ID = "teachbook-sidebar-buttons-wrapper";
    const existingWrapper = document.getElementById(WRAPPER_ID);

    if (existingWrapper) {
        console.log("TeachBook: Removing existing wrapper to prevent duplicates.");
        existingWrapper.remove();
    }

    // Fallback: cleaning up potential debris from previous versions of the script
    const oldDebris = document.querySelectorAll(".custom-sidebar-buttons");
    oldDebris.forEach(el => {
        // Only remove if it's not inside our new wrapper (which doesn't exist yet, so remove all)
        el.remove();
        // Also remove parent if it's an empty div we created previously? 
        // Hard to identify, but the new ID system will prevent future debris.
        if (el.parentElement && el.parentElement.tagName === 'DIV' && !el.parentElement.id && el.parentElement.children.length === 0) {
            el.parentElement.remove();
        }
    });

    // 1. Fetch available languages with robust fallback
    // Use DOCUMENTATION_OPTIONS.URL_ROOT if available to handle relative paths correctly
    const rootPath = (typeof DOCUMENTATION_OPTIONS !== 'undefined' && DOCUMENTATION_OPTIONS.URL_ROOT) ? DOCUMENTATION_OPTIONS.URL_ROOT : '';
    const jsonPath = rootPath + '_static/languages.json';

    fetch(jsonPath)
        .then(response => {
            if (!response.ok) throw new Error("Languages JSON missing at " + jsonPath);
            return response.json();
        })
        .catch(err => {
            console.warn("TeachBook: Could not load languages.json", err);
            // Fallback default - INCLUDING ENGLISH to prevent filtering failure if fetch fails
            return [
                { code: "es", name: "Español", flag: "🇪🇸" },
                { code: "en", name: "English", flag: "🇬🇧" }
            ];
        })
        .then(languages => {
            console.log("TeachBook: Languages loaded:", languages);
            injectButtons(languages, WRAPPER_ID, rootPath);
        });
});

function injectButtons(languages, wrapperId, rootPath) {
    // Detect current language from URL
    const path = window.location.pathname;
    let currentLangCode = 'es'; // Default

    languages.forEach(lang => {
        if (path.includes(`/${lang.code}/`)) {
            currentLangCode = lang.code;
        }
    });

    // Build language options HTML
    let langOptionsHtml = '';
    languages.forEach(lang => {
        const isActive = lang.code === currentLangCode ? 'active' : '';
        // Link logic: go to root then to lang folder
        // Only works if structure is consistent
        let link = (isActive) ? '#' : rootPath + lang.code + '/intro.html';

        // If we are on a page that exists in the other language, ideally we link there.
        // But for now, linking to repo root/lang/intro.html is safer than 404s.

        langOptionsHtml += `
            <a href="${link}" class="lang-option ${isActive}">
                <span class="flag">${lang.flag}</span> ${lang.name}
            </a>
        `;
    });

    // 2. Define HTML
    const pdfPath = rootPath + '_static/teachbook.pdf';

    const buttonsHtml = `
        <div class="custom-sidebar-buttons">
            <!-- PDF Download Button -->
            <a href="${pdfPath}" class="sidebar-btn pdf-btn" id="download-pdf-btn" download title="Descargar libro en PDF">
                <i class="fa-solid fa-file-pdf"></i>
                <span>Descargar PDF</span>
            </a>
            
            <!-- Language Switcher (Dynamic Dropdown) -->
            <div class="language-dropdown">
                <button class="sidebar-btn lang-btn" onclick="toggleLanguageMenu()">
                    <i class="fa-solid fa-globe"></i>
                    <span>Idiomas / Languages</span>
                    <i class="fa-solid fa-chevron-down arrow-icon"></i>
                </button>
                <div id="lang-menu" class="lang-menu-content">
                    ${langOptionsHtml}
                </div>
            </div>
        </div>
    `;

    // 3. Inject into Sidebar
    const logoContainer = document.querySelector(".navbar-brand");
    const sidebarStart = document.querySelector(".sidebar-primary-items__start");

    // Create wrapper with unique ID
    const container = document.createElement("div");
    container.id = wrapperId;
    container.innerHTML = buttonsHtml;

    if (logoContainer && logoContainer.parentNode) {
        logoContainer.parentNode.insertBefore(container, logoContainer.nextSibling);
    } else if (sidebarStart) {
        sidebarStart.insertBefore(container, sidebarStart.firstChild);
    }

    // 4. Attach Listeners (Graceful PDF Check)
    const pdfBtn = document.getElementById("download-pdf-btn");
    if (pdfBtn) {
        pdfBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const pdfUrl = this.getAttribute("href");
            fetch(pdfUrl, { method: 'HEAD' })
                .then(res => {
                    if (res.ok) {
                        window.location.href = pdfUrl;
                    } else {
                        alert("⚠️ El archivo PDF no se ha generado todavía.\n\nPor favor, ejecuta la tarea 'Exportar PDF' en el terminal para crearlo.");
                    }
                })
                .catch(err => {
                    window.location.href = pdfUrl;
                });
        });
    }

    // 5. Smart Filtering (Hide irrelevant language sections)
    filterSidebar(languages);
}

function filterSidebar(languages) {
    // Determine current language
    const path = window.location.pathname;
    let currentLang = 'es'; // Default
    languages.forEach(lang => {
        if (path.includes(`/${lang.code}/`)) {
            currentLang = lang.code;
        }
    });

    console.log(`TeachBook: Filtering sidebar for language '${currentLang}'...`);

    // Select all captions and their following lists
    // Jupyter Book / Sphinx usually renders captions as <p class="caption">...
    const captions = document.querySelectorAll("p.caption");

    captions.forEach(caption => {
        const nextUl = caption.nextElementSibling;
        if (nextUl && nextUl.tagName === 'UL') {
            const links = nextUl.querySelectorAll("a");
            let hasOtherLangLinks = false;
            let hasCurrentLangLinks = false;

            for (let link of links) {
                const href = link.getAttribute("href");
                if (!href) continue;

                // Normalize href (remove ../ and leading /)
                const normalizedHref = href.replace(/^(\.\.\/)+/, '').replace(/^\//, '');

                for (let lang of languages) {
                    // If href starts with "lang/" or is exactly "lang/" or "lang.html"
                    if (normalizedHref.startsWith(lang.code + '/') || normalizedHref === lang.code + '.html') {
                        if (lang.code === currentLang) {
                            hasCurrentLangLinks = true;
                        } else {
                            hasOtherLangLinks = true;
                        }
                    }
                }
            }

            // If a section is clearly marked for ANOTHER language and has no links for current, hide it.
            // Also check the caption text as a fallback
            const captionText = caption.textContent.toLowerCase();
            const LangNames = languages.map(l => l.name.toLowerCase());

            let isOtherLangCaption = false;
            languages.forEach(l => {
                if (l.code !== currentLang && (captionText.includes(l.name.toLowerCase()) || captionText.includes(`(${l.code.toUpperCase()})`))) {
                    isOtherLangCaption = true;
                }
            });

            if (isOtherLangCaption || (hasOtherLangLinks && !hasCurrentLangLinks)) {
                console.log(`TeachBook: Hiding section '${caption.textContent}' (not for ${currentLang})`);
                caption.style.display = 'none';
                nextUl.style.display = 'none';
            }
        }
    });
}

window.toggleLanguageMenu = function () {
    const menu = document.getElementById("lang-menu");
    const btn = document.querySelector(".lang-btn .arrow-icon");
    if (menu) {
        const isVisible = menu.style.display === "block";
        menu.style.display = isVisible ? "none" : "block";
        if (btn) {
            btn.style.transform = isVisible ? "rotate(0deg)" : "rotate(180deg)";
        }
    }
}
