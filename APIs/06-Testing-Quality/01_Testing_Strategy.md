# 01. استراتيجية الاختبارات | Testing Strategy

## 🎯 **نظرة عامة | Overview**

استراتيجية اختبار شاملة لضمان جودة وموثوقية واجهات الـ API.

**الهدف | Purpose**: تحديد نهج الاختبار الشامل  
**الجمهور | Audience**: فرق QA، مطورو Backend  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [هرم الاختبار](#هرم-الاختبار)
2. [أنواع الاختبارات](#أنواع-الاختبارات)
3. [معايير القبول](#معايير-القبول)
4. [بيئات الاختبار](#بيئات-الاختبار)
5. [التغطية المطلوبة](#التغطية-المطلوبة)

---

## 1️⃣ هرم الاختبار | Testing Pyramid {#هرم-الاختبار}

```
           🔺 E2E Tests (قليلة، بطيئة، شاملة)
               - User Journeys
               - Full Integration
          
         🔶 Integration Tests (متوسطة)
            - API + DB
            - Service Communication
       
     🟦 Unit Tests (كثيرة، سريعة، محددة)
        - Business Logic
        - Validation Rules
        - Helpers/Utilities
```

### **التوزيع الموصى به**
- **70%** Unit Tests
- **20%** Integration Tests
- **10%** E2E Tests

---

## 2️⃣ أنواع الاختبارات | Test Types {#أنواع-الاختبارات}

### **1. اختبارات الوحدة | Unit Tests**

#### **الهدف**
اختبار الوحدات الصغيرة بشكل معزول.

#### **مثال (Laravel/Pest)**
```php
it('calculates order total correctly', function () {
    $order = new Order();
    $order->subtotal = 500.00;
    $order->tax_rate = 0.15;
    $order->shipping_fee = 15.00;
    
    expect($order->calculateTotal())
        ->toBe(590.00); // 500 + 75 (tax) + 15 (shipping)
});

it('validates phone number format', function () {
    $validator = new PhoneValidator();
    
    expect($validator->validate('+966501234567'))->toBeTrue();
    expect($validator->validate('0501234567'))->toBeFalse();
    expect($validator->validate('invalid'))->toBeFalse();
});
```

---

### **2. اختبارات التكامل | Integration Tests**

#### **الهدف**
اختبار التكامل بين المكونات (API + DB + Redis).

#### **مثال**
```php
it('creates order with stock reservation', function () {
    // إعداد
    $customer = Customer::factory()->create();
    $variant = Variant::factory()->create(['stock' => 10]);
    
    // تنفيذ
    $response = $this->actingAs($customer)
        ->postJson('/v1/orders', [
            'items' => [
                ['variant_id' => $variant->id, 'quantity' => 2]
            ]
        ]);
    
    // التحقق
    $response->assertStatus(201);
    $response->assertJsonStructure(['id', 'status', 'total']);
    
    // التحقق من حجز المخزون
    expect($variant->fresh()->available_stock)->toBe(8);
});
```

---

### **3. اختبارات العقد | Contract Tests**

#### **الهدف**
التحقق من مطابقة التنفيذ لمواصفة OpenAPI.

#### **باستخدام Dredd**
```bash
# تثبيت
npm install -g dredd

# تشغيل
dredd openapi.yaml https://api.staging.zahraah.com \
  --header "Authorization: Bearer $TOKEN"

# النتيجة
pass: GET /products (200) OK
pass: GET /products/123 (200) OK
fail: POST /orders (201) Response doesn't match schema
  - Expected property 'id' but got 'order_id'
```

#### **باستخدام Schemathesis**
```bash
# تثبيت
pip install schemathesis

# تشغيل
schemathesis run openapi.yaml \
  --base-url https://api.staging.zahraah.com \
  --header "Authorization: Bearer $TOKEN" \
  --checks all

# النتيجة
✅ 45 passed
❌ 2 failed
⚠️ 3 errors
```

---

### **4. اختبارات E2E | End-to-End Tests**

#### **الهدف**
اختبار رحلات المستخدم الكاملة.

#### **مثال: رحلة الشراء**
```javascript
// باستخدام Postman/Newman
{
  "name": "Complete Purchase Journey",
  "tests": [
    {
      "name": "1. Login",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/auth/login",
        "body": {
          "phone": "+966501234567",
          "otp": "123456"
        }
      },
      "tests": [
        "pm.response.to.have.status(200)",
        "pm.response.to.have.jsonBody('access_token')"
      ]
    },
    {
      "name": "2. Browse Products",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/products?category=dresses"
      }
    },
    {
      "name": "3. Add to Cart",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/carts/{{cartId}}/items",
        "body": {
          "variant_id": 123,
          "quantity": 1
        }
      }
    },
    {
      "name": "4. Create Order",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/orders",
        "headers": {
          "Idempotency-Key": "{{$guid}}"
        }
      },
      "tests": [
        "pm.response.to.have.status(201)",
        "pm.response.to.have.header('Location')"
      ]
    }
  ]
}
```

---

### **5. اختبارات الأمان | Security Tests**

#### **الهدف**
كشف الثغرات الأمنية.

#### **OWASP ZAP - API Scan**
```bash
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.staging.zahraah.com/openapi.yaml \
  -f openapi \
  -r zap-report.html

# الفحوص
- SQL Injection
- XSS
- Authentication bypass
- Authorization flaws
- Rate limiting
```

---

### **6. اختبارات الأداء | Performance Tests**

#### **الهدف**
قياس الأداء تحت الحمل.

#### **باستخدام k6**
```javascript
// checkout-flow.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },  // ramp-up
    { duration: '5m', target: 100 },  // steady
    { duration: '2m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],  // 95% < 300ms
    http_req_failed: ['rate<0.01'],    // أخطاء < 1%
  },
};

export default function () {
  const token = 'Bearer ...';
  
  // 1. List products
  let res = http.get('https://api.staging.zahraah.com/v1/products', {
    headers: { 'Authorization': token },
  });
  check(res, { 'products listed': (r) => r.status === 200 });
  
  // 2. Create order
  res = http.post('https://api.staging.zahraah.com/v1/orders', 
    JSON.stringify({
      items: [{ variant_id: 123, quantity: 1 }]
    }),
    {
      headers: {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Idempotency-Key': `key-${__VU}-${__ITER}`
      }
    }
  );
  check(res, { 'order created': (r) => r.status === 201 });
  
  sleep(1);
}
```

**تشغيل**:
```bash
k6 run checkout-flow.js
```

---

## 3️⃣ معايير القبول | Acceptance Criteria {#معايير-القبول}

### **قبل النشر إلى Staging**
- [ ] Unit Tests: تغطية ≥ 60%
- [ ] Integration Tests: جميع المسارات الحرجة
- [ ] Contract Tests: 0 فروقات

### **قبل النشر إلى Production**
- [ ] جميع اختبارات Staging ناجحة
- [ ] Security Scan: 0 ثغرات حرجة
- [ ] Performance Tests: P95 ≤ 300ms
- [ ] E2E Tests: رحلات أساسية تعمل

---

## 4️⃣ بيئات الاختبار | Test Environments {#بيئات-الاختبار}

| البيئة | الاستخدام | البيانات |
|--------|----------|---------|
| **Local** | التطوير اليومي | SQLite/Memory |
| **Dev** | Integration Tests | بيانات وهمية |
| **Staging** | Contract + E2E + Security | شبيهة بالإنتاج |
| **Production** | Smoke Tests فقط | حقيقية |

---

## 🔗 **التنقل | Navigation**

[← السابق: الترقيم | Previous: Pagination](../04-Implementation/02_Pagination_Filtering_Sorting.md)

[التالي: خط CI/CD | Next: CI/CD Pipeline →](02_CI_CD_Pipeline.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved