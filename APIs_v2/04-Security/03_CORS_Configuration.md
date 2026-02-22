# إعداد CORS — CORS Configuration

---

## **CORS Setup (Laravel)**

```php
// config/cors.php
return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    
    'allowed_methods' => ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    
    'allowed_origins' => [
        env('FRONTEND_URL', 'http://localhost:3000'),
        'https://app.example.com',
        'https://admin.example.com',
    ],
    
    'allowed_origins_patterns' => [],
    
    'allowed_headers' => [
        'Content-Type',
        'Authorization',
        'Accept',
        'Origin',
    ],
    
    'exposed_headers' => [
        'X-RateLimit-Limit',
        'X-RateLimit-Remaining',
    ],
    
    'max_age' => 86400,
    
    'supports_credentials' => true,
];
```

---

## **Best Practices**

**DO:**
- Whitelist specific origins (لا *)
- Minimal headers
- `credentials: true` للـSPA فقط
- Preflight caching (max_age)

**DON'T:**
- `'allowed_origins' => ['*']` // خطير!

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
