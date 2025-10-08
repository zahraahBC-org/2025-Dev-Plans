# 02. الخصوصية والامتثال | Privacy & Compliance

## 🎯 **نظرة عامة | Overview**

سياسات الخصوصية والامتثال لحماية بيانات العملاء وتلبية المتطلبات القانونية.

**الهدف | Purpose**: حماية البيانات والامتثال  
**الجمهور | Audience**: Security، Legal، Compliance  
**المتطلبات | Prerequisites**: فهم [الأمان](../03-Security/02_Security_Hardening.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [GDPR](#gdpr)
2. [PCI-DSS](#pci-dss)
3. [Data Classification](#data-classification)
4. [Consent Management](#consent)
5. [Data Retention](#retention)

---

## 1️⃣ GDPR | General Data Protection Regulation {#gdpr}

### **الحقوق الأساسية**

#### **1. Right to Access**
```http
GET /v1/customers/me/data-export
Authorization: Bearer <token>

⟶ يُرجع كل بيانات العميل
{
  "profile": {...},
  "orders": [...],
  "addresses": [...],
  "payment_methods": [...],
  "activity_log": [...]
}
```

---

#### **2. Right to Erasure (حق النسيان)**
```http
DELETE /v1/customers/me
Authorization: Bearer <token>

⟶ يحذف/يُخفي جميع البيانات
- حذف PII (الاسم، البريد، الهاتف)
- Anonymize الطلبات التاريخية
- حذف الجلسات والرموز
```

**التنفيذ**:
```php
public function deleteAccount(Request $request)
{
    $customer = $request->user();
    
    DB::transaction(function () use ($customer) {
        // 1. Anonymize orders (للتقارير)
        Order::where('customer_id', $customer->id)
            ->update([
                'customer_name' => 'Deleted User',
                'customer_email' => null,
                'customer_phone' => null,
            ]);
        
        // 2. حذف البيانات الشخصية
        $customer->addresses()->delete();
        $customer->paymentMethods()->delete();
        $customer->sessions()->delete();
        
        // 3. حذف الحساب
        $customer->delete();
        
        // 4. إلغاء الرموز
        RefreshToken::where('user_id', $customer->id)->delete();
    });
    
    return response()->json([
        'message' => 'تم حذف حسابك بنجاح'
    ]);
}
```

---

#### **3. Right to Portability**
```http
GET /v1/customers/me/export?format=json
Authorization: Bearer <token>

⟶ تصدير بتنسيق قياسي (JSON/CSV)
```

---

## 2️⃣ PCI-DSS | Payment Card Industry {#pci-dss}

### **المتطلبات**

#### **✅ ما يجب فعله**
```
- لا تُخزن CVV أبدًا
- تشفير بيانات البطاقات
- استخدام Tokenization
- Secure transmission (TLS)
- Access control صارم
- Audit logs
```

#### **التنفيذ**
```php
// ✅ تخزين آمن
{
  "payment_method_id": "pm_abc123",
  "type": "card",
  "card_last4": "4242",      // آخر 4 أرقام فقط
  "card_brand": "visa",
  "card_exp_month": 12,
  "card_exp_year": 2026,
  "card_token": "tok_xyz789"  // من Payment Gateway
  // لا CVV، لا رقم بطاقة كامل
}
```

---

## 3️⃣ Data Classification | تصنيف البيانات {#data-classification}

### **مستويات الحساسية**

| المستوى | الوصف | أمثلة | الحماية |
|---------|-------|--------|---------|
| **Public** | عام | أسماء المنتجات | لا |
| **Internal** | داخلي | Metrics | Auth |
| **Confidential** | سري | بيانات العملاء | Auth + Encryption |
| **Restricted** | مقيد جدًا | بيانات الدفع | Auth + Encryption + Audit |

---

### **Masking في Logs**

```php
// ✅ إخفاء البيانات الحساسة
Log::info('Order created', [
    'order_id' => $order->id,
    'customer_id' => $order->customer_id,
    'email' => $this->maskEmail($order->email),     // a***@example.com
    'phone' => $this->maskPhone($order->phone),     // +9665012***67
    'total' => $order->total
]);

private function maskEmail(string $email): string
{
    [$local, $domain] = explode('@', $email);
    return substr($local, 0, 1) . '***@' . $domain;
}

private function maskPhone(string $phone): string
{
    return substr($phone, 0, 7) . '***' . substr($phone, -2);
}
```

---

## 4️⃣ Consent Management | إدارة الموافقات {#consent}

### **أنواع الموافقات**

```sql
CREATE TABLE customer_consents (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT UNSIGNED NOT NULL,
    
    -- الموافقات
    marketing_sms BOOLEAN DEFAULT false,
    marketing_email BOOLEAN DEFAULT false,
    marketing_push BOOLEAN DEFAULT false,
    marketing_whatsapp BOOLEAN DEFAULT false,
    
    -- Analytics
    analytics_tracking BOOLEAN DEFAULT false,
    personalization BOOLEAN DEFAULT false,
    
    -- الطوابع
    consented_at DATETIME NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    
    updated_at DATETIME,
    
    INDEX idx_customer (customer_id)
);
```

---

### **احترام الموافقات**

```php
// قبل إرسال SMS تسويقي
if (!$customer->consents->marketing_sms) {
    Log::info('Skipped SMS - no consent', ['customer_id' => $customer->id]);
    return;
}

// إرسال
$this->smsService->send($customer->phone, $message);
```

---

## 5️⃣ Data Retention | الاحتفاظ بالبيانات {#retention}

### **سياسات الاحتفاظ**

| نوع البيانات | المدة | الإجراء |
|--------------|------|---------|
| **Logs** | 30 يوم | حذف تلقائي |
| **Sessions** | 30 يوم | حذف |
| **Orders (active)** | دائم | الاحتفاظ |
| **Orders (cancelled)** | 3 سنوات | أرشفة ثم حذف |
| **Customer (inactive)** | 2 سنة | إخطار ثم حذف |
| **Analytics** | 13 شهر | تجميع ثم حذف التفاصيل |

---

### **التنفيذ**

```php
// Scheduled Job - يومي
public function cleanupOldData()
{
    // حذف logs قديمة
    Log::where('created_at', '<', now()->subDays(30))->delete();
    
    // حذف sessions منتهية
    Session::where('last_activity', '<', now()->subDays(30))->delete();
    
    // أرشفة طلبات قديمة
    Order::where('status', 'cancelled')
        ->where('created_at', '<', now()->subYears(3))
        ->chunk(100, function ($orders) {
            foreach ($orders as $order) {
                $this->archiveOrder($order);
                $order->delete();
            }
        });
}
```

---

## ✅ **قائمة التحقق | Checklist**

### **الخصوصية**
- [ ] GDPR compliance (Right to access، erasure، portability)
- [ ] PCI-DSS (لا CVV، Tokenization)
- [ ] Data classification محددة
- [ ] Masking في Logs
- [ ] Encryption at rest & in transit

### **الموافقات**
- [ ] Consent management مدمج
- [ ] موافقات دقيقة (per channel)
- [ ] احترام الموافقات في كل إرسال
- [ ] Audit trail للتغييرات

### **الاحتفاظ**
- [ ] Retention policies محددة
- [ ] حذف/أرشفة تلقائي
- [ ] إشعارات للعملاء غير النشطين

---

## 🔗 **التنقل | Navigation**

[← السابق: الحوكمة | Previous: Governance & Change Management](01_Governance_Change_Management.md)

[التالي: النسخ الاحتياطي | Next: Backup & Recovery →](03_Backup_Recovery.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
