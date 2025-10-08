# 03. قائمة التحقق OWASP | OWASP Checklist

## 🎯 **نظرة عامة | Overview**

قائمة تحقق شاملة لـ OWASP API Security Top 10 لحماية واجهات الـ API من التهديدات الأمنية الشائعة.

**الهدف | Purpose**: تطبيق معايير OWASP الأمنية  
**الجمهور | Audience**: مهندسو الأمان، مطورو Backend  
**المتطلبات | Prerequisites**: فهم [تقوية الأمان](02_Security_Hardening.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [OWASP API Security Top 10](#owasp-top-10)
2. [API1: Broken Object Level Authorization](#api1)
3. [API2: Broken Authentication](#api2)
4. [API3: Broken Object Property Level Authorization](#api3)
5. [API4: Unrestricted Resource Consumption](#api4)
6. [API5-API10: بقية التهديدات](#api5-10)

---

## 1️⃣ OWASP API Security Top 10 (2023) {#owasp-top-10}

### **نظرة عامة**

| # | التهديد | الخطورة | التغطية |
|---|---------|---------|---------|
| **API1** | Broken Object Level Authorization | 🔴 حرجة | ✅ |
| **API2** | Broken Authentication | 🔴 حرجة | ✅ |
| **API3** | Broken Object Property Level Authorization | 🟡 عالية | ✅ |
| **API4** | Unrestricted Resource Consumption | 🟡 عالية | ✅ |
| **API5** | Broken Function Level Authorization | 🟡 عالية | ✅ |
| **API6** | Unrestricted Access to Sensitive Business Flows | 🟡 متوسطة | ✅ |
| **API7** | Server Side Request Forgery | 🟡 متوسطة | ✅ |
| **API8** | Security Misconfiguration | 🟠 متوسطة | ✅ |
| **API9** | Improper Inventory Management | 🟠 منخفضة | ✅ |
| **API10** | Unsafe Consumption of APIs | 🟠 منخفضة | ✅ |

---

## 2️⃣ API1: Broken Object Level Authorization {#api1}

### **الوصف**
المهاجم يصل إلى موارد لا يملك صلاحيات عليها بتغيير المعرف في الطلب.

### **مثال الهجوم**
```http
# المستخدم 123 يحاول الوصول لطلب المستخدم 456
GET /v1/orders/ORD-456
Authorization: Bearer <user-123-token>

❌ بدون حماية: يُرجع الطلب (خطر!)
✅ مع حماية: يُرجع 403 Forbidden
```

### **الحماية**

```php
// ✅ التحقق من الملكية
public function show(Request $request, string $orderId)
{
    $order = Order::where('customer_id', $request->user()->id)
                  ->where('id', $orderId)
                  ->firstOrFail();
    
    return new OrderResource($order);
}

// ❌ بدون حماية (خطر!)
public function show(string $orderId)
{
    $order = Order::findOrFail($orderId);  // أي أحد يمكنه الوصول!
    return new OrderResource($order);
}
```

### **قائمة التحقق**
- [ ] التحقق من ملكية المورد في كل endpoint
- [ ] استخدام `where('user_id', auth()->id())`
- [ ] Policy classes لإدارة الصلاحيات
- [ ] اختبارات للوصول غير المصرح
- [ ] لا تعتمد على معرف فقط

---

## 3️⃣ API2: Broken Authentication {#api2}

### **الوصف**
آليات مصادقة ضعيفة تسمح للمهاجم بانتحال هويات.

### **أمثلة الضعف**
```
❌ JWT بدون توقيع
❌ Tokens طويلة العمر (> 1 ساعة)
❌ بدون Refresh Token Rotation
❌ Weak password requirements
❌ بدون Rate Limiting على /login
```

### **الحماية**

```php
// ✅ JWT قصير العمر
'ttl' => 15,  // 15 دقيقة فقط

// ✅ Refresh Token Rotation
public function refresh(Request $request)
{
    $oldToken = $request->refresh_token;
    
    // التحقق من عدم إعادة الاستخدام
    if (RefreshToken::isUsed($oldToken)) {
        // إلغاء كل عائلة الرموز (Refresh Token Family)
        RefreshToken::revokeFamily($oldToken);
        abort(401, 'Token reuse detected');
    }
    
    // إلغاء القديم وإنشاء جديد
    RefreshToken::revoke($oldToken);
    $newTokens = $this->generateTokenPair($user);
    
    return response()->json($newTokens);
}

// ✅ Rate Limiting على Auth
Route::post('/auth/login')
    ->middleware('throttle:5,1');  // 5 محاولات/دقيقة

// ✅ Hash آمن
use Illuminate\Support\Facades\Hash;
Hash::make($password);  // Argon2id or bcrypt
```

### **قائمة التحقق**
- [ ] JWT قصير العمر (≤ 30 دقيقة)
- [ ] Refresh Token Rotation
- [ ] كشف إعادة استخدام Token
- [ ] Rate Limiting على Auth endpoints
- [ ] Password hash آمن (Argon2id/bcrypt)
- [ ] 2FA للمسؤولين
- [ ] Account lockout بعد فشل متكرر

---

## 4️⃣ API3: Broken Object Property Level Authorization {#api3}

### **الوصف**
المهاجم يُعدّل حقول لا يجب أن يصل إليها (Mass Assignment).

### **مثال الهجوم**
```http
# المستخدم العادي يحاول تعيين نفسه كـ admin
PATCH /v1/customers/123
{
  "name": "Ahmed",
  "role": "admin"  ← حقل حساس!
}

❌ بدون حماية: يصبح admin
✅ مع حماية: الحقل مُتجاهَل أو 403
```

### **الحماية**

```php
// ✅ في Model - تحديد fillable فقط
class Customer extends Model
{
    protected $fillable = [
        'first_name',
        'last_name',
        'phone',
        'email'
    ];
    
    protected $guarded = [
        'id',
        'role',           // فقط Admin
        'is_verified',    // عبر عملية محددة
        'balance',        // عبر Transactions فقط
        'created_at',
        'updated_at'
    ];
}

// ✅ في FormRequest - تصفية المدخلات
public function validated($key = null, $default = null)
{
    $validated = parent::validated($key, $default);
    
    // إزالة الحقول الحساسة
    unset($validated['role'], $validated['is_verified']);
    
    return $validated;
}

// ✅ تصفية الاستجابات - إخفاء الحقول الحساسة
class CustomerResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            // لا تُرجع: password_hash, role, balance
        ];
    }
}
```

### **قائمة التحقق**
- [ ] `$fillable` محدد في كل Model
- [ ] `$guarded` للحقول الحساسة
- [ ] Resource classes تُصفي المخرجات
- [ ] FormRequest يُصفي المدخلات
- [ ] لا Mass Assignment بدون تصفية
- [ ] اختبارات لمحاولات التعديل غير المصرح

---

## 5️⃣ API4: Unrestricted Resource Consumption {#api4}

### **الوصف**
المهاجم يستهلك موارد زائدة (CPU، Memory، Network) بطلبات كثيرة أو ثقيلة.

### **أمثلة الهجوم**
```http
# طلب صفحة ضخمة
GET /v1/products?limit=999999  ← DDoS محتمل

# طلبات متكررة سريعة
for i in {1..10000}; do
  curl /v1/products &
done

# Query معقد ومكلف
GET /v1/reports?from=2020-01-01&to=2025-12-31&group_by=day
```

### **الحماية**

```php
// ✅ حد أقصى للـ limit
$limit = min($request->input('limit', 20), 100);

// ✅ حد أقصى لحجم الطلب
// في server config (NGINX)
client_max_body_size 1M;

// ✅ Timeout على العمليات الطويلة
DB::statement('SET SESSION MAX_EXECUTION_TIME=5000');  // 5 ثوان

// ✅ Rate Limiting متعدد المستويات
Route::middleware('throttle:100,1')->group(function () {
    // 100 طلب/دقيقة للعملاء
});

Route::middleware('throttle:10,1')->group(function () {
    // 10 طلب/دقيقة للعمليات الثقيلة
});
```

### **قائمة التحقق**
- [ ] حد أقصى للـ pagination limit (≤ 100)
- [ ] حد أقصى لحجم الطلب (≤ 1MB)
- [ ] Rate Limiting على جميع endpoints
- [ ] Timeout على Queries
- [ ] تقييد العمليات الثقيلة
- [ ] مراقبة استهلاك الموارد

---

## 6️⃣ API5: Broken Function Level Authorization {#api5}

### **الوصف**
المستخدم العادي يصل إلى وظائف إدارية.

### **مثال الهجوم**
```http
# العميل يحاول حذف منتج (وظيفة Admin)
DELETE /v1/products/123
Authorization: Bearer <customer-token>

❌ بدون حماية: يُحذف المنتج
✅ مع حماية: 403 Forbidden
```

### **الحماية**

```php
// ✅ Middleware للأدوار
Route::middleware(['auth:api', 'role:admin'])->group(function () {
    Route::delete('/products/{id}', [ProductController::class, 'destroy']);
    Route::post('/products', [ProductController::class, 'store']);
});

// ✅ Policy
class ProductPolicy
{
    public function delete(User $user, Product $product)
    {
        return $user->hasRole('admin');
    }
}

// في Controller
$this->authorize('delete', $product);
```

### **قائمة التحقق**
- [ ] فصل routes الإدارية
- [ ] Middleware للأدوار
- [ ] Policy classes لكل مورد
- [ ] اختبارات privilege escalation
- [ ] لا admin endpoints في public routes

---

## 7️⃣ API6: Unrestricted Access to Sensitive Business Flows {#api6}

### **الوصف**
سهولة إساءة استخدام تدفقات الأعمال الحساسة (مثل إنشاء طلبات متكررة).

### **الحماية**

```php
// ✅ Idempotency للعمليات الحساسة
public function createOrder(Request $request)
{
    $idempotencyKey = $request->header('Idempotency-Key');
    
    if (!$idempotencyKey) {
        abort(400, 'Idempotency-Key required');
    }
    
    // التحقق من وجود مفتاح سابق
    $existing = IdempotencyKey::where('key', $idempotencyKey)
        ->where('user_id', auth()->id())
        ->first();
    
    if ($existing) {
        if ($existing->fingerprint !== $this->calculateFingerprint($request)) {
            abort(409, 'Idempotency key conflict');
        }
        return response()->json($existing->response, $existing->status_code)
            ->header('Idempotent-Replayed', 'true');
    }
    
    // إنشاء الطلب
    // ...
}

// ✅ التحقق من الحالة قبل التحويلات
public function cancelOrder(string $orderId)
{
    $order = Order::findOrFail($orderId);
    
    if (!in_array($order->status, ['pending', 'confirmed'])) {
        abort(422, 'Cannot cancel order in current state');
    }
    
    $order->cancel();
}
```

### **قائمة التحقق**
- [ ] Idempotency-Key للعمليات المالية
- [ ] State machine للحالات
- [ ] Audit log للعمليات الحساسة
- [ ] Rate limiting أقل على العمليات الحرجة
- [ ] فحوص business logic قبل التنفيذ

---

## 8️⃣ API7: Server Side Request Forgery (SSRF) {#api7}

### **الوصف**
المهاجم يجعل الخادم يطلب موارد داخلية أو خارجية ضارة.

### **مثال الهجوم**
```http
# المستخدم يُرسل URL خبيث
POST /v1/webhooks/test
{
  "url": "http://169.254.169.254/latest/meta-data/"  ← AWS metadata!
}

POST /v1/images/fetch
{
  "url": "http://localhost:8080/admin"  ← خدمة داخلية!
}
```

### **الحماية**

```php
// ✅ Allowlist للنطاقات
private $allowedDomains = [
    'api.partner1.com',
    'webhook.partner2.com',
];

public function validateWebhookUrl(string $url)
{
    $parsed = parse_url($url);
    
    // رفض URLs غير HTTP/HTTPS
    if (!in_array($parsed['scheme'], ['http', 'https'])) {
        abort(400, 'Invalid URL scheme');
    }
    
    // رفض IPs المحلية
    $blockedHosts = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '169.254.169.254',  // AWS metadata
        '10.0.0.0/8',       // Private network
    ];
    
    if (in_array($parsed['host'], $blockedHosts)) {
        abort(400, 'Access to internal resources not allowed');
    }
    
    // التحقق من Allowlist
    if (!in_array($parsed['host'], $this->allowedDomains)) {
        abort(400, 'Domain not in allowlist');
    }
    
    return true;
}
```

### **قائمة التحقق**
- [ ] Allowlist للنطاقات المسموحة
- [ ] منع الوصول للـ IPs المحلية
- [ ] منع الوصول لـ metadata endpoints
- [ ] Timeout على المكالمات الخارجية
- [ ] عدم اتباع redirects
- [ ] التحقق من Content-Type في الاستجابات

---

## 9️⃣ API8: Security Misconfiguration {#api8}

### **الوصف**
سوء تكوين الأمان (CORS، Headers، TLS، إلخ).

### **قائمة التحقق الشاملة**

#### **TLS/HTTPS**
- [ ] TLS 1.2+ فقط
- [ ] إعادة توجيه HTTP → HTTPS
- [ ] HSTS مفعل
- [ ] شهادات صالحة ومحدثة

#### **CORS**
```php
// ✅ تكوين صارم
'paths' => ['api/*'],
'allowed_origins' => [
    'https://zahraah.com',
    'https://app.zahraah.com',
],
'allowed_methods' => ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
'allowed_headers' => ['Authorization', 'Content-Type'],
'exposed_headers' => ['X-RateLimit-*'],
'max_age' => 3600,
'supports_credentials' => true,

// ❌ خطر!
'allowed_origins' => ['*'],  // يسمح لأي نطاق
```

#### **Security Headers**
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'
```

#### **إخفاء معلومات النظام**
```php
// ✅ إخفاء Laravel version
// في public/index.php
header_remove('X-Powered-By');

// في NGINX
server_tokens off;
```

### **قائمة التحقق**
- [ ] HTTPS إلزامي
- [ ] CORS محدد بدقة
- [ ] Security headers مفعلة
- [ ] إخفاء معلومات الخادم
- [ ] Debug mode = false في Production
- [ ] Error reporting محدود
- [ ] File permissions صحيحة

---

## 🔟 API9: Improper Inventory Management {#api9}

### **الوصف**
عدم توثيق أو تتبع جميع endpoints (endpoints مخفية، قديمة، أو غير موثقة).

### **الحماية**

```yaml
# ✅ OpenAPI كامل ومحدث
openapi: 3.1.0
info:
  version: 1.0.0
  
paths:
  /products: ...
  /orders: ...
  /customers: ...
  # جميع endpoints موثقة

# ✅ Version tracking
# جميع endpoints لها version واضح
/v1/products
/v2/products  # مع Deprecation plan
```

### **قائمة التحقق**
- [ ] جميع endpoints في OpenAPI
- [ ] لا endpoints غير موثقة
- [ ] Deprecation policy واضحة
- [ ] Version management
- [ ] جرد دوري للـ endpoints
- [ ] إزالة endpoints غير المستخدمة

---

## 🔟 API10: Unsafe Consumption of APIs {#api10}

### **الوصف**
استهلاك غير آمن لـ APIs خارجية (عدم التحقق من الاستجابات).

### **الحماية**

```php
// ✅ التحقق من استجابات الطرف الثالث
public function processPayment($orderId, $amount)
{
    try {
        $response = Http::timeout(10)  // Timeout
            ->withHeaders(['X-API-Key' => config('payment.api_key')])
            ->post('https://payment-gateway.com/charge', [
                'order_id' => $orderId,
                'amount' => $amount
            ]);
        
        // التحقق من Status
        if (!$response->successful()) {
            throw new PaymentException('Payment failed');
        }
        
        // التحقق من البنية
        $data = $response->json();
        if (!isset($data['transaction_id']) || !isset($data['status'])) {
            throw new PaymentException('Invalid response structure');
        }
        
        // Sanitize البيانات
        return [
            'transaction_id' => filter_var($data['transaction_id'], FILTER_SANITIZE_STRING),
            'status' => in_array($data['status'], ['success', 'pending', 'failed']) 
                ? $data['status'] 
                : 'unknown'
        ];
        
    } catch (ConnectionException $e) {
        // Circuit Breaker
        Cache::put('payment-gateway-down', true, 300);  // 5 دقائق
        throw new ServiceUnavailableException();
    }
}
```

### **قائمة التحقق**
- [ ] Timeout على المكالمات الخارجية
- [ ] التحقق من Status Code
- [ ] التحقق من بنية الاستجابة
- [ ] Sanitize البيانات الواردة
- [ ] Circuit Breaker للخدمات غير الموثوقة
- [ ] عدم الثقة العمياء بالبيانات الخارجية
- [ ] Retry مع Exponential Backoff

---

## ✅ **قائمة التحقق الشاملة | Complete Checklist**

### **قبل النشر إلى Production**

#### **المصادقة والتخويل**
- [ ] ✅ Object Level Authorization في كل endpoint
- [ ] ✅ JWT قصير العمر + Refresh Rotation
- [ ] ✅ Property Level Authorization (fillable/guarded)
- [ ] ✅ Function Level Authorization (roles/policies)
- [ ] ✅ 2FA للمسؤولين

#### **الموارد والحدود**
- [ ] ✅ Rate Limiting على جميع endpoints
- [ ] ✅ حد أقصى لـ pagination (100)
- [ ] ✅ حد أقصى لحجم الطلب (1MB)
- [ ] ✅ Timeout على Queries
- [ ] ✅ Circuit Breaker للخدمات الخارجية

#### **التدفقات الحساسة**
- [ ] ✅ Idempotency-Key للعمليات المالية
- [ ] ✅ State validation قبل التحويلات
- [ ] ✅ Audit log للعمليات الحرجة
- [ ] ✅ Business logic validation

#### **SSRF والتكاملات**
- [ ] ✅ Allowlist للنطاقات
- [ ] ✅ منع الوصول للموارد الداخلية
- [ ] ✅ التحقق من استجابات الطرف الثالث
- [ ] ✅ Timeout على المكالمات الخارجية

#### **التكوين الأمني**
- [ ] ✅ HTTPS فقط
- [ ] ✅ CORS محدد
- [ ] ✅ Security Headers مفعلة
- [ ] ✅ Debug mode = false
- [ ] ✅ إخفاء معلومات النظام

#### **الجرد والتوثيق**
- [ ] ✅ OpenAPI كامل ومحدث
- [ ] ✅ جميع endpoints موثقة
- [ ] ✅ Deprecation policy
- [ ] ✅ Version management

#### **استهلاك APIs**
- [ ] ✅ Timeout + Circuit Breaker
- [ ] ✅ التحقق من الاستجابات
- [ ] ✅ Sanitization للبيانات الواردة
- [ ] ✅ عدم الثقة العمياء

---

## 🔍 **أدوات الفحص | Scanning Tools**

### **1. OWASP ZAP**
```bash
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.staging.zahraah.com/openapi.yaml \
  -f openapi \
  -r zap-report.html
```

### **2. Burp Suite**
- Import OpenAPI
- Active Scan
- Manual testing

### **3. SQLMap (للـ SQL Injection)**
```bash
sqlmap -u "https://api.staging.zahraah.com/v1/products?id=123" \
  --cookie="token=..." \
  --level=5 \
  --risk=3
```

---

## 📊 **معايير القبول | Acceptance Criteria**

| التهديد | الحالة | الأدلة |
|---------|--------|--------|
| API1 | ✅ محمي | Authorization checks في كل endpoint |
| API2 | ✅ محمي | JWT قصير + Rotation + Rate Limit |
| API3 | ✅ محمي | fillable/guarded + Resource filtering |
| API4 | ✅ محمي | Rate Limits + Max sizes + Timeouts |
| API5 | ✅ محمي | Role-based routes + Policies |
| API6 | ✅ محمي | Idempotency + State validation |
| API7 | ✅ محمي | URL validation + Allowlist |
| API8 | ✅ محمي | TLS + CORS + Headers + Config |
| API9 | ✅ محمي | OpenAPI complete + Versioning |
| API10 | ✅ محمي | Timeout + Validation + Circuit Breaker |

---

## 🔗 **التنقل | Navigation**

[← السابق: تقوية الأمان | Previous: Security Hardening](02_Security_Hardening.md)

[التالي: معالجة الأخطاء | Next: Error Handling →](../04-Implementation/01_Response_Error_Handling.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [API Security Best Practices](https://owasp.org/www-community/api_security_project)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
