#!/usr/bin/env python3
"""
build_full_database.py
Fills in the default content blocks (nexusStats, consoleCategories, curatedMods,
communityReviews) for games that do not have them yet.

Only fields a game is missing are written, through gamedata_guard: the master data
must exist, radar and trainer fields are never written, and in public/data.js only
the GAMES_DATA segment changes (TRANSLATIONS_DATA is left alone). Games that already
have these fields (all games in the current data) are not touched.

No placeholder content is generated: a new game starts with no console commands
(the same codes do not work across games), no curated mods, no player reviews and
"未记录" Nexus stats, until they are filled in from a source.

Usage: python3 scripts/build_full_database.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

OWNED_FIELDS = ("nexusStats", "consoleCategories", "curatedMods", "communityReviews")

# Starting values for a game that does not have these fields yet.
DEFAULT_FIELDS = {
    "nexusStats": {
        "totalDownloads": "未记录",
        "totalEndorsements": "未记录",
        "totalMods": "未记录",
        "latestPatch": "未记录",
    },
    "consoleCategories": [],
    "curatedMods": [],
    "communityReviews": [],
}


def build_updates(games):
    updates = {}
    for game in games:
        missing = {k: v for k, v in DEFAULT_FIELDS.items() if k not in game}
        if missing:
            updates[game["id"]] = missing
    return updates


if __name__ == "__main__":
    write_owned_fields("build_full_database.py", OWNED_FIELDS, build_updates)
