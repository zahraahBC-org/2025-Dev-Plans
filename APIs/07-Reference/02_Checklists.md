# 02. قوائم التحقق | Checklists

## 🎯 **نظرة عامة | Overview**

قوائم تحقق شاملة لضمان الجودة والاكتمال في كل مرحلة من مراحل تطوير الـ API.

**الهدف | Purpose**: ضمان عدم تفويت أي خطوة مهمة  
**الجمهور | Audience**: جميع الفرق (Backend, QA, DevOps)  
**الاستخدام | Usage**: مراجعة قبل كل milestone

---

## 📋 **جدول المحتويات | Table of Contents**

1. [قائمة تصميم Endpoint](#قائمة-تصميم-endpoint)
2. [قائمة الأمان](#قائمة-الأمان)
3. [قائمة الجودة](#قائمة-الجودة)
4. [قائمة النشر](#قائمة-النشر)
5. [قائمة المراجعة](#قائمة-المراجعة)

---

## 1️⃣ قائمة تصميم Endpoint | Endpoint Design Checklist {#قائمة-تصميم-endpoint}

### **عند إضافة endpoint جديد**

#### **التصميم | Design**
- [ ] المسار يتبع naming convention (`kebab-case`)
- [ ] المورد بصيغة الجمع (`/products` وليس `/product`)
- [ ] الإصدار في المسار (`/v1/...`)
- [ ] لا أفعال في المسار
- [ ] العمق ≤ 3 مستويات
- [ ] استخدام HTTP method الصحيح

#### **الأمان | Security**
- [ ] المصادقة مطلوبة (JWT/OAuth)
- [ ] التخويل محدد (Role/Scope)
- [ ] Idempotency-Key للعمليات الحساسة
- [ ] Input validation شامل
- [ ] Rate limiting محدد

#### **التوثيق | Documentation**
- [ ] موثق في OpenAPI
- [ ] أمثلة طلبات واستجابات
- [ ] جميع الأخطاء المتوقعة موثقة
- [ ] Parameters موثقة
- [ ] Response schemas معرفة

#### **الاختبار | Testing**
- [ ] Unit tests
- [ ] Integration tests
- [ ] Contract tests ضد OpenAPI
- [ ] Security tests
- [ ] Performance tests (للمسارات الحرجة)

---

## 2️⃣ قائمة الأمان | Security Checklist {#قائمة-الأمان}

### **OWASP API Security Top 10**

#### **1. Broken Object Level Authorization**
- [ ] التحقق من ملكية المورد
- [ ] لا يمكن للمستخدم الوصول لموارد غيره
- [ ] اختبارات للوصول غير المصرح

#### **2. Broken Authentication**
- [ ] JWT قصير العمر (≤ 30 دقيقة)
- [ ] Refresh token rotation
- [ ] Rate limiting على auth endpoints
- [ ] Hash آمن للكلمات (Argon2id)

#### **3. Broken Object Property Level Authorization**
- [ ] تصفية الحقول الحساسة
- [ ] منع Mass Assignment
- [ ] التحقق من صلاحية كتابة الحقول

#### **4. Unrestricted Resource Consumption**
- [ ] Rate limiting مطبق
- [ ] حد أقصى للـ payload size
- [ ] حد أقصى للـ pagination limit
- [ ] Timeout على العمليات الطويلة

#### **5. Broken Function Level Authorization**
- [ ] التحقق من Role/Scope لكل endpoint
- [ ] فصل endpoints الإدارية
- [ ] اختبارات privilege escalation

#### **6. Unrestricted Access to Sensitive Business Flows**
- [ ] Idempotency للعمليات المالية
- [ ] التحقق من الحالة قبل التحويل
- [ ] Audit log للعمليات الحساسة

#### **7. Server Side Request Forgery (SSRF)**
- [ ] التحقق من URLs المدخلة
- [ ] Allowlist للنطاقات
- [ ] منع الوصول للموارد الداخلية

#### **8. Security Misconfiguration**
- [ ] HTTPS فقط
- [ ] Security headers (HSTS, CSP, etc.)
- [ ] تحديث منتظم للمكتبات
- [ ] إخفاء معلومات الخادم

#### **9. Improper Inventory Management**
- [ ] OpenAPI محدث
- [ ] جرد لجميع endpoints
- [ ] توثيق الإصدارات
- [ ] Deprecation policy واضحة

#### **10. Unsafe Consumption of APIs**
- [ ] التحقق من استجابات الطرف الثالث
- [ ] Timeout على المكالمات الخارجية
- [ ] Circuit breaker للخدمات الخارجية

---

## 3️⃣ قائمة الجودة | Quality Checklist {#قائمة-الجودة}

### **قبل الدمج | Pre-Merge**
- [ ] CI/CD أخضر (جميع المراحل)
- [ ] Code review من شخصين على الأقل
- [ ] Unit tests تغطية ≥ 60%
- [ ] Integration tests تمر
- [ ] Contract tests: 0 فروقات
- [ ] Lint/Static analysis نظيف
- [ ] لا أسرار في الكود

### **قبل Staging**
- [ ] OpenAPI محدث
- [ ] Changelog محدث
- [ ] Migration scripts جاهزة (إذا لزم)
- [ ] Feature flags مهيأة
- [ ] Smoke tests جاهزة

### **قبل Production**
- [ ] جميع اختبارات Staging ناجحة
- [ ] Security scan: 0 ثغرات حرجة
- [ ] Performance tests: SLOs محققة
- [ ] Rollback plan جاهز
- [ ] On-call محدد
- [ ] Monitoring/Alerts جاهزة
- [ ] Communication plan للتغييرات الكبيرة

---

## 4️⃣ قائمة النشر | Deployment Checklist {#قائمة-النشر}

### **Pre-Deployment**
- [ ] Tag Git (vX.Y.Z)
- [ ] Release notes جاهزة
- [ ] Database migrations محضرة
- [ ] Environment variables محدثة
- [ ] Secrets محدثة (إذا لزم)
- [ ] Backup حديث موجود
- [ ] Rollback command مُختبر

### **During Deployment**
- [ ] Database migrations نجحت
- [ ] Canary deployment (5% → 25% → 100%)
- [ ] Health gates تمر في كل خطوة
- [ ] Monitoring active
- [ ] No alerts firing

### **Post-Deployment**
- [ ] Smoke tests نجحت
- [ ] مراقبة Metrics (30 دقيقة)
- [ ] لا ارتفاع في الأخطاء
- [ ] P95 latency ضمن الحدود
- [ ] Feature flags تعمل كما متوقع
- [ ] Documentation deployed

---

## 5️⃣ قائمة المراجعة | Review Checklist {#قائمة-المراجعة}

### **مراجعة كود API**
- [ ] هل يتبع REST principles؟
- [ ] هل الأسماء واضحة؟
- [ ] هل Input validation كافٍ؟
- [ ] هل Error handling موحد؟
- [ ] هل التعليقات واضحة؟
- [ ] هل استخدم Dependency Injection؟
- [ ] هل تجنب N+1 queries؟
- [ ] هل استخدم Transactions للعمليات المتعددة؟

### **مراجعة OpenAPI**
- [ ] هل جميع endpoints موثقة؟
- [ ] هل الأمثلة واقعية؟
- [ ] هل schemas كاملة؟
- [ ] هل الأخطاء موثقة؟
- [ ] هل security schemes واضحة؟
- [ ] هل tags منظمة؟

### **مراجعة الأمان**
- [ ] هل Authentication/Authorization صحيح؟
- [ ] هل Input sanitization مطبق؟
- [ ] هل لا يوجد PII في Logs؟
- [ ] هل Secrets في Secret Manager؟
- [ ] هل CORS محدد بدقة؟
- [ ] هل Rate limiting مناسب؟

---

## 📊 **مؤشرات الجودة | Quality Metrics**

### **معايير القبول الشاملة**

| المعيار | الهدف | القياس |
|---------|-------|--------|
| **Coverage** | ≥ 60% | من CI |
| **Contract Tests** | 0 فروقات | Dredd/Schemathesis |
| **P95 Latency** | ≤ 300ms | من Load Tests |
| **Error Rate** | ≤ 0.1% | من Production |
| **Availability** | ≥ 99.9% | Uptime Monitoring |
| **Security Score** | A+ | من Security Scan |

---

## ✅ **قائمة تحقق سريعة | Quick Checklist**

### **الأساسيات (يجب أن تكون دائمًا Yes)**
- [ ] HTTPS فقط
- [ ] Authentication مطلوب
- [ ] أخطاء موحدة
- [ ] OpenAPI محدث
- [ ] اختبارات تمر
- [ ] لا أسرار في الكود

---

## 🔗 **التنقل | Navigation**

[← السابق: قوالب وأمثلة | Previous: Templates & Examples](01_Templates_Examples.md)

[التالي: مرجع سريع | Next: Quick Reference →](03_Quick_Reference.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved