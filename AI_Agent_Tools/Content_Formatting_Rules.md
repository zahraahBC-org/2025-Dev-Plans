# قواعد تنسيق المحتوى | Content Formatting Rules

**النوع | Type**: قواعد إلزامية | Mandatory Rules  
**النطاق | Scope**: جميع التوثيقات | All Documentation  
**التاريخ | Date**: 2025-10-20  
**الحالة | Status**: نشط | Active

---

## **نظرة عامة | Overview**

هذا المستند يحدد القواعد الإلزامية لتنسيق المحتوى في جميع التوثيقات، مع التركيز على:
1. استخدام Emojis بالحد الأدنى
2. أمثلة الكود المختصرة والمركزة
3. التنسيق المهني والنظيف

---

## **القسم 1: قواعد Emojis | Emoji Rules**

### **القاعدة الأساسية**

**استخدم emojis فقط عند الضرورة القصوى. حافظ على استخدام emojis بالحد الأدنى للحفاظ على معايير التوثيق المهنية.**

Use emojis sparingly and only when necessary for clarity or emphasis. Keep emoji usage to a minimum to maintain professional documentation standards.

---

### **الاستخدامات المسموحة | Allowed Uses**

#### **1. تحذيرات حرجة | Critical Warnings**
```markdown
## ⚠️ **مهم | Important**
⚠️ تنبيه: هذا إعداد حرج
```
**متى:** فقط للتحذيرات الحرجة التي تحتاج انتباه فوري

---

#### **2. أمثلة الكود التعليمية | Code Examples**
```php
// ✅ صحيح - Correct
$user = auth()->user();

// ❌ خطأ - Wrong
$user = User::first();
```
**متى:** للتمييز الواضح بين الممارسات الصحيحة والخاطئة في الكود

---

#### **3. جداول المقارنة | Comparison Tables**
```markdown
| Feature | Customer | Admin |
|---------|----------|-------|
| RBAC    | ❌ No    | ✅ Yes |
```
**متى:** كمؤشرات حالة في الجداول فقط

---

#### **4. مؤشرات التقييم | Rating Indicators**
```markdown
| التعقيد | عالي (⭐⭐⭐⭐⭐) | متوسط (⭐⭐⭐) |
```
**متى:** للتقييمات والتصنيفات النسبية

---

### **الاستخدامات الممنوعة | Prohibited Uses**

#### **❌ لا تستخدم emojis في:**

**1. Headers (العناوين):**
```markdown
❌ ## 📊 **الفرق عن الإصدار الأول**
✓ ## **الفرق عن الإصدار الأول**
```

**2. القوائم العادية:**
```markdown
❌ - ✅ معايير عامة
❌ - 📊 تقييم APIs
✓ - معايير عامة
✓ - تقييم APIs
```

**3. زخرفة المحتوى:**
```markdown
❌ تم الإنجاز! 🎉
❌ دليل شامل 📚
✓ تم الإنجاز
✓ دليل شامل
```

**4. الترقيم:**
```markdown
❌ 1️⃣ الخطوة الأولى
❌ 2️⃣ الخطوة الثانية
✓ 1. الخطوة الأولى
✓ 2. الخطوة الثانية
```

**5. مؤشرات الأولوية الملونة:**
```markdown
❌ ملفات حرجة 🔴
❌ ملفات مفيدة 🟡
✓ ملفات حرجة (أولوية عالية)
✓ ملفات مفيدة (أولوية متوسطة)
```

---

### **Checklist استخدام Emojis**

قبل إضافة emoji، اسأل:
- [ ] هل هذا تحذير حرج يحتاج انتباه فوري؟
- [ ] هل هذا في مثال كود تعليمي للتمييز بين صحيح/خطأ؟
- [ ] هل هذا مؤشر حالة في جدول مقارنة؟
- [ ] هل هذا مؤشر تقييم ضروري؟

إذا كانت الإجابة "لا" على جميع الأسئلة → **لا تستخدم emoji**

---

## **القسم 2: قواعد Code Snippets | Code Snippet Rules**

### **القاعدة الأساسية**

**استخدم فقط الأمثلة المختصرة الضرورية بدلاً من الكود الكامل. ركز على توضيح المفاهيم المحددة بكود مستهدف بدلاً من التطبيقات الكاملة.**

Use only necessary code snippets instead of full code examples. Focus on illustrating specific concepts with minimal, targeted code rather than complete implementations.

---

### **المبادئ | Principles**

#### **1. الحد الأدنى من الكود | Minimal Code**
- أظهر فقط الجزء الضروري لفهم المفهوم
- احذف الكود الزائد الذي لا يضيف قيمة تعليمية
- استخدم `// ...` للإشارة إلى الكود المحذوف

#### **2. التركيز على المفهوم | Focus on Concept**
- كل مثال يوضح فكرة واحدة فقط
- لا تخلط مفاهيم متعددة في مثال واحد
- أضف تعليقاً واضحاً يشرح الهدف

#### **3. تجنب التكرار | Avoid Repetition**
- لا تكرر نفس المثال في أماكن متعددة
- استخدم المراجع للأمثلة الموجودة
- ضع الأمثلة الطويلة في ملفات مرجعية منفصلة

---

### **حدود الأسطر | Line Limits**

| النوع | الأسطر | التقييم | الإجراء |
|-------|--------|---------|---------|
| **قصير** | 5-10 | مثالي | استخدمه |
| **متوسط** | 10-20 | مقبول | افحصه |
| **طويل** | 20-30 | راجعه | قد يحتاج تقسيم |
| **طويل جداً** | 30+ | ❌ غير مقبول | يجب تقليله |

---

### **أمثلة | Examples**

#### **❌ خطأ - كود كامل طويل (67 سطر):**

```php
<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Product;
use App\Http\Resources\ProductResource;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class ProductController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth:sanctum');
        $this->middleware('throttle:api');
    }
    
    public function index(Request $request)
    {
        $perPage = $request->input('per_page', 15);
        $sortBy = $request->input('sort_by', 'created_at');
        $sortOrder = $request->input('sort_order', 'desc');
        
        $products = Product::query()
            ->where('is_active', true)
            ->orderBy($sortBy, $sortOrder)
            ->paginate($perPage);
        
        return response()->json([
            'success' => true,
            'data' => ProductResource::collection($products),
            'meta' => [
                'current_page' => $products->currentPage(),
                'total' => $products->total(),
            ],
        ]);
    }
    // ... more methods
}
```

---

#### **✅ صحيح - أمثلة مختصرة مركزة:**

**مثال 1: هيكل Response (8 أسطر)**
```php
// مثال: هيكل Response موحد
public function index()
{
    return response()->json([
        'success' => true,
        'data' => Product::paginate(15),
    ]);
}
```

**مثال 2: Validation (6 أسطر)**
```php
// مثال: قواعد Validation
$request->validate([
    'name' => 'required|string|max:255',
    'price' => 'required|numeric|min:0',
]);
```

---

### **ما يجب حذفه | What to Remove**

```php
// ❌ احذف:
- namespace declarations (إلا إذا كان ضرورياً)
- use statements (إلا إذا كان غير واضح)
- __construct() methods
- Error handling التفصيلي
- Logging statements
- Middleware declarations
- Helper methods غير ضرورية
- Type declarations المفرطة

// ✅ أبقِ:
- الكود الأساسي للمفهوم
- التعليقات التوضيحية
- Structure الضروري فقط
- return statements
```

---

### **قوالب موصى بها | Recommended Templates**

#### **Controller Method:**
```php
// مثال: CRUD endpoint
public function store(Request $request)
{
    $data = $request->validate([...]);
    $resource = Model::create($data);
    
    return response()->json([
        'success' => true,
        'data' => new ResourceClass($resource),
    ], 201);
}
```

#### **Middleware:**
```php
// مثال: Custom middleware
public function handle($request, Closure $next)
{
    if (!$this->checkCondition($request)) {
        return response()->json(['message' => 'Forbidden'], 403);
    }
    
    return $next($request);
}
```

#### **Model Method:**
```php
// مثال: Relationship
public function orders()
{
    return $this->hasMany(Order::class);
}
```

---

### **Checklist مراجعة الكود | Code Review Checklist**

عند كتابة أو مراجعة مثال كود:

- [ ] المثال يوضح مفهوم واحد فقط
- [ ] عدد الأسطر < 20 (في الغالب)
- [ ] يوجد تعليق توضيحي (`// مثال: ...`)
- [ ] تم حذف الكود الزائد
- [ ] قابل للفهم بدون سياق إضافي
- [ ] لا يوجد تكرار مع أمثلة أخرى
- [ ] أسماء واضحة ومعبرة
- [ ] استخدام `// ...` للكود المحذوف

---

## **القسم 3: التطبيق العملي | Practical Application**

### **عند كتابة توثيق جديد:**

**1. التخطيط:**
- حدد المفاهيم الرئيسية التي تحتاج توضيح
- لكل مفهوم، خطط لمثال واحد مختصر
- تجنب الأمثلة الشاملة

**2. الكتابة:**
- ابدأ بأقل كود ممكن
- أضف سطر واحد في كل مرة إذا لزم الأمر
- توقف عند توضيح المفهوم

**3. المراجعة:**
- احذف أي سطر غير ضروري
- تحقق من Checklist
- قارن مع القوالب الموصى بها

---

### **عند مراجعة توثيق موجود:**

**تحديد الأولوية:**
1. الملفات مع متوسط >25 سطر/مثال (أولوية عالية)
2. الملفات مع متوسط 20-25 سطر/مثال (أولوية متوسطة)
3. الملفات مع متوسط <20 سطر/مثال (أولوية منخفضة)

**الإجراء:**
- راجع كل مثال كود بشكل فردي
- قسّم الأمثلة الطويلة (>30 سطر) إلى أمثلة متعددة
- احذف الكود الزائد من الأمثلة المتوسطة (20-30 سطر)

---

## **القسم 4: الأمثلة المقارنة | Before/After Examples**

### **مثال 1: Controller**

**❌ قبل (45 سطر):**
```php
namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Order;
use App\Http\Resources\OrderResource;
use Illuminate\Http\Request;

class OrderController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth:sanctum');
    }
    
    public function index(Request $request)
    {
        $customer = auth()->user();
        
        $query = $customer->orders();
        
        if ($request->has('status')) {
            $query->where('status', $request->status);
        }
        
        $orders = $query->orderBy('created_at', 'desc')
                       ->paginate(20);
        
        return response()->json([
            'success' => true,
            'data' => OrderResource::collection($orders),
            'meta' => [
                'current_page' => $orders->currentPage(),
                'per_page' => $orders->perPage(),
                'total' => $orders->total(),
            ],
        ]);
    }
}
```

**✅ بعد (8 أسطر):**
```php
// مثال: Customer orders endpoint
public function index()
{
    $orders = auth()->user()->orders()->paginate(20);
    
    return response()->json([
        'success' => true,
        'data' => OrderResource::collection($orders),
    ]);
}
```

---

### **مثال 2: Authentication**

**❌ قبل (35 سطر):**
```php
public function login(LoginRequest $request)
{
    $user = User::where('email', $request->email)->first();
    
    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json([
            'success' => false,
            'message' => 'بيانات الدخول غير صحيحة',
            'error_code' => 'INVALID_CREDENTIALS',
        ], 401);
    }
    
    if (!$user->is_active) {
        return response()->json([
            'success' => false,
            'message' => 'الحساب غير نشط',
            'error_code' => 'ACCOUNT_INACTIVE',
        ], 403);
    }
    
    $token = $user->createToken('mobile-app')->plainTextToken;
    
    activity()
        ->causedBy($user)
        ->log('User logged in');
    
    return response()->json([
        'success' => true,
        'message' => 'تم تسجيل الدخول بنجاح',
        'data' => [
            'user' => new UserResource($user),
            'token' => $token,
        ],
    ]);
}
```

**✅ بعد (12 سطر):**
```php
// مثال: Login endpoint
public function login(LoginRequest $request)
{
    $user = User::where('email', $request->email)->first();
    
    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json(['message' => 'بيانات خاطئة'], 401);
    }
    
    return response()->json([
        'user' => new UserResource($user),
        'token' => $user->createToken('app')->plainTextToken,
    ]);
}
```

---

### **مثال 3: Model**

**❌ قبل (25 سطر):**
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\SoftDeletes;

class Order extends Model
{
    use SoftDeletes;
    
    protected $fillable = [
        'customer_id',
        'total_amount',
        'status',
    ];
    
    protected $casts = [
        'total_amount' => 'decimal:2',
    ];
    
    public function customer(): BelongsTo
    {
        return $this->belongsTo(Customer::class);
    }
    
    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }
}
```

**✅ بعد (7 أسطر):**
```php
// مثال: Model relationships
class Order extends Model
{
    public function customer()
    {
        return $this->belongsTo(Customer::class);
    }
    
    public function items()
    {
        return $this->hasMany(OrderItem::class);
    }
}
```

---

## **القسم 5: إرشادات خاصة بالملفات | File-Specific Guidelines**

### **ملفات Reference:**
- يمكن أن تحتوي أمثلة أطول (20-30 سطر)
- لأنها مرجع شامل
- لكن يجب تقسيم الأمثلة الكبيرة

### **ملفات Implementation:**
- أمثلة قصيرة جداً (5-15 سطر)
- مركزة على الخطوة المحددة
- استخدم المراجع للتفاصيل

### **ملفات Quick Reference:**
- أمثلة قصيرة جداً (3-8 أسطر)
- فقط الأساسيات
- بدون شرح مطول

---

## **القسم 6: معايير الامتثال | Compliance Standards**

### **Emoji Compliance:**

**الهدف:**
- استخدام emojis الوظيفية فقط
- إزالة جميع emojis الزخرفية
- حد أقصى: 10-15 emoji لكل 1000 سطر

**التحقق:**
```bash
# عدد emojis الزخرفية يجب أن يكون = 0
grep -o '[🎯📊📁✨🔄🏗️📚➕🎓]' file.md | wc -l

# عدد emojis الوظيفية يجب أن يكون محدود
grep -o '[⚠️✅❌]' file.md | wc -l
```

---

### **Code Snippet Compliance:**

**الهدف:**
- متوسط 10-15 سطر لكل مثال كود
- أقصى 30 سطر للأمثلة الاستثنائية
- تعليقات واضحة لكل مثال

**التحقق:**
```python
# حساب متوسط أسطر أمثلة الكود
# الهدف: 10-15 سطر
# الحد الأقصى المقبول: 20 سطر
```

---

## **القسم 7: استثناءات | Exceptions**

### **متى يمكن استخدام أمثلة أطول:**

1. **Complete Template files** في 08-Reference/
2. **Integration examples** معقدة لا يمكن تبسيطها
3. **Migration scripts** أو Database schemas
4. **Configuration files** كاملة

**شرط:** يجب توضيح السبب في تعليق

```php
// ⚠️ مثال كامل: Template كامل للـController
// يمكن العثور على أمثلة مختصرة في الأقسام الأخرى
class CompleteTemplateController extends Controller
{
    // ... full implementation
}
```

---

## **القسم 8: أدوات المراجعة | Review Tools**

### **Manual Review:**
```bash
# عد أمثلة الكود في الملف
grep -c '```' file.md

# اعرض الأمثلة الطويلة
# (يدوياً - ابحث عن code blocks > 30 سطر)
```

### **Automated Checks:**
- استخدم scripts Python للتحليل الآلي
- ابحث عن patterns شائعة للكود الزائد
- راجع النتائج يدوياً

---

## **الخلاصة | Summary**

### **القواعد الأساسية:**

**Emojis:**
- ⚠️ فقط للتحذيرات الحرجة في Headers
- ✅❌ فقط في أمثلة الكود والجداول
- ⭐ فقط للتقييمات
- ❌ لا emojis زخرفية في أي مكان

**Code Snippets:**
- 10-15 سطر هو المثالي
- 20 سطر هو الحد المقبول
- 30+ سطر يجب تقليله
- استخدم `// ...` للكود المحذوف

**النتيجة:**
- توثيق مهني ونظيف
- أمثلة واضحة ومركزة
- صيانة أسهل
- تجربة قراءة أفضل

---

## **المراجع | References**

- `.cursorrules` - Content Quality Standards
- Repository: `/Users/ZahraahIT/Documents/Zahraah/2025-Plans`
- Related: `AI_Agent_Content_Management_Guide.md`

---

**آخر تحديث | Last Updated**: 2025-10-20  
**الحالة | Status**: نشط ومطلوب التطبيق | Active & Required  
**النطاق | Scope**: جميع التوثيقات | All Documentation  
**الأولوية | Priority**: إلزامي | Mandatory

