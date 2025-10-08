# 03. دليل العمليات | Operations Playbook

## 🎯 **نظرة عامة | Overview**

دليل شامل للعمليات اليومية والاستجابة للحوادث والصيانة الدورية.

**الهدف | Purpose**: تشغيل الـ API بشكل موثوق 24/7  
**الجمهور | Audience**: مهندسو SRE، فرق العمليات، On-call  
**المتطلبات | Prerequisites**: فهم [المراقبة](02_Monitoring_Observability.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [نموذج التشغيل](#نموذج-التشغيل)
2. [المناوبة](#المناوبة)
3. [إدارة الحوادث](#إدارة-الحوادث)
4. [Runbooks](#runbooks)
5. [الصيانة الدورية](#الصيانة-الدورية)

---

## 1️⃣ نموذج التشغيل | Operating Model {#نموذج-التشغيل}

### **الأدوار والمسؤوليات**

| الدور | المسؤولية | المتوفرية |
|------|-----------|----------|
| **On-call Primary** | الاستجابة الأولى للحوادث | 24/7 |
| **On-call Secondary** | الدعم والتصعيد | 24/7 |
| **SRE Lead** | القرارات المعمارية | ساعات العمل |
| **Security Engineer** | الحوادث الأمنية | On-demand |
| **Backend DRI** | الإصلاحات التقنية | ساعات العمل |

---

## 2️⃣ المناوبة | On-Call {#المناوبة}

### **جدول المناوبة**
```
الأسبوع    Primary           Secondary
1          أحمد             سارة
2          سارة             محمد
3          محمد             أحمد
4          أحمد             سارة
```

### **تسليم المناوبة | Handover**
```markdown
## Handover Checklist

### الحوادث النشطة
- [ ] INC-123: ارتفاع latency - قيد التحقيق
- [ ] INC-124: فشل webhook - تم الإصلاح

### التنبيهات المتكررة
- [ ] Redis memory 80% - مراقبة

### التغييرات المخططة
- [ ] نشر v1.3.0 - غدًا 10:00 AM

### ملاحظات
- بوابة الدفع X بطيئة قليلاً - طبيعي
```

---

## 3️⃣ إدارة الحوادث | Incident Management {#إدارة-الحوادث}

### **تصنيف الشدة**

| المستوى | التأثير | مثال | SLA الاستجابة |
|---------|---------|------|---------------|
| **S0** | انقطاع كامل | API down | ≤ 5 دقائق |
| **S1** | تأثير كبير | 50% من الطلبات تفشل | ≤ 15 دقيقة |
| **S2** | تأثير متوسط | بعض endpoints بطيئة | ≤ 60 دقيقة |
| **S3** | تأثير منخفض | مشكلة طفيفة | ≤ 24 ساعة |

---

### **دورة حياة الحادث**

```
1. الرصد (Detection)
   ↓ التنبيه التلقائي
   
2. الإقرار (Acknowledgment)
   ↓ On-call يقر خلال 5 دقائق
   
3. التحليل (Investigation)
   ↓ جمع المعلومات، فحص logs/metrics
   
4. الاحتواء (Mitigation)
   ↓ حل مؤقت لاستعادة الخدمة
   
5. الحل (Resolution)
   ↓ إصلاح دائم
   
6. المراجعة (Postmortem)
   ↓ خلال 72 ساعة، بلا لوم
```

---

### **قنوات التواصل**

```
S0/S1 - حرج:
├─ PagerDuty (فوري)
├─ Slack #incidents (فوري)
├─ Email الإدارة (فوري)
└─ Status Page (علني)

S2/S3 - غير حرج:
├─ Slack #incidents
└─ Jira Ticket
```

---

## 4️⃣ Runbooks | كتيبات التشغيل {#runbooks}

### **1. ارتفاع معدل 5xx | High 5xx Rate**

#### **الأعراض**
```
- Dashboard: 5xx% > 1%
- Alert: HighErrorRate firing
- Customer impact: طلبات تفشل
```

#### **التحقيق**
```bash
# 1. فحص logs الأخيرة
kubectl logs -l app=api-service --since=10m | grep "ERROR"

# 2. فحص metrics
curl "$PROM/query?query=rate(api_errors_total{status=~\"5..\"}[5m])"

# 3. فحص DB
mysql -e "SHOW PROCESSLIST;" | grep -i "locked"

# 4. فحص Redis
redis-cli INFO stats | grep instantaneous_ops_per_sec
```

#### **الإصلاحات المحتملة**
```
□ إعادة تشغيل pods المتعطلة
□ زيادة DB connections
□ تنظيف Redis memory
□ Rollback إلى آخر إصدار جيد
```

---

### **2. فشل قاعدة البيانات | Database Failure**

#### **الأعراض**
```
- Errors: "Connection refused"
- Latency: مرتفع جدًا
- All endpoints: فشل
```

#### **الإصلاحات**
```bash
# 1. فحص حالة DB
mysql -e "SELECT 1;"

# 2. فحص الاتصالات
mysql -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -e "SHOW VARIABLES LIKE 'max_connections';"

# 3. إذا ممتلئ، قتل الاتصالات الخاملة
mysql -e "SHOW PROCESSLIST;" | grep Sleep | awk '{print $1}' | xargs -I {} mysql -e "KILL {};"

# 4. Failover إلى Replica (إذا توفر)
./scripts/db-failover.sh
```

---

### **3. فشل Cache (Redis)**

#### **الأعراض**
```
- Cache Miss Rate: 100%
- DB Load: مرتفع
- Latency: زيادة
```

#### **الإصلاحات**
```bash
# 1. فحص Redis
redis-cli PING
redis-cli INFO memory

# 2. إذا memory ممتلئ
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# 3. تنظيف يدوي
redis-cli FLUSHDB  # حذر!

# 4. إعادة تشغيل
docker restart redis
# أو
kubectl rollout restart deployment/redis
```

---

## 5️⃣ الصيانة الدورية | Routine Maintenance {#الصيانة-الدورية}

### **يومياً | Daily**
- [ ] مراجعة Dashboard (errors, latency)
- [ ] فحص Alerts الليلية
- [ ] مراجعة Capacity (DB, Redis, Disk)
- [ ] تنظيف Logs القديمة

### **أسبوعياً | Weekly**
- [ ] مراجعة SLO Compliance
- [ ] تحليل Top Errors
- [ ] مراجعة Security Scan
- [ ] تحديث Dependencies
- [ ] Backup verification

### **شهرياً | Monthly**
- [ ] Load Testing
- [ ] Security Penetration Test
- [ ] Cost Review
- [ ] Capacity Planning
- [ ] Postmortem Review

### **ربع سنوي | Quarterly**
- [ ] DR Drill (Disaster Recovery)
- [ ] Key Rotation
- [ ] Architecture Review
- [ ] SLO Adjustment

---

## ✅ **قائمة التحقق | Checklist**

### **جاهزية العمليات**
- [ ] On-call schedule محدث
- [ ] Runbooks محدثة
- [ ] Monitoring/Alerts تعمل
- [ ] Incident process معروف
- [ ] Rollback tested
- [ ] DR plan موثق
- [ ] Contact list محدث

---

## 🔗 **التنقل | Navigation**

[← السابق: المراقبة | Previous: Monitoring](02_Monitoring_Observability.md)

[التالي: استراتيجية الاختبار | Next: Testing Strategy →](../06-Testing-Quality/01_Testing_Strategy.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved