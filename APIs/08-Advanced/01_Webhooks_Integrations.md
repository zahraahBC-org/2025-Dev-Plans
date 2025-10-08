# 01. Webhooks والتكاملات | Webhooks & Integrations

## 🎯 **نظرة عامة | Overview**

تكامل آمن وموثوق مع الأنظمة الخارجية عبر Webhooks للإشعارات الفورية بالأحداث.

**الهدف | Purpose**: تفعيل تكاملات فورية  
**الجمهور | Audience**: مطورو Backend، مهندسو التكامل  
**المتطلبات | Prerequisites**: فهم [الأمان](../03-Security/02_Security_Hardening.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [ما هي Webhooks](#ما-هي-webhooks)
2. [الأحداث](#الأحداث)
3. [التوقيع](#التوقيع)
4. [إعادة المحاولة](#إعادة-المحاولة)
5. [التنفيذ](#التنفيذ)

---

## 1️⃣ ما هي Webhooks | What are Webhooks {#ما-هي-webhooks}

### **التعريف**
إشعارات HTTP تُرسل تلقائيًا عند وقوع أحداث معينة.

### **الفرق بين Webhook وPolling**

```
Polling (تقليدي):
العميل: هل هناك تحديث؟ (كل 30 ثانية)
الخادم: لا
العميل: هل هناك تحديث؟
الخادم: لا
العميل: هل هناك تحديث؟
الخادم: نعم! ← بعد 100 طلب

Webhook (حديث):
الخادم → العميل: حدث جديد! ← فوري
```

---

## 2️⃣ الأحداث | Events {#الأحداث}

### **أحداث زهراء**

```
order.created           - طلب جديد
order.confirmed         - طلب مؤكد
order.paid              - دفع ناجح
order.packed            - تعبئة مكتملة
order.shipped           - شُحن الطلب
order.delivered         - تم التوصيل
order.cancelled         - ألغي الطلب
order.returned          - طلب إرجاع

payment.authorized      - دفع مُفوض
payment.captured        - دفع مُلتقط
payment.failed          - دفع فاشل
payment.refunded        - استرداد

product.created         - منتج جديد
product.updated         - منتج محدث
product.deleted         - منتج محذوف

stock.adjusted          - تعديل مخزون
stock.low               - مخزون منخفض

customer.registered     - عميل جديد
customer.verified       - عميل مُحقق
```

---

## 3️⃣ التوقيع | Signature {#التوقيع}

### **HMAC-SHA256**

```
التوقيع = HMAC-SHA256(
  secret_key,
  timestamp + "." + body
)
```

---

### **إرسال Webhook**

```php
public function sendWebhook(WebhookEndpoint $endpoint, array $event)
{
    $timestamp = now()->timestamp;
    $body = json_encode($event);
    
    // حساب التوقيع
    $signature = hash_hmac(
        'sha256',
        $timestamp . '.' . $body,
        $endpoint->secret
    );
    
    // إرسال
    $response = Http::timeout(5)
        ->withHeaders([
            'Content-Type' => 'application/json',
            'X-Webhook-Signature' => $signature,
            'X-Webhook-Timestamp' => $timestamp,
            'X-Webhook-ID' => $event['id'],
            'User-Agent' => 'Zahraah-Webhooks/1.0'
        ])
        ->post($endpoint->url, $event);
    
    // تسجيل
    WebhookDelivery::create([
        'endpoint_id' => $endpoint->id,
        'event_id' => $event['id'],
        'status_code' => $response->status(),
        'duration_ms' => $response->handlerStats()['total_time'] * 1000,
        'delivered_at' => now()
    ]);
    
    return $response->successful();
}
```

---

### **التحقق من التوقيع (المستقبِل)**

```php
public function verifyWebhook(Request $request)
{
    $signature = $request->header('X-Webhook-Signature');
    $timestamp = $request->header('X-Webhook-Timestamp');
    $body = $request->getContent();
    
    // 1. التحقق من الطابع الزمني (< 5 دقائق)
    if (abs(now()->timestamp - $timestamp) > 300) {
        abort(400, 'Webhook timestamp too old');
    }
    
    // 2. حساب التوقيع المتوقع
    $expectedSignature = hash_hmac(
        'sha256',
        $timestamp . '.' . $body,
        config('webhooks.secret')
    );
    
    // 3. مقارنة آمنة
    if (!hash_equals($expectedSignature, $signature)) {
        abort(401, 'Invalid webhook signature');
    }
    
    return true;
}
```

---

## 4️⃣ إعادة المحاولة | Retry Logic {#إعادة-المحاولة}

### **استراتيجية Exponential Backoff**

```
Attempt   Delay      Total Time
1         0s         0s
2         10s        10s
3         30s        40s
4         2m         2m 40s
5         5m         7m 40s
6         15m        22m 40s
7         30m        52m 40s
8         1h         1h 52m
9         2h         3h 52m
10        6h         9h 52m

توقف بعد 10 محاولات أو 24 ساعة
```

---

### **التنفيذ**

```php
public function retryWebhook(WebhookDelivery $delivery, int $attempt = 1)
{
    $maxAttempts = 10;
    $delays = [0, 10, 30, 120, 300, 900, 1800, 3600, 7200, 21600];  // بالثواني
    
    if ($attempt > $maxAttempts) {
        // نقل لـ Dead Letter Queue
        $delivery->update(['status' => 'failed_permanently']);
        return false;
    }
    
    $delay = $delays[$attempt - 1] ?? 21600;
    
    // إعادة محاولة مجدولة
    RetryWebhook::dispatch($delivery->id)
        ->delay(now()->addSeconds($delay))
        ->onQueue('webhooks');
    
    return true;
}
```

---

## 5️⃣ التنفيذ | Implementation {#التنفيذ}

### **جدول Webhook Endpoints**

```sql
CREATE TABLE webhook_endpoints (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    partner_id BIGINT UNSIGNED NOT NULL,
    url VARCHAR(500) NOT NULL,
    secret VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    
    -- الأحداث المشتركة
    events JSON NOT NULL,
    -- مثال: ["order.created", "order.shipped"]
    
    -- Metadata
    description VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    
    INDEX idx_partner (partner_id),
    INDEX idx_active (is_active)
);

CREATE TABLE webhook_deliveries (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    endpoint_id BIGINT UNSIGNED NOT NULL,
    event_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    
    -- الطلب
    request_body JSON NOT NULL,
    
    -- الاستجابة
    status_code SMALLINT NULL,
    response_body TEXT NULL,
    duration_ms INT NULL,
    
    -- الحالة
    status ENUM('pending', 'delivered', 'failed', 'failed_permanently') NOT NULL,
    attempt INT DEFAULT 1,
    next_retry_at DATETIME NULL,
    
    -- الأوقات
    created_at DATETIME,
    delivered_at DATETIME NULL,
    
    INDEX idx_endpoint_status (endpoint_id, status),
    INDEX idx_event (event_id),
    INDEX idx_retry (next_retry_at)
);
```

---

## ✅ **قائمة التحقق | Checklist**

### **الإرسال**
- [ ] HMAC signature
- [ ] Timestamp verification
- [ ] Event ID (منع ازدواج)
- [ ] Timeout (5 ثوان)
- [ ] Retry مع Backoff
- [ ] DLQ للفشل الدائم
- [ ] تسجيل كل محاولة

### **الاستقبال**
- [ ] التحقق من التوقيع
- [ ] التحقق من Timestamp
- [ ] Idempotency (event_id)
- [ ] إرجاع 2xx سريعًا
- [ ] معالجة في Background

---

## 🔗 **التنقل | Navigation**

[← السابق: اختبارات العقد | Previous: Contract Testing](../06-Testing-Quality/04_Contract_Testing.md)

[التالي: معايير البيانات | Next: Data Standards →](02_Data_Standards.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
