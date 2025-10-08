# 04. التوافقية والتكاملات الخارجية | Compatibility & External Integrations

## 🎯 **نظرة عامة | Overview**

إدارة التكاملات مع الأنظمة الخارجية (الدفع، الشحن، ERP) بشكل آمن وموثوق.

**الهدف | Purpose**: تكاملات خارجية آمنة  
**الجمهور | Audience**: مطورو Backend، مهندسو التكامل  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [نمط Adapter](#adapter)
2. [Circuit Breaker](#circuit-breaker)
3. [Retry Logic](#retry)
4. [التكاملات الرئيسية](#التكاملات)
5. [المراقبة](#المراقبة)

---

## 1️⃣ نمط Adapter | Adapter Pattern {#adapter}

### **الفكرة**
عزل التكاملات الخارجية خلف واجهة موحدة.

```php
// واجهة موحدة
interface PaymentGatewayInterface
{
    public function charge(float $amount, string $currency): PaymentResult;
    public function refund(string $transactionId, float $amount): RefundResult;
}

// Adapter لبوابة 1
class StripeAdapter implements PaymentGatewayInterface
{
    public function charge(float $amount, string $currency): PaymentResult
    {
        $stripeResult = $this->stripeClient->charges->create([
            'amount' => $amount * 100,  // cents
            'currency' => strtolower($currency),
        ]);
        
        // تحويل إلى شكل موحد
        return new PaymentResult(
            id: $stripeResult->id,
            status: $this->mapStatus($stripeResult->status),
            amount: $amount,
            currency: $currency
        );
    }
}

// Adapter لبوابة 2
class TapAdapter implements PaymentGatewayInterface
{
    public function charge(float $amount, string $currency): PaymentResult
    {
        // تكامل مختلف لكن نفس الواجهة
    }
}
```

---

## 2️⃣ Circuit Breaker {#circuit-breaker}

### **الحالات**

```
Closed (مغلق)         - طبيعي، كل الطلبات تمر
    ↓ (فشل متكرر)
    
Open (مفتوح)          - يرفض الطلبات فورًا
    ↓ (بعد timeout)
    
Half-Open (نصف مفتوح)  - يسمح بطلب واحد تجريبي
    ↓ (نجح)           ↓ (فشل)
    
Closed                Open
```

---

### **التنفيذ**

```php
use Illuminate\Support\Facades\Cache;

class CircuitBreaker
{
    private string $serviceName;
    private int $failureThreshold = 5;
    private int $timeout = 60;  // ثواني
    
    public function call(callable $action)
    {
        $state = Cache::get("circuit:{$this->serviceName}:state", 'closed');
        
        if ($state === 'open') {
            // التحقق من Timeout
            $openedAt = Cache::get("circuit:{$this->serviceName}:opened_at");
            if (now()->timestamp - $openedAt < $this->timeout) {
                throw new ServiceUnavailableException("{$this->serviceName} circuit is open");
            }
            
            // الانتقال لـ Half-Open
            Cache::put("circuit:{$this->serviceName}:state", 'half-open');
        }
        
        try {
            $result = $action();
            
            // نجح - إعادة تعيين
            if ($state === 'half-open') {
                $this->close();
            }
            Cache::put("circuit:{$this->serviceName}:failures", 0);
            
            return $result;
            
        } catch (\Exception $e) {
            $failures = Cache::increment("circuit:{$this->serviceName}:failures");
            
            if ($failures >= $this->failureThreshold) {
                $this->open();
            }
            
            throw $e;
        }
    }
    
    private function open()
    {
        Cache::put("circuit:{$this->serviceName}:state", 'open');
        Cache::put("circuit:{$this->serviceName}:opened_at", now()->timestamp);
    }
    
    private function close()
    {
        Cache::put("circuit:{$this->serviceName}:state", 'closed');
        Cache::forget("circuit:{$this->serviceName}:failures");
    }
}
```

---

## 3️⃣ Retry Logic | إعادة المحاولة {#retry}

### **Exponential Backoff**

```php
use Illuminate\Support\Facades\Http;

public function callExternalAPI($url, $data, $maxAttempts = 3)
{
    $attempt = 0;
    
    while ($attempt < $maxAttempts) {
        try {
            $response = Http::timeout(10)
                ->retry($maxAttempts, function ($exception, $request) use (&$attempt) {
                    $attempt++;
                    $delay = min(1000 * (2 ** $attempt), 10000);  // max 10s
                    usleep($delay * 1000);  // تحويل لـ microseconds
                    
                    return $exception instanceof ConnectionException;
                })
                ->post($url, $data);
            
            return $response->json();
            
        } catch (\Exception $e) {
            if ($attempt >= $maxAttempts) {
                throw $e;
            }
        }
    }
}
```

---

## 4️⃣ التكاملات الرئيسية | Key Integrations {#التكاملات}

### **بوابات الدفع**
```
- Stripe
- Tap Payments
- PayPal
- Hyperpay
```

### **خدمات الشحن**
```
- Aramex
- DHL
- FedEx
- SMSA
```

### **الإشعارات**
```
- Twilio (SMS)
- WhatsApp Business API
- Firebase Cloud Messaging (Push)
- SendGrid (Email)
```

---

## 5️⃣ المراقبة | Monitoring {#المراقبة}

### **مقاييس التكامل**

```
- Integration requests/sec
- Success rate per provider
- Latency per provider
- Error rate per error type
- Circuit breaker states
- Retry attempts
```

---

## ✅ **قائمة التحقق | Checklist**

### **التكاملات**
- [ ] Adapter pattern لكل تكامل
- [ ] Circuit Breaker مفعل
- [ ] Retry مع Exponential Backoff
- [ ] Timeout محدد (5-10 ثوان)
- [ ] Fallback عند الفشل
- [ ] مراقبة كل تكامل
- [ ] Sandbox للاختبار

---

## 🔗 **التنقل | Navigation**

[← السابق: إدارة الإصدارات | Previous: Version Management](03_Version_Management.md)

[التالي: الحوكمة | Next: Governance & Change Management →](../09-Governance/01_Governance_Change_Management.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
