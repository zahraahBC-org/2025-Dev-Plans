# عمليات CRUD — CRUD Operations

---

## **الهدف | Objective**

تنفيذ عمليات CRUD (Create, Read, Update, Delete) بشكل احترافي وموحد.

---

## **CRUD Standard Pattern**

### **REST Mapping:**

| Operation | HTTP Method | Endpoint | Response Code |
|-----------|-------------|----------|---------------|
| **Create** | POST | `/api/v1/products` | 201 Created |
| **Read (List)** | GET | `/api/v1/products` | 200 OK |
| **Read (Single)** | GET | `/api/v1/products/{id}` | 200 OK |
| **Update (Full)** | PUT | `/api/v1/products/{id}` | 200 OK |
| **Update (Partial)** | PATCH | `/api/v1/products/{id}` | 200 OK |
| **Delete** | DELETE | `/api/v1/products/{id}` | 204 No Content |

---

## **التنفيذ | Implementation**

### **Controller Example:**

```php
class ProductController extends Controller
{
    public function __construct(private ProductService $service) {}
    
    // GET /api/v1/products
    public function index()
    {
        return ProductResource::collection(
            $this->service->getProducts(request()->all())
        );
    }
    
    // POST /api/v1/products
    public function store(StoreProductRequest $request)
    {
        $product = $this->service->createProduct($request->validated());
        return (new ProductResource($product))->setStatusCode(201);
    }
}
```

### **Service Layer Pattern:**

```php
public function createProduct(array $data): Product
{
    return DB::transaction(function () use ($data) {
        $product = $this->repository->create($data);
        Cache::tags(['products'])->flush();
        event(new ProductCreated($product));
        return $product;
    });
}
```

---

## **Request Validation Example:**

```php
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

## **Testing Example:**

```php
public function test_can_create_product(): void
{
    $response = $this->actingAs($this->admin(), 'sanctum')
        ->postJson('/api/v1/products', [
            'name' => 'Test Product',
            'price' => 99.99,
        ]);
    
    $response->assertStatus(201)
        ->assertJsonStructure(['success', 'data' => ['id']]);
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
