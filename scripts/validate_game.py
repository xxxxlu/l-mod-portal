#!/usr/bin/env python3
"""
scripts/validate_game.py
L-MOD Vault 强类型 Schema 离线自动化验证工具 (根目录便捷入口)
直接复用并扩展 .agent/skills/game-vault-enricher/scripts/validate_game.py
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_VALIDATOR = os.path.join(BASE_DIR, ".agent/skills/game-vault-enricher/scripts/validate_game.py")
DATA_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")

def main():
    game_id = sys.argv[1] if len(sys.argv) > 1 else None
    data_path = sys.argv[2] if len(sys.argv) > 2 else DATA_PATH

    cmd = [sys.executable, SKILL_VALIDATOR]
    if game_id:
        cmd.append(game_id)
    if len(sys.argv) > 2:
        cmd.append(data_path)
    
    import subprocess
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == '__main__':
    main()
