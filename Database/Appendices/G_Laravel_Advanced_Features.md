# ملحق ز: ميزات Laravel المتقدمة | Appendix G: Laravel Advanced Features
## Jobs, Events, Notifications, Queues & More

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: شرح الميزات المتقدمة في Laravel 12 للتطبيقات على مستوى المؤسسات  
**Purpose**: Explain advanced Laravel 12 features for enterprise-level applications

**الجمهور**: مطورو Laravel المتقدمين، معماريو النظم، قادة التقنية  
**Audience**: Advanced Laravel developers, system architects, technical leads

**المواضيع المغطاة | Topics Covered**:
- Background Jobs & Queues
- Events & Listeners
- Notifications (Email, SMS, Push)
- Task Scheduling
- Broadcasting & WebSockets
- File Storage & Media Management

---

## 🎯 **نظرة عامة | Overview**

Laravel يوفر مجموعة قوية من الميزات المتقدمة التي تمكنك من بناء تطبيقات قابلة للتوسع، موثوقة، وسريعة الاستجابة.

---

## 📑 **جدول المحتويات | Table of Contents**

1. [Background Jobs & Queues](#background-jobs)
2. [Events & Listeners](#events-listeners)
3. [Notifications System](#notifications)
4. [Task Scheduling](#task-scheduling)
5. [Broadcasting & WebSockets](#broadcasting)
6. [File Storage & Media](#file-storage)

---

## 1. Background Jobs & Queues | الوظائف الخلفية وقوائم الانتظار {#background-jobs}

### **1.1 متى تستخدم Jobs | When to Use Jobs**

استخدم Background Jobs عندما:
- العملية تستغرق وقتاً طويلاً (> 2 ثانية)
- العملية لا تحتاج تنفيذ فوري
- تريد تحسين استجابة التطبيق
- تحتاج معالجة بيانات دُفعية (Batch Processing)
- تريد إعادة محاولة العمليات الفاشلة تلقائياً

### **1.2 Order Processing Job | وظيفة معالجة الطلب**

```php
<?php

namespace App\Jobs;

use App\Models\Order;
use App\Services\InventoryService;
use App\Services\NotificationService;
use App\Services\AnalyticsService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

/**
 * وظيفة معالجة الطلب
 * Order Processing Job
 * 
 * يتم تشغيلها في الخلفية بعد إنشاء الطلب
 * Runs in background after order creation
 */
class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * عدد محاولات التنفيذ
     * Number of times to attempt the job
     */
    public int $tries = 3;

    /**
     * عدد الثواني قبل إعادة المحاولة
     * Number of seconds to wait before retrying
     */
    public int $backoff = 60;

    /**
     * الوقت الأقصى للتنفيذ (بالثواني)
     * Maximum execution time (seconds)
     */
    public int $timeout = 120;

    /**
     * يجب حذف الوظيفة إذا فشلت الموديلات في التحميل
     * Delete job if models are missing
     */
    public bool $deleteWhenMissingModels = true;

    /**
     * إنشاء instance جديد من الوظيفة
     * Create a new job instance
     */
    public function __construct(
        public Order $order
    ) {}

    /**
     * تنفيذ الوظيفة
     * Execute the job
     */
    public function handle(
        InventoryService $inventoryService,
        NotificationService $notificationService,
        AnalyticsService $analyticsService
    ): void {
        Log::info('Processing order', ['order_id' => $this->order->id]);

        try {
            // 1. تحديث لقطة المخزون
            // Update inventory snapshot
            $inventoryService->updateSnapshotForOrder($this->order);

            // 2. إرسال إشعار للعميل
            // Send customer notification
            $notificationService->sendOrderConfirmation($this->order);

            // 3. إشعار المستودع
            // Notify warehouse
            $notificationService->notifyWarehouse($this->order);

            // 4. تحديث التحليلات
            // Update analytics
            $analyticsService->trackOrderCreated($this->order);

            // 5. تحديث حالة الطلب
            // Update order status
            $this->order->update(['processed_at' => now()]);

            Log::info('Order processed successfully', ['order_id' => $this->order->id]);

        } catch (\Exception $e) {
            Log::error('Order processing failed', [
                'order_id' => $this->order->id,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);

            // إعادة رمي الاستثناء لإعادة المحاولة التلقائية
            // Re-throw for automatic retry
            throw $e;
        }
    }

    /**
     * معالجة فشل الوظيفة
     * Handle a job failure
     */
    public function failed(\Throwable $exception): void
    {
        Log::critical('Order processing failed permanently', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage()
        ]);

        // إشعار المسؤولين
        // Notify administrators
        // ...

        // تحديث حالة الطلب
        // Update order status
        $this->order->update([
            'status' => 'failed',
            'error_message' => $exception->getMessage()
        ]);
    }

    /**
     * الحصول على tags للوظيفة (للمراقبة)
     * Get tags for the job (monitoring)
     */
    public function tags(): array
    {
        return [
            'order',
            'order:' . $this->order->id,
            'customer:' . $this->order->customer_id,
        ];
    }
}
```

### **1.3 Batch Jobs | الوظائف الدُفعية**

```php
<?php

namespace App\Jobs;

use App\Models\Product;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

/**
 * وظيفة تحديث أسعار المنتجات
 * Update Product Prices Job
 */
class UpdateProductPricesJob implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public array $productIds,
        public float $discountPercentage
    ) {}

    public function handle(): void
    {
        // التحقق من أن الدفعة لم يتم إلغاؤها
        // Check if batch was cancelled
        if ($this->batch()->cancelled()) {
            return;
        }

        // تحديث الأسعار
        // Update prices
        Product::whereIn('id', $this->productIds)->each(function ($product) {
            $product->update([
                'discounted_price' => $product->base_price * (1 - $this->discountPercentage / 100),
                'discount_valid_from' => now(),
                'discount_valid_until' => now()->addDays(7),
            ]);
        });
    }
}
```

```php
<?php

// استخدام Batch Jobs | Using Batch Jobs
use App\Jobs\UpdateProductPricesJob;
use Illuminate\Support\Facades\Bus;

// تقسيم المنتجات إلى مجموعات
// Chunk products into groups
$products = Product::where('category_id', 5)->pluck('id')->chunk(100);

$jobs = [];
foreach ($products as $chunk) {
    $jobs[] = new UpdateProductPricesJob($chunk->toArray(), 20);
}

// إطلاق الدفعة
// Dispatch batch
$batch = Bus::batch($jobs)
    ->name('Summer Sale - 20% Discount')
    ->then(function (Batch $batch) {
        // عند اكتمال جميع الوظائف بنجاح
        // When all jobs completed successfully
        Log::info('All product prices updated', ['batch_id' => $batch->id]);
    })
    ->catch(function (Batch $batch, Throwable $e) {
        // عند فشل أول وظيفة
        // When first job fails
        Log::error('Batch failed', ['batch_id' => $batch->id, 'error' => $e->getMessage()]);
    })
    ->finally(function (Batch $batch) {
        // عند اكتمال الدفعة (نجاح أو فشل)
        // When batch completes (success or failure)
        Log::info('Batch processing finished', ['batch_id' => $batch->id]);
    })
    ->allowFailures()
    ->onQueue('batch-processing')
    ->dispatch();
```

### **1.4 Queue Configuration | تكوين قوائم الانتظار**

```php
// config/queue.php

return [
    'default' => env('QUEUE_CONNECTION', 'redis'),

    'connections' => [
        'redis' => [
            'driver' => 'redis',
            'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
            'queue' => env('REDIS_QUEUE', 'default'),
            'retry_after' => 90,
            'block_for' => null,
            'after_commit' => false,
        ],

        // قوائم انتظار مخصصة
        // Custom queues
        'notifications' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => 'notifications',
            'retry_after' => 60,
        ],

        'batch-processing' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => 'batch-processing',
            'retry_after' => 300,
        ],
    ],

    'failed' => [
        'driver' => env('QUEUE_FAILED_DRIVER', 'database-uuids'),
        'database' => env('DB_CONNECTION', 'mysql'),
        'table' => 'failed_jobs',
    ],
];
```

---

## 2. Events & Listeners | الأحداث والمستمعين {#events-listeners}

### **2.1 Order Events | أحداث الطلبات**

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

/**
 * حدث إنشاء الطلب
 * Order Created Event
 */
class OrderCreated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public Order $order
    ) {}

    /**
     * قنوات البث
     * Broadcast channels
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('orders.' . $this->order->customer_id),
            new PrivateChannel('admin.orders'),
        ];
    }

    /**
     * اسم الحدث للبث
     * Broadcast event name
     */
    public function broadcastAs(): string
    {
        return 'order.created';
    }

    /**
     * البيانات المبثوثة
     * Broadcast data
     */
    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            'order_no' => $this->order->order_no,
            'total' => $this->order->total,
            'status' => $this->order->status,
            'created_at' => $this->order->created_at->toIso8601String(),
        ];
    }
}
```

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

/**
 * حدث تحديث حالة الطلب
 * Order Status Updated Event
 */
class OrderStatusUpdated
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public Order $order,
        public string $oldStatus,
        public string $newStatus
    ) {}
}
```

### **2.2 Event Listeners | مستمعو الأحداث**

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use App\Jobs\ProcessOrderJob;
use App\Notifications\OrderConfirmationNotification;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Support\Facades\Log;

/**
 * مستمع إرسال تأكيد الطلب
 * Send Order Confirmation Listener
 */
class SendOrderConfirmationListener implements ShouldQueue
{
    /**
     * عدد محاولات التنفيذ
     * Attempts
     */
    public int $tries = 3;

    /**
     * الانتظار قبل إعادة المحاولة (ثواني)
     * Backoff (seconds)
     */
    public int $backoff = 60;

    /**
     * معالجة الحدث
     * Handle the event
     */
    public function handle(OrderCreated $event): void
    {
        Log::info('Sending order confirmation', [
            'order_id' => $event->order->id
        ]);

        // إرسال إشعار للعميل
        // Send notification to customer
        $event->order->customer->notify(
            new OrderConfirmationNotification($event->order)
        );
    }

    /**
     * معالجة الفشل
     * Handle failure
     */
    public function failed(OrderCreated $event, \Throwable $exception): void
    {
        Log::error('Failed to send order confirmation', [
            'order_id' => $event->order->id,
            'error' => $exception->getMessage()
        ]);
    }
}
```

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use App\Services\InventoryService;
use Illuminate\Contracts\Queue\ShouldQueue;

/**
 * مستمع تحديث المخزون
 * Update Inventory Listener
 */
class UpdateInventoryListener implements ShouldQueue
{
    public function __construct(
        private InventoryService $inventoryService
    ) {}

    public function handle(OrderCreated $event): void
    {
        // تحديث لقطة المخزون
        // Update inventory snapshot
        $this->inventoryService->updateSnapshotForOrder($event->order);
    }
}
```

### **2.3 Event Service Provider | مزود خدمة الأحداث**

```php
<?php

namespace App\Providers;

use App\Events\OrderCreated;
use App\Events\OrderStatusUpdated;
use App\Events\PaymentProcessed;
use App\Listeners\SendOrderConfirmationListener;
use App\Listeners\UpdateInventoryListener;
use App\Listeners\NotifyWarehouseListener;
use App\Listeners\SendPaymentReceiptListener;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * مستمعو الأحداث للتطبيق
     * Application event listeners
     */
    protected $listen = [
        OrderCreated::class => [
            SendOrderConfirmationListener::class,
            UpdateInventoryListener::class,
            NotifyWarehouseListener::class,
        ],

        OrderStatusUpdated::class => [
            // Listeners for order status updates
        ],

        PaymentProcessed::class => [
            SendPaymentReceiptListener::class,
        ],
    ];

    /**
     * تسجيل الخدمات
     * Register services
     */
    public function boot(): void
    {
        //
    }

    /**
     * تحديد ما إذا كان يجب اكتشاف الأحداث تلقائياً
     * Determine if events should be discovered automatically
     */
    public function shouldDiscoverEvents(): bool
    {
        return false;
    }
}
```

---

## 3. Notifications System | نظام الإشعارات {#notifications}

### **3.1 Multi-Channel Notification | إشعار متعدد القنوات**

```php
<?php

namespace App\Notifications;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Messages\BroadcastMessage;
use Illuminate\Notifications\Notification;
use NotificationChannels\Fcm\FcmChannel;
use NotificationChannels\Fcm\FcmMessage;
use NotificationChannels\Fcm\Resources\Notification as FcmNotification;

/**
 * إشعار تأكيد الطلب
 * Order Confirmation Notification
 */
class OrderConfirmationNotification extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public Order $order
    ) {}

    /**
     * قنوات التوصيل
     * Delivery channels
     */
    public function via(object $notifiable): array
    {
        $channels = ['mail', 'database'];

        // إضافة FCM إذا كان لدى المستخدم device token
        // Add FCM if user has device token
        if ($notifiable->fcm_token) {
            $channels[] = FcmChannel::class;
        }

        // إضافة SMS إذا وافق المستخدم
        // Add SMS if user consented
        if ($notifiable->consent_sms) {
            $channels[] = 'twilio';
        }

        return $channels;
    }

    /**
     * إشعار البريد الإلكتروني
     * Email notification
     */
    public function toMail(object $notifiable): MailMessage
    {
        $url = route('orders.show', $this->order->id);

        return (new MailMessage)
            ->subject('تأكيد طلبك - ' . $this->order->order_no)
            ->greeting('مرحباً ' . $notifiable->first_name . '!')
            ->line('شكراً لك على طلبك من زهراء.')
            ->line('رقم الطلب: **' . $this->order->order_no . '**')
            ->line('المبلغ الإجمالي: **' . $this->order->total . ' ' . $this->order->currency . '**')
            ->action('عرض الطلب', $url)
            ->line('سنقوم بإشعارك عند شحن طلبك.')
            ->salutation('مع أطيب التحيات، فريق زهراء');
    }

    /**
     * إشعار قاعدة البيانات
     * Database notification
     */
    public function toArray(object $notifiable): array
    {
        return [
            'type' => 'order_confirmation',
            'order_id' => $this->order->id,
            'order_no' => $this->order->order_no,
            'total' => $this->order->total,
            'currency' => $this->order->currency,
            'message_ar' => 'تم تأكيد طلبك رقم ' . $this->order->order_no,
            'message_en' => 'Your order ' . $this->order->order_no . ' has been confirmed',
            'action_url' => route('orders.show', $this->order->id),
        ];
    }

    /**
     * إشعار Firebase FCM
     * Firebase FCM notification
     */
    public function toFcm(object $notifiable): FcmMessage
    {
        return (new FcmMessage(notification: new FcmNotification(
            title: 'تأكيد الطلب',
            body: 'تم تأكيد طلبك رقم ' . $this->order->order_no . ' بنجاح',
            image: asset('images/logo.png'),
        )))
        ->data([
            'order_id' => (string) $this->order->id,
            'order_no' => $this->order->order_no,
            'type' => 'order_confirmation',
            'action' => 'view_order',
            'click_action' => 'FLUTTER_NOTIFICATION_CLICK',
        ])
        ->android(
            config: [
                'priority' => 'high',
                'notification' => [
                    'sound' => 'default',
                    'color' => '#FF6B35',
                    'channel_id' => 'orders',
                ],
            ],
        )
        ->apns(
            config: [
                'headers' => [
                    'apns-priority' => '10',
                ],
                'payload' => [
                    'aps' => [
                        'sound' => 'default',
                        'badge' => 1,
                    ],
                ],
            ],
        );
    }

    /**
     * إشعار البث (Real-time)
     * Broadcast notification (Real-time)
     */
    public function toBroadcast(object $notifiable): BroadcastMessage
    {
        return new BroadcastMessage([
            'order_id' => $this->order->id,
            'order_no' => $this->order->order_no,
            'total' => $this->order->total,
            'message' => 'تم تأكيد طلبك بنجاح',
        ]);
    }
}
```

### **3.2 SMS Notification (Twilio) | إشعار SMS**

```php
<?php

namespace App\Notifications;

use App\Models\Order;
use Illuminate\Notifications\Notification;
use NotificationChannels\Twilio\TwilioChannel;
use NotificationChannels\Twilio\TwilioSmsMessage;

/**
 * إشعار شحن الطلب عبر SMS
 * Order Shipped SMS Notification
 */
class OrderShippedNotification extends Notification
{
    public function __construct(
        public Order $order
    ) {}

    public function via($notifiable): array
    {
        return [TwilioChannel::class];
    }

    public function toTwilio($notifiable): TwilioSmsMessage
    {
        $trackingUrl = route('tracking.show', $this->order->shipment->tracking_number);

        return (new TwilioSmsMessage())
            ->content(
                "مرحباً {$notifiable->first_name}، " .
                "تم شحن طلبك رقم {$this->order->order_no}. " .
                "يمكنك تتبع الشحنة من هنا: {$trackingUrl}"
            );
    }
}
```

---

## 4. Task Scheduling | جدولة المهام {#task-scheduling}

### **4.1 Scheduled Tasks | المهام المجدولة**

```php
<?php

namespace App\Console\Kernel;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    /**
     * تسجيل الأوامر المجدولة
     * Register scheduled commands
     */
    protected function schedule(Schedule $schedule): void
    {
        // 1. تحديث لقطات المخزون كل ساعة
        // Update inventory snapshots every hour
        $schedule->command('inventory:update-snapshots')
            ->hourly()
            ->withoutOverlapping()
            ->runInBackground();

        // 2. إرسال تذكير السلة المهجورة بعد 24 ساعة
        // Send abandoned cart reminder after 24 hours
        $schedule->command('cart:send-reminders')
            ->daily()
            ->at('10:00')
            ->timezone('Asia/Riyadh')
            ->emailOutputOnFailure('admin@zahraah.com');

        // 3. تنظيف الجلسات القديمة يومياً
        // Clean old sessions daily
        $schedule->command('session:gc')
            ->daily()
            ->at('03:00');

        // 4. إنشاء تقرير المبيعات اليومي
        // Generate daily sales report
        $schedule->call(function () {
            app(\App\Services\ReportService::class)->generateDailySalesReport();
        })
            ->daily()
            ->at('23:00')
            ->name('daily-sales-report')
            ->onOneServer();

        // 5. مزامنة البيانات مع BigQuery كل 6 ساعات
        // Sync data with BigQuery every 6 hours
        $schedule->job(new \App\Jobs\SyncToBigQueryJob())
            ->everySixHours()
            ->onOneServer();

        // 6. التحقق من انتهاء صلاحية القسائم
        // Check for expired coupons
        $schedule->command('coupons:expire')
            ->hourly()
            ->between('08:00', '23:00');

        // 7. معالجة المبالغ المستردة المعلقة
        // Process pending refunds
        $schedule->command('refunds:process')
            ->everyTenMinutes()
            ->withoutOverlapping(5); // 5 minutes expiry

        // 8. نسخ احتياطي لقاعدة البيانات يومياً
        // Database backup daily
        $schedule->command('backup:run')
            ->daily()
            ->at('02:00')
            ->onSuccess(function () {
                // إشعار عند النجاح
                // Notify on success
            })
            ->onFailure(function () {
                // إشعار عند الفشل
                // Notify on failure
            });
    }

    /**
     * تسجيل الأوامر للتطبيق
     * Register commands for the application
     */
    protected function commands(): void
    {
        $this->load(__DIR__.'/Commands');

        require base_path('routes/console.php');
    }
}
```

### **4.2 Custom Artisan Command | أمر Artisan مخصص**

```php
<?php

namespace App\Console\Commands;

use App\Models\Cart;
use App\Notifications\AbandonedCartReminderNotification;
use Illuminate\Console\Command;

/**
 * أمر إرسال تذكير السلة المهجورة
 * Send Abandoned Cart Reminder Command
 */
class SendCartRemindersCommand extends Command
{
    /**
     * اسم وتوقيع الأمر
     * Command name and signature
     */
    protected $signature = 'cart:send-reminders 
                            {--hours=24 : Hours since cart was abandoned}
                            {--limit=100 : Maximum carts to process}';

    /**
     * وصف الأمر
     * Command description
     */
    protected $description = 'Send reminders for abandoned carts';

    /**
     * تنفيذ الأمر
     * Execute the command
     */
    public function handle(): int
    {
        $hours = $this->option('hours');
        $limit = $this->option('limit');

        $this->info("Processing abandoned carts from {$hours} hours ago...");

        // الحصول على السلال المهجورة
        // Get abandoned carts
        $carts = Cart::where('status', 'abandoned')
            ->where('last_activity_at', '<=', now()->subHours($hours))
            ->whereNull('reminder_sent_at')
            ->with('customer')
            ->limit($limit)
            ->get();

        $count = $carts->count();
        $this->info("Found {$count} abandoned carts");

        if ($count === 0) {
            return Command::SUCCESS;
        }

        // إنشاء شريط تقدم
        // Create progress bar
        $progressBar = $this->output->createProgressBar($count);
        $progressBar->start();

        // إرسال التذكيرات
        // Send reminders
        foreach ($carts as $cart) {
            $cart->customer->notify(
                new AbandonedCartReminderNotification($cart)
            );

            $cart->update(['reminder_sent_at' => now()]);
            
            $progressBar->advance();
        }

        $progressBar->finish();
        $this->newLine(2);
        $this->info("✓ Sent {$count} cart reminders successfully!");

        return Command::SUCCESS;
    }
}
```

---

## 5. File Storage & Media | تخزين الملفات والوسائط {#file-storage}

### **5.1 Media Upload Service | خدمة رفع الوسائط**

```php
<?php

namespace App\Services;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Intervention\Image\Facades\Image;

/**
 * خدمة إدارة الوسائط
 * Media Management Service
 */
class MediaService
{
    /**
     * رفع صورة المنتج
     * Upload product image
     */
    public function uploadProductImage(UploadedFile $file, int $productId): array
    {
        // التحقق من نوع الملف
        // Validate file type
        $allowedMimeTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!in_array($file->getMimeType(), $allowedMimeTypes)) {
            throw new \InvalidArgumentException('Invalid file type');
        }

        // توليد اسم فريد
        // Generate unique name
        $filename = Str::uuid() . '.' . $file->getClientOriginalExtension();
        $path = "products/{$productId}";

        // معالجة الصورة
        // Process image
        $image = Image::make($file);

        // 1. الصورة الأصلية (1200x1200)
        // Original image (1200x1200)
        $original = $image->fit(1200, 1200, function ($constraint) {
            $constraint->upsize();
        })->encode('webp', 90);
        
        Storage::disk('s3')->put(
            "{$path}/original/{$filename}",
            $original,
            'public'
        );

        // 2. صورة مصغرة (400x400)
        // Thumbnail (400x400)
        $thumbnail = $image->fit(400, 400)->encode('webp', 85);
        Storage::disk('s3')->put(
            "{$path}/thumbnails/{$filename}",
            $thumbnail,
            'public'
        );

        // 3. صورة صغيرة جداً (150x150)
        // Small thumbnail (150x150)
        $small = $image->fit(150, 150)->encode('webp', 80);
        Storage::disk('s3')->put(
            "{$path}/small/{$filename}",
            $small,
            'public'
        );

        // إرجاع الروابط
        // Return URLs
        return [
            'original' => Storage::disk('s3')->url("{$path}/original/{$filename}"),
            'thumbnail' => Storage::disk('s3')->url("{$path}/thumbnails/{$filename}"),
            'small' => Storage::disk('s3')->url("{$path}/small/{$filename}"),
            'filename' => $filename,
            'size' => $file->getSize(),
            'mime_type' => $file->getMimeType(),
        ];
    }

    /**
     * حذف صورة المنتج
     * Delete product image
     */
    public function deleteProductImage(int $productId, string $filename): bool
    {
        $path = "products/{$productId}";
        
        Storage::disk('s3')->delete([
            "{$path}/original/{$filename}",
            "{$path}/thumbnails/{$filename}",
            "{$path}/small/{$filename}",
        ]);

        return true;
    }

    /**
     * رفع ملف CSV
     * Upload CSV file
     */
    public function uploadCsvFile(UploadedFile $file, string $directory = 'imports'): string
    {
        $filename = Str::uuid() . '.csv';
        $path = Storage::disk('local')->putFileAs(
            $directory,
            $file,
            $filename
        );

        return $path;
    }

    /**
     * توليد URL موقع مؤقتاً
     * Generate temporary signed URL
     */
    public function generateTemporaryUrl(string $path, int $minutes = 60): string
    {
        return Storage::disk('s3')->temporaryUrl(
            $path,
            now()->addMinutes($minutes)
        );
    }
}
```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [ملحق د: أمثلة الكود | D. Code Examples](D_Code_Examples.md)
- [ملحق هـ: معمارية Laravel النظيفة | E. Laravel Clean Architecture](E_Laravel_Clean_Architecture.md)
- [ملحق و: أفضل ممارسات Laravel | F. Laravel Best Practices](F_Laravel_Best_Practices.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ جاهز للإنتاج | Production Ready