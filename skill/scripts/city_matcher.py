#!/usr/bin/env python3
"""City fuzzy matcher for the Travel Planner skill.
Usage: python3 city_matcher.py "<user_input>"
Outputs JSON: {"matched": bool, "city": str|null, "input": str, "suggestions": [...], "confidence": "high"|"low"|"none"}
"""
import json
import sys
from difflib import get_close_matches
from pathlib import Path

REF_DIR = Path(__file__).resolve().parent.parent / 'references'

def load_json(filename):
    path = REF_DIR / filename
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def match_city(user_input):
    user_input = user_input.strip()
    if not user_input:
        return {'matched': False, 'city': None, 'input': user_input,
                'suggestions': [], 'confidence': 'none'}

    aliases = load_json('city_alias_map.json')
    cities = load_json('china_cities.json')
    if not cities:
        return {'matched': False, 'city': None, 'input': user_input,
                'suggestions': [], 'confidence': 'none'}

    # Step 1: exact alias match
    if user_input in aliases:
        return {'matched': True, 'city': aliases[user_input], 'input': user_input,
                'suggestions': [], 'confidence': 'high'}

    # Step 2: auto-append suffix (市/县/区)
    for suffix in ['市', '县', '区', '镇', '村']:
        candidate = user_input + suffix
        if candidate in cities:
            return {'matched': True, 'city': candidate, 'input': user_input,
                    'suggestions': [], 'confidence': 'high'}

    # Step 3: direct match in city list (e.g. "黄山" exact match but not alias)
    if user_input in cities:
        return {'matched': True, 'city': user_input, 'input': user_input,
                'suggestions': [], 'confidence': 'high'}

    # Step 4: fuzzy matching with tiered thresholds
    # High confidence: cutoff 0.6
    high_matches = get_close_matches(user_input, cities, n=5, cutoff=0.6)
    if high_matches and len(high_matches) == 1:
        return {'matched': True, 'city': high_matches[0], 'input': user_input,
                'suggestions': [], 'confidence': 'high'}

    # Medium confidence: cutoff 0.45 — present as suggestions
    med_matches = get_close_matches(user_input, cities, n=5, cutoff=0.45)
    if med_matches:
        # If only 1 match at medium confidence, return as low-confidence match
        # Agent should confirm: "请问你想去的是{med_matches[0]}吗？"
        if len(med_matches) == 1:
            return {'matched': True, 'city': med_matches[0], 'input': user_input,
                    'suggestions': [], 'confidence': 'low'}
        # Multiple matches: return as suggestions
        return {'matched': False, 'city': None, 'input': user_input,
                'suggestions': med_matches[:5], 'confidence': 'low'}

    # Step 5: very short input (1-2 chars) — try substring match
    if len(user_input) <= 2:
        substring_matches = [c for c in cities if user_input in c]
        if substring_matches:
            # Sort by length (shorter = closer match)
            substring_matches.sort(key=len)
            return {'matched': False, 'city': None, 'input': user_input,
                    'suggestions': substring_matches[:5], 'confidence': 'low'}

    return {'matched': False, 'city': None, 'input': user_input,
            'suggestions': [], 'confidence': 'none'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'matched': False, 'city': None, 'input': '',
                         'suggestions': [], 'confidence': 'none'}, ensure_ascii=False))
        sys.exit(0)
    result = match_city(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
