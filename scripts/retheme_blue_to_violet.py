#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/retheme_blue_to_violet.py
Converts legacy blue branding accents in public/index.html to the chosen #A855F7 Neon Violet identity
"""

import re

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace hex codes
content = content.replace("#0071e3", "#A855F7")
content = content.replace("brand-gradient-bg", "bg-[#A855F7]")
content = content.replace("brand-gradient-text", "text-[#A855F7]")

# Replace Tailwind classes
content = re.sub(r'\btext-blue-600\b', 'text-[#A855F7]', content)
content = re.sub(r'\btext-blue-500\b', 'text-[#A855F7]', content)
content = re.sub(r'\btext-blue-400\b', 'text-purple-400', content)
content = re.sub(r'\bbg-blue-600\b', 'bg-[#A855F7]', content)
content = re.sub(r'\bbg-blue-500\b', 'bg-[#A855F7]', content)
content = re.sub(r'\bbg-blue-50\b', 'bg-purple-500/10', content)
content = re.sub(r'\bborder-blue-500\b', 'border-[#A855F7]', content)
content = re.sub(r'\bborder-blue-600\b', 'border-[#A855F7]', content)
content = re.sub(r'\bborder-blue-400\b', 'border-purple-400', content)
content = re.sub(r'\bring-blue-500\b', 'ring-[#A855F7]', content)

# Hover states
content = re.sub(r'\bhover:bg-blue-600\b', 'hover:bg-[#A855F7]', content)
content = re.sub(r'\bhover:bg-blue-500\b', 'hover:bg-[#9333ea]', content)
content = re.sub(r'\bhover:text-blue-600\b', 'hover:text-[#A855F7]', content)
content = re.sub(r'\bhover:text-blue-400\b', 'hover:text-purple-300', content)
content = re.sub(r'\bhover:border-blue-500\b', 'hover:border-[#A855F7]', content)

# Group hover states
content = re.sub(r'\bgroup-hover:text-blue-600\b', 'group-hover:text-[#A855F7]', content)
content = re.sub(r'\bgroup-hover:text-blue-400\b', 'group-hover:text-purple-300', content)
content = re.sub(r'\bgroup-hover:bg-blue-600\b', 'group-hover:bg-[#A855F7]', content)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully rethemed all blue accents to #A855F7 Neon Violet!")
