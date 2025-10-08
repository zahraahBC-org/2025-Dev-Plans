# 10. قائمة أفضل الممارسات | Best Practices Checklist
## دليل مرجعي سريع | Quick Reference Guide

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: قائمة فحص سريعة لأفضل ممارسات قاعدة البيانات  
**Purpose**: Quick checklist for database best practices

**الجمهور**: جميع أعضاء الفريق (مرجع سريع)  
**Audience**: All team members (quick reference)

**النطاق**: قوائم فحص لجميع جوانب قاعدة البيانات  
**Scope**: Checklists for all database aspects

---

## 🎯 **نظرة عامة | Overview**

هذا المستند يوفر قوائم فحص سريعة وقابلة للتنفيذ لضمان اتباع أفضل الممارسات في جميع جوانب تصميم وإدارة قاعدة البيانات.

---

## 📑 **جدول المحتويات | Table of Contents**

1. [قائمة فحص تصميم المخطط | Schema Design Checklist](#schema-design-checklist)
2. [قائمة فحص تحسين الاستعلامات | Query Optimization Checklist](#query-optimization-checklist)
3. [قائمة فحص الأمان | Security Checklist](#security-checklist)
4. [قائمة فحص النسخ الاحتياطي | Backup Checklist](#backup-checklist)
5. [قائمة فحص النشر | Deployment Checklist](#deployment-checklist)
6. [قائمة فحص الترحيل | Migration Checklist](#migration-checklist)
7. [المشاكل الشائعة والحلول | Common Pitfalls & Solutions](#common-pitfalls)
8. [دليل استكشاف الأخطاء | Troubleshooting Guide](#troubleshooting)

---

## 1. قائمة فحص تصميم المخطط | Schema Design Checklist {#schema-design-checklist}

### **قبل إنشاء جدول جديد | Before Creating a New Table**

- [ ] اسم الجدول بصيغة **snake_case** ومفرد
- [ ] المفتاح الأساسي محدد بوضوح (BIGINT أو UUID)
- [ ] جميع المفاتيح الخارجية لها قيود FK
- [ ] سياسات ON DELETE/UPDATE واضحة
- [ ] أعمدة التدقيق موجودة (created_at، updated_at)
- [ ] عمود archived_at للحذف الناعم (إذا مطلوب)
- [ ] جميع الحقول المطلوبة بـ NOT NULL
- [ ] أنواع البيانات مناسبة (DECIMAL للأموال)
- [ ] قيود CHECK لتحقق القيم
- [ ] قيود UNIQUE للحقول الفريدة
- [ ] الترميز utf8mb4 محدد
- [ ] المحرك InnoDB محدد
- [ ] تعليقات على الجدول والأعمدة

**مثال**:
```sql
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    archived_at DATETIME,
    
    CONSTRAINT chk_phone_format CHECK (phone REGEXP '^\\+[1-9][0-9]{1,14}$'),
    
    INDEX idx_phone (phone),
    INDEX idx_archived (archived_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='جدول العملاء الرئيسي';
```

---

## 2. قائمة فحص تحسين الاستعلامات | Query Optimization Checklist {#query-optimization-checklist}

### **قبل نشر استعلام جديد | Before Deploying a New Query**

- [ ] استخدام Prepared Statements (ضد SQL Injection)
- [ ] الاستعلام يستخدم فهارس موجودة
- [ ] EXPLAIN يُظهر type = ref/range (ليس ALL)
- [ ] عدد الصفوف المفحوصة معقول (< 10K)
- [ ] لا استخدام دالات على أعمدة مفهرسة في WHERE
- [ ] تجنب SELECT * (حدد الأعمدة المطلوبة)
- [ ] استخدام LIMIT للتحكم في النتائج
- [ ] JOINs على أعمدة مفهرسة
- [ ] ORDER BY على أعمدة مفهرسة
- [ ] تجنب subqueries متداخلة (استخدم JOINs)
- [ ] الترقيم بـ Keyset للقوائم الكبيرة
- [ ] وقت الاستجابة < SLO المحدد

**مثال EXPLAIN جيد**:
```
+----+-------------+--------+------+---------------+---------+---------+-------+------+-------------+
| id | select_type | table  | type | key           | key_len | ref     | rows  | Extra       |
+----+-------------+--------+------+---------------+---------+---------+-------+------+-------------+
|  1 | SIMPLE      | orders | ref  | idx_customer  | 8       | const   | 25    | Using index |
+----+-------------+--------+------+---------------+---------+---------+-------+------+-------------+
```

---

## 3. قائمة فحص الأمان | Security Checklist {#security-checklist}

### **الأمان العام | General Security**

- [ ] **لا استخدام root** للتطبيق
- [ ] حسابات منفصلة لكل غرض (app، readonly، backup)
- [ ] **مبدأ الصلاحيات الأقل** مطبق لجميع المستخدمين
- [ ] **TLS/SSL إلزامي** لجميع الاتصالات
- [ ] كلمات مرور قوية (12+ حرف، معقدة)
- [ ] تدوير كلمات المرور دوري (90 يوم)
- [ ] **تقييد IP** للوصول الحساس
- [ ] VPN أو Bastion Host للوصول الإنتاجي
- [ ] **2FA** لحسابات Admin
- [ ] سجلات التدقيق مفعلة للعمليات الحساسة

---

### **حماية البيانات | Data Protection**

- [ ] **لا PII غير مشفر** في السجلات
- [ ] Views مقنّعة لخدمة العملاء
- [ ] **لا تخزين بيانات بطاقات** (استخدم Tokenization)
- [ ] التشفير في الراحة مفعّل (TDE)
- [ ] التشفير في النقل مفعّل (TLS)
- [ ] الأسرار في Secret Manager (ليس في الكود)
- [ ] موافقات التسويق محترمة
- [ ] سياسات GDPR مطبقة
- [ ] إجراءات DSAR موثقة ومختبرة

---

## 4. قائمة فحص النسخ الاحتياطي | Backup Checklist {#backup-checklist}

### **إعداد النسخ الاحتياطي | Backup Setup**

- [ ] نسخ احتياطي كامل يومي مجدول
- [ ] Binary Logs مفعلة ومنسوخة
- [ ] **تشفير** جميع النسخ الاحتياطية
- [ ] التخزين في موقع خارجي (S3)
- [ ] سياسة احتفاظ واضحة (7/14/30 يوم)
- [ ] **checksums** لجميع النسخ
- [ ] تنبيهات عند فشل النسخ
- [ ] توثيق إجراءات الاستعادة

---

### **اختبار الاستعادة | Recovery Testing**

- [ ] اختبار استعادة **ربع سنوي** مجدول
- [ ] توثيق نتائج كل اختبار
- [ ] التحقق من checksums بعد الاستعادة
- [ ] التحقق من عدد الصفوف
- [ ] اختبار وظيفي بعد الاستعادة
- [ ] قياس RTO الفعلي
- [ ] قياس RPO الفعلي
- [ ] تحديث إجراءات الاستعادة عند الحاجة

---

## 5. قائمة فحص النشر | Deployment Checklist {#deployment-checklist}

### **قبل النشر للإنتاج | Before Production Deployment**

#### **البيئة | Environment**

- [ ] بيئات منفصلة (dev/stage/prod)
- [ ] نسخ احتياطي قبل النشر
- [ ] نافذة صيانة محددة (إذا مطلوب)
- [ ] إشعار الفريق والمستخدمين
- [ ] خطة الرجوع جاهزة

---

#### **المخطط | Schema**

- [ ] الترحيلات مختبرة في stage
- [ ] الترحيلات لها rollback
- [ ] EXPLAIN للاستعلامات الجديدة
- [ ] الفهارس الجديدة مختبرة
- [ ] لا تغييرات تكسر التوافق
- [ ] التوثيق محدّث

---

#### **البيانات | Data**

- [ ] بيانات seed للاختبار
- [ ] التحقق من سلامة البيانات
- [ ] لا PII في بيئات غير الإنتاج
- [ ] التحقق من القيود
- [ ] التحقق من FK

---

## 6. قائمة فحص الترحيل | Migration Checklist {#migration-checklist}

### **قبل تنفيذ الترحيل | Before Running Migration**

- [ ] مراجعة الكود (PR approved)
- [ ] اختبار في dev
- [ ] اختبار في staging
- [ ] **نسخ احتياطي** قبل الترحيل
- [ ] تقدير الوقت المطلوب
- [ ] خطة rollback مكتوبة
- [ ] إشعار الفريق

---

### **أثناء الترحيل | During Migration**

- [ ] مراقبة السجلات
- [ ] مراقبة الأداء
- [ ] التحقق من القفل
- [ ] التحقق من النسخ المتماثل

---

### **بعد الترحيل | After Migration**

- [ ] التحقق من نجاح الترحيل
- [ ] اختبار وظيفي
- [ ] التحقق من البيانات
- [ ] مراقبة الأداء لـ 24 ساعة
- [ ] تحديث التوثيق
- [ ] إغلاق تذكرة النشر

---

## 7. المشاكل الشائعة والحلول | Common Pitfalls & Solutions {#common-pitfalls}

### **المشكلة 1: استعلامات بطيئة | Slow Queries**

**الأعراض**:
- استعلامات تأخذ > 500ms
- طلبات المستخدم بطيئة
- CPU عالي على قاعدة البيانات

**الأسباب الشائعة**:
- ❌ لا فهارس على أعمدة WHERE
- ❌ استخدام دالات على أعمدة مفهرسة
- ❌ JOINs على أعمدة غير مفهرسة
- ❌ SELECT * على جداول كبيرة
- ❌ OFFSET كبير في الترقيم

**الحلول**:
```sql
-- 1. تحليل الاستعلام
EXPLAIN SELECT ...;

-- 2. إضافة فهارس مناسبة
CREATE INDEX idx_table_column ON table(column);

-- 3. إعادة كتابة الاستعلام
-- بدلاً من:
WHERE DATE(created_at) = '2025-01-08'

-- استخدم:
WHERE created_at >= '2025-01-08 00:00:00'
  AND created_at < '2025-01-09 00:00:00'
```

---

### **المشكلة 2: سجلات يتيمة | Orphaned Records**

**الأعراض**:
- سجلات في order_items بدون orders
- سجلات في addresses بدون customers

**السبب**:
- ❌ لا قيود FK
- ❌ سياسات ON DELETE غير صحيحة

**الحل**:
```sql
-- إضافة قيود FK
ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_orders
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE;

-- البحث عن سجلات يتيمة موجودة
SELECT oi.*
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;
```

---

### **المشكلة 3: رصيد محفظة غير صحيح | Incorrect Wallet Balance**

**الأعراض**:
- الرصيد في wallets.balance_available لا يتطابق مع المعاملات

**السبب**:
- ❌ تحديث مباشر للرصيد بدون معاملة
- ❌ معاملات متزامنة بدون قفل

**الحل**:
```sql
-- استخدام FOR UPDATE دائماً
START TRANSACTION;

SELECT balance_available
FROM wallets
WHERE customer_id = 123
FOR UPDATE;

-- ... تنفيذ المعاملة

COMMIT;

-- تسوية يومية للتحقق
SELECT 
    w.customer_id,
    w.balance_available AS wallet_balance,
    COALESCE(SUM(
        CASE 
            WHEN wt.type = 'credit' THEN wt.amount
            WHEN wt.type = 'debit' THEN -wt.amount
            ELSE 0
        END
    ), 0) AS ledger_balance
FROM wallets w
LEFT JOIN wallet_transactions wt ON w.wallet_id = wt.wallet_id
WHERE wt.status = 'posted'
GROUP BY w.customer_id, w.balance_available
HAVING ABS(wallet_balance - ledger_balance) > 0.01;
```

---

### **المشكلة 4: مخزون سالب | Negative Inventory**

**الأعراض**:
- available_to_promise < 0
- بيع زائد Overselling

**السبب**:
- ❌ عدم استخدام نمط Ledger
- ❌ تحديث مباشر لـ stock_on_hand
- ❌ عدم قفل عند فحص المخزون

**الحل**:
```sql
-- استخدام نمط Ledger دائماً
-- لا تحديث مباشر للمخزون

-- عند حجز مخزون (reservation)
START TRANSACTION;

-- 1. التحقق من المخزون المتاح
SELECT available_to_promise INTO @available
FROM stock_snapshot
WHERE variant_id = 123
  AND warehouse_id = 1
FOR UPDATE;

IF @available < @requested_qty THEN
    ROLLBACK;
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'مخزون غير كافٍ';
END IF;

-- 2. إنشاء حركة reservation
INSERT INTO inventory_ledger (
    variant_id, warehouse_id, movement_type, quantity,
    reference_type, reference_id
) VALUES (
    123, 1, 'reservation', -@requested_qty,
    'order', @order_id
);

-- 3. تحديث snapshot
UPDATE stock_snapshot
SET available_to_promise = available_to_promise - @requested_qty
WHERE variant_id = 123 AND warehouse_id = 1;

COMMIT;
```

---

### **المشكلة 5: deadlocks**

**الأعراض**:
- أخطاء "Deadlock found"
- معاملات تفشل بشكل عشوائي

**الأسباب**:
- ❌ ترتيب قفل غير متسق
- ❌ معاملات طويلة
- ❌ فهارس مفقودة

**الحل**:
```sql
-- دائماً قفل الجداول بنفس الترتيب
-- جيد:
START TRANSACTION;
SELECT * FROM customers WHERE ... FOR UPDATE;  -- أولاً
SELECT * FROM orders WHERE ... FOR UPDATE;     -- ثانياً
COMMIT;

-- سيء (قد يسبب deadlock):
-- معاملة 1: قفل customers → قفل orders
-- معاملة 2: قفل orders → قفل customers

-- تقصير المعاملات
-- قلل الوقت بين BEGIN و COMMIT

-- إضافة فهارس
-- لتقليل عدد الصفوف المقفلة
```

---

### **المشكلة 6: بيانات غير صحيحة | Invalid Data**

**الأعراض**:
- أسعار سالبة
- كميات سالبة
- تواريخ غير صالحة

**السبب**:
- ❌ لا قيود CHECK
- ❌ SQL Mode غير صارم

**الحل**:
```sql
-- إضافة قيود CHECK
ALTER TABLE products
ADD CONSTRAINT chk_price_positive 
    CHECK (base_price > 0);

-- تفعيل وضع SQL صارم
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,...';

-- التحقق من البيانات الموجودة
SELECT * FROM products WHERE base_price <= 0;
SELECT * FROM order_items WHERE quantity <= 0;
```

---

## 8. دليل استكشاف الأخطاء | Troubleshooting Guide {#troubleshooting}

### **الأداء البطيء | Slow Performance**

#### **الخطوة 1: تحديد الاستعلامات البطيئة**

```sql
-- استعلامات من slow query log
SELECT 
    DIGEST_TEXT,
    COUNT_STAR AS exec_count,
    AVG_TIMER_WAIT / 1000000000000 AS avg_time_sec,
    MAX_TIMER_WAIT / 1000000000000 AS max_time_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 10;
```

---

#### **الخطوة 2: تحليل الاستعلام**

```sql
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE customer_id = 123 
ORDER BY created_at DESC;
```

---

#### **الخطوة 3: إضافة/تحسين الفهارس**

```sql
-- إضافة فهرس مركب
CREATE INDEX idx_orders_customer_created 
    ON orders(customer_id, created_at DESC);
```

---

### **اتصالات ممتلئة | Connection Pool Exhaustion**

**الأعراض**:
- "Too many connections"
- التطبيق لا يتصل بقاعدة البيانات

**التشخيص**:
```sql
-- عرض الاتصالات الحالية
SHOW PROCESSLIST;

-- عرض حالة الاتصالات
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
SHOW VARIABLES LIKE 'max_connections';
```

**الحلول**:
```sql
-- 1. زيادة max_connections
SET GLOBAL max_connections = 1000;

-- 2. إغلاق اتصالات معلقة
KILL CONNECTION connection_id;

-- 3. في كود التطبيق: استخدام connection pooling
-- 4. تقليل wait_timeout
SET GLOBAL wait_timeout = 300;  -- 5 دقائق
```

---

### **مساحة قرص ممتلئة | Disk Space Full**

**الأعراض**:
- أخطاء "No space left on device"
- فشل الكتابة

**التشخيص**:
```bash
# التحقق من المساحة
df -h

# حجم قاعدة البيانات
du -sh /var/lib/mysql/

# أكبر الجداول
mysql -e "
SELECT 
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'zahraah_db'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC
LIMIT 10;
"
```

**الحلول**:
```sql
-- 1. تنظيف binary logs القديمة
PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 2. أرشفة/حذف البيانات القديمة
DELETE FROM events_raw WHERE event_date < CURDATE() - INTERVAL 90 DAY;

-- 3. تحسين الجداول
OPTIMIZE TABLE table_name;

-- 4. تقسيم وأرشفة الجداول الكبيرة
```

---

## 📊 **المراجع السريعة | Quick References**

### **أوامر مفيدة | Useful Commands**

```sql
-- حجم الجداول
SELECT 
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS size_mb,
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'zahraah_db'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- الفهارس على جدول
SHOW INDEXES FROM table_name;

-- حالة InnoDB
SHOW ENGINE INNODB STATUS\G

-- المتغيرات
SHOW VARIABLES LIKE '%buffer%';

-- الحالة
SHOW STATUS LIKE '%connection%';

-- العمليات الجارية
SHOW PROCESSLIST;

-- المستخدمون والصلاحيات
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'username'@'host';
```

---

### **أهداف الأداء | Performance Targets**

| السيناريو | الهدف | الإجراء عند التجاوز |
|----------|--------|---------------------|
| قائمة منتجات | < 300ms | فحص الفهارس |
| إنشاء طلب | < 2s | تحسين المعاملة |
| فحص مخزون | < 100ms | فهرس ledger |
| معالجة دفع | < 1s | فحص مزود الدفع |
| تحديث تتبع | < 1min | فحص webhooks |

---

## ✅ **قائمة الفحص النهائية | Final Checklist**

### **قبل إطلاق النظام للإنتاج | Before Production Launch**

#### **المخطط | Schema**
- [ ] جميع الجداول المطلوبة موجودة
- [ ] جميع FK محددة بشكل صحيح
- [ ] جميع الفهارس الأساسية موجودة
- [ ] قيود CHECK مطبقة
- [ ] أعمدة التدقيق موجودة

#### **البيانات | Data**
- [ ] بيانات seed مضافة
- [ ] لا سجلات يتيمة
- [ ] القيم صالحة
- [ ] العلاقات سليمة

#### **الأداء | Performance**
- [ ] جميع الاستعلامات الحرجة محسّنة
- [ ] EXPLAIN جميع الاستعلامات
- [ ] أهداف SLO محققة
- [ ] اختبار الحمل منفذ

#### **الأمان | Security**
- [ ] RBAC مطبق
- [ ] PII محمي
- [ ] TLS مفعّل
- [ ] سجلات التدقيق مفعّلة

#### **النسخ الاحتياطي | Backup**
- [ ] نسخ احتياطي يومي مجدول
- [ ] Binary logs مفعلة
- [ ] اختبار استعادة منفذ
- [ ] توثيق الإجراءات

#### **المراقبة | Monitoring**
- [ ] لوحات معلومات جاهزة
- [ ] تنبيهات مضبوطة
- [ ] Runbooks موثقة
- [ ] فريق مدرب

---

## 🔗 **التنقل | Navigation**

[← السابق: 09. سياسة التحليلات | Previous: Analytics Policy](09_Analytics_Policy.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
