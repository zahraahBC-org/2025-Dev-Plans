# مرجع سريع — Quick Reference
**الأهمية | Importance**: 🟢 مفيدة

---

## **Artisan Commands**

### **API Development:**

```bash
# Create API controller
php artisan make:controller API/V1/ProductController --api --model=Product

# Create form request
php artisan make:request API/V1/StoreProductRequest
php artisan make:request API/V1/UpdateProductRequest

# Create resource
php artisan make:resource API/V1/ProductResource
php artisan make:resource API/V1/ProductCollection

# Create middleware
php artisan make:middleware CheckApiVersion

# Create service
php artisan make:class Services/ProductService
```

---

### **Database:**

```bash
# Create migration
php artisan make:migration create_products_table
php artisan make:migration add_discount_to_products_table

# Run migrations
php artisan migrate

# Rollback
php artisan migrate:rollback
php artisan migrate:fresh  # Drop all tables & re-run

# Seed
php artisan db:seed
php artisan migrate:fresh --seed
```

---

### **Testing:**

```bash
# Run all tests
php artisan test

# Run specific test
php artisan test --filter=ProductTest

# Run with coverage
php artisan test --coverage

# Create test
php artisan make:test API/ProductTest
php artisan make:test API/ProductTest --unit
```

---

### **Cache:**

```bash
# Clear all caches
php artisan optimize:clear

# Clear specific
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Create cache
php artisan config:cache
php artisan route:cache
```

---

### **Queue:**

```bash
# Run queue worker
php artisan queue:work

# Run specific queue
php artisan queue:work --queue=high,default

# Failed jobs
php artisan queue:failed
php artisan queue:retry all
```

---

## **Eloquent Patterns**

### **Basic CRUD:**

```php
// Create
$product = Product::create([
    'name' => 'Product Name',
    'price' => 99.99,
]);

// Read
$product = Product::find(1);
$product = Product::findOrFail(1);  // 404 if not found
$product = Product::where('slug', $slug)->firstOrFail();

// Update
$product->update(['price' => 89.99]);

// Delete
$product->delete();  // Soft delete
$product->forceDelete();  // Permanent delete

// Restore soft-deleted
$product->restore();
```

---

### **Querying:**

```php
// Where clauses
Product::where('price', '>', 100)->get();
Product::where('status', 'active')
    ->where('stock', '>', 0)
    ->get();

// Or where
Product::where('price', '<', 50)
    ->orWhere('discount_price', '<', 50)
    ->get();

// Where in
Product::whereIn('category_id', [1, 2, 3])->get();

// Where null
Product::whereNull('discount_price')->get();
Product::whereNotNull('discount_price')->get();

// Where date
Product::whereDate('created_at', '2025-10-19')->get();
Product::whereMonth('created_at', 10)->get();

// Where JSON
User::where('settings->notifications', true)->get();
```

---

### **Ordering & Limiting:**

```php
// Order by
Product::orderBy('created_at', 'desc')->get();
Product::latest()->get();  // Same as orderBy('created_at', 'desc')
Product::oldest()->get();

// Multiple orders
Product::orderBy('category_id')
    ->orderBy('price', 'desc')
    ->get();

// Limit
Product::limit(10)->get();
Product::take(10)->get();  // Same

// Offset
Product::offset(20)->limit(10)->get();
```

---

### **Relationships:**

```php
// Eager loading (1 query per relationship)
$products = Product::with(['category', 'images'])->get();

// Nested eager loading
$products = Product::with('category.parent')->get();

// Lazy eager loading
$products->load('reviews');

// Conditional eager loading
$products = Product::with(['reviews' => function ($query) {
    $query->where('rating', '>=', 4);
}])->get();

// Count relationships
$products = Product::withCount('reviews')->get();
$product->reviews_count;  // Access count
```

---

### **Aggregates:**

```php
// Count
$count = Product::count();
$count = Product::where('status', 'active')->count();

// Sum
$total = Order::sum('total');
$total = Order::where('status', 'completed')->sum('total');

// Average
$avg = Product::avg('price');

// Min/Max
$min = Product::min('price');
$max = Product::max('price');
```

---

### **Pagination:**

```php
// Simple pagination
$products = Product::paginate(20);

// Custom per page
$products = Product::paginate($request->get('per_page', 20));

// Simple paginator (only next/prev)
$products = Product::simplePaginate(20);

// Cursor pagination (for large datasets)
$products = Product::cursorPaginate(20);
```

---

## **Sanctum Authentication**

### **Login/Register:**

```php
// Register & create token
$user = User::create([
    'name' => $request->name,
    'email' => $request->email,
    'password' => Hash::make($request->password),
]);

$token = $user->createToken('mobile-app')->plainTextToken;

return response()->json([
    'user' => new UserResource($user),
    'token' => $token,
]);

// Login
if (!Auth::attempt($request->only('email', 'password'))) {
    return response()->json([
        'message' => 'بيانات الدخول غير صحيحة',
    ], 401);
}

$user = Auth::user();
$token = $user->createToken('mobile-app')->plainTextToken;

return response()->json([
    'user' => new UserResource($user),
    'token' => $token,
]);
```

---

### **Token Management:**

```php
// Get current user
$user = $request->user();

// Revoke current token (logout)
$request->user()->currentAccessToken()->delete();

// Revoke all tokens
$user->tokens()->delete();

// Revoke specific token
$user->tokens()->where('id', $tokenId)->delete();

// Get all tokens
$tokens = $user->tokens;

// Token abilities
$token = $user->createToken('admin-token', [
    'products:read',
    'products:write',
    'orders:read',
])->plainTextToken;

// Check ability
if ($request->user()->tokenCan('products:write')) {
    // Has permission
}
```

---

## **Validation Rules Reference**

### **Common Rules:**

```php
$request->validate([
    // Required
    'name' => 'required|string|max:255',
    'email' => 'required|email|unique:users,email',
    'password' => 'required|min:8|confirmed',
    
    // Numbers
    'price' => 'required|numeric|min:0',
    'quantity' => 'required|integer|between:1,100',
    
    // Dates
    'birth_date' => 'required|date|before:today',
    'start_date' => 'required|date|after:tomorrow',
    
    // Files
    'avatar' => 'required|file|image|max:2048',  // 2MB
    'document' => 'required|file|mimes:pdf,doc,docx|max:10240',  // 10MB
    
    // Arrays
    'items' => 'required|array|min:1',
    'items.*.product_id' => 'required|exists:products,id',
    'items.*.quantity' => 'required|integer|min:1',
    
    // Boolean
    'is_active' => 'required|boolean',
    
    // Exists in DB
    'category_id' => 'required|exists:categories,id',
    
    // Unique with conditions
    'email' => 'required|unique:users,email,'.$userId,  // Except current user
    
    // Sometimes (only validate if present)
    'discount' => 'sometimes|numeric|min:0|max:100',
    
    // Nullable
    'notes' => 'nullable|string|max:1000',
    
    // Multiple rules
    'username' => [
        'required',
        'string',
        'min:3',
        'max:20',
        'alpha_dash',
        'unique:users,username',
    ],
]);
```

---

### **Custom Messages:**

```php
$request->validate([
    'email' => 'required|email',
    'password' => 'required|min:8',
], [
    'email.required' => 'البريد الإلكتروني مطلوب',
    'email.email' => 'البريد الإلكتروني غير صالح',
    'password.required' => 'كلمة المرور مطلوبة',
    'password.min' => 'كلمة المرور يجب أن تكون 8 أحرف على الأقل',
]);
```

---

## **Response Shortcuts**

```php
// Success
return response()->json(['data' => $data], 200);

// Created
return response()->json(['data' => $data], 201);

// No Content
return response()->noContent();  // 204

// Not Found
return response()->json(['message' => 'Not found'], 404);

// Validation Error
return response()->json([
    'message' => 'Validation error',
    'errors' => $errors,
], 422);

// Unauthorized
return response()->json(['message' => 'Unauthorized'], 401);

// Forbidden
return response()->json(['message' => 'Forbidden'], 403);

// Server Error
return response()->json(['message' => 'Server error'], 500);

// With headers
return response()->json($data)->header('X-Custom-Header', 'value');

// Download file
return response()->download($pathToFile);
return response()->download($pathToFile, $filename);
```

---

## **Testing Shortcuts**

```php
// GET request
$response = $this->getJson('/api/v1/products');

// POST request
$response = $this->postJson('/api/v1/products', [
    'name' => 'Product Name',
    'price' => 99.99,
]);

// Authenticated request
$response = $this->actingAs($user, 'sanctum')
    ->getJson('/api/v1/orders');

// Assert status
$response->assertStatus(200);
$response->assertOk();
$response->assertCreated();
$response->assertNoContent();

// Assert JSON
$response->assertJson(['success' => true]);
$response->assertJsonStructure([
    'data' => [
        'id',
        'name',
        'price',
    ],
]);

// Assert database
$this->assertDatabaseHas('products', [
    'name' => 'Product Name',
]);

$this->assertDatabaseMissing('products', [
    'id' => 999,
]);
```

---

## **HTTP Status Codes**

| Code | Meaning | Usage |
|------|---------|-------|
| **200** | OK | Successful GET, PUT, PATCH |
| **201** | Created | Successful POST (created) |
| **204** | No Content | Successful DELETE |
| **400** | Bad Request | Malformed request |
| **401** | Unauthorized | Not authenticated |
| **403** | Forbidden | Not authorized |
| **404** | Not Found | Resource not found |
| **422** | Unprocessable | Validation failed |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Server Error | Internal error |

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
