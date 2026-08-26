# خطة التعديل — استبدال صفحة الأذكار

## الهدف

**حذف** صفحة الأذكار الحالية (`src/adhkar.html`) واستبدالها بتصميم من [OSRC Zikr](https://osrcz.vercel.app/azkar/morning) مع تعديلات.

---

## ما يُحذف

- `src/adhkar.html` → يُحذف بالكامل

---

## ما يُستبدل به (من OSRC Zikr)

| العنصر | الوصف |
|--------|-------|
| تصميم الكارت | نص الذكر في صندوق داكن داخل الكارت |
| عداد تفاعلي | زر احتساب مع عداد تصاعدي |
| شريط تقدم | دائرة conic-gradient |
| زر إعادة العد | لإعادة العداد |
| عرض الفضل | "فضله:" |
| عرض المصدر | "صحته:" |

---

## التعديلات المطلوبة

### 1. الثيم
| OSRC Zikr | نور |
|-----------|-----|
| `#6EE7B7` (أخضر) | `#d4a843` (ذهبي) |
| `#111A18` (خلفية كارت) | `var(--bg-card)` |
| `#0B1110` (خلفية الصفحة) | `var(--bg-primary)` |

### 2. الـ API
- OSRC Zikr: يقرأ JSON محلياً عبر `import`
- نور: يجلب البيانات عبر `fetch` من GitHub raw

### 3. الـ JSON
| OSRC Zikr | نور |
|-----------|-----|
| `text`, `count`, `virtue`, `reference` | `text`, `count`, `source`, `tags`, `footer` |

يجب دمج الهيكلين: إضافة `tags` و `footer` من نور + `virtue` و `reference` من OSRC Zikr

---

## الخطوات

### 1. تحميل بيانات OSRC Zikr
```
morningAzkar.json → https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/morningAzkar.json
nightAzkar.json   → https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/nightAzkar.json
sleepAzkar.json   → https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/sleepAzkar.json
```

### 2. تحويل الهيكل
إضافة `tags` لكل ذكر:
```json
{
    "text": "...",
    "count": 1,
    "virtue": "...",
    "reference": "...",
    "tags": ["أذكار الصباح"]
}
```

### 3. كتابة `src/adhkar.html` جديد
- تصميم من OSRC Zikr
- ثيم ذهبي
- fetch من GitHub raw
- فلاتر التصنيف
- عداد تفاعلي

---

## الملفات

| الملف | الإجراء |
|-------|---------|
| `src/adhkar.html` | حذف + إعادة كتابة |
| `data/morningAzkar.json` | إنشاء |
| `data/nightAzkar.json` | إنشاء |
| `data/sleepAzkar.json` | إنشاء |

---

# قسم ٢ — صفحة القرآن من quran.prh.gov.sa

## الهدف
استبدال أو تطوير `src/quran.html` باستخدام تصميم و API من `https://quran.prh.gov.sa`

---

## ⚠️ ملاحظة مهمة
**ممكن نسخ الصفحة بالكامل من quran.prh.gov.sa ولصقها مع تغييرات:**
- الموقع React SPA — لكن الملفات الثابتة (HTML/CSS/JS) ممكن ننسخها
- نغيّر الألوان من أخضر `#00AB55` إلى ذهبي `#d4a843`
- نحذف features ما نبيها (وضع الطالب، chat widget)
- نضيف features نبيها (تحميل PDF)

---

## الميزات المطلوب تنفيذها

### 1. اختيار القارئ (🔴 عالية)
```javascript
const RECITERS = [
  { id: 7, name: 'مشاري العفاسي', style: 'عادي' },
  { id: 3, name: 'عبدالرحمن السديس', style: 'عادي' },
  { id: 10, name: ' Saud ash-Shuraym', style: 'عادي' },
  { id: 6, name: 'محمود خليل الحصري', style: 'عادي' },
  { id: 12, name: 'محمود خليل الحصري', style: 'معلم' },
  { id: 4, name: 'أبو بكر الشاطري', style: 'عادي' },
  { id: 5, name: 'هاني الرفاعي', style: 'عادي' },
  { id: 11, name: 'محمد الطبراوي', style: 'عادي' },
  { id: 9, name: 'محمد صديق المنشاوي', style: 'مرتل' },
  { id: 8, name: 'محمد صديق المنشاوي', style: 'مجود' },
  { id: 2, name: 'عبدالباسط عبدالصمد', style: 'مرتل' },
  { id: 1, name: 'عبدالباسط عبدالصمد', style: 'مجود' },
];
```

- Dropdown في الصفحة يختار القارئ
- يحفظ 선택 المستخدم في `localStorage`
- الصوت يتغير حسب القارئ المختار

### 2. تغيير القارئ أثناء التشغيل (🔴 عالية)
- زر أو قائمة_minor في مشغل الصوت
- يغيّر القارئ بدون ما يوقف التشغيل

### 3. تغيير الـ API إلى api.quran.com (🟡 متوسطة)
| القديم (alquran.cloud) | الجديد (api.quran.com) |
|-------------------------|------------------------|
| `GET /surah/{num}/quran-uthmani` | `GET /verses/by_chapter/{num}?language=ar` |
| لا يدعم الترجمة | يدعم الترجمة بـ `translation_id` |
| صوت فقط من CDN واحد | 12 قارئ |

### 4. عرض صور المصحف (🟢 منخفضة)
- `https://quran.prh.gov.sa` فيه عرض المصحف كصور
- ممكن نستخدم `quran.islam-db.com` (الحالي) أو نضيف صور من الموقع الجديد

### 5. تحديث الثيم
| quran.prh.gov.sa | نور |
|------------------|-----|
| `#00AB55` (أخضر) | `#d4a843` (ذهبي) |
| `#1A1A2E` (خلفية) | `var(--bg-primary)` |
| `Public Sans` | `Amiri` + `Noto Naskh Arabic` |

---

## الـ API الأساسي

| الهدف | الرابط |
|-------|--------|
| قائمة السور | `GET https://api.quran.com/api/v4/chapters` |
| آيات سورة | `GET https://api.quran.com/api/v4/verses/by_chapter/{surah}` |
| ترجمة | `GET https://api.quran.com/api/v4/verses/by_chapter/{surah}?translation_id=131` |
| صوت قارئ | `GET https://api.quran.com/api/v4/recitations/{recitation_id}/by_chapter/{surah}` |
| صفحة مصحف | `GET https://api.quran.com/api/v4/pages/{page_number}` |
| أجزاء | `GET https://api.quran.com/api/v4/juzs` |

---

## مصادر الصوت — MP3Quran.net

**المصدر:** [TilawaPlayer](https://github.com/MohssineX/TilawaPlayer)

### نمط الرابط

```
https://server{N}.mp3quran.net/{reciter}/{surah:03d}.mp3
```

**مثال:**
```
https://server8.mp3quran.net/afs/001.mp3  ← الفاتحة (مشاري)
https://server8.mp3quran.net/afs/002.mp3  ← البقرة (مشاري)
https://server8.mp3quran.net/afs/114.mp3  ← الناس (مشاري)
```

### القارئون (30 قارئ)

| # | القارئ | السيرفر | الرابط |
|---|--------|---------|--------|
| 1 | **عبدالباسط عبدالصمد** | server7 | `server7.mp3quran.net/basit/` |
| 2 | **محمود خليل الحصري** | server13 | `server13.mp3quran.net/husr/` |
| 3 | **محمد صديق المنشاوي** | server10 | `server10.mp3quran.net/minsh/` |
| 4 | **مشاري العفاسي** | server8 | `server8.mp3quran.net/afs/` |
| 5 | **ماهر المعيقلي** | server12 | `server12.mp3quran.net/maher/` |
| 6 | **ياسر الدوسري** | server11 | `server11.mp3quran.net/yasser/` |
| 7 | **سعد الغامدي** | server7 | `server7.mp3quran.net/s_gmd/` |
| 8 | **سعود الشريم** | server7 | `server7.mp3quran.net/shur/` |
| 9 | **أحمد العجمي** | server10 | `server10.mp3quran.net/ajm/` |
| 10 | **عبدالرحمن السديس** | server11 | `server11.mp3quran.net/sds/` |
| 11 | **أبو بكر الشاطري** | server11 | `server11.mp3quran.net/shatri/` |
| 12 | **محمد أيوب** | server8 | `server8.mp3quran.net/ayyub/` |
| 13 | **ناصر القطامي** | server6 | `server6.mp3quran.net/qtm/` |
| 14 | **علي الحذيفي** | server9 | `server9.mp3quran.net/hthfi/` |
| 15 | **خليفة التنيجي** | server12 | `server12.mp3quran.net/tnjy/` |
| 16 | **علي جابر** | server11 | `server11.mp3quran.net/a_jbr/` |
| 17 | **بندر بليلة** | server6 | `server6.mp3quran.net/balilah/` |
| 18 | **خالد الجليل** | server10 | `server10.mp3quran.net/jleel/` |
| 19 | **عبدالله بصفر** | server6 | `server6.mp3quran.net/bsfr/` |
| 20 | **صالح بوخاطر** | server8 | `server8.mp3quran.net/bu_khtr/` |
| 21 | **عبدالمحسن القاسم** | server8 | `server8.mp3quran.net/qasm/` |
| 22 | **عبدالله الجهني** | server13 | `server13.mp3quran.net/jhn/` |
| 23 | **صالح البودعي** | server6 | `server6.mp3quran.net/s_bud/` |
| 24 | **هاني الرفاعي** | server8 | `server8.mp3quran.net/hani/` |
| 25 | **محمد جبريل** | server8 | `server8.mp3quran.net/jbrl/` |
| 26 | **محمود علي البنا** | server8 | `server8.mp3quran.net/bna/` |
| 27 | **مصطفى اسماعيل** | server8 | `server8.mp3quran.net/mustafa/` |
| 28 | **عبدالباري ال臭بيتي** | server6 | `server6.mp3quran.net/thubti/` |
| 29 | **وديع اليمني** | server6 | `server6.mp3quran.net/wdee3/` |
| 30 | **خالد القحطاني** | server10 | `server10.mp3quran.net/qht/` |

### مثال على الاستخدام في JavaScript

```javascript
function getAudioUrl(reciter, surah) {
  const RECITERS = {
    mishary: 'server8.mp3quran.net/afs/',
    sudais: 'server11.mp3quran.net/sds/',
    husary: 'server13.mp3quran.net/husr/',
    minshawi: 'server10.mp3quran.net/minsh/',
  };
  const padded = String(surah).padStart(3, '0');
  return `https://${RECITERS[reciter]}${padded}.mp3`;
}

// مثال
const url = getAudioUrl('mishary', 36); // يس
// https://server8.mp3quran.net/afs/036.mp3
```

---

## مثال على الاستخدام (api.quran.com)

```javascript
// جلب سورة آل عمران
const surah = await fetch('https://api.quran.com/api/v4/verses/by_chapter/3?language=ar&per_page=10');
const data = await surah.json();

// جلب صوت السديس لسورة آل عمران
const audio = await fetch('https://api.quran.com/api/v4/recitations/3/by_chapter/3');

// جلب صوت الحصري لسورة آل عمران
const audio2 = await fetch('https://api.quran.com/api/v4/recitations/6/by_chapter/3');
```

---

# قسم ٣ — مصادر JSON الأذكار من GitHub Raw

## الهدف
جمع الأذكار من مصادر متعددة وتحزينها كملفات JSON في `data/` — ثم جلبها عبر `fetch` من GitHub raw في الـ frontend.

---

## المصادر

### 1. OSRC Zikr (suss200)
| الملف | الرابط |
|-------|--------|
| أذكار الصباح | `https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/morningAzkar.json` |
| أذكار المساء | `https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/nightAzkar.json` |
| أذكار النوم | `https://raw.githubusercontent.com/suss200/osrc-zikr/main/src/app/data/sleepAzkar.json` |

**البنية:**
```json
{
  "text": "...",
  "count": 1,
  "virtue": "...",
  "reference": "..."
}
```

---

### 2. Dhikrly (nazrulislambhat)
| الملف | الرابط | الحالة |
|-------|--------|--------|
| أدعية + أذكار | `https://raw.githubusercontent.com/nazrulislambhat/dhikrly/main/data/duas.json` | ✅ تم التحميل |

**الملف المحلي:** `/home/mahmoud/Desktop/dhikrly_duas.json`

**عدد الأذكار:** 18 ذكر/دعاء

**البنية:**
```json
{
  "id": "ayat-kursi",
  "category": "quran",
  "session": ["After Ṣalāh", "Evening"],
  "priority": true,
  "count": "After every Fard Ṣalāh · Before sleep",
  "title": "Ayat al-Kursi",
  "titleAr": "آية الكرسي",
  "transliteration": "...",
  "en": "...",
  "ar": "..."
}
```

**التصنيفات:**
- `quran` — آيات قرآنية (آية الكرسي، الإخلاص، الفلق، الناس)
- `dua` — أدعية نبوية
- `athkar` — أذكار متنوعة

---

### 3. Ayah (nawafalqari)
| الملف | الرابط |
|-------|--------|
| أذكار مجمعة | `https://raw.githubusercontent.com/nawafalqari/ayah/main/src/data/adkar.json` |
| نص القرآن | `https://raw.githubusercontent.com/nawafalqari/ayah/main/src/data/quran.json` |

**بنية الأذكار:**
```json
{
  "أذكار الصباح": [
    {
      "category": "أذكار الصباح",
      "count": "1",
      "description": "من قالها حين يصبح أجير...",
      "reference": "[آية الكرسى]",
      "content": "أَصْـبَحْنا..."
    }
  ]
}
```

---

### 4. Seen-Arabic (Morning & Evening Adhkar DB) ⭐ الأفضل
| الملف | الرابط |
|-------|--------|
| **عربي** | `https://raw.githubusercontent.com/Seen-Arabic/Morning-And-Evening-Adhkar-DB/main/ar.json` |
| **إنجليزي** | `https://raw.githubusercontent.com/Seen-Arabic/Morning-And-Evening-Adhkar-DB/main/en.json` |

**المصدر:** حصن المسلم — الشيخ ابن القيم / الشيخ صالح المغامسي

**الإحصائيات:**
- **34 ذكر** — أذكار الصباح والمساء
- **33 ذكر فيه صوت** — من hisnmuslim.com
- **MIT License** — مفتوح المصدر

**بنية الـ JSON:**
```json
{
  "order": 1,
  "content": "الْحَمْدُ لِلَّهِ وَحْدَهُ...",
  "count": 1,
  "count_description": "مَرَّةٌ وَاحِدَةٌ",
  "fadl": "استحباب ابتداء الدعاء بالحمد لله...",
  "source": "عن أنس يرفعه...",
  "type": 0,
  "audio": "https://...",
  "hadith_text": "...",
  "explanation_of_hadith_vocabulary": ""
}
```

**التصنيفات:**
| type | التصنيف | العدد |
|------|---------|-------|
| 0 | صباح + مساء | 16 |
| 1 | صباح فقط | 10 |
| 2 | مساء فقط | 8 |

---

### 4. Islambook (تم استخراجه مسبقاً)
| الملف | الموقع |
|-------|--------|
| `azkar_complete.json` | `/home/mahmoud/Desktop/azkar_complete.json` |

**البنية:**
```json
{
  "source": "https://www.islambook.com/azkar/",
  "total_categories": 27,
  "total_azkar": 314,
  "categories": [
    {
      "category_id": 1,
      "category_name_ar": "أذكار الصباح",
      "azkar": [
        {
          "text": "...",
          "subtitle": "أَعُوذُ بِاللهِ...",
          "source": "[آية الكرسى - البقرة 255]",
          "virtue": "من قالها حين يصبح أجير من الجن...",
          "count": 1
        }
      ]
    }
  ]
}
```

---

## خطة الدمج

### Step 1 — نسخ الملفات إلى `data/`
```
data/
├── adhkar.json              ← current (37 azkar)
├── ahadith.json             ← current (30 hadith)
├── morningAzkar.json        ← من OSRC Zikr
├── nightAzkar.json          ← من OSRC Zikr
├── sleepAzkar.json          ← من OSRC Zikr
├── duas.json                ← من Dhikrly
├── ayah_azkar.json          ← من Ayah
└── islambook_azkar.json     ← من Islambook
```

### Step 2 — تحويل الهيكل الموحد
كل مصدر有不同的 بنية — يجب تحويلها إلى بنية موحدة:

```json
{
  "id": "unique-id",
  "text": "نص الذكر",
  "count": 1,
  "source": "المصدر (البقرة 255)",
  "virtue": "فضله",
  "tags": ["أذكار الصباح", "أذكار المساء"],
  "footer": "ملاحظة إضافية"
}
```

### Step 3 — الـ Fetch في Frontend
```javascript
const SOURCES = {
  morning: 'https://raw.githubusercontent.com/Gameman2012/athkar/main/data/morningAzkar.json',
  night: 'https://raw.githubusercontent.com/Gameman2012/athkar/main/data/nightAzkar.json',
  sleep: 'https://raw.githubusercontent.com/Gameman2012/athkar/main/data/sleepAzkar.json',
  duas: 'https://raw.githubusercontent.com/Gameman2012/athkar/main/data/duas.json',
};

async function loadAzkar(category) {
  const res = await fetch(SOURCES[category]);
  return await res.json();
}
```

---

## التصنيفات النهائية (بعد الدمج)

| التصنيف | العدد التقديري | المصادر |
|---------|---------------|--------|
| أذكار الصباح | ~50 | OSRC + Islambook + Ayah + **Seen-Arabic** |
| أذكار المساء | ~50 | OSRC + Islambook + Ayah + **Seen-Arabic** |
| أذكار النوم | ~20 | OSRC + Islambook |
| أذكار بعد الصلاة | ~15 | Islambook + Dhikrly |
| أذكار الاستيقاظ | ~10 | Islambook |
| أذكار الوضوء | ~5 | Islambook |
| أذكار المسجد | ~5 | Islambook |
| أذكار الطعام | ~10 | Islambook |
| أذكار الآذان | ~10 | Islambook |
| أذكار المنزل | ~5 | Islambook |
| أذكار الخلاء | ~5 | Islambook |
| أذكار الحج | ~5 | Islambook |
| تسابيح | ~20 | OSRC + Islambook |
| أدعية قرآنية | ~30 | Islambook + Dhikrly |
| أدعية نبوية | ~30 | Islambook |
| جوامع الدعاء | ~35 | Islambook |
| أدعية الأنبياء | ~15 | Islambook |
| أسماء الله الحسنى | ~10 | Islambook |
| الرقية الشرعية | ~5 | Islambook |
| **الإجمالي** | **~384+** | **5 مصادر** |

---

## ⭐ أفضل مصدر — Seen-Arabic

**السبب:** أدق مصدر — 34 ذكر من حصن المسلم + صوت + ترجمة + مصادر أحاديث.

**يجب أن يكون المصدر الأساسي** — باقي المصادر تكملة.

---

# قسم ٤ — دليل Quran.com API الشامل

## الهدف
توثيق جميع endpoints المتاحة في Quran.com API لاستخدامها في `src/quran.html` وصفحات أخرى.

---

## ١. مستويات الـ API

| المستوى | الرابط | الملاحظات |
|---------|--------|-----------|
| **Legacy v3** | `https://api.quran.com/api/v3/` | مفتوح بدون تسجيل دخول — بعض الـ endpoints شغال وبعضها محذوف |
| **v4 Content API** | `https://apis.quran.foundation/content/api/v4/` | رسمي — يحتاج OAuth2 (`client_id` + `x-auth-token`) |
| **JavaScript SDK** | `@quranjs/api` (npm) | يدير التوكن والتخزين المؤقت — موصى به لـ Node/TS |

---

## ٢. المصادقة (v4 فقط — مطلوب لـ production)

1. التسجيل في [Developer Console](https://dev-console.quran.foundation)
2. جلب التوكن:
```bash
curl --request POST \
  --url https://oauth2.quran.foundation/oauth2/token \
  --user 'CLIENT_ID:CLIENT_SECRET' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data 'grant_type=client_credentials&scope=content'
```
3. استخدام التوكن:
   - `x-auth-token: <JWT>` (صالح 3600 ثانية)
   - `x-client-id: <your_client_id>`

**ملاحظة:** بدون OAuth2 نقدر نستخدم v3 (المتبقية) أو نسجّل تطبيق.

---

## ٣. endpoints v3 المتبقية (تعمل بدون مصادقة)

| الـ Endpoint | الوصف | الحالة |
|-------------|-------|--------|
| `GET /api/v3/chapters` | قائمة السور (114) | ✅ يعمل |
| `GET /api/v3/chapters/{id}` | سورة محددة | ✅ يعمل |
| `GET /api/v3/chapters/{id}/verses?words=true&fields=text_uthmani` | آيات سورة مع كلمات | ✅ يعمل |
| `GET /api/v3/juzs` | قائمة الأجزاء | ✅ يعمل |
| `GET /api/v3/search?q={query}` | بحث في القرآن | ✅ يعمل |
| `GET /api/v3/pages` | صفحات المصحف | ❌ 404 |
| `GET /api/v3/verses/by_page/{page}` | آيات صفحة | ❌ 404 |
| `GET /api/v3/translations` | الترجمات | ❌ 404 |
| `GET /api/v3/tafsirs` | التفاسير | ❌ 404 |
| `GET /api/v3/recitations` | القراءات | ❌ 404 |

---

## ٤. endpoints v4 الشاملة

### ٤.١ السور
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /chapters` | كل السور (114) — يدعم `language` |
| `GET /chapters/{id}` | سورة محددة |
| `GET /chapters/{id}/info` | معلومات السورة (مكي/مدني) |

### ٤.٢ الآيات (11 طريقة للجلب)
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /verses/by_chapter/{id}` | آيات سورة بالرقم |
| `GET /verses/by_page/{page}` | آيات بالصفحة |
| `GET /verses/by_juz/{juz}` | آيات بالجزء |
| `GET /verses/by_hizb/{hizb}` | آيات بالحزب |
| `GET /verses/by_rub_el_hizb/{rub}` | آيات بالربع |
| `GET /verses/by_key/{key}` | آية واحدة (مثلاً `2:255`) |
| `GET /verses/by_id/{id}` | آية بالـ ID |
| `GET /verses/random` | آية عشوائية |
| `GET /verses/search` | بحث في الآيات |

**المعلمات المشتركة للآيات:**
- `fields=text_uthmani,text_indopak,text_qpc_hafs` — نصوص مختلفة
- `word_fields=text_uthmani,translation` — بيانات على مستوى الكلمة
- `translations=131` — إضافة ترجمة (ID=131 للإنجليزية)
- `tafsirs=1` — إضافة تفسير
- `words=true` — بيانات كلمة بكلمة
- `audio=true&recitation=7` — روابط صوتية
- `per_page=10&page=1` — ترقيم الصفحات

### ٤.٣ صفحات المصحف
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /pages` | كل الصفحات (604) |
| `GET /pages/{number}` | صفحة محددة |
| `GET /pages/by_juz/{juz}` | صفحات جزء معين |

### ٤.٤ الأجزاء والحبسات
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /juzs` | كل الأجزاء (30) |
| `GET /hizbs` | كل الحبسات |
| `GET /rub_el_hizbs` | كل أرباع الحبسات |
| `GET /rukus` | كل الركوعات |
| `GET /manzils` | كل المنازل |

### ٤.٥ الترجمات والتفسير
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /resources/translations` | قائمة الترجمات المتاحة |
| `GET /resources/translations/{id}` | تفاصيل ترجمة |
| `GET /resources/tafsirs` | قائمة التفاسير المتاحة |
| `GET /resources/tafsirs/{id}` | تفاصيل تفسير |

### ٤.٦ الصوت والقراءات
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /resources/recitations` | قائمة القراء |
| `GET /resources/recitations/{id}` | تفاصيل قارئ |
| `GET /audio/reciter/{id}/timestamp` | توقيت التلاوة |

### ٤.٧ نصوص القرآن (11 شكل مختلف)
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /quran/verses/uthmani` | خط عثماني |
| `GET /quran/verses/uthmani_simple` | عثماني مبسط |
| `GET /quran/verses/uthmani_tajweed` | عثماني مع تجويد HTML |
| `GET /quran/verses/imlaei` | إملائي |
| `GET /quran/verses/imlaei_simple` | إملائي مبسط |
| `GET /quran/verses/indopak` | إندو باك |
| `GET /quran/verses/code_v1` | كود V1 |
| `GET /quran/verses/code_v2` | كود V2 |
| `GET /quran/verses/qpc_hafs` | QPC حفص |
| `GET /quran/verses/qpc_nastaleeq_hafs` | QPC نستعليق حفص |
| `GET /quran/words/uthmani` | كلمات عثمانية |

### ٤.٨ أحاديث المرتبطة بآيات
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /hadith/references/by_ayah/{surah}/{ayah}` | أحاديث مرتبطة بآية |
| `GET /hadith/references/by_verse_key/{key}` | بالمفتاح (2:255) |
| `GET /hadith/references/by_verse_id/{id}` | بالـ ID |

### ٤.٩ أدعية القرآن
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /answers/by_ayah/{surah}/{ayah}` | أدعية مرتبطة بآية |
| `GET /answers/by_verse_key/{key}` | بالمفتاح |
| `GET /answers/by_verse_id/{id}` | بالـ ID |

### ٤.١٠ هامشات
| الـ Endpoint | الوصف |
|-------------|-------|
| `GET /foot_note/{id}` | هامش معين |

### ٤.١١ Quran Reflect (اجتماعي)
| الـ Endpoint | المصادقة | الوصف |
|-------------|---------|-------|
| `GET /posts/feed` | `post.read` | تغذية التأملات |
| `GET /posts/{id}` | `post.read` | تأمل واحد |
| `GET /posts/{id}/comments` | `comment.read` | تعليقات |

---

## ٥. م-fields المتاحة (Fields Reference)

### على مستوى الآية (`fields`):
| الحقل | الوصف |
|-------|-------|
| `text_uthmani` | نص عثماني |
| `text_uthmani_simple` | عثماني مبسط |
| `text_uthmani_tajweed` | عثماني مع تجويد HTML |
| `text_indopak` | إندو باك |
| `text_imlaei` | إملائي |
| `text_imlaei_simple` | إملائي مبسط |
| `text_qpc_hafs` | QPC حفص |
| `text_qpc_nastaleeq_hafs` | QPC نستعليق حفص |
| `code_v1` / `code_v2` | أكواد |
| `page_number` | رقم الصفحة |
| `image_url` | رابط صورة الصفحة |

### على مستوى الكلمة (`word_fields`):
`text_uthmani`, `text_indopak`, `text_imlaei_simple`, `transliteration`, `translation`, `verse_key`, `location`

---

## ٦. مثال عملي — بناء quran.html

### تحميل السور
```javascript
const chaptersRes = await fetch('https://api.quran.com/api/v3/chapters');
const { chapters } = await chaptersRes.json();
// chapters = [{id:1, name_arabic:"الفاتحة", verses_count:7, pages:[1,1]}, ...]
```

### تحميل آيات سورة
```javascript
const versesRes = await fetch(
  `https://api.quran.com/api/v3/chapters/1/verses?words=true&fields=text_uthmani&per_page=10`
);
const { verses, pagination } = await versesRes.json();
// verses[0] = {id:1, verse_key:"1:1", text_madani:"بِسْمِ...", words:[...]}
```

### جلب صوت قارئ
```javascript
// MP3Quran.net (مباشر — بدون API)
const audioUrl = `https://server8.mp3quran.net/afs/001.mp3`;
// server8 = مشاري العفاسي
```

### البحث
```javascript
const searchRes = await fetch(
  'https://api.quran.com/api/v3/search?q=الرحمن&per_page=10'
);
const { search } = await searchRes.json();
// search.results = [{verse_key:"1:3", text:"الرَّحْمَـٰنِ...", ...}]
```

---

## ٧. مقارنة المصادر

| الميزة | api.quran.com (v3) | api.quran.com (v4) | alquran.cloud (الحالي) |
|--------|--------------------|--------------------|----------------------|
| **المصادقة** | ❌ لا يحتاج | ✅ OAuth2 | ❌ لا يحتاج |
| **عدد endpoints** | 5 شغالة | 73+ | ~5 |
| **الآيات** | ✅ | ✅ | ✅ |
| **البحث** | ✅ | ✅ | ❌ |
| **الترجمة** | ❌ (محذوف) | ✅ | محدود |
| **التفاسير** | ❌ (محذوف) | ✅ | ❌ |
| **الصوت** | ❌ (محذوف) | ✅ (16 قارئ) | ✅ (قارئ واحد) |
| **صور المصحف** | ❌ | عبر `image_url` | ❌ |
| **توثيق** | قديم | [api-docs.quran.foundation](https://api-docs.quran.foundation) | بسيط |
| **SDK** | `@quranjs/api` | `@quranjs/api` | ❌ |

---

## ٨. خطة التنفيذ المقترحة

### المرحلة ١ — استخدام v3 (بدون تسجيل)
```javascript
// работают بدون مصادقة:
GET /api/v3/chapters                    // ✅ السور
GET /api/v3/chapters/{id}/verses       // ✅ الآيات (مع words=true)
GET /api/v3/juzs                        // ✅ الأجزاء
GET /api/v3/search?q=...                // ✅ البحث
```

### المرحلة ٢ — تسجيل تطبيق و启用 v4
1. التسجيل في https://dev-console.quran.foundation
2. جلب `client_id` و `client_secret`
3. حفظهم في environment variables
4. جلب التوكن في runtime
5. استخدام الـ endpoints الكاملة (ترجمات، تفاسير، صوت)

### المرحلة ٣ — بناء quran.html
| الخطوة | الوصف |
|--------|-------|
| 1 | تحميل السور من `/api/v3/chapters` |
| 2 | عرض قائمة السور (اسم عربي + رقم + عدد آيات) |
| 3 | عند النقر → جلب الآيات من `/api/v3/chapters/{id}/verses?words=true` |
| 4 | عرض الآيات مع نص عثماني + ترجمة (إن أمكن) |
| 5 | تشغيل الصوت من MP3Quran.net |
| 6 | إضافة فلتر: جزء / حزب / صفحة |
| 7 | إضافة بحث |

---

## ٩. ملاحظات تقنية

1. **rate limiting:** v3 لا يوجد rate limit رسمي — لكن لا نكثر الطلبات
2. **CORS:** v3 يدعم CORS — يشتغل من المتصفح مباشرة
3. **JSON:** كل الـ endpoints ترجع JSON
4. **اللغة:** `language=ar` يدعم العربية في معظم الـ endpoints
5. **ترقيم الصفحات:** `per_page` و `page` — العدد الافتراضي يتغير حسب الـ endpoint
