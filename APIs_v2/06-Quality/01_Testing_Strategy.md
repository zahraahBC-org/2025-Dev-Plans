# استراتيجية الاختبارات — Testing Strategy

---

## **أنواع الاختبارات | Test Types**

### **1. Unit Tests**
```php
// tests/Unit/Services/ProductServiceTest.php
public function test_creates_product_with_valid_data(): void
{
    $service = new ProductService(new ProductRepository);
    $product = $service->createProduct(['name' => 'Test']);
    
    $this->assertInstanceOf(Product::class, $product);
}
```

### **2. Feature Tests**
```php
// tests/Feature/API/ProductTest.php
public function test_can_list_products(): void
{
    Product::factory()->count(5)->create();
    
    $response = $this->actingAs($this->user(), 'sanctum')
        ->getJson('/api/v1/products');
    
    $response->assertStatus(200)
        ->assertJsonCount(5, 'data');
}
```

---

## **Coverage Target**

**Goals:**
- الهدف: ≥ 70% coverage
- Critical paths: ≥ 90%

```bash
# Run with coverage
php artisan test --coverage --min=70
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
