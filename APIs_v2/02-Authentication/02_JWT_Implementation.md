# تنفيذ JWT — JWT Implementation
**المعيار | Standard**: RFC 7519

---

## **الهدف | Objective**

دليل عملي شامل لتنفيذ JWT Authentication في APIs.

---

## **ما هو JWT؟ | What is JWT?**

**JSON Web Token** - رمز موقّع يحمل معلومات (claims) بشكل آمن.

### **الهيكل | Structure**

```
header.payload.signature

مثال:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

---

### **الأجزاء الثلاثة:**

#### **1. Header**
```json
{
  "alg": "HS256",      // Algorithm
  "typ": "JWT"         // Type
}
```

#### **2. Payload (Claims)**

**للعملاء | For Customers (Authentication Only):**
```json
{
  "sub": "1234567890",      // Subject (User ID)
  "name": "John Doe",
  "email": "john@example.com",
  // ⚠️ لا roles أو permissions - العملاء يحتاجون authentication فقط
  "iat": 1705662000,        // Issued At
  "exp": 1705748400         // Expires At
}
```

**لمستخدمي لوحة التحكم | For Admin Panel Users (Authentication + RBAC):**
```json
{
  "sub": "789",             // Admin User ID
  "name": "Mohamed Ahmed",
  "email": "mohamed@company.com",
  "roles": ["support"],     // ✅ فقط للإداريين
  "permissions": [          // ✅ فقط للإداريين
    "orders:read",
    "orders:update"
  ],
  "iat": 1705662000,
  "exp": 1705748400
}
```

#### **3. Signature**
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

---

## **التنفيذ العملي | Practical Implementation**

### **A. باستخدام مكتبة PHP-JWT**

#### **التثبيت:**
```bash
composer require firebase/php-jwt
```

#### **إنشاء Token (Customer):**
```php
public function createCustomerToken(User $user): string
{
    $payload = [
        'sub' => $user->id,
        'email' => $user->email,
        'user_type' => 'customer', // ⚠️ No roles/permissions
        'iat' => time(),
        'exp' => time() + 86400,
    ];
    
    return JWT::encode($payload, env('JWT_SECRET'), 'HS256');
}
```

#### **إنشاء Token (Admin):**
```php
public function createAdminToken(User $user): string
{
    $payload = [
        'sub' => $user->id,
        'roles' => $user->roles->pluck('name'), // ✅ Only for admins
        'permissions' => $user->getAllPermissions()->pluck('name'),
        'user_type' => 'admin',
        'iat' => time(),
        'exp' => time() + 86400,
    ];
    
    return JWT::encode($payload, env('JWT_SECRET'), 'HS256');
}
```

#### **Verify Token:**
```php
public function verifyToken(string $token): object
{
    return JWT::decode($token, new Key(env('JWT_SECRET'), 'HS256'));
}
```

---

#### **Auth Middleware Example:**
```php
class AuthenticateJWT
{
    public function handle($request, Closure $next)
    {
        $token = $request->bearerToken();
        if (!$token) {
            return response()->json(['message' => 'Token مفقود'], 401);
        }
        
        try {
            $decoded = $this->jwtService->verifyToken($token);
            $request->setUserResolver(fn() => User::find($decoded->sub));
        } catch (\Exception $e) {
            return response()->json(['message' => 'Token غير صالح'], 401);
        }
        
        return $next($request);
    }
}
```

---

### **B. باستخدام tymon/jwt-auth**

#### **التثبيت:**
```bash
composer require tymon/jwt-auth
php artisan jwt:secret
```

#### **User Model:**
```php
class User extends Authenticatable implements JWTSubject
{
    public function getJWTIdentifier() { return $this->getKey(); }
    
    public function getJWTCustomClaims()
    {
        return ['email' => $this->email, 'roles' => $this->roles->pluck('name')];
    }
}
```

#### **الاستخدام:**
```php
// Login & Generate Token
$token = JWTAuth::attempt($credentials);

// Get authenticated user
$user = JWTAuth::parseToken()->authenticate();

// Refresh token
$newToken = JWTAuth::refresh($token);
```

---

## **Refresh Token Strategy**

### **لماذا Refresh Tokens؟**

```
Access Token (قصير العمر):
├── 15-30 دقيقة
├── للطلبات اليومية
└── أقل خطورة عند السرقة

Refresh Token (طويل العمر):
├── 7-30 يوم
├── لتجديد Access token
└── يُخزن بأمان
```

---

### **التنفيذ:**

```php
// Create tokens at login
$accessToken = $this->createAccessToken($user);
$refreshToken = bin2hex(random_bytes(64));

// Store refresh token
$user->refreshTokens()->create([
    'token' => hash('sha256', $refreshToken),
    'expires_at' => now()->addDays(30),
]);

return [
    'access_token' => $accessToken,  // 30 minutes
    'refresh_token' => $refreshToken, // 30 days
    'expires_in' => 1800,
];
```

```php
// Refresh endpoint
public function refresh(string $refreshToken): array
{
    $tokenRecord = RefreshToken::where('token', hash('sha256', $refreshToken))
        ->where('expires_at', '>', now())
        ->firstOrFail();
    
    return ['access_token' => $this->createAccessToken($tokenRecord->user)];
}
```

### **Database Schema:**

```php
// Refer to Database plan for full schema
Schema::create('refresh_tokens', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('token', 128)->unique();
    $table->timestamp('expires_at');
    // ... other columns - see Database plan
});
```

---

## **Best Practices الأمان | Security Best Practices**

### **1. Secret Key Management**

```bash
# .env
JWT_SECRET=very-long-random-string-at-least-32-characters

# Generate secure secret
php artisan key:generate --show
openssl rand -base64 32
```

**DO:**
- استخدم secret طويل (≥256 bits)
- احفظه في .env فقط
- لا تُشاركه أبداً
- دوّر بشكل دوري (كل 6-12 شهر)

**DON'T:**
- لا تحفظه في الكود
- لا تُرسله للـclient
- لا تُسجّله في logs

---

### **2. Token Expiration**

```php
// ✅ موصى به
$payload = [
    'sub' => $user->id,
    'iat' => time(),
    'exp' => time() + 1800,  // 30 minutes
];

// ❌ خطير - بدون expiration
$payload = [
    'sub' => $user->id,
    'iat' => time(),
    // No exp!
];
```

**التوصيات:**
- Access Token: 15-30 دقيقة
- Refresh Token: 7-30 يوم
- Remember me: حتى 90 يوم (مع تحذيرات أمنية)

---

### **3. Token Storage على Client**

**Mobile Apps:**
- Secure Storage (Keychain/KeyStore)
- NOT SharedPreferences/UserDefaults

**Web/SPA:**
- httpOnly cookies (الأفضل)
- أو sessionStorage (ليس localStorage)

**NEVER:**
- localStorage بدون تشفير
- URL parameters
- Plain text anywhere

---

### **4. Token Revocation**

```php
// Blacklist approach
public function revoke(string $token): void
{
    $jti = $this->getJti($token); // Token ID from claims
    Cache::put("blacklist:{$jti}", true, $this->getExpiry($token));
}

// Check in middleware
if (Cache::has("blacklist:{$jti}")) {
    throw new UnauthorizedException('Token محظور');
}
```

---

## **Claims الموصى بها | Recommended Claims**

### **Standard Claims (RFC 7519):**

```json
{
  "iss": "https://api.example.com",    // Issuer
  "sub": "123456",                      // Subject (User ID)
  "aud": "mobile-app",                  // Audience
  "exp": 1705748400,                    // Expiration
  "nbf": 1705662000,                    // Not Before
  "iat": 1705662000,                    // Issued At
  "jti": "unique-token-id"              // JWT ID (للـrevocation)
}
```

---

### **Custom Claims (حسب الحاجة):**

**للعملاء | For Customers:**
```json
{
  // User info
  "user_id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "user_type": "customer",
  
  // ⚠️ NO roles or permissions for customers
  
  // Context
  "device_id": "abc123",
  "app_version": "1.0.0",
  "locale": "ar"
}
```

**لمستخدمي لوحة التحكم | For Admin Users:**
```json
{
  // User info
  "user_id": 456,
  "email": "admin@company.com",
  "name": "Mohamed Ahmed",
  "user_type": "admin",
  
  // Roles & Permissions (✅ فقط للإداريين)
  "roles": ["support", "moderator"],
  "permissions": ["products:read", "orders:write", "users:read"],
  
  // Context
  "device_id": "desktop-123",
  "app_version": "1.0.0",
  "locale": "ar"
}
```

**⚠️ تحذير:**

**DON'T - لا تضع بيانات حساسة:**
- Passwords
- Credit card numbers
- Personal identifiable info (PII)

**DO:**
- فقط معلومات ضرورية للـauthorization

---

## **Complete Auth Flow**

### **1. Registration (Customer)**

```php
public function register(RegisterRequest $request)
{
    $user = User::create([
        'name' => $request->name,
        'email' => $request->email,
        'password' => Hash::make($request->password),
        'user_type' => 'customer', // ⚠️ NO roles for customers
    ]);
    
    $accessToken = $this->jwtService->createCustomerToken($user);
    
    return response()->json([
        'success' => true,
        'data' => ['user' => new UserResource($user), 'access_token' => $accessToken],
    ], 201);
}
```

### **2. Login**

```php
public function login(LoginRequest $request)
{
    $user = User::where('email', $request->email)->first();
    
    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json(['message' => 'بيانات الدخول غير صحيحة'], 401);
    }
    
    $token = $this->jwtService->createAccessToken($user);
    
    return response()->json(['access_token' => $token, 'expires_in' => 1800]);
}
```

### **3. Refresh**

```php
public function refresh(Request $request)
{
    $tokens = $this->jwtService->refreshTokens($request->refresh_token);
    return response()->json(['access_token' => $tokens['access_token']]);
}
```

### **4. Logout**

```php
public function logout(Request $request)
{
    $this->jwtService->revokeToken($request->bearerToken());
    return response()->json(['message' => 'تم تسجيل الخروج']);
}
```

---

## **Token Security Checklist**

### **الإنشاء:**
- [ ] Secret key قوي (≥256 bits)
- [ ] Algorithm آمن (HS256, RS256)
- [ ] Expiration محدد
- [ ] Claims ضرورية فقط
- [ ] لا بيانات حساسة في payload

### **التخزين:**
- [ ] Secret في .env فقط
- [ ] Secret غير مُشارك أبداً
- [ ] Token rotation strategy

### **الاستخدام:**
- [ ] HTTPS فقط
- [ ] Bearer token في header
- [ ] Validation في كل طلب
- [ ] Blacklist للـrevocation

### **الحماية:**
- [ ] Rate limiting على auth endpoints
- [ ] Brute force protection
- [ ] Token expiration قصير
- [ ] Refresh token آمن

---

## **Routes Example**

```php
// Public routes
Route::prefix('v1')->group(function () {
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
});

// Protected routes - requires JWT
Route::prefix('v1')->middleware('auth.jwt')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me', [AuthController::class, 'me']);
    Route::apiResource('products', ProductController::class);
});
```

---

## **Testing Example**

```php
public function test_user_can_login_and_get_token(): void
{
    $user = User::factory()->create(['password' => Hash::make('password')]);
    
    $response = $this->postJson('/api/v1/login', [
        'email' => $user->email,
        'password' => 'password',
    ]);
    
    $response->assertStatus(200)
        ->assertJsonStructure(['access_token', 'expires_in']);
}

public function test_cannot_access_protected_route_without_token(): void
{
    $this->getJson('/api/v1/me')->assertStatus(401);
}
```

---

## **Checklist التنفيذ | Implementation Checklist**

### **Setup:**
- [ ] مكتبة JWT مثبتة
- [ ] JWT_SECRET في .env
- [ ] TTL محدد بوضوح
- [ ] Algorithm محدد (HS256/RS256)

### **Endpoints:**
- [ ] POST /register
- [ ] POST /login
- [ ] POST /refresh
- [ ] POST /logout
- [ ] GET /me

### **Security:**
- [ ] Passwords hashed
- [ ] Tokens signed
- [ ] Expiration enforced
- [ ] HTTPS only
- [ ] Rate limiting

### **Testing:**
- [ ] Login successful test
- [ ] Invalid credentials test
- [ ] Token validation test
- [ ] Expired token test
- [ ] Refresh token test

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
