# الأدوار والصلاحيات — RBAC & Permissions
**النمط | Pattern**: Role-Based Access Control  
**النطاق | Scope**: ⚠️ **لوحة التحكم فقط | Admin Panel Only**

---

## ️ **تنبيه مهم جداً | Critical Notice**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  هذا النظام لمستخدمي لوحة التحكم فقط                        ┃
┃  This System is for Admin Panel Users ONLY                  ┃
┃                                                              ┃
┃  ❌ NOT for customers (end users)                           ┃
┃  ✅ ONLY for admin, support, managers, moderators           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## **الهدف | Objective**

تنفيذ نظام أدوار وصلاحيات فعّال لـ**مستخدمي لوحة التحكم فقط**.

**⚠️ العملاء (Customers) لا يحتاجون هذا النظام:**
- العملاء يستخدمون **Sanctum للمصادقة فقط**
- لا أدوار، لا صلاحيات
- التحكم بالوصول يتم عبر ملكية الموارد (Own resources only)

---

## **ما هو RBAC؟ | What is RBAC?**

```
Role-Based Access Control:
└─ التحكم بالوصول بناءً على الأدوار

Admin User → Role → Permissions → Resources

مثال (لمستخدم لوحة التحكم):
Admin User "محمد" 
  → Role "Support"
    → Permissions ["orders:read", "orders:update"]
      → يمكنه قراءة وتحديث الطلبات

---

⚠️ مثال خاطئ (العملاء لا يستخدمون RBAC):
Customer "أحمد" 
  → ❌ لا يوجد Role
    → ❌ لا توجد Permissions
      → ✅ يمكنه فقط عرض/تعديل طلباته الخاصة (via ownership)
```

---

## **كيف تتحكم بوصول العملاء؟ | How to Control Customer Access?**

### **بدون RBAC - استخدم Ownership | Without RBAC - Use Ownership**

```php
// ✅ Customer Access Control - Ownership-based
class OrderController extends Controller
{
    public function show(Order $order)
    {
        if ($order->user_id !== auth()->id()) {
            return response()->json(['message' => 'غير مصرح'], 403);
        }
        return new OrderResource($order);
    }
    
    public function index()
    {
        return OrderResource::collection(auth()->user()->orders()->paginate(20));
    }
}

// ✅ Policy Example
class OrderPolicy
{
    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->user_id;
    }
}

// ✅ Routes - Separate Customer & Admin
Route::prefix('v1')->middleware('auth:sanctum')->group(function () {
    Route::get('/my-orders', [OrderController::class, 'myOrders']);
});

Route::prefix('v1/admin')->middleware(['auth:sanctum', 'admin.only'])->group(function () {
    Route::middleware('permission:orders:read')->group(function () {
        Route::get('/orders', [AdminOrderController::class, 'index']);
    });
});
```

---

## **Database Schema**

```php
// Refer to Database plan for full schema
// Roles table (للإداريين فقط | For admin users only)
Schema::create('roles', function (Blueprint $table) {
    $table->id();
    $table->string('name')->unique();           // 'admin', 'support', 'manager'
    $table->string('display_name');             // 'مدير', 'دعم فني', 'مدير عام'
    // ... other columns - see Database plan
    $table->timestamps();
});

// Permissions table
Schema::create('permissions', function (Blueprint $table) {
    $table->id();
    $table->string('name')->unique();           // 'products:read'
    // ... other columns - see Database plan
    $table->timestamps();
});

// Role-User pivot
Schema::create('role_user', function (Blueprint $table) {
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->primary(['role_id', 'user_id']);
});

// Permission-Role pivot
Schema::create('permission_role', function (Blueprint $table) {
    $table->foreignId('permission_id')->constrained()->onDelete('cascade');
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->primary(['permission_id', 'role_id']);
});
```

---

## **Models Setup**

### **Role & Permission Models:**

```php
// Role Model
class Role extends Model
{
    protected $fillable = ['name', 'display_name'];
    
    public function permissions()
    {
        return $this->belongsToMany(Permission::class);
    }
    
    public function givePermissionTo($permission)
    {
        $this->permissions()->syncWithoutDetaching($permission);
        return $this;
    }
}

// Permission Model
class Permission extends Model
{
    protected $fillable = ['name', 'display_name'];
    
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

---

### **User Model (مع RBAC):**

```php
// AdminUser Model with RBAC methods
class AdminUser extends Authenticatable
{
    use HasRoles;  // Spatie package or custom
    
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
    
    public function assignRole($role)
    {
        $this->roles()->syncWithoutDetaching($role);
        return $this;
    }
    
    public function hasRole(string $role): bool
    {
        return $this->roles()->where('name', $role)->exists();
    }
    
    public function hasPermission(string $permission): bool
    {
        return Cache::remember(
            "user:{$this->id}:perm:{$permission}",
            3600,
            fn() => $this->roles()->whereHas('permissions', 
                fn($q) => $q->where('name', $permission)
            )->exists()
        );
    }
}

// ⚠️ Note: For full implementation, consider using Spatie Laravel Permission package
```

---

## **الأدوار النموذجية | Standard Roles**

### **️ للوحة التحكم فقط | For Admin Panel Only:**

```php
// database/seeders/AdminRoleSeeder.php

class AdminRoleSeeder extends Seeder
{
    public function run(): void
    {
        // ⚠️ هذه الأدوار للإداريين فقط - العملاء لا يحتاجون أدوار
        // These roles are for admin users only - customers don't need roles
        
        $roles = [
            [
                'name' => 'admin',
                'display_name' => 'مدير النظام',
                'description' => 'صلاحيات كاملة على النظام',
                'permissions' => [
                    'products:*',
                    'orders:*',
                    'users:*',
                    'reports:*',
                    'settings:*',
                ],
            ],
            [
                'name' => 'manager',
                'display_name' => 'مدير عام',
                'description' => 'إدارة المنتجات والطلبات',
                'permissions' => [
                    'products:*',
                    'orders:*',
                    'reports:read',
                ],
            ],
            [
                'name' => 'support',
                'display_name' => 'دعم فني',
                'description' => 'مساعدة العملاء وإدارة الطلبات',
                'permissions' => [
                    'orders:read',
                    'orders:update',
                    'users:read',
                ],
            ],
            [
                'name' => 'moderator',
                'display_name' => 'مشرف محتوى',
                'description' => 'إدارة المحتوى والمراجعات',
                'permissions' => [
                    'products:read',
                    'products:update',
                    'reviews:*',
                ],
            ],
        ];
        
        foreach ($roles as $roleData) {
            $role = Role::create([
                'name' => $roleData['name'],
                'display_name' => $roleData['display_name'],
            ]);
            
            foreach ($roleData['permissions'] as $permName) {
                $permission = Permission::firstOrCreate([
                    'name' => $permName,
                    'display_name' => $this->getPermissionDisplay($permName),
                ]);
                
                $role->givePermissionTo($permission);
            }
        }
    }
    
    private function getPermissionDisplay(string $name): string
    {
        $map = [
            'products:read' => 'قراءة المنتجات',
            'products:write' => 'إدارة المنتجات',
            'products:*' => 'صلاحيات كاملة للمنتجات',
            'orders:read' => 'قراءة الطلبات',
            'orders:write' => 'إنشاء الطلبات',
            'orders:update' => 'تحديث الطلبات',
            'orders:*' => 'صلاحيات كاملة للطلبات',
        ];
        
        return $map[$name] ?? $name;
    }
}
```

---

## **Middleware للتحقق من الصلاحيات**

```php
// app/Http/Middleware/CheckPermission.php
namespace App\Http\Middleware;

use Closure;

class CheckPermission
{
    public function handle($request, Closure $next, string $permission)
    {
        if (!$request->user()) {
            return response()->json([
                'success' => false,
                'message' => 'غير مصادق',
            ], 401);
        }
        
        if (!$request->user()->hasPermission($permission)) {
            return response()->json([
                'success' => false,
                'message' => 'ليس لديك صلاحية للوصول',
                'error_code' => 'FORBIDDEN',
            ], 403);
        }
        
        return $next($request);
    }
}

// app/Http/Kernel.php
protected $middlewareAliases = [
    'permission' => \App\Http\Middleware\CheckPermission::class,
    'role' => \App\Http\Middleware\CheckRole::class,
];
```

---

## **استخدام Middleware**

```php
// routes/api.php

Route::middleware(['auth:sanctum'])->group(function () {
    
    // يتطلب صلاحية محددة
    Route::middleware('permission:products.write')->group(function () {
        Route::post('/products', [ProductController::class, 'store']);
        Route::put('/products/{id}', [ProductController::class, 'update']);
        Route::delete('/products/{id}', [ProductController::class, 'destroy']);
    });
    
    // يتطلب دور محدد
    Route::middleware('role:admin')->group(function () {
        Route::get('/admin/dashboard', [AdminController::class, 'dashboard']);
    });
    
    // يتطلب أحد الأدوار
    Route::middleware('role:admin,support')->group(function () {
        Route::get('/orders', [OrderController::class, 'index']);
    });
});
```

---

## **Laravel Policies (بديل/إضافي)**

### **إنشاء Policy:**

```bash
php artisan make:policy ProductPolicy --model=Product
```

```php
// Policy example
class ProductPolicy
{
    public function create(User $user): bool
    {
        return $user->hasPermission('products:write');
    }
    
    public function update(User $user, Product $product): bool
    {
        return $user->hasPermission('products:write');
    }
}

// Register in AuthServiceProvider
protected $policies = [Product::class => ProductPolicy::class];

// Use in Controller
$this->authorize('create', Product::class);
```

---

## **تسمية الصلاحيات | Permission Naming**

### **النمط الموصى به:**

**Format:** `resource:action`

**DO - أمثلة صحيحة:**
- `products:read`
- `products:write`
- `products:delete`
- `products:*` (كل الصلاحيات)
- `orders:read`
- `orders:write`
- `users:manage`

**DON'T - أسماء غير واضحة:**
- `read_products`
- `canEditProducts`
- `product_access`

---

### **مجموعات الصلاحيات:**

```php
const PERMISSION_GROUPS = [
    'products' => [
        'products:read',
        'products:write',
        'products:delete',
        'products:*',
    ],
    'orders' => [
        'orders:read',
        'orders:write',
        'orders:update',
        'orders:cancel',
        'orders:*',
    ],
    'users' => [
        'users:read',
        'users:write',
        'users:delete',
        'users:*',
    ],
];
```

---

## **Middleware للأدوار**

```php
// app/Http/Middleware/CheckRole.php
namespace App\Http\Middleware;

use Closure;

class CheckRole
{
    public function handle($request, Closure $next, ...$roles)
    {
        if (!$request->user()) {
            return response()->json([
                'success' => false,
                'message' => 'غير مصادق',
            ], 401);
        }
        
        if (!$request->user()->hasAnyRole($roles)) {
            return response()->json([
                'success' => false,
                'message' => 'ليس لديك الدور المطلوب',
                'error_code' => 'INSUFFICIENT_ROLE',
            ], 403);
        }
        
        return $next($request);
    }
}
```

---

## **أمثلة عملية | Practical Examples**

### **مثال 1: صلاحيات بسيطة (للإداريين فقط)**

```php
// ✅ Assign role to admin user
$adminUser = User::find(1);
$adminUser->assignRole('support');

// Check role
if ($adminUser->hasRole('admin')) {
    // Admin user has admin role
}

// Check permission
if ($adminUser->hasPermission('products:write')) {
    // Admin user can write products
}

// ❌ WRONG - Don't assign roles to customers
$customer = User::find(2);
// $customer->assignRole('customer'); // ❌ NO! Customers don't have roles
```

---

### **مثال 2: صلاحيات متقدمة (للإداريين فقط)**

```php
// ✅ Multiple roles for admin users
$adminUser->assignRole(['support', 'moderator']);

// Check any role
if ($adminUser->hasAnyRole(['admin', 'support'])) {
    // Admin user has at least one of these roles
}

// Check all roles
if ($adminUser->hasAllRoles(['support', 'moderator'])) {
    // Admin user has both roles
}

// Give permission directly (bypass role)
$adminUser->givePermissionTo('special:feature');

// ⚠️ Reminder: Customers don't use this system at all
// They authenticate with Sanctum and access only their own resources
```

---

### **مثال 3: الحماية في Routes**

```php
// Single permission
Route::middleware(['permission:products.write'])
    ->post('/products', [ProductController::class, 'store']);

// Single role
Route::middleware(['role:admin'])
    ->get('/admin/dashboard', [AdminController::class, 'index']);

// Multiple roles (OR)
Route::middleware(['role:admin,support'])
    ->get('/orders', [OrderController::class, 'index']);

// Multiple permissions (AND)
Route::middleware([
    'permission:orders.read',
    'permission:orders.export',
])->get('/orders/export', [OrderController::class, 'export']);
```

---

## **Testing RBAC**

```php
namespace Tests\Feature;

use App\Models\Role;
use App\Models\User;
use Tests\TestCase;

class RBACTest extends TestCase
{
    public function test_admin_can_access_protected_route(): void
    {
        $admin = User::factory()->create();
        $admin->assignRole('admin');
        
        $response = $this->actingAs($admin, 'sanctum')
            ->getJson('/api/v1/admin/dashboard');
        
        $response->assertStatus(200);
    }
    
    public function test_customer_cannot_access_admin_route(): void
    {
        $customer = User::factory()->create();
        $customer->assignRole('customer');
        
        $response = $this->actingAs($customer, 'sanctum')
            ->getJson('/api/v1/admin/dashboard');
        
        $response->assertStatus(403)
            ->assertJson([
                'success' => false,
                'error_code' => 'INSUFFICIENT_ROLE',
            ]);
    }
    
    public function test_user_with_permission_can_create_product(): void
    {
        $user = User::factory()->create();
        $role = Role::factory()->create();
        $role->givePermissionTo('products:write');
        $user->assignRole($role);
        
        $response = $this->actingAs($user, 'sanctum')
            ->postJson('/api/v1/products', [
                'name' => 'Test Product',
                'price' => 99.99,
            ]);
        
        $response->assertStatus(201);
    }
}
```

---

## **Performance Optimization**

### **Caching Permissions:**

```php
// في User Model
public function hasPermission(string $permission): bool
{
    return Cache::tags(['permissions', "user:{$this->id}"])
        ->remember(
            "user:{$this->id}:perm:{$permission}",
            3600,
            fn() => $this->roles()
                ->whereHas('permissions', fn($q) => $q->where('name', $permission))
                ->exists()
        );
}

// Clear cache عند تغيير الأدوار
public function assignRole($role): self
{
    $this->roles()->syncWithoutDetaching($role);
    Cache::tags(["user:{$this->id}"])->flush();
    return $this;
}
```

---

### **Eager Loading:**

```php
// Load roles with user
$user = User::with('roles.permissions')->find($id);

// In middleware
$user->load('roles.permissions');
```

---

## **Checklist RBAC**

### **Database:**
- [ ] جداول roles, permissions
- [ ] جداول pivot (role_user, permission_role)
- [ ] Indexes للأداء

### **Models:**
- [ ] Role model كامل
- [ ] Permission model
- [ ] User مع RBAC methods
- [ ] Relationships صحيحة

### **Seeders:**
- [ ] Default roles created
- [ ] Default permissions
- [ ] Admin user with admin role

### **Middleware:**
- [ ] CheckPermission middleware
- [ ] CheckRole middleware
- [ ] مسجلة في Kernel

### **Testing:**
- [ ] Role assignment tests
- [ ] Permission check tests
- [ ] Middleware tests
- [ ] Policy tests

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
