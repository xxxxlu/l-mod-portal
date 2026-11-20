#!/usr/bin/env python3
"""
build_full_database.py
Fills in the empty content blocks (consoleCategories, curatedMods, communityReviews)
for games that do not have them yet, so the page always gets a list.

Only fields a game is missing are written, through gamedata_guard: the master data
must exist, radar and trainer fields are never written, and in public/data.js only
the GAMES_DATA segment changes (TRANSLATIONS_DATA is left alone). Games that already
have these fields (all games in the current data) are not touched.

No placeholder content is generated: a new game starts with no console commands
(the same codes do not work across games), no curated mods and no player reviews.
nexusStats is not written at all: it only exists for games whose numbers were read
from Nexus Mods (with the date), and the page hides the block when it is missing.

Usage: python3 scripts/build_full_database.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

OWNED_FIELDS = ("consoleCategories", "curatedMods", "communityReviews")

# Starting values for a game that does not have these fields yet.
DEFAULT_FIELDS = {
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
