# الترقيم والتصفية — Pagination & Filtering

---

## **Pagination**

### **Offset-based (Laravel Default):**

```php
// Controller
public function index()
{
    $products = Product::paginate(20);
    return ProductResource::collection($products);
}

// Response
{
  "data": [...],
  "meta": {
    "current_page": 1,
    "last_page": 10,
    "per_page": 20,
    "total": 200
  },
  "links": {
    "first": "...",
    "last": "...",
    "prev": null,
    "next": "..."
  }
}
```

---

## **Filtering & Sorting**

```php
public function index(Request $request)
{
    $query = Product::query();
    
    // Filtering
    $query->when($request->category_id, 
        fn($q, $v) => $q->where('category_id', $v)
    );
    
    $query->when($request->search, 
        fn($q, $v) => $q->where('name', 'like', "%{$v}%")
    );
    
    // Sorting
    $query->when($request->sort, function ($q, $v) {
        $direction = str_starts_with($v, '-') ? 'desc' : 'asc';
        $field = ltrim($v, '-');
        return $q->orderBy($field, $direction);
    });
    
    return ProductResource::collection($query->paginate(20));
}

// Request: GET /api/v1/products?category_id=5&search=dress&sort=-price
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
