# 01. التخزين المؤقت والأداء | Caching & Performance

## 🎯 **نظرة عامة | Overview**

استراتيجيات التخزين المؤقت وتحسين الأداء لضمان استجابة سريعة وتجربة مستخدم ممتازة.

**الهدف | Purpose**: تحسين زمن الاستجابة وتقليل الحمل  
**الجمهور | Audience**: مطورو Backend، مهندسو SRE  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [استراتيجيات الكاش](#استراتيجيات-الكاش)
2. [رؤوس HTTP](#رؤوس-http)
3. [Redis Caching](#redis-caching)
4. [تحسينات الأداء](#تحسينات-الأداء)
5. [SLOs](#slos)

---

## 1️⃣ استراتيجيات الكاش | Caching Strategies {#استراتيجيات-الكاش}

### **طبقات الكاش المتعددة**

```
1. Browser Cache (العميل)
   ↓ Cache-Control: public, max-age=300
   
2. CDN/Edge Cache (Cloudflare)
   ↓ 5-15 دقائق للموارد الثابتة
   
3. API Gateway Cache
   ↓ 1-5 دقائق للموارد العامة
   
4. Application Cache (Redis)
   ↓ Query results, Sessions
   
5. Database Query Cache
   ↓ MySQL query cache
```

---

### **سياسات الكاش حسب المورد**

| المورد | الطبقة | TTL | السياسة |
|--------|--------|-----|---------|
| **قائمة منتجات** | Edge + Redis | 5 دقائق | `public, max-age=300` |
| **تفاصيل منتج** | Edge + Redis | 10 دقائق | `public, max-age=600` |
| **الفئات** | Edge + Redis | 1 ساعة | `public, max-age=3600` |
| **ملف عميل** | Application | 5 دقائق | `private, max-age=300` |
| **طلبات عميل** | لا كاش | - | `no-store` |
| **سلة** | Application | 10 دقائق | `private, max-age=600` |

---

## 2️⃣ رؤوس HTTP | HTTP Headers {#رؤوس-http}

### **Cache-Control**

#### **للموارد العامة**
```http
Cache-Control: public, max-age=3600, s-maxage=7200

public      ← يمكن تخزينه في أي cache
max-age     ← صلاحية في browser (1 ساعة)
s-maxage    ← صلاحية في shared cache/CDN (2 ساعة)
```

#### **للموارد الخاصة**
```http
Cache-Control: private, max-age=300

private     ← browser فقط، ليس CDN
max-age     ← 5 دقائق
```

#### **بدون كاش**
```http
Cache-Control: no-store, no-cache, must-revalidate

no-store    ← لا تخزين أبدًا
no-cache    ← تحقق دائمًا من النسخة
must-revalidate ← تحقق عند انتهاء الصلاحية
```

---

### **ETag**

#### **الطلب الأول**
```http
GET /v1/products/123

⟶ الاستجابة

HTTP/1.1 200 OK
ETag: "33a64df551425fcc55e"
Content-Type: application/json

{
  "id": 123,
  "name_ar": "فستان"
}
```

#### **الطلب الثاني (مع If-None-Match)**
```http
GET /v1/products/123
If-None-Match: "33a64df551425fcc55e"

⟶ الاستجابة

HTTP/1.1 304 Not Modified
ETag: "33a64df551425fcc55e"

[no body - توفير في النقل]
```

---

### **Last-Modified**

```http
GET /v1/products/123

⟶ الاستجابة

HTTP/1.1 200 OK
Last-Modified: Wed, 08 Jan 2025 12:00:00 GMT

# الطلب التالي
GET /v1/products/123
If-Modified-Since: Wed, 08 Jan 2025 12:00:00 GMT

⟶ إذا لم يتغير
HTTP/1.1 304 Not Modified
```

---

## 3️⃣ Redis Caching {#redis-caching}

### **استراتيجيات Redis**

#### **1. Cache-Aside (Lazy Loading)**
```php
// قراءة
$products = Redis::get("products:list:page:1");

if (!$products) {
    // Cache miss - اجلب من DB
    $products = Product::paginate(20);
    
    // خزن في Redis
    Redis::setex(
        "products:list:page:1",
        300,  // TTL: 5 دقائق
        json_encode($products)
    );
}

return $products;
```

---

#### **2. Write-Through**
```php
// عند التحديث
$product->update($data);

// تحديث Cache فورًا
Redis::setex(
    "product:{$product->id}",
    600,
    json_encode($product)
);
```

---

#### **3. Cache Invalidation**
```php
// عند حذف أو تحديث
Redis::del("product:{$productId}");
Redis::del("products:list:*");  // حذف جميع قوائم المنتجات

// أو باستخدام Tags
Redis::tags(['products'])->flush();
```

---

### **مفاتيح Redis منظمة**
```
Schema: {resource}:{id}:{context}

أمثلة:
product:123                    ← منتج واحد
products:list:page:1           ← قائمة
products:list:category:5       ← مصفاة بالفئة
customer:789:profile           ← ملف عميل
customer:789:orders:recent     ← طلبات حديثة
session:uuid                   ← جلسة
```

---

## 4️⃣ تحسينات الأداء | Performance Optimizations {#تحسينات-الأداء}

### **1. N+1 Query Problem**

#### **❌ المشكلة**
```php
// Query لكل منتج في حلقة
$products = Product::all();  // 1 query

foreach ($products as $product) {
    echo $product->brand->name;  // N queries
}
// المجموع: 1 + N queries
```

#### **✅ الحل - Eager Loading**
```php
$products = Product::with('brand', 'category')->get();  // 3 queries فقط

foreach ($products as $product) {
    echo $product->brand->name;  // لا query إضافي
}
```

---

### **2. Database Indexing**

```sql
-- فهارس للبحث والفرز
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_created ON products(created_at DESC);

-- فهارس مركبة للاستعلامات الشائعة
CREATE INDEX idx_products_category_price 
ON products(category_id, price);

CREATE INDEX idx_orders_customer_created 
ON orders(customer_id, created_at DESC);
```

---

### **3. Query Optimization**

```php
// ❌ بطيء - جلب كل الحقول
$products = Product::all();

// ✅ أسرع - حقول محددة فقط
$products = Product::select('id', 'name_ar', 'price')->get();

// ✅ أسرع - مع pagination
$products = Product::select('id', 'name_ar', 'price')
    ->paginate(20);
```

---

### **4. Response Compression**

```nginx
# NGINX
gzip on;
gzip_vary on;
gzip_min_length 1000;
gzip_types
    application/json
    application/javascript
    text/css
    text/plain;

# أو Brotli (أفضل)
brotli on;
brotli_types application/json;
```

---

## 5️⃣ SLOs | Service Level Objectives {#slos}

### **أهداف الأداء**

| المؤشر | الهدف | القياس |
|--------|-------|--------|
| **P50 Latency** | ≤ 100ms | من Monitoring |
| **P95 Latency** | ≤ 300ms | من Monitoring |
| **P99 Latency** | ≤ 500ms | من Monitoring |
| **Cache Hit Ratio** | ≥ 80% | Redis Stats |
| **DB Query Time** | ≤ 50ms | Slow Query Log |
| **Error Rate** | ≤ 0.1% | من Logs |

---

### **مراقبة الأداء**

```promql
# Latency P95
histogram_quantile(0.95,
  rate(api_request_duration_seconds_bucket[5m])
)

# Cache Hit Ratio
rate(redis_keyspace_hits_total[5m])
/ (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m]))

# DB Query Time
mysql_global_status_slow_queries
```

---

## ✅ **قائمة التحقق | Checklist**

### **الكاش**
- [ ] Cache-Control محدد لكل endpoint
- [ ] ETag مفعل للـ GET
- [ ] Redis للقوائم الثقيلة
- [ ] TTL مناسب لكل نوع
- [ ] Cache invalidation عند التحديث

### **الأداء**
- [ ] Eager Loading للعلاقات
- [ ] فهارس DB مناسبة
- [ ] Query optimization
- [ ] Compression مفعل
- [ ] SLOs محققة

---

## 🔗 **التنقل | Navigation**

[← السابق: OpenAPI | Previous: OpenAPI Specification](../02-Architecture/03_OpenAPI_Specification.md)

[التالي: المراقبة | Next: Monitoring →](02_Monitoring_Observability.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved