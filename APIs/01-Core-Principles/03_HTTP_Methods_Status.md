# 03. أساليب HTTP وحالات الاستجابة | HTTP Methods & Status Codes

## 🎯 **نظرة عامة | Overview**

دليل شامل لاستخدام أساليب HTTP الصحيحة وإرجاع حالات الاستجابة المناسبة.

**الهدف | Purpose**: تحديد استخدام HTTP Methods والـ Status Codes  
**الجمهور | Audience**: مطورو الـ Backend، مهندسو الـ API  
**المتطلبات | Prerequisites**: فهم [مبادئ REST](01_REST_Design_Principles.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [أساليب HTTP](#أساليب-http)
2. [حالات الاستجابة](#حالات-الاستجابة)
3. [Idempotency](#idempotency)
4. [أمثلة عملية](#أمثلة-عملية)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ أساليب HTTP | HTTP Methods {#أساليب-http}

### **GET - القراءة | Read**

#### **الهدف**
استرجاع مورد أو قائمة موارد **بدون تعديل**.

#### **الخصائص**
- ✅ **Safe**: لا يُعدّل البيانات
- ✅ **Idempotent**: استدعاءات متعددة = نفس النتيجة
- ✅ **Cacheable**: قابل للتخزين المؤقت

#### **الاستخدامات**
```http
GET /v1/products              ← قائمة جميع المنتجات
GET /v1/products/123          ← منتج محدد
GET /v1/products/123/reviews  ← مراجعات المنتج
```

#### **الاستجابة النموذجية**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e"

{
  "data": {
    "id": 123,
    "name_ar": "فستان صيفي",
    "price": 299.00
  }
}
```

**قواعد GET**:
- ❌ لا تُعدّل البيانات أبدًا
- ❌ لا معاملات حساسة في URL
- ✅ استخدم معاملات الاستعلام للتصفية
- ✅ دعم ETag وCache-Control

---

### **POST - الإنشاء | Create**

#### **الهدف**
إنشاء مورد جديد أو تنفيذ عملية.

#### **الخصائص**
- ❌ **Not Safe**: يُعدّل البيانات
- ❌ **Not Idempotent** (عادةً)
- ❌ **Not Cacheable**

#### **الاستخدامات**
```http
POST /v1/orders           ← إنشاء طلب جديد
POST /v1/products         ← إنشاء منتج جديد
POST /v1/auth/login       ← تسجيل دخول (عملية)
```

#### **الطلب النموذجي**
```http
POST /v1/orders
Content-Type: application/json
Idempotency-Key: c5a8bd76-b6d9-4c49-8e1a-1b2c3d4e5f6g

{
  "customer_id": 789,
  "items": [
    {
      "variant_id": 123,
      "quantity": 2
    }
  ]
}
```

#### **الاستجابة النموذجية**
```http
HTTP/1.1 201 Created
Location: /v1/orders/ORD-20250108-00123
Content-Type: application/json

{
  "id": "ORD-20250108-00123",
  "status": "pending",
  "total": 598.00,
  "created_at": "2025-01-08T12:00:00Z"
}
```

**قواعد POST**:
- ✅ إرجاع `201 Created` عند النجاح
- ✅ إضافة رأس `Location` للمورد الجديد
- ✅ استخدام `Idempotency-Key` للعمليات المالية
- ✅ إرجاع تمثيل المورد الجديد

---

### **PUT - الاستبدال الكامل | Full Replacement**

#### **الهدف**
استبدال مورد كامل بتمثيل جديد.

#### **الخصائص**
- ❌ **Not Safe**: يُعدّل البيانات
- ✅ **Idempotent**: استدعاءات متعددة = نفس النتيجة
- ❌ **Not Cacheable**

#### **الاستخدامات**
```http
PUT /v1/products/123      ← استبدال المنتج كاملاً
PUT /v1/customers/789     ← استبدال العميل كاملاً
```

#### **الطلب النموذجي**
```http
PUT /v1/products/123
Content-Type: application/json
If-Match: "33a64df551425fcc55e"

{
  "name_ar": "فستان صيفي محدث",
  "name_en": "Updated Summer Dress",
  "price": 349.00,
  "is_active": true,
  "category_id": 12,
  "brand_id": 45
}
```

**ملاحظة**: يجب تضمين **جميع** الحقول المطلوبة.

#### **الاستجابة النموذجية**
```http
HTTP/1.1 200 OK
ETag: "9f4b2c8e1d3a5f7b9c0e"
Content-Type: application/json

{
  "id": 123,
  "name_ar": "فستان صيفي محدث",
  "price": 349.00,
  "updated_at": "2025-01-08T12:30:00Z"
}
```

**قواعد PUT**:
- ✅ استبدال كامل للمورد
- ✅ استخدام `If-Match` مع ETag لمنع Lost Updates
- ✅ إرجاع `200 OK` أو `204 No Content`
- ❌ لا تستخدمه للتحديثات الجزئية

---

### **PATCH - التحديث الجزئي | Partial Update**

#### **الهدف**
تحديث جزئي لبعض حقول المورد فقط.

#### **الخصائص**
- ❌ **Not Safe**: يُعدّل البيانات
- ⚠️ **Idempotent** (إذا صُمم بشكل صحيح)
- ❌ **Not Cacheable**

#### **الاستخدامات**
```http
PATCH /v1/products/123        ← تحديث بعض الحقول
PATCH /v1/orders/ORD-123      ← تحديث حالة الطلب
PATCH /v1/customers/789       ← تحديث بعض المعلومات
```

#### **الطلب النموذجي (JSON Merge Patch)**
```http
PATCH /v1/products/123
Content-Type: application/merge-patch+json
If-Match: "9f4b2c8e1d3a5f7b9c0e"

{
  "price": 279.00,
  "is_active": false
}
```

**ملاحظة**: فقط الحقول المُرسلة سيتم تحديثها.

#### **الاستجابة النموذجية**
```http
HTTP/1.1 200 OK
ETag: "1a2b3c4d5e6f7g8h9i0j"
Content-Type: application/json

{
  "id": 123,
  "price": 279.00,
  "is_active": false,
  "updated_at": "2025-01-08T12:45:00Z"
}
```

**قواعد PATCH**:
- ✅ فقط الحقول المُرسلة يتم تحديثها
- ✅ استخدام `If-Match` مع ETag
- ✅ دعم `application/merge-patch+json`
- ✅ إرجاع `200 OK` مع المورد المحدث

---

### **DELETE - الحذف | Delete**

#### **الهدف**
حذف مورد موجود.

#### **الخصائص**
- ❌ **Not Safe**: يُعدّل البيانات
- ✅ **Idempotent**: حذف نفس المورد عدة مرات = نفس النتيجة
- ❌ **Not Cacheable**

#### **الاستخدامات**
```http
DELETE /v1/products/123       ← حذف منتج
DELETE /v1/carts/456          ← حذف سلة
DELETE /v1/addresses/789      ← حذف عنوان
```

#### **الطلب النموذجي**
```http
DELETE /v1/products/123
If-Match: "1a2b3c4d5e6f7g8h9i0j"
```

#### **الاستجابة النموذجية**
```http
HTTP/1.1 204 No Content
```

**أو (مع تفاصيل)**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "تم حذف المنتج بنجاح",
  "deleted_at": "2025-01-08T13:00:00Z"
}
```

**قواعد DELETE**:
- ✅ إرجاع `204 No Content` (موصى به)
- ✅ أو `200 OK` مع رسالة تأكيد
- ✅ الحذف الثاني لنفس المورد = `404 Not Found`
- ⚠️ النظر في **Soft Delete** للبيانات الحساسة

---

## 2️⃣ حالات الاستجابة | HTTP Status Codes {#حالات-الاستجابة}

### **2xx - النجاح | Success**

| الكود | الاسم | الاستخدام | مثال |
|------|------|----------|------|
| **200** | OK | نجاح عام | GET، PUT، PATCH |
| **201** | Created | مورد جديد أُنشئ | POST |
| **202** | Accepted | تم قبول الطلب للمعالجة | عمليات غير متزامنة |
| **204** | No Content | نجاح بدون محتوى | DELETE |

#### **أمثلة**

**200 OK** - قراءة ناجحة
```http
GET /v1/products/123
⟶
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name_ar": "فستان صيفي"
}
```

**201 Created** - إنشاء ناجح
```http
POST /v1/orders
⟶
HTTP/1.1 201 Created
Location: /v1/orders/ORD-123

{
  "id": "ORD-123",
  "status": "pending"
}
```

**202 Accepted** - معالجة غير متزامنة
```http
POST /v1/reports
⟶
HTTP/1.1 202 Accepted
Location: /v1/jobs/job-456

{
  "job_id": "job-456",
  "status": "pending",
  "estimated_completion": "2025-01-08T13:30:00Z"
}
```

**204 No Content** - حذف ناجح
```http
DELETE /v1/products/123
⟶
HTTP/1.1 204 No Content
```

---

### **4xx - أخطاء العميل | Client Errors**

| الكود | الاسم | الاستخدام | مثال |
|------|------|----------|------|
| **400** | Bad Request | طلب خاطئ | JSON غير صحيح |
| **401** | Unauthorized | غير مصادق | رمز مفقود/منتهي |
| **403** | Forbidden | غير مصرح | صلاحيات ناقصة |
| **404** | Not Found | مورد غير موجود | معرف خاطئ |
| **409** | Conflict | تعارض | Idempotency Key مكرر |
| **422** | Unprocessable Entity | فشل التحقق | بيانات غير صالحة |
| **429** | Too Many Requests | تجاوز الحد | Rate Limit |

#### **أمثلة**

**400 Bad Request**
```http
POST /v1/orders
{
  "invalid_json": 
}
⟶
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "E1001",
    "message": "Invalid JSON format",
    "details": [
      {
        "field": "body",
        "issue": "syntax_error"
      }
    ],
    "trace_id": "c9b1f3a0..."
  }
}
```

**401 Unauthorized**
```http
GET /v1/orders
⟶
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="API"

{
  "error": {
    "code": "E2001",
    "message": "Authentication required",
    "details": "Missing or invalid access token"
  }
}
```

**403 Forbidden**
```http
DELETE /v1/products/123
Authorization: Bearer <customer-token>
⟶
HTTP/1.1 403 Forbidden

{
  "error": {
    "code": "E2002",
    "message": "Insufficient permissions",
    "details": "Admin role required for this operation"
  }
}
```

**404 Not Found**
```http
GET /v1/products/99999
⟶
HTTP/1.1 404 Not Found

{
  "error": {
    "code": "E3001",
    "message": "Product not found",
    "details": "No product with ID 99999"
  }
}
```

**409 Conflict**
```http
POST /v1/orders
Idempotency-Key: duplicate-key-123
⟶
HTTP/1.1 409 Conflict

{
  "error": {
    "code": "E4001",
    "message": "Idempotency key conflict",
    "details": "Key already used for different request"
  }
}
```

**422 Unprocessable Entity**
```http
POST /v1/orders
{
  "customer_id": "invalid",
  "items": []
}
⟶
HTTP/1.1 422 Unprocessable Entity

{
  "error": {
    "code": "E5001",
    "message": "Validation failed",
    "details": [
      {
        "field": "customer_id",
        "rule": "numeric",
        "message": "Customer ID must be numeric"
      },
      {
        "field": "items",
        "rule": "min:1",
        "message": "At least one item required"
      }
    ]
  }
}
```

**429 Too Many Requests**
```http
GET /v1/products
⟶
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704715200
Retry-After: 60

{
  "error": {
    "code": "E6001",
    "message": "Rate limit exceeded",
    "details": "Maximum 100 requests per minute"
  }
}
```

---

### **5xx - أخطاء الخادم | Server Errors**

| الكود | الاسم | الاستخدام | مثال |
|------|------|----------|------|
| **500** | Internal Server Error | خطأ داخلي عام | استثناء غير متوقع |
| **502** | Bad Gateway | خطأ من خدمة خلفية | فشل اتصال DB |
| **503** | Service Unavailable | الخدمة غير متوفرة | صيانة/زيادة حمل |
| **504** | Gateway Timeout | مهلة الخادم | استعلام طويل |

#### **أمثلة**

**500 Internal Server Error**
```http
GET /v1/products/123
⟶
HTTP/1.1 500 Internal Server Error

{
  "error": {
    "code": "E7001",
    "message": "Internal server error",
    "details": "An unexpected error occurred",
    "trace_id": "a1b2c3d4..."
  }
}
```

**503 Service Unavailable**
```http
GET /v1/products
⟶
HTTP/1.1 503 Service Unavailable
Retry-After: 300

{
  "error": {
    "code": "E7002",
    "message": "Service temporarily unavailable",
    "details": "Scheduled maintenance in progress"
  }
}
```

---

## 3️⃣ Idempotency | عدم التكرار {#idempotency}

### **التعريف**
عملية **Idempotent** تعني: تنفيذها عدة مرات = نفس النتيجة كتنفيذها مرة واحدة.

### **جدول Idempotency**

| الأسلوب | Idempotent؟ | ملاحظات |
|---------|------------|---------|
| GET | ✅ نعم | قراءة فقط |
| POST | ❌ لا | يُنشئ مورد جديد كل مرة |
| PUT | ✅ نعم | استبدال بنفس القيم |
| PATCH | ⚠️ يعتمد | إذا صُمم بشكل صحيح |
| DELETE | ✅ نعم | حذف مرتين = نفس النتيجة |

---

### **جعل POST Idempotent**

#### **استخدام Idempotency-Key**
```http
POST /v1/orders
Idempotency-Key: c5a8bd76-b6d9-4c49-8e1a-1b2c3d4e5f6g
Content-Type: application/json

{
  "customer_id": 789,
  "items": [...]
}
```

**السلوك**:
1. **الطلب الأول**: يُنشئ الطلب، يُخزّن المفتاح
2. **الطلب الثاني** (بنفس المفتاح + نفس البيانات): يُرجع نفس الاستجابة
3. **الطلب الثاني** (بنفس المفتاح + بيانات مختلفة): `409 Conflict`

**راجع**: [دليل Idempotency المفصل](../04-Implementation/03_Idempotency_Transactions.md)

---

## 4️⃣ أمثلة عملية | Practical Examples {#أمثلة-عملية}

### **سيناريو 1: إدارة المنتجات**

```http
# قراءة قائمة
GET /v1/products
⟶ 200 OK + قائمة المنتجات

# قراءة منتج محدد
GET /v1/products/123
⟶ 200 OK + تفاصيل المنتج

# إنشاء منتج جديد
POST /v1/products
⟶ 201 Created + Location: /v1/products/456

# تحديث كامل
PUT /v1/products/123
⟶ 200 OK + المنتج المحدث

# تحديث جزئي
PATCH /v1/products/123
⟶ 200 OK + المنتج المحدث

# حذف منتج
DELETE /v1/products/123
⟶ 204 No Content
```

---

### **سيناريو 2: رحلة الطلب**

```http
# 1. إنشاء طلب
POST /v1/orders
Idempotency-Key: order-key-123
⟶ 201 Created

# 2. قراءة حالة الطلب
GET /v1/orders/ORD-123
⟶ 200 OK { "status": "pending" }

# 3. تحديث عنوان الشحن
PATCH /v1/orders/ORD-123
{ "shipping_address_id": 789 }
⟶ 200 OK

# 4. إلغاء الطلب
POST /v1/orders/ORD-123/cancel
⟶ 200 OK { "status": "cancelled" }
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **استخدم الأسلوب الصحيح**
   - GET للقراءة
   - POST للإنشاء
   - PUT للاستبدال الكامل
   - PATCH للتحديث الجزئي
   - DELETE للحذف

2. **أرجع الحالة المناسبة**
   - 200 للنجاح العام
   - 201 للإنشاء
   - 204 للحذف
   - 4xx لأخطاء العميل
   - 5xx لأخطاء الخادم

3. **استخدم Idempotency-Key**
   - للعمليات المالية
   - POST للطلبات
   - أي عملية حساسة

4. **دعم ETag وIf-Match**
   - لمنع Lost Updates
   - للتخزين المؤقت الفعال

---

### ❌ **لا تفعل | Don't**

1. **لا تُعدّل البيانات مع GET**
   ```http
   ❌ GET /v1/products/123/activate
   ✅ POST /v1/products/123/activate
   ```

2. **لا تُخلط بين الحالات**
   ```http
   ❌ 200 OK مع رسالة خطأ في Body
   ✅ 400 Bad Request مع تفاصيل الخطأ
   ```

3. **لا تستخدم POST لكل شيء**
   ```http
   ❌ POST /v1/products/get
   ✅ GET /v1/products
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **عند تنفيذ endpoint جديد**
- [ ] هل استخدمت الأسلوب الصحيح؟
- [ ] هل الحالة المُرجعة مناسبة؟
- [ ] هل تدعم Idempotency (POST)؟
- [ ] هل تدعم ETag (GET)؟
- [ ] هل تدعم If-Match (PUT/PATCH)؟
- [ ] هل الأخطاء موحدة؟
- [ ] هل اختبرت جميع الحالات؟

---

## 🔗 **التنقل | Navigation**

[← السابق: الإصدار والمسارات | Previous: Versioning & URLs](02_Versioning_URLs.md)

[التالي: نظرة معمارية | Next: Architecture Overview →](../02-Architecture/01_Architecture_Overview.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [HTTP Methods - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [HTTP Status Codes - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RFC 7231 - HTTP/1.1](https://tools.ietf.org/html/rfc7231)
- [Idempotency Keys](https://stripe.com/docs/api/idempotent_requests)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved