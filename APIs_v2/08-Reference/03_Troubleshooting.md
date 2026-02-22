# حل المشكلات — Troubleshooting

---

## **مشاكل شائعة | Common Issues**

### **1. CORS Errors**

**المشكلة:**
```
Access to fetch at 'https://api.example.com' from origin 'https://app.example.com' 
has been blocked by CORS policy
```

**الحل:**
```php
// config/cors.php
'allowed_origins' => [
    'https://app.example.com',  // أضف الـorigin
],
```

---

### **2. 401 Unauthorized**

**الأسباب المحتملة:**
- Token مفقود
- Token منتهي
- Token غير صالح
- Bearer prefix مفقود

**الحل:**
```php
// تحقق من Header
Authorization: Bearer {token}

// تحقق من Expiration
// تحقق من Signature
```

---

### **3. 403 Forbidden**

**السبب:**
- User مصادق لكن بدون صلاحية

**الحل:**
```php
// تحقق من الأدوار
$user->roles; // []?

// أعط الصلاحية
$user->assignRole('admin');
```

---

### **4. Slow Queries**

**التشخيص:**
```php
// Enable query log
DB::enableQueryLog();
// ... your code
dd(DB::getQueryLog());
```

**الحل:**
- أضف indexes
- استخدم eager loading
- استخدم cache

---

### **5. Rate Limit 429**

**السبب:**
تجاوز الحد المسموح

**الحل:**
```php
// انتظر حتى Reset time
// أو زد الحد في RouteServiceProvider
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
