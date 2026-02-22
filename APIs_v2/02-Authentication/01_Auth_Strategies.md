# استراتيجيات المصادقة — Authentication Strategies
**النطاق | Scope**: Internal APIs

---

## **الهدف | Objective**

تحديد استراتيجيات المصادقة المناسبة للـAPIs الداخلية مع مقارنة الخيارات المتاحة.

---

## **نظرة عامة | Overview**

### **ما هي المصادقة؟ | What is Authentication?**

```
Authentication (AuthN):
└─ التحقق من هوية المستخدم
   "من أنت؟"

Authorization (AuthZ):
└─ التحقق من الصلاحيات
   "ماذا يمكنك أن تفعل؟"
```

---

## **تمييز مهم: نوعان من المستخدمين | Important: Two User Types**

### **هناك فرق جوهري بين نوعين من المستخدمين:**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. العملاء | Customers (End Users)                          │
│    ├─ مستخدمو التطبيق النهائيون                            │
│    ├─ يحتاجون: Authentication ONLY (Sanctum)               │
│    ├─ لا يحتاجون: Roles & Permissions                       │
│    └─ مثال: المتسوقون في تطبيق التجارة الإلكترونية         │
│                                                               │
│ 2. مستخدمو لوحة التحكم | Admin Panel Users                 │
│    ├─ الموظفون والمسؤولون                                   │
│    ├─ يحتاجون: Authentication + RBAC                        │
│    ├─ يحتاجون: Roles & Permissions                          │
│    └─ مثال: Admin, Support, Manager, Moderator              │
└─────────────────────────────────────────────────────────────┘
```

---

### **الفرق التقني | Technical Difference:**

```php
// ✅ العميل (Customer) - Authentication Only
POST /api/v1/auth/login
Response:
{
  "user": {
    "id": 123,
    "name": "أحمد",
    "email": "ahmed@example.com"
    // لا توجد roles أو permissions
  },
  "token": "1|abc123..."
}

// بعد المصادقة، يمكن للعميل:
// - عرض المنتجات
// - إضافة إلى السلة
// - إنشاء طلبات
// - عرض طلباته فقط
// كل هذا بدون نظام roles/permissions

---

// ✅ مستخدم لوحة التحكم (Admin User) - Authentication + RBAC
POST /api/v1/admin/auth/login
Response:
{
  "user": {
    "id": 456,
    "name": "محمد",
    "email": "mohamed@company.com",
    "roles": ["support"],                    // هنا نحتاج roles
    "permissions": [                         // وهنا permissions
      "orders:read",
      "orders:update",
      "users:read"
    ]
  },
  "token": "2|xyz789..."
}

// بعد المصادقة، يتحقق النظام من:
// - هل لديه role مناسب؟
// - هل لديه permission للعملية؟
```

---

### **متى تستخدم ماذا؟ | When to Use What?**

| النوع | المصادقة | الأدوار | الصلاحيات | الاستخدام |
|-------|----------|---------|-----------|-----------|
| **العملاء** | ✅ Sanctum | ❌ لا | ❌ لا | تطبيقات Mobile/Web |
| **الإداريون** | ✅ Sanctum | ✅ نعم | ✅ نعم | لوحة التحكم Admin Panel |

---

**للـAPIs الداخلية نحتاج:**
- Stateless authentication
- Token-based
- بسيط وآمن
- قابل للتوسع
- **تمييز واضح بين العملاء والإداريين**

---

## **مقارنة الاستراتيجيات | Strategy Comparison**

| الاستراتيجية | مناسب لـ | المزايا | العيوب | التوصية |
|--------------|---------|---------|---------|---------|
| **Session-based** | Web apps تقليدية | بسيط | Stateful | ❌ غير موصى |
| **JWT** | Mobile/SPA | Stateless، شامل | Token size كبير | ✅ موصى به |
| **Laravel Sanctum** | Laravel SPA/Mobile | بسيط، Laravel-friendly | Laravel only | ✅ ممتاز لـLaravel |
| **Laravel Passport** | OAuth2 كامل | شامل جداً | معقد | ⚠️ للتكاملات فقط |
| **API Keys** | Server-to-server | بسيط جداً | أمان أقل | ⚠️ محدود |

---

## **الاستراتيجية الموصى بها: Token-Based**

### **المبدأ:**

```
1. User يرسل credentials (email/password)
   ↓
2. Server يتحقق
   ↓
3. Server يُنشئ Token
   ↓
4. User يحفظ Token
   ↓
5. كل طلب لاحق: Authorization: Bearer {token}
```

---

### **التقنيات المتاحة:**

#### **A. JWT (JSON Web Tokens)**

**الهيكل:**
```
header.payload.signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4iLCJpYXQiOjE1MTYyMzkwMjJ9.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Payload Example:**
```json
{
  "sub": "123456",           // User ID
  "name": "John Doe",
  "email": "john@example.com",
  "roles": ["customer"],
  "iat": 1705662000,         // Issued at
  "exp": 1705748400          // Expires at (24h later)
}
```

**المزايا:**
- Stateless (لا حاجة لـDB lookup)
- يحمل البيانات (claims)
- يمكن توقيعه والتحقق منه

**العيوب:**
- ⚠️ Token size كبير
- ⚠️ لا يمكن إبطاله بسهولة

**متى تستخدمه:**
- Multi-service architecture
- Microservices
- تريد Stateless 100%

**التنفيذ (PHP):**
```php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

// Create token
$payload = [
    'sub' => $user->id,
    'email' => $user->email,
    'iat' => time(),
    'exp' => time() + (24 * 60 * 60), // 24 hours
];

$token = JWT::encode($payload, env('JWT_SECRET'), 'HS256');

// Verify token
try {
    $decoded = JWT::decode($token, new Key(env('JWT_SECRET'), 'HS256'));
    $userId = $decoded->sub;
} catch (\Exception $e) {
    // Invalid token
}
```

---

#### **B. Laravel Sanctum (موصى به لـLaravel)**

**المبدأ:**

**Hybrid approach:**
- SPA: Cookie-based (stateful)
- Mobile: Token-based (stateless)

**المزايا:**
- بسيط جداً
- Laravel-native
- يدعم SPA و Mobile
- Abilities/Scopes مدمجة
- سهولة الإبطال

**العيوب:**
- ⚠️ Laravel only
- ⚠️ يحتاج DB lookup لكل طلب

**متى تستخدمه:**
- Laravel project
- Internal APIs فقط
- تريد بساطة

**التنفيذ:**
```php
// Login - Create token
$user = User::where('email', $request->email)->first();

if (!Hash::check($request->password, $user->password)) {
    throw ValidationException::withMessages([
        'email' => ['بيانات الدخول غير صحيحة'],
    ]);
}

$token = $user->createToken('mobile-app', [
    'products:read',
    'orders:write',
])->plainTextToken;

return response()->json([
    'token' => $token,
]);

// Protect routes
Route::middleware(['auth:sanctum'])->group(function () {
    // Protected routes
});

// Check abilities
if ($request->user()->tokenCan('products:read')) {
    // Allowed
}

// Revoke token
$request->user()->currentAccessToken()->delete();
```

---

#### **C. Laravel Passport (للـOAuth2)**

**متى تستخدمه:**
- **لا** للـAPIs الداخلية البسيطة
- **نعم** عند الحاجة لـOAuth2 كامل
- **نعم** للتكاملات الخارجية

**OAuth2 Flows:**
- Authorization Code (للـthird-party apps)
- Client Credentials (server-to-server)
- Password Grant (الأبسط لكن deprecated)

---

## **تصميم تدفق المصادقة | Authentication Flow Design**

### **Register Flow**

```
Client → POST /api/v1/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password_confirmation": "SecurePass123"
}

Server validates:
✓ Email unique
✓ Password strong
✓ All required fields

Server creates:
✓ User record (password hashed)
✓ Default role assigned
✓ Email verification sent (optional)
✓ Token created

Response:
{
  "success": true,
  "message": "تم التسجيل بنجاح",
  "data": {
    "user": {...},
    "token": "1|abc123..."
  }
}
```

---

### **Login Flow**

```
Client → POST /api/v1/login
{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Server:
1. Find user by email
2. Verify password (Hash::check)
3. Generate token
4. (Optional) Revoke old tokens
5. Log login event

Response:
{
  "success": true,
  "message": "تم تسجيل الدخول بنجاح",
  "data": {
    "user": {...},
    "token": "2|xyz789..."
  }
}
```

---

### **Protected Request Flow**

```
Client → GET /api/v1/products
Headers:
  Authorization: Bearer 2|xyz789...

Server Middleware:
1. Extract token من header
2. Validate token (signature, expiry)
3. Load user
4. Check permissions (optional)
5. Continue to controller

Response: Product data
```

---

### **Logout Flow**

```
Client → POST /api/v1/logout
Headers:
  Authorization: Bearer 2|xyz789...

Server:
1. Revoke current token
2. (Optional) Revoke all user tokens
3. Log logout event

Response:
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

---

## **Best Practices الأمان | Security Best Practices**

### **1. Password Security**

```php
// ✅ Always hash passwords
use Illuminate\Support\Facades\Hash;

// Store
$user->password = Hash::make($request->password);

// Verify
if (!Hash::check($request->password, $user->password)) {
    // Invalid
}

// Never:
❌ Store plain text passwords
❌ Send passwords in responses
❌ Log passwords
```

---

### **2. Token Security**

```
✅ DO:
- استخدم HTTPS فقط
- Token expiration محدد
- Revoke على logout
- Store securely في client (secure storage)

❌ DON'T:
- إرسال Token في URL
- تخزين في localStorage بدون تشفير
- Token بدون expiration
- نفس Token لكل الأجهزة
```

---

### **3. Rate Limiting على Auth**

```php
// Protect auth endpoints
RateLimiter::for('auth', function (Request $request) {
    return Limit::perMinute(5)
        ->by($request->ip())
        ->response(function () {
            return response()->json([
                'success' => false,
                'message' => 'محاولات كثيرة. حاول بعد دقيقة.',
            ], 429);
        });
});

Route::middleware(['throttle:auth'])->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
});
```

---

## **Checklist المصادقة | Authentication Checklist**

### **الأساسيات:**
- [ ] استراتيجية مصادقة محددة (JWT/Sanctum/etc.)
- [ ] Passwords مُشفّرة (bcrypt/argon2)
- [ ] Tokens تنتهي صلاحيتها
- [ ] HTTPS فقط في production

### **التدفقات:**
- [ ] Register flow مكتمل
- [ ] Login flow مكتمل
- [ ] Logout flow مكتمل
- [ ] Password reset (optional)

### **الأمان:**
- [ ] Rate limiting على auth endpoints
- [ ] Token revocation يعمل
- [ ] رسائل خطأ آمنة (لا تكشف معلومات)
- [ ] Brute force protection

### **التجربة:**
- [ ] رسائل واضحة بالعربية
- [ ] Error handling شامل
- [ ] Response موحد

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
