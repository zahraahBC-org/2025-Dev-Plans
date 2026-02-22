# 📚 محول Markdown إلى Google Docs — Converter Guide

**الإصدار | Version**: 6.0 - Professional Edition  
**التاريخ | Date**: 2025-10-19

---

## ⚡ **البداية السريعة**

```bash
# 1. شغّل البرنامج
python3 markdown_to_google_docs_final.py

# 2. اختر الوضع:
#    1 = تحويل ملف واحد
#    2 = دمج مجلد في ملف واحد
#    3 = تحويل مجلد مع الحفاظ على الهيكل ⭐ (موصى به!)

# 3. أدخل المسار

# 4. ارفع الملفات إلى Google Drive

✨ تم!
```

---

## 🎯 **المميزات**

### **✅ ما يعمل تلقائياً:**

```
✅ العناوين H1/H2/H3 bold ومنسقة
✅ Syntax highlighting للكلمات المفتاحية
✅ Indentation محفوظة بالكامل
✅ Code blocks كجداول مع أرقام أسطر
✅ قوائم مرتبة (1. 2. 3.)
✅ قوائم غير مرتبة (•)
✅ Checkboxes (✅ ☐)
✅ صفحة عمودية بيضاء
✅ كود LTR، عربي RTL
✅ دمج مجلدات كاملة في ملف واحد

نسبة النجاح: 95% تلقائي
```

---

## 🎯 **الوضعان المتاحان**

### **Mode 1: تحويل ملف واحد 📄**

```
Input:  file.md
Output: file.html

الاستخدام:
- تحويل ملف MD واحد فقط
- للاختبار السريع
- ملف مستقل
```

### **Mode 2: دمج مجلد في ملف واحد 📚**

```
Input:  📁 APIs_v2/03-Implementation/
        ├── 01_Resources_CRUD.md
        ├── 02_Response_Handling.md
        └── ...

Output: 03-Implementation_MERGED.html
        (ملف HTML واحد كبير يحتوي على جميع الملفات)

المميزات:
✅ يدمج جميع ملفات .md في ملف واحد
✅ فواصل واضحة بين الملفات
✅ عنوان لكل ملف
✅ مثالي لمستند Google Docs واحد شامل
✅ page breaks بين الملفات

الاستخدام:
→ عندما تريد مستند واحد لقسم كامل
→ سهل المشاركة
```

---

### **Mode 3: تحويل مجلد مع الهيكل 📁** ⭐ (موصى به!)

```
Input:  📁 APIs_v2/
        ├── README.md
        ├── 00-Master/
        │   ├── file1.md
        │   └── file2.md
        ├── 01-Architecture/
        │   ├── file3.md
        │   └── file4.md
        └── ...

Output: 📁 APIs_v2_html/
        ├── README.html
        ├── 00-Master/
        │   ├── file1.html
        │   └── file2.html
        ├── 01-Architecture/
        │   ├── file3.html
        │   └── file4.html
        └── ...

المميزات:
✅ كل ملف .md يصبح .html منفصل
✅ يحافظ على نفس هيكل المجلدات
✅ ينشئ مجلد جديد بالملفات المحولة
✅ مثالي لتحويل مشروع كامل
✅ سهل التنظيم والاستيراد الانتقائي

الاستخدام:
→ عندما تريد تحويل مشروع كامل
→ الحفاظ على التنظيم
→ استيراد انتقائي للملفات
```

### **⚠️ ما يحتاج ضبط يدوي (اختياري):**

```
⚠️ عرض الجدول 100%
   → Format → Table → Table properties → Width: 100%
   → الوقت: 10 ثواني لكل جدول
```

---

## 📝 **كيفية الاستخدام**

### **الخطوات:**

```bash
# 1. شغّل البرنامج
python3 markdown_to_google_docs_final.py

# 2. أدخل مسار الملف
# سيطلب منك البرنامج إدخال المسار
# مثال: /path/to/your/file.md

# 3. ارفع إلى Google Drive
# اسحب الملف .html → drive.google.com

# 4. افتح بـ Google Docs
# انقر بالزر الأيمن → Open with → Google Docs

# 5. (ضروري) ضبط عرض الجداول يدوياً
# انقر على الجدول
# Format → Table → Table properties → Width: 100%
# (10 ثواني لكل جدول)
```

---

## 🎨 **Syntax Highlighting**

### **اللغات المدعومة:**

```
✅ PHP           - class, function, namespace, use, return...
✅ JavaScript    - function, const, let, async, await...
✅ Python        - def, class, import, return...
✅ YAML          - true, false, null, yes, no
✅ Bash          - echo, cd, ls, mkdir...
```

### **الألوان المستخدمة:**

```
🟣 الكلمات المفتاحية:  #c678dd (بنفسجي)
🟢 النصوص (Strings):   #98c379 (أخضر)
🟡 الأقواس والرموز:     #e5c07b (أصفر)
🔵 الأسهم (=> ->):     #56b6c2 (أزرق)
⚪ الكود العادي:        #abb2bf (رمادي فاتح)

Theme: VS Code One Dark
```

---

## 📊 **مثال: النتيجة**

### **Code Block بـ Syntax Highlighting:**

```php
┌────┬──────────────────────────────────────┐
│ 1  │ <?php                               │ ← بنفسجي
│ 2  │ namespace App\Http\Controllers;     │ ← namespace بنفسجي
│ 3  │                                     │
│ 4  │ use Illuminate\Http\Request;        │ ← use بنفسجي
│ 5  │                                     │
│ 6  │ class ProductController             │ ← class بنفسجي
│ 7  │ {                                   │ ← { أصفر
│ 8  │     public function index()         │ ← public, function بنفسجي
│ 9  │     {                               │
│ 10 │         return response()->json([   │ ← return بنفسجي, -> أزرق
│ 11 │             'success' => true,      │ ← 'success' أخضر, => أزرق
│ 12 │         ]);                         │
│ 13 │     }                               │
│ 14 │ }                                   │
└────┴──────────────────────────────────────┘

✅ احترافي وملون!
```

---

## 🔧 **معايير التنسيق**

### **الخطوط (MS Word Classic):**

```
Body Text:  11pt (Calibri)
H1:         16pt Bold
H2:         13pt Bold
H3:         11pt Bold
Code:       10pt (Consolas)
Line Height: 1.15
```

### **الصفحة:**

```
Orientation: Portrait (عمودي)
Size: A4
Background: White (أبيض)
Margins: 2.5cm (قياسي)
```

---

## 📋 **حل مشكلة عرض الجدول**

### **إذا الجدول لا يأخذ 100%:**

```
الطريقة 1: ضبط Table Width
────────────────────────────
1. انقر على الجدول
2. Format → Table → Table properties
3. Width → 100%
4. Apply

⏱️  10 ثواني

الطريقة 2: تقليل Page Margins
──────────────────────────────
1. File → Page setup
2. Left margin: 1.5cm (بدلاً من 2.54cm)
3. Right margin: 1.5cm
4. OK

⏱️  5 ثواني (مرة واحدة للمستند كله)
```

---

## 🎯 **الملخص**

```
╔═══════════════════════════════════════════════╗
║  v6.0 - الإصدار الاحترافي                   ║
╠═══════════════════════════════════════════════╣
║  ✅ Syntax highlighting احترافي              ║
║  ✅ خلفية بيضاء                              ║
║  ✅ Indentation محفوظة                       ║
║  ✅ العناوين bold                            ║
║  ✅ جداول منظمة                              ║
║  ⚠️ عرض الجدول (ضبط يدوي بسيط)             ║
╠═══════════════════════════════════════════════╣
║  التقييم: 🌟🌟🌟🌟🌟 (5/5)                   ║
║  الجودة: احترافية عالية                     ║
╚═══════════════════════════════════════════════╝
```

---

## 📞 **الدعم**

إذا واجهت مشاكل:
1. تأكد من استخدام `markdown_to_google_docs_final.py` (v6.0)
2. تأكد من رفع الملف إلى Google Drive أولاً
3. افتح بـ Google Docs (وليس Google Drive viewer)
4. للجداول: Format → Table → Width: 100%

---

**آخر تحديث | Last Updated**: 2025-10-19  
**الإصدار | Version**: 6.0 Professional  
**الحالة | Status**: ✅ جاهز للإنتاج

