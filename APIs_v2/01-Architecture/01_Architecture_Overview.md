# نظرة معمارية شاملة — Architecture Overview

---

## **الهدف | Objective**

تحديد البنية المعمارية المثالية لـRESTful APIs للاستهلاك الداخلي بناءً على أفضل الممارسات العالمية.

---

## **البنية المعمارية المقترحة | Recommended Architecture**

### **النموذج المرجعي | Reference Model**

```
┌──────────────────────────────────────────┐
│         Clients (Mobile/Web/Admin)        │
│    (Flutter, React, Vue, Admin Panel)    │
└───────────────┬──────────────────────────┘
                │ HTTPS
                │ Bearer Token
                ▼
┌──────────────────────────────────────────┐
│           API Gateway / Edge              │
│  ┌────────────────────────────────────┐  │
│  │  • HTTPS/TLS Termination           │  │
│  │  • Rate Limiting                   │  │
│  │  │  │  • Security Headers                 │  │
│  └────────────────────────────────────┘  │
└───────────────┬──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────┐
│         Application Server                │
│  ┌────────────────────────────────────┐  │
│  │    HTTP Layer (Controllers)        │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Request Validation          │  │  │
│  │  │  Authentication Check        │  │  │
│  │  │  Authorization Check         │  │  │
│  │  └──────────────────────────────┘  │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │    Business Logic (Services)       │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Domain Rules                │  │  │
│  │  │  Data Processing             │  │  │
│  │  │  Event Dispatching           │  │  │
│  │  └──────────────────────────────┘  │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │   Data Access (Repositories)       │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Query Building              │  │  │
│  │  │  Data Mapping                │  │  │
│  │  │  Transaction Management      │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└───────────────┬──────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
    ▼                       ▼
┌─────────┐           ┌──────────┐
│Database │           │  Cache   │
│(MySQL)  │           │ (Redis)  │
└─────────┘           └──────────┘
```

---

## **الطبقات الأساسية | Core Layers**

### **1. Client Layer | طبقة العميل**

**المسؤوليات:**
- إرسال الطلبات HTTP
- إدارة Authentication tokens
- معالجة الردود
- Error handling

**التقنيات:**
- Mobile Apps (Flutter, React Native, Swift, Kotlin)
- Web Apps (React, Vue, Angular)
- Admin Panels (Vue.js, React)

---

### **2. Edge/Gateway Layer | طبقة الحافة**

**المسؤوليات:**
- إنهاء TLS/HTTPS
- Rate Limiting
- CORS handling
- Security headers injection
- Request logging
- Load balancing

**التقنيات:**
- NGINX
- Apache (with modules)
- Cloudflare (CDN/WAF)
- Kong Gateway
- AWS API Gateway

**التهيئة النموذجية (NGINX):**
```nginx
# API Gateway configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Security & CORS headers
    add_header X-Frame-Options "DENY" always;
    add_header Access-Control-Allow-Origin "https://app.example.com" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=60r/m;
    
    location / {
        proxy_pass http://app_server;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### **3. Application Layer | طبقة التطبيق**

#### **3.1 HTTP Layer (Controllers)**

**المسؤوليات:**
- استقبال الطلبات HTTP
- Validation أولية
- استدعاء Services
- تحويل الردود (Resources)

**مثال (Laravel):**
```php
// Controller layer - HTTP handling only
class ProductController extends Controller
{
    public function __construct(private ProductService $service) {}
    
    public function index()
    {
        $products = $this->service->getAllProducts(request()->all());
        return ProductResource::collection($products);
    }
    
    public function store(StoreProductRequest $request)
    {
        $product = $this->service->createProduct($request->validated());
        return new ProductResource($product);
    }
}
```

---

#### **3.2 Business Logic Layer (Services)**

**المسؤوليات:**
- تنفيذ قواعد العمل
- معالجة البيانات
- إطلاق Events
- إدارة Transactions

**مثال:**
```php
// Service layer - Business logic
class ProductService
{
    public function __construct(private ProductRepository $repository) {}
    
    public function createProduct(array $data): Product
    {
        return DB::transaction(function () use ($data) {
            $product = $this->repository->create($data);
            Event::dispatch(new ProductCreated($product));
            Cache::tags(['products'])->flush();
            return $product;
        });
    }
}
```

---

#### **3.3 Data Access Layer (Repositories)**

**المسؤوليات:**
- بناء الاستعلامات
- الوصول للبيانات
- Data mapping

**مثال:**
```php
// Repository layer - Data access
class ProductRepository
{
    public function create(array $data): Product
    {
        return Product::create($data);
    }
    
    public function getFiltered(array $filters = [])
    {
        return Product::query()
            ->when($filters['category_id'] ?? null, fn($q, $v) => $q->where('category_id', $v))
            ->when($filters['search'] ?? null, fn($q, $v) => $q->where('name', 'like', "%{$v}%"))
            ->with(['category', 'images'])
            ->paginate(20);
    }
}
```

---

### **4. Data Layer | طبقة البيانات**

#### **4.1 Primary Database**

**الخصائص:**
- مخزن البيانات الأساسي
- Relational (MySQL, PostgreSQL)
- ACID transactions
- Normalized schema

**أفضل الممارسات:**
```sql
-- Indexes للأداء
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_created ON products(created_at);

-- Composite index لـqueries شائعة
CREATE INDEX idx_products_cat_active 
ON products(category_id, is_active, created_at);
```

---

#### **4.2 Cache Layer**

**الاستخدامات:**
- تخزين مؤقت للبيانات المتكررة
- Session storage
- Rate limiting counters
- Queue backend

**التقنيات:**
- Redis (موصى به)
- Memcached
- DynamoDB

**مثال:**
```php
// Cache strategy
Cache::tags(['products', 'category:' . $categoryId])
    ->remember($cacheKey, 3600, function () {
        return Product::with('category')->get();
    });

// Invalidation
Cache::tags(['products'])->flush();
```

---

## **تدفق الطلب النموذجي | Request Flow**

### **مثال: GET /api/v1/products**

```
1. Client → HTTPS Request
   ↓
2. Gateway/NGINX
   ├─ TLS termination
   ├─ Rate limit check
   ├─ CORS headers
   └─ Forward to app
   ↓
3. Application Middleware
   ├─ Authentication
   ├─ Authorization
   └─ Input sanitization
   ↓
4. Controller
   ├─ Validate request
   └─ Call service
   ↓
5. Service Layer
   ├─ Check cache 
   ├─ If cached → return
   └─ If not → query DB
   ↓
6. Repository
   ├─ Build query
   ├─ Execute
   └─ Return models
   ↓
7. Service → Cache result
   ↓
8. Controller → Transform (Resource)
   ↓
9. Response
   ├─ JSON structure
   ├─ Headers (Cache-Control, ETag)
   └─ Status code
   ↓
10. Client ← JSON Response
```

**الزمن المستهدف:** ≤ 300ms (p95)

---

## **المبادئ المعمارية | Architectural Principles**

### **1. Separation of Concerns | فصل المسؤوليات**

**DO:**
- Controller → HTTP handling only
- Service → Business logic only
- Repository → Data access only
- Model → Data structure only

**DON'T:**
- Controller لا يحتوي business logic
- Model لا يحتوي queries معقدة

---

### **2. Dependency Injection**

```php
// ✅ صحيح
class ProductController
{
    public function __construct(
        private ProductService $service
    ) {}
}

// ❌ خطأ
class ProductController
{
    public function index()
    {
        $service = new ProductService(); // ❌
    }
}
```

---

### **3. Stateless APIs**

**DO:**
- كل طلب مستقل
- لا session state على الخادم
- Authentication via token فقط
- قابل للتوسع الأفقي

**DON'T:**
- لا cookies للـstate
- لا server-side sessions

---

### **4. Fail Fast Principle**

```php
// ✅ Validation في البداية
public function store(Request $request)
{
    // Fail fast - validate immediately
    $validated = $request->validate([...]);
    
    // Continue only if valid
    return $this->service->create($validated);
}
```

---

## **المكونات الأساسية | Core Components**

### **مصفوفة المكونات | Component Matrix**

| المكون | التقنية الموصى بها | البديل | الاستخدام |
|--------|-------------------|--------|-----------|
| **Web Server** | NGINX | Apache | Reverse proxy, TLS |
| **Application** | Laravel, FastAPI, Express | Django, ASP.NET | Business logic |
| **Database** | MySQL, PostgreSQL | MongoDB | Primary storage |
| **Cache** | Redis | Memcached | Temporary storage |
| **Queue** | Redis, RabbitMQ | SQS, Kafka | Async jobs |
| **Storage** | S3, MinIO | Local FS | Files, images |
| **Monitoring** | Prometheus, Datadog | ELK Stack | Metrics, logs |

---

## **البيئات | Environments**

### **الفصل الإلزامي | Mandatory Separation**

```
Development (Dev)
├── للتطوير اليومي
├── بيانات وهمية
├── Debug mode ON
└── Relaxed security

Staging
├── محاكاة production
├── بيانات وهمية واقعية
├── Debug mode OFF  
└── Full security

Production (Prod)
├── البيئة الحية
├── بيانات حقيقية
├── Debug mode OFF
├── Maximum security
└── Monitoring 24/7
```

**القواعد:**

**DON'T:**
- لا تخلط البيئات أبداً

**DO:**
- Database منفصلة لكل بيئة
- Credentials مختلفة تماماً
- Deploy pipeline منفصل

---

## ️ **أنماط المعمارية | Architecture Patterns**

### **النمط المفضل: Layered Architecture**

```
Presentation Layer (Controllers, Resources)
        ↓
Application Layer (Services, Use Cases)
        ↓
Domain Layer (Business Rules, Entities)
        ↓
Infrastructure Layer (Repositories, External)
```

**المزايا:**
- فصل واضح للمسؤوليات
- سهولة الاختبار
- قابلية الصيانة
- قابلية التوسع

---

### **بدائل أخرى (عند الحاجة):**

#### **Clean Architecture**

**مناسب للمشاريع الكبيرة والمعقدة**

**Pros:**
- فصل كامل عن الـframework
- قابلية اختبار عالية جداً

**Cons:**
- أكثر تعقيداً

#### **Hexagonal Architecture**

**مناسب للتكاملات الكثيرة**

**Pros:**
- ports & adapters واضحة
- سهولة استبدال المكونات

**Cons:**
- منحنى تعلم أعلى

---

## **القرارات المعمارية | Architectural Decisions**

### **ADR Template | قالب القرار المعماري**

```markdown
# ADR-001: استخدام Repository Pattern

## الحالة | Status
✅ مقبول | Accepted

## السياق | Context
نحتاج لعزل Data access logic عن Business logic

## القرار | Decision
استخدام Repository Pattern لكل Model

## البدائل | Alternatives
- Active Record (Eloquent مباشر)
- Data Mapper

## النتائج | Consequences
✅ سهولة الاختبار
✅ قابلية التبديل
⚠️ طبقة إضافية (overhead بسيط)

## التنفيذ | Implementation
- إنشاء interface لكل repository
- Binding في Service Provider
- Dependency injection في Controllers
```

---

## **SLIs/SLOs المعمارية | Architectural SLIs/SLOs**

### **مؤشرات الجودة:**

| المؤشر | الهدف | القياس |
|--------|-------|--------|
| **Latency (p95)** | ≤ 300ms | Response time للقراءة |
| **Latency (p95)** | ≤ 800ms | Response time للكتابة |
| **Availability** | ≥ 99.9% | Uptime شهري |
| **Error Rate** | ≤ 0.5% | 5xx responses |
| **Throughput** | حسب الحاجة | Requests/second |

---

## **الأمان المعماري | Architectural Security**

### **Defense in Depth | الدفاع المتعدد الطبقات**

```
Layer 1: Edge/WAF
├── DDoS protection
├── Bot detection
└── IP filtering

Layer 2: Gateway
├── Rate limiting
├── CORS
└── Security headers

Layer 3: Application
├── Authentication
├── Authorization
└── Input validation

Layer 4: Data
├── Encryption at rest
├── Access control
└── Audit logging
```

---

## **القابلية للتوسع | Scalability**

### **Horizontal Scaling | التوسع الأفقي**

```
✅ Stateless application servers
✅ Shared cache (Redis)
✅ Shared storage (S3)
✅ Load balancer
✅ Database read replicas

مثال:
[Load Balancer]
     ↓
┌────┴────┬────────┬────────┐
│  App 1  │ App 2  │ App 3  │  ← Multiple instances
└────┬────┴────┬───┴────┬───┘
     └─────────┼────────┘
               ↓
         [Shared Redis]
               ↓
      [Master DB] → [Read Replica]
```

---

## **الحوكمة المعمارية | Architectural Governance**

### **Standards & Guidelines:**

✅ **API Design:**
- REST principles
- Naming conventions  
- Versioning strategy

✅ **Code Organization:**
- Directory structure
- Naming patterns
- PSR standards

✅ **Security:**
- Authentication strategy
- Authorization model
- Data protection

✅ **Performance:**
- Caching policy
- Database optimization
- Response optimization

✅ **Quality:**
- Testing requirements
- Code review process
- Documentation standards

---

## **التكاملات | Integrations**

### **Internal Services:**

```
API Server
    ↓
┌───┴──────┬──────────┬─────────┐
│  Cache   │  Queue   │ Storage │
└──────────┴──────────┴─────────┘
```

### **External Services (optional):**

```
API Server
    ↓
┌───┴──────┬──────────┬─────────┐
│  Email   │   SMS    │ Payment │
│ Service  │  Service │ Gateway │
└──────────┴──────────┴─────────┘
```

**التعامل مع External:**
- Circuit breaker pattern
- Retry with backoff
- Timeout limits
- Fallback mechanisms

---

## **Checklist البنية | Architecture Checklist**

### **التصميم:**
- [ ] الطبقات محددة بوضوح
- [ ] فصل المسؤوليات مطبق
- [ ] Dependency injection مستخدم
- [ ] ADRs موثقة

### **الأداء:**
- [ ] Caching strategy واضحة
- [ ] Database optimization مخططة
- [ ] قابلية التوسع محسوبة

### **الأمان:**
- [ ] Defense in depth مطبق
- [ ] Authentication centralized
- [ ] Authorization granular

### **العمليات:**
- [ ] Monitoring ready
- [ ] Logging structured
- [ ] Deployment automated

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
