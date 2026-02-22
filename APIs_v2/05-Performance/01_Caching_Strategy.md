# استراتيجية التخزين المؤقت — Caching Strategy

---

## **Redis Caching (Laravel)**

```php
// Cache with tags
Cache::tags(['products'])
    ->remember($key, 3600, fn() => Product::all());

// Invalidate
Cache::tags(['products'])->flush();

// Multiple tags
Cache::tags(['products', 'category:5'])
    ->put($key, $value, 3600);
```

---

## **Caching Patterns**

### **Query Caching:**
```php
public function getProducts(array $filters)
{
    $cacheKey = 'products:' . md5(json_encode($filters));
    
    return Cache::remember($cacheKey, 3600, function () use ($filters) {
        return Product::where($filters)->get();
    });
}
```

### **Model Caching:**
```php
public function getProduct(int $id)
{
    return Cache::remember("product:{$id}", 3600, 
        fn() => Product::with('category')->findOrFail($id)
    );
}
```

---

## **Cache Invalidation**

```php
// Model Observer
class ProductObserver
{
    public function saved($product)
    {
        Cache::tags(['products'])->flush();
        Cache::forget("product:{$product->id}");
    }
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
