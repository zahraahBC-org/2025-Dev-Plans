# مفاتيح عدم التكرار — Idempotency Keys
**الأهمية | Importance**: 🔴 حرجة للعمليات المالية

---

## **ما هو Idempotency؟ | What is Idempotency?**

**التعريف:**
> ضمان أن تكرار نفس الطلب عدة مرات ينتج نفس النتيجة بدون آثار جانبية إضافية.

### **المشكلة:**

**Scenario 1:**
```
المستخدم ينقر "أطلب" → الشبكة بطيئة → ينقر مرة أخرى
                                    ↓
                              طلبان بدل واحد!
```

**Scenario 2:**
```
المستخدم يدفع COD → timeout → يعيد المحاولة
                          ↓
                    دفعتان بدل واحدة!
```

### **الحل: Idempotency-Key**

**With Idempotency Key:**
- الطلب 1: `POST /orders + Idempotency-Key: abc-123` → Order #1
- الطلب 2: `POST /orders + Idempotency-Key: abc-123` → Order #1 (نفسه)
- الطلب 3: `POST /orders + Idempotency-Key: abc-123` → Order #1 (نفسه)

**النتيجة:** طلب واحد فقط بغض النظر عن عدد المحاولات

---

## **متى نستخدمه؟ | When to Use?**

### **إلزامي لـ:**

- **إنشاء طلبات** (Orders)
- **معاملات دفع** (Payments, COD confirmation)
- **استرداد** (Refunds)
- **تفعيل قسائم** (Coupon redemption)
- **أي POST يؤثر مالياً أو حساساً**

### **غير ضروري لـ:**

- GET (قراءة فقط)
- DELETE (idempotent بطبيعته)
- PUT (idempotent بطبيعته)
- عمليات بسيطة غير مالية

---

## **التنفيذ العملي | Implementation**

### **1. Database Schema**

```php
// Refer to Database plan for full schema
// database/migrations/create_idempotency_keys_table.php
Schema::create('idempotency_keys', function (Blueprint $table) {
    $table->id();
    $table->string('key', 64)->unique();           // الـkey الفريد
    $table->foreignId('user_id')->nullable()
        ->constrained()->onDelete('cascade');
    $table->enum('status', ['processing', 'completed', 'failed'])
        ->default('processing');
    $table->timestamp('expires_at');
    // ... other columns - see Database plan
    $table->timestamps();
});
```

---

### **2. Model Example**

```php
class IdempotencyKey extends Model
{
    protected $fillable = ['key', 'user_id', 'fingerprint', 'response_body', 'status', 'expires_at'];
    protected $casts = ['response_body' => 'array', 'expires_at' => 'datetime'];
    
    public function isProcessing(): bool { return $this->status === 'processing'; }
    public function isCompleted(): bool { return $this->status === 'completed'; }
}
```

---

### **3. Service Layer Example**

```php
class IdempotencyService
{
    public function check(Request $request): ?IdempotencyKey
    {
        return IdempotencyKey::where('key', $request->header('Idempotency-Key'))
            ->where('user_id', auth()->id())
            ->where('expires_at', '>', now())
            ->first();
    }
    
    public function create(Request $request): IdempotencyKey
    {
        return IdempotencyKey::create([
            'key' => $request->header('Idempotency-Key'),
            'user_id' => auth()->id(),
            'fingerprint' => $this->generateFingerprint($request),
            'status' => 'processing',
            'expires_at' => now()->addHours(24),
        ]);
    }
    
    private function generateFingerprint(Request $request): string
    {
        return hash('sha256', json_encode([
            'method' => $request->method(),
            'body' => $request->all(),
            'user_id' => auth()->id(),
        ]));
    }
}
```

---

### **4. Middleware Example**

```php
class CheckIdempotency
{
    public function handle(Request $request, Closure $next)
    {
        if ($request->method() !== 'POST') {
            return $next($request);
        }
        
        if (!$request->header('Idempotency-Key')) {
            return response()->json(['error_code' => 'IDEMPOTENCY_KEY_REQUIRED'], 400);
        }
        
        $existing = $this->service->check($request);
        
        if ($existing && $existing->isCompleted()) {
            // Return cached response
            return response()
                ->json($existing->response_body, $existing->response_code)
                ->header('Idempotent-Replayed', 'true');
        }
        
        if ($existing && $existing->isProcessing()) {
            return response()->json(['error_code' => 'REQUEST_PROCESSING'], 409);
        }
        
        // Create new record
        $record = $this->service->create($request);
        $request->attributes->set('idempotency_record', $record);
        
        return $next($request);
    }
}
```

---

### **5. Controller Usage**

```php
public function store(StoreOrderRequest $request)
{
    $idempotencyRecord = $request->attributes->get('idempotency_record');
    
    try {
        $order = DB::transaction(fn() => $this->orderService->createOrder($request->validated()));
        
        $responseData = ['success' => true, 'data' => new OrderResource($order)];
        
        // Store response for future replays
        if ($idempotencyRecord) {
            $this->idempotencyService->storeResponse($idempotencyRecord, 201, $responseData);
        }
        
        return response()->json($responseData, 201);
        
    } catch (\Exception $e) {
        $idempotencyRecord?->update(['status' => 'failed']);
        throw $e;
    }
}
```

---

### **6. Routes**

```php
// routes/api.php
Route::middleware(['auth:sanctum', 'throttle:api'])
    ->prefix('v1')
    ->group(function () {
        
        // Endpoints تتطلب Idempotency
        Route::middleware(['check.idempotency'])->group(function () {
            Route::post('/orders', [OrderController::class, 'store']);
            Route::post('/payments', [PaymentController::class, 'process']);
            Route::post('/refunds', [RefundController::class, 'create']);
        });
    });
```

---

## **الاستخدام من Client (Flutter/Mobile)**

### **إنشاء Idempotency-Key:**

```dart
// Flutter Example
import 'package:uuid/uuid.dart';

class ApiService {
  final Uuid _uuid = Uuid();
  
  Future<Order> createOrder(OrderData data) async {
    // Generate unique key
    final idempotencyKey = _uuid.v4();
    
    final response = await http.post(
      Uri.parse('$baseUrl/api/v1/orders'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey,
      },
      body: jsonEncode(data.toJson()),
    );
    
    if (response.statusCode == 201) {
      // Success
      return Order.fromJson(jsonDecode(response.body)['data']);
    } else if (response.statusCode == 409) {
      // Already processing or conflict
      throw IdempotencyConflictException();
    }
    
    throw ApiException(response.body);
  }
}
```

---

## **سيناريوهات الاستخدام | Use Case Scenarios**

### **السيناريو 1: طلب جديد**

```
Request 1:
POST /api/v1/orders
Idempotency-Key: abc-123
Body: { cart_id: 1, address_id: 5 }

Response 1:
201 Created
Idempotent-Replayed: false
{ order_id: "ORD-001", ... }

✅ تم إنشاء الطلب
```

---

### **السيناريو 2: إعادة نفس الطلب (شبكة بطيئة)**

```
Request 2 (Same):
POST /api/v1/orders
Idempotency-Key: abc-123
Body: { cart_id: 1, address_id: 5 }

Response 2:
201 Created
Idempotent-Replayed: true
{ order_id: "ORD-001", ... }  // نفس الرد!

✅ لم يُنشأ طلب جديد
✅ تم إرجاع نفس الطلب
```

---

### **السيناريو 3: نفس المفتاح لكن بيانات مختلفة**

```
Request 3:
POST /api/v1/orders
Idempotency-Key: abc-123
Body: { cart_id: 2, address_id: 8 }  // بيانات مختلفة!

Response 3:
409 Conflict
{
  "success": false,
  "message": "Idempotency-Key مستخدم لطلب مختلف",
  "error_code": "IDEMPOTENCY_KEY_MISMATCH"
}

❌ تم رفض الطلب
```

---

### **السيناريو 4: الطلب قيد المعالجة**

```
Request 1: POST /orders + Key: xyz-789 → قيد المعالجة...
Request 2: POST /orders + Key: xyz-789 (قبل انتهاء الأول)

Response:
409 Conflict
{
  "success": false,
  "message": "الطلب قيد المعالجة، يرجى الانتظار",
  "error_code": "REQUEST_PROCESSING"
}
```

---

## **Best Practices**

### **1. Key Generation**

```dart
// ✅ Client generates unique key
import 'package:uuid/uuid.dart';

final key = Uuid().v4(); // abc-123-def-456...

// ❌ DON'T use predictable keys
final key = DateTime.now().toString(); // ❌
final key = userId + timestamp; // ❌
```

---

### **2. Key Storage على Client**

```dart
// ✅ Store key مع الطلب
class PendingOrder {
  String idempotencyKey;
  OrderData data;
  DateTime createdAt;
  
  // حفظ في local DB
  Future<void> save() async {
    await db.insert('pending_orders', {
      'idempotency_key': idempotencyKey,
      'data': jsonEncode(data),
    });
  }
  
  // إعادة المحاولة بنفس المفتاح
  Future<void> retry() async {
    await createOrder(data, idempotencyKey: this.idempotencyKey);
  }
}
```

---

### **3. TTL (Time To Live)**

```php
// التوصيات:
$ttl = [
    'orders' => 72,      // 72 ساعة (3 أيام)
    'payments' => 24,    // 24 ساعة (يوم واحد)
    'refunds' => 168,    // 7 أيام
];

// في Service
'expires_at' => now()->addHours($ttl['orders']),
```

**القواعد:**
```
✅ طويل بما يكفي للإعادة المشروعة
✅ قصير بما يكفي لعدم استهلاك التخزين
✅ حسب طبيعة العملية
```

---

### **4. Fingerprint Validation**

```php
private function generateFingerprint(Request $request): string
{
    // يشمل كل ما يحدد فرادة الطلب
    $data = [
        'method' => $request->method(),
        'path' => $request->path(),
        'body' => $request->all(),      // كل البيانات
        'user_id' => auth()->id(),
    ];
    
    // ترتيب ثابت
    ksort($data['body']);
    
    return hash('sha256', json_encode($data));
}
```

---

## **Cleanup Example**

```php
// Cleanup Command
class CleanupExpiredIdempotencyKeys extends Command
{
    public function handle(): int
    {
        $deleted = IdempotencyKey::where('expires_at', '<', now())->delete();
        $this->info("Deleted {$deleted} expired keys");
        return 0;
    }
}

// Schedule (Kernel.php)
$schedule->command('idempotency:cleanup')->dailyAt('02:00');
```

---

## **Testing Examples**

```php
public function test_creates_order_with_idempotency_key(): void
{
    $response = $this->actingAs($user, 'sanctum')
        ->withHeader('Idempotency-Key', 'test-key-123')
        ->postJson('/api/v1/orders', ['cart_id' => 1]);
    
    $response->assertStatus(201)->assertHeader('Idempotent-Replayed', 'false');
    $this->assertDatabaseHas('idempotency_keys', ['key' => 'test-key-123', 'status' => 'completed']);
}

public function test_returns_same_response_for_duplicate_request(): void
{
    $key = 'test-key-456';
    
    // First request
    $response1 = $this->withHeader('Idempotency-Key', $key)
        ->postJson('/api/v1/orders', ['cart_id' => 1]);
    
    // Duplicate request
    $response2 = $this->withHeader('Idempotency-Key', $key)
        ->postJson('/api/v1/orders', ['cart_id' => 1]);
    
    $this->assertEquals($response1->json('data.id'), $response2->json('data.id'));
    $response2->assertHeader('Idempotent-Replayed', 'true');
    $this->assertDatabaseCount('orders', 1);  // Only one order created
}
```

---

## **Checklist التنفيذ**

### **Database:**
- [ ] جدول idempotency_keys
- [ ] Indexes (key, user_id, expires_at)
- [ ] Migration منفذة

### **Models:**
- [ ] IdempotencyKey model
- [ ] Relationships
- [ ] Helper methods

### **Service:**
- [ ] IdempotencyService
- [ ] check() method
- [ ] create() method
- [ ] storeResponse() method
- [ ] generateFingerprint() method

### **Middleware:**
- [ ] CheckIdempotency middleware
- [ ] مسجل في Kernel
- [ ] مطبق على routes الحساسة

### **Cleanup:**
- [ ] Cleanup command
- [ ] مجدول (daily)

### **Testing:**
- [ ] New request test
- [ ] Duplicate request test
- [ ] Mismatch test
- [ ] Required key test

---

## **Best Practices Summary**

### ** DO:**
- استخدم UUIDv4 للـkeys
- احفظ الـkey على client
- تحقق من fingerprint
- خزّن الرد كاملاً
- نظّف المفاتيح المنتهية

### ** DON'T:**
- استخدام keys متوقعة
- مفاتيح بدون expiration
- تجاهل fingerprint
- نفس key لطلبات مختلفة

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
