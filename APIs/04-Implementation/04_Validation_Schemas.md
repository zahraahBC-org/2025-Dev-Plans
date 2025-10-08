# 04. التحقق والمخططات | Validation & Schemas

## 🎯 **نظرة عامة | Overview**

معايير التحقق من البيانات والمخططات لضمان جودة وسلامة البيانات المتبادلة.

**الهدف | Purpose**: تطبيق تحقق شامل للبيانات  
**الجمهور | Audience**: مطورو Backend  
**المتطلبات | Prerequisites**: فهم [معالجة الأخطاء](01_Response_Error_Handling.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [JSON Schema](#json-schema)
2. [أنواع البيانات](#أنواع-البيانات)
3. [قواعد التحقق](#قواعد-التحقق)
4. [التحقق في Laravel](#التحقق-في-laravel)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ JSON Schema {#json-schema}

### **مثال Schema كامل**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateOrderRequest",
  "type": "object",
  "required": ["customer_id", "items", "shipping_address_id", "payment_method"],
  "properties": {
    "customer_id": {
      "type": "integer",
      "minimum": 1,
      "description": "معرف العميل"
    },
    "items": {
      "type": "array",
      "minItems": 1,
      "maxItems": 50,
      "items": {
        "type": "object",
        "required": ["variant_id", "quantity"],
        "properties": {
          "variant_id": {
            "type": "integer",
            "minimum": 1
          },
          "quantity": {
            "type": "integer",
            "minimum": 1,
            "maximum": 99
          }
        }
      }
    },
    "shipping_address_id": {
      "type": "integer",
      "minimum": 1
    },
    "payment_method": {
      "type": "string",
      "enum": ["cod", "online", "wallet"]
    },
    "note": {
      "type": "string",
      "maxLength": 500
    },
    "coupon_code": {
      "type": "string",
      "pattern": "^[A-Z0-9]{6,12}$"
    }
  },
  "additionalProperties": false
}
```

---

## 2️⃣ أنواع البيانات | Data Types {#أنواع-البيانات}

### **التواريخ والأوقات**

#### **✅ التنسيق الصحيح: ISO-8601 UTC**
```json
{
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T13:30:45.123Z",
  "delivery_date": "2025-01-10"
}
```

#### **❌ تنسيقات خاطئة**
```json
{
  "created_at": "08/01/2025",           // ممنوع
  "updated_at": "2025-01-08 12:00:00",  // ممنوع
  "delivery_date": "10-01-2025"         // ممنوع
}
```

**قواعد**:
- ✅ دائمًا UTC (Z في النهاية)
- ✅ تنسيق: `YYYY-MM-DDTHH:MM:SS.sssZ`
- ✅ التاريخ فقط: `YYYY-MM-DD`

---

### **القيم المالية**

#### **✅ التنسيق الصحيح**
```json
{
  "price": 299.00,
  "currency": "SAR",
  "tax_amount": 44.85,
  "total": 343.85
}
```

**قواعد**:
- ✅ `Decimal(10,2)` - رقمين بعد الفاصلة
- ✅ دائمًا مع `currency` (ISO 4217)
- ✅ موجب أو صفر (لا سالب للأسعار)
- ❌ لا Float (استخدم Decimal أو Integer بالفلس)

#### **✅ البديل: Integer بأصغر وحدة**
```json
{
  "price_cents": 29900,      // 299.00 ريال
  "tax_cents": 4485,         // 44.85 ريال
  "total_cents": 34385,      // 343.85 ريال
  "currency": "SAR"
}
```

---

### **المعرفات | Identifiers**

#### **✅ UUID/ULID (موصى به)**
```json
{
  "id": "c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m",
  "customer_id": "01HN8X7ZGQPXZK9VNWJT5JHQE3",
  "order_id": "ORD-20250108-00123"
}
```

**قواعد**:
- ✅ UUID v4 للمعرفات العامة
- ✅ ULID للترتيب الزمني
- ✅ رموز قابلة للقراءة للطلبات
- ❌ لا أرقام متسلسلة مكشوفة

---

### **النصوص | Strings**

```json
{
  "name_ar": "فستان صيفي بالورود",
  "name_en": "Floral Summer Dress",
  "description": "وصف طويل...",
  "email": "customer@example.com",
  "phone": "+966501234567",
  "url": "https://zahraah.com/product/123"
}
```

**قواعد**:
- ✅ UTF-8 encoding
- ✅ Trim whitespace
- ✅ حد أقصى للطول
- ✅ Sanitize HTML/Scripts
- ✅ تنسيق E.164 للهواتف

---

## 3️⃣ قواعد التحقق | Validation Rules {#قواعد-التحقق}

### **القواعد الأساسية**

| القاعدة | الوصف | مثال |
|---------|-------|------|
| `required` | إلزامي | `email` مطلوب |
| `nullable` | يمكن أن يكون null | `middle_name` اختياري |
| `string` | نص | `name` |
| `integer` | عدد صحيح | `quantity` |
| `numeric` | رقم (integer or decimal) | `price` |
| `boolean` | true/false | `is_active` |
| `array` | مصفوفة | `items` |
| `email` | بريد إلكتروني صالح | `customer@example.com` |
| `url` | رابط صالح | `https://...` |
| `date` | تاريخ | `2025-01-08` |
| `date_format` | تنسيق محدد | `Y-m-d H:i:s` |
| `min:n` | حد أدنى | `min:1` |
| `max:n` | حد أقصى | `max:100` |
| `between:min,max` | بين قيمتين | `between:1,99` |
| `in:list` | في قائمة | `in:cod,online,wallet` |
| `regex` | تعبير منتظم | `regex:/^\+9665[0-9]{8}$/` |
| `exists:table,column` | موجود في DB | `exists:customers,id` |
| `unique:table,column` | فريد في DB | `unique:customers,email` |

---

## 4️⃣ التحقق في Laravel | Laravel Validation {#التحقق-في-laravel}

### **FormRequest كامل**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CreateOrderRequest extends FormRequest
{
    /**
     * التحقق من الصلاحية
     */
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }
    
    /**
     * قواعد التحقق
     */
    public function rules(): array
    {
        return [
            // العميل
            'customer_id' => [
                'required',
                'integer',
                'exists:customers,id'
            ],
            
            // العناصر
            'items' => [
                'required',
                'array',
                'min:1',
                'max:50'
            ],
            'items.*.variant_id' => [
                'required',
                'integer',
                'exists:product_variants,id'
            ],
            'items.*.quantity' => [
                'required',
                'integer',
                'min:1',
                'max:99'
            ],
            
            // العنوان
            'shipping_address_id' => [
                'required',
                'integer',
                'exists:addresses,id,customer_id,' . $this->customer_id
            ],
            
            // الدفع
            'payment_method' => [
                'required',
                'string',
                'in:cod,online,wallet'
            ],
            
            // القسيمة (اختياري)
            'coupon_code' => [
                'nullable',
                'string',
                'regex:/^[A-Z0-9]{6,12}$/',
                'exists:coupons,code'
            ],
            
            // ملاحظة (اختياري)
            'note' => [
                'nullable',
                'string',
                'max:500'
            ],
        ];
    }
    
    /**
     * رسائل مخصصة بالعربية
     */
    public function messages(): array
    {
        return [
            'customer_id.required' => 'معرف العميل مطلوب',
            'customer_id.exists' => 'العميل غير موجود',
            
            'items.required' => 'يجب إضافة عنصر واحد على الأقل',
            'items.min' => 'يجب إضافة عنصر واحد على الأقل',
            'items.max' => 'الحد الأقصى 50 عنصر',
            
            'items.*.variant_id.required' => 'معرف المنتج مطلوب',
            'items.*.variant_id.exists' => 'المنتج غير موجود',
            
            'items.*.quantity.required' => 'الكمية مطلوبة',
            'items.*.quantity.min' => 'الكمية يجب أن تكون 1 على الأقل',
            'items.*.quantity.max' => 'الحد الأقصى 99 لكل عنصر',
            
            'payment_method.required' => 'طريقة الدفع مطلوبة',
            'payment_method.in' => 'طريقة دفع غير صالحة',
            
            'coupon_code.regex' => 'رمز القسيمة غير صالح',
            'coupon_code.exists' => 'القسيمة غير موجودة',
            
            'note.max' => 'الملاحظة طويلة جدًا (الحد الأقصى 500 حرف)',
        ];
    }
    
    /**
     * تخصيص أسماء الحقول
     */
    public function attributes(): array
    {
        return [
            'customer_id' => 'معرف العميل',
            'items' => 'العناصر',
            'shipping_address_id' => 'عنوان التوصيل',
            'payment_method' => 'طريقة الدفع',
            'coupon_code' => 'رمز القسيمة',
            'note' => 'الملاحظة',
        ];
    }
    
    /**
     * تحقق إضافي (بعد القواعد الأساسية)
     */
    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            // التحقق من توفر المخزون
            foreach ($this->items as $item) {
                $variant = ProductVariant::find($item['variant_id']);
                if ($variant && $variant->available_stock < $item['quantity']) {
                    $validator->errors()->add(
                        'items',
                        "مخزون غير كافٍ للمنتج {$variant->sku}"
                    );
                }
            }
            
            // التحقق من صلاحية القسيمة
            if ($this->coupon_code) {
                $coupon = Coupon::where('code', $this->coupon_code)->first();
                if ($coupon && $coupon->isExpired()) {
                    $validator->errors()->add('coupon_code', 'القسيمة منتهية الصلاحية');
                }
            }
        });
    }
}
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **استخدم FormRequest للتحقق**
   ```php
   ✅ public function store(CreateOrderRequest $request)
   ❌ public function store(Request $request) { $request->validate(...) }
   ```

2. **رسائل واضحة بالعربية**
   ```
   ✅ "رقم الهاتف يجب أن يبدأ بـ +9665"
   ❌ "The phone field format is invalid"
   ```

3. **التحقق من العلاقات**
   ```php
   ✅ 'customer_id' => 'exists:customers,id'
   ```

4. **Strict schemas - رفض حقول إضافية**
   ```php
   ✅ $request->only(['name', 'price'])
   ❌ $request->all()  // يقبل أي حقول
   ```

---

### ❌ **لا تفعل | Don't**

1. **لا تثق بالمدخلات**
   ```php
   ❌ $product->update($request->all());
   ✅ $product->update($request->validated());
   ```

2. **لا تُرجع تفاصيل التحقق الداخلية**
   ```php
   ❌ "SQLSTATE[23000]: Integrity constraint violation"
   ✅ "القيمة مستخدمة سابقًا"
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **التحقق الشامل**
- [ ] FormRequest لكل endpoint يقبل بيانات
- [ ] قواعد شاملة لكل حقل
- [ ] رسائل مخصصة بالعربية
- [ ] التحقق من العلاقات (exists)
- [ ] التحقق من القيود الفريدة (unique)
- [ ] Strict mode (additionalProperties: false)
- [ ] اختبارات لجميع القواعد

---

## 🔗 **التنقل | Navigation**

[← السابق: عدم التكرار | Previous: Idempotency](03_Idempotency_Transactions.md)

[التالي: الملفات والروابط | Next: Files & Signed URLs →](05_Files_Signed_URLs.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
