# 🎓 موقع تخرج محمد

موقع مفاجأة تفاعلي لمحمد بمناسبة تخرجه، مبني بـ Flask + SQLite/PostgreSQL.

---

## 📁 هيكل المشروع

```
mohammed-grad/
├── app.py               ← التطبيق الرئيسي
├── requirements.txt     ← المكتبات
├── render.yaml          ← إعدادات Render
├── Procfile             ← أمر التشغيل
└── templates/
    ├── base.html        ← القالب الأساسي المشترك
    ├── index.html       ← الصفحة الرئيسية
    ├── quiz.html        ← صفحة الأسئلة
    ├── unlock.html      ← صفحة كلمة المرور
    ├── letters.html     ← صفحة الرسائل (الظرف)
    ├── write.html       ← صفحة كتابة رسالة
    └── finale.html      ← صفحة الختام
```

---

## 🚀 رفع الموقع على GitHub + Render

### الخطوة 1 — إنشاء Repo على GitHub
1. روح [github.com](https://github.com) وسجل دخول
2. اضغط **New repository**
3. اسم الـ repo: `mohammed-graduation`
4. اجعله **Private** (عشان ما يشوفه محمد)
5. اضغط **Create repository**

### الخطوة 2 — رفع الملفات
```bash
cd mohammed-grad
git init
git add .
git commit -m "🎓 Mohammed graduation surprise"
git remote add origin https://github.com/USERNAME/mohammed-graduation.git
git push -u origin main
```

### الخطوة 3 — ربطه بـ Render
1. روح [render.com](https://render.com) وسجل دخول
2. اضغط **New** → **Web Service**
3. اربطه بـ GitHub وأختار الـ repo
4. الإعدادات:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. في **Environment Variables** أضف:
   - `SECRET_KEY` = أي نص عشوائي طويل
   - `ADMIN_PASSWORD` = كلمة المرور اللي تختارها (الافتراضي: `mohammed2025`)
6. اضغط **Create Web Service**

بعد دقيقتين الموقع يكون شغال! ✅

---

## 🔗 الروابط

| الصفحة | الرابط |
|--------|--------|
| الصفحة الرئيسية | `yoursite.onrender.com/` |
| صفحة الأسئلة | `yoursite.onrender.com/quiz` |
| صفحة الرسائل | `yoursite.onrender.com/letters` (تحتاج كلمة مرور) |
| كتابة رسالة | `yoursite.onrender.com/write` ← أرسل هذا الرابط لأهله وأصحابه |
| الختام | `yoursite.onrender.com/finale` |

---

## ⚙️ تعديل الرسائل الافتراضية

في `app.py` ابحث عن `samples` وعدّل الرسائل الثلاث أو احذفها واتركها فارغة:
```python
samples = []  # ← خلها فارغة لو تبي
```

## 🔐 تغيير كلمة المرور

في Environment Variables على Render غيّر `ADMIN_PASSWORD` لأي كلمة تريدها.

---

## 💡 نصائح

- **أرسل رابط `/write`** لكل أهله وأصحابه قبل يوم التخرج بأسبوع على الأقل
- **الرسائل محفوظة** في قاعدة بيانات SQLite على الخادم
- **لو تبي تشيل الرسائل الافتراضية** من app.py احذف الـ `samples` block
- **كلمة المرور الافتراضية:** `mohammed2025` — غيّرها من Render

---

صُنع بكل حب ❤️
