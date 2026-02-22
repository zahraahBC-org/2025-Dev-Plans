# معالجة الأخطاء — Error Handling

---

## **Exception Handler**

```php
// app/Exceptions/Handler.php - API error handling
public function register(): void
{
    $this->renderable(function (Throwable $e, $request) {
        if (!$request->is('api/*')) return;
        
        // Model not found → 404
        if ($e instanceof ModelNotFoundException) {
            return response()->json(['message' => 'Not found'], 404);
        }
        
        // Validation → 422
        if ($e instanceof ValidationException) {
            return response()->json(['errors' => $e->errors()], 422);
        }
        
        // Default → 500
        Log::error('API Error', ['message' => $e->getMessage()]);
        return response()->json(['message' => 'Server error'], 500);
    });
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
