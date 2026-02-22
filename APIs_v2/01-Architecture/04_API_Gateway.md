# بوابة API — API Gateway Setup
**الأهمية | Importance**: 🟡 متوسطة-عالية

---

## **ما هو API Gateway؟ | What is API Gateway?**

**API Gateway = طبقة على الحافة (Edge Layer)**

**تجلس بين Clients والـApplication:**
- توحد نقطة الدخول
- تطبق السياسات المشتركة
- تحمي الـApplication

---

## **الموقع في البنية | Position in Architecture**

```
Clients (Mobile/Web)
        ↓ HTTPS
┌───────────────────┐
│   API Gateway     │  ← هنا
│  (NGINX/Apache)   │
└────────┬──────────┘
         ↓
┌────────────────────┐
│  Laravel App       │
└────────────────────┘
```

---

## **NGINX as API Gateway**

### **Basic Configuration:**

```nginx
# NGINX API Gateway - Key configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;
    root /var/www/api/public;
    
    # SSL
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    # CORS
    add_header Access-Control-Allow-Origin "https://app.example.com" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=60r/m;
    
    # Laravel routing
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    # PHP-FPM
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
        include fastcgi_params;
    }
}
```

---

## **Apache as API Gateway**

### **Configuration (.htaccess):**

```apache
# .htaccess
<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Force HTTPS
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
    
    # Laravel routing
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^ index.php [L]
</IfModule>

# Security Headers
<IfModule mod_headers.c>
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # CORS
    Header always set Access-Control-Allow-Origin "https://app.example.com"
    Header always set Access-Control-Allow-Methods "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
</IfModule>

# Rate Limiting (يحتاج mod_ratelimit)
<IfModule mod_ratelimit.c>
    <Location "/api">
        SetOutputFilter RATE_LIMIT
        SetEnv rate-limit 400
    </Location>
</IfModule>
```

---

## **Cloudflare as Edge Gateway**

### **المزايا:**

- DDoS protection تلقائي
- WAF (Web Application Firewall)
- Rate limiting عالمي
- SSL/TLS مجاني
- CDN للـstatic assets
- Bot protection

### **Cloudflare Rules:**

```javascript
// Page Rule
URL: api.example.com/*
Settings:
- SSL: Full (strict)
- Cache Level: Bypass (للـAPIs)
- Security Level: Medium
- Browser Integrity Check: On

// Firewall Rule
(http.request.uri.path contains "/api/v1/admin")
Then: Challenge (Captcha)

// Rate Limiting Rule
(http.request.uri.path eq "/api/v1/login")
Then: Rate Limit (5 req/min per IP)
```

---

## **Gateway Responsibilities**

### **ما يفعله Gateway:**

| المسؤولية | الوصف | الأداة |
|-----------|--------|-------|
| **TLS Termination** | إنهاء HTTPS | NGINX/Apache |
| **Rate Limiting** | تحديد المعدل | NGINX/Cloudflare |
| **CORS** | السماح للـorigins | NGINX/Laravel |
| **Security Headers** | إضافة headers أمنية | NGINX/Apache |
| **Load Balancing** | توزيع الحمل | NGINX/HAProxy |
| **Request Logging** | تسجيل الطلبات | Access logs |
| **IP Filtering** | منع/سماح IPs | Firewall |
| **WAF** | حماية من هجمات | Cloudflare/ModSecurity |

---

## **Load Balancing (للتوسع)**

```nginx
# NGINX Load Balancer
upstream api_backend {
    least_conn;  # أو ip_hash أو round_robin
    
    server 192.168.1.10:8000 weight=3;
    server 192.168.1.11:8000 weight=2;
    server 192.168.1.12:8000 backup;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }
}
```

---

## **WAF - ModSecurity (NGINX)**

```nginx
# Install
apt-get install libnginx-mod-security

# Enable
load_module modules/ngx_http_modsecurity_module.so;

# Configuration
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/main.conf;

# OWASP Core Rule Set
SecRuleEngine On
SecRule ARGS "@detectSQLi" \
    "id:1001,phase:2,deny,status:403,msg:'SQL Injection detected'"
```

---

## **Health Check Endpoint**

```php
// routes/api.php
Route::get('/health', function () {
    return response()->json([
        'status' => 'healthy',
        'timestamp' => now()->toIso8601String(),
        'services' => [
            'database' => DB::connection()->getPdo() ? 'up' : 'down',
            'redis' => Redis::ping() ? 'up' : 'down',
        ],
    ]);
});

// NGINX health check
location /health {
    access_log off;
    return 200 "healthy\n";
}
```

---

## **Checklist**

### **NGINX/Apache:**
- [ ] HTTPS مفعل (TLS 1.2+)
- [ ] HTTP → HTTPS redirect
- [ ] Security headers
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Client max body size
- [ ] Timeouts محددة

### **Cloudflare (optional):**
- [ ] DNS pointing
- [ ] SSL/TLS mode: Full (strict)
- [ ] Firewall rules
- [ ] Rate limiting rules
- [ ] Bot protection

### **Security:**
- [ ] WAF enabled (optional)
- [ ] IP whitelist/blacklist
- [ ] DDoS protection
- [ ] Certificate auto-renewal

### **Monitoring:**
- [ ] Access logs enabled
- [ ] Error logs enabled
- [ ] Health check endpoint
- [ ] Uptime monitoring

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
