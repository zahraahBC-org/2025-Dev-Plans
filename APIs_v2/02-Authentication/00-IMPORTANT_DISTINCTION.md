# ⚠️ تمييز حرج: العملاء مقابل الإداريين | Critical Distinction: Customers vs Admin Users
**الأهمية | Importance**: 🔴 حرج جداً | Critical

---

## **القاعدة الأساسية | The Golden Rule**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  العملاء ≠ الإداريون                                            │
│  Customers ≠ Admin Users                                        │
│                                                                  │
│  ⚠️ لديهم احتياجات مختلفة تماماً للمصادقة والتخويل            │
│  ⚠️ They have completely different authentication needs         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## **نوعان من المستخدمين | Two User Types**

### **العملاء | Customers (End Users)**

**الوصف | Description:**

- مستخدمو التطبيق النهائيون
- المتسوقون في تطبيق التجارة الإلكترونية
- مستخدمو تطبيق Mobile أو Web

**المصادقة | Authentication:**

- **Sanctum فقط** للمصادقة
- **Token-based** authentication
- **لا يحتاجون** نظام Roles
- **لا يحتاجون** نظام Permissions

**التحكم بالوصول | Access Control:**

- **Ownership-based** - يمكنهم الوصول لمواردهم فقط
- **Policy-based** - التحقق من ملكية المورد
- مثال: يمكن للعميل رؤية طلباته فقط، لا يمكنه رؤية طلبات الآخرين

**مثال الـAPI Response:**

```json
{
  "user": {
    "id": 123,
    "name": "أحمد محمد",
    "email": "ahmed@example.com",
    "phone": "+966501234567"
  },
  "token": "1|abc123xyz..."
}

// ⚠️ لاحظ: لا توجد roles أو permissions
```

**Routes (API):**

```
GET  /api/v1/products              ← عام، لا يحتاج authentication
POST /api/v1/auth/register         ← تسجيل عميل جديد
POST /api/v1/auth/login            ← تسجيل دخول العميل

GET  /api/v1/my-orders             ← طلبات العميل فقط (auth required)
GET  /api/v1/my-profile            ← معلومات العميل (auth required)
POST /api/v1/cart                  ← سلة العميل (auth required)
```

**⚠️ ملاحظة:**
العملاء **يستخدمون APIs فقط** (Stateless, Token-based)

---

### **مستخدمو لوحة التحكم | Admin Panel Users**

**الوصف | Description:**

- الموظفون والإداريون
- فريق الدعم الفني
- المشرفون والمديرون
- أي شخص يدير النظام من خلال لوحة التحكم

**المصادقة | Authentication:**

- **Sanctum** للمصادقة
- **RBAC System** - نظام الأدوار والصلاحيات
- **Roles**: admin, support, manager, moderator
- **Permissions**: products:*, orders:*, users:*

**التحكم بالوصول | Access Control:**

- **Permission-based** - حسب الصلاحيات المعطاة
- **Role-based** - حسب الدور الوظيفي
- مثال: مستخدم Support يمكنه رؤية وتعديل جميع الطلبات (حسب صلاحياته)

**مثال الـAPI Response:**

```json
{
  "user": {
    "id": 456,
    "name": "محمد أحمد",
    "email": "mohamed@company.com",
    "roles": ["support", "moderator"],           // ✅ لديه أدوار
    "permissions": [                             // ✅ لديه صلاحيات
      "orders:read",
      "orders:update",
      "users:read",
      "products:update"
    ]
  },
  "token": "2|xyz789abc..."
}
```

**Routes (Web - NOT API):**

```
GET  /admin/login                  ← صفحة تسجيل الدخول
POST /admin/login                  ← تسجيل دخول إداري

GET  /admin/dashboard              ← لوحة التحكم الرئيسية
GET  /admin/orders                 ← جميع الطلبات (permission: orders:read)
POST /admin/orders/{id}/update     ← تحديث طلب (permission: orders:update)
GET  /admin/users                  ← جميع المستخدمين (permission: users:read)
POST /admin/products               ← إضافة منتج (permission: products:write)
```

**⚠️ ملاحظة مهمة:**مستخدمو لوحة التحكم **لا يستخدمون APIs مباشرة**:

- يستخدمون Traditional Web (Blade/Inertia/Livewire)
- Session-based authentication
- يشاركون نفس Models و Services مع الـAPIs
- **لكن لهم Controllers منفصلة** (`Admin\*` ليس `API\*`)

---

## **البنية التقنية | Technical Architecture**

### **️ Important: Separate Tables & Controllers**

```
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  📱 Customer App          🖥️ Admin Panel                       │
│  (Mobile/SPA)             (Web Dashboard)                       │
│  │                        │                                     │
│  ├─ API Controllers       ├─ Admin Controllers                 │
│  │  (Stateless)           │  (Stateful - Sessions)             │
│  │                        │                                     │
│  ├─ Sanctum Auth          ├─ Session Auth + RBAC               │
│  │  (Token-based)         │  (Session-based)                   │
│  │                        │                                     │
│  ├─ customers table       ├─ admin_users table                 │
│  │                        │  + roles/permissions tables        │
│  │                        │                                     │
│  └───────────┬────────────┘                                     │
│              │                                                  │
│              ├─ Shared: Models, Services, Business Logic       │
│              │                                                  │
│              └─ Database: products, orders, etc.               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### **Database Schema:**

```sql
-- Refer to Database plan for full schema
-- ✅ جدول منفصل للعملاء | Separate table for customers
CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    -- ... other columns - see Database plan
);

-- ✅ جدول منفصل للإداريين | Separate table for admin users
CREATE TABLE admin_users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    -- ... other columns - see Database plan
);

-- ✅ جداول RBAC للإداريين فقط | RBAC tables for admins only
CREATE TABLE roles (
    id BIGINT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,        -- admin, support, manager
    -- ... other columns - see Database plan
);

CREATE TABLE permissions (
    id BIGINT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,        -- products:read, orders:*
    -- ... other columns - see Database plan
);

CREATE TABLE admin_user_role (
    admin_user_id BIGINT,
    role_id BIGINT,
    PRIMARY KEY (admin_user_id, role_id),
    FOREIGN KEY (admin_user_id) REFERENCES admin_users(id)
);
```

---

### **Models:**

```php
// ✅ Customer Model - API authentication
class Customer extends Authenticatable
{
    use HasApiTokens;
    protected $fillable = ['name', 'email', 'phone', 'password'];
    protected $hidden = ['password'];
  
    public function orders() { return $this->hasMany(Order::class); }
}

// ✅ AdminUser Model - Session + RBAC
class AdminUser extends Authenticatable
{
    use HasRoles;
    protected $fillable = ['name', 'email', 'password', 'is_active'];
    protected $hidden = ['password'];
}
```

---

### **Controllers:**

```php
// ✅ API Controller - للعملاء | For Customers
namespace App\Http\Controllers\API;

class OrderController extends Controller
{
    public function index()
    {
        return auth('sanctum')->user()->orders()->paginate(20);
    }
  
    public function show(Order $order)
    {
        if ($order->customer_id !== auth('sanctum')->id()) {
            return response()->json(['message' => 'غير مصرح'], 403);
        }
        return new OrderResource($order);
    }
}

// ✅ Admin Controller - للإداريين | For Admin Panel
namespace App\Http\Controllers\Admin;

class OrderController extends Controller
{
    public function index()
    {
        abort_unless(auth()->user()->can('orders:read'), 403);
        return view('admin.orders.index', [
            'orders' => Order::with('customer')->paginate(50)
        ]);
    }
}
```

---

### **Authentication Configuration:**

```php
// config/auth.php - Separate guards
'guards' => [
    'web' => ['driver' => 'session', 'provider' => 'admin_users'],
    'sanctum' => ['driver' => 'sanctum', 'provider' => 'customers'],
],

'providers' => [
    'admin_users' => ['driver' => 'eloquent', 'model' => AdminUser::class],
    'customers' => ['driver' => 'eloquent', 'model' => Customer::class],
],
```

---

### **Routes:**

```php
// routes/api.php - للعملاء فقط | For Customers Only
Route::prefix('v1')->group(function () {
  
    // Public routes
    Route::post('/auth/register', [API\AuthController::class, 'register']);
    Route::post('/auth/login', [API\AuthController::class, 'login']);
  
    // Protected routes - Sanctum
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/my-orders', [API\OrderController::class, 'index']);
        Route::get('/my-profile', [API\ProfileController::class, 'show']);
        Route::post('/cart', [API\CartController::class, 'store']);
    });
});

// routes/web.php - للإداريين فقط | For Admin Panel Only
Route::prefix('admin')->group(function () {
  
    // Admin login page
    Route::get('/login', [Admin\AuthController::class, 'showLoginForm'])
        ->name('admin.login');
    Route::post('/login', [Admin\AuthController::class, 'login']);
  
    // Protected admin routes - Session-based + RBAC
    Route::middleware(['auth:web'])->group(function () {
      
        Route::get('/dashboard', [Admin\DashboardController::class, 'index'])
            ->name('admin.dashboard');
      
        // Orders management - requires permission
        Route::middleware('can:orders:read')->group(function () {
            Route::get('/orders', [Admin\OrderController::class, 'index']);
            Route::get('/orders/{order}', [Admin\OrderController::class, 'show']);
        });
      
        Route::middleware('can:orders:update')->group(function () {
            Route::put('/orders/{order}', [Admin\OrderController::class, 'update']);
        });
      
    });
});

---

## **جدول المقارنة السريع | Quick Comparison Table**

| المعيار | العملاء<br>Customers | الإداريون<br>Admin Users |
|---------|---------------------|--------------------------|
| **التطبيق** | Mobile/SPA App | Admin Dashboard (Web) |
| **المصادقة** | Sanctum (Token) ✅ | Session (Web) ✅ |
| **Guard** | `auth:sanctum` | `auth:web` |
| **الجدول** | `customers` | `admin_users` |
| **الموديل** | `Customer` | `AdminUser` |
| **Controllers** | `API\*Controller` | `Admin\*Controller` |
| **Routes File** | `routes/api.php` | `routes/web.php` |
| **Routes Prefix** | `/api/v1/*` | `/admin/*` |
| **Response Type** | JSON (API) | Views (Blade/Inertia) |
| **Roles** | ❌ لا | ✅ نعم |
| **Permissions** | ❌ لا | ✅ نعم |
| **RBAC System** | ❌ لا | ✅ نعم (Spatie/Custom) |
| **Access Control** | Ownership-based | Permission-based |
| **يمكنه رؤية** | موارده فقط | كل الموارد (حسب الصلاحية) |
| **Stateless** | ✅ نعم | ❌ لا (Session-based) |

---

## ️ **أخطاء شائعة | Common Mistakes**

### ** خطأ 1: استخدام نفس الجدول للعملاء والإداريين**

```php
// ❌ خطأ
Schema::create('users', function (Blueprint $table) {
    $table->user_type ENUM('customer', 'admin');  // لا تفعل هذا!
});

// ✅ صحيح - جداول منفصلة
Schema::create('customers', function (Blueprint $table) { ... });
Schema::create('admin_users', function (Blueprint $table) { ... });
```

---

### ** خطأ 2: إعطاء العملاء أدوار**

```php
// ❌ خطأ
$customer = Customer::create([...]);
$customer->assignRole('customer');  // العملاء لا يستخدمون roles!

// ✅ صحيح - العملاء لا يحتاجون roles
$customer = Customer::create([
    'name' => 'أحمد',
    'email' => 'ahmed@example.com',
    // فقط البيانات الأساسية
]);
```

---

### ** خطأ 3: استخدام API authentication للإداريين**

```php
// ❌ خطأ - Admin Panel يستخدم Sessions ليس Tokens
Route::middleware(['auth:sanctum'])->group(function () {
    Route::get('/admin/orders', ...);  // خطأ!
});

// ✅ صحيح - Admin Panel يستخدم Session-based auth
Route::middleware(['auth:web'])->group(function () {
    Route::get('/admin/orders', ...);
});
```

---

### ** خطأ 4: دمج API Controllers مع Admin Controllers**

```php
// ❌ خطأ - Controller واحد للاثنين
class OrderController extends Controller
{
    public function index() {
        // للعملاء أم للإداريين؟ غير واضح!
    }
}

// ✅ صحيح - Controllers منفصلة
namespace App\Http\Controllers\API;
class OrderController extends Controller { ... }  // للعملاء

namespace App\Http\Controllers\Admin;
class OrderController extends Controller { ... }  // للإداريين
```

---

## **الملفات المرجعية | Reference Files**

### **لفهم المصادقة للعملاء:**

- `01_Auth_Strategies.md` - استراتيجيات المصادقة
- `02_JWT_Implementation.md` - تنفيذ JWT/Sanctum

### **لفهم RBAC للإداريين:**

- `03_RBAC_Permissions.md` - نظام الأدوار والصلاحيات (للإداريين فقط)

---

## **Checklist التنفيذ | Implementation Checklist**

### **للعملاء (Customer API):**

- [ ] جدول `customers` منفصل
- [ ] موديل `Customer` مع `HasApiTokens`
- [ ] Sanctum authentication مثبت
- [ ] Authentication guard: `sanctum`
- [ ] API Controllers في `app/Http/Controllers/API/`
- [ ] Customer registration endpoint (`POST /api/v1/auth/register`)
- [ ] Customer login endpoint (`POST /api/v1/auth/login`)
- [ ] Routes في `routes/api.php` مع prefix `/api/v1/*`
- [ ] Policies للتحقق من الملكية
- [ ] API Resources للـJSON responses
- [ ] ❌ **لا** جداول roles/permissions للعملاء
- [ ] ❌ **لا** middleware للصلاحيات في routes العملاء
- [ ] ❌ **لا** session authentication للعملاء

### **للإداريين (Admin Panel):**

- [ ] جدول `admin_users` منفصل
- [ ] موديل `AdminUser` مع `HasRoles`
- [ ] جداول RBAC (roles, permissions, admin_user_role, permission_role)
- [ ] Authentication guard: `web` (Session-based)
- [ ] Admin Controllers في `app/Http/Controllers/Admin/`
- [ ] Admin login page (`GET /admin/login`)
- [ ] Admin login action (`POST /admin/login`)
- [ ] Routes في `routes/web.php` مع prefix `/admin/*`
- [ ] Middleware `auth:web` للإداريين
- [ ] Middleware للتحقق من الصلاحيات (`can:permission`)
- [ ] Seeders للأدوار والصلاحيات الافتراضية
- [ ] Blade views أو Inertia pages
- [ ] ✅ RBAC system كامل (Spatie Permission أو custom)
- [ ] ❌ **لا** API tokens للإداريين (يستخدمون Sessions)

### **المشتركة (Shared):**

- [ ] Models للموارد (Product, Order, etc.)
- [ ] Services للـBusiness Logic
- [ ] Repositories (اختياري)
- [ ] Events & Listeners
- [ ] Jobs & Queues
- [ ] Notifications

---

## **الخلاصة | Conclusion**

```
┌──────────────────────────────────────────────────────────────────┐
│                       المعمارية الصحيحة                       │
│                   The Correct Architecture                       │
│                                                                   │
│  📱 Customers (API)          🖥️ Admin Panel (Web)               │
│  ├─ Table: customers         ├─ Table: admin_users              │
│  ├─ Guard: sanctum           ├─ Guard: web (session)            │
│  ├─ Token-based              ├─ Session-based                   │
│  ├─ Controllers: API/*       ├─ Controllers: Admin/*            │
│  ├─ Routes: api.php          ├─ Routes: web.php                 │
│  ├─ Response: JSON           ├─ Response: Views                 │
│  ├─ ❌ NO RBAC               ├─ ✅ WITH RBAC                    │
│  └─ Ownership-based          └─ Permission-based                │
│                                                                   │
│  ⚠️ جداول منفصلة، Controllers منفصلة، Auth منفصل              │
│  ⚠️ Separate tables, controllers, authentication                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

### **المبادئ الأساسية | Core Principles:**

**1. الفصل الكامل | Complete Separation:**

- جداول منفصلة (`customers` vs `admin_users`)
- Models منفصلة (`Customer` vs `AdminUser`)
- Controllers منفصلة (`API\*` vs `Admin\*`)
- Authentication منفصل (Tokens vs Sessions)
- Routes منفصلة (`api.php` vs `web.php`)

**2. الموارد المشتركة | Shared Resources:**

- Models للبيانات (Product, Order, Category)
- Services للـBusiness Logic
- Database tables للموارد
- Events, Jobs, Notifications

**3. التحكم بالوصول | Access Control:**

- **Customers**: Ownership-based (هل المورد له؟)
- **Admin Users**: Permission-based (هل لديه صلاحية؟)

---

### **القاعدة الذهبية | The Golden Rule:**

```php
// ❌ لا تفعل هذا NEVER:
- جدول users واحد لكلا النوعين
- Controllers مشتركة
- خلط API authentication مع Session authentication
- إعطاء العملاء roles/permissions

// ✅ افعل هذا ALWAYS:
- جداول منفصلة (customers, admin_users)
- Controllers منفصلة (API\*, Admin\*)
- Authentication منفصل (sanctum, web)
- RBAC للإداريين فقط
```

---

### **متى تقرأ هذا الملف؟ | When to Read This?**

⚠️ **اقرأ هذا الملف قبل:**

- بدء التطوير
- تصميم Database Schema
- إنشاء Authentication System
- كتابة Controllers
- تطبيق RBAC System

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
