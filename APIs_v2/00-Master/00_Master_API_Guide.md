# الدليل الرئيسي الشامل — Master API Guide
**التقنيات | Stack**: Laravel 10+ + Sanctum + MySQL + Redis

---

## **مقدمة | Introduction**

### **الغرض من هذا الدليل | Purpose**

هذا الدليل هو **المرجع الشامل والموحد** لفريق التطوير عند بناء وصيانة APIs تطبيق زهراه للتجارة الإلكترونية باستخدام Laravel وSanctum.

### **لمن هذا الدليل؟ | Who is this for?**

- **Backend Developers**: للتنفيذ اليومي
- **Tech Leads**: للمراجعة والتصميم
- **DevOps/SRE**: للـDeployment والمراقبة
- **QA Engineers**: للاختبارات
- **Flutter Developers**: لفهم الـAPIs

### **نطاق الخطة | Scope**

#### **ما يُغطيه:**
- APIs لتطبيق Flutter (iOS + Android)
- APIs للوحة التحكم الإدارية
- مصادقة Sanctum لـ SPA/Mobile
- RBAC بسيط وواضح
- Performance optimization
- Testing strategy

#### **ما لا يُغطيه:**
- تكاملات شركاء خارجيين
- OAuth2 للأطراف الثالثة
- Public Developer Portal
- SDK Generation
- Webhooks للشركاء

---

## **البنية المعمارية | Architecture Overview**

### **الطبقات الأساسية | Core Layers**

```
┌─────────────────────────────────────┐
│    Flutter App + Admin Panel        │  ← Clients
└──────────────┬──────────────────────┘
               │ HTTPS + Sanctum Token
               ▼
┌─────────────────────────────────────┐
│        API Gateway (NGINX)          │  ← Edge Layer
│  • HTTPS/TLS                        │
│  • Rate Limiting                    │
│  • CORS                             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Laravel Application            │  ← Application Layer
│  ┌─────────────────────────────┐   │
│  │  Controllers (HTTP Layer)   │   │
│  └────────────┬────────────────┘   │
│               │                     │
│  ┌────────────▼────────────────┐   │
│  │  Services (Business Logic)  │   │
│  └────────────┬────────────────┘   │
│               │                     │
│  ┌────────────▼────────────────┐   │
│  │  Repositories (Data Access) │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌─────────┐
│  MySQL  │         │  Redis  │  ← Data Layer
└─────────┘         └─────────┘
```

### **المكونات الأساسية | Core Components**

| المكون | التقنية | الدور |
|--------|---------|-------|
| **Web Server** | NGINX | Reverse proxy, HTTPS, Rate limit |
| **Application** | Laravel 10+ | Business logic, APIs |
| **Authentication** | Sanctum | Token-based auth |
| **Database** | MySQL 8+ | Primary data store |
| **Cache** | Redis | Session, cache, queues |
| **Queue** | Redis/Database | Background jobs |
| **Storage** | S3-compatible | Files, images |

---

## **المصادقة والتخويل | Authentication & Authorization**

### **1. Laravel Sanctum Setup**

#### **التثبيت | Installation**

```bash
# Install Sanctum
composer require laravel/sanctum

# Publish config
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"

# Run migrations
php artisan migrate
```

#### **التهيئة | Configuration**

```php
// config/sanctum.php - Key settings
return [
    'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', 'localhost')),
    'guard' => ['web'],
    'expiration' => null,
    // ... see full config in Laravel Sanctum docs
];
```

### **2. User Model Setup**

```php
// User Model with Sanctum
class User extends Authenticatable
{
    use HasApiTokens;
    
    protected $fillable = ['name', 'email', 'phone', 'password'];
    protected $hidden = ['password', 'remember_token'];
    protected $casts = ['email_verified_at' => 'datetime', 'password' => 'hashed'];
    
    public function roles() { return $this->belongsToMany(Role::class); }
}
```

### **3. Authentication Endpoints**

```php
// Register endpoint
public function register(RegisterRequest $request)
{
    $user = User::create([
        'email' => $request->email,
        'password' => Hash::make($request->password),
    ]);
    
    return response()->json([
        'user' => new UserResource($user),
        'token' => $user->createToken('app')->plainTextToken,
    ], 201);
}

// Login endpoint
public function login(LoginRequest $request)
{
    $user = User::where('email', $request->email)->first();
    
    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json(['message' => 'Invalid credentials'], 401);
    }
    
    return response()->json([
        'user' => new UserResource($user),
        'token' => $user->createToken('app')->plainTextToken,
    ]);
}
```

### **4. RBAC Implementation**

#### **Database Schema**

```php
// Refer to Database plan for full schema
// database/migrations/create_roles_tables.php
Schema::create('roles', function (Blueprint $table) {
    $table->id();
    $table->string('name')->unique();
    $table->string('display_name');
    // ... other columns - see Database plan
    $table->timestamps();
});

Schema::create('permissions', function (Blueprint $table) {
    $table->id();
    $table->string('name')->unique();
    // ... other columns - see Database plan
    $table->timestamps();
});

Schema::create('role_user', function (Blueprint $table) {
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->primary(['role_id', 'user_id']);
});

Schema::create('permission_role', function (Blueprint $table) {
    $table->foreignId('permission_id')->constrained()->onDelete('cascade');
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->primary(['permission_id', 'role_id']);
});
```

#### **الأدوار الأساسية | Default Roles**

```php
// database/seeders/RoleSeeder.php - Basic structure
$roles = [
    ['name' => 'admin', 'permissions' => ['products:*', 'orders:*', 'users:*']],
    ['name' => 'support', 'permissions' => ['orders:read', 'orders:update']],
];

foreach ($roles as $roleData) {
    $role = Role::create(['name' => $roleData['name']]);
    // ... attach permissions
}

// ⚠️ Note: Customers don't have roles - see 02-Authentication/00-IMPORTANT_DISTINCTION.md
```

#### **Middleware للتحقق من الصلاحيات**

```php
// Permission middleware
public function handle($request, Closure $next, string $permission)
{
    if (!$request->user()->hasPermission($permission)) {
        return response()->json(['message' => 'Forbidden'], 403);
    }
    
    return $next($request);
}
```

---

## **تصميم الـAPIs | API Design**

### **1. مبادئ REST الأساسية**

#### **التسمية الموحدة | Naming Conventions**

```
✅ استخدم أسماء جمع للـResources:
   GET    /api/v1/products
   GET    /api/v1/products/{id}
   POST   /api/v1/products
   PUT    /api/v1/products/{id}
   PATCH  /api/v1/products/{id}
   DELETE /api/v1/products/{id}

✅ استخدم kebab-case للمسارات:
   /api/v1/order-items
   /api/v1/product-categories

✅ استخدم snake_case لحقول JSON:
   {
     "product_id": 123,
     "created_at": "2025-10-19T10:00:00Z",
     "is_active": true
   }
```

#### **HTTP Methods القياسية**

| Method | الاستخدام | Idempotent |
|--------|-----------|-----------|
| **GET** | قراءة البيانات | ✅ نعم |
| **POST** | إنشاء جديد | ❌ لا |
| **PUT** | استبدال كامل | ✅ نعم |
| **PATCH** | تحديث جزئي | ❌ لا |
| **DELETE** | حذف | ✅ نعم |

#### **Status Codes القياسية**

```
✅ Success:
   200 OK           - قراءة ناجحة
   201 Created      - إنشاء ناجح
   204 No Content   - حذف ناجح

⚠️ Client Errors:
   400 Bad Request       - طلب خاطئ
   401 Unauthorized      - غير مصادق
   403 Forbidden         - ليس لديك صلاحية
   404 Not Found         - غير موجود
   422 Unprocessable     - بيانات غير صالحة
   429 Too Many Requests - تجاوز الحد

❌ Server Errors:
   500 Internal Error    - خطأ في الخادم
   503 Service Unavailable
```

### **2. Response Structure الموحد**

```php
// app/Http/Resources/BaseResource.php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

abstract class BaseResource extends JsonResource
{
    /**
     * Wrap response with standard structure
     */
    public function with($request): array
    {
        return [
            'success' => true,
            'timestamp' => now()->toIso8601String(),
        ];
    }
}
```

#### **Success Response**

```json
{
  "success": true,
  "message": "تم الحصول على البيانات بنجاح",
  "data": {
    "id": 123,
    "name": "فستان أنيق",
    "price": 299.99,
    "currency": "SAR"
  },
  "timestamp": "2025-10-19T10:00:00Z"
}
```

#### **Success with Pagination**

```json
{
  "success": true,
  "message": "تم الحصول على المنتجات بنجاح",
  "data": [
    { "id": 1, "name": "منتج 1" },
    { "id": 2, "name": "منتج 2" }
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
    "first": "https://api.zahraah.com/v1/products?page=1",
    "last": "https://api.zahraah.com/v1/products?page=10",
    "prev": null,
    "next": "https://api.zahraah.com/v1/products?page=2"
  },
  "timestamp": "2025-10-19T10:00:00Z"
}
```

#### **Error Response**

```json
{
  "success": false,
  "message": "فشل في معالجة الطلب",
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

### **3. API Resources**

```php
// Product Resource - Transform data
class ProductResource extends BaseResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
            'images' => ImageResource::collection($this->whenLoaded('images')),
            'category' => new CategoryResource($this->whenLoaded('category')),
            // ... other fields
        ];
    }
}
```

---

## **الأداء والتحسين | Performance & Optimization**

### **1. Caching Strategy**

```php
// Caching with tags
public function getProducts(array $filters = [])
{
    $cacheKey = 'products:' . md5(json_encode($filters));
    
    return Cache::tags(['products'])
        ->remember($cacheKey, now()->addHours(2), function () use ($filters) {
            return Product::with(['category', 'images'])
                ->filter($filters)
                ->paginate(20);
        });
}

// Clear cache
Cache::tags(['products'])->flush();
```

### **2. Database Optimization**

#### **Eager Loading**

```php
// ❌ N+1 Problem
$products = Product::all();
foreach ($products as $product) {
    echo $product->category->name; // N queries!
}

// ✅ Eager Loading
$products = Product::with('category')->get();
foreach ($products as $product) {
    echo $product->category->name; // 2 queries only!
}
```

#### **Indexes**

```php
// Refer to Database plan for full schema
// database/migrations/create_products_table.php
Schema::create('products', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->foreignId('category_id')->constrained();
    $table->decimal('price', 10, 2);
    $table->boolean('is_active')->default(true);
    // ... other columns - see Database plan
    $table->timestamps();
    
    // Key indexes only
    $table->index('category_id');
    $table->index('is_active');
});
```

### **3. Response Optimization**

```php
// Select only needed fields
public function index(Request $request)
{
    $products = Product::select(['id', 'name', 'price', 'category_id'])
        ->with('category:id,name')
        ->paginate(20);
    
    return ProductResource::collection($products);
}
```

---

## **الأمان | Security**

### **1. Rate Limiting**

```php
// app/Providers/RouteServiceProvider.php
protected function configureRateLimiting()
{
    RateLimiter::for('api', function (Request $request) {
        return $request->user()
            ? Limit::perMinute(60)->by($request->user()->id)
            : Limit::perMinute(20)->by($request->ip());
    });
    
    RateLimiter::for('auth', function (Request $request) {
        return Limit::perMinute(5)->by($request->ip());
    });
}

// routes/api.php
Route::middleware(['throttle:auth'])->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
});

Route::middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    // Protected routes
});
```

### **2. CORS Configuration**

```php
// config/cors.php - Key settings
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_origins' => [
        'https://app.zahraah.com',
        'https://admin.zahraah.com',
    ],
    'supports_credentials' => true,
];
```

### **3. Input Validation**

```php
// Form Request validation
class StoreProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->hasPermission('products:write');
    }
    
    public function rules(): array
    {
        return [
            'name' => 'required|string|max:255',
            'price' => 'required|numeric|min:0',
            'category_id' => 'required|exists:categories,id',
            'images.*' => 'image|mimes:jpeg,png,jpg|max:2048',
        ];
    }
    
    public function messages(): array
    {
        return [
            'name.required' => 'اسم المنتج مطلوب',
            'price.min' => 'السعر يجب أن يكون أكبر من صفر',
        ];
    }
}
```

---

## **الاختبارات | Testing**

### **1. Feature Tests**

```php
// Test authenticated access
public function test_user_can_list_products(): void
{
    Sanctum::actingAs(User::factory()->create());
    Product::factory()->count(5)->create();
    
    $response = $this->getJson('/api/v1/products');
    
    $response->assertStatus(200)
        ->assertJsonStructure(['success', 'data', 'meta']);
}

// Test authorization
public function test_guest_cannot_create_product(): void
{
    $response = $this->postJson('/api/v1/products', ['name' => 'Test']);
    $response->assertStatus(401);
}
```

### **2. Unit Tests**

```php
// Test role assignment
public function test_user_has_role(): void
{
    $user = User::factory()->create();
    $user->assignRole('admin');
    
    $this->assertTrue($user->hasRole('admin'));
}
```

---

## **المراقبة | Monitoring**

### **1. Laravel Telescope**

```bash
composer require laravel/telescope --dev
php artisan telescope:install
php artisan migrate
```

```php
// config/telescope.php - Enable in development only
'enabled' => env('TELESCOPE_ENABLED', false),
'watchers' => [
    QueryWatcher::class => ['slow' => 100],  // Log slow queries >100ms
    // ... other watchers
],
```

### **2. Logging**

```php
// config/logging.php - API channel
'channels' => [
    'api' => [
        'driver' => 'daily',
        'path' => storage_path('logs/api.log'),
        'days' => 14,
    ],
],

// Usage
Log::channel('api')->info('Product created', ['id' => $product->id]);
```

---

## **الإطلاق | Deployment**

### **1. Checklist قبل الإطلاق**

#### **Security:**
- [ ] APP_DEBUG=false في .env
- [ ] تم تغيير APP_KEY
- [ ] CORS محدد بدقة
- [ ] Rate limiting مفعل
- [ ] SSL/TLS مثبت

#### **Performance:**
- [ ] Caching مفعل
- [ ] Queue workers يعملون
- [ ] Database indexes محسنة
- [ ] Assets مضغوطة

#### **Testing:**
- [ ] جميع الاختبارات تمر
- [ ] Load testing منفذ
- [ ] Security scan نظيف

#### **Monitoring:**
- [ ] Telescope متاح للمراقبة
- [ ] Error reporting مفعل
- [ ] Logs تكتب بشكل صحيح

### **2. Environment Variables**

```bash
# .env.production - Key settings
APP_ENV=production
APP_DEBUG=false
APP_URL=https://api.zahraah.com

DB_CONNECTION=mysql
DB_DATABASE=zahraah_prod

CACHE_DRIVER=redis
QUEUE_CONNECTION=redis

SANCTUM_STATEFUL_DOMAINS=app.zahraah.com,admin.zahraah.com
```

---

## **المراجع السريعة | Quick Reference**

### **Sanctum Commands**

```php
// Create token
$token = $user->createToken('app', ['products:read'])->plainTextToken;

// Revoke current token
$request->user()->currentAccessToken()->delete();

// Check ability
$request->user()->tokenCan('products:read');
```

### **Common Queries**

```php
Product::paginate(20);                                      // Pagination
Product::where('name', 'like', "%{$search}%")->get();     // Search
Product::where('category_id', $id)->get();                 // Filter
Product::orderBy('price', 'desc')->get();                  // Sort
Product::with(['category', 'images'])->get();              // Eager load
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
