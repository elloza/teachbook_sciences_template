import os
import shutil
import glob
import sys

BOOK_DIR = "book"
lang = "en"
temp_build_root = os.path.abspath(os.path.join(BOOK_DIR, f"temp_debug_{lang}"))

def debug_setup():
    print(f"🔍 Setting up debug environment for '{lang}' in {temp_build_root}")
    
    if os.path.exists(temp_build_root):
        shutil.rmtree(temp_build_root)
    os.makedirs(temp_build_root)
    
    # Copy localized content
    lang_src_dir = os.path.join(BOOK_DIR, lang)
    lang_dst_dir = os.path.join(temp_build_root, lang)
    print(f"   Copying {lang_src_dir} -> {lang_dst_dir}")
    shutil.copytree(lang_src_dir, lang_dst_dir)
    
    # Copy Config and TOC
    config_file = f"_config_{lang}.yml"
    toc_file = f"_toc_{lang}.yml"
    
    print(f"   Copying {config_file} -> _config.yml")
    shutil.copy2(os.path.join(BOOK_DIR, config_file), os.path.join(temp_build_root, "_config.yml"))
    
    print(f"   Copying {toc_file} -> _toc.yml")
    shutil.copy2(os.path.join(BOOK_DIR, toc_file), os.path.join(temp_build_root, "_toc.yml"))
    
    # INSPECTION
    print("\n🧐 INSPECTION RESULTS:")
    
    # 1. Check _toc.yml content
    toc_path = os.path.join(temp_build_root, "_toc.yml")
    with open(toc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"   📄 _toc.yml content:\n{'-'*20}\n{content}\n{'-'*20}")
    
    # 2. Check existence of referenced file
    # Extract a file path from TOC (naive parse)
    ref_file_rel = "en/01_tutorial/01_what_is_a_teachbook.md" # hardcoded from what we know
    ref_file_abs = os.path.join(temp_build_root, ref_file_rel)
    
    if os.path.exists(ref_file_abs):
        print(f"   ✅ Referenced file exists: {ref_file_rel}")
        with open(ref_file_abs, 'r', encoding='utf-8') as f:
            head = f.read(100)
        print(f"      Header: {head.splitlines()[0]}")
    else:
        print(f"   ❌ Referenced file MISSING: {ref_file_rel}")
        
    # 3. Check for Spanish Pollution
    es_file_rel = "en/01_tutorial/01_que_es_un_teachbook.md"
    es_file_abs = os.path.join(temp_build_root, es_file_rel)
    if os.path.exists(es_file_abs):
         print(f"   ⚠️ Spanish filename found in EN folder: {es_file_rel}")
    
    # 4. Check for 'es' folder
    es_folder = os.path.join(temp_build_root, "es")
    if os.path.exists(es_folder):
        print(f"   ⚠️ 'es' folder found in root!")

if __name__ == "__main__":
    debug_setup()
