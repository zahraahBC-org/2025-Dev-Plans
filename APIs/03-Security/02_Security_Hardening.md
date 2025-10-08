# 02. تقوية الأمان | Security Hardening

## 🎯 **نظرة عامة | Overview**

إجراءات وسياسات تقوية الأمان لحماية واجهات الـ API من الهجمات والتهديدات الشائعة.

**الهدف | Purpose**: تطبيق طبقات الأمان المتعددة  
**الجمهور | Audience**: مهندسو الأمان، DevOps، Backend  
**المتطلبات | Prerequisites**: فهم [المصادقة](01_Authentication_Authorization.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [TLS/SSL](#tlsssl)
2. [WAF - Web Application Firewall](#waf)
3. [Rate Limiting](#rate-limiting)
4. [Input Validation](#input-validation)
5. [Secret Management](#secret-management)

---

## 1️⃣ TLS/SSL {#tlsssl}

### **التكوين الإلزامي**

```nginx
# NGINX Configuration
server {
    listen 443 ssl http2;
    server_name api.zahraah.com;
    
    # TLS 1.2+ فقط
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Ciphers قوية فقط
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    
    # الشهادات
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}

# إعادة توجيه HTTP → HTTPS
server {
    listen 80;
    server_name api.zahraah.com;
    return 301 https://$server_name$request_uri;
}
```

---

### **قائمة التحقق**
- [ ] TLS 1.2+ فقط
- [ ] شهادات صالحة ومحدثة
- [ ] تجديد تلقائي (Let's Encrypt)
- [ ] HSTS مفعل
- [ ] إعادة توجيه HTTP → HTTPS
- [ ] HTTP/2 أو HTTP/3 مفعل

---

## 2️⃣ WAF - Web Application Firewall {#waf}

### **Cloudflare WAF**

#### **القواعد الأساسية**
```yaml
# OWASP Core Ruleset
- SQL Injection Protection
- XSS Protection
- Command Injection
- Path Traversal
- LDAP Injection

# Custom Rules
- Block known bad IPs
- Challenge suspicious behavior
- Rate limit aggressive bots
```

#### **قواعد مخصصة**
```javascript
// Cloudflare Firewall Rule
(
  http.request.uri.path contains "/admin" and
  not ip.src in {185.46.0.0/16 10.0.0.0/8}
)
  → Block

(
  http.request.uri.path eq "/v1/auth/login" and
  cf.threat_score > 10
)
  → Challenge (CAPTCHA)
```

---

## 3️⃣ Rate Limiting {#rate-limiting}

### **استراتيجيات متعددة الطبقات**

#### **الطبقة 1: Edge (Cloudflare)**
```
IP-based Rate Limiting:
- 1000 requests / 60 seconds per IP
- Block: 429 Too Many Requests
```

#### **الطبقة 2: API Gateway**
```yaml
rate_limits:
  # حسب المستخدم
  by_user:
    customer: 100/min
    partner: 600/min
    admin: unlimited
  
  # حسب Endpoint
  by_endpoint:
    /v1/auth/login: 5/min
    /v1/auth/otp/request: 3/min
    /v1/orders: 30/min
    /v1/products: 120/min
```

#### **الطبقة 3: Application Layer**
```php
// Laravel Middleware
use Illuminate\Routing\Middleware\ThrottleRequests;

Route::middleware(['throttle:100,1'])->group(function () {
    Route::get('/products', [ProductController::class, 'index']);
});

// حد مخصص لـ OTP
Route::post('/auth/otp/request')
    ->middleware('throttle:3,1'); // 3 طلبات/دقيقة
```

---

### **استجابة Rate Limit**
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704715260
Retry-After: 60

{
  "error": {
    "code": "E6001",
    "message": "Rate limit exceeded",
    "details": "Maximum 100 requests per minute. Retry after 60 seconds."
  }
}
```

---

## 4️⃣ Input Validation {#input-validation}

### **التحقق الشامل**

#### **Laravel Validation Rules**
```php
// في FormRequest
public function rules(): array
{
    return [
        // أساسي
        'email' => 'required|email|max:255',
        'phone' => ['required', 'regex:/^\+9665[0-9]{8}$/'],
        
        // أرقام
        'quantity' => 'required|integer|min:1|max:99',
        'price' => 'required|numeric|min:0|max:999999.99',
        
        // تواريخ
        'birth_date' => 'nullable|date|before:today|after:1900-01-01',
        'delivery_date' => 'required|date|after:today',
        
        // مصفوفات
        'items' => 'required|array|min:1|max:50',
        'items.*.variant_id' => 'required|exists:variants,id',
        'items.*.quantity' => 'required|integer|min:1',
        
        // enum
        'status' => 'required|in:pending,confirmed,cancelled',
        'payment_method' => 'required|in:cod,online,wallet',
        
        // علاقات
        'category_id' => 'required|exists:categories,id',
        'brand_id' => 'nullable|exists:brands,id',
        
        // نصوص
        'description' => 'nullable|string|max:5000',
        'note' => 'nullable|string|max:500',
    ];
}

// رسائل مخصصة بالعربية
public function messages(): array
{
    return [
        'email.required' => 'البريد الإلكتروني مطلوب',
        'email.email' => 'يجب أن يكون بريد إلكتروني صالح',
        'phone.regex' => 'رقم الهاتف يجب أن يبدأ بـ +9665',
        'quantity.min' => 'الكمية يجب أن تكون 1 على الأقل',
        'items.min' => 'يجب إضافة عنصر واحد على الأقل',
    ];
}
```

---

### **منع Mass Assignment**
```php
// في Model
protected $fillable = [
    'name_ar',
    'name_en',
    'price',
    'category_id'
];

protected $guarded = [
    'id',
    'created_at',
    'updated_at',
    'is_verified',  // فقط Admin
    'status'        // عبر workflow محدد
];
```

---

## 5️⃣ Secret Management {#secret-management}

### **تخزين الأسرار**

#### **✅ الطريقة الصحيحة**
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name zahraah/api/jwt-secret \
  --secret-string "your-secret-key-here"

# في التطبيق
$jwtSecret = $secretsManager->getSecret('zahraah/api/jwt-secret');
```

```php
// .env (مشفر في Production)
JWT_SECRET=${AWS_SECRET:zahraah/api/jwt-secret}
DB_PASSWORD=${AWS_SECRET:zahraah/api/db-password}
PAYMENT_API_KEY=${AWS_SECRET:zahraah/api/payment-key}
```

#### **❌ الطريقة الخاطئة**
```php
❌ $jwtSecret = "my-secret-123";  // hard-coded
❌ .env (في Git)
❌ في ملف config مُشارك
```

---

### **دوران المفاتيح | Key Rotation**

```
Schedule: كل 90 يوم

1. إنشاء مفتاح جديد (KID: key-2025-02)
2. إضافة للـ JWKS (مع القديم)
3. بدء التوقيع بالمفتاح الجديد
4. الاحتفاظ بالقديم للتحقق (30 يوم)
5. إزالة المفتاح القديم بعد 30 يوم
```

---

## ✅ **قائمة التحقق | Checklist**

### **الأمان الأساسي**
- [ ] HTTPS إلزامي
- [ ] TLS 1.2+ فقط
- [ ] WAF مفعل
- [ ] Rate Limiting على جميع endpoints
- [ ] Input validation شامل
- [ ] Output encoding
- [ ] CORS مقيد
- [ ] Security headers

### **المصادقة والتخويل**
- [ ] JWT قصير العمر
- [ ] Refresh token rotation
- [ ] RBAC مطبق
- [ ] 2FA للمسؤولين
- [ ] Session management

### **البيانات**
- [ ] لا PII في logs
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Secret Manager للأسرار
- [ ] Data Classification

---

## 🔗 **التنقل | Navigation**

[← السابق: المصادقة | Previous: Authentication](01_Authentication_Authorization.md)

[التالي: قائمة OWASP | Next: OWASP Checklist →](03_OWASP_Checklist.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved