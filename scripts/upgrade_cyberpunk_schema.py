import json
import re

JSON_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/src/data/games_top100.json'
JS_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/data.js'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

for g in games:
    if g["id"] == "cyberpunk-2077":
        cmd_idx = 1
        for cat in g.get("consoleCategories", []):
            for cmd in cat.get("commands", []):
                # Ensure id
                if not cmd.get("id"):
                    # create a clean slug from name en
                    en_name = cmd.get("name", {}).get("en", f"cmd_{cmd_idx}")
                    slug = re.sub(r'[^a-zA-Z0-9]+', '_', en_name).strip('_').lower()
                    if not slug or len(slug) < 3:
                        slug = f"cp_cmd_{cmd_idx}"
                    else:
                        slug = f"cp_{slug}"
                    cmd["id"] = slug[:50]
                
                # Ensure syntax_type
                if not cmd.get("syntax_type"):
                    cmd["syntax_type"] = "lua_function"
                
                # Ensure min_version
                if not cmd.get("min_version"):
                    cmd["min_version"] = "2.13 (CET 2.13)"
                
                # Ensure framework_required
                if not cmd.get("framework_required"):
                    cmd["framework_required"] = "Cyber Engine Tweaks"
                
                cmd_idx += 1
        break

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully upgraded Cyberpunk commands schema in {JSON_PATH}")

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write('// L-MOD Vault Offline Database (Enriched v3)\n')
    f.write('window.GAMES_DATA = ')
    json.dump(games, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"✅ Successfully synchronized {JS_PATH}")
