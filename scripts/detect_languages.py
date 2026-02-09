import os
import json

# Configuration
BOOK_DIR = "book"
STATIC_DIR = os.path.join(BOOK_DIR, "_static")
OUTPUT_FILE = os.path.join(STATIC_DIR, "languages.json")

# Map of ISO codes to names and flags
# Add more as needed
LANG_MAP = {
    "es": {"name": "Español", "flag": "🇪🇸"},
    "en": {"name": "English", "flag": "🇬🇧"},
    "fr": {"name": "Français", "flag": "🇫🇷"},
    "pt": {"name": "Português", "flag": "🇵🇹"},
    "it": {"name": "Italiano", "flag": "🇮🇹"},
    "de": {"name": "Deutsch", "flag": "🇩🇪"},
    "ca": {"name": "Català", "flag": "🏴"},
    "eu": {"name": "Euskara", "flag": "🏴"},
    "gl": {"name": "Galego", "flag": "🏴"},
}

def detect_and_save_languages():
    """
    Scans BOOK_DIR for 2-letter directories, matches them with LANG_MAP,
    and saves the list to languages.json in STATIC_DIR.
    """
    if not os.path.exists(BOOK_DIR):
        print(f"❌ Error: {BOOK_DIR} not found.")
        return

    # Find all 2-letter directories in book/
    found_langs = []
    try:
        entries = os.listdir(BOOK_DIR)
        for entry in entries:
            full_path = os.path.join(BOOK_DIR, entry)
            if os.path.isdir(full_path) and len(entry) == 2:
                # It's a language folder
                lang_info = LANG_MAP.get(entry, {"name": entry.upper(), "flag": "🌐"})
                found_langs.append({
                    "code": entry,
                    "name": lang_info["name"],
                    "flag": lang_info["flag"]
                })
    except Exception as e:
        print(f"❌ Error scanning languages: {e}")
        return

    # Sort by code (or prioritize 'es'/'en' if desired)
    found_langs.sort(key=lambda x: x['code'])

    # Ensure output dir exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    # Write JSON
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(found_langs, f, ensure_ascii=False, indent=2)
        print(f"✅ Idiomas detectados: {[l['code'] for l in found_langs]}")
        print(f"📄 Guardado en: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error writing languages.json: {e}")

if __name__ == "__main__":
    detect_and_save_languages()
