# تحسين قاعدة البيانات — Database Optimization

---

## **Eager Loading**

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

---

## **Indexes**

```php
// Refer to Database plan for full schema and indexes
Schema::table('products', function (Blueprint $table) {
    $table->index('category_id');
    $table->index('is_active');
    $table->index(['category_id', 'is_active']);
});
```

---

## **Query Optimization**

```php
// ✅ Select specific columns
Product::select(['id', 'name', 'price'])->get();

// ✅ Chunk for large datasets
Product::chunk(200, function ($products) {
    foreach ($products as $product) {
        // Process
    }
});

// ✅ Limit results
Product::latest()->limit(100)->get();
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
