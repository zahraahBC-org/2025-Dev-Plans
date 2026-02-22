# المراقبة المتقدمة — Advanced Observability
**الأهمية | Importance**: 🟡 متوسطة

---

## **ما هو Observability؟ | What is Observability?**

```
Observability = القدرة على فهم الحالة الداخلية للنظام من المخرجات الخارجية

الأركان الثلاثة:
├── Logs (ماذا حدث؟)
├── Metrics (كم؟ كيف؟)
└── Traces (أين؟ متى؟)
```

---

## **Metrics Collection**

### **باستخدام Prometheus:**

```bash
composer require promphp/prometheus_client_php
```

```php
// app/Http/Middleware/CollectMetrics.php
use Prometheus\CollectorRegistry;
use Prometheus\Storage\Redis;

class CollectMetrics
{
    public function handle($request, Closure $next)
    {
        $start = microtime(true);
        
        $response = $next($request);
        
        $duration = (microtime(true) - $start) * 1000; // ms
        
        // Collect metrics
        $registry = new CollectorRegistry(new Redis());
        
        // Request duration
        $histogram = $registry->getOrRegisterHistogram(
            'api',
            'request_duration_ms',
            'Request duration in milliseconds',
            ['method', 'endpoint', 'status']
        );
        
        $histogram->observe(
            $duration,
            [$request->method(), $request->path(), $response->status()]
        );
        
        // Request counter
        $counter = $registry->getOrRegisterCounter(
            'api',
            'requests_total',
            'Total requests',
            ['method', 'endpoint', 'status']
        );
        
        $counter->inc([
            $request->method(),
            $request->path(),
            $response->status()
        ]);
        
        return $response;
    }
}

// Metrics endpoint
Route::get('/metrics', function () {
    $registry = new CollectorRegistry(new Redis());
    $renderer = new RenderTextFormat();
    
    return response($renderer->render($registry->getMetricFamilySamples()))
        ->header('Content-Type', RenderTextFormat::MIME_TYPE);
});
```

---

## **Distributed Tracing**

### **OpenTelemetry (Laravel):**

```bash
composer require open-telemetry/sdk
composer require open-telemetry/exporter-otlp
```

```php
// app/Providers/TracingServiceProvider.php
use OpenTelemetry\SDK\Trace\TracerProvider;

class TracingServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        $tracerProvider = TracerProvider::builder()
            ->addSpanProcessor(/* ... */)
            ->build();
        
        $tracer = $tracerProvider->getTracer('api');
        
        $this->app->instance('tracer', $tracer);
    }
}

// في Controller
public function index()
{
    $tracer = app('tracer');
    $span = $tracer->spanBuilder('get-products')->startSpan();
    
    try {
        $products = Product::all();
        $span->setAttribute('product.count', $products->count());
        
        return ProductResource::collection($products);
    } finally {
        $span->end();
    }
}
```

---

## **Application Performance Monitoring (APM)**

### **Laravel Telescope (Built-in):**

```php
// config/telescope.php
'enabled' => env('TELESCOPE_ENABLED', false),

'watchers' => [
    // Requests
    Watchers\RequestWatcher::class => [
        'enabled' => true,
        'size_limit' => 64,
    ],
    
    // Queries
    Watchers\QueryWatcher::class => [
        'enabled' => true,
        'slow' => 100,  // Log queries > 100ms
    ],
    
    // Cache
    Watchers\CacheWatcher::class => true,
    
    // Jobs
    Watchers\JobWatcher::class => true,
    
    // Exceptions
    Watchers\ExceptionWatcher::class => true,
],
```

---

### **External APM (Sentry, New Relic):**

```bash
# Sentry
composer require sentry/sentry-laravel
php artisan sentry:publish --dsn=your-dsn
```

```php
// config/sentry.php
'dsn' => env('SENTRY_DSN'),
'traces_sample_rate' => env('SENTRY_TRACES_SAMPLE_RATE', 0.2),
'send_default_pii' => false,  // لا PII

// Usage
try {
    // Code
} catch (\Exception $e) {
    Sentry\captureException($e);
    throw $e;
}
```

---

## **Structured Logging**

### **JSON Logging:**

```php
// config/logging.php
'channels' => [
    'json' => [
        'driver' => 'single',
        'path' => storage_path('logs/api.log'),
        'formatter' => \Monolog\Formatter\JsonFormatter::class,
        'level' => 'info',
    ],
],

// Usage
Log::channel('json')->info('Product created', [
    'product_id' => $product->id,
    'user_id' => auth()->id(),
    'ip' => request()->ip(),
    'duration_ms' => 45,
]);

// Output (JSON)
{
  "message": "Product created",
  "context": {
    "product_id": 123,
    "user_id": 45,
    "ip": "192.168.1.1",
    "duration_ms": 45
  },
  "level": 200,
  "level_name": "INFO",
  "channel": "json",
  "datetime": "2025-10-19T10:00:00+00:00"
}
```

---

## **Key Metrics to Track**

### **Performance Metrics:**

```
Request Latency:
├── p50 (median)
├── p95
├── p99
└── max

Throughput:
├── Requests per second (RPS)
├── Requests per minute (RPM)
└── Concurrent requests

Error Rates:
├── 4xx rate (client errors)
├── 5xx rate (server errors)
└── Timeout rate
```

---

### **Business Metrics:**

```
Orders:
├── Orders per minute
├── Average order value
└── Conversion rate

Users:
├── Active users
├── New registrations
└── Login success rate

Products:
├── Products viewed
├── Search queries
└── Add to cart rate
```

---

## **Grafana Dashboard Example**

```json
{
  "dashboard": {
    "title": "API Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "rate(api_requests_total[5m])"
        }]
      },
      {
        "title": "Response Time (p95)",
        "targets": [{
          "expr": "histogram_quantile(0.95, api_request_duration_ms)"
        }]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "rate(api_requests_total{status=~\"5..\"}[5m])"
        }]
      }
    ]
  }
}
```

---

## **Alerting**

### **Alert Rules:**

```yaml
# prometheus-alerts.yml
groups:
  - name: api_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(api_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "معدل أخطاء عالي"
          description: "{{ $value }}% من الطلبات تفشل"
      
      # Slow responses
      - alert: SlowResponses
        expr: histogram_quantile(0.95, api_request_duration_ms) > 500
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "استجابات بطيئة"
          description: "p95 = {{ $value }}ms"
      
      # Queue backlog
      - alert: QueueBacklog
        expr: redis_queue_size > 1000
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Queue متراكمة"
```

---

## **Request ID Tracing**

### **تتبع الطلبات عبر الخدمات:**

```php
// app/Http/Middleware/AddRequestId.php
class AddRequestId
{
    public function handle($request, Closure $next)
    {
        $requestId = $request->header('X-Request-ID') 
            ?? (string) Str::uuid();
        
        // Add to request
        $request->headers->set('X-Request-ID', $requestId);
        
        // Add to logs context
        Log::withContext(['request_id' => $requestId]);
        
        $response = $next($request);
        
        // Add to response
        $response->header('X-Request-ID', $requestId);
        
        return $response;
    }
}

// في Logs
Log::info('Product created', [
    'product_id' => $product->id,
    // request_id موجود تلقائياً من withContext
]);
```

---

## **Checklist**

### **Metrics:**
- [ ] Request rate tracking
- [ ] Response time tracking (p50, p95, p99)
- [ ] Error rate tracking
- [ ] Business metrics

### **Logs:**
- [ ] Structured logging (JSON)
- [ ] Log levels صحيحة
- [ ] Request ID في كل log
- [ ] لا PII في logs

### **Tracing:**
- [ ] Request ID generation
- [ ] Request ID propagation
- [ ] OpenTelemetry (optional)

### **Dashboards:**
- [ ] Performance dashboard
- [ ] Error dashboard
- [ ] Business metrics dashboard

### **Alerts:**
- [ ] High error rate alert
- [ ] Slow response alert
- [ ] Queue backlog alert
- [ ] Down service alert

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
