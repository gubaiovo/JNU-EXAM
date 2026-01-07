import os
import json
import re
import sys
from urllib.parse import quote
from pathlib import Path

PROJECT_ROOT = Path("/app/repo")
DATA_ROOT = PROJECT_ROOT / "data"
CONFIG_PATH = Path("/app/config/sources.json") 

IGNORES = {
    '.git', '.gitignore', '.upload_cache', 'tools', '__pycache__', 
    'README.md', 'LICENSE', 'directory_structure.json', 'upload.txt', 
    'uv.lock', 'pyproject.toml', 'main.py', '.venv', '.idea', '.vscode',
    'source_list.json', '.new_files_for_lanzou', 'bigfile', 'data'
}
SEPARATOR = "__"

def load_sources():
    if CONFIG_PATH.exists():
        print(f"检测到外部配置文件: {CONFIG_PATH}，正在加载...")
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                custom_sources = json.load(f)
                if isinstance(custom_sources, list):
                    for src in custom_sources:
                        if not src.get("key"):
                            src["key"] = src["name"].lower().replace(" ", "_") + "_url"
                    print(f"成功加载 {len(custom_sources)} 个自定义源")
                    return custom_sources
                else:
                    print("配置文件格式错误: 根对象必须是列表")
        except Exception as e:
            print(f"读取配置文件失败: {e}，回退到默认配置")

    print("使用默认源配置")
    return [
        {
            "name": "Github",
            "key": "github_raw_url",
            "base": "https://raw.githubusercontent.com/gubaiovo/JNU-EXAM/main/data",
            "json_url": "https://github.com/gubaiovo/JNU-EXAM/raw/main/directory_structure.json",
            "type": "tree",
            "enabled": True
        },
        {
            "name": "CloudFlare R2",
            "key": "cf_url",
            "base": "https://jnuexam.xyz",
            "json_url": "https://jnuexam.xyz/directory_structure.json",
            "type": "tree",
            "enabled": True
        }
    ]

SOURCES = load_sources()

def sanitize_name(name):
    name = re.sub(r'\s+', '', name)
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    while SEPARATOR in name:
        name = name.replace(SEPARATOR, "")
    return name

def get_flattened_path(rel_path):
    p = Path(rel_path)
    parts = p.parts
    sanitized_parts = [sanitize_name(p) for p in parts]
    if len(sanitized_parts) <= 1:
        return sanitized_parts[0]
    top_folder = sanitized_parts[0]
    if len(sanitized_parts) > 1:
        rest_of_path = sanitized_parts[1:]
        new_filename = SEPARATOR.join(rest_of_path)
        return f"{top_folder}/{new_filename}"
    return rel_path

def create_file_entry(name, rel_path, root_dir, sources):
    full_path = os.path.join(root_dir, rel_path)
    size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
    standard_rel_path = rel_path.replace("\\", "/")
    
    entry = {
        "name": name,
        "path": standard_rel_path,
        "size": size
    }

    for source in sources:
        if not source.get("enabled", True): continue
        key = source["key"]

        if source.get("type") == "flat":
            final_path = get_flattened_path(standard_rel_path)
        else:
            final_path = standard_rel_path
            
        encoded_path = quote(final_path)
        url = f"{source['base'].rstrip('/')}/{encoded_path}"
        entry[key] = url
            
    return entry

def generate_directory_structure(root_dir, sources, ignore_list=None):
    if ignore_list is None: ignore_list = []
    result = {"dirs": [], "files": []}
    
    for current_dir, subdirs, files in os.walk(root_dir):
        rel_dir = os.path.relpath(current_dir, root_dir)
        if rel_dir == ".": rel_dir = ""
        
        subdirs[:] = [d for d in subdirs if d not in ignore_list]
        files = [f for f in files if f not in ignore_list]
        
        if rel_dir == "":
            for file in files:
                if not any(ignore in file for ignore in ignore_list):
                    entry = create_file_entry(file, file, root_dir, sources)
                    result["files"].append(entry)
        else:
            dir_name = os.path.basename(current_dir)
            if dir_name in ignore_list: continue
            
            dir_entry = {
                "name": dir_name,
                "path": rel_dir.replace("\\", "/"),
                "files": []
            }
            
            for file in files:
                if file in ignore_list: continue
                file_rel_path = os.path.join(rel_dir, file).replace("\\", "/")
                entry = create_file_entry(file, file_rel_path, root_dir, sources)
                dir_entry["files"].append(entry)
            
            result["dirs"].append(dir_entry)
    return result

def generate_source_list_file(sources, output_path):
    source_list = {}
    for source in sources:
        if source.get("enabled", True) and source.get("json_url"):
            source_list[source["name"]] = {
                "json_url": source["json_url"],
                "file_key": source["key"]
            }
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(source_list, f, indent=4, ensure_ascii=False)
        print(f"Source List 已生成: {output_path}")
        # 打印预览
        # print(json.dumps(source_list, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Source List 生成失败: {e}")

def run():
    print("正在生成索引文件")
    target_dir = str(DATA_ROOT)
    
    output_json = PROJECT_ROOT / "directory_structure.json"
    output_source_list = PROJECT_ROOT / "source_list.json"
    
    if not os.path.exists(target_dir):
        print(f"数据目录 {target_dir} 不存在，跳过生成")
        return

    # 1. 生成目录结构 directory_structure.json
    try:
        structure = generate_directory_structure(target_dir, SOURCES, list(IGNORES))
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        print(f"Directory Structure 已生成: {output_json}")
    except Exception as e:
        print(f"JSON 生成失败: {e}")
        return

    # 2. 生成源列表 source_list.json (供下载器读取)
    generate_source_list_file(SOURCES, output_source_list)

if __name__ == "__main__":
    run()