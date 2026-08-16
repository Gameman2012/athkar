# AGENTS.md

موقع ثابت (HTML/CSS/JS بدون build أو framework). كل التعديلات منشورة عبر GitHub Pages.

## بنية مهمة

- `src/` يحتوي صفحات HTML (`index.html`, `adhkar.html`). المسارات النسبية من داخل `src/` تذهب للأعلى أولاً (`../data/...`).
- `data/adhkar.json` مصدر البيانات الوحيد للأذكار. ملف JSON واحد لكل الأقسام (ليس ملف لكل tag).

## حقائق غير واضحة من الأسماء

- `src/adhkar.html` يجيب بياناته عبر `fetch` من **GitHub raw** وليس ملف محلي:
  `https://raw.githubusercontent.com/Gameman2012/athkar/main/data/adhkar.json`
  هذا مقصود ليشتغل على GitHub Pages ويفصل البيانات عن الكود. لا تغيره لـ `data/...` إلا إذا نقلت الملفات للـ root.
- فلاتر الصفحة (صباح/مساء/صلاة/نوم/طعام/سفر/عادات) تتولد ديناميكياً من حقل `tags` في JSON، وكل ذكر يمكن أن يحمل أكثر من tag.
- البطاقات في `index.html` تستخدم `<a href="...">` لصفحات placeholder لم تُنشأ بعد (quran.html, dhikr.html, wird.html, ahadith.html).

## أوامر

لا يوجد build/test/lint. للتحقق من صحة JSON:
```
python3 -c "import json; json.load(open('data/adhkar.json'))"
```

## نشر / git

- الريبو: `https://github.com/Gameman2012/athkar` على فرع `main`.
- عند الرفع: الريموت قد يحتوي محتوى سابق، استخدم:
  `git pull origin main --rebase` ثم `git push`.
- أي تعديل على `data/adhkar.json` ينعكس تلقائياً بعد النشر (تجاوز كاش المتصفح عند الاختبار).

## اتفاقيات

- نصوص الأذكار تُكتب بالتشكيل الكامل. الحقل `source` يذكر اسم الكتاب/الراوي (مسلم، البخاري، أبو داود، الترمذي، ابن ماجه، الطبراني).
- `footer` = ملاحظة/فائدة إضافية للذكر (عدد التكرار، فضل، وقت القول). لا تجعله خاطئاً في النسبة (مثل نسبة دعاء لغيره).
- الوصف في README.md هو المرجع للمستخدم؛ هذا الملف للـ agent فقط.
