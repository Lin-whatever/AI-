#!/usr/bin/env python3
"""city_matcher.py 单元测试 — v1.1 包含模糊匹配"""
import sys, json, subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / 'skill' / 'scripts' / 'city_matcher.py'

def match(city_input):
    result = subprocess.run([sys.executable, str(SCRIPT), city_input],
        capture_output=True, text=True, timeout=5)
    return json.loads(result.stdout.strip())

def test_direct_city():
    assert match("北京")["confidence"] == "high"
    assert match("北京")["city"] == "北京市"
    assert match("成都")["city"] == "成都市"

def test_alias_nickname():
    assert match("帝都")["city"] == "北京市"
    assert match("魔都")["city"] == "上海市"

def test_scenic_to_city():
    assert match("喀纳斯")["city"] == "阿勒泰地区"
    assert match("莫高窟")["city"] == "敦煌市"
    assert match("西湖")["city"] == "杭州市"

def test_fuzzy_short_input():
    """模糊匹配：简短输入"""
    r = match("成")
    assert r["matched"] == True
    assert r["confidence"] == "low"  # 低置信度，Agent应确认
    assert r["city"] == "成都市"

def test_fuzzy_partial():
    """模糊匹配：部分输入"""
    r = match("杭")
    assert r["confidence"] == "low"
    assert r["city"] == "杭州市"

def test_no_match():
    r = match("abc123")
    assert r["matched"] == False
    assert r["confidence"] == "none"

def test_empty():
    r = match("")
    assert r["matched"] == False

def test_return_structure():
    r = match("北京")
    for field in ["matched", "city", "input", "suggestions", "confidence"]:
        assert field in r, f"Missing field: {field}"
    assert r["confidence"] in ("high", "low", "none")

if __name__ == '__main__':
    passed = failed = 0
    for name, func in list(globals().items()):
        if name.startswith('test_'):
            try:
                func()
                print(f"  PASS {name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL {name}: {e}")
                failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
