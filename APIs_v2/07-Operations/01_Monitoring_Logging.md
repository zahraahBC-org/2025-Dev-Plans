# المراقبة والسجلات — Monitoring & Logging

---

## **Laravel Telescope**

```bash
composer require laravel/telescope --dev
php artisan telescope:install
php artisan migrate
```

```php
// config/telescope.php
'enabled' => env('TELESCOPE_ENABLED', false),
'path' => 'admin/telescope',

'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => true,
        'slow' => 100, // >100ms
    ],
    Watchers\RequestWatcher::class => true,
    Watchers\ExceptionWatcher::class => true,
],
```

---

## **Structured Logging**

```php
// config/logging.php
'channels' => [
    'api' => [
        'driver' => 'daily',
        'path' => storage_path('logs/api.log'),
        'level' => 'info',
        'days' => 14,
    ],
],

// Usage
use Illuminate\Support\Facades\Log;

Log::channel('api')->info('Product created', [
    'product_id' => $product->id,
    'user_id' => auth()->id(),
]);
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
