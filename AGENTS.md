# AGENTS.md

موقع ثابت (HTML/CSS/JS بدون build أو framework). كل التعديلات منشورة عبر GitHub Pages.

## بنية مهمة

- `src/` يحتوي صفحات HTML: index.html, adhkar.html, dhikr.html, quran.html, wird.html, ahadith.html, salah.html, misbaha.html, tafsir.html
- `data/adhkar.json` و `data/ahadith.json` — ملفات بيانات الأذكار والأحاديث

## حقائق غير واضحة من الأسماء

- `src/adhkar.html` و `src/ahadith.html` يجيبان بياناتهما عبر `fetch` من **GitHub raw** وليس ملف محلي:
  - `https://raw.githubusercontent.com/Gameman2012/athkar/main/data/adhkar.json`
  - `https://raw.githubusercontent.com/Gameman2012/athkar/main/data/ahadith.json`
  هذا مقصود ليشتغل على GitHub Pages ويفصل البيانات عن الكود. لا تغيره لـ `data/...` إلا إذا نقلت الملفات للـ root.
- فلاتر الأذكار/الأحاديث تتولد ديناميكياً من حقل `tags` في JSON.
- `src/dhikr.html` يستخدم `https://api.aladhan.com/v1/timingsByIp` لكشف الوقت تلقائياً.
- `src/salah.html` يستخدم `https://api.aladhan.com/v1/timingsByIp?method=2` (MWL) لكشف الموقع والوقت تلقائياً.
- `src/quran.html` يستخدم:
  - `https://api.alquran.cloud/v1` للنصوص
  - `https://cdn.islamic.network/quran/audio/128/ar.alafasy/{ayah_number}.mp3` للصوت
  - `https://quran.islam-db.com/public/data/pages/quranpages_1024/images/page{NNN}.png` لصور المصحف
- `src/wird.html` يستخدم `https://quran.islam-db.com/public/data/pages/quranpages_1024/images/page{NNN}.png` — صفحة واحدة يومياً.
- `src/misbaha.html` — مسبحة رقمية: عداد دائري مع Web Audio click + localStorage + 8 أذكار جاهزة.
- `src/tafsir.html` — تدبر آية: آية عشوائية مع تفسير الجلالين (API: alquran.cloud). 30 آية مختارة.
- البطاقات في `index.html` تستخدم `<a href="...">` لصفحات الموقع.

## أوامر

لا يوجد build/test/lint. للتحقق من صحة JSON:
```
python3 -c "import json; json.load(open('data/adhkar.json'))"
python3 -c "import json; json.load(open('data/ahadith.json'))"
```

## نشر / git

- الريبو: `https://github.com/Gameman2012/athkar` على فرع `main`.
- عند الرفع: الريموت قد يحتوي محتوى سابق، استخدم:
  `git pull origin main --rebase` ثم `git push`.
- أي تعديل على `data/adhkar.json` أو `data/ahadith.json` ينعكس تلقائياً بعد النشر.

## اتفاقيات

- نصوص الأذكار تُكتب بالتشكيل الكامل. الحقل `source` يذكر اسم الكتاب/الراوي.
- `footer` = ملاحظة/فائدة إضافية للذكر. لا تجعله خاطئاً في النسبة.
- الوصف في README.md هو المرجع للمستخدم؛ هذا الملف للـ agent فقط.
