# معالجة الردود — Response Handling
**الأهمية | Importance**: 🟢 أساسية

---

## **Response Structure Standard**

### **Success Response:**
```json
{
  "success": true,
  "message": "تم الحصول على البيانات بنجاح",
  "data": {...},
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z",
    "version": "1.0"
  }
}
```

### **Error Response:**
```json
{
  "success": false,
  "message": "فشل في التحقق من البيانات",
  "errors": {...},
  "error_code": "VALIDATION_ERROR",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

## **Response Types Examples**

### **1. Single Resource:**

```json
GET /api/v1/products/1

{
  "success": true,
  "message": "تم الحصول على المنتج بنجاح",
  "data": {
    "id": 1,
    "name": "Product Name",
    "price": 99.99,
    "category": {
      "id": 5,
      "name": "Electronics"
    },
    "created_at": "2025-10-19T10:00:00Z"
  },
  "meta": {
    "timestamp": "2025-10-19T10:05:00Z"
  }
}
```

---

### **2. Collection (No Pagination):**

```json
GET /api/v1/categories

{
  "success": true,
  "message": "تم الحصول على الفئات بنجاح",
  "data": [
    {
      "id": 1,
      "name": "Electronics"
    },
    {
      "id": 2,
      "name": "Fashion"
    }
  ],
  "meta": {
    "total": 2,
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **3. Paginated Collection:**

```json
GET /api/v1/products?page=2&per_page=20

{
  "success": true,
  "message": "تم الحصول على المنتجات بنجاح",
  "data": [
    {
      "id": 21,
      "name": "Product 21",
      "price": 49.99
    },
    // ... 19 more items
  ],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total": 150,
    "last_page": 8,
    "from": 21,
    "to": 40
  },
  "links": {
    "first": "https://api.example.com/v1/products?page=1",
    "last": "https://api.example.com/v1/products?page=8",
    "prev": "https://api.example.com/v1/products?page=1",
    "next": "https://api.example.com/v1/products?page=3"
  }
}
```

---

### **4. Created Resource (201):**

```json
POST /api/v1/products

{
  "success": true,
  "message": "تم إنشاء المنتج بنجاح",
  "data": {
    "id": 156,
    "name": "New Product",
    "price": 99.99,
    "created_at": "2025-10-19T10:00:00Z"
  },
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **5. Updated Resource (200):**

```json
PUT /api/v1/products/156

{
  "success": true,
  "message": "تم تحديث المنتج بنجاح",
  "data": {
    "id": 156,
    "name": "Updated Product Name",
    "price": 89.99,
    "updated_at": "2025-10-19T10:05:00Z"
  }
}
```

---

### **6. Deleted Resource (204):**

```
DELETE /api/v1/products/156

HTTP/1.1 204 No Content
```

**أو بـBody (200):**

```json
{
  "success": true,
  "message": "تم حذف المنتج بنجاح"
}
```

---

### **7. Validation Error (422):**

```json
POST /api/v1/products

{
  "success": false,
  "message": "فشل في التحقق من البيانات",
  "errors": {
    "name": [
      "حقل الاسم مطلوب"
    ],
    "price": [
      "يجب أن يكون السعر رقماً",
      "يجب أن يكون السعر أكبر من صفر"
    ],
    "category_id": [
      "الفئة المحددة غير موجودة"
    ]
  },
  "error_code": "VALIDATION_ERROR",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **8. Authentication Error (401):**

```json
GET /api/v1/orders

{
  "success": false,
  "message": "يجب تسجيل الدخول للوصول إلى هذا المورد",
  "error_code": "UNAUTHENTICATED",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **9. Authorization Error (403):**

```json
DELETE /api/v1/products/1

{
  "success": false,
  "message": "ليس لديك صلاحية لتنفيذ هذا الإجراء",
  "error_code": "UNAUTHORIZED",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **10. Not Found (404):**

```json
GET /api/v1/products/999999

{
  "success": false,
  "message": "المنتج غير موجود",
  "error_code": "RESOURCE_NOT_FOUND",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z"
  }
}
```

---

### **11. Server Error (500):**

```json
GET /api/v1/products

{
  "success": false,
  "message": "حدث خطأ في الخادم. يرجى المحاولة لاحقاً",
  "error_code": "INTERNAL_SERVER_ERROR",
  "meta": {
    "timestamp": "2025-10-19T10:00:00Z",
    "request_id": "abc-123-def-456"
  }
}
```

---

## **API Resources (Laravel)**

### **Single Resource Example:**

```php
class ProductResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
            'category' => new CategoryResource($this->whenLoaded('category')),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}

// Usage
return new ProductResource($product);
```

### **Collection Example:**

```php
public function index(Request $request)
{
    $products = Product::with('category')
        ->paginate($request->get('per_page', 20));
    
    return ProductResource::collection($products);
}
```

---

## **Response Helper Trait:**

```php
trait ApiResponse
{
    protected function successResponse($data, string $message = 'Success', int $code = 200)
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'meta' => ['timestamp' => now()->toIso8601String()],
        ], $code);
    }
    
    protected function errorResponse(string $message, string $errorCode, int $code = 400)
    {
        return response()->json([
            'success' => false,
            'message' => $message,
            'error_code' => $errorCode,
        ], $code);
    }
}

// Usage
return $this->successResponse(new ProductResource($product), 'تم الإنشاء', 201);
```

---

## **Exception Handler Examples**

```php
// app/Exceptions/Handler.php
class Handler extends ExceptionHandler
{
    public function register(): void
    {
        // Model Not Found (404)
        $this->renderable(function (ModelNotFoundException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'success' => false,
                    'message' => 'المورد غير موجود',
                    'error_code' => 'RESOURCE_NOT_FOUND',
                ], 404);
            }
        });
        
        // Validation Exception (422)
        $this->renderable(function (ValidationException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'success' => false,
                    'message' => 'فشل في التحقق',
                    'errors' => $e->errors(),
                    'error_code' => 'VALIDATION_ERROR',
                ], 422);
            }
        });
    }
}
```

---

## **HTTP Status Codes Reference**

| Code | الاستخدام | مثال |
|------|-----------|------|
| **200** | OK - نجاح | GET /products |
| **201** | Created - تم الإنشاء | POST /products |
| **202** | Accepted - تم القبول | POST /reports (async) |
| **204** | No Content - لا محتوى | DELETE /products/1 |
| **400** | Bad Request - طلب خاطئ | بيانات مشوهة |
| **401** | Unauthorized - غير مصادق | بدون token |
| **403** | Forbidden - ممنوع | بدون صلاحية |
| **404** | Not Found - غير موجود | مورد غير موجود |
| **422** | Unprocessable - validation | فشل validation |
| **429** | Too Many Requests - rate limit | تجاوز الحد |
| **500** | Server Error - خطأ خادم | Exception |
| **503** | Service Unavailable - غير متاح | Maintenance |

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
