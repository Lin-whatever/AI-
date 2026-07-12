#!/usr/bin/env python3
"""Feishu Interactive Card builder for the Travel Planner skill.
Reads a JSON itinerary from stdin, outputs a Feishu card JSON to stdout.
"""
import json
import sys
from pathlib import Path

REF_DIR = Path(__file__).resolve().parent.parent / 'references'
TEMPLATE_PATH = REF_DIR / 'lark_card_template.json'

NL = chr(10)


def build_daily_plan_md(daily_plan):
    out = []
    for day in daily_plan:
        d = day.get('day', '?')
        out.append(f'**Day {d}**')
        if day.get('morning'):
            out.append(f'上午: {day["morning"]}')
        if day.get('afternoon'):
            out.append(f'下午: {day["afternoon"]}')
        if day.get('evening'):
            out.append(f'晚上: {day["evening"]}')
        if day.get('food'):
            out.append(f'美食: {day["food"]}')
        out.append('')
    return NL.join(out)


def build_budget_md(breakdown):
    if not breakdown:
        return ''
    items = [
        ('住宿', breakdown.get('accommodation', 0)),
        ('餐饮', breakdown.get('meals', 0)),
        ('交通', breakdown.get('transport', 0)),
        ('门票', breakdown.get('tickets', 0)),
        ('其他', breakdown.get('other', 0)),
    ]
    total = sum(v for _, v in items)
    out = ['**预算明细**', '']
    for name, cost in items:
        out.append(f'{name}: {cost}元')
    out.append(f'**合计**: {total}元')
    return NL.join(out)


def build_tips_md(tips):
    if not tips:
        return ''
    out = ['**重要提示**', '']
    for tip in tips:
        out.append(f'- {tip}')
    return NL.join(out)


def set_nested_value(obj, path, value):
    """Set a value in a nested dict by dot-separated path."""
    keys = path.split('.')
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        obj = obj[key]
    last = keys[-1]
    if last.isdigit():
        last = int(last)
    obj[last] = value


def get_nested_value(obj, path):
    """Get a value from a nested dict by dot-separated path."""
    keys = path.split('.')
    for key in keys:
        if key.isdigit():
            key = int(key)
        obj = obj[key]
    return obj


def replace_in_obj(obj, replacements):
    """Recursively replace {placeholders} in all string values of a dict/list."""
    if isinstance(obj, dict):
        return {k: replace_in_obj(v, replacements) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_in_obj(item, replacements) for item in obj]
    elif isinstance(obj, str):
        result = obj
        for placeholder, value in replacements.items():
            result = result.replace('{' + placeholder + '}', str(value))
        return result
    else:
        return obj


def build_card(itinerary):
    if not TEMPLATE_PATH.exists():
        return {'error': 'Template not found: ' + str(TEMPLATE_PATH)}

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = json.load(f)

    city = itinerary.get('city', '未知')
    days = itinerary.get('days', '?')
    budget = itinerary.get('budget', '?')
    companions = itinerary.get('companions', '未知')
    preferences = itinerary.get('preferences', '无')
    daily_plan = itinerary.get('daily_plan', [])
    budget_breakdown = itinerary.get('budget_breakdown', {})
    tips = itinerary.get('tips', [])

    replacements = {
        'city': city,
        'days': days,
        'budget': budget,
        'companions': companions,
        'preferences': preferences,
        'daily_plan_md': build_daily_plan_md(daily_plan),
        'budget_breakdown_md': build_budget_md(budget_breakdown),
        'tips_md': build_tips_md(tips),
    }

    result = replace_in_obj(template, replacements)
    return result


if __name__ == '__main__':
    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'Invalid JSON input: {e}'}, ensure_ascii=False))
        sys.exit(1)

    result = build_card(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
