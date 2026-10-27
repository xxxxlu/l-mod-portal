#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/retheme_radar_to_violet.py
Converts legacy blue branding accents in public/radar.html to the chosen #A855F7 Neon Violet identity
"""

import re

RADAR_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/radar.html"

with open(RADAR_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Tailwind classes
content = re.sub(r'\btext-blue-600\b', 'text-[#A855F7]', content)
content = re.sub(r'\btext-blue-500\b', 'text-[#A855F7]', content)
content = re.sub(r'\btext-blue-400\b', 'text-[#A855F7]', content)
content = re.sub(r'\btext-blue-300\b', 'text-purple-300', content)
content = re.sub(r'\bbg-blue-600\b', 'bg-[#A855F7]', content)
content = re.sub(r'\bbg-blue-500\b', 'bg-[#A855F7]', content)
content = re.sub(r'\bbg-blue-500/10\b', 'bg-[#A855F7]/10', content)
content = re.sub(r'\bbg-blue-500/20\b', 'bg-[#A855F7]/20', content)
content = re.sub(r'\bborder-blue-500\b', 'border-[#A855F7]', content)
content = re.sub(r'\bborder-blue-500/20\b', 'border-[#A855F7]/20', content)
content = re.sub(r'\bborder-blue-500/30\b', 'border-[#A855F7]/30', content)
content = re.sub(r'\bring-blue-500\b', 'ring-[#A855F7]', content)

# Hover & focus
content = re.sub(r'\bhover:bg-blue-600\b', 'hover:bg-[#A855F7]', content)
content = re.sub(r'\bhover:bg-blue-500\b', 'hover:bg-[#9333ea]', content)
content = re.sub(r'\bhover:text-blue-400\b', 'hover:text-[#A855F7]', content)
content = re.sub(r'\bhover:text-blue-300\b', 'hover:text-purple-300', content)
content = re.sub(r'\bfocus:border-blue-500\b', 'focus:border-[#A855F7]', content)
content = re.sub(r'\bfocus:ring-blue-500\b', 'focus:ring-[#A855F7]', content)
content = re.sub(r'\bgroup-hover:text-blue-400\b', 'group-hover:text-[#A855F7]', content)
content = re.sub(r'\bshadow-blue-500/20\b', 'shadow-[#A855F7]/20', content)
content = re.sub(r'\bshadow-blue-600/20\b', 'shadow-[#A855F7]/20', content)

with open(RADAR_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully rethemed radar.html to #A855F7 Neon Violet!")
