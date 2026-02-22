# دليل تكامل Shofy — Shofy Integration Guide
**النسخة | Version**: 2.0  
**التطبيق | Application**: زهراء (Zahraah)  
**المنصة | Platform**: Botble Shofy E-commerce  
**Laravel**: 12

---

## 🎯 **الغرض من هذا الدليل | Purpose**

هذا الدليل هو **جسر الربط** بين:
- ✅ **APIs الموجودة** في Shofy/Botble (الأساس الحالي)
- ✅ **المعايير العالمية** في خطة APIs v2 (الهدف المنشود)

### **الاستخدامات الرئيسية:**
1. 📊 **Audit**: تقييم APIs الموجودة مقابل المعايير
2. 🔄 **Improvement**: خطة تحسين تدريجية
3. ➕ **Extension**: إضافة endpoints جديدة بشكل صحيح
4. 📚 **Reference**: مرجع للمعايير العالمية

---

## 📋 **نظرة على Shofy APIs | Shofy APIs Overview**

### **ما يوفره Shofy حالياً:**

بناءً على [التوثيق الرسمي](https://shofy.botble.com/docs/):

```
✅ Authentication & Authorization
├── Register, Login, Logout
├── Social Login (Google, Facebook, Apple, Twitter)
├── Password Reset & Email Verification
└── Profile Management

✅ Product Management
├── List Products (with filters)
├── Product Details
├── Categories & Brands
├── Product Reviews
├── Related & Cross-sale Products
└── Product Variations

✅ Shopping Experience
├── Cart Management
├── Wishlist
├── Compare Products
├── Checkout Process
└── Coupons

✅ Order Management
├── Order Creation
├── Order History
├── Order Tracking
├── Order Returns
├── Invoice Download
└── Payment Proof Upload

✅ User Features
├── Address Management
├── Notifications
├── Device Tokens (Push)
├── Downloads (Digital Products)
└── User Settings

✅ Content & Support
├── Blog Posts
├── Pages
├── Flash Sales
├── Sliders
└── FAQs
```

---

## 🔍 **Audit Matrix | مصفوفة التقييم**

### **تقييم APIs الموجودة مقابل المعايير العالمية:**

| المعيار | Shofy الحالي | المعيار المطلوب | الحالة | الأولوية |
|---------|--------------|-----------------|--------|----------|
| **REST Principles** | ✅ متبع جزئياً | REST كامل | 🟡 جيد | متوسطة |
| **Response Structure** | ⚠️ غير موحد | موحد 100% | 🟠 يحتاج تحسين | عالية |
| **Error Handling** | ⚠️ أخطاء إنجليزية | عربي + موحد | 🔴 مهم جداً | عالية |
| **Authentication** | ✅ Sanctum | ✅ Sanctum | 🟢 ممتاز | منخفضة |
| **Pagination** | ✅ موجود | Cursor/Offset | 🟡 جيد | متوسطة |
| **Filtering & Search** | ✅ موجود | محسّن | 🟡 جيد | متوسطة |
| **Rate Limiting** | ❌ غير موثق | مطبق ومحدد | 🔴 ناقص | عالية |
| **CORS** | ⚠️ غير واضح | محدد بدقة | 🟠 يحتاج تحسين | متوسطة |
| **Caching** | ❓ غير موثق | استراتيجية واضحة | 🟠 يحتاج تحسين | متوسطة |
| **Validation** | ✅ موجود | رسائل عربية | 🟠 يحتاج تحسين | عالية |
| **Documentation** | ✅ ممتاز | ✅ ممتاز | 🟢 ممتاز | منخفضة |
| **Testing** | ❓ غير معروف | Strategy كاملة | 🔴 ناقص | عالية |
| **Monitoring** | ❓ غير معروف | Telescope + Logs | 🔴 ناقص | متوسطة |
| **Security Headers** | ❓ غير معروف | كاملة | 🔴 ناقص | عالية |

### **مفتاح الحالة:**
- 🟢 **ممتاز**: يطابق المعايير
- 🟡 **جيد**: يعمل لكن يحتاج تحسينات بسيطة
- 🟠 **يحتاج تحسين**: فجوات واضحة
- 🔴 **ناقص/مهم**: يحتاج عمل فوري

---

## 🎯 **خطة التحسين التدريجية | Improvement Roadmap**

### **المرحلة 1: الأساسيات (أسبوع 1-2)** 🔥

#### **1.1 توحيد الردود (Response Standardization)**

**المشكلة الحالية:**
```json
// Shofy حالياً - غير موحد
{
  "error": false,
  "data": {...},
  "message": null
}

// أحياناً:
{
  "error": true,
  "message": "Error message"
}
```

**الحل المطلوب:**
```json
// Response موحد دائماً
{
  "success": true,
  "message": "تم الحصول على البيانات بنجاح",
  "data": {...},
  "timestamp": "2025-10-19T10:00:00Z"
}

// للأخطاء
{
  "success": false,
  "message": "فشل في معالجة الطلب",
  "errors": {
    "email": ["البريد الإلكتروني مطلوب"]
  },
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-10-19T10:00:00Z"
}
```

**التنفيذ:**
```php
// app/Http/Middleware/StandardizeApiResponse.php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\JsonResponse;

class StandardizeApiResponse
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        if ($response instanceof JsonResponse) {
            $data = $response->getData(true);
            
            // Standardize success responses
            if (!isset($data['success'])) {
                $standardized = [
                    'success' => !($data['error'] ?? false),
                    'message' => $data['message'] ?? null,
                    'data' => $data['data'] ?? $data,
                    'timestamp' => now()->toIso8601String(),
                ];
                
                $response->setData($standardized);
            }
        }
        
        return $response;
    }
}
```

**الأولوية:** 🔥 عالية جداً

---

#### **1.2 رسائل خطأ بالعربية (Arabic Error Messages)**

**المشكلة:**
```json
{
  "error": true,
  "message": "The email field is required"
}
```

**الحل:**
```php
// resources/lang/ar/validation.php
return [
    'required' => 'حقل :attribute مطلوب',
    'email' => 'يجب أن يكون :attribute بريداً إلكترونياً صالحاً',
    'min' => [
        'string' => 'يجب أن يحتوي :attribute على :min أحرف على الأقل',
    ],
    'confirmed' => 'حقل التأكيد غير مطابق لـ :attribute',
    'unique' => ':attribute موجود مسبقاً',
    
    'attributes' => [
        'email' => 'البريد الإلكتروني',
        'password' => 'كلمة المرور',
        'name' => 'الاسم',
        'phone' => 'رقم الهاتف',
        'address' => 'العنوان',
    ],
];

// config/app.php
'locale' => 'ar',
'fallback_locale' => 'en',
```

**الأولوية:** 🔥 عالية جداً

---

#### **1.3 Rate Limiting واضح**

**التنفيذ:**
```php
// app/Providers/RouteServiceProvider.php
protected function configureRateLimiting()
{
    // للعملاء المسجلين
    RateLimiter::for('api', function (Request $request) {
        return $request->user()
            ? Limit::perMinute(120)->by($request->user()->id)
            : Limit::perMinute(30)->by($request->ip());
    });
    
    // لـ Auth endpoints
    RateLimiter::for('auth', function (Request $request) {
        return Limit::perMinute(5)
            ->by($request->ip())
            ->response(function () {
                return response()->json([
                    'success' => false,
                    'message' => 'تجاوزت الحد المسموح. يرجى المحاولة بعد دقيقة.',
                    'error_code' => 'RATE_LIMIT_EXCEEDED',
                ], 429);
            });
    });
    
    // للعمليات الحساسة
    RateLimiter::for('sensitive', function (Request $request) {
        return Limit::perMinute(10)->by($request->user()->id ?? $request->ip());
    });
}

// routes/api.php - تطبيق
Route::middleware(['throttle:auth'])->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/register', [AuthController::class, 'register']);
});

Route::middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    // Protected routes
});
```

**الأولوية:** 🔥 عالية

---

### **المرحلة 2: الأمان (أسبوع 3)** 🛡️

#### **2.1 CORS محدد بدقة**

```php
// config/cors.php
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    
    'allowed_methods' => ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    
    'allowed_origins' => [
        env('FRONTEND_URL', 'http://localhost:3000'),
        'https://app.zahraah.com',      // Flutter App
        'https://admin.zahraah.com',    // Admin Panel
    ],
    
    'allowed_origins_patterns' => [],
    
    'allowed_headers' => [
        'Content-Type',
        'X-Requested-With',
        'Authorization',
        'Accept',
        'Origin',
        'X-CSRF-TOKEN',
    ],
    
    'exposed_headers' => [
        'X-RateLimit-Limit',
        'X-RateLimit-Remaining',
        'X-RateLimit-Reset',
    ],
    
    'max_age' => 86400,
    
    'supports_credentials' => true,
];
```

**الأولوية:** 🔥 عالية

---

#### **2.2 Security Headers**

```php
// app/Http/Middleware/SecurityHeaders.php
namespace App\Http\Middleware;

use Closure;

class SecurityHeaders
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
        $response->headers->set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
        
        if (app()->environment('production')) {
            $response->headers->set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
        }
        
        return $response;
    }
}

// app/Http/Kernel.php
protected $middleware = [
    // ...
    \App\Http\Middleware\SecurityHeaders::class,
];
```

**الأولوية:** 🔥 عالية

---

### **المرحلة 3: الأداء (أسبوع 4)** ⚡

#### **3.1 استراتيجية Caching واضحة**

```php
// app/Services/ProductService.php
namespace App\Services;

use Botble\Ecommerce\Models\Product;
use Illuminate\Support\Facades\Cache;

class EnhancedProductService
{
    /**
     * Get products with intelligent caching
     */
    public function getProducts(array $filters = [])
    {
        $cacheKey = $this->generateCacheKey('products', $filters);
        
        return Cache::tags(['products', 'ecommerce'])
            ->remember($cacheKey, now()->addHours(2), function () use ($filters) {
                return Product::query()
                    ->with(['category:id,name', 'images'])
                    ->when($filters['category_id'] ?? null, fn($q, $v) => $q->where('category_id', $v))
                    ->when($filters['brand_id'] ?? null, fn($q, $v) => $q->where('brand_id', $v))
                    ->when($filters['search'] ?? null, fn($q, $v) => $q->where('name', 'like', "%{$v}%"))
                    ->when($filters['min_price'] ?? null, fn($q, $v) => $q->where('price', '>=', $v))
                    ->when($filters['max_price'] ?? null, fn($q, $v) => $q->where('price', '<=', $v))
                    ->latest()
                    ->paginate(20);
            });
    }
    
    /**
     * Clear cache when product changes
     */
    public function clearProductCache(): void
    {
        Cache::tags(['products'])->flush();
    }
    
    /**
     * Generate consistent cache key
     */
    private function generateCacheKey(string $prefix, array $params): string
    {
        ksort($params);
        return $prefix . ':' . md5(json_encode($params));
    }
}

// في Model observer
namespace App\Observers;

class ProductObserver
{
    public function saved($product)
    {
        app(EnhancedProductService::class)->clearProductCache();
    }
    
    public function deleted($product)
    {
        app(EnhancedProductService::class)->clearProductCache();
    }
}
```

**الأولوية:** متوسطة

---

#### **3.2 Database Query Optimization**

```php
// إضافة indexes ناقصة
// database/migrations/add_performance_indexes.php
Schema::table('ec_products', function (Blueprint $table) {
    $table->index(['status', 'is_variation']);
    $table->index(['category_id', 'status']);
    $table->index(['brand_id', 'status']);
    $table->index('price');
    $table->index('created_at');
    $table->index(['status', 'created_at']);
});

Schema::table('ec_orders', function (Blueprint $table) {
    $table->index(['user_id', 'status']);
    $table->index(['status', 'created_at']);
});

Schema::table('ec_reviews', function (Blueprint $table) {
    $table->index(['product_id', 'status']);
    $table->index(['user_id', 'status']);
});
```

**الأولوية:** متوسطة-عالية

---

### **المرحلة 4: المراقبة والجودة (أسبوع 5-6)** 📊

#### **4.1 Laravel Telescope Setup**

```bash
composer require laravel/telescope
php artisan telescope:install
php artisan migrate
```

```php
// config/telescope.php
'enabled' => env('TELESCOPE_ENABLED', false),
'path' => 'admin/telescope',

'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => true,
        'slow' => 100, // Log queries > 100ms
    ],
    Watchers\RequestWatcher::class => [
        'enabled' => true,
        'size_limit' => 64,
    ],
    Watchers\CacheWatcher::class => true,
    Watchers\ExceptionWatcher::class => true,
],
```

**الأولوية:** متوسطة

---

#### **4.2 Structured Logging**

```php
// config/logging.php
'channels' => [
    'api' => [
        'driver' => 'daily',
        'path' => storage_path('logs/api.log'),
        'level' => env('LOG_LEVEL', 'info'),
        'days' => 14,
        'formatter' => \Monolog\Formatter\JsonFormatter::class,
    ],
    
    'security' => [
        'driver' => 'daily',
        'path' => storage_path('logs/security.log'),
        'level' => 'warning',
        'days' => 30,
    ],
],

// الاستخدام
use Illuminate\Support\Facades\Log;

Log::channel('api')->info('Product viewed', [
    'product_id' => $product->id,
    'user_id' => auth()->id(),
    'ip' => request()->ip(),
]);

Log::channel('security')->warning('Failed login attempt', [
    'email' => $request->email,
    'ip' => request()->ip(),
]);
```

**الأولوية:** متوسطة

---

## 📚 **إضافة Endpoints جديدة بشكل صحيح**

### **نموذج: إضافة API جديد**

عندما تحتاج إضافة endpoint جديد، اتبع هذا النموذج:

```php
// 1. Request Validation
// app/Http/Requests/API/CustomFeatureRequest.php
namespace App\Http\Requests\API;

use Illuminate\Foundation\Http\FormRequest;

class CustomFeatureRequest extends FormRequest
{
    public function authorize(): bool
    {
        return auth()->check();
    }
    
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'description' => ['required', 'string'],
        ];
    }
    
    public function messages(): array
    {
        return [
            'name.required' => 'الاسم مطلوب',
            'description.required' => 'الوصف مطلوب',
        ];
    }
}

// 2. Service Layer
// app/Services/CustomFeatureService.php
namespace App\Services;

class CustomFeatureService
{
    public function create(array $data)
    {
        // Business logic here
        return CustomFeature::create($data);
    }
}

// 3. Resource (Response)
// app/Http/Resources/CustomFeatureResource.php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class CustomFeatureResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'description' => $this->description,
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
    
    public function with($request): array
    {
        return [
            'success' => true,
            'timestamp' => now()->toIso8601String(),
        ];
    }
}

// 4. Controller
// app/Http/Controllers/API/CustomFeatureController.php
namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Http\Requests\API\CustomFeatureRequest;
use App\Http\Resources\CustomFeatureResource;
use App\Services\CustomFeatureService;

class CustomFeatureController extends Controller
{
    public function __construct(
        private CustomFeatureService $service
    ) {}
    
    public function store(CustomFeatureRequest $request)
    {
        $feature = $this->service->create($request->validated());
        
        return (new CustomFeatureResource($feature))
            ->response()
            ->setStatusCode(201);
    }
}

// 5. Route
// routes/api.php
Route::middleware(['auth:sanctum', 'throttle:api'])->group(function () {
    Route::apiResource('custom-features', CustomFeatureController::class);
});

// 6. Test
// tests/Feature/CustomFeatureTest.php
namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;

class CustomFeatureTest extends TestCase
{
    use RefreshDatabase;
    
    public function test_user_can_create_custom_feature(): void
    {
        Sanctum::actingAs(User::factory()->create());
        
        $response = $this->postJson('/api/v1/custom-features', [
            'name' => 'Test Feature',
            'description' => 'Test Description',
        ]);
        
        $response->assertStatus(201)
            ->assertJsonStructure([
                'success',
                'data' => ['id', 'name', 'description'],
                'timestamp',
            ]);
    }
}
```

---

## ✅ **Checklist للتحسين | Improvement Checklist**

استخدم هذا الـ Checklist لتتبع التحسينات:

### **الأساسيات (Must Have)**
- [ ] توحيد Response structure
- [ ] رسائل خطأ بالعربية
- [ ] Rate Limiting مطبق وموثق
- [ ] CORS محدد بدقة
- [ ] Security Headers مضافة
- [ ] Validation messages بالعربية
- [ ] Error codes موحدة

### **الأمان (Security)**
- [ ] HTTPS فقط في production
- [ ] Sanctum محدث
- [ ] Password hashing آمن (Argon2/Bcrypt)
- [ ] Input sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection

### **الأداء (Performance)**
- [ ] Caching strategy واضحة
- [ ] Database indexes محسّنة
- [ ] Eager loading مطبق
- [ ] N+1 queries محلولة
- [ ] Response compression
- [ ] Query optimization

### **الجودة (Quality)**
- [ ] Tests coverage ≥ 70%
- [ ] PHPStan level 5+
- [ ] Laravel Pint مطبق
- [ ] Telescope مفعّل
- [ ] Structured logging
- [ ] Error tracking

### **التوثيق (Documentation)**
- [ ] API endpoints موثقة
- [ ] Response examples
- [ ] Error codes catalog
- [ ] Postman collection
- [ ] README محدث

---

## 🎯 **الخلاصة | Summary**

### **الأولويات:**

**🔥 فوري (الأسبوعين الأولين):**
1. توحيد Response structure
2. رسائل خطأ بالعربية
3. Rate Limiting
4. CORS
5. Security Headers

**⚡ مهم (الأسبوع 3-4):**
1. Caching strategy
2. Database optimization
3. Query optimization

**📊 تحسينات (الأسبوع 5-6):**
1. Telescope
2. Logging
3. Testing
4. Monitoring

---

## 🔗 **التنقل | Navigation**

[🏠 العودة للرئيسية](../README.md) | [📖 الدليل الرئيسي](00_Master_API_Guide.md)

**المرتبط:**
- 📋 [APIs Audit Checklist](02_APIs_Audit_Checklist.md)
- 🔄 [Improvement Tracking](03_Improvement_Tracking.md)
- 📚 [Standards Reference](../08-Reference/01_Code_Templates.md)

---

**آخر تحديث | Last Updated**: 2025-10-19  
**الحالة | Status**: ✅ جاهز للتطبيق  
**الإصدار | Version**: 2.0 - Shofy Integration

