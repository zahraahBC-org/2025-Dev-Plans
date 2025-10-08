# 02. بوابة الـ API | API Gateway

## 🎯 **نظرة عامة | Overview**

دليل شامل لبوابة الـ API كطبقة موحدة للدخول، الأمان، والتحكم في جميع واجهات الـ API.

**الهدف | Purpose**: فهم دور ووظائف API Gateway  
**الجمهور | Audience**: مهندسو البرمجيات، DevOps  
**المتطلبات | Prerequisites**: فهم [العمارة](01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [ما هي بوابة الـ API](#ما-هي-بوابة-api)
2. [المسؤوليات الرئيسية](#المسؤوليات-الرئيسية)
3. [التكوين والإعداد](#التكوين-والإعداد)
4. [السياسات](#السياسات)
5. [المراقبة](#المراقبة)

---

## 1️⃣ ما هي بوابة الـ API | What is API Gateway {#ما-هي-بوابة-api}

### **التعريف**
نقطة دخول موحدة أمام جميع خدمات الـ API، تطبق سياسات مشتركة وتحمي الخدمات الخلفية.

### **الموقع في العمارة**
```
العملاء (Clients)
    ↓
CDN/WAF (Cloudflare)
    ↓
Load Balancer (NGINX)
    ↓
🔷 API Gateway  ← نحن هنا
    ↓
خدمات الـ API (Microservices)
```

---

## 2️⃣ المسؤوليات الرئيسية | Core Responsibilities {#المسؤوليات-الرئيسية}

### **1. المصادقة والتخويل | Authentication & Authorization**

#### **تحقق JWT**
```http
GET /v1/products
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Gateway:
1. استخراج التوكن
2. التحقق من التوقيع (JWKS)
3. التحقق من انتهاء الصلاحية
4. استخراج المطالبات (Claims)
   {
     "sub": 789,
     "role": "customer",
     "exp": 1704715200
   }
5. ✅ تمرير للخدمة أو ❌ إرجاع 401
```

#### **التحقق من الصلاحيات**
```
المسار: DELETE /v1/products/123
الدور المطلوب: admin

User Role: customer  → ❌ 403 Forbidden
User Role: admin     → ✅ تمرير للخدمة
```

---

### **2. تحديد معدل الطلبات | Rate Limiting**

#### **سياسات الحدود**
```yaml
rate_limits:
  # للعملاء
  customer:
    requests: 100
    window: 60s  # دقيقة واحدة
    
  # للشركاء
  partner:
    requests: 600
    window: 60s
    
  # للمسؤولين
  admin:
    requests: unlimited
```

#### **آلية العمل**
```
1. استلام الطلب
2. تحديد المستخدم (من JWT)
3. التحقق من العداد الحالي في Redis
   Key: rate_limit:{user_id}:{window}
   
4. إذا تجاوز الحد:
   ❌ 429 Too Many Requests
   Headers:
     X-RateLimit-Limit: 100
     X-RateLimit-Remaining: 0
     X-RateLimit-Reset: 1704715260
     Retry-After: 45
     
5. إذا ضمن الحد:
   ✅ تمرير الطلب
   Headers:
     X-RateLimit-Limit: 100
     X-RateLimit-Remaining: 42
     X-RateLimit-Reset: 1704715260
```

---

### **3. CORS - مشاركة الموارد عبر الأصول**

#### **القائمة البيضاء**
```yaml
cors:
  allowed_origins:
    - https://zahraah.com
    - https://app.zahraah.com
    - https://m.zahraah.com
    - https://admin.zahraah.com
    
  allowed_methods:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE
    - OPTIONS
    
  allowed_headers:
    - Authorization
    - Content-Type
    - X-Request-ID
    - Idempotency-Key
    
  exposed_headers:
    - X-RateLimit-Limit
    - X-RateLimit-Remaining
    - X-RateLimit-Reset
    - Location
    
  max_age: 3600  # ساعة واحدة
  credentials: true
```

#### **معالجة Preflight**
```http
# طلب Preflight
OPTIONS /v1/orders
Origin: https://app.zahraah.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Authorization, Content-Type

# استجابة Gateway
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.zahraah.com
Access-Control-Allow-Methods: POST, GET, PUT, PATCH, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 3600
Access-Control-Allow-Credentials: true
```

---

### **4. التوجيه | Request Routing**

#### **قواعد التوجيه**
```yaml
routes:
  - path: /v1/products/*
    upstream: http://products-service:8001
    strip_path: false
    
  - path: /v1/orders/*
    upstream: http://orders-service:8002
    strip_path: false
    
  - path: /v1/payments/*
    upstream: http://payments-service:8003
    strip_path: false
    
  - path: /v1/customers/*
    upstream: http://customers-service:8004
    strip_path: false
```

#### **التوجيه بناءً على الإصدار**
```
/v1/products  → products-service-v1
/v2/products  → products-service-v2
```

---

### **5. التحويلات | Request/Response Transformation**

#### **حقن رؤوس الطلب**
```http
# طلب العميل
GET /v1/products

# بعد Gateway (للخدمة)
GET /v1/products
X-Request-ID: c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m
X-Forwarded-For: 185.46.212.35
X-User-ID: 789
X-User-Role: customer
traceparent: 00-4bf92f3577b34da6-00f067aa0ba902b7-01
```

#### **تنظيف رؤوس الاستجابة**
```http
# من الخدمة
HTTP/1.1 200 OK
X-Powered-By: Laravel/10.0
X-Internal-Info: sensitive-data

# بعد Gateway (للعميل)
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-Request-ID: c9b1f3a0...
# حذف الرؤوس الداخلية
```

---

### **6. التخزين المؤقت | Caching**

#### **سياسات الكاش**
```yaml
cache:
  # قوائم المنتجات (عامة)
  - path: /v1/products
    methods: [GET]
    ttl: 300  # 5 دقائق
    vary: [Accept-Language]
    
  # تفاصيل منتج
  - path: /v1/products/{id}
    methods: [GET]
    ttl: 600  # 10 دقائق
    
  # لا كاش للطلبات
  - path: /v1/orders/*
    methods: [GET, POST, PUT, PATCH]
    cache: false
```

#### **مثال عملي**
```http
# الطلب الأول
GET /v1/products?page=1
⟶
Gateway: Miss (لا يوجد في الكاش)
→ توجيه للخدمة
← استجابة 200 OK
→ تخزين في Redis (TTL: 300s)
→ إرجاع للعميل

# الطلب الثاني (خلال 5 دقائق)
GET /v1/products?page=1
⟶
Gateway: Hit (موجود في الكاش)
→ إرجاع من Redis مباشرة
← استجابة 200 OK (أسرع)
```

---

### **7. التتبع والمراقبة | Tracing & Monitoring**

#### **توليد معرف الطلب**
```
إذا لم يرسل العميل X-Request-ID:
  Gateway يولد UUID جديد
  
Gateway يضيف/يمرر:
  X-Request-ID: c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m
  traceparent: 00-{trace-id}-{span-id}-{flags}
```

#### **السجلات**
```json
{
  "timestamp": "2025-01-08T12:00:00Z",
  "level": "INFO",
  "component": "api-gateway",
  "request_id": "c9b1f3a0...",
  "method": "GET",
  "path": "/v1/products",
  "user_id": 789,
  "ip": "185.46.212.35",
  "user_agent": "Zahraah/1.0 (iOS 17.2)",
  "status": 200,
  "duration_ms": 45,
  "upstream": "products-service",
  "cache_status": "HIT"
}
```

---

## 3️⃣ التكوين والإعداد | Configuration & Setup {#التكوين-والإعداد}

### **مثال: Kong Gateway**

#### **إضافة خدمة**
```bash
curl -X POST http://kong:8001/services \
  --data name=products-service \
  --data url=http://products-service:8001
```

#### **إضافة مسار**
```bash
curl -X POST http://kong:8001/services/products-service/routes \
  --data 'paths[]=/v1/products' \
  --data 'methods[]=GET' \
  --data 'methods[]=POST'
```

#### **تفعيل المصادقة JWT**
```bash
curl -X POST http://kong:8001/services/products-service/plugins \
  --data name=jwt \
  --data config.secret_is_base64=false \
  --data config.key_claim_name=kid
```

#### **تفعيل Rate Limiting**
```bash
curl -X POST http://kong:8001/services/products-service/plugins \
  --data name=rate-limiting \
  --data config.minute=100 \
  --data config.policy=redis
```

---

## 4️⃣ السياسات | Policies {#السياسات}

### **الأولوية في تنفيذ السياسات**
```
1. WAF (على الحافة - Cloudflare)
2. Rate Limiting
3. CORS (Preflight)
4. Authentication (JWT)
5. Authorization (Roles)
6. Request Transformation
7. Routing
8. Caching
9. Response Transformation
10. Logging & Metrics
```

---

## 5️⃣ المراقبة | Monitoring {#المراقبة}

### **المقاييس الأساسية**
```
- gateway.requests.total (counter)
- gateway.requests.duration (histogram)
- gateway.requests.errors (counter)
- gateway.cache.hits (counter)
- gateway.cache.misses (counter)
- gateway.rate_limit.exceeded (counter)
- gateway.auth.failures (counter)
```

### **لوحات المراقبة**
```
Dashboard: API Gateway
- Requests per Second (RPS)
- Latency P50/P95/P99
- Error Rate (4xx, 5xx)
- Cache Hit Ratio
- Rate Limit Events
- Authentication Failures
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند إعداد Gateway**
- [ ] تكوين JWKS Endpoint
- [ ] ضبط قواعد Rate Limiting
- [ ] إعداد قائمة CORS البيضاء
- [ ] تكوين المسارات (Routes)
- [ ] تفعيل السجلات المنظمة
- [ ] إعداد لوحات المراقبة
- [ ] اختبار جميع السياسات

---

## 🔗 **التنقل | Navigation**

[← السابق: نظرة معمارية | Previous: Architecture Overview](01_Architecture_Overview.md)

[التالي: مواصفة OpenAPI | Next: OpenAPI Specification →](03_OpenAPI_Specification.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [Kong Gateway Documentation](https://docs.konghq.com/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Rate Limiting Algorithms](https://en.wikipedia.org/wiki/Rate_limiting)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved