#!/usr/bin/env python3
"""
Phase 1: Merge Azkar from 5 sources into unified JSON files.
Sources: OSRC Zikr, Dhikrly, Islambook, Seen-Arabic, Ayah
Output: data/*.json files with schema {id, text, count, source, footer, tags}
"""

import json
import re
import hashlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
PLAN_DIR = BASE_DIR / "plan"
DATA_DIR = BASE_DIR / "data"

# ─── Helper Functions ───────────────────────────────────────────────

def normalize_text(text):
    """Normalize Arabic text for deduplication comparison."""
    if not text:
        return ""
    # Remove tashkeel (diacritics)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Remove tatweel
    text = re.sub(r'\u0640', '', text)
    # Remove non-Arabic chars except spaces
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def make_id(text, source_prefix):
    """Generate a unique ID from normalized text."""
    normalized = normalize_text(text)[:50]
    hash_val = hashlib.md5(normalized.encode('utf-8')).hexdigest()[:8]
    return f"{source_prefix}-{hash_val}"


# ─── Tag Conversion Maps ───────────────────────────────────────────

SESSION_MAP = {
    'Morning': 'أذكار الصباح',
    'Evening': 'أذكار المساء',
    'After Ṣalāh': 'أذكار بعد الصلاة',
    'Before sleep': 'أذكار النوم',
    'Anytime': 'أدعية متنوعة',
    'Daily': 'أذكار يومية',
    'After Salat': 'أذكار بعد الصلاة',
    'Before Sleep': 'أذكار النوم',
    'General': 'أذكار يومية',
}

TYPE_MAP = {
    0: ['أذكار الصباح', 'أذكار المساء'],
    1: ['أذكار الصباح'],
    2: ['أذكار المساء'],
}

ISLAMBOOK_CATEGORY_MAP = {
    'أذكار الصباح': ['أذكار الصباح'],
    'أذكار المساء': ['أذكار المساء'],
    'أذكار النوم': ['أذكار النوم'],
    'أذكار الاستيقاظ': ['أذكار الصباح'],
    'أذكار بعد الصلاة': ['أذكار بعد الصلاة'],
    'تسابيح': ['تسابيح'],
    'أذكار المنزل': ['أذكار المنزل'],
    'أذكار الآذان': ['أذكار الآذان'],
    'أذكار المسجد': ['أذكار المسجد'],
    'أذكار الخلاء': ['أذكار الخلاء'],
    'أذكار الحج والعمرة': ['أذكار الحج'],
    'أذكار الطعام': ['أذكار الطعام'],
    'أذكار السفر': ['أذكار السفر'],
    'أدعية قرآنية': ['أدعية قرآنية'],
    'أدعية نبوية': ['أدعية نبوية'],
    'جوامع الدعاء': ['جوامع الدعاء'],
    'أدعية الأنبياء': ['أدعية الأنبياء'],
    'أسماء الله الحسنى': ['أسماء الله الحسنى'],
    'الرقية الشرعية': ['الرقية الشرعية'],
    'أذكار متنوعة': ['أذكار يومية'],
}

OSRC_TAG_MAP = {
    'morning': ['أذكار الصباح'],
    'night': ['أذكار المساء'],
    'sleep': ['أذكار النوم'],
}

AYAH_CATEGORY_MAP = {
    'أذكار الصباح': ['أذكار الصباح'],
    'أذكار المساء': ['أذكار المساء'],
    'أذكار النوم': ['أذكار النوم'],
    'أذكار الاستيقاظ': ['أذكار الصباح'],
    'أذكار بعد الصلاة': ['أذكار بعد الصلاة'],
    'أذكار متنوعة': ['أذكار يومية'],
    'أدعية متنوعة': ['أدعية متنوعة'],
}


# ─── Source Loaders ─────────────────────────────────────────────────

def load_osrc(filename, tag_key):
    """Load OSRC Zikr data (morning/night/sleep)."""
    filepath = PLAN_DIR / filename
    if not filepath.exists():
        print(f"  [SKIP] {filepath} not found")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tags = OSRC_TAG_MAP.get(tag_key, [])
    azkar = []
    
    for item in data:
        if not item.get('text'):
            continue
        
        azkar.append({
            'id': make_id(item['text'], 'osrc'),
            'text': item['text'].strip(),
            'count': item.get('count', 1),
            'source': item.get('reference', ''),
            'footer': item.get('virtue', ''),
            'tags': tags[:],
        })
    
    print(f"  [OSRC] {filename}: {len(azkar)} azkar")
    return azkar


def load_dhikrly():
    """Load Dhikrly data."""
    filepath = PLAN_DIR / "dhikrly_duas.json"
    if not filepath.exists():
        print(f"  [SKIP] {filepath} not found")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    azkar = []
    
    for item in data:
        text = item.get('ar', '')
        if not text:
            continue
        
        # Parse count from string like "After every Fard Ṣalāh · Before sleep"
        count_str = item.get('count', '1')
        try:
            count = int(count_str) if str(count_str).isdigit() else 1
        except (ValueError, TypeError):
            count = 1
        
        # Convert session to tags
        tags = []
        for session in item.get('session', []):
            mapped = SESSION_MAP.get(session, 'أذكار يومية')
            if mapped not in tags:
                tags.append(mapped)
        
        if not tags:
            tags = ['أذكار يومية']
        
        azkar.append({
            'id': make_id(text, 'dhikrly'),
            'text': text.strip(),
            'count': count,
            'source': item.get('source', ''),
            'footer': '',
            'tags': tags,
        })
    
    print(f"  [Dhikrly] {len(azkar)} duas")
    return azkar


def load_islambook():
    """Load Islambook data."""
    filepath = PLAN_DIR / "azkar_complete.json"
    if not filepath.exists():
        print(f"  [SKIP] {filepath} not found")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    azkar = []
    
    # Structure: {categories: [{category_name_ar, azkar: [{text, count, source, virtue}]}]}
    categories = data.get('categories', [])
    
    for category in categories:
        cat_name = category.get('category_name_ar', '')
        tags = ISLAMBOOK_CATEGORY_MAP.get(cat_name, ['أذكار يومية'])
        
        for item in category.get('azkar', []):
            text = item.get('text', '')
            if not text:
                continue
            
            source = item.get('source', '') or ''
            virtue = item.get('virtue', '') or ''
            
            azkar.append({
                'id': make_id(text, 'islambook'),
                'text': text.strip(),
                'count': item.get('count', 1),
                'source': source,
                'footer': virtue,
                'tags': tags[:],
            })
    
    print(f"  [Islambook] {len(azkar)} azkar")
    return azkar


def load_seen_arabic():
    """Load Seen-Arabic data."""
    filepath = PLAN_DIR / "seen_arabic.json"
    if not filepath.exists():
        print(f"  [SKIP] {filepath} not found")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    azkar = []
    
    for item in data:
        text = item.get('content', '')
        if not text:
            continue
        
        # Convert type to tags
        type_val = item.get('type', 0)
        tags = TYPE_MAP.get(type_val, ['أذكار الصباح', 'أذكار المساء'])
        
        azkar.append({
            'id': make_id(text, 'seen'),
            'text': text.strip(),
            'count': item.get('count', 1),
            'source': item.get('source', ''),
            'footer': item.get('fadl', ''),
            'tags': tags[:],
        })
    
    print(f"  [Seen-Arabic] {len(azkar)} azkar")
    return azkar


def load_ayah():
    """Load Ayah data."""
    filepath = PLAN_DIR / "ayah_azkar.json"
    if not filepath.exists():
        print(f"  [SKIP] {filepath} not found")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    azkar = []
    
    for category_name, items in data.items():
        if not isinstance(items, list):
            continue
        
        for item in items:
            text = item.get('content', '')
            if not text:
                continue
            
            cat = item.get('category', category_name)
            tags = AYAH_CATEGORY_MAP.get(cat, ['أذكار يومية'])
            
            # Parse count
            count_str = str(item.get('count', '1'))
            try:
                count = int(count_str) if count_str.isdigit() else 1
            except (ValueError, TypeError):
                count = 1
            
            azkar.append({
                'id': make_id(text, 'ayah'),
                'text': text.strip(),
                'count': count,
                'source': item.get('reference', ''),
                'footer': item.get('description', ''),
                'tags': tags[:],
            })
    
    print(f"  [Ayah] {len(azkar)} azkar")
    return azkar


# ─── Deduplication ──────────────────────────────────────────────────

def deduplicate(all_azkar):
    """Remove duplicates by normalized text, merging tags."""
    seen = {}
    unique = []
    
    for dhikr in all_azkar:
        normalized = normalize_text(dhikr['text'])
        if not normalized:
            continue
        
        if normalized in seen:
            # Merge tags from duplicate
            existing = seen[normalized]
            for tag in dhikr['tags']:
                if tag not in existing['tags']:
                    existing['tags'].append(tag)
            # Merge sources
            if dhikr['source'] and dhikr['source'] not in existing['source']:
                existing['source'] = f"{existing['source']}; {dhikr['source']}"
            # Use longer footer if available
            if len(dhikr['footer']) > len(existing['footer']):
                existing['footer'] = dhikr['footer']
        else:
            seen[normalized] = dhikr
            unique.append(dhikr)
    
    return unique


# ─── Split by Tags ──────────────────────────────────────────────────

def split_by_tags(azkar):
    """Split azkar into output files by primary tag."""
    output = {
        'morningAzkar': [],
        'nightAzkar': [],
        'sleepAzkar': [],
        'tasbih': [],
        'duas': [],
        'foodAzkar': [],
        'travelAzkar': [],
        'prayerAzkar': [],
        'miscAzkar': [],
    }
    
    tag_to_file = {
        'أذكار الصباح': 'morningAzkar',
        'أذكار المساء': 'nightAzkar',
        'أذكار النوم': 'sleepAzkar',
        'تسابيح': 'tasbih',
        'أدعية قرآنية': 'duas',
        'أدعية نبوية': 'duas',
        'أدعية الأنبياء': 'duas',
        'جوامع الدعاء': 'duas',
        'أدعية متنوعة': 'duas',
        'أذكار الطعام': 'foodAzkar',
        'أذكار السفر': 'travelAzkar',
        'أذكار بعد الصلاة': 'prayerAzkar',
        'أسماء الله الحسنى': 'miscAzkar',
        'الرقية الشرعية': 'miscAzkar',
        'أذكار الآذان': 'miscAzkar',
        'أذكار المسجد': 'miscAzkar',
        'أذكار الخلاء': 'miscAzkar',
        'أذكار المنزل': 'miscAzkar',
        'أذكار الحج': 'miscAzkar',
    }
    
    for dhikr in azkar:
        primary_tag = dhikr['tags'][0] if dhikr['tags'] else 'أذكار يومية'
        target = tag_to_file.get(primary_tag, 'miscAzkar')
        output[target].append(dhikr)
    
    return output


# ─── Main ───────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Phase 1: Merging Azkar Data")
    print("=" * 60)
    
    DATA_DIR.mkdir(exist_ok=True)
    
    # Load all sources
    print("\n📥 Loading sources...")
    all_azkar = []
    all_azkar.extend(load_osrc('morningAzkar.json', 'morning'))
    all_azkar.extend(load_osrc('nightAzkar.json', 'night'))
    all_azkar.extend(load_osrc('sleepAzkar.json', 'sleep'))
    all_azkar.extend(load_dhikrly())
    all_azkar.extend(load_islambook())
    all_azkar.extend(load_seen_arabic())
    all_azkar.extend(load_ayah())
    
    print(f"\n📊 Total before dedup: {len(all_azkar)}")
    
    # Deduplicate
    unique_azkar = deduplicate(all_azkar)
    print(f"📊 Total after dedup: {len(unique_azkar)}")
    
    # Split by tags
    split = split_by_tags(unique_azkar)
    
    # Write output files
    print("\n📝 Writing output files...")
    total_written = 0
    for name, items in split.items():
        output = {
            'tags': [name.replace('Azkar', '').replace('azkar', '')],
            'count': len(items),
            'adhkar': items
        }
        
        filepath = DATA_DIR / f"{name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ {filepath.name}: {len(items)} azkar")
        total_written += len(items)
    
    print(f"\n📊 Total written: {total_written} azkar in {len(split)} files")
    
    # Validate JSON
    print("\n🔍 Validating JSON...")
    errors = 0
    for name in split:
        filepath = DATA_DIR / f"{name}.json"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"  ✅ {filepath.name}: valid")
        except json.JSONDecodeError as e:
            print(f"  ❌ {filepath.name}: {e}")
            errors += 1
    
    if errors == 0:
        print("\n🎉 All files valid!")
    else:
        print(f"\n⚠️  {errors} file(s) have errors")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == '__main__':
    main()
