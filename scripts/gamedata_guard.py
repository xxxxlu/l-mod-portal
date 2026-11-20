#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/gamedata_guard.py
Shared write path for the scripts that fill in GAMES_DATA content
(enrich_flagship_scenarios / enrich_rank5_7_flagships / enrich_rank8_14_tier2 /
rebuild_bg3_flagship / build_full_database).

These scripts used to load the master data, change it, then rewrite the whole
master file and the whole public/data.js (TRANSLATIONS_DATA included). That reset
the radar fields (written by steam_patch_monitor.py) and the trainer fields
(written by fling_trainer_sync.py) to whatever the script had.
They now go through write_owned_fields():

- The master data (src/data/games_top100.json) must exist, or nothing is written.
- Each script names the fields it owns. Radar and trainer fields can never be owned.
- Only those fields of the named games change: in the master data, and in the
  `window.GAMES_DATA = ...;` segment of public/data.js. Game order, every other
  field and game, the file header, window.GAMES_DATABASE and
  window.TRANSLATIONS_DATA stay as they are (same approach as build_i18n_matrix.py).
- Both files are rebuilt and checked first; if anything is off, nothing is written.
- `--dry-run` on the calling script reports what would change and writes nothing.
- Radar fields belong to steam_patch_monitor.py (and the older ai_patch_analyzer.py),
  trainer fields to fling_trainer_sync.py: those scripts pass owner="radar" /
  owner="trainer" and may write only that group; no other script can.
- Content that was checked against sources (CHECKED_FIELDS: commands, popular commands,
  bundles, curated and must-have mods, Nexus numbers, the console flag, console guides,
  pitfall notes and .bat scripts) is never
  replaced by a script: a run that would change it stops. Filling a field a game does
  not have yet with an empty value is allowed. Change checked content in the data,
  with a source, and keep the scripts' literals equal to it.
- Scripts that edit the whole games list in place use load_games_for_edit() and
  write_changed_fields(): only the (game, field) pairs that actually changed are written.
"""

import copy
import json
import os
import sys

from steam_patch_monitor import RADAR_FIELDS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "public/data.js")
GAMES_MARKER = "window.GAMES_DATA = "

# Written by fling_trainer_sync.py only.
TRAINER_FIELDS = ("hasTrainer", "trainerHotkeys", "trainerInfo")
PROTECTED_FIELDS = frozenset(RADAR_FIELDS) | frozenset(TRAINER_FIELDS)
OWNER_FIELDS = {"radar": frozenset(RADAR_FIELDS), "trainer": frozenset(TRAINER_FIELDS)}

# Checked against wikis / official docs / Nexus Mods / GitHub (2026-11-20). Scripts may not replace these.
CHECKED_FIELDS = frozenset({
    "consoleCategories", "popularCommands", "scenarioBundles", "curatedMods",
    "mustHaveMods", "nexusStats", "hasConsole",
    "consoleEnableGuide", "pitfallNote", "batScript",
})


class _Remove:
    def __repr__(self):
        return "REMOVE"


# Value for an update that deletes the field (e.g. the radar clears emergencyAlert).
REMOVE = _Remove()


def _is_empty(value):
    return value is REMOVE or value in (None, [], {}, "", False)


def _stop(script, msg):
    raise SystemExit(f"❌ {script}: {msg}; nothing written.")


def load_master(script):
    """Master data as a list of games. Stops if the file is missing."""
    if not os.path.exists(MASTER_PATH):
        _stop(script, f"master data not found at {MASTER_PATH}")
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        games = json.loads(text)
    except json.JSONDecodeError as exc:
        _stop(script, f"{MASTER_PATH} is not valid JSON ({exc})")
    if not isinstance(games, list):
        _stop(script, f"{MASTER_PATH} is not a list of games")
    return text, games


def split_games_segment(script, content):
    """(start, end, games) of the GAMES_DATA array inside public/data.js."""
    idx = content.find(GAMES_MARKER)
    if idx == -1 or content.find(GAMES_MARKER, idx + 1) != -1:
        _stop(script, f"expected exactly one {GAMES_MARKER!r} in {DATA_JS_PATH}")
    start = idx + len(GAMES_MARKER)
    try:
        games, length = json.JSONDecoder().raw_decode(content[start:])
    except json.JSONDecodeError as exc:
        _stop(script, f"GAMES_DATA in {DATA_JS_PATH} is not plain JSON ({exc})")
    end = start + length
    if not content.startswith(";", end) or not isinstance(games, list):
        _stop(script, f"GAMES_DATA in {DATA_JS_PATH} is not a `[...];` array")
    return start, end, games


def _index(script, games, where):
    out = {}
    for g in games:
        gid = g.get("id") if isinstance(g, dict) else None
        if not gid or gid in out:
            _stop(script, f"{where} has a game without an id or a duplicate id ({gid!r})")
        out[gid] = g
    return out


def write_owned_fields(script, owned_fields, updates, dry_run=None, owner=None):
    """Write `updates` ({game_id: {field: value}}) into both data files.

    `updates` may also be a function that takes a copy of the master games list and
    returns that dict (for scripts that build on the current values).
    owner="radar" / "trainer" lets the radar / trainer script own that group of fields.
    """
    if dry_run is None:
        dry_run = "--dry-run" in sys.argv[1:]
    if owner is not None and owner not in OWNER_FIELDS:
        _stop(script, f"unknown owner {owner!r}")
    own_protected = OWNER_FIELDS.get(owner, frozenset())
    owned = set(owned_fields)
    bad = sorted(owned & (PROTECTED_FIELDS - own_protected))
    if bad:
        _stop(script, f"radar/trainer fields cannot be owned: {bad}")

    master_text, master = load_master(script)
    if not os.path.exists(DATA_JS_PATH):
        _stop(script, f"{DATA_JS_PATH} not found")
    with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
        js_text = f.read()
    start, end, js_games = split_games_segment(script, js_text)

    m_by_id = _index(script, master, MASTER_PATH)
    j_by_id = _index(script, js_games, DATA_JS_PATH)
    if set(m_by_id) != set(j_by_id):
        only_m = sorted(set(m_by_id) - set(j_by_id))
        only_j = sorted(set(j_by_id) - set(m_by_id))
        _stop(script, f"the two files list different games (master only: {only_m}, data.js only: {only_j})")

    if callable(updates):
        updates = updates(copy.deepcopy(master))
    for gid, fields in updates.items():
        if gid not in m_by_id:
            _stop(script, f"unknown game id {gid!r}")
        extra = sorted(set(fields) - owned)
        if extra:
            _stop(script, f"{gid}: fields not declared as owned: {extra}")
        for field, value in fields.items():
            if field in PROTECTED_FIELDS - own_protected:
                _stop(script, f"{gid}: {field} is a radar/trainer field")
            # radar / trainer owners set their own fields in both files; everyone else needs them equal first
            if field not in own_protected and m_by_id[gid].get(field) != j_by_id[gid].get(field):
                _stop(script, f"{gid}.{field} differs between the master data and data.js; reconcile them first")
            old_value = m_by_id[gid].get(field)
            new_value = None if value is REMOVE else value
            if field in CHECKED_FIELDS and new_value != old_value and not (_is_empty(old_value) and _is_empty(value)):
                _stop(script, f"{gid}.{field} holds content checked against sources; this run would replace it "
                              f"(change it in the data with a source, then make the script's literal match)")

    before_master = copy.deepcopy(master)
    before_js = copy.deepcopy(js_games)
    changed = {}
    for gid, fields in updates.items():
        for field, value in fields.items():
            if value is REMOVE:
                if field in m_by_id[gid] or field in j_by_id[gid]:
                    changed.setdefault(field, []).append(gid)
                m_by_id[gid].pop(field, None)
                j_by_id[gid].pop(field, None)
                continue
            if m_by_id[gid].get(field) != value or field not in j_by_id[gid]:
                changed.setdefault(field, []).append(gid)
            m_by_id[gid][field] = copy.deepcopy(value)
            j_by_id[gid][field] = copy.deepcopy(value)

    # Nothing outside the declared (game, field) pairs may have moved.
    for before, after in ((before_master, master), (before_js, js_games)):
        if [g["id"] for g in before] != [g["id"] for g in after]:
            _stop(script, "game order changed")
        for b, a in zip(before, after):
            touched = set(updates.get(b["id"], {}))
            for key in set(b) | set(a):
                if key not in touched and b.get(key) != a.get(key):
                    _stop(script, f"{b['id']}.{key} changed without being declared")

    tail = master_text[len(master_text.rstrip()):]
    new_master_text = json.dumps(master, ensure_ascii=False, indent=2) + tail
    new_js_text = js_text[:start] + json.dumps(js_games, ensure_ascii=False, indent=2) + js_text[end:]
    if json.loads(new_master_text) != master or split_games_segment(script, new_js_text)[2] != js_games:
        _stop(script, "output did not read back the same")

    if not changed:
        print(f"✅ {script}: already up to date, nothing to change.")
        return changed
    for field, gids in sorted(changed.items()):
        print(f"  {field}: {len(gids)} game(s) — {', '.join(gids[:8])}{' …' if len(gids) > 8 else ''}")
    if dry_run:
        print(f"ℹ️ {script}: --dry-run, nothing written.")
        return changed

    for path, text in ((MASTER_PATH, new_master_text), (DATA_JS_PATH, new_js_text)):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    kept = "TRANSLATIONS_DATA and all other fields untouched" if owner else "radar, trainer and TRANSLATIONS_DATA untouched"
    print(f"✅ {script}: updated {MASTER_PATH} and the GAMES_DATA segment of {DATA_JS_PATH} ({kept})")
    return changed


def load_games_for_edit(script):
    """A copy of the master games list, for scripts that change games in place.
    Hand the edited list to write_changed_fields()."""
    return copy.deepcopy(load_master(script)[1])


def write_changed_fields(script, owned_fields, games, dry_run=None, owner=None):
    """Write only the (game, field) pairs where `games` differs from the master data.

    Stops (nothing written) if a game was added, removed or reordered, or if a field
    outside `owned_fields` changed. An owned field that was deleted is deleted in both files.
    """
    _, master = load_master(script)
    if [g.get("id") for g in games] != [g.get("id") for g in master]:
        _stop(script, "games were added, removed or reordered")
    owned = set(owned_fields)
    updates = {}
    for before, after in zip(master, games):
        for key in set(before) | set(after):
            if before.get(key) == after.get(key) and (key in before) == (key in after):
                continue
            if key not in owned:
                _stop(script, f"{before['id']}.{key} changed but the script does not own it")
            updates.setdefault(before["id"], {})[key] = after[key] if key in after else REMOVE
    return write_owned_fields(script, owned_fields, updates, dry_run=dry_run, owner=owner)
