# تحسين الردود — Response Optimization

---

## **Sparse Fieldsets**

```php
// Request: ?fields=id,name,price
public function index(Request $request)
{
    $query = Product::query();
    
    if ($request->has('fields')) {
        $fields = explode(',', $request->fields);
        $query->select($fields);
    }
    
    return ProductResource::collection($query->get());
}
```

---

## **Response Compression**

```nginx
# NGINX
gzip on;
gzip_types application/json text/plain;
gzip_min_length 1000;
```

```php
// Laravel Middleware
class CompressResponse
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        if (function_exists('gzencode')) {
            $response->setContent(gzencode($response->getContent(), 9));
            $response->header('Content-Encoding', 'gzip');
        }
        
        return $response;
    }
}
```

---

## **Conditional Responses (ETag)**

```php
public function show($id)
{
    $product = Product::findOrFail($id);
    $etag = md5(json_encode($product));
    
    if ($request->header('If-None-Match') === $etag) {
        return response('', 304); // Not Modified
    }
    
    return response()
        ->json(new ProductResource($product))
        ->header('ETag', $etag);
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
