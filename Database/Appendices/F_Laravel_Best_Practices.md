# ملحق و: أفضل ممارسات Laravel | Appendix F: Laravel Best Practices
## Service Classes, Repositories, Form Requests & More

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: توثيق أفضل ممارسات Laravel 12 للتطوير على مستوى المؤسسات  
**Purpose**: Document Laravel 12 best practices for enterprise-level development

**الجمهور**: مطورو Laravel، معماريو Backend، قادة الفريق  
**Audience**: Laravel developers, backend architects, team leads

**التغطية | Coverage**:
- Service Classes Pattern
- Repository Pattern
- Form Request Validation
- API Resources & Collections
- Query Optimization
- Security Best Practices

---

## 🎯 **نظرة عامة | Overview**

هذا الملحق يوفر أفضل الممارسات والأنماط الموصى بها لتطوير تطبيقات Laravel على مستوى المؤسسات، مع التركيز على الجودة، قابلية الصيانة، والأداء.

---

## 📑 **جدول المحتويات | Table of Contents**

1. [Service Classes Pattern](#service-classes)
2. [Repository Pattern](#repository-pattern)
3. [Form Request Validation](#form-requests)
4. [API Resources](#api-resources)
5. [Query Optimization](#query-optimization)
6. [Security Best Practices](#security)
7. [Testing Strategies](#testing)
8. [Code Organization](#code-organization)

---

## 1. Service Classes Pattern | نمط فئات الخدمة {#service-classes}

### **متى تستخدم Service Classes | When to Use**

استخدم Service Classes عندما:
- العملية تتطلب منطق أعمال معقد
- العملية تتفاعل مع عدة Models
- تريد فصل منطق الأعمال عن Controllers
- تحتاج إلى إعادة استخدام المنطق في أماكن متعددة

### **1.1 Order Service Example | مثال خدمة الطلبات**

```php
<?php

namespace App\Services;

use App\Models\Order;
use App\Models\OrderItem;
use App\Models\Customer;
use App\Repositories\OrderRepository;
use App\Repositories\InventoryRepository;
use App\Notifications\OrderConfirmationNotification;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use App\Exceptions\InsufficientStockException;

/**
 * خدمة إدارة الطلبات
 * Order Management Service
 * 
 * المسؤولية: تنسيق العمليات المتعلقة بالطلبات
 * Responsibility: Coordinate order-related operations
 */
class OrderService
{
    public function __construct(
        private OrderRepository $orderRepository,
        private InventoryRepository $inventoryRepository,
        private PricingService $pricingService,
        private NotificationService $notificationService
    ) {}

    /**
     * إنشاء طلب جديد
     * Create new order
     *
     * @param array $data
     * @return Order
     * @throws InsufficientStockException
     */
    public function createOrder(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            // 1. التحقق من المخزون
            // Verify inventory
            $this->verifyInventoryAvailability($data['items']);

            // 2. حساب الأسعار
            // Calculate prices
            $pricing = $this->pricingService->calculateOrderTotal($data['items']);

            // 3. إنشاء الطلب
            // Create order
            $order = $this->orderRepository->create([
                'customer_id' => $data['customer_id'],
                'order_no' => $this->generateOrderNumber(),
                'subtotal' => $pricing['subtotal'],
                'discount_amount' => $pricing['discount'],
                'tax_amount' => $pricing['tax'],
                'shipping_fee' => $pricing['shipping_fee'],
                'total' => $pricing['total'],
                'status' => 'created',
                'payment_method' => $data['payment_method'],
            ]);

            // 4. إضافة العناصر
            // Add items
            $this->addOrderItems($order, $data['items']);

            // 5. حجز المخزون
            // Reserve inventory
            $this->inventoryRepository->reserveStock($order->id, $data['items']);

            // 6. إرسال إشعار
            // Send notification
            $this->notificationService->sendOrderConfirmation($order);

            // 7. تسجيل في Log
            // Log activity
            Log::info('Order created', [
                'order_id' => $order->id,
                'customer_id' => $data['customer_id'],
                'total' => $pricing['total']
            ]);

            return $order;
        });
    }

    /**
     * إلغاء الطلب
     * Cancel order
     *
     * @param int $orderId
     * @param string $reason
     * @return bool
     */
    public function cancelOrder(int $orderId, string $reason): bool
    {
        return DB::transaction(function () use ($orderId, $reason) {
            $order = $this->orderRepository->findOrFail($orderId);

            // التحقق من إمكانية الإلغاء
            // Check if cancellable
            if (!$this->canBeCancelled($order)) {
                throw new \Exception('Cannot cancel order in ' . $order->status . ' status');
            }

            // تحديث الحالة
            // Update status
            $order->update([
                'status' => 'cancelled',
                'cancelled_at' => now(),
                'cancellation_reason' => $reason,
            ]);

            // إطلاق المخزون المحجوز
            // Release reserved inventory
            $this->inventoryRepository->releaseReservation($orderId);

            // معالجة الاسترداد إذا مدفوع
            // Process refund if paid
            if ($order->payment_status === 'captured') {
                $this->processRefund($order);
            }

            // إرسال إشعار
            // Send notification
            $this->notificationService->sendOrderCancellation($order);

            return true;
        });
    }

    /**
     * التحقق من توفر المخزون
     * Verify inventory availability
     *
     * @param array $items
     * @throws InsufficientStockException
     */
    private function verifyInventoryAvailability(array $items): void
    {
        foreach ($items as $item) {
            $available = $this->inventoryRepository->getAvailableStock($item['variant_id']);
            
            if ($available < $item['quantity']) {
                throw new InsufficientStockException(
                    "Insufficient stock for variant {$item['variant_id']}. " .
                    "Available: {$available}, Requested: {$item['quantity']}"
                );
            }
        }
    }

    /**
     * إضافة عناصر الطلب
     * Add order items
     */
    private function addOrderItems(Order $order, array $items): void
    {
        foreach ($items as $item) {
            OrderItem::create([
                'order_id' => $order->id,
                'variant_id' => $item['variant_id'],
                'quantity' => $item['quantity'],
                'unit_price' => $item['unit_price'],
                'line_total' => $item['quantity'] * $item['unit_price'],
            ]);
        }
    }

    /**
     * توليد رقم طلب فريد
     * Generate unique order number
     */
    private function generateOrderNumber(): string
    {
        $date = now()->format('Ymd');
        $count = Order::whereDate('created_at', today())->count() + 1;
        
        return sprintf('ORD-%s-%05d', $date, $count);
    }

    /**
     * التحقق من إمكانية الإلغاء
     * Check if order can be cancelled
     */
    private function canBeCancelled(Order $order): bool
    {
        return in_array($order->status, ['created', 'paid', 'confirmed']);
    }

    /**
     * معالجة الاسترداد
     * Process refund
     */
    private function processRefund(Order $order): void
    {
        // Implementation depends on payment gateway
        // ...
    }
}
```

### **1.2 Pricing Service | خدمة التسعير**

```php
<?php

namespace App\Services;

use App\Models\Product;
use App\Models\Coupon;
use Illuminate\Support\Collection;

/**
 * خدمة حساب الأسعار
 * Pricing Calculation Service
 */
class PricingService
{
    private const VAT_RATE = 0.15; // 15% VAT
    private const FREE_SHIPPING_THRESHOLD = 200.00;
    private const STANDARD_SHIPPING_FEE = 20.00;

    /**
     * حساب إجمالي الطلب
     * Calculate order total
     *
     * @param array $items
     * @param string|null $couponCode
     * @return array
     */
    public function calculateOrderTotal(array $items, ?string $couponCode = null): array
    {
        // 1. حساب المجموع الفرعي
        // Calculate subtotal
        $subtotal = $this->calculateSubtotal($items);

        // 2. تطبيق الخصم
        // Apply discount
        $discount = $this->calculateDiscount($subtotal, $couponCode);

        // 3. حساب الضريبة
        // Calculate tax
        $taxableAmount = $subtotal - $discount;
        $tax = $taxableAmount * self::VAT_RATE;

        // 4. حساب رسوم الشحن
        // Calculate shipping
        $shippingFee = $this->calculateShippingFee($taxableAmount);

        // 5. الإجمالي
        // Total
        $total = $subtotal - $discount + $tax + $shippingFee;

        return [
            'subtotal' => round($subtotal, 2),
            'discount' => round($discount, 2),
            'tax' => round($tax, 2),
            'shipping_fee' => round($shippingFee, 2),
            'total' => round($total, 2),
        ];
    }

    /**
     * حساب المجموع الفرعي
     * Calculate subtotal
     */
    private function calculateSubtotal(array $items): float
    {
        $subtotal = 0;

        foreach ($items as $item) {
            $product = Product::find($item['product_id']);
            $price = $product->discounted_price ?? $product->base_price;
            $subtotal += $price * $item['quantity'];
        }

        return $subtotal;
    }

    /**
     * حساب الخصم
     * Calculate discount
     */
    private function calculateDiscount(float $subtotal, ?string $couponCode): float
    {
        if (!$couponCode) {
            return 0;
        }

        $coupon = Coupon::where('code', $couponCode)
            ->where('valid_from', '<=', now())
            ->where('valid_until', '>=', now())
            ->first();

        if (!$coupon) {
            return 0;
        }

        // قسيمة نسبة مئوية | Percentage coupon
        if ($coupon->type === 'percentage') {
            $discount = $subtotal * ($coupon->value / 100);
            
            // تطبيق الحد الأقصى للخصم
            // Apply max discount cap
            if ($coupon->max_discount && $discount > $coupon->max_discount) {
                return $coupon->max_discount;
            }
            
            return $discount;
        }

        // قسيمة مبلغ ثابت | Fixed amount coupon
        return min($coupon->value, $subtotal);
    }

    /**
     * حساب رسوم الشحن
     * Calculate shipping fee
     */
    private function calculateShippingFee(float $orderAmount): float
    {
        // شحن مجاني للطلبات فوق الحد
        // Free shipping above threshold
        if ($orderAmount >= self::FREE_SHIPPING_THRESHOLD) {
            return 0;
        }

        return self::STANDARD_SHIPPING_FEE;
    }
}
```

---

## 2. Repository Pattern | نمط المستودع {#repository-pattern}

### **2.1 Repository Interface | واجهة المستودع**

```php
<?php

namespace App\Repositories\Interfaces;

use App\Models\Order;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

/**
 * واجهة مستودع الطلبات
 * Order Repository Interface
 */
interface OrderRepositoryInterface
{
    /**
     * الحصول على جميع الطلبات
     * Get all orders
     */
    public function all(): Collection;

    /**
     * الحصول على طلبات مع ترقيم
     * Get paginated orders
     */
    public function paginate(int $perPage = 15): LengthAwarePaginator;

    /**
     * الحصول على طلب بالمعرف
     * Find order by ID
     */
    public function find(int $id): ?Order;

    /**
     * الحصول على طلب أو فشل
     * Find order or fail
     */
    public function findOrFail(int $id): Order;

    /**
     * إنشاء طلب جديد
     * Create new order
     */
    public function create(array $data): Order;

    /**
     * تحديث طلب
     * Update order
     */
    public function update(int $id, array $data): bool;

    /**
     * حذف طلب
     * Delete order
     */
    public function delete(int $id): bool;

    /**
     * الحصول على طلبات العميل
     * Get customer orders
     */
    public function getByCustomerId(int $customerId): Collection;

    /**
     * الحصول على طلبات بحالة معينة
     * Get orders by status
     */
    public function getByStatus(string $status): Collection;

    /**
     * الحصول على طلبات بين تاريخين
     * Get orders between dates
     */
    public function getBetweenDates(\DateTime $from, \DateTime $to): Collection;

    /**
     * البحث في الطلبات
     * Search orders
     */
    public function search(string $query): Collection;
}
```

### **2.2 Repository Implementation | تطبيق المستودع**

```php
<?php

namespace App\Repositories;

use App\Models\Order;
use App\Repositories\Interfaces\OrderRepositoryInterface;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\Cache;

/**
 * تطبيق مستودع الطلبات
 * Order Repository Implementation
 */
class OrderRepository implements OrderRepositoryInterface
{
    protected Order $model;

    public function __construct(Order $model)
    {
        $this->model = $model;
    }

    /**
     * الحصول على جميع الطلبات
     */
    public function all(): Collection
    {
        return Cache::remember('orders.all', 3600, function () {
            return $this->model->with(['customer', 'items'])->get();
        });
    }

    /**
     * الحصول على طلبات مع ترقيم
     */
    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return $this->model
            ->with(['customer', 'items'])
            ->latest()
            ->paginate($perPage);
    }

    /**
     * الحصول على طلب بالمعرف
     */
    public function find(int $id): ?Order
    {
        return Cache::remember("orders.{$id}", 3600, function () use ($id) {
            return $this->model
                ->with(['customer', 'items.variant', 'shippingAddress'])
                ->find($id);
        });
    }

    /**
     * الحصول على طلب أو فشل
     */
    public function findOrFail(int $id): Order
    {
        return $this->model
            ->with(['customer', 'items.variant'])
            ->findOrFail($id);
    }

    /**
     * إنشاء طلب جديد
     */
    public function create(array $data): Order
    {
        $order = $this->model->create($data);
        
        // مسح الكاش
        // Clear cache
        Cache::forget('orders.all');
        
        return $order->load(['customer', 'items']);
    }

    /**
     * تحديث طلب
     */
    public function update(int $id, array $data): bool
    {
        $order = $this->findOrFail($id);
        $updated = $order->update($data);
        
        if ($updated) {
            // مسح الكاش
            Cache::forget("orders.{$id}");
            Cache::forget('orders.all');
        }
        
        return $updated;
    }

    /**
     * حذف طلب
     */
    public function delete(int $id): bool
    {
        $deleted = $this->findOrFail($id)->delete();
        
        if ($deleted) {
            Cache::forget("orders.{$id}");
            Cache::forget('orders.all');
        }
        
        return $deleted;
    }

    /**
     * الحصول على طلبات العميل
     */
    public function getByCustomerId(int $customerId): Collection
    {
        return $this->model
            ->where('customer_id', $customerId)
            ->with(['items.variant'])
            ->latest()
            ->get();
    }

    /**
     * الحصول على طلبات بحالة معينة
     */
    public function getByStatus(string $status): Collection
    {
        return $this->model
            ->where('status', $status)
            ->with(['customer', 'items'])
            ->latest()
            ->get();
    }

    /**
     * الحصول على طلبات بين تاريخين
     */
    public function getBetweenDates(\DateTime $from, \DateTime $to): Collection
    {
        return $this->model
            ->whereBetween('created_at', [$from, $to])
            ->with(['customer', 'items'])
            ->get();
    }

    /**
     * البحث في الطلبات
     */
    public function search(string $query): Collection
    {
        return $this->model
            ->where('order_no', 'LIKE', "%{$query}%")
            ->orWhereHas('customer', function ($q) use ($query) {
                $q->where('first_name', 'LIKE', "%{$query}%")
                  ->orWhere('last_name', 'LIKE', "%{$query}%");
            })
            ->with(['customer', 'items'])
            ->get();
    }
}
```

### **2.3 Repository Service Provider | مزود خدمة المستودعات**

```php
<?php

namespace App\Providers;

use App\Repositories\Interfaces\OrderRepositoryInterface;
use App\Repositories\OrderRepository;
use App\Repositories\Interfaces\CustomerRepositoryInterface;
use App\Repositories\CustomerRepository;
use App\Repositories\Interfaces\ProductRepositoryInterface;
use App\Repositories\ProductRepository;
use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    /**
     * تسجيل الخدمات
     * Register services
     */
    public function register(): void
    {
        // تسجيل المستودعات
        // Register repositories
        $this->app->bind(
            OrderRepositoryInterface::class,
            OrderRepository::class
        );

        $this->app->bind(
            CustomerRepositoryInterface::class,
            CustomerRepository::class
        );

        $this->app->bind(
            ProductRepositoryInterface::class,
            ProductRepository::class
        );
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

---

## 3. Form Request Validation | التحقق من طلبات النماذج {#form-requests}

### **3.1 Create Order Request | طلب إنشاء طلب**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

/**
 * طلب إنشاء طلب
 * Create Order Request
 */
class CreateOrderRequest extends FormRequest
{
    /**
     * تحديد ما إذا كان المستخدم مصرحاً لهذا الطلب
     * Determine if the user is authorized to make this request
     */
    public function authorize(): bool
    {
        // التأكد من أن المستخدم مسجل دخول
        // Ensure user is authenticated
        return $this->user() !== null;
    }

    /**
     * قواعد التحقق للطلب
     * Validation rules for the request
     */
    public function rules(): array
    {
        return [
            // معلومات الشحن | Shipping info
            'shipping_address_id' => [
                'required',
                'integer',
                Rule::exists('addresses', 'id')->where(function ($query) {
                    $query->where('customer_id', $this->user()->id);
                }),
            ],

            // طريقة الدفع | Payment method
            'payment_method' => [
                'required',
                'string',
                Rule::in(['cod', 'online', 'wallet']),
            ],

            // عناصر الطلب | Order items
            'items' => [
                'required',
                'array',
                'min:1',
                'max:20',
            ],
            'items.*.variant_id' => [
                'required',
                'integer',
                'exists:product_variants,id',
            ],
            'items.*.quantity' => [
                'required',
                'integer',
                'min:1',
                'max:99',
            ],

            // كود القسيمة | Coupon code
            'coupon_code' => [
                'nullable',
                'string',
                'max:50',
                'exists:coupons,code',
            ],

            // إسناد التسويق | Marketing attribution
            'utm_source' => ['nullable', 'string', 'max:50'],
            'utm_medium' => ['nullable', 'string', 'max:50'],
            'utm_campaign' => ['nullable', 'string', 'max:100'],
            'utm_term' => ['nullable', 'string', 'max:100'],
            'utm_content' => ['nullable', 'string', 'max:100'],

            // ملاحظات | Notes
            'notes' => ['nullable', 'string', 'max:500'],
        ];
    }

    /**
     * رسائل التحقق المخصصة
     * Custom validation messages
     */
    public function messages(): array
    {
        return [
            // عنوان الشحن | Shipping address
            'shipping_address_id.required' => 'عنوان الشحن مطلوب',
            'shipping_address_id.exists' => 'عنوان الشحن المحدد غير موجود أو لا ينتمي لك',

            // طريقة الدفع | Payment method
            'payment_method.required' => 'طريقة الدفع مطلوبة',
            'payment_method.in' => 'طريقة الدفع المحددة غير صالحة',

            // عناصر الطلب | Order items
            'items.required' => 'يجب إضافة منتج واحد على الأقل',
            'items.min' => 'يجب إضافة منتج واحد على الأقل',
            'items.max' => 'لا يمكن إضافة أكثر من 20 منتج في طلب واحد',
            'items.*.variant_id.required' => 'معرف المنتج مطلوب',
            'items.*.variant_id.exists' => 'المنتج المحدد غير موجود',
            'items.*.quantity.required' => 'الكمية مطلوبة',
            'items.*.quantity.min' => 'الحد الأدنى للكمية هو 1',
            'items.*.quantity.max' => 'الحد الأقصى للكمية هو 99',

            // كود القسيمة | Coupon code
            'coupon_code.exists' => 'كود القسيمة غير صالح',

            // ملاحظات | Notes
            'notes.max' => 'الملاحظات يجب ألا تتجاوز 500 حرف',
        ];
    }

    /**
     * تخصيص أسماء الحقول
     * Customize attribute names
     */
    public function attributes(): array
    {
        return [
            'shipping_address_id' => 'عنوان الشحن',
            'payment_method' => 'طريقة الدفع',
            'items' => 'المنتجات',
            'items.*.variant_id' => 'المنتج',
            'items.*.quantity' => 'الكمية',
            'coupon_code' => 'كود القسيمة',
            'notes' => 'الملاحظات',
        ];
    }

    /**
     * إعداد البيانات للتحقق
     * Prepare data for validation
     */
    protected function prepareForValidation(): void
    {
        // تنظيف كود القسيمة
        // Sanitize coupon code
        if ($this->has('coupon_code')) {
            $this->merge([
                'coupon_code' => strtoupper(trim($this->coupon_code)),
            ]);
        }
    }

    /**
     * التحقق بعد قواعد التحقق الأساسية
     * Validation after base rules pass
     */
    public function withValidator($validator): void
    {
        $validator->after(function ($validator) {
            // التحقق من توفر المخزون
            // Verify inventory availability
            if ($this->has('items')) {
                $this->validateInventory($validator);
            }

            // التحقق من صلاحية القسيمة
            // Verify coupon validity
            if ($this->has('coupon_code')) {
                $this->validateCoupon($validator);
            }
        });
    }

    /**
     * التحقق من توفر المخزون
     * Validate inventory availability
     */
    private function validateInventory($validator): void
    {
        // Implementation
        // ...
    }

    /**
     * التحقق من صلاحية القسيمة
     * Validate coupon validity
     */
    private function validateCoupon($validator): void
    {
        // Implementation
        // ...
    }
}
```

### **3.2 Update Profile Request | طلب تحديث الملف الشخصي**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class UpdateProfileRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $userId = $this->user()->id;

        return [
            'first_name' => ['required', 'string', 'max:100'],
            'last_name' => ['required', 'string', 'max:100'],
            'email' => [
                'nullable',
                'email',
                'max:255',
                Rule::unique('customers', 'email')->ignore($userId),
            ],
            'phone' => [
                'required',
                'string',
                'regex:/^\+966[0-9]{9}$/',
                Rule::unique('customers', 'phone')->ignore($userId),
            ],
            'birth_year' => [
                'nullable',
                'integer',
                'min:1920',
                'max:' . (date('Y') - 18),
            ],
            'gender' => [
                'nullable',
                Rule::in(['male', 'female', 'prefer_not_to_say']),
            ],
        ];
    }

    public function messages(): array
    {
        return [
            'first_name.required' => 'الاسم الأول مطلوب',
            'last_name.required' => 'اسم العائلة مطلوب',
            'email.unique' => 'البريد الإلكتروني مستخدم بالفعل',
            'phone.required' => 'رقم الهاتف مطلوب',
            'phone.regex' => 'رقم الهاتف يجب أن يكون بصيغة +966xxxxxxxxx',
            'phone.unique' => 'رقم الهاتف مستخدم بالفعل',
            'birth_year.max' => 'يجب أن يكون عمرك 18 عاماً على الأقل',
        ];
    }
}
```

---

## 4. API Resources | موارد API {#api-resources}

### **4.1 Order Resource | مورد الطلب**

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * مورد الطلب
 * Order Resource
 */
class OrderResource extends JsonResource
{
    /**
     * تحويل المورد إلى مصفوفة
     * Transform the resource into an array
     *
     * @param Request $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            // المعلومات الأساسية | Basic info
            'id' => $this->id,
            'order_no' => $this->order_no,
            'status' => $this->status,
            'status_label' => $this->getStatusLabel(),
            'status_color' => $this->getStatusColor(),

            // معلومات الدفع | Payment info
            'payment_method' => $this->payment_method,
            'payment_method_label' => $this->getPaymentMethodLabel(),
            'payment_status' => $this->payment_status,

            // المبالغ | Amounts
            'subtotal' => $this->formatMoney($this->subtotal),
            'discount_amount' => $this->formatMoney($this->discount_amount),
            'tax_amount' => $this->formatMoney($this->tax_amount),
            'shipping_fee' => $this->formatMoney($this->shipping_fee),
            'total' => $this->formatMoney($this->total),
            'currency' => $this->currency,

            // العلاقات | Relationships
            'customer' => new CustomerResource($this->whenLoaded('customer')),
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            'shipping_address' => new AddressResource($this->whenLoaded('shippingAddress')),
            'shipment' => new ShipmentResource($this->whenLoaded('shipment')),

            // التواريخ | Dates
            'created_at' => $this->created_at?->toIso8601String(),
            'paid_at' => $this->paid_at?->toIso8601String(),
            'confirmed_at' => $this->confirmed_at?->toIso8601String(),
            'shipped_at' => $this->shipped_at?->toIso8601String(),
            'delivered_at' => $this->delivered_at?->toIso8601String(),
            'cancelled_at' => $this->cancelled_at?->toIso8601String(),

            // الإجراءات المتاحة | Available actions
            'can_cancel' => $this->canBeCancelled(),
            'can_return' => $this->canBeReturned(),
            'can_track' => $this->canBeTracked(),

            // معلومات إضافية | Additional info
            'tracking_url' => $this->when(
                $this->shipment,
                fn() => route('tracking.show', $this->shipment->tracking_number)
            ),
            'estimated_delivery' => $this->when(
                $this->shipment,
                fn() => $this->shipment->estimated_delivery
            ),
        ];
    }

    /**
     * تنسيق المبلغ
     * Format money amount
     */
    private function formatMoney(float $amount): string
    {
        return number_format($amount, 2, '.', ',');
    }

    /**
     * الحصول على تسمية الحالة
     * Get status label
     */
    private function getStatusLabel(): string
    {
        return match($this->status) {
            'created' => 'تم الإنشاء',
            'paid' => 'مدفوع',
            'confirmed' => 'مؤكد',
            'packed' => 'جاهز للشحن',
            'shipped' => 'تم الشحن',
            'out_for_delivery' => 'في طريق التوصيل',
            'delivered' => 'تم التوصيل',
            'cancelled' => 'ملغي',
            'failed' => 'فشل',
            default => 'غير معروف',
        };
    }

    /**
     * الحصول على لون الحالة
     * Get status color
     */
    private function getStatusColor(): string
    {
        return match($this->status) {
            'created', 'paid' => '#FFA500',
            'confirmed', 'packed' => '#2196F3',
            'shipped', 'out_for_delivery' => '#9C27B0',
            'delivered' => '#4CAF50',
            'cancelled', 'failed' => '#F44336',
            default => '#9E9E9E',
        };
    }

    /**
     * الحصول على تسمية طريقة الدفع
     * Get payment method label
     */
    private function getPaymentMethodLabel(): string
    {
        return match($this->payment_method) {
            'cod' => 'الدفع عند الاستلام',
            'online' => 'الدفع الإلكتروني',
            'wallet' => 'المحفظة',
            default => 'غير محدد',
        };
    }

    /**
     * مع بيانات إضافية
     * With additional data
     *
     * @param Request $request
     * @return array
     */
    public function with(Request $request): array
    {
        return [
            'meta' => [
                'version' => '1.0',
                'timestamp' => now()->toIso8601String(),
            ],
        ];
    }
}
```

### **4.2 Order Collection Resource | مورد مجموعة الطلبات**

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

/**
 * مورد مجموعة الطلبات
 * Order Collection Resource
 */
class OrderCollection extends ResourceCollection
{
    /**
     * تحويل المجموعة إلى مصفوفة
     * Transform the collection into an array
     *
     * @param Request $request
     * @return array
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'count' => $this->count(),
                'per_page' => $this->perPage(),
                'current_page' => $this->currentPage(),
                'total_pages' => $this->lastPage(),
            ],
            'links' => [
                'first' => $this->url(1),
                'last' => $this->url($this->lastPage()),
                'prev' => $this->previousPageUrl(),
                'next' => $this->nextPageUrl(),
            ],
        ];
    }

    /**
     * مع بيانات إضافية
     * With additional data
     *
     * @param Request $request
     * @return array
     */
    public function with(Request $request): array
    {
        return [
            'statistics' => [
                'total_orders' => $this->total(),
                'total_revenue' => $this->collection->sum('total'),
                'avg_order_value' => $this->collection->avg('total'),
            ],
        ];
    }
}
```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [ملحق د: أمثلة الكود | D. Code Examples](D_Code_Examples.md)
- [ملحق هـ: معمارية Laravel النظيفة | E. Laravel Clean Architecture](E_Laravel_Clean_Architecture.md)
- [ملحق ز: ميزات Laravel المتقدمة | G. Laravel Advanced Features](G_Laravel_Advanced_Features.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ جاهز للإنتاج | Production Ready

**ملاحظة | Note**: هذا الملحق يغطي الجزء الأول من أفضل الممارسات. سيتم إضافة أقسام Query Optimization، Security Best Practices، Testing Strategies، وCode Organization في التحديثات القادمة.
