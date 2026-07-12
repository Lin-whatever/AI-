#!/usr/bin/env python3
"""City fuzzy matcher for the Travel Planner skill.
Usage: python3 city_matcher.py "<user_input>"
Outputs JSON: {"matched": bool, "city": str|null, "input": str, "suggestions": [...]}
"""
import json
import sys
from difflib import get_close_matches
from pathlib import Path

REF_DIR = Path(__file__).resolve().parent.parent / 'references'

def load_json(filename):
    path = REF_DIR / filename
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def match_city(user_input):
    user_input = user_input.strip()
    if not user_input:
        return {'matched': False, 'city': None, 'input': user_input, 'suggestions': []}

    # Step 1: check alias map
    aliases = load_json('city_alias_map.json')
    if user_input in aliases:
        return {'matched': True, 'city': aliases[user_input], 'input': user_input, 'suggestions': []}

    # Step 2: auto-complete common short forms (append 市 if missing)
    cities = load_json('china_cities.json')
    if not cities:
        return {'matched': False, 'city': None, 'input': user_input, 'suggestions': []}

    # Try direct match after appending 市/县/etc
    for suffix in ['市', '县', '区']:
        candidate = user_input + suffix
        if candidate in cities:
            return {'matched': True, 'city': candidate, 'input': user_input, 'suggestions': []}

    # Step 3: fuzzy matching
    matches = get_close_matches(user_input, cities, n=5, cutoff=0.45)
    if matches:
        if len(matches) == 1 or (matches and get_close_matches(user_input, cities, n=1, cutoff=0.7)):
            # High confidence single match or first match is very close
            best = get_close_matches(user_input, cities, n=1, cutoff=0.6)
            if best:
                return {'matched': True, 'city': best[0], 'input': user_input, 'suggestions': []}
        # Multiple possible matches
        return {'matched': False, 'city': None, 'input': user_input, 'suggestions': matches[:5]}

    return {'matched': False, 'city': None, 'input': user_input, 'suggestions': []}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'matched': False, 'city': None, 'input': '', 'suggestions': []}, ensure_ascii=False))
        sys.exit(0)
    result = match_city(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
