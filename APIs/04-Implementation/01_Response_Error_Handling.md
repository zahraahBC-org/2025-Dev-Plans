# 01. نماذج الاستجابة والأخطاء | Response & Error Handling

## 🎯 **نظرة عامة | Overview**

معايير موحدة لتصميم الاستجابات والأخطاء لضمان تجربة متسقة عبر جميع واجهات الـ API.

**الهدف | Purpose**: توحيد شكل الاستجابات والأخطاء  
**الجمهور | Audience**: مطورو Backend والـ Frontend  
**المتطلبات | Prerequisites**: فهم [أساليب HTTP](../01-Core-Principles/03_HTTP_Methods_Status.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [نماذج الاستجابة الناجحة](#نماذج-الاستجابة-الناجحة)
2. [نماذج الأخطاء](#نماذج-الأخطاء)
3. [كتالوج الأخطاء](#كتالوج-الأخطاء)
4. [معالجة الأخطاء](#معالجة-الأخطاء)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ نماذج الاستجابة الناجحة | Success Response Patterns {#نماذج-الاستجابة-الناجحة}

### **مورد واحد | Single Resource**

```http
GET /v1/products/123
⟶
HTTP/1.1 200 OK
Content-Type: application/json
ETag: "33a64df551425fcc55e"
Cache-Control: public, max-age=3600

{
  "data": {
    "id": 123,
    "type": "product",
    "attributes": {
      "name_ar": "فستان صيفي بالورود",
      "name_en": "Floral Summer Dress",
      "price": 299.00,
      "currency": "SAR",
      "is_active": true,
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-08T12:00:00Z"
    },
    "relationships": {
      "brand": {
        "data": { "type": "brands", "id": 45 }
      },
      "category": {
        "data": { "type": "categories", "id": 12 }
      }
    }
  },
  "included": [
    {
      "id": 45,
      "type": "brands",
      "attributes": {
        "name": "فاشن بلس"
      }
    },
    {
      "id": 12,
      "type": "categories",
      "attributes": {
        "name_ar": "فساتين",
        "name_en": "Dresses"
      }
    }
  ]
}
```

---

### **قائمة موارد | Resource Collection**

```http
GET /v1/products?page=1&limit=20&sort=-created_at
⟶
HTTP/1.1 200 OK
Content-Type: application/json
Link: </v1/products?page=2&limit=20>; rel="next"

{
  "data": [
    {
      "id": 123,
      "type": "product",
      "attributes": { ... }
    },
    {
      "id": 124,
      "type": "product",
      "attributes": { ... }
    }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total": 1250,
    "total_pages": 63
  },
  "links": {
    "self": "/v1/products?page=1&limit=20",
    "next": "/v1/products?page=2&limit=20",
    "last": "/v1/products?page=63&limit=20"
  }
}
```

---

### **إنشاء مورد | Resource Creation**

```http
POST /v1/orders
Idempotency-Key: c5a8bd76-b6d9-4c49-8e1a-1b2c3d4e5f6g
⟶
HTTP/1.1 201 Created
Location: /v1/orders/ORD-20250108-00123
Content-Type: application/json

{
  "data": {
    "id": "ORD-20250108-00123",
    "type": "order",
    "attributes": {
      "status": "pending",
      "subtotal": 598.00,
      "tax_amount": 89.70,
      "shipping_fee": 15.00,
      "total": 702.70,
      "currency": "SAR",
      "created_at": "2025-01-08T12:00:00Z"
    }
  }
}
```

---

### **حذف مورد | Resource Deletion**

```http
DELETE /v1/products/123
⟶
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

---

## 2️⃣ نماذج الأخطاء | Error Patterns {#نماذج-الأخطاء}

### **النموذج الموحد للأخطاء**

```json
{
  "error": {
    "code": "E1001",
    "message": "رسالة واضحة قابلة للقراءة",
    "details": [
      {
        "field": "اسم الحقل",
        "issue": "نوع المشكلة",
        "message": "رسالة تفصيلية"
      }
    ],
    "trace_id": "c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m",
    "timestamp": "2025-01-08T12:00:00Z",
    "path": "/v1/orders",
    "method": "POST"
  }
}
```

---

### **أمثلة الأخطاء الشائعة**

#### **400 Bad Request - طلب خاطئ**
```json
{
  "error": {
    "code": "E1001",
    "message": "Invalid JSON format",
    "details": [
      {
        "field": "body",
        "issue": "syntax_error",
        "message": "Unexpected token at position 45"
      }
    ],
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **401 Unauthorized - غير مصادق**
```json
{
  "error": {
    "code": "E2001",
    "message": "Authentication required",
    "details": "Missing or invalid access token",
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **403 Forbidden - غير مصرح**
```json
{
  "error": {
    "code": "E2002",
    "message": "Insufficient permissions",
    "details": "Admin role required for this operation",
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **404 Not Found - غير موجود**
```json
{
  "error": {
    "code": "E3001",
    "message": "Resource not found",
    "details": "No product with ID 99999",
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **422 Unprocessable Entity - فشل التحقق**
```json
{
  "error": {
    "code": "E5001",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "rule": "email",
        "message": "يجب أن يكون بريد إلكتروني صالح"
      },
      {
        "field": "phone",
        "rule": "required",
        "message": "رقم الهاتف مطلوب"
      },
      {
        "field": "items",
        "rule": "min:1",
        "message": "يجب إضافة عنصر واحد على الأقل"
      }
    ],
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **429 Too Many Requests - تجاوز الحد**
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704715200
Retry-After: 60

{
  "error": {
    "code": "E6001",
    "message": "Rate limit exceeded",
    "details": "Maximum 100 requests per minute. Please try again in 60 seconds.",
    "trace_id": "c9b1f3a0..."
  }
}
```

---

#### **500 Internal Server Error - خطأ داخلي**
```json
{
  "error": {
    "code": "E7001",
    "message": "Internal server error",
    "details": "An unexpected error occurred. Our team has been notified.",
    "trace_id": "c9b1f3a0..."
  }
}
```

**ملاحظة مهمة**: 
- ❌ لا تكشف تفاصيل تقنية داخلية
- ❌ لا تكشف Stack Trace
- ✅ استخدم trace_id للتتبع الداخلي

---

## 3️⃣ كتالوج الأخطاء | Error Catalog {#كتالوج-الأخطاء}

### **هيكل الأكواد**
```
E + نطاق رقمي (4 أرقام)

E1xxx - أخطاء الطلب (Request)
E2xxx - أخطاء المصادقة/التخويل (Auth)
E3xxx - أخطاء الموارد (Resources)
E4xxx - أخطاء منطق الأعمال (Business)
E5xxx - أخطاء التحقق (Validation)
E6xxx - أخطاء التحديد (Rate Limiting)
E7xxx - أخطاء الخادم (Server)
```

### **أمثلة**

| الكود | الوصف | HTTP Status |
|------|--------|-------------|
| **E1001** | Invalid JSON format | 400 |
| **E1002** | Invalid request parameters | 400 |
| **E2001** | Authentication required | 401 |
| **E2002** | Insufficient permissions | 403 |
| **E2003** | Token expired | 401 |
| **E3001** | Resource not found | 404 |
| **E3002** | Resource already exists | 409 |
| **E4001** | Insufficient stock | 422 |
| **E4002** | Invalid order state transition | 422 |
| **E5001** | Validation failed | 422 |
| **E6001** | Rate limit exceeded | 429 |
| **E7001** | Internal server error | 500 |
| **E7002** | Database connection failed | 503 |

---

## 4️⃣ معالجة الأخطاء | Error Handling {#معالجة-الأخطاء}

### **معالج الأخطاء المركزي**

```php
// Laravel Exception Handler
public function render($request, Throwable $exception)
{
    // 1. تسجيل الخطأ
    Log::error('API Error', [
        'trace_id' => $request->header('X-Request-ID'),
        'exception' => get_class($exception),
        'message' => $exception->getMessage(),
        'file' => $exception->getFile(),
        'line' => $exception->getLine()
    ]);
    
    // 2. تحديد نوع الخطأ
    $error = $this->mapException($exception);
    
    // 3. إرجاع استجابة موحدة
    return response()->json([
        'error' => [
            'code' => $error['code'],
            'message' => $error['message'],
            'details' => $error['details'] ?? null,
            'trace_id' => $request->header('X-Request-ID'),
            'timestamp' => now()->toIso8601String(),
            'path' => $request->path(),
            'method' => $request->method()
        ]
    ], $error['status']);
}
```

---

### **التعامل مع أخطاء التحقق**

```php
// Validation في Controller
$validated = $request->validate([
    'email' => 'required|email',
    'phone' => 'required|regex:/^\+9665[0-9]{8}$/',
    'items' => 'required|array|min:1',
    'items.*.variant_id' => 'required|exists:variants,id',
    'items.*.quantity' => 'required|integer|min:1'
]);

// إذا فشل، إرجاع 422 تلقائياً:
{
  "error": {
    "code": "E5001",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "rule": "email",
        "message": "يجب أن يكون بريد إلكتروني صالح"
      }
    ]
  }
}
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **استخدم نموذج موحد دائمًا**
   ```json
   ✅ { "error": { "code": "...", "message": "..." } }
   ❌ { "status": "error", "msg": "..." }
   ```

2. **أكواد خطأ واضحة**
   ```
   ✅ E3001 - Resource not found
   ❌ ERR_NOT_FOUND
   ```

3. **رسائل قابلة للقراءة**
   ```
   ✅ "رقم الهاتف يجب أن يبدأ بـ +966"
   ❌ "Invalid phone format"
   ```

4. **تضمين trace_id دائمًا**
   ```
   يساعد في تتبع المشكلة في السجلات
   ```

5. **لا تكشف تفاصيل داخلية**
   ```
   ❌ "MySQL Error: Duplicate entry..."
   ✅ "Resource already exists"
   ```

---

### ❌ **لا تفعل | Don't**

1. **لا تُرجع HTML للأخطاء**
   ```html
   ❌ <html><body>Error 500</body></html>
   ✅ {"error": {...}}
   ```

2. **لا تكشف Stack Traces**
   ```
   ❌ في Production
   ✅ فقط في Dev/Staging
   ```

3. **لا تستخدم 200 مع أخطاء**
   ```json
   ❌ HTTP 200 { "success": false, "error": "..." }
   ✅ HTTP 400 { "error": {...} }
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **عند تنفيذ معالجة الأخطاء**
- [ ] نموذج خطأ موحد مطبق
- [ ] كتالوج أكواد الأخطاء موثق
- [ ] معالج أخطاء مركزي
- [ ] تسجيل جميع الأخطاء
- [ ] trace_id في كل خطأ
- [ ] عدم كشف تفاصيل داخلية
- [ ] رسائل قابلة للقراءة
- [ ] HTTP Status مناسب

---

## 🔗 **التنقل | Navigation**

[← السابق: المصادقة | Previous: Authentication](../03-Security/01_Authentication_Authorization.md)

[التالي: الترقيم والتصفية | Next: Pagination & Filtering →](02_Pagination_Filtering_Sorting.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [RFC 7807 - Problem Details](https://tools.ietf.org/html/rfc7807)
- [JSON:API Specification](https://jsonapi.org/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved