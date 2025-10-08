# ملحق هـ: معمارية Laravel النظيفة | Appendix E: Laravel Clean Architecture
## أنماط ومبادئ Clean Architecture | Clean Architecture Patterns and Principles

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: شرح تطبيق مبادئ Clean Architecture في Laravel 12  
**Purpose**: Explain Clean Architecture principles implementation in Laravel 12

**الجمهور**: معماريو Backend، مطورو Laravel المتقدمين، قادة التقنية  
**Audience**: Backend architects, senior Laravel developers, technical leads

**المتطلبات | Prerequisites**:
- Laravel 12 fundamentals
- SOLID principles understanding
- Design patterns knowledge
- Domain-Driven Design basics

---

## 🎯 **نظرة عامة | Overview**

Clean Architecture هي نهج معماري يهدف إلى فصل المخاوف التجارية عن التفاصيل التقنية، مما يجعل التطبيق:
- ✅ قابل للاختبار بشكل مستقل عن UI وقاعدة البيانات والخدمات الخارجية
- ✅ مستقل عن الإطار Framework-agnostic
- ✅ مستقل عن قاعدة البيانات Database-independent
- ✅ مستقل عن أي واجهة مستخدم UI-independent
- ✅ سهل الصيانة والتطوير Maintainable and scalable

---

## 📑 **جدول المحتويات | Table of Contents**

1. [مبادئ Clean Architecture الأساسية](#core-principles)
2. [هيكل الطبقات في Laravel](#layer-structure)
3. [طبقة Domain | Domain Layer](#domain-layer)
4. [طبقة Application | Application Layer](#application-layer)
5. [طبقة Infrastructure | Infrastructure Layer](#infrastructure-layer)
6. [طبقة Presentation | Presentation Layer](#presentation-layer)
7. [تدفق البيانات | Data Flow](#data-flow)
8. [أفضل الممارسات | Best Practices](#best-practices)

---

## 1. مبادئ Clean Architecture الأساسية | Core Principles {#core-principles}

### **قاعدة التبعية | Dependency Rule**

القاعدة الذهبية: **التبعيات تشير دائماً للداخل نحو طبقة Domain**

```
┌─────────────────────────────────────────────┐
│  Presentation Layer (HTTP, API)             │
│  ↓ depends on                               │
├─────────────────────────────────────────────┤
│  Infrastructure Layer (DB, External APIs)   │
│  ↓ depends on                               │
├─────────────────────────────────────────────┤
│  Application Layer (Use Cases)              │
│  ↓ depends on                               │
├─────────────────────────────────────────────┤
│  Domain Layer (Business Logic)              │
│  ✓ No dependencies on outer layers         │
└─────────────────────────────────────────────┘
```

### **مبادئ SOLID**

| المبدأ Principle | الشرح Explanation | التطبيق في Laravel |
|-----------------|------------------|-------------------|
| **S**ingle Responsibility | كل class له مسؤولية واحدة | Use Cases منفصلة لكل عملية |
| **O**pen/Closed | مفتوح للتوسع، مغلق للتعديل | Repository Pattern + Interfaces |
| **L**iskov Substitution | الـ subclasses تستبدل parent classes | Interface implementations |
| **I**nterface Segregation | واجهات صغيرة ومحددة | Repository interfaces per entity |
| **D**ependency Inversion | الاعتماد على Abstractions | Dependency Injection |

---

## 2. هيكل الطبقات في Laravel | Layer Structure {#layer-structure}

### **الهيكل الموصى به | Recommended Structure**

```
app/
├── Domain/                          # طبقة المجال | Domain Layer
│   ├── Entities/                   # كيانات الأعمال | Business Entities
│   │   ├── Order.php
│   │   ├── Customer.php
│   │   └── Product.php
│   │
│   ├── ValueObjects/               # كائنات القيمة | Value Objects
│   │   ├── Money.php
│   │   ├── Address.php
│   │   └── Email.php
│   │
│   ├── Repositories/               # واجهات المستودعات | Repository Interfaces
│   │   ├── OrderRepositoryInterface.php
│   │   ├── CustomerRepositoryInterface.php
│   │   └── ProductRepositoryInterface.php
│   │
│   ├── Services/                   # خدمات المجال | Domain Services
│   │   ├── PricingService.php
│   │   ├── InventoryService.php
│   │   └── ShippingCalculator.php
│   │
│   └── Exceptions/                 # استثناءات المجال | Domain Exceptions
│       ├── InsufficientStockException.php
│       ├── InsufficientBalanceException.php
│       └── InvalidOrderStatusException.php
│
├── Application/                     # طبقة التطبيق | Application Layer
│   ├── UseCases/                   # حالات الاستخدام | Use Cases
│   │   ├── Order/
│   │   │   ├── CreateOrderUseCase.php
│   │   │   ├── CancelOrderUseCase.php
│   │   │   └── GetOrderDetailsUseCase.php
│   │   │
│   │   ├── Payment/
│   │   │   ├── ProcessPaymentUseCase.php
│   │   │   └── RefundPaymentUseCase.php
│   │   │
│   │   └── Customer/
│   │       ├── RegisterCustomerUseCase.php
│   │       └── UpdateProfileUseCase.php
│   │
│   ├── DTOs/                       # كائنات نقل البيانات | Data Transfer Objects
│   │   ├── CreateOrderDTO.php
│   │   ├── CustomerRegistrationDTO.php
│   │   └── PaymentRequestDTO.php
│   │
│   ├── Events/                     # أحداث التطبيق | Application Events
│   │   ├── OrderCreated.php
│   │   ├── PaymentProcessed.php
│   │   └── CustomerRegistered.php
│   │
│   └── Listeners/                  # مستمعو الأحداث | Event Listeners
│       ├── SendOrderConfirmation.php
│       ├── UpdateInventorySnapshot.php
│       └── NotifyWarehouse.php
│
├── Infrastructure/                  # طبقة البنية التحتية | Infrastructure Layer
│   ├── Repositories/               # تطبيقات المستودعات | Repository Implementations
│   │   ├── EloquentOrderRepository.php
│   │   ├── EloquentCustomerRepository.php
│   │   └── EloquentProductRepository.php
│   │
│   ├── Services/                   # خدمات خارجية | External Services
│   │   ├── PaymentGateway/
│   │   │   ├── MoyasarPaymentService.php
│   │   │   └── TapPaymentService.php
│   │   │
│   │   ├── Notification/
│   │   │   ├── FirebaseNotificationService.php
│   │   │   └── TwilioSmsService.php
│   │   │
│   │   └── Shipping/
│   │       ├── AramexShippingService.php
│   │       └── SmashShippingService.php
│   │
│   ├── Jobs/                       # وظائف خلفية | Background Jobs
│   │   ├── ProcessOrderJob.php
│   │   ├── SendNotificationJob.php
│   │   └── UpdateInventoryJob.php
│   │
│   └── Persistence/                # تفاصيل قاعدة البيانات | Database Details
│       ├── Migrations/
│       ├── Seeders/
│       └── Factories/
│
└── Http/                           # طبقة العرض | Presentation Layer
    ├── Controllers/                # المتحكمات | Controllers
    │   ├── Api/
    │   │   └── V1/
    │   │       ├── OrderController.php
    │   │       ├── CustomerController.php
    │   │       └── ProductController.php
    │   │
    │   └── Web/
    │       └── AdminController.php
    │
    ├── Requests/                   # طلبات النماذج | Form Requests
    │   ├── CreateOrderRequest.php
    │   ├── UpdateCustomerRequest.php
    │   └── ProcessPaymentRequest.php
    │
    ├── Resources/                  # موارد API | API Resources
    │   ├── OrderResource.php
    │   ├── CustomerResource.php
    │   └── ProductResource.php
    │
    └── Middleware/                 # الوسيطات | Middleware
        ├── CheckStockAvailability.php
        ├── ValidatePaymentMethod.php
        └── EnsureOrderOwnership.php
```

---

## 3. طبقة Domain | Domain Layer {#domain-layer}

### **3.1 Entities | الكيانات**

الكيانات تمثل مفاهيم الأعمال الأساسية مع هويتها الفريدة.

```php
<?php

namespace App\Domain\Entities;

use App\Domain\ValueObjects\Money;
use App\Domain\Exceptions\InvalidOrderStatusException;

class Order
{
    private int $id;
    private string $orderNo;
    private int $customerId;
    private Money $total;
    private OrderStatus $status;
    private array $items = [];
    private \DateTimeImmutable $createdAt;
    
    public function __construct(
        int $id,
        string $orderNo,
        int $customerId,
        Money $total,
        OrderStatus $status,
        \DateTimeImmutable $createdAt
    ) {
        $this->id = $id;
        $this->orderNo = $orderNo;
        $this->customerId = $customerId;
        $this->total = $total;
        $this->status = $status;
        $this->createdAt = $createdAt;
    }

    /**
     * منطق الأعمال: يمكن إلغاء الطلب فقط في مراحل معينة
     * Business Logic: Order can only be cancelled in specific stages
     */
    public function cancel(): void
    {
        if (!$this->status->canBeCancelled()) {
            throw new InvalidOrderStatusException(
                "Cannot cancel order in {$this->status->value} status"
            );
        }
        
        $this->status = OrderStatus::CANCELLED;
    }

    /**
     * منطق الأعمال: حساب إجمالي الطلب
     * Business Logic: Calculate order total
     */
    public function calculateTotal(): Money
    {
        $total = Money::zero();
        
        foreach ($this->items as $item) {
            $total = $total->add($item->getLineTotal());
        }
        
        return $total;
    }

    public function addItem(OrderItem $item): void
    {
        $this->items[] = $item;
        $this->total = $this->calculateTotal();
    }

    // Getters
    public function getId(): int
    {
        return $this->id;
    }

    public function getOrderNo(): string
    {
        return $this->orderNo;
    }

    public function getStatus(): OrderStatus
    {
        return $this->status;
    }

    public function getTotal(): Money
    {
        return $this->total;
    }
}
```

### **3.2 Value Objects | كائنات القيمة**

كائنات غير قابلة للتغيير تمثل قيماً دون هوية.

```php
<?php

namespace App\Domain\ValueObjects;

use InvalidArgumentException;

/**
 * كائن قيمة المال - Immutable Money Value Object
 */
final class Money
{
    private function __construct(
        private readonly float $amount,
        private readonly string $currency
    ) {
        if ($amount < 0) {
            throw new InvalidArgumentException('Amount cannot be negative');
        }
        
        if (strlen($currency) !== 3) {
            throw new InvalidArgumentException('Invalid currency code');
        }
    }

    public static function fromFloat(float $amount, string $currency = 'SAR'): self
    {
        return new self($amount, $currency);
    }

    public static function zero(string $currency = 'SAR'): self
    {
        return new self(0.0, $currency);
    }

    /**
     * إضافة مبلغ آخر
     * Add another amount
     */
    public function add(Money $other): self
    {
        $this->assertSameCurrency($other);
        
        return new self(
            $this->amount + $other->amount,
            $this->currency
        );
    }

    /**
     * طرح مبلغ آخر
     * Subtract another amount
     */
    public function subtract(Money $other): self
    {
        $this->assertSameCurrency($other);
        
        return new self(
            $this->amount - $other->amount,
            $this->currency
        );
    }

    /**
     * ضرب في رقم
     * Multiply by a number
     */
    public function multiply(float $multiplier): self
    {
        return new self(
            $this->amount * $multiplier,
            $this->currency
        );
    }

    /**
     * التحقق من العملة المتطابقة
     * Assert same currency
     */
    private function assertSameCurrency(Money $other): void
    {
        if ($this->currency !== $other->currency) {
            throw new InvalidArgumentException(
                "Cannot operate on different currencies: {$this->currency} vs {$other->currency}"
            );
        }
    }

    /**
     * مقارنة
     * Comparison
     */
    public function isGreaterThan(Money $other): bool
    {
        $this->assertSameCurrency($other);
        return $this->amount > $other->amount;
    }

    public function isLessThan(Money $other): bool
    {
        $this->assertSameCurrency($other);
        return $this->amount < $other->amount;
    }

    public function equals(Money $other): bool
    {
        return $this->amount === $other->amount 
            && $this->currency === $other->currency;
    }

    // Getters
    public function getAmount(): float
    {
        return $this->amount;
    }

    public function getCurrency(): string
    {
        return $this->currency;
    }

    public function __toString(): string
    {
        return number_format($this->amount, 2) . ' ' . $this->currency;
    }
}
```

```php
<?php

namespace App\Domain\ValueObjects;

use InvalidArgumentException;

/**
 * كائن قيمة البريد الإلكتروني
 * Email Value Object
 */
final class Email
{
    private function __construct(
        private readonly string $value
    ) {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException("Invalid email: {$value}");
        }
    }

    public static function fromString(string $email): self
    {
        return new self(strtolower(trim($email)));
    }

    public function getValue(): string
    {
        return $this->value;
    }

    public function getDomain(): string
    {
        return substr($this->value, strpos($this->value, '@') + 1);
    }

    public function equals(Email $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
```

### **3.3 Repository Interfaces | واجهات المستودعات**

```php
<?php

namespace App\Domain\Repositories;

use App\Domain\Entities\Order;
use App\Domain\ValueObjects\Money;
use Illuminate\Support\Collection;

/**
 * واجهة مستودع الطلبات
 * Order Repository Interface
 * 
 * هذه الواجهة تحدد العقد دون الارتباط بتفاصيل التنفيذ
 * This interface defines the contract without coupling to implementation details
 */
interface OrderRepositoryInterface
{
    /**
     * حفظ طلب جديد
     * Save new order
     */
    public function save(Order $order): Order;

    /**
     * الحصول على طلب بالمعرف
     * Find order by ID
     */
    public function findById(int $id): ?Order;

    /**
     * الحصول على طلب برقم الطلب
     * Find order by order number
     */
    public function findByOrderNo(string $orderNo): ?Order;

    /**
     * الحصول على طلبات العميل
     * Get customer orders
     */
    public function findByCustomerId(int $customerId, int $limit = 20): Collection;

    /**
     * الحصول على طلبات بحالة معينة
     * Get orders by status
     */
    public function findByStatus(string $status, int $limit = 100): Collection;

    /**
     * تحديث حالة الطلب
     * Update order status
     */
    public function updateStatus(int $orderId, string $newStatus): bool;

    /**
     * حذف طلب (حذف ناعم)
     * Delete order (soft delete)
     */
    public function delete(int $orderId): bool;

    /**
     * حساب إجمالي مبيعات اليوم
     * Calculate today's total sales
     */
    public function getTodayTotalSales(): Money;

    /**
     * الحصول على الطلبات المعلقة
     * Get pending orders
     */
    public function getPendingOrders(): Collection;
}
```

### **3.4 Domain Services | خدمات المجال**

خدمات تحتوي على منطق أعمال لا ينتمي لكيان واحد.

```php
<?php

namespace App\Domain\Services;

use App\Domain\Entities\Order;
use App\Domain\ValueObjects\Money;
use App\Domain\Repositories\ProductRepositoryInterface;
use App\Domain\Repositories\CouponRepositoryInterface;

/**
 * خدمة حساب الأسعار
 * Pricing Calculation Service
 */
class PricingService
{
    public function __construct(
        private ProductRepositoryInterface $productRepository,
        private CouponRepositoryInterface $couponRepository
    ) {}

    /**
     * حساب إجمالي الطلب
     * Calculate order total
     */
    public function calculateOrderTotal(array $items, ?string $couponCode = null): array
    {
        // 1. حساب المجموع الفرعي
        // Calculate subtotal
        $subtotal = Money::zero();
        foreach ($items as $item) {
            $product = $this->productRepository->findById($item['product_id']);
            $lineTotal = $product->getPrice()->multiply($item['quantity']);
            $subtotal = $subtotal->add($lineTotal);
        }

        // 2. حساب الخصم
        // Calculate discount
        $discount = Money::zero();
        if ($couponCode) {
            $coupon = $this->couponRepository->findByCode($couponCode);
            if ($coupon && $coupon->isValid()) {
                $discount = $this->calculateDiscount($subtotal, $coupon);
            }
        }

        // 3. حساب الضريبة (15% ضريبة القيمة المضافة)
        // Calculate tax (15% VAT)
        $taxableAmount = $subtotal->subtract($discount);
        $tax = $taxableAmount->multiply(0.15);

        // 4. حساب رسوم الشحن
        // Calculate shipping fee
        $shippingFee = $this->calculateShippingFee($taxableAmount);

        // 5. الإجمالي النهائي
        // Final total
        $total = $subtotal
            ->subtract($discount)
            ->add($tax)
            ->add($shippingFee);

        return [
            'subtotal' => $subtotal,
            'discount' => $discount,
            'tax' => $tax,
            'shipping_fee' => $shippingFee,
            'total' => $total,
        ];
    }

    /**
     * حساب الخصم بناءً على نوع القسيمة
     * Calculate discount based on coupon type
     */
    private function calculateDiscount(Money $subtotal, Coupon $coupon): Money
    {
        if ($coupon->getType() === 'percentage') {
            $discount = $subtotal->multiply($coupon->getValue() / 100);
            
            // تطبيق الحد الأقصى للخصم
            // Apply maximum discount cap
            if ($coupon->getMaxDiscount() && $discount->isGreaterThan($coupon->getMaxDiscount())) {
                return $coupon->getMaxDiscount();
            }
            
            return $discount;
        }

        // خصم ثابت | Fixed discount
        return Money::fromFloat($coupon->getValue());
    }

    /**
     * حساب رسوم الشحن
     * Calculate shipping fee
     */
    private function calculateShippingFee(Money $orderAmount): Money
    {
        // شحن مجاني للطلبات فوق 200 ريال
        // Free shipping for orders above 200 SAR
        if ($orderAmount->getAmount() >= 200) {
            return Money::zero();
        }

        // رسوم شحن قياسية
        // Standard shipping fee
        return Money::fromFloat(20.00);
    }
}
```

---

## 4. طبقة Application | Application Layer {#application-layer}

### **4.1 Use Cases | حالات الاستخدام**

كل use case يمثل عملية واحدة في النظام.

```php
<?php

namespace App\Application\UseCases\Order;

use App\Domain\Entities\Order;
use App\Domain\Repositories\OrderRepositoryInterface;
use App\Domain\Repositories\CustomerRepositoryInterface;
use App\Domain\Services\PricingService;
use App\Domain\Services\InventoryService;
use App\Application\DTOs\CreateOrderDTO;
use App\Application\Events\OrderCreated;
use App\Domain\Exceptions\InsufficientStockException;
use App\Domain\Exceptions\CustomerNotFoundException;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Event;

/**
 * حالة استخدام: إنشاء طلب جديد
 * Use Case: Create New Order
 * 
 * المسؤولية الوحيدة: تنسيق عملية إنشاء الطلب
 * Single Responsibility: Orchestrate order creation process
 */
class CreateOrderUseCase
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private CustomerRepositoryInterface $customerRepository,
        private PricingService $pricingService,
        private InventoryService $inventoryService
    ) {}

    /**
     * تنفيذ حالة الاستخدام
     * Execute use case
     * 
     * @throws CustomerNotFoundException
     * @throws InsufficientStockException
     */
    public function execute(CreateOrderDTO $dto): Order
    {
        // 1. التحقق من وجود العميل
        // Verify customer exists
        $customer = $this->customerRepository->findById($dto->customerId);
        if (!$customer) {
            throw new CustomerNotFoundException("Customer {$dto->customerId} not found");
        }

        // 2. التحقق من توفر المخزون
        // Verify inventory availability
        $this->inventoryService->validateAvailability($dto->items);

        // 3. حساب الأسعار
        // Calculate pricing
        $pricing = $this->pricingService->calculateOrderTotal(
            $dto->items,
            $dto->couponCode
        );

        // 4. إنشاء الطلب في معاملة
        // Create order in transaction
        return DB::transaction(function () use ($dto, $pricing) {
            // إنشاء كيان الطلب
            // Create order entity
            $order = Order::create(
                orderNo: $this->generateOrderNumber(),
                customerId: $dto->customerId,
                total: $pricing['total'],
                status: OrderStatus::CREATED,
                createdAt: new \DateTimeImmutable()
            );

            // حفظ في قاعدة البيانات
            // Save to database
            $savedOrder = $this->orderRepository->save($order);

            // حجز المخزون
            // Reserve inventory
            $this->inventoryService->reserveStock($savedOrder->getId(), $dto->items);

            // إطلاق حدث إنشاء الطلب
            // Dispatch order created event
            Event::dispatch(new OrderCreated($savedOrder));

            return $savedOrder;
        });
    }

    /**
     * توليد رقم طلب فريد
     * Generate unique order number
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

### **4.2 Data Transfer Objects (DTOs) | كائنات نقل البيانات**

```php
<?php

namespace App\Application\DTOs;

/**
 * DTO لإنشاء طلب
 * Create Order DTO
 * 
 * Immutable object للنقل البيانات بين الطبقات
 * Immutable object for transferring data between layers
 */
final class CreateOrderDTO
{
    public function __construct(
        public readonly int $customerId,
        public readonly int $shippingAddressId,
        public readonly string $paymentMethod,
        public readonly array $items,
        public readonly ?string $couponCode = null,
        public readonly ?array $utmParams = null
    ) {
        $this->validate();
    }

    /**
     * إنشاء من مصفوفة
     * Create from array
     */
    public static function fromArray(array $data): self
    {
        return new self(
            customerId: $data['customer_id'],
            shippingAddressId: $data['shipping_address_id'],
            paymentMethod: $data['payment_method'],
            items: $data['items'],
            couponCode: $data['coupon_code'] ?? null,
            utmParams: [
                'source' => $data['utm_source'] ?? null,
                'medium' => $data['utm_medium'] ?? null,
                'campaign' => $data['utm_campaign'] ?? null,
            ]
        );
    }

    /**
     * التحقق من صحة البيانات
     * Validate data
     */
    private function validate(): void
    {
        if (empty($this->items)) {
            throw new \InvalidArgumentException('Order must have at least one item');
        }

        if (!in_array($this->paymentMethod, ['cod', 'online', 'wallet'])) {
            throw new \InvalidArgumentException('Invalid payment method');
        }

        foreach ($this->items as $item) {
            if (!isset($item['product_id'], $item['quantity'])) {
                throw new \InvalidArgumentException('Invalid item structure');
            }

            if ($item['quantity'] <= 0) {
                throw new \InvalidArgumentException('Item quantity must be positive');
            }
        }
    }

    /**
     * تحويل إلى مصفوفة
     * Convert to array
     */
    public function toArray(): array
    {
        return [
            'customer_id' => $this->customerId,
            'shipping_address_id' => $this->shippingAddressId,
            'payment_method' => $this->paymentMethod,
            'items' => $this->items,
            'coupon_code' => $this->couponCode,
            'utm_params' => $this->utmParams,
        ];
    }
}
```

---

## 5. طبقة Infrastructure | Infrastructure Layer {#infrastructure-layer}

### **5.1 Repository Implementation | تطبيق المستودع**

```php
<?php

namespace App\Infrastructure\Repositories;

use App\Domain\Entities\Order;
use App\Domain\Repositories\OrderRepositoryInterface;
use App\Domain\ValueObjects\Money;
use App\Models\Order as OrderModel;
use Illuminate\Support\Collection;

/**
 * تطبيق مستودع الطلبات باستخدام Eloquent
 * Eloquent Order Repository Implementation
 */
class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function save(Order $order): Order
    {
        $model = OrderModel::create([
            'order_no' => $order->getOrderNo(),
            'customer_id' => $order->getCustomerId(),
            'total' => $order->getTotal()->getAmount(),
            'currency' => $order->getTotal()->getCurrency(),
            'status' => $order->getStatus()->value,
            'created_at' => $order->getCreatedAt(),
        ]);

        return $this->toDomainEntity($model);
    }

    public function findById(int $id): ?Order
    {
        $model = OrderModel::find($id);
        
        return $model ? $this->toDomainEntity($model) : null;
    }

    public function findByOrderNo(string $orderNo): ?Order
    {
        $model = OrderModel::where('order_no', $orderNo)->first();
        
        return $model ? $this->toDomainEntity($model) : null;
    }

    public function findByCustomerId(int $customerId, int $limit = 20): Collection
    {
        return OrderModel::where('customer_id', $customerId)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get()
            ->map(fn($model) => $this->toDomainEntity($model));
    }

    public function findByStatus(string $status, int $limit = 100): Collection
    {
        return OrderModel::where('status', $status)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get()
            ->map(fn($model) => $this->toDomainEntity($model));
    }

    public function updateStatus(int $orderId, string $newStatus): bool
    {
        return OrderModel::where('id', $orderId)
            ->update(['status' => $newStatus]);
    }

    public function delete(int $orderId): bool
    {
        return OrderModel::where('id', $orderId)->delete();
    }

    public function getTodayTotalSales(): Money
    {
        $total = OrderModel::whereDate('created_at', today())
            ->where('status', 'delivered')
            ->sum('total');

        return Money::fromFloat($total);
    }

    public function getPendingOrders(): Collection
    {
        return OrderModel::whereIn('status', ['created', 'paid', 'confirmed'])
            ->orderBy('created_at', 'asc')
            ->get()
            ->map(fn($model) => $this->toDomainEntity($model));
    }

    /**
     * تحويل Eloquent Model إلى Domain Entity
     * Convert Eloquent Model to Domain Entity
     */
    private function toDomainEntity(OrderModel $model): Order
    {
        return new Order(
            id: $model->id,
            orderNo: $model->order_no,
            customerId: $model->customer_id,
            total: Money::fromFloat($model->total, $model->currency),
            status: OrderStatus::from($model->status),
            createdAt: new \DateTimeImmutable($model->created_at)
        );
    }
}
```

---

## 6. طبقة Presentation | Presentation Layer {#presentation-layer}

### **6.1 Controller | المتحكم**

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Application\UseCases\Order\CreateOrderUseCase;
use App\Application\DTOs\CreateOrderDTO;
use App\Http\Requests\CreateOrderRequest;
use App\Http\Resources\OrderResource;
use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;

/**
 * متحكم الطلبات
 * Order Controller
 * 
 * المسؤولية: معالجة HTTP requests وإرجاع HTTP responses
 * Responsibility: Handle HTTP requests and return HTTP responses
 */
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
            // 1. تحويل الطلب إلى DTO
            // Convert request to DTO
            $dto = CreateOrderDTO::fromArray([
                'customer_id' => $request->user()->id,
                ...$request->validated()
            ]);

            // 2. تنفيذ Use Case
            // Execute Use Case
            $order = $this->createOrderUseCase->execute($dto);

            // 3. إرجاع Resource
            // Return Resource
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

---

## 7. تدفق البيانات | Data Flow {#data-flow}

### **مثال: تدفق إنشاء طلب | Example: Order Creation Flow**

```
1. HTTP Request ──────────────────────────────────────┐
   POST /api/v1/orders                                │
   {                                                  │ Presentation
     "shipping_address_id": 1,                        │ Layer
     "payment_method": "cod",                         │
     "items": [...]                                   │
   }                                                  │
                                                      ↓
2. CreateOrderRequest ────────────────────────────────┐
   - Validation rules                                │ HTTP
   - Custom messages                                 │ Layer
   - Authorization                                   │
                                                      ↓
3. OrderController ───────────────────────────────────┐
   - Convert to DTO                                  │ Presentation
   - Call Use Case                                   │ Layer
   - Return Response                                 │
                                                      ↓
4. CreateOrderDTO ────────────────────────────────────┐
   - Immutable data object                           │ Application
   - Data validation                                 │ Layer
   - Type safety                                     │
                                                      ↓
5. CreateOrderUseCase ────────────────────────────────┐
   - Business workflow                               │ Application
   - Orchestration                                   │ Layer
   - Transaction management                          │
                                                      ↓
6. Domain Services ───────────────────────────────────┐
   - PricingService                                  │ Domain
   - InventoryService                                │ Layer
   - Business rules                                  │
                                                      ↓
7. Repository Interface ──────────────────────────────┐
   - OrderRepositoryInterface                        │ Domain
   - Abstract data access                            │ Layer
                                                      ↓
8. Repository Implementation ─────────────────────────┐
   - EloquentOrderRepository                         │ Infrastructure
   - Database operations                             │ Layer
   - Entity mapping                                  │
                                                      ↓
9. Database ──────────────────────────────────────────┐
   MySQL 8.x                                         │ Infrastructure
   - Orders table                                    │ Layer
   - Order items table                               │
   - Inventory ledger                                │
                                                      ↓
10. Events ───────────────────────────────────────────┐
    - OrderCreated event                             │ Application
    - Event listeners                                │ Layer
    - Background jobs                                │
```

---

## 8. أفضل الممارسات | Best Practices {#best-practices}

### **✅ Do's | افعل**

1. **استخدم Dependency Injection دائماً**
   ```php
   // ✅ Good
   public function __construct(
       private OrderRepositoryInterface $orderRepository
   ) {}
   
   // ❌ Bad
   public function getOrders() {
       $repository = new EloquentOrderRepository();
   }
   ```

2. **اجعل Value Objects غير قابلة للتغيير**
   ```php
   // ✅ Good
   final class Money {
       private function __construct(
           private readonly float $amount
       ) {}
   }
   
   // ❌ Bad
   class Money {
       public float $amount;
   }
   ```

3. **Use Cases تحتوي على منطق واحد فقط**
   ```php
   // ✅ Good
   class CreateOrderUseCase {}
   class CancelOrderUseCase {}
   
   // ❌ Bad
   class OrderUseCase {
       public function create() {}
       public function cancel() {}
       public function update() {}
   }
   ```

4. **استخدم DTOs للنقل البيانات بين الطبقات**
   ```php
   // ✅ Good
   $dto = CreateOrderDTO::fromArray($request->validated());
   $order = $this->createOrderUseCase->execute($dto);
   
   // ❌ Bad
   $order = $this->createOrderUseCase->execute(
       $request->customer_id,
       $request->items,
       $request->address_id
       // ... many parameters
   );
   ```

5. **اختبر كل طبقة بشكل مستقل**
   ```php
   // ✅ Good - Unit test for Use Case
   public function test_create_order_success()
   {
       $mockRepo = Mockery::mock(OrderRepositoryInterface::class);
       $useCase = new CreateOrderUseCase($mockRepo);
       // Test use case logic independently
   }
   ```

### **❌ Don'ts | لا تفعل**

1. **لا تضع منطق الأعمال في Controllers**
   ```php
   // ❌ Bad
   class OrderController {
       public function store(Request $request) {
           // Business logic in controller - WRONG!
           if ($inventory < $quantity) {
               throw new Exception('Out of stock');
           }
       }
   }
   ```

2. **لا تستخدم Eloquent في Domain Layer**
   ```php
   // ❌ Bad
   namespace App\Domain\Services;
   
   class OrderService {
       public function getOrders() {
           return Order::where('status', 'active')->get(); // WRONG!
       }
   }
   ```

3. **لا تخلط المسؤوليات**
   ```php
   // ❌ Bad
   class OrderService {
       public function createOrder() {
           // Create order
           // Send email
           // Update inventory
           // Process payment
           // Too many responsibilities!
       }
   }
   ```

4. **لا تعتمد الطبقات الداخلية على الخارجية**
   ```php
   // ❌ Bad - Domain depending on Infrastructure
   namespace App\Domain\Entities;
   
   use App\Infrastructure\Services\PaymentGateway;
   
   class Order {
       public function process(PaymentGateway $gateway) {} // WRONG!
   }
   ```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [ملحق د: أمثلة الكود | D. Code Examples](D_Code_Examples.md)
- [ملحق و: أفضل ممارسات Laravel | F. Laravel Best Practices](F_Laravel_Best_Practices.md)
- [ملحق ز: ميزات Laravel المتقدمة | G. Laravel Advanced Features](G_Laravel_Advanced_Features.md)
- [02. معمارية قاعدة البيانات | Database Architecture](../02_Database_Architecture.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ جاهز للإنتاج | Production Ready