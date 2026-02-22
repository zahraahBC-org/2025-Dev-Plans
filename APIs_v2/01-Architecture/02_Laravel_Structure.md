# هيكل Laravel للـAPIs — Laravel Structure for APIs

---

## **الهدف | Objective**

تحديد الهيكل التنظيمي المثالي لمشروع Laravel APIs بناءً على أفضل الممارسات.

---

## **الهيكل الموصى به | Recommended Structure**

```
app/
├── Console/
│   └── Commands/              # Artisan commands
│
├── Exceptions/
│   └── Handler.php            # Global exception handling
│
├── Http/
│   ├── Controllers/
│   │   └── API/              # API controllers namespace
│   │       ├── V1/           # Version 1 APIs
│   │       │   ├── AuthController.php
│   │       │   ├── ProductController.php
│   │       │   ├── OrderController.php
│   │       │   └── ...
│   │       └── V2/           # Version 2 (future)
│   │
│   ├── Middleware/
│   │   ├── AuthenticateAPI.php
│   │   ├── CheckPermission.php
│   │   ├── StandardizeResponse.php
│   │   └── SecurityHeaders.php
│   │
│   ├── Requests/
│   │   └── API/
│   │       ├── LoginRequest.php
│   │       ├── StoreProductRequest.php
│   │       ├── UpdateProductRequest.php
│   │       └── ...
│   │
│   └── Resources/
│       └── API/
│           ├── ProductResource.php
│           ├── ProductCollection.php
│           ├── OrderResource.php
│           └── ...
│
├── Models/
│   ├── Product.php
│   ├── Order.php
│   ├── User.php
│   └── ...
│
├── Services/                  # Business logic layer
│   ├── ProductService.php
│   ├── OrderService.php
│   ├── AuthService.php
│   └── ...
│
├── Repositories/              # Data access layer
│   ├── ProductRepository.php
│   ├── OrderRepository.php
│   └── ...
│
├── Observers/                 # Model observers
│   ├── ProductObserver.php
│   └── OrderObserver.php
│
└── Providers/
    ├── AppServiceProvider.php
    ├── AuthServiceProvider.php
    └── RouteServiceProvider.php

config/
├── api.php                    # API configurations
├── auth.php
├── cors.php
├── sanctum.php
└── ...

database/
├── migrations/
├── seeders/
└── factories/

routes/
├── api.php                    # API routes (v1, v2, ...)
└── web.php                    # Web routes (if any)

tests/
├── Feature/
│   └── API/
│       ├── ProductTest.php
│       ├── OrderTest.php
│       └── ...
└── Unit/
    └── Services/
        ├── ProductServiceTest.php
        └── ...

resources/
└── lang/
    ├── ar/                    # Arabic translations
    │   ├── validation.php
    │   ├── auth.php
    │   └── messages.php
    └── en/                    # English (fallback)
```

---

## **التنظيم حسب الطبقات | Layer Organization**

### **1. HTTP Layer | طبقة HTTP**

#### **Controllers**

```php
// Controller Example
namespace App\Http\Controllers\API\V1;

class ProductController extends Controller
{
    public function __construct(private ProductService $service) {}
    
    public function index()
    {
        return ProductResource::collection($this->service->getProducts(request()->all()));
    }
    
    public function store(StoreProductRequest $request)
    {
        $product = $this->service->createProduct($request->validated());
        return (new ProductResource($product))->setStatusCode(201);
    }
    
    public function show(int $id)
    {
        return new ProductResource($this->service->getProduct($id));
    }
}
```

---

#### **Form Requests**

```php
// Form Request Example
class StoreProductRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'price' => ['required', 'numeric', 'min:0'],
            'category_id' => ['required', 'exists:categories,id'],
        ];
    }
    
    public function messages(): array
    {
        return ['name.required' => 'اسم المنتج مطلوب'];
    }
}
```

---

#### **API Resources**

```php
// Resource Example
class ProductResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'price' => (float) $this->price,
            'category' => new CategoryResource($this->whenLoaded('category')),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}
```

---

### **2. Business Logic Layer | طبقة منطق الأعمال**

#### **Services**

```php
// Service Layer Example
class ProductService
{
    public function __construct(private ProductRepository $repository) {}
    
    public function getProducts(array $filters = []): LengthAwarePaginator
    {
        $cacheKey = 'products:' . md5(json_encode($filters));
        return Cache::tags(['products'])
            ->remember($cacheKey, 3600, fn() => $this->repository->getFiltered($filters));
    }
    
    public function createProduct(array $data): Product
    {
        return DB::transaction(function () use ($data) {
            $product = $this->repository->create($data);
            Cache::tags(['products'])->flush();
            event(new ProductCreated($product));
            return $product;
        });
    }
}
```

---

### **3. Data Access Layer | طبقة الوصول للبيانات**

#### **Repositories**

```php
// Repository Example
class ProductRepository
{
    public function create(array $data): Product
    {
        return Product::create($data);
    }
    
    public function findOrFail(int $id): Product
    {
        return Product::with(['category', 'images'])->findOrFail($id);
    }
    
    public function getFiltered(array $filters = []): LengthAwarePaginator
    {
        return Product::query()
            ->when($filters['category_id'] ?? null, fn($q, $v) => $q->where('category_id', $v))
            ->when($filters['search'] ?? null, fn($q, $v) => $q->where('name', 'like', "%{$v}%"))
            ->with(['category:id,name'])
            ->paginate($filters['per_page'] ?? 20);
    }
}
```

---

## **Service Providers**

### **إعداد Bindings**

```php
// app/Providers/RepositoryServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(
            \App\Repositories\ProductRepository::class,
            \App\Repositories\Eloquent\ProductRepository::class
        );
        
        // More bindings...
    }
}
```

---

## **Routes Organization**

### **API Routes**

```php
// routes/api.php
use Illuminate\Support\Facades\Route;

// Public routes
Route::prefix('v1')->group(function () {
    // Auth
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
    
    // Public endpoints
    Route::get('/products', [ProductController::class, 'index']);
    Route::get('/products/{id}', [ProductController::class, 'show']);
});

// Protected routes
Route::prefix('v1')
    ->middleware(['auth:sanctum', 'throttle:api'])
    ->group(function () {
        // Auth
        Route::post('/logout', [AuthController::class, 'logout']);
        Route::get('/me', [AuthController::class, 'me']);
        
        // Products (admin only)
        Route::middleware('permission:products.write')
            ->group(function () {
                Route::post('/products', [ProductController::class, 'store']);
                Route::put('/products/{id}', [ProductController::class, 'update']);
                Route::delete('/products/{id}', [ProductController::class, 'destroy']);
            });
        
        // Orders
        Route::apiResource('orders', OrderController::class);
        
        // Cart
        Route::prefix('cart')->group(function () {
            Route::get('/', [CartController::class, 'index']);
            Route::post('/items', [CartController::class, 'addItem']);
            Route::patch('/items/{id}', [CartController::class, 'updateItem']);
            Route::delete('/items/{id}', [CartController::class, 'removeItem']);
        });
    });
```

---

## **Naming Conventions | قواعد التسمية**

### **Controllers**

**DO:**
```
ProductController
OrderController
UserController
```
*Use singular noun + Controller*

**DON'T:**
```
ProductsController
GetProductController
```
*Avoid plural nouns or verbs*

---

### **Services**

```
✅ Singular noun + Service
   ProductService
   OrderService
   PaymentService

✅ Or action-based for specific services
   EmailNotificationService
   OrderProcessingService
```

---

### **Repositories**

```
✅ Singular noun + Repository
   ProductRepository
   OrderRepository
```

---

### **Resources**

```
✅ Singular + Resource
   ProductResource
   OrderResource

✅ Collection suffix for collections
   ProductCollection
```

---

### **Requests**

```
✅ Action + Noun + Request
   StoreProductRequest
   UpdateProductRequest
   LoginRequest
```

---

## **Models Organization**

### **Basic Model**

```php
// Model Example
class Product extends Model
{
    use HasFactory, SoftDeletes;
    
    protected $fillable = ['name', 'description', 'price', 'category_id', 'stock_quantity'];
    protected $casts = [
        'price' => 'decimal:2',
        'is_available' => 'boolean',
        'created_at' => 'datetime',
    ];
    
    // Relationships
    public function category() { return $this->belongsTo(Category::class); }
    public function images() { return $this->hasMany(ProductImage::class); }
    
    // Scopes
    public function scopeAvailable($query) { return $query->where('is_available', true); }
}
```

---

## **Best Practices**

### **1. التزم بـ PSR Standards**

```php
// ✅ صحيح - PSR-12
namespace App\Http\Controllers\API;

use App\Services\ProductService;
use Illuminate\Http\JsonResponse;

class ProductController extends Controller
{
    public function __construct(
        private ProductService $service
    ) {}
    
    public function index(): JsonResponse
    {
        // Implementation
    }
}
```

---

### **2. استخدم Type Hints**

```php
// ✅ صحيح
public function createProduct(array $data): Product
{
    return Product::create($data);
}

// ❌ خطأ - بدون types
public function createProduct($data)
{
    return Product::create($data);
}
```

---

### **3. استخدم Dependency Injection**

```php
// ✅ صحيح
class ProductController extends Controller
{
    public function __construct(
        private ProductService $service,
        private CacheService $cache
    ) {}
}

// ❌ خطأ - استدعاء مباشر
class ProductController extends Controller
{
    public function index()
    {
        $service = new ProductService(); // ❌
    }
}
```

---

### **4. فصل Business Logic عن Controllers**

```php
// ✅ صحيح
class ProductController extends Controller
{
    public function store(StoreProductRequest $request)
    {
        // Controller: HTTP handling only
        $product = $this->service->createProduct(
            $request->validated()
        );
        
        return new ProductResource($product);
    }
}

class ProductService
{
    public function createProduct(array $data): Product
    {
        // Service: Business logic
        return DB::transaction(function () use ($data) {
            $product = Product::create($data);
            $this->handleImages($product, $data['images'] ?? []);
            Cache::tags(['products'])->flush();
            return $product;
        });
    }
}

// ❌ خطأ - Business logic في Controller
class ProductController extends Controller
{
    public function store(Request $request)
    {
        // ❌ كل شيء في Controller
        $product = Product::create($request->all());
        foreach ($request->images as $image) {
            // Complex logic here...
        }
        Cache::forget('products');
        // ...
    }
}
```

---

## **Checklist الهيكل | Structure Checklist**

### **التنظيم:**
- [ ] Controllers في `API/` namespace
- [ ] Versioning واضح (V1/, V2/)
- [ ] Services layer منفصل
- [ ] Repositories layer منفصل
- [ ] Resources منظمة
- [ ] Requests منظمة

### **التسمية:**
- [ ] Controllers: SingularController
- [ ] Services: SingularService
- [ ] Repositories: SingularRepository
- [ ] Resources: SingularResource
- [ ] Requests: ActionNounRequest

### **Best Practices:**
- [ ] Type hints مستخدم
- [ ] Dependency injection مطبق
- [ ] Business logic في Services
- [ ] Data access في Repositories
- [ ] PSR-12 compliance

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
