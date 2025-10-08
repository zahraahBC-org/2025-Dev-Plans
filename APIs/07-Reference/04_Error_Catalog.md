# 04. كتالوج الأخطاء | Error Catalog

## 🎯 **نظرة عامة | Overview**

مرجع شامل لجميع أكواد الأخطاء المحتملة، أسبابها، وطرق حلها.

**الهدف | Purpose**: توثيق جميع أكواد الأخطاء  
**الجمهور | Audience**: المطورون، فرق الدعم، QA  
**الاستخدام | Usage**: مرجع لفهم وحل الأخطاء

---

## 📋 **هيكل الأكواد | Code Structure**

```
E + XYZZ

X    = الفئة (1-7)
YZZ  = رقم فريد داخل الفئة

أمثلة:
E1001 - خطأ طلب
E2001 - خطأ مصادقة
E3001 - مورد غير موجود
```

---

## 1️⃣ E1xxx - أخطاء الطلب | Request Errors

| الكود | الوصف | HTTP | الحل |
|------|-------|------|-----|
| **E1001** | Invalid JSON format | 400 | تحقق من صيغة JSON |
| **E1002** | Missing required header | 400 | أضف الـ header المطلوب |
| **E1003** | Invalid content type | 400 | استخدم `application/json` |
| **E1004** | Request body too large | 413 | قلل حجم الطلب (max 1MB) |
| **E1005** | Invalid query parameter | 400 | تحقق من المعاملات |

### **أمثلة**

#### **E1001 - Invalid JSON**
```json
{
  "error": {
    "code": "E1001",
    "message": "Invalid JSON format",
    "details": "Unexpected token at position 45",
    "trace_id": "c9b1f3a0..."
  }
}
```

**السبب**: JSON syntax error  
**الحل**: تحقق من الأقواس، الفواصل، الاقتباسات

---

## 2️⃣ E2xxx - أخطاء المصادقة/التخويل | Auth Errors

| الكود | الوصف | HTTP | الحل |
|------|-------|------|-----|
| **E2001** | Authentication required | 401 | أضف Authorization header |
| **E2002** | Insufficient permissions | 403 | اطلب صلاحيات أعلى |
| **E2003** | Token expired | 401 | جدد التوكن |
| **E2004** | Invalid token | 401 | احصل على توكن جديد |
| **E2005** | Token revoked | 401 | أعد تسجيل الدخول |
| **E2006** | Invalid OTP | 401 | تحقق من الرمز |
| **E2007** | OTP expired | 401 | اطلب رمز جديد |
| **E2008** | Too many OTP attempts | 429 | انتظر 60 ثانية |

### **أمثلة**

#### **E2001 - Authentication Required**
```json
{
  "error": {
    "code": "E2001",
    "message": "Authentication required",
    "details": "Missing Authorization header with Bearer token",
    "trace_id": "c9b1f3a0..."
  }
}
```

**الحل للعميل**:
```javascript
// أضف header
headers: {
  'Authorization': `Bearer ${accessToken}`
}
```

---

#### **E2003 - Token Expired**
```json
{
  "error": {
    "code": "E2003",
    "message": "Access token expired",
    "details": "Token expired at 2025-01-08T12:15:00Z",
    "trace_id": "c9b1f3a0..."
  }
}
```

**الحل للعميل**:
```javascript
// استخدم refresh token
const response = await fetch('/v1/auth/refresh', {
  method: 'POST',
  body: JSON.stringify({ refresh_token: refreshToken })
});
```

---

## 3️⃣ E3xxx - أخطاء الموارد | Resource Errors

| الكود | الوصف | HTTP | الحل |
|------|-------|------|-----|
| **E3001** | Resource not found | 404 | تحقق من ID |
| **E3002** | Resource already exists | 409 | استخدم مورد موجود |
| **E3003** | Resource deleted | 410 | المورد محذوف نهائيًا |
| **E3004** | Parent resource not found | 404 | تحقق من المورد الأب |

---

## 4️⃣ E4xxx - منطق الأعمال | Business Logic Errors

| الكود | الوصف | HTTP | الحل |
|------|-------|------|-----|
| **E4001** | Insufficient stock | 422 | قلل الكمية أو اختر منتج آخر |
| **E4002** | Invalid order state | 422 | لا يمكن تنفيذ العملية في هذه الحالة |
| **E4003** | Payment declined | 422 | جرب طريقة دفع أخرى |
| **E4004** | Coupon expired | 422 | استخدم قسيمة صالحة |
| **E4005** | Coupon already used | 422 | القسيمة مستخدمة سابقًا |
| **E4006** | Minimum order not met | 422 | أضف منتجات (الحد الأدنى 50 ريال) |
| **E4007** | Delivery area not covered | 422 | اختر عنوان آخر |
| **E4008** | COD not allowed | 422 | استخدم الدفع عبر الإنترنت |

### **أمثلة**

#### **E4001 - Insufficient Stock**
```json
{
  "error": {
    "code": "E4001",
    "message": "Insufficient stock",
    "details": {
      "variant_id": 123,
      "requested": 5,
      "available": 2
    },
    "trace_id": "c9b1f3a0..."
  }
}
```

**الحل للعميل**:
- عرض رسالة: "متبقي فقط 2 قطع"
- اقتراح منتجات بديلة
- تمكين التنبيهات عند التوفر

---

## 5️⃣ E5xxx - التحقق | Validation Errors

| الكود | الوصف | HTTP | مثال |
|------|-------|------|------|
| **E5001** | Validation failed | 422 | أخطاء حقول متعددة |
| **E5002** | Invalid email | 422 | تنسيق بريد خاطئ |
| **E5003** | Invalid phone | 422 | تنسيق هاتف خاطئ |
| **E5004** | Invalid date format | 422 | استخدم ISO-8601 |

### **مثال E5001 - Validation Failed**
```json
{
  "error": {
    "code": "E5001",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "rule": "email",
        "message": "يجب أن يكون بريد إلكتروني صالح",
        "value": "invalid-email"
      },
      {
        "field": "phone",
        "rule": "regex",
        "message": "رقم الهاتف يجب أن يبدأ بـ +9665",
        "value": "0501234567"
      }
    ],
    "trace_id": "c9b1f3a0..."
  }
}
```

---

## 6️⃣ E6xxx - Rate Limiting

| الكود | الوصف | HTTP | الحل |
|------|-------|------|-----|
| **E6001** | Rate limit exceeded | 429 | انتظر حتى reset time |
| **E6002** | Too many OTP requests | 429 | انتظر 60 ثانية |
| **E6003** | Too many failed attempts | 429 | انتظر 5 دقائق |

---

## 7️⃣ E7xxx - أخطاء الخادم | Server Errors

| الكود | الوصف | HTTP | الإجراء |
|------|-------|------|--------|
| **E7001** | Internal server error | 500 | تم إبلاغ الفريق التقني |
| **E7002** | Database connection failed | 503 | إعادة المحاولة بعد قليل |
| **E7003** | Service unavailable | 503 | صيانة مجدولة |
| **E7004** | Gateway timeout | 504 | إعادة المحاولة |

---

## 📊 **إحصائيات الأخطاء | Error Statistics**

### **الأخطاء الأكثر شيوعًا**
```
1. E5001 - Validation failed     (35%)
2. E3001 - Resource not found    (25%)
3. E2001 - Auth required          (20%)
4. E4001 - Insufficient stock     (10%)
5. E6001 - Rate limit             (5%)
6. E7001 - Internal error         (3%)
7. Others                         (2%)
```

---

## 🔗 **التنقل | Navigation**

[← السابق: مرجع سريع | Previous: Quick Reference](03_Quick_Reference.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved