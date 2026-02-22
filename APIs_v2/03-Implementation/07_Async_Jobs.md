# المهام غير المتزامنة — Async Jobs & Queues
**الأهمية | Importance**: 🟡 متوسطة-عالية

---

## **الهدف | Objective**

تنفيذ المهام الطويلة/الثقيلة بشكل غير متزامن لتحسين تجربة المستخدم.

---

## **متى نستخدم Async Jobs؟ | When to Use?**

### **حالات الاستخدام:**

- إرسال البريد الإلكتروني
- إرسال SMS/WhatsApp
- معالجة الصور (resize, optimize)
- توليد التقارير
- تصدير البيانات
- Import bulk data
- إشعارات Push
- أي عملية > 5 ثوانٍ

---

## **Laravel Queues Setup**

### **1. Configuration**

```php
// .env
QUEUE_CONNECTION=redis

// config/queue.php
'connections' => [
    'redis' => [
        'driver' => 'redis',
        'connection' => 'default',
        'queue' => env('REDIS_QUEUE', 'default'),
        'retry_after' => 90,
        'block_for' => null,
    ],
],
```

---

### **2. Create Job**

```bash
php artisan make:job SendOrderConfirmation
```

```php
class SendOrderConfirmation implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    
    public $tries = 3;
    public $timeout = 60;
    
    public function __construct(public Order $order) {}
    
    public function handle(): void
    {
        $this->order->user->notify(new OrderCreatedNotification($this->order));
        SMS::send($this->order->user->phone, "Order #{$this->order->number} created");
    }
    
    public function failed(\Throwable $exception): void
    {
        Log::error('Failed to send confirmation', ['order_id' => $this->order->id]);
    }
}
```

---

### **3. Dispatch Job**

```php
// في Controller
public function store(StoreOrderRequest $request)
{
    $order = $this->orderService->createOrder($request->validated());
    
    // Dispatch job للـqueue
    SendOrderConfirmation::dispatch($order);
    
    // أو مع delay
    SendOrderConfirmation::dispatch($order)->delay(now()->addMinutes(5));
    
    // أو على queue محدد
    SendOrderConfirmation::dispatch($order)->onQueue('notifications');
    
    return response()->json([
        'success' => true,
        'message' => 'تم إنشاء الطلب بنجاح',
        'data' => new OrderResource($order),
    ], 201);
}
```

---

## **Pattern: 202 Accepted**

### **للعمليات الطويلة جداً (> 1 دقيقة):**

```php
// app/Http/Controllers/API/V1/ReportController.php
public function generate(Request $request)
{
    // إنشاء Job record
    $job = ReportJob::create([
        'user_id' => auth()->id(),
        'type' => $request->type,
        'params' => $request->all(),
        'status' => 'pending',
    ]);
    
    // Dispatch للـqueue
    GenerateReport::dispatch($job);
    
    // 202 Accepted
    return response()->json([
        'success' => true,
        'message' => 'جاري إنشاء التقرير',
        'data' => [
            'job_id' => $job->id,
            'status' => 'pending',
            'check_url' => route('reports.status', $job),
        ],
    ], 202)
    ->header('Location', route('reports.status', $job));
}

// Check status
public function status($jobId)
{
    $job = ReportJob::where('id', $jobId)
        ->where('user_id', auth()->id())
        ->firstOrFail();
    
    return response()->json([
        'success' => true,
        'data' => [
            'job_id' => $job->id,
            'status' => $job->status,  // pending, processing, completed, failed
            'progress' => $job->progress,  // 0-100
            'result_url' => $job->status === 'completed' ? $job->result_url : null,
            'error' => $job->error,
        ],
    ]);
}
```

---

### **Job Implementation Example:**

```php
class GenerateReport implements ShouldQueue
{
    public function handle(): void
    {
        $this->job->update(['status' => 'processing']);
        
        try {
            $data = $this->fetchData();
            $this->job->update(['progress' => 30]);
            
            $file = $this->generatePDF($data);
            $path = Storage::put('reports', $file);
            
            $this->job->update([
                'status' => 'completed',
                'progress' => 100,
                'result_url' => Storage::url($path),
            ]);
        } catch (\Exception $e) {
            $this->job->update(['status' => 'failed', 'error' => $e->getMessage()]);
            throw $e;
        }
    }
}
```

---

## **Queue Workers**

### **تشغيل Workers:**

```bash
# Development
php artisan queue:work

# Production (with supervisor)
php artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
```

---

### **Supervisor Configuration:**

```ini
; /etc/supervisor/conf.d/laravel-worker.conf
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /path/to/artisan queue:work redis --sleep=3 --tries=3
autostart=true
autorestart=true
user=www-data
numprocs=2
redirect_stderr=true
stdout_logfile=/var/log/laravel-worker.log
```

---

## **Monitoring Example**

```php
class MonitorQueue extends Command
{
    public function handle(): void
    {
        $size = Redis::llen('queues:default');
        
        if ($size > 1000) {
            Log::warning('Queue backlog detected', ['size' => $size]);
        }
    }
}

$schedule->command('queue:monitor')->everyFiveMinutes();
```

---

## **Testing Example**

```php
public function test_dispatches_confirmation_job(): void
{
    Queue::fake();
    $order = $this->createOrder();
    
    Queue::assertPushed(SendOrderConfirmation::class, 
        fn($job) => $job->order->id === $order->id
    );
}

public function test_job_sends_email(): void
{
    Mail::fake();
    (new SendOrderConfirmation($order))->handle();
    Mail::assertSent(OrderConfirmationMail::class);
}
```

---

## **Checklist**

### **Setup:**
- [ ] QUEUE_CONNECTION محدد
- [ ] Redis/Database connection
- [ ] Workers running
- [ ] Supervisor configured (prod)

### **Jobs:**
- [ ] Jobs created للعمليات الطويلة
- [ ] Retry logic محدد
- [ ] Timeout محدد
- [ ] Failed job handling

### **Monitoring:**
- [ ] Queue size monitoring
- [ ] Failed jobs tracking
- [ ] Worker health check
- [ ] Alerts للـbacklog

### **Testing:**
- [ ] Job dispatch tests
- [ ] Job execution tests
- [ ] Retry tests
- [ ] Failed job tests

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
