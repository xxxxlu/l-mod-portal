#!/usr/bin/env python3
"""
scripts/upgrade_cyberpunk_schema.py
Writes through gamedata_guard (write_changed_fields): only the fields in OWNED_FIELDS of the
games it changes, in both the master data and the GAMES_DATA segment of public/data.js
(radar, trainer and TRANSLATIONS_DATA untouched). The commands and mods it would write are
older, unchecked versions of content that has since been checked against sources, so the
guard stops the run without writing anything; the script is kept for its history.
Usage: python3 scripts/upgrade_cyberpunk_schema.py [--dry-run]
"""

import re

from gamedata_guard import load_games_for_edit, write_changed_fields

SCRIPT = "upgrade_cyberpunk_schema.py"
OWNED_FIELDS = ('consoleCategories',)

games = load_games_for_edit(SCRIPT)

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

write_changed_fields(SCRIPT, OWNED_FIELDS, games)
