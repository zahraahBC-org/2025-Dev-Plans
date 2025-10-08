# 03. إدارة الإصدارات | Version Management

## 🎯 **نظرة عامة | Overview**

إدارة شاملة لإصدارات الـ API، الإيقاف، والترحيل بين الإصدارات.

**الهدف | Purpose**: إدارة دورة حياة الإصدارات  
**الجمهور | Audience**: Product Managers، Backend، DevRel  
**المتطلبات | Prerequisites**: فهم [الإصدار](../01-Core-Principles/02_Versioning_URLs.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [سياسة الإصدار](#سياسة-الإصدار)
2. [Deprecation](#deprecation)
3. [الترحيل](#الترحيل)
4. [التشغيل المتوازي](#التشغيل-المتوازي)
5. [Changelog](#changelog)

---

## 1️⃣ سياسة الإصدار | Versioning Policy {#سياسة-الإصدار}

### **Semantic Versioning**

```
v{MAJOR}.{MINOR}.{PATCH}

MAJOR: تغييرات كاسرة
MINOR: ميزات جديدة متوافقة
PATCH: إصلاحات فقط

أمثلة:
v1.0.0 → v1.1.0  (ميزة جديدة)
v1.1.0 → v1.1.1  (إصلاح)
v1.1.1 → v2.0.0  (تغيير كاسر)
```

**في المسارات**: فقط MAJOR (`/v1`, `/v2`)

---

## 2️⃣ Deprecation | الإيقاف {#deprecation}

### **الجدول الزمني**

```
اليوم 0:    إعلان
اليوم 30:   تحذيرات
اليوم 60:   v2 إطلاق (متوازي)
اليوم 90:   بدء التضييق
اليوم 120:  إيقاف نهائي
```

---

### **رؤوس Deprecation**

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Wed, 08 Apr 2025 12:00:00 GMT
Link: </v2/products>; rel="alternate"
Warning: 299 - "This API version will be sunset on 2025-04-08. Migrate to /v2"
```

---

## 3️⃣ الترحيل | Migration {#الترحيل}

### **دليل الترحيل**

```markdown
# دليل الترحيل: v1 → v2

## التغييرات الكاسرة

### Products API

#### تغيير 1: حقل `price` أصبح كائن
```json
# v1
{
  "price": 299.00,
  "currency": "SAR"
}

# v2
{
  "price": {
    "amount": 299.00,
    "currency": "SAR"
  }
}
```

**Migration**:
```javascript
// قبل
const price = product.price;

// بعد
const price = product.price.amount;
```

#### تغيير 2: حقل `images` أصبح مصفوفة كائنات
```json
# v1
{
  "images": [
    "https://cdn.com/image1.jpg",
    "https://cdn.com/image2.jpg"
  ]
}

# v2
{
  "images": [
    {
      "url": "https://cdn.com/image1.jpg",
      "alt": "صورة رئيسية",
      "order": 1
    }
  ]
}
```

---

## 4️⃣ التشغيل المتوازي | Parallel Running {#التشغيل-المتوازي}

### **استراتيجية النشر**

```
Week 1-4:   v1 فقط (100%)
Week 5:     v1 (100%) + v2 Beta
Week 6-8:   v1 (95%) + v2 (5%) - Canary
Week 9-12:  v1 (70%) + v2 (30%)
Week 13-16: v1 (30%) + v2 (70%)
Week 17+:   v2 فقط (100%) - v1 أُوقف
```

---

## 5️⃣ Changelog | سجل التغييرات {#changelog}

### **تنسيق Changelog**

```markdown
# Changelog

## [2.0.0] - 2025-02-01

### Added
- حقل `rating` في Products
- Endpoint `/v2/recommendations`
- دعم WebP للصور

### Changed
- 🔴 BREAKING: `price` أصبح كائن
- 🔴 BREAKING: `images` أصبح مصفوفة كائنات
- تحسين أداء `/products` بنسبة 40%

### Deprecated
- حقل `old_field` في Orders (سيُزال في v3)

### Removed
- 🔴 حقل `legacy_id`
- 🔴 Endpoint `/v1/old-api`

### Fixed
- إصلاح حساب الضريبة
- إصلاح Pagination cursor

### Security
- تحديث JWT library
- إصلاح CORS configuration
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند إصدار نسخة جديدة**
- [ ] SemVer صحيح
- [ ] Changelog محدث
- [ ] Migration guide جاهز
- [ ] Deprecation headers
- [ ] إشعارات للمستخدمين
- [ ] فترة تشغيل متوازي
- [ ] اختبارات لكلا الإصدارين
- [ ] مراقبة الاستخدام

---

## 🔗 **التنقل | Navigation**

[← السابق: معايير البيانات | Previous: Data Standards](02_Data_Standards.md)

[التالي: التوافقية | Next: Compatibility & External →](04_Compatibility_External.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
