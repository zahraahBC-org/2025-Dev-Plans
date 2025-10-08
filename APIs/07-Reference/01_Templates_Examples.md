# 01. قوالب وأمثلة | Templates & Examples

## 🎯 **نظرة عامة | Overview**

قوالب جاهزة وأمثلة عملية لتسريع تطوير واجهات الـ API.

**الهدف | Purpose**: توفير قوالب قابلة لإعادة الاستخدام  
**الجمهور | Audience**: جميع مطوري الـ API  
**الاستخدام | Usage**: نسخ ولصق وتعديل حسب الحاجة

---

## 📋 **جدول المحتويات | Table of Contents**

1. [قوالب الطلبات](#قوالب-الطلبات)
2. [قوالب الاستجابات](#قوالب-الاستجابات)
3. [قوالب الأخطاء](#قوالب-الأخطاء)
4. [أمثلة Controllers](#أمثلة-controllers)
5. [أمثلة OpenAPI](#أمثلة-openapi)

---

## 1️⃣ قوالب الطلبات | Request Templates {#قوالب-الطلبات}

### **GET - قراءة قائمة**
```http
GET /v1/products?page=1&limit=20&sort=-created_at&filter[category]=dresses
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json
Accept-Language: ar
```

### **GET - قراءة عنصر واحد**
```http
GET /v1/products/123?expand=brand,category
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
If-None-Match: "33a64df551425fcc55e"
```

### **POST - إنشاء**
```http
POST /v1/orders
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json
Idempotency-Key: c5a8bd76-b6d9-4c49-8e1a-1b2c3d4e5f6g

{
  "customer_id": 789,
  "items": [
    {
      "variant_id": 123,
      "quantity": 2
    }
  ],
  "shipping_address_id": 456,
  "payment_method": "cod",
  "note": "اتصال قبل التوصيل"
}
```

### **PATCH - تحديث جزئي**
```http
PATCH /v1/orders/ORD-123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/merge-patch+json
If-Match: "9f4b2c8e1d3a5f7b9c0e"

{
  "shipping_address_id": 789,
  "note": "تحديث: اتصال مساءً فقط"
}
```

### **DELETE - حذف**
```http
DELETE /v1/products/123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
If-Match: "1a2b3c4d5e6f7g8h9i0j"
```

---

## 2️⃣ قوالب الاستجابات | Response Templates {#قوالب-الاستجابات}

### **نجاح - مورد واحد**
```json
{
  "data": {
    "id": 123,
    "type": "product",
    "attributes": {
      "name_ar": "فستان صيفي",
      "price": 299.00,
      "currency": "SAR",
      "created_at": "2025-01-08T12:00:00Z"
    }
  }
}
```

### **نجاح - قائمة**
```json
{
  "data": [
    { "id": 123, "type": "product", "attributes": {...} },
    { "id": 124, "type": "product", "attributes": {...} }
  ],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total": 1250
  },
  "links": {
    "self": "/v1/products?page=1",
    "next": "/v1/products?page=2",
    "last": "/v1/products?page=63"
  }
}
```

### **نجاح - إنشاء**
```json
HTTP/1.1 201 Created
Location: /v1/orders/ORD-20250108-00123

{
  "id": "ORD-20250108-00123",
  "status": "pending",
  "total": 702.70,
  "created_at": "2025-01-08T12:00:00Z"
}
```

---

## 3️⃣ قوالب الأخطاء | Error Templates {#قوالب-الأخطاء}

### **400 Bad Request**
```json
{
  "error": {
    "code": "E1001",
    "message": "Invalid request format",
    "details": "JSON syntax error at position 45",
    "trace_id": "c9b1f3a0..."
  }
}
```

### **422 Validation Failed**
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
      }
    ],
    "trace_id": "c9b1f3a0..."
  }
}
```

---

## 4️⃣ أمثلة Controllers | Controller Examples {#أمثلة-controllers}

### **ProductController مع أفضل الممارسات**

```php
<?php

namespace App\Http\Controllers\API\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreProductRequest;
use App\Http\Resources\ProductResource;
use App\Services\ProductService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function __construct(
        private ProductService $productService
    ) {}
    
    /**
     * قائمة المنتجات
     * GET /v1/products
     */
    public function index(Request $request): JsonResponse
    {
        $products = $this->productService->list(
            page: $request->input('page', 1),
            limit: min($request->input('limit', 20), 100),
            filters: $request->input('filter', []),
            sort: $request->input('sort')
        );
        
        return response()->json([
            'data' => ProductResource::collection($products),
            'meta' => [
                'current_page' => $products->currentPage(),
                'per_page' => $products->perPage(),
                'total' => $products->total()
            ]
        ]);
    }
    
    /**
     * تفاصيل منتج
     * GET /v1/products/{id}
     */
    public function show(Request $request, int $id): JsonResponse
    {
        $product = $this->productService->find($id);
        
        if (!$product) {
            return response()->json([
                'error' => [
                    'code' => 'E3001',
                    'message' => 'Product not found',
                    'trace_id' => $request->header('X-Request-ID')
                ]
            ], 404);
        }
        
        return response()->json([
            'data' => new ProductResource($product)
        ])->setEtag(md5(json_encode($product)));
    }
    
    /**
     * إنشاء منتج
     * POST /v1/products
     */
    public function store(StoreProductRequest $request): JsonResponse
    {
        $product = $this->productService->create($request->validated());
        
        return response()->json([
            'data' => new ProductResource($product)
        ], 201)
        ->header('Location', route('products.show', $product->id));
    }
}
```

---

## 5️⃣ أمثلة OpenAPI | OpenAPI Examples {#أمثلة-openapi}

### **Endpoint كامل**

```yaml
/products:
  get:
    summary: قائمة المنتجات
    description: استرجاع قائمة مُقسمة ومُصفاة من المنتجات
    tags: [products]
    security:
      - bearerAuth: []
    parameters:
      - name: page
        in: query
        description: رقم الصفحة
        schema:
          type: integer
          minimum: 1
          default: 1
        example: 2
        
      - name: limit
        in: query
        description: عدد العناصر لكل صفحة
        schema:
          type: integer
          minimum: 1
          maximum: 100
          default: 20
        example: 20
        
      - name: sort
        in: query
        description: ترتيب النتائج
        schema:
          type: string
          enum: [price, -price, created_at, -created_at, rating, -rating]
        example: -created_at
        
      - name: filter[category]
        in: query
        description: تصفية بالفئة
        schema:
          type: string
        example: dresses
        
    responses:
      '200':
        description: قائمة المنتجات
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Product'
                meta:
                  $ref: '#/components/schemas/PaginationMeta'
            examples:
              success:
                value:
                  data:
                    - id: 123
                      name_ar: "فستان صيفي"
                      price: 299.00
                  meta:
                    current_page: 1
                    per_page: 20
                    total: 1250
                    
      '401':
        $ref: '#/components/responses/Unauthorized'
      '429':
        $ref: '#/components/responses/TooManyRequests'
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند استخدام القوالب**
- [ ] تعديل الأسماء والمعاملات
- [ ] إضافة التحقق المناسب
- [ ] تحديث OpenAPI
- [ ] إضافة الاختبارات
- [ ] مراجعة الأمان

---

## 🔗 **التنقل | Navigation**

[← السابق: المراقبة | Previous: Monitoring](../05-Operations/02_Monitoring_Observability.md)

[التالي: قوائم التحقق | Next: Checklists →](02_Checklists.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved