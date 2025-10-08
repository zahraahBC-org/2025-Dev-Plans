# 01. المصادقة والتخويل | Authentication & Authorization

## 🎯 **نظرة عامة | Overview**

دليل شامل لآليات المصادقة والتخويل في منصة **زهراء** لضمان أمان الوصول للموارد.

**الهدف | Purpose**: تطبيق مصادقة وتخويل آمن  
**الجمهور | Audience**: مطورو Backend، مهندسو الأمان  
**المتطلبات | Prerequisites**: فهم [بوابة الـ API](../02-Architecture/02_API_Gateway.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [المصادقة - AuthN](#المصادقة)
2. [التخويل - AuthZ](#التخويل)
3. [JWT Tokens](#jwt-tokens)
4. [OAuth 2.0](#oauth-20)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ المصادقة | Authentication (AuthN) {#المصادقة}

### **ما هي المصادقة؟**
التحقق من هوية المستخدم: **"من أنت؟"**

### **طرق المصادقة**

#### **1. OTP عبر الهاتف | Phone OTP (أساسي)**

```
تدفق تسجيل الدخول:

1. العميل يرسل رقم الهاتف
   POST /v1/auth/otp/request
   {
     "phone": "+966501234567"
   }
   
2. النظام يرسل OTP عبر SMS
   → "رمز التحقق: 123456"
   
3. العميل يرسل OTP
   POST /v1/auth/otp/verify
   {
     "phone": "+966501234567",
     "otp": "123456"
   }
   
4. النظام يتحقق ويُرجع JWT
   {
     "access_token": "eyJhbGc...",
     "refresh_token": "dGhpc2lz...",
     "expires_in": 900
   }
```

**قواعد OTP**:
- ✅ صلاحية: 3-5 دقائق
- ✅ محاولات: 5 كحد أقصى
- ✅ تبريد: 60 ثانية بين الطلبات
- ✅ 6 أرقام عشوائية

---

#### **2. تسجيل الدخول الاجتماعي | Social Login**

##### **Google OAuth 2.0**
```
1. العميل يبدأ تدفق OAuth
   → Google Authorization URL
   
2. المستخدم يوافق
   
3. Google ترجع Authorization Code
   
4. النظام يستبدل Code بـ Access Token
   
5. النظام يحصل على معلومات المستخدم
   
6. النظام ينشئ/يحدّث الحساب ويُرجع JWT
```

##### **Apple Sign In**
```
مشابه لـ Google مع:
- استخدام Apple ID
- دعم إخفاء البريد الإلكتروني
- التحقق من id_token
```

---

#### **3. كلمة المرور | Password (للمسؤولين)**

```http
POST /v1/auth/login
{
  "email": "admin@zahraah.com",
  "password": "***********",
  "totp": "123456"  // 2FA إلزامي
}

# التحقق:
1. Hash كلمة المرور (Argon2id)
2. مطابقة مع DB
3. التحقق من TOTP
4. إرجاع JWT
```

**متطلبات كلمة المرور**:
- ✅ طول ≥ 10 أحرف
- ✅ أحرف كبيرة وصغيرة
- ✅ أرقام ورموز
- ✅ ليست في القائمة السوداء
- ✅ Hash: Argon2id (أو bcrypt ≥ 12)

---

## 2️⃣ التخويل | Authorization (AuthZ) {#التخويل}

### **ما هو التخويل؟**
التحقق من صلاحيات المستخدم: **"ماذا يمكنك أن تفعل؟"**

### **نموذج RBAC | Role-Based Access Control**

#### **الأدوار الأساسية**

| الدور | الصلاحيات | الاستخدام |
|------|-----------|----------|
| **customer** | قراءة/تعديل حسابه وطلباته فقط | العملاء |
| **support** | قراءة بيانات العملاء والطلبات | الدعم الفني |
| **merchandiser** | إدارة الكتالوج والمنتجات | فريق المحتوى |
| **ops_logistics** | إدارة الشحن والتوصيل | العمليات |
| **finance** | المدفوعات والاستردادات | المالية |
| **marketing** | الحملات والقسائم | التسويق |
| **admin** | إدارة المستخدمين والأدوار | الإدارة |
| **superadmin** | كل الصلاحيات | مقيد جدًا |

---

#### **مصفوفة الصلاحيات**

```
المورد:       products
الصلاحيات:    read, write, delete

customer:     ✅ read  ❌ write  ❌ delete
merchandiser: ✅ read  ✅ write  ❌ delete
admin:        ✅ read  ✅ write  ✅ delete
```

---

### **التحقق من الصلاحيات**

#### **على مستوى المورد**
```php
// في Middleware
if (!$user->hasPermission('products.write')) {
    return response()->json([
        'error' => [
            'code' => 'E2002',
            'message' => 'Insufficient permissions'
        ]
    ], 403);
}
```

#### **على مستوى السجل**
```php
// العميل يمكنه رؤية طلباته فقط
$order = Order::where('customer_id', $user->id)
              ->findOrFail($orderId);

// المسؤول يمكنه رؤية كل الطلبات
$order = Order::findOrFail($orderId);
```

---

## 3️⃣ JWT Tokens {#jwt-tokens}

### **البنية**
```
JWT = Header.Payload.Signature
```

#### **Header**
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-2025-01"
}
```

#### **Payload (Claims)**
```json
{
  "sub": "789",              // User ID
  "role": "customer",        // الدور
  "scopes": [                // الصلاحيات
    "orders.read",
    "orders.write"
  ],
  "iss": "https://api.zahraah.com",
  "aud": "zahraah-mobile",
  "iat": 1704715200,         // Issued At
  "exp": 1704716100,         // Expires (15 دقيقة)
  "jti": "c9b1f3a0..."       // JWT ID
}
```

#### **Signature**
```
RSASHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  privateKey
)
```

---

### **دورة حياة الرموز | Token Lifecycle**

```
Access Token:  15-30 دقيقة (قصير العمر)
Refresh Token: 30 يوم (طويل العمر)

1. تسجيل الدخول
   ← Access + Refresh
   
2. استخدام Access
   (حتى انتهاء الصلاحية)
   
3. Access Token منتهي؟
   → استخدام Refresh للتجديد
   
4. تجديد ناجح
   ← Access جديد + Refresh جديد
   
5. Refresh Token منتهي؟
   → إعادة تسجيل الدخول
```

---

### **تجديد الرمز | Token Refresh**

```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "dGhpc2lzYXJlZnJlc2h0b2tlbg..."
}

# الاستجابة
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "bmV3cmVmcmVzaHRva2VuaGVyZQ...",
  "expires_in": 900
}
```

**آلية Refresh Token Rotation**:
- ✅ كل استخدام = رمز جديد
- ✅ إلغاء الرمز القديم
- ✅ اكتشاف إعادة الاستخدام
- ✅ إلغاء كل العائلة عند الشك

---

## 4️⃣ OAuth 2.0 (للشركاء) {#oauth-20}

### **Client Credentials Flow**

```
الشريك → Client ID + Client Secret
         ↓
    Token Endpoint
         ↓
    Access Token (no refresh)
         ↓
    استخدام مع API
```

#### **طلب الرمز**
```http
POST /v1/oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic base64(client_id:client_secret)

grant_type=client_credentials
&scope=products.read orders.read
```

#### **الاستجابة**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "products.read orders.read"
}
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **استخدام HTTPS فقط**
   ```
   ✅ https://api.zahraah.com
   ❌ http://api.zahraah.com
   ```

2. **رموز قصيرة العمر**
   ```
   Access Token:  15 دقيقة
   Refresh Token: 30 يوم
   OTP:           5 دقائق
   ```

3. **تخزين الأسرار بأمان**
   ```
   ✅ Secret Manager
   ✅ Environment Variables (encrypted)
   ❌ Hard-coded في الكود
   ❌ في Git
   ```

4. **2FA للمسؤولين**
   ```
   كلمة المرور + TOTP = إلزامي
   ```

5. **تدوير المفاتيح**
   ```
   كل 90-180 يوم
   دعم مفاتيح متعددة خلال الانتقال
   ```

---

### ❌ **لا تفعل | Don't**

1. **لا تُخزن كلمات مرور بنص واضح**
   ```
   ❌ plain_password
   ✅ Argon2id hash
   ```

2. **لا JWT في URL**
   ```
   ❌ GET /api/data?token=eyJhbG...
   ✅ Authorization: Bearer eyJhbG...
   ```

3. **لا أسرار في الـ Logs**
   ```json
   ❌ { "password": "secret123" }
   ✅ { "password": "[REDACTED]" }
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **عند تنفيذ المصادقة**
- [ ] HTTPS إلزامي
- [ ] JWT قصير العمر (≤ 30 دقيقة)
- [ ] Refresh Token Rotation
- [ ] كشف إعادة الاستخدام
- [ ] Rate Limiting على Auth endpoints
- [ ] 2FA للمسؤولين
- [ ] Hash آمن للكلمات (Argon2id)
- [ ] تسجيل محاولات الفشل

### **عند تنفيذ التخويل**
- [ ] RBAC محدد بوضوح
- [ ] Least Privilege
- [ ] فحص الصلاحيات في كل طلب
- [ ] فصل الأدوار والصلاحيات
- [ ] Audit Log للوصول الحساس

---

## 🔗 **التنقل | Navigation**

[← السابق: بوابة الـ API | Previous: API Gateway](../02-Architecture/02_API_Gateway.md)

[التالي: تقوية الأمان | Next: Security Hardening →](02_Security_Hardening.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved