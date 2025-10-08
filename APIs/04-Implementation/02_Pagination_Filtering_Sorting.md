# 02. الترقيم والتصفية والفرز | Pagination, Filtering & Sorting

## 🎯 **نظرة عامة | Overview**

معايير موحدة للترقيم، التصفية، والفرز لضمان أداء عالي وتجربة مستخدم ممتازة.

**الهدف | Purpose**: تطبيق ترقيم وتصفية فعالة  
**الجمهور | Audience**: مطورو Backend والـ Frontend  
**المتطلبات | Prerequisites**: فهم [نماذج الاستجابة](01_Response_Error_Handling.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [الترقيم - Pagination](#الترقيم)
2. [التصفية - Filtering](#التصفية)
3. [الفرز - Sorting](#الفرز)
4. [اختيار الحقول](#اختيار-الحقول)
5. [توسيع العلاقات](#توسيع-العلاقات)

---

## 1️⃣ الترقيم | Pagination {#الترقيم}

### **النمط 1: Cursor-Based (موصى به)**

#### **لماذا Cursor-Based؟**
- ✅ أداء ثابت حتى مع صفحات عميقة
- ✅ لا تخطي أو تكرار عند إضافة/حذف بيانات
- ✅ مناسب للبيانات المتغيرة بسرعة

#### **الاستخدام**
```http
GET /v1/products?limit=20&cursor=eyJjcmVhdGVkX2F0IjoiMjAyNS0wMS0wOCIsImlkIjoxMjN9
```

#### **الاستجابة**
```json
{
  "data": [
    { "id": 124, "name_ar": "منتج 1", "created_at": "2025-01-08T11:00:00Z" },
    { "id": 125, "name_ar": "منتج 2", "created_at": "2025-01-08T10:00:00Z" }
  ],
  "page_info": {
    "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNS0wMS0wOCIsImlkIjoxNDN9",
    "has_more": true,
    "limit": 20
  }
}
```

#### **بناء Cursor**
```php
// Encode
$cursor = base64_encode(json_encode([
    'created_at' => $lastItem->created_at,
    'id' => $lastItem->id  // tie-breaker
]));

// Decode
$decoded = json_decode(base64_decode($cursor), true);

// Query
$products = Product::where('created_at', '<', $decoded['created_at'])
    ->orWhere(function($q) use ($decoded) {
        $q->where('created_at', '=', $decoded['created_at'])
          ->where('id', '<', $decoded['id']);
    })
    ->orderBy('created_at', 'desc')
    ->orderBy('id', 'desc')
    ->limit($limit)
    ->get();
```

---

### **النمط 2: Offset/Limit (بسيط)**

#### **الاستخدام**
```http
GET /v1/products?page=2&limit=20
```

#### **الاستجابة**
```json
{
  "data": [ ... ],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total": 1250,
    "total_pages": 63,
    "from": 21,
    "to": 40
  },
  "links": {
    "first": "/v1/products?page=1&limit=20",
    "prev": "/v1/products?page=1&limit=20",
    "self": "/v1/products?page=2&limit=20",
    "next": "/v1/products?page=3&limit=20",
    "last": "/v1/products?page=63&limit=20"
  }
}
```

**القيود**:
- ⚠️ بطء مع offset كبير (OFFSET 10000 بطيء)
- ⚠️ مشاكل عند إضافة/حذف بيانات أثناء التصفح

**متى تستخدمه**:
- قوائم إدارية صغيرة
- تقارير ثابتة
- عدد صفحات معروف ومطلوب

---

### **المعاملات القياسية**

| المعامل | النوع | الافتراضي | الحد الأقصى | الوصف |
|---------|------|----------|-------------|-------|
| `limit` | integer | 20 | 100 | عدد العناصر |
| `cursor` | string | null | - | مؤشر الصفحة |
| `page` | integer | 1 | - | رقم الصفحة (offset) |

---

## 2️⃣ التصفية | Filtering {#التصفية}

### **بناء الجملة**
```
?filter[field]=value
?filter[field.operator]=value
```

### **أمثلة**

#### **تصفية بسيطة**
```http
GET /v1/products?filter[category]=dresses
GET /v1/products?filter[is_active]=true
GET /v1/products?filter[brand_id]=45
```

#### **تصفية بمعاملات**
```http
GET /v1/products?filter[price.gte]=100&filter[price.lte]=500
GET /v1/orders?filter[created_at.gte]=2025-01-01
GET /v1/customers?filter[registration_date.between]=2025-01-01,2025-01-31
```

#### **تصفية متعددة**
```http
GET /v1/products?filter[category]=dresses&filter[brand_id]=45&filter[is_active]=true
```

---

### **المعاملات المدعومة**

| المعامل | الوصف | مثال |
|---------|-------|------|
| `eq` | يساوي (افتراضي) | `filter[status]=active` |
| `ne` | لا يساوي | `filter[status.ne]=cancelled` |
| `gt` | أكبر من | `filter[price.gt]=100` |
| `gte` | أكبر من أو يساوي | `filter[price.gte]=100` |
| `lt` | أصغر من | `filter[price.lt]=500` |
| `lte` | أصغر من أو يساوي | `filter[price.lte]=500` |
| `in` | في القائمة | `filter[status.in]=pending,confirmed` |
| `between` | بين قيمتين | `filter[date.between]=2025-01-01,2025-01-31` |
| `like` | يحتوي على | `filter[name.like]=فستان` |

---

## 3️⃣ الفرز | Sorting {#الفرز}

### **بناء الجملة**
```
?sort=field        ← تصاعدي (ascending)
?sort=-field       ← تنازلي (descending)
?sort=field1,-field2  ← متعدد
```

### **أمثلة**

```http
# فرز بالسعر (تصاعدي)
GET /v1/products?sort=price

# فرز بالسعر (تنازلي)
GET /v1/products?sort=-price

# فرز بالتاريخ ثم بالسعر
GET /v1/products?sort=-created_at,price

# فرز بالتقييم
GET /v1/products?sort=-rating,-review_count
```

---

### **الحقول المسموحة للفرز**

#### **Products**
```
✅ price
✅ created_at
✅ rating
✅ review_count
✅ name_ar
✅ name_en
❌ description (نص طويل - غير فعال)
```

#### **Orders**
```
✅ created_at
✅ total
✅ status
❌ items (علاقة - غير مدعوم)
```

**القاعدة الذهبية**: فقط الحقول المفهرسة أو البسيطة

---

## 4️⃣ اختيار الحقول | Field Selection {#اختيار-الحقول}

### **Sparse Fieldsets**

```http
# كل الحقول (افتراضي)
GET /v1/products/123
⟶
{
  "id": 123,
  "name_ar": "...",
  "name_en": "...",
  "description_ar": "نص طويل جدًا...",
  "description_en": "long text...",
  "price": 299.00,
  "images": [...],
  "specifications": {...}
}

# حقول محددة فقط
GET /v1/products/123?fields=id,name_ar,price
⟶
{
  "id": 123,
  "name_ar": "...",
  "price": 299.00
}
```

**الفوائد**:
- ✅ تقليل حجم الاستجابة
- ✅ استجابة أسرع
- ✅ استهلاك أقل للبيانات (Mobile)

---

## 5️⃣ توسيع العلاقات | Expand Relationships {#توسيع-العلاقات}

### **بدون Expand**
```http
GET /v1/products/123
⟶
{
  "id": 123,
  "name_ar": "فستان",
  "brand_id": 45,       ← فقط ID
  "category_id": 12     ← فقط ID
}
```

### **مع Expand**
```http
GET /v1/products/123?expand=brand,category
⟶
{
  "id": 123,
  "name_ar": "فستان",
  "brand": {           ← كائن كامل
    "id": 45,
    "name": "فاشن بلس"
  },
  "category": {        ← كائن كامل
    "id": 12,
    "name_ar": "فساتين"
  }
}
```

**القيود**:
- حد أقصى للـ expand: 3 علاقات
- تجنب N+1 queries (استخدم Eager Loading)

---

## 🎯 **مثال شامل | Complete Example**

```http
GET /v1/products?
    page=2&
    limit=20&
    sort=-created_at,price&
    filter[category]=dresses&
    filter[price.gte]=100&
    filter[price.lte]=500&
    filter[is_active]=true&
    fields=id,name_ar,price,images&
    expand=brand
```

**الاستجابة**:
```json
{
  "data": [
    {
      "id": 124,
      "name_ar": "فستان أنيق",
      "price": 349.00,
      "images": ["url1", "url2"],
      "brand": {
        "id": 45,
        "name": "فاشن بلس"
      }
    }
  ],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total": 85
  }
}
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند تنفيذ Pagination/Filtering/Sorting**
- [ ] اختيار نمط الترقيم (Cursor أو Offset)
- [ ] حد أقصى للـlimit (100)
- [ ] قائمة بيضاء لحقول الفرز
- [ ] قائمة بيضاء لحقول التصفية
- [ ] دعم معاملات التصفية المتقدمة
- [ ] فهارس DB للحقول المفروزة/المصفاة
- [ ] توثيق في OpenAPI
- [ ] اختبارات للحالات الحدية

---

## 🔗 **التنقل | Navigation**

[← السابق: معالجة الأخطاء | Previous: Error Handling](01_Response_Error_Handling.md)

[التالي: عدم التكرار | Next: Idempotency →](03_Idempotency_Transactions.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [Cursor Pagination Guide](https://jsonapi.org/profiles/ethanresnick/cursor-pagination/)
- [GraphQL Cursor Connections](https://relay.dev/graphql/connections.htm)
- [JSON:API Filtering](https://jsonapi.org/format/#fetching-filtering)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved