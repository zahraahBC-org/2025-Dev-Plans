# ملحق د: أمثلة الكود | Appendix D: Code Examples
## Flutter وLaravel 12 | Flutter and Laravel 12 Examples

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: أمثلة كود عملية للتكامل مع قاعدة البيانات باستخدام Laravel 12  
**Purpose**: Practical code examples for database integration using Laravel 12

**الجمهور**: مطورو Flutter، مطورو Laravel، معماريو Backend  
**Audience**: Flutter developers, Laravel developers, backend architects

**التقنيات | Technologies**: 
- Frontend: Flutter + Firebase Analytics
- Backend: Laravel 12 + Clean Architecture
- Database: MySQL 8.x
- Cache: Redis

---

## 🎯 **نظرة عامة | Overview**

هذا الملحق يوفر أمثلة كود جاهزة للاستخدام للتكامل مع قاعدة البيانات من تطبيق Flutter وواجهة خلفية Laravel 12 تتبع مبادئ Clean Architecture.

---

## 📱 **أمثلة Flutter | Flutter Examples**

### **1. تسجيل الدخول مع Firebase Analytics**

```dart
import 'package:firebase_analytics/firebase_analytics.dart';

class AuthService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  
  Future<void> onUserLogin(String userId) async {
    // تعيين user_id في Firebase Analytics
    await _analytics.setUserId(id: userId);
    
    // تسجيل حدث تسجيل الدخول
    await _analytics.logEvent(
      name: 'login',
      parameters: {
        'method': 'phone',
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      },
    );
    
    // حفظ في التخزين المحلي
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_id', userId);
  }
  
  Future<void> onUserLogout() async {
    // إزالة user_id
    await _analytics.setUserId(id: null);
    
    // إعادة تعيين بيانات التحليلات
    await _analytics.resetAnalyticsData();
    
    // حذف من التخزين المحلي
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user_id');
  }
}
```

---

### **2. تتبع أحداث التجارة الإلكترونية**

```dart
class AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  
  // عرض منتج
  Future<void> trackViewItem({
    required String skuId,
    required double price,
    required String currency,
    required String category,
  }) async {
    await _analytics.logEvent(
      name: 'view_item',
      parameters: {
        'sku_id': skuId,
        'price': price,
        'currency': currency,
        'category': category,
      },
    );
  }
  
  // إضافة لسلة
  Future<void> trackAddToCart({
    required String skuId,
    required int quantity,
    required double price,
  }) async {
    await _analytics.logEvent(
      name: 'add_to_cart',
      parameters: {
        'sku_id': skuId,
        'quantity': quantity,
        'price': price,
        'currency': 'SAR',
      },
    );
  }
  
  // بدء الدفع
  Future<void> trackBeginCheckout({
    required double cartValue,
    required int itemsCount,
  }) async {
    await _analytics.logEvent(
      name: 'begin_checkout',
      parameters: {
        'cart_value': cartValue,
        'items_count': itemsCount,
        'currency': 'SAR',
      },
    );
  }
  
  // إتمام الشراء
  Future<void> trackPurchase({
    required String orderId,
    required double value,
    required String currency,
    required List<Map<String, dynamic>> items,
  }) async {
    await _analytics.logEvent(
      name: 'purchase',
      parameters: {
        'order_id': orderId,
        'value': value,
        'currency': currency,
        'transaction_id': orderId,
        'items': items,
      },
    );
  }
}
```

---

## 🔷 **أمثلة Laravel 12 (Backend) | Laravel 12 Examples**

### **معمارية المشروع | Project Architecture**

```
app/
├── Domain/              # Business Logic Layer
│   ├── Entities/       # Domain Models
│   ├── Repositories/   # Repository Interfaces
│   └── Services/       # Business Services
├── Application/         # Application Layer
│   ├── UseCases/       # Use Case Classes
│   ├── DTOs/           # Data Transfer Objects
│   └── Events/         # Domain Events
├── Infrastructure/      # Infrastructure Layer
│   ├── Repositories/   # Repository Implementations
│   ├── Services/       # External Services
│   └── Jobs/           # Background Jobs
└── Http/               # Presentation Layer
    ├── Controllers/    # API Controllers
    ├── Requests/       # Form Requests
    └── Resources/      # API Resources
```

---

### **1. إنشاء طلب - Clean Architecture**

#### **1.1 Controller | المتحكم**

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Application\UseCases\Order\CreateOrderUseCase;
use App\Http\Requests\CreateOrderRequest;
use App\Http\Resources\OrderResource;
use Illuminate\Http\JsonResponse;

class OrderController extends Controller
{
    public function __construct(
        private CreateOrderUseCase $createOrderUseCase
    ) {}

    /**
     * إنشاء طلب جديد
     * Create new order
     *
     * @param CreateOrderRequest $request
     * @return JsonResponse
     */
    public function store(CreateOrderRequest $request): JsonResponse
    {
        try {
            $order = $this->createOrderUseCase->execute(
                customerId: $request->user()->id,
                cartItems: $request->validated('items'),
                shippingAddressId: $request->validated('shipping_address_id'),
                paymentMethod: $request->validated('payment_method'),
                utmParams: $request->only(['utm_source', 'utm_medium', 'utm_campaign'])
            );

            return response()->json([
                'success' => true,
                'message' => 'تم إنشاء الطلب بنجاح',
                'data' => new OrderResource($order)
            ], 201);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'فشل إنشاء الطلب',
                'error' => $e->getMessage()
            ], 500);
        }
    }
}
```

#### **1.2 Form Request | طلب النموذج**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CreateOrderRequest extends FormRequest
{
    /**
     * تحديد قواعد التحقق
     * Validation rules
     */
    public function rules(): array
    {
        return [
            'shipping_address_id' => ['required', 'exists:addresses,id'],
            'payment_method' => ['required', 'in:cod,online,wallet'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.variant_id' => ['required', 'exists:product_variants,id'],
            'items.*.quantity' => ['required', 'integer', 'min:1', 'max:99'],
            'coupon_code' => ['nullable', 'string', 'exists:coupons,code'],
            'utm_source' => ['nullable', 'string', 'max:50'],
            'utm_medium' => ['nullable', 'string', 'max:50'],
            'utm_campaign' => ['nullable', 'string', 'max:100'],
        ];
    }

    /**
     * رسائل التحقق المخصصة
     * Custom validation messages
     */
    public function messages(): array
    {
        return [
            'shipping_address_id.required' => 'عنوان الشحن مطلوب',
            'shipping_address_id.exists' => 'عنوان الشحن غير موجود',
            'payment_method.required' => 'طريقة الدفع مطلوبة',
            'payment_method.in' => 'طريقة الدفع غير صالحة',
            'items.required' => 'يجب إضافة عناصر للطلب',
            'items.*.variant_id.exists' => 'المنتج غير موجود',
            'items.*.quantity.min' => 'الحد الأدنى للكمية 1',
        ];
    }
}
```

#### **1.3 Use Case | حالة الاستخدام**

```php
<?php

namespace App\Application\UseCases\Order;

use App\Domain\Entities\Order;
use App\Domain\Repositories\OrderRepositoryInterface;
use App\Domain\Services\InventoryService;
use App\Domain\Services\PricingService;
use App\Application\Events\OrderCreated;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;

class CreateOrderUseCase
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private InventoryService $inventoryService,
        private PricingService $pricingService
    ) {}

    /**
     * تنفيذ حالة الاستخدام
     * Execute use case
     */
    public function execute(
        int $customerId,
        array $cartItems,
        int $shippingAddressId,
        string $paymentMethod,
        array $utmParams = []
    ): Order {
        return DB::transaction(function () use (
            $customerId, $cartItems, $shippingAddressId, $paymentMethod, $utmParams
        ) {
            // 1. التحقق من توفر المخزون
            // Validate inventory availability
            $this->inventoryService->validateAvailability($cartItems);

            // 2. حساب الأسعار
            // Calculate pricing
            $pricing = $this->pricingService->calculateOrderTotal($cartItems);

            // 3. إنشاء الطلب
            // Create order
            $order = $this->orderRepository->create([
                'order_no' => $this->generateOrderNumber(),
                'customer_id' => $customerId,
                'shipping_address_id' => $shippingAddressId,
                'payment_method' => $paymentMethod,
                'subtotal' => $pricing['subtotal'],
                'discount_amount' => $pricing['discount'],
                'tax_amount' => $pricing['tax'],
                'shipping_fee' => $pricing['shipping'],
                'total' => $pricing['total'],
                'currency' => 'SAR',
                'status' => 'created',
                'payment_status' => 'pending',
                'utm_source' => $utmParams['utm_source'] ?? null,
                'utm_medium' => $utmParams['utm_medium'] ?? null,
                'utm_campaign' => $utmParams['utm_campaign'] ?? null,
            ]);

            // 4. إضافة عناصر الطلب
            // Add order items
            foreach ($cartItems as $item) {
                $this->orderRepository->addItem($order->id, [
                    'variant_id' => $item['variant_id'],
                    'quantity' => $item['quantity'],
                    'unit_price' => $item['unit_price'],
                    'discount_per_unit' => $item['discount'] ?? 0,
                    'tax_per_unit' => $item['tax'] ?? 0,
                    'line_total' => $item['line_total'],
                ]);
            }

            // 5. حجز المخزون
            // Reserve inventory
            $this->inventoryService->reserveStock($order->id, $cartItems);

            // 6. إطلاق الحدث
            // Dispatch event
            Event::dispatch(new OrderCreated($order));

            return $order;
        });
    }

    /**
     * توليد رقم الطلب
     * Generate order number
     */
    private function generateOrderNumber(): string
    {
        $date = now()->format('Ymd');
        $sequence = str_pad($this->getNextSequence(), 5, '0', STR_PAD_LEFT);
        
        return "ORD-{$date}-{$sequence}";
    }

    private function getNextSequence(): int
    {
        return DB::table('orders')
            ->whereDate('created_at', today())
            ->count() + 1;
    }
}
```

#### **1.4 Repository Interface | واجهة المستودع**

```php
<?php

namespace App\Domain\Repositories;

use App\Domain\Entities\Order;
use Illuminate\Support\Collection;

interface OrderRepositoryInterface
{
    /**
     * إنشاء طلب جديد
     * Create new order
     */
    public function create(array $data): Order;

    /**
     * إضافة عنصر للطلب
     * Add item to order
     */
    public function addItem(int $orderId, array $itemData): void;

    /**
     * الحصول على طلب بالمعرف
     * Find order by ID
     */
    public function findById(int $orderId): ?Order;

    /**
     * تحديث حالة الطلب
     * Update order status
     */
    public function updateStatus(int $orderId, string $status): bool;

    /**
     * الحصول على طلبات العميل
     * Get customer orders
     */
    public function getCustomerOrders(int $customerId, int $perPage = 15): Collection;
}
```

#### **1.5 Repository Implementation | تطبيق المستودع**

```php
<?php

namespace App\Infrastructure\Repositories;

use App\Domain\Entities\Order;
use App\Domain\Repositories\OrderRepositoryInterface;
use App\Models\Order as OrderModel;
use Illuminate\Support\Collection;

class OrderRepository implements OrderRepositoryInterface
{
    public function create(array $data): Order
    {
        $orderModel = OrderModel::create($data);
        
        return $this->toEntity($orderModel);
    }

    public function addItem(int $orderId, array $itemData): void
    {
        OrderModel::find($orderId)->items()->create($itemData);
    }

    public function findById(int $orderId): ?Order
    {
        $orderModel = OrderModel::with(['items', 'customer', 'shippingAddress'])
            ->find($orderId);

        return $orderModel ? $this->toEntity($orderModel) : null;
    }

    public function updateStatus(int $orderId, string $status): bool
    {
        return OrderModel::where('id', $orderId)
            ->update([
                'status' => $status,
                "{$status}_at" => now(),
            ]);
    }

    public function getCustomerOrders(int $customerId, int $perPage = 15): Collection
    {
        return OrderModel::where('customer_id', $customerId)
            ->with(['items.variant.product'])
            ->orderBy('created_at', 'desc')
            ->paginate($perPage);
    }

    /**
     * تحويل النموذج إلى كيان
     * Convert model to entity
     */
    private function toEntity(OrderModel $model): Order
    {
        return new Order(
            id: $model->id,
            orderNo: $model->order_no,
            customerId: $model->customer_id,
            total: $model->total,
            status: $model->status,
            // ... additional properties
        );
    }
}
```

#### **1.6 Inventory Service | خدمة المخزون**

```php
<?php

namespace App\Domain\Services;

use App\Domain\Exceptions\InsufficientStockException;
use Illuminate\Support\Facades\DB;

class InventoryService
{
    /**
     * التحقق من توفر المخزون
     * Validate inventory availability
     */
    public function validateAvailability(array $cartItems): void
    {
        foreach ($cartItems as $item) {
            $available = $this->getAvailableStock($item['variant_id']);
            
            if ($available < $item['quantity']) {
                throw new InsufficientStockException(
                    "مخزون غير كافٍ للمنتج {$item['variant_id']}"
                );
            }
        }
    }

    /**
     * حجز المخزون للطلب
     * Reserve stock for order
     */
    public function reserveStock(int $orderId, array $cartItems): void
    {
        foreach ($cartItems as $item) {
            DB::table('inventory_ledger')->insert([
                'variant_id' => $item['variant_id'],
                'warehouse_id' => 1, // Default warehouse
                'movement_type' => 'reservation',
                'quantity' => -$item['quantity'],
                'reference_type' => 'order',
                'reference_id' => $orderId,
                'movement_date' => now(),
                'created_at' => now(),
            ]);
        }
    }

    /**
     * الحصول على المخزون المتاح
     * Get available stock
     */
    private function getAvailableStock(int $variantId): int
    {
        return DB::table('stock_snapshot')
            ->where('variant_id', $variantId)
            ->where('warehouse_id', 1)
            ->latest('snapshot_date')
            ->value('available_to_promise') ?? 0;
    }
}
```

---

### **2. معالجة دفع بالمحفظة - Clean Architecture**

#### **2.1 Wallet Payment Use Case | حالة استخدام دفع المحفظة**

```php
<?php

namespace App\Application\UseCases\Payment;

use App\Domain\Entities\Payment;
use App\Domain\Repositories\WalletRepositoryInterface;
use App\Domain\Repositories\OrderRepositoryInterface;
use App\Domain\Exceptions\InsufficientBalanceException;
use App\Application\Events\PaymentProcessed;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;

class ProcessWalletPaymentUseCase
{
    public function __construct(
        private WalletRepositoryInterface $walletRepository,
        private OrderRepositoryInterface $orderRepository
    ) {}

    /**
     * معالجة الدفع من المحفظة
     * Process wallet payment
     */
    public function execute(int $customerId, int $orderId, float $amount): Payment
    {
        return DB::transaction(function () use ($customerId, $orderId, $amount) {
            // 1. قفل المحفظة (Pessimistic Locking)
            // Lock wallet (Pessimistic Locking)
            $wallet = $this->walletRepository->lockAndGet($customerId);

            if (!$wallet) {
                throw new \Exception('المحفظة غير موجودة');
            }

            // 2. التحقق من الرصيد
            // Verify balance
            if ($wallet->balance < $amount) {
                throw new InsufficientBalanceException(
                    "رصيد غير كافٍ. الرصيد المتاح: {$wallet->balance} ريال"
                );
            }

            // 3. إنشاء معاملة الخصم
            // Create debit transaction
            $transaction = $this->walletRepository->createTransaction([
                'wallet_id' => $wallet->id,
                'customer_id' => $customerId,
                'type' => 'debit',
                'amount' => $amount,
                'currency' => 'SAR',
                'source' => 'purchase',
                'reference_type' => 'order',
                'reference_id' => $orderId,
                'status' => 'posted',
                'balance_before' => $wallet->balance,
                'balance_after' => $wallet->balance - $amount,
                'reason_code' => 'order_payment',
                'transaction_date' => now(),
            ]);

            // 4. تحديث رصيد المحفظة
            // Update wallet balance
            $this->walletRepository->updateBalance(
                $wallet->id,
                $wallet->balance - $amount
            );

            // 5. تحديث حالة الطلب
            // Update order status
            $this->orderRepository->updatePaymentStatus($orderId, 'captured');

            // 6. إطلاق الحدث
            // Dispatch event
            Event::dispatch(new PaymentProcessed($transaction, $orderId));

            return $transaction;
        });
    }
}
```

#### **2.2 Wallet Repository | مستودع المحفظة**

```php
<?php

namespace App\Infrastructure\Repositories;

use App\Domain\Entities\Wallet;
use App\Domain\Repositories\WalletRepositoryInterface;
use App\Models\Wallet as WalletModel;
use App\Models\WalletTransaction;

class WalletRepository implements WalletRepositoryInterface
{
    /**
     * قفل المحفظة والحصول عليها
     * Lock and get wallet
     */
    public function lockAndGet(int $customerId): ?Wallet
    {
        $walletModel = WalletModel::where('customer_id', $customerId)
            ->lockForUpdate()
            ->first();

        return $walletModel ? $this->toEntity($walletModel) : null;
    }

    /**
     * إنشاء معاملة محفظة
     * Create wallet transaction
     */
    public function createTransaction(array $data): WalletTransaction
    {
        return WalletTransaction::create($data);
    }

    /**
     * تحديث رصيد المحفظة
     * Update wallet balance
     */
    public function updateBalance(int $walletId, float $newBalance): bool
    {
        return WalletModel::where('id', $walletId)
            ->update([
                'balance' => $newBalance,
                'updated_at' => now(),
            ]);
    }

    /**
     * الحصول على معاملات المحفظة
     * Get wallet transactions
     */
    public function getTransactions(int $walletId, int $perPage = 20)
    {
        return WalletTransaction::where('wallet_id', $walletId)
            ->orderBy('transaction_date', 'desc')
            ->paginate($perPage);
    }

    /**
     * تحويل النموذج إلى كيان
     * Convert model to entity
     */
    private function toEntity(WalletModel $model): Wallet
    {
        return new Wallet(
            id: $model->id,
            customerId: $model->customer_id,
            balance: $model->balance,
            currency: $model->currency,
            status: $model->status
        );
    }
}
```

---

### **3. Background Jobs | الوظائف الخلفية**

#### **3.1 Process Order Job | وظيفة معالجة الطلب**

```php
<?php

namespace App\Infrastructure\Jobs;

use App\Domain\Entities\Order;
use App\Domain\Services\NotificationService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * عدد محاولات التنفيذ
     * Number of attempts
     */
    public $tries = 3;

    /**
     * الوقت الأقصى للتنفيذ (بالثواني)
     * Maximum execution time (seconds)
     */
    public $timeout = 120;

    public function __construct(
        private Order $order
    ) {}

    /**
     * تنفيذ الوظيفة
     * Execute job
     */
    public function handle(NotificationService $notificationService): void
    {
        // 1. إرسال إشعار للعميل
        // Send notification to customer
        $notificationService->sendOrderConfirmation($this->order);

        // 2. إشعار المستودع
        // Notify warehouse
        $notificationService->notifyWarehouse($this->order);

        // 3. تحديث التحليلات
        // Update analytics
        $this->updateAnalytics();
    }

    /**
     * معالجة الفشل
     * Handle failure
     */
    public function failed(\Throwable $exception): void
    {
        // Log the error
        \Log::error('Order processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);

        // Notify admin
        // ...
    }

    private function updateAnalytics(): void
    {
        // Update analytics data
        // ...
    }
}
```

---

### **4. Events & Listeners | الأحداث والمستمعين**

#### **4.1 Order Created Event | حدث إنشاء الطلب**

```php
<?php

namespace App\Application\Events;

use App\Domain\Entities\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderCreated
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public Order $order
    ) {}
}
```

#### **4.2 Send Order Notification Listener | مستمع إرسال إشعار الطلب**

```php
<?php

namespace App\Application\Listeners;

use App\Application\Events\OrderCreated;
use App\Infrastructure\Jobs\ProcessOrderJob;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendOrderNotification implements ShouldQueue
{
    /**
     * معالجة الحدث
     * Handle the event
     */
    public function handle(OrderCreated $event): void
    {
        // إطلاق وظيفة خلفية لإرسال الإشعارات
        // Dispatch background job for notifications
        ProcessOrderJob::dispatch($event->order)
            ->onQueue('notifications');
    }
}
```

#### **4.3 Update Inventory Listener | مستمع تحديث المخزون**

```php
<?php

namespace App\Application\Listeners;

use App\Application\Events\OrderCreated;
use App\Domain\Services\InventoryService;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateInventorySnapshot implements ShouldQueue
{
    public function __construct(
        private InventoryService $inventoryService
    ) {}

    /**
     * معالجة الحدث
     * Handle the event
     */
    public function handle(OrderCreated $event): void
    {
        // تحديث لقطة المخزون
        // Update inventory snapshot
        $this->inventoryService->updateSnapshot($event->order->items);
    }
}
```

---

### **5. Notifications | الإشعارات**

#### **5.1 Order Confirmation Notification | إشعار تأكيد الطلب**

```php
<?php

namespace App\Infrastructure\Notifications;

use App\Domain\Entities\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;
use NotificationChannels\Fcm\FcmChannel;
use NotificationChannels\Fcm\FcmMessage;
use NotificationChannels\Fcm\Resources\Notification as FcmNotification;

class OrderConfirmationNotification extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        private Order $order
    ) {}

    /**
     * قنوات الإشعار
     * Notification channels
     */
    public function via($notifiable): array
    {
        return ['mail', 'database', FcmChannel::class];
    }

    /**
     * إشعار البريد الإلكتروني
     * Email notification
     */
    public function toMail($notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('تأكيد طلبك رقم ' . $this->order->orderNo)
            ->greeting('مرحباً ' . $notifiable->first_name)
            ->line('شكراً لك على طلبك!')
            ->line('رقم الطلب: ' . $this->order->orderNo)
            ->line('المبلغ الإجمالي: ' . $this->order->total . ' ريال')
            ->action('عرض الطلب', url('/orders/' . $this->order->id))
            ->line('سنقوم بإشعارك عند شحن طلبك.');
    }

    /**
     * إشعار قاعدة البيانات
     * Database notification
     */
    public function toArray($notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_no' => $this->order->orderNo,
            'total' => $this->order->total,
            'status' => $this->order->status,
            'message_ar' => 'تم تأكيد طلبك رقم ' . $this->order->orderNo,
            'message_en' => 'Your order ' . $this->order->orderNo . ' has been confirmed',
        ];
    }

    /**
     * إشعار Firebase FCM
     * Firebase FCM notification
     */
    public function toFcm($notifiable): FcmMessage
    {
        return (new FcmMessage(notification: new FcmNotification(
            title: 'تأكيد الطلب',
            body: 'تم تأكيد طلبك رقم ' . $this->order->orderNo,
        )))
        ->data([
            'order_id' => (string) $this->order->id,
            'type' => 'order_confirmation',
            'action' => 'view_order',
        ]);
    }
}
```

---

### **6. API Resources | موارد API**

#### **6.1 Order Resource | مورد الطلب**

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OrderResource extends JsonResource
{
    /**
     * تحويل المورد إلى مصفوفة
     * Transform resource to array
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'order_no' => $this->order_no,
            'status' => $this->status,
            'status_label' => $this->getStatusLabel(),
            'payment_method' => $this->payment_method,
            'payment_status' => $this->payment_status,
            
            // المبالغ | Amounts
            'subtotal' => $this->subtotal,
            'discount_amount' => $this->discount_amount,
            'tax_amount' => $this->tax_amount,
            'shipping_fee' => $this->shipping_fee,
            'total' => $this->total,
            'currency' => $this->currency,
            
            // العناصر | Items
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            
            // العنوان | Address
            'shipping_address' => new AddressResource($this->whenLoaded('shippingAddress')),
            
            // التواريخ | Dates
            'created_at' => $this->created_at?->toIso8601String(),
            'paid_at' => $this->paid_at?->toIso8601String(),
            'delivered_at' => $this->delivered_at?->toIso8601String(),
            
            // التتبع | Tracking
            'tracking_number' => $this->whenLoaded('shipment', fn() => $this->shipment->tracking_number),
            'can_cancel' => $this->canBeCancelled(),
            'can_return' => $this->canBeReturned(),
        ];
    }

    private function getStatusLabel(): string
    {
        return match($this->status) {
            'created' => 'تم الإنشاء',
            'paid' => 'مدفوع',
            'confirmed' => 'مؤكد',
            'packed' => 'جاهز للشحن',
            'shipped' => 'تم الشحن',
            'delivered' => 'تم التوصيل',
            'cancelled' => 'ملغي',
            default => 'غير معروف',
        };
    }
}
```

#### **6.2 Order Item Resource | مورد عنصر الطلب**

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OrderItemResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'variant_id' => $this->variant_id,
            'product' => new ProductResource($this->whenLoaded('variant.product')),
            'variant' => new VariantResource($this->whenLoaded('variant')),
            'quantity' => $this->quantity,
            'unit_price' => $this->unit_price,
            'discount_per_unit' => $this->discount_per_unit,
            'tax_per_unit' => $this->tax_per_unit,
            'line_total' => $this->line_total,
        ];
    }
}
```

---

### **7. Service Providers | مزودو الخدمة**

#### **7.1 Repository Service Provider | مزود خدمة المستودعات**

```php
<?php

namespace App\Providers;

use App\Domain\Repositories\OrderRepositoryInterface;
use App\Domain\Repositories\WalletRepositoryInterface;
use App\Domain\Repositories\CustomerRepositoryInterface;
use App\Infrastructure\Repositories\OrderRepository;
use App\Infrastructure\Repositories\WalletRepository;
use App\Infrastructure\Repositories\CustomerRepository;
use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    /**
     * تسجيل الخدمات
     * Register services
     */
    public function register(): void
    {
        // تسجيل واجهات المستودعات مع تطبيقاتها
        // Register repository interfaces with implementations
        $this->app->bind(OrderRepositoryInterface::class, OrderRepository::class);
        $this->app->bind(WalletRepositoryInterface::class, WalletRepository::class);
        $this->app->bind(CustomerRepositoryInterface::class, CustomerRepository::class);
    }

    /**
     * تشغيل الخدمات
     * Bootstrap services
     */
    public function boot(): void
    {
        //
    }
}
```

#### **7.2 Event Service Provider | مزود خدمة الأحداث**

```php
<?php

namespace App\Providers;

use App\Application\Events\OrderCreated;
use App\Application\Events\PaymentProcessed;
use App\Application\Listeners\SendOrderNotification;
use App\Application\Listeners\UpdateInventorySnapshot;
use App\Application\Listeners\ProcessPaymentNotification;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * مستمعو الأحداث للتطبيق
     * Event listeners for the application
     */
    protected $listen = [
        OrderCreated::class => [
            SendOrderNotification::class,
            UpdateInventorySnapshot::class,
        ],
        PaymentProcessed::class => [
            ProcessPaymentNotification::class,
        ],
    ];

    /**
     * تسجيل أي أحداث للتطبيق
     * Register any events for your application
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

### **8. Middleware | الوسيطة**

#### **8.1 Check Stock Availability Middleware | وسيطة التحقق من توفر المخزون**

```php
<?php

namespace App\Http\Middleware;

use App\Domain\Services\InventoryService;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckStockAvailability
{
    public function __construct(
        private InventoryService $inventoryService
    ) {}

    /**
     * معالجة الطلب الوارد
     * Handle an incoming request
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->routeIs('orders.store')) {
            try {
                $this->inventoryService->validateAvailability(
                    $request->input('items', [])
                );
            } catch (\Exception $e) {
                return response()->json([
                    'success' => false,
                    'message' => 'بعض المنتجات غير متوفرة',
                    'error' => $e->getMessage()
                ], 422);
            }
        }

        return $next($request);
    }
}
```

---

### **9. Database Migrations | هجرات قاعدة البيانات**

#### **9.1 Create Orders Table Migration | هجرة إنشاء جدول الطلبات**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * تشغيل الهجرة
     * Run the migrations
     */
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->string('order_no', 20)->unique()->comment('رقم الطلب');
            $table->foreignId('customer_id')->constrained()->comment('معرف العميل');
            
            // المبالغ | Amounts
            $table->decimal('subtotal', 10, 2)->comment('المجموع الفرعي');
            $table->decimal('discount_amount', 10, 2)->default(0)->comment('مبلغ الخصم');
            $table->decimal('tax_amount', 10, 2)->default(0)->comment('مبلغ الضريبة');
            $table->decimal('shipping_fee', 10, 2)->default(0)->comment('رسوم الشحن');
            $table->decimal('total', 10, 2)->comment('الإجمالي');
            $table->char('currency', 3)->default('SAR')->comment('العملة');
            
            // الحالة | Status
            $table->enum('status', [
                'created', 'paid', 'confirmed', 'packed', 
                'shipped', 'out_for_delivery', 'delivered',
                'cancelled', 'failed', 'returned'
            ])->default('created')->comment('حالة الطلب');
            
            // الدفع | Payment
            $table->enum('payment_method', ['cod', 'online', 'wallet'])->comment('طريقة الدفع');
            $table->enum('payment_status', [
                'pending', 'authorized', 'captured', 'settled', 'refunded', 'failed'
            ])->default('pending')->comment('حالة الدفع');
            
            // الشحن | Shipping
            $table->foreignId('shipping_address_id')->constrained('addresses')->comment('عنوان الشحن');
            $table->foreignId('warehouse_id')->constrained()->comment('المستودع');
            
            // إسناد التسويق | Marketing Attribution
            $table->string('utm_source', 50)->nullable()->comment('مصدر UTM');
            $table->string('utm_medium', 50)->nullable()->comment('وسيط UTM');
            $table->string('utm_campaign', 100)->nullable()->comment('حملة UTM');
            $table->string('utm_term', 100)->nullable()->comment('مصطلح UTM');
            $table->string('utm_content', 100)->nullable()->comment('محتوى UTM');
            
            // الطوابع الزمنية | Timestamps
            $table->timestamp('paid_at')->nullable()->comment('وقت الدفع');
            $table->timestamp('confirmed_at')->nullable()->comment('وقت التأكيد');
            $table->timestamp('packed_at')->nullable()->comment('وقت التعبئة');
            $table->timestamp('shipped_at')->nullable()->comment('وقت الشحن');
            $table->timestamp('delivered_at')->nullable()->comment('وقت التوصيل');
            $table->timestamp('cancelled_at')->nullable()->comment('وقت الإلغاء');
            $table->timestamps();
            $table->softDeletes()->comment('الحذف الناعم');
            
            // الفهارس | Indexes
            $table->index(['customer_id', 'created_at']);
            $table->index(['status', 'created_at']);
            $table->index('payment_status');
            $table->index('created_at');
        });
    }

    /**
     * عكس الهجرة
     * Reverse the migrations
     */
    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
};
```

---

### **10. Model with Relationships | النموذج مع العلاقات**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Database\Eloquent\SoftDeletes;

class Order extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'order_no',
        'customer_id',
        'subtotal',
        'discount_amount',
        'tax_amount',
        'shipping_fee',
        'total',
        'currency',
        'status',
        'payment_method',
        'payment_status',
        'shipping_address_id',
        'warehouse_id',
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'paid_at',
        'confirmed_at',
        'delivered_at',
    ];

    protected $casts = [
        'subtotal' => 'decimal:2',
        'discount_amount' => 'decimal:2',
        'tax_amount' => 'decimal:2',
        'shipping_fee' => 'decimal:2',
        'total' => 'decimal:2',
        'paid_at' => 'datetime',
        'confirmed_at' => 'datetime',
        'packed_at' => 'datetime',
        'shipped_at' => 'datetime',
        'delivered_at' => 'datetime',
        'cancelled_at' => 'datetime',
    ];

    /**
     * علاقة العميل
     * Customer relationship
     */
    public function customer(): BelongsTo
    {
        return $this->belongsTo(Customer::class);
    }

    /**
     * علاقة عناصر الطلب
     * Order items relationship
     */
    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    /**
     * علاقة عنوان الشحن
     * Shipping address relationship
     */
    public function shippingAddress(): BelongsTo
    {
        return $this->belongsTo(Address::class, 'shipping_address_id');
    }

    /**
     * علاقة المستودع
     * Warehouse relationship
     */
    public function warehouse(): BelongsTo
    {
        return $this->belongsTo(Warehouse::class);
    }

    /**
     * علاقة الشحنة
     * Shipment relationship
     */
    public function shipment(): HasOne
    {
        return $this->hasOne(Shipment::class);
    }

    /**
     * علاقة الدفع
     * Payment relationship
     */
    public function payment(): HasOne
    {
        return $this->hasOne(Payment::class);
    }

    /**
     * Scopes
     */
    public function scopeDelivered($query)
    {
        return $query->where('status', 'delivered');
    }

    public function scopePending($query)
    {
        return $query->whereIn('status', ['created', 'paid', 'confirmed']);
    }

    /**
     * Helper Methods
     */
    public function canBeCancelled(): bool
    {
        return in_array($this->status, ['created', 'paid', 'confirmed']);
    }

    public function canBeReturned(): bool
    {
        return $this->status === 'delivered' 
            && $this->delivered_at?->diffInDays(now()) <= 14;
    }
}
```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [ملحق هـ: معمارية Laravel النظيفة | E. Laravel Clean Architecture](E_Laravel_Clean_Architecture.md)
- [ملحق و: أفضل ممارسات Laravel | F. Laravel Best Practices](F_Laravel_Best_Practices.md)
- [ملحق ز: ميزات Laravel المتقدمة | G. Laravel Advanced Features](G_Laravel_Advanced_Features.md)
- [08. نظام المحفظة | Wallet System](../08_Wallet_System.md)
- [02. معمارية قاعدة البيانات | Database Architecture](../02_Database_Architecture.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 2.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ تم التحديث لـ Laravel 12 | Updated to Laravel 12
