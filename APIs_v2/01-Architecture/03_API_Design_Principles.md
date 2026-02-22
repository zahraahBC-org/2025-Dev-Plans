# مبادئ تصميم API — API Design Principles

---

## **الهدف | Objective**

تحديد المبادئ الأساسية لتصميم RESTful APIs احترافية وسهلة الاستخدام.

---

## **المبادئ الأساسية | Core Principles**

### **1. Resource-Oriented Design**

**فكّر في الموارد (Resources) لا الأفعال (Actions)**

**DO:**
```
GET    /api/v1/products
POST   /api/v1/products
GET    /api/v1/products/{id}
PUT    /api/v1/products/{id}
DELETE /api/v1/products/{id}
```

**DON'T:**
```
GET    /api/v1/getProducts
POST   /api/v1/createProduct
GET    /api/v1/product/get/{id}
```

---

### **2. استخدام HTTP Methods بشكل صحيح**

| Method | الاستخدام | Idempotent | Safe |
|--------|-----------|-----------|------|
| **GET** | قراءة | ✅ | ✅ |
| **POST** | إنشاء | ❌ | ❌ |
| **PUT** | استبدال كامل | ✅ | ❌ |
| **PATCH** | تحديث جزئي | ❌ | ❌ |
| **DELETE** | حذف | ✅ | ❌ |

**التوضيح:**
- **Idempotent**: نفس الطلب مرتين → نفس النتيجة
- **Safe**: لا يغير البيانات

---

### **3. Status Codes المناسبة**

#### **النجاح (2xx):**

| Code | متى تستخدمه | المثال |
|------|-------------|---------|
| **200 OK** | قراءة/تحديث ناجح | GET, PUT, PATCH |
| **201 Created** | إنشاء ناجح | POST |
| **204 No Content** | حذف ناجح أو تحديث بدون رد | DELETE |

---

#### **أخطاء العميل (4xx):**

| Code | متى تستخدمه | المثال |
|------|-------------|---------|
| **400 Bad Request** | طلب خاطئ/غير مفهوم | JSON خاطئ |
| **401 Unauthorized** | غير مصادق | Token مفقود/منتهي |
| **403 Forbidden** | مصادق لكن بدون صلاحية | User عادي يحاول حذف |
| **404 Not Found** | المورد غير موجود | Product ID غير موجود |
| **422 Unprocessable** | Validation فشل | Email خاطئ، Price سالب |
| **429 Too Many Requests** | تجاوز Rate limit | أكثر من 60 req/min |

---

#### **أخطاء الخادم (5xx):**

| Code | متى تستخدمه | المثال |
|------|-------------|---------|
| **500 Internal Error** | خطأ غير متوقع | Exception غير مُعالج |
| **503 Service Unavailable** | الخدمة معطلة مؤقتاً | Maintenance mode |

---

## **تسمية الموارد | Resource Naming**

### **القواعد الأساسية:**

```
✅ استخدم أسماء جمع:
   /products (لا /product)
   /orders (لا /order)
   /users (لا /user)

✅ استخدم kebab-case للمسارات:
   /order-items
   /product-categories
   /user-addresses

✅ استخدم snake_case لحقول JSON:
   {
     "product_id": 123,
     "created_at": "2025-10-19T10:00:00Z",
     "is_active": true
   }

✅ المعرفات في المسار:
   /products/{id}
   /orders/{orderId}/items/{itemId}

✅ العلاقات واضحة:
   /products/{id}/reviews
   /orders/{id}/items
   /users/{id}/addresses
```

---

## **Response Structure | بنية الاستجابة**

### **Success Response Template**

```json
{
  "success": true,
  "message": "تم الحصول على البيانات بنجاح",
  "data": {
    "id": 123,
    "name": "Product Name",
    "price": 99.99
  },
  "timestamp": "2025-10-19T10:00:00Z"
}
```

---

### **Success with Pagination**

```json
{
  "success": true,
  "message": "تم الحصول على المنتجات بنجاح",
  "data": [
    {"id": 1, "name": "Product 1"},
    {"id": 2, "name": "Product 2"}
  ],
  "meta": {
    "current_page": 1,
    "last_page": 10,
    "per_page": 20,
    "total": 200,
    "from": 1,
    "to": 20
  },
  "links": {
    "first": "/api/v1/products?page=1",
    "last": "/api/v1/products?page=10",
    "prev": null,
    "next": "/api/v1/products?page=2"
  },
  "timestamp": "2025-10-19T10:00:00Z"
}
```

---

### **Error Response Template**

```json
{
  "success": false,
  "message": "فشل في التحقق من البيانات",
  "errors": {
    "email": [
      "حقل البريد الإلكتروني مطلوب",
      "البريد الإلكتروني غير صالح"
    ],
    "password": [
      "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
    ]
  },
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-10-19T10:00:00Z"
}
```

---

## **Filtering & Sorting | التصفية والفرز**

### **Query Parameters Standards**

```
GET /api/v1/products?category_id=5&min_price=100&max_price=500

✅ Filtering:
   ?category_id=5
   ?is_available=true
   ?status=active

✅ Search:
   ?search=dress
   ?q=product+name

✅ Sorting:
   ?sort=price          (ascending)
   ?sort=-price         (descending)
   ?sort=category,-created_at  (multiple)

✅ Pagination:
   ?page=2&per_page=20
   ?limit=50&offset=100

✅ Field selection (Sparse Fieldsets):
   ?fields=id,name,price

✅ Include relations:
   ?include=category,images,reviews
```

---

## **Pagination Strategies | استراتيجيات الترقيم**

### **1. Offset-based (بسيط)**

```
Request:
GET /api/v1/products?page=2&per_page=20

Response:
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "last_page": 10,
    "per_page": 20,
    "total": 200
  }
}
```

**المزايا:**
- بسيط وسهل
- مدعوم افتراضياً في Laravel

**العيوب:**
- ⚠️ مشاكل عند إضافة/حذف بيانات أثناء التصفح

---

### **2. Cursor-based (متقدم)**

```
Request:
GET /api/v1/products?cursor=eyJpZCI6MTAwfQ&limit=20

Response:
{
  "data": [...],
  "meta": {
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  }
}
```

**المزايا:**
- أداء أفضل على جداول كبيرة
- لا مشاكل مع البيانات المتغيرة

**العيوب:**
- ⚠️ لا يمكن القفز لصفحة معينة

---

## **Versioning | الإصدارات**

### **الاستراتيجية الموصى بها: Path Versioning**

```
✅ في المسار:
   /api/v1/products
   /api/v2/products

❌ في الـHeader:
   GET /api/products
   Accept: application/vnd.api+json; version=1

❌ في الـQuery:
   /api/products?version=1
```

**القواعد:**
- ابدأ بـ v1
- تغييرات كاسرة → إصدار جديد
- تشغيل متوازي خلال فترة انتقال
- Deprecation notice ≥ 90 يوماً

---

## **Headers Standards | معايير الرؤوس**

### **Request Headers**

```
✅ إلزامية:
   Content-Type: application/json
   Accept: application/json
   Authorization: Bearer {token}

✅ موصى بها:
   Accept-Language: ar
   X-Request-ID: unique-request-id

✅ اختيارية:
   If-None-Match: "etag-value"  (للـcaching)
   If-Match: "etag-value"       (للـconcurrency)
```

---

### **Response Headers**

```
✅ إلزامية:
   Content-Type: application/json; charset=utf-8

✅ موصى بها:
   X-RateLimit-Limit: 60
   X-RateLimit-Remaining: 45
   X-RateLimit-Reset: 1705662000
   X-Request-ID: unique-request-id

✅ للـCaching:
   Cache-Control: public, max-age=3600
   ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
   Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT

✅ للـSecurity:
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
```

---

## **Design Patterns | أنماط التصميم**

### **1. Repository Pattern**

```php
// Interface
interface ProductRepositoryInterface
{
    public function find(int $id): ?Product;
    public function create(array $data): Product;
    public function update(int $id, array $data): Product;
    public function delete(int $id): bool;
}

// Implementation
class ProductRepository implements ProductRepositoryInterface
{
    // Implementation here
}
```

---

### **2. Service Layer Pattern**

```php
// Service encapsulates business logic
class ProductService
{
    public function __construct(
        private ProductRepository $repository,
        private ImageService $imageService,
        private CacheService $cache
    ) {}
    
    public function createProduct(array $data): Product
    {
        // Complex business logic
    }
}
```

---

### **3. Resource Transformation Pattern**

```php
// Clean separation of data transformation
class ProductResource extends JsonResource
{
    public function toArray($request): array
    {
        // Transform logic here
    }
}
```

---

## **API Design Checklist**

### **التسمية:**
- [ ] أسماء جمع للموارد
- [ ] kebab-case للمسارات
- [ ] snake_case لحقول JSON
- [ ] أفعال عبر HTTP methods فقط

### **HTTP:**
- [ ] Methods صحيحة (GET, POST, PUT, PATCH, DELETE)
- [ ] Status codes مناسبة
- [ ] Headers قياسية

### **Response:**
- [ ] Structure موحد
- [ ] Error handling شامل
- [ ] Pagination واضح
- [ ] Timestamps بصيغة ISO-8601 UTC

### **Versioning:**
- [ ] في المسار (/v1/)
- [ ] Backward compatibility
- [ ] Deprecation policy

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
