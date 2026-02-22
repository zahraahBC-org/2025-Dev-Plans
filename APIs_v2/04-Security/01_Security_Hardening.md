# تقوية الأمان — Security Hardening

---

## **HTTPS/TLS**

```nginx
# Force HTTPS
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

---

## **Security Headers**

```php
// app/Http/Middleware/SecurityHeaders.php
class SecurityHeaders
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
        
        return $response;
    }
}
```

---

## **Input Validation**

```php
// Always validate & sanitize
public function store(Request $request)
{
    $validated = $request->validate([
        'email' => 'required|email|max:255',
        'name' => 'required|string|max:255',
    ]);
    
    // Use validated data only
    User::create($validated);
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
