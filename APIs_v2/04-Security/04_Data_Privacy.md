# الخصوصية وحماية البيانات — Data Privacy & Protection
**الأهمية | Importance**: 🔴 حرجة - إلزامية قانونياً

---

## **الهدف | Objective**

ضمان حماية بيانات المستخدمين والامتثال للمتطلبات القانونية (GDPR، قوانين حماية البيانات).

---

## **المبادئ الأساسية | Core Principles**

### **1. Data Minimization | تقليل البيانات**

**Principles:**
- اجمع فقط ما تحتاجه
- لا تطلب بيانات زائدة
- احذف ما لم تعد تحتاجه

**Example:**
- **DON'T:** طلب رقم الهوية لإنشاء حساب
- **DO:** طلب اسم وبريد فقط

---

### **2. Privacy by Design | الخصوصية بالتصميم**

```
✅ تشفير البيانات الحساسة
✅ إخفاء PII في logs
✅ التحكم في الوصول (RBAC)
✅ Audit logs لكل عملية
```

---

## **أنواع البيانات | Data Classification**

### **التصنيف:**

| المستوى | أمثلة | المعالجة |
|---------|-------|----------|
| **Public** | أسماء منتجات، فئات | عام، يمكن cache |
| **Internal** | Order IDs، statistics | داخلي فقط |
| **Confidential** | بريد، هاتف، عنوان | تشفير، محدود الوصول |
| **Restricted** | كلمة مرور، بيانات دفع | تشفير قوي، audit |

---

## **PII Handling | معالجة البيانات الشخصية**

### **ما هو PII؟**

**Personally Identifiable Information:**
- الاسم الكامل
- البريد الإلكتروني
- رقم الهاتف
- العنوان
- IP Address
- رقم الهوية
- بيانات البطاقة

---

### **الحماية المطلوبة:**

#### **1. التشفير | Encryption**

```php
// At Rest (في قاعدة البيانات)
// Refer to Database plan for full schema

// في Model
class User extends Model
{
    protected $casts = [
        'phone' => 'encrypted',
        'address' => 'encrypted',
    ];
}

// In Transit (أثناء النقل)
// HTTPS فقط - لا HTTP أبداً
```

---

#### **2. Masking | الإخفاء**

```php
// في اللوغ - لا تسجل PII
Log::info('User registered', [
    'user_id' => $user->id,  // ✅ ID فقط
    // ❌ لا email, phone, name
]);

// في Admin Panel - إخفاء جزئي
public function getMaskedPhoneAttribute(): string
{
    // 05XXXXXXX12
    return substr($this->phone, 0, 2) . 'XXXXXX' . substr($this->phone, -2);
}

// في Error messages - لا PII
return response()->json([
    'message' => 'بيانات غير صالحة',
    // ❌ لا 'Email john@example.com already exists'
]);
```

---

#### **3. Access Control | التحكم في الوصول**

```php
// فقط المخول يمكنه رؤية PII
class UserPolicy
{
    public function viewSensitiveData(User $viewer, User $target): bool
    {
        // نفس المستخدم أو admin
        return $viewer->id === $target->id 
            || $viewer->hasRole('admin');
    }
}

// في Resource
class UserResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            
            // PII فقط للمخول
            'email' => $this->when(
                $request->user()->can('viewSensitiveData', $this->resource),
                $this->email
            ),
            
            'phone' => $this->when(
                $request->user()->can('viewSensitiveData', $this->resource),
                $this->phone
            ),
        ];
    }
}
```

---

## **Data Retention | الاحتفاظ بالبيانات**

### **Retention Policies | سياسات الاحتفاظ**

```php
// config/data-retention.php
return [
    'users' => [
        'inactive_account' => 365,     // حذف بعد سنة من عدم النشاط
        'deleted_account' => 30,       // حذف نهائي بعد 30 يوم من الحذف
    ],
    'orders' => [
        'completed' => 1825,           // 5 سنوات (متطلبات محاسبية)
        'cancelled' => 365,            // سنة واحدة
    ],
    'logs' => [
        'api_logs' => 90,              // 3 أشهر
        'security_logs' => 365,        // سنة
    ],
];
```

---

### **Auto-deletion Command:**

```php
// app/Console/Commands/ApplyDataRetention.php
class ApplyDataRetention extends Command
{
    protected $signature = 'data:retention';
    
    public function handle(): int
    {
        // Soft-deleted users (بعد 30 يوم)
        User::onlyTrashed()
            ->where('deleted_at', '<', now()->subDays(30))
            ->forceDelete();
        
        // Inactive users (بعد سنة)
        User::where('last_login_at', '<', now()->subYear())
            ->where('is_active', false)
            ->delete();
        
        // Old logs
        DB::table('activity_log')
            ->where('created_at', '<', now()->subDays(90))
            ->delete();
        
        return 0;
    }
}
```

---

## ️ **Right to Erasure | حق النسيان**

### **GDPR Article 17 - حق الحذف**

```php
// app/Services/DataErasureService.php
namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\DB;

class DataErasureService
{
    /**
     * Anonymize user data (GDPR compliant)
     */
    public function anonymizeUser(User $user): void
    {
        DB::transaction(function () use ($user) {
            // Anonymize PII
            $user->update([
                'name' => 'User-' . $user->id,
                'email' => 'deleted-' . $user->id . '@example.com',
                'phone' => null,
                'address' => null,
                'deleted_at' => now(),
            ]);
            
            // Anonymize related data
            $user->addresses()->delete();
            $user->tokens()->delete();
            
            // Keep orders لكن anonymize
            $user->orders()->update([
                'customer_name' => 'مستخدم محذوف',
                'customer_email' => null,
                'customer_phone' => null,
            ]);
            
            // Log erasure
            activity()
                ->causedBy($user)
                ->log('User data anonymized (GDPR)');
        });
    }
    
    /**
     * Complete data deletion
     */
    public function completeErasure(User $user): void
    {
        DB::transaction(function () use ($user) {
            // حذف كل شيء
            $user->orders()->delete();
            $user->reviews()->delete();
            $user->addresses()->delete();
            $user->forceDelete();
        });
    }
}
```

---

### **API Endpoint:**

```php
// Request account deletion (30-day grace period)
public function requestDeletion(Request $request)
{
    $deletion = DeletionRequest::create([
        'user_id' => $request->user()->id,
        'scheduled_at' => now()->addDays(30),
    ]);
    
    Mail::to($request->user())->send(new DeletionRequestedMail($deletion));
    
    return response()->json([
        'message' => 'سيتم الحذف خلال 30 يوماً',
        'scheduled_at' => $deletion->scheduled_at,
    ]);
}

// Cancel deletion request
public function cancelDeletion($deletionId)
{
    DeletionRequest::findOrFail($deletionId)->update(['status' => 'cancelled']);
    return response()->json(['message' => 'تم الإلغاء']);
}
```

---

## **Consent Management | إدارة الموافقات**

### **Database Schema:**

```php
// Refer to Database plan for full schema
Schema::create('user_consents', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('consent_type');  // 'marketing', 'analytics', 'push'
    $table->boolean('granted')->default(false);
    // ... other columns - see Database plan
    $table->timestamps();
});
```

---

### **Model:**

```php
class UserConsent extends Model
{
    protected $fillable = [
        'user_id',
        'consent_type',
        'granted',
        'granted_at',
        'ip_address',
    ];
    
    protected $casts = [
        'granted' => 'boolean',
        'granted_at' => 'datetime',
        'revoked_at' => 'datetime',
    ];
}
```

---

### **API Endpoints:**

```php
// Update consents
public function updateConsents(Request $request)
{
    $request->validate([
        'marketing' => 'required|boolean',
        'analytics' => 'required|boolean',
        'push_notifications' => 'required|boolean',
    ]);
    
    $user = $request->user();
    
    foreach ($request->only(['marketing', 'analytics', 'push_notifications']) as $type => $granted) {
        $user->consents()->updateOrCreate(
            ['consent_type' => $type],
            [
                'granted' => $granted,
                'granted_at' => $granted ? now() : null,
                'revoked_at' => !$granted ? now() : null,
                'ip_address' => $request->ip(),
            ]
        );
    }
    
    return response()->json([
        'success' => true,
        'message' => 'تم تحديث الموافقات بنجاح',
    ]);
}

// Get consents
public function getConsents(Request $request)
{
    $consents = $request->user()
        ->consents()
        ->pluck('granted', 'consent_type');
    
    return response()->json([
        'success' => true,
        'data' => [
            'marketing' => $consents['marketing'] ?? false,
            'analytics' => $consents['analytics'] ?? false,
            'push_notifications' => $consents['push_notifications'] ?? false,
        ],
    ]);
}
```

---

## **Encryption Standards**

### **At Rest (قاعدة البيانات):**

```php
// Laravel Encryption
class User extends Model
{
    protected $casts = [
        'phone' => 'encrypted',
        'national_id' => 'encrypted',
        'address' => 'encrypted',
    ];
}

// Database encryption (MySQL)
// يُفضل تشفير الـdatabase بالكامل - see Database plan
```

---

### **In Transit (أثناء النقل):**

**Requirements:**
- HTTPS فقط (TLS 1.2+)
- لا HTTP أبداً في production
- Certificate valid ومحدث

---

### **In Memory (في الذاكرة):**

```php
// تنظيف الذاكرة بعد الاستخدام
try {
    $sensitiveData = decrypt($encrypted);
    // Use data
} finally {
    unset($sensitiveData);  // Clear من memory
}
```

---

## **Audit Logging | سجلات التدقيق**

### **ما يجب تسجيله:**

```php
// Audit logging for sensitive data access
class User extends Model
{
    use LogsActivity;
    
    protected static $logAttributes = ['email', 'phone', 'is_active'];
    protected static $logOnlyDirty = true;
    
    // Log when PII is accessed by other users
    protected static function boot()
    {
        parent::boot();
        static::retrieved(fn($user) => 
            activity()->log('Accessed user PII')
        );
    }
}
```

---

### **Activity Log Schema:**

```php
// Refer to Database plan for full schema
Schema::create('activity_log', function (Blueprint $table) {
    $table->id();
    $table->text('description');
    $table->nullableMorphs('subject', 'subject');
    $table->nullableMorphs('causer', 'causer');
    // ... other columns - see Database plan
    $table->timestamps();
});
```

---

## **ما لا يجب فعله | What NOT to Do**

### ** في Logs:**

```php
// ❌ خطأ - تسجيل PII
Log::info('User logged in', [
    'email' => $user->email,        // ❌
    'phone' => $user->phone,        // ❌
    'ip' => $request->ip(),         // ⚠️ PII في بعض القوانين
]);

// ✅ صحيح
Log::info('User logged in', [
    'user_id' => $user->id,         // ✅ ID فقط
    'timestamp' => now(),           // ✅
]);
```

---

### ** في Error Messages:**

```php
// ❌ خطأ
return response()->json([
    'message' => "User with email {$email} already exists",
]);

// ✅ صحيح
return response()->json([
    'message' => 'البريد الإلكتروني موجود مسبقاً',
    'error_code' => 'EMAIL_EXISTS',
]);
```

---

### ** في Analytics:**

```php
// ❌ خطأ
Analytics::track('Purchase', [
    'user_email' => $user->email,   // ❌
    'user_phone' => $user->phone,   // ❌
]);

// ✅ صحيح
Analytics::track('Purchase', [
    'user_id' => $user->id,         // ✅ pseudonymized
    'amount' => $order->total,
]);
```

---

## **GDPR Compliance Checklist**

### **حقوق المستخدم:**

| الحق | التطبيق | الـAPI |
|------|---------|-------|
| **Right to Access** | تصدير البيانات | GET /me/data-export |
| **Right to Rectification** | تعديل البيانات | PATCH /me/profile |
| **Right to Erasure** | حذف/إخفاء البيانات | DELETE /me/account |
| **Right to Restrict** | إيقاف المعالجة | PATCH /me/consents |
| **Right to Portability** | تصدير بصيغة قياسية | GET /me/data-export?format=json |

---

### **API Endpoints للـGDPR:**

```php
// تصدير البيانات
public function exportData(Request $request)
{
    $user = $request->user();
    
    $data = [
        'personal_info' => [
            'name' => $user->name,
            'email' => $user->email,
            'phone' => $user->phone,
            'created_at' => $user->created_at,
        ],
        'orders' => $user->orders()->get(),
        'addresses' => $user->addresses()->get(),
        'reviews' => $user->reviews()->get(),
    ];
    
    return response()->json([
        'success' => true,
        'data' => $data,
    ])->header('Content-Disposition', 'attachment; filename=user-data.json');
}

// حذف الحساب
public function deleteAccount(DeleteAccountRequest $request)
{
    $user = $request->user();
    
    // Verify password
    if (!Hash::check($request->password, $user->password)) {
        return response()->json([
            'success' => false,
            'message' => 'كلمة المرور غير صحيحة',
        ], 403);
    }
    
    // Create deletion request
    app(DataErasureService::class)->requestDeletion($user);
    
    return response()->json([
        'success' => true,
        'message' => 'سيتم حذف حسابك خلال 30 يوماً',
    ]);
}
```

---

## **Security Best Practices**

### **1. لا تُسرّب PII:**

```php
// ✅ صحيح - responses آمنة
return response()->json([
    'success' => false,
    'message' => 'بيانات غير صالحة',
]);

// ❌ خطأ - تسريب PII
return response()->json([
    'message' => "User {$email} not found",
]);
```

---

### **2. Sanitize قبل التخزين:**

```php
use Illuminate\Support\Str;

$user->name = Str::of($request->name)
    ->trim()
    ->limit(255)
    ->stripTags()
    ->value();
```

---

### **3. Rate Limiting على PII:**

```php
// حماية endpoints الحساسة
Route::middleware(['throttle:sensitive'])->group(function () {
    Route::get('/me/data-export', [UserController::class, 'exportData']);
    Route::delete('/me/account', [UserController::class, 'deleteAccount']);
});

// في RouteServiceProvider
RateLimiter::for('sensitive', function (Request $request) {
    return Limit::perDay(5)->by($request->user()->id);
});
```

---

## **Privacy Policy API**

### **عرض سياسة الخصوصية:**

```php
public function privacyPolicy()
{
    return response()->json([
        'success' => true,
        'data' => [
            'version' => '1.0',
            'last_updated' => '2025-10-19',
            'url' => 'https://example.com/privacy',
            'sections' => [
                'data_collection' => 'ما البيانات التي نجمعها',
                'data_usage' => 'كيف نستخدم البيانات',
                'data_sharing' => 'مع من نشارك البيانات',
                'user_rights' => 'حقوقك',
                'contact' => 'كيف تتواصل معنا',
            ],
        ],
    ]);
}
```

---

## **Testing Privacy**

```php
class PrivacyTest extends TestCase
{
    public function test_pii_not_in_logs(): void
    {
        Log::shouldReceive('info')
            ->once()
            ->withArgs(function ($message, $context) {
                // تأكد أن الـcontext لا يحتوي email أو phone
                return !isset($context['email']) 
                    && !isset($context['phone']);
            });
        
        $this->postJson('/api/v1/register', [
            'email' => 'test@example.com',
            'phone' => '0501234567',
        ]);
    }
    
    public function test_user_can_export_data(): void
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user, 'sanctum')
            ->getJson('/api/v1/me/data-export');
        
        $response->assertStatus(200)
            ->assertJsonStructure([
                'data' => [
                    'personal_info',
                    'orders',
                    'addresses',
                ],
            ]);
    }
    
    public function test_user_can_request_deletion(): void
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user, 'sanctum')
            ->deleteJson('/api/v1/me/account', [
                'password' => 'password',
            ]);
        
        $response->assertStatus(200);
        
        $this->assertDatabaseHas('deletion_requests', [
            'user_id' => $user->id,
            'status' => 'pending',
        ]);
    }
}
```

---

## **Checklist الامتثال | Compliance Checklist**

### **GDPR/Privacy:**
- [ ] PII encrypted at rest
- [ ] HTTPS only (TLS 1.2+)
- [ ] PII masked في logs
- [ ] PII masked في admin panel
- [ ] Access control (RBAC)
- [ ] Audit logging لـPII access

### **User Rights:**
- [ ] Right to access (data export)
- [ ] Right to rectification (update profile)
- [ ] Right to erasure (delete account)
- [ ] Right to restrict (consents)
- [ ] Right to portability (JSON export)

### **Retention:**
- [ ] Retention policies محددة
- [ ] Auto-deletion مجدول
- [ ] Soft delete أولاً (grace period)
- [ ] Force delete بعد الفترة

### **Consents:**
- [ ] Consent management API
- [ ] Opt-in/opt-out واضح
- [ ] Audit trail للموافقات
- [ ] Respect consents في التطبيق

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
