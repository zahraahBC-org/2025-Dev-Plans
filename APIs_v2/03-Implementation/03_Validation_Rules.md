# قواعد التحقق — Validation Rules

---

## **Laravel Validation**

### **Form Requests:**

```php
namespace App\Http\Requests\API;

use Illuminate\Foundation\Http\FormRequest;

class StoreProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Product::class);
    }
    
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users'],
            'price' => ['required', 'numeric', 'min:0', 'max:999999'],
            'category_id' => ['required', 'exists:categories,id'],
        ];
    }
    
    public function messages(): array
    {
        return [
            'name.required' => 'الاسم مطلوب',
            'email.unique' => 'البريد الإلكتروني موجود مسبقاً',
            'price.min' => 'السعر يجب أن يكون أكبر من صفر',
        ];
    }
}
```

---

## **Arabic Validation Messages**

```php
// resources/lang/ar/validation.php
return [
    'required' => 'حقل :attribute مطلوب',
    'email' => ':attribute غير صالح',
    'unique' => ':attribute موجود مسبقاً',
    'min' => [
        'string' => ':attribute يجب أن يحتوي على :min أحرف على الأقل',
        'numeric' => ':attribute يجب أن يكون :min على الأقل',
    ],
    'max' => [
        'string' => ':attribute يجب ألا يتجاوز :max حرف',
    ],
    
    'attributes' => [
        'name' => 'الاسم',
        'email' => 'البريد الإلكتروني',
        'password' => 'كلمة المرور',
        'phone' => 'رقم الهاتف',
        'price' => 'السعر',
    ],
];
```

---

## **Custom Validation Rules**

```php
// app/Rules/PhoneSaudi.php
namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class PhoneSaudi implements Rule
{
    public function passes($attribute, $value): bool
    {
        return preg_match('/^(05|5)[0-9]{8}$/', $value);
    }
    
    public function message(): string
    {
        return 'رقم الهاتف يجب أن يبدأ بـ 05 ويتكون من 10 أرقام';
    }
}

// Usage
'phone' => ['required', new PhoneSaudi],
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
