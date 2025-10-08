# 06. الأمان والخصوصية | Security & Privacy
## RBAC، إخفاء PII، وسجلات التدقيق | RBAC, PII Masking, and Audit Logs

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد سياسات الأمان والخصوصية لقاعدة البيانات  
**Purpose**: Define security and privacy policies for the database

**الجمهور**: مهندسو الأمان، مسؤولو الامتثال، مديرو قواعد البيانات  
**Audience**: Security engineers, compliance officers, DBAs

**النطاق**: التحكم في الوصول، حماية PII، التشفير، التدقيق  
**Scope**: Access control, PII protection, encryption, auditing

---

## 🎯 **نظرة عامة | Overview**

يحدد هذا المستند سياسات شاملة للأمان والخصوصية لحماية بيانات العملاء وضمان الامتثال للوائح (GDPR، PDPL).

**المبادئ الأساسية**:
- **الحد الأدنى من الصلاحيات**: كل مستخدم يحصل فقط على ما يحتاجه
- **الدفاع المتعمق**: طبقات متعددة من الحماية
- **الشفافية**: تسجيل جميع الإجراءات الحساسة
- **الامتثال**: احترام حقوق العملاء والخصوصية

---

## 📑 **جدول المحتويات | Table of Contents**

1. [التحكم في الوصول RBAC | Role-Based Access Control](#rbac)
2. [إخفاء البيانات الشخصية PII | PII Masking](#pii-masking)
3. [التشفير | Encryption](#encryption)
4. [سجلات التدقيق | Audit Logs](#audit-logs)
5. [إدارة الأسرار | Secret Management](#secret-management)
6. [الامتثال GDPR | GDPR Compliance](#gdpr-compliance)
7. [اختبار الأمان | Security Testing](#security-testing)
8. [أمان الشبكة | Network Security](#network-security)

---

## 1. التحكم في الوصول RBAC | Role-Based Access Control {#rbac}

### **الأدوار المحددة | Defined Roles**

#### **Admin/DBA (إدارة كاملة)**

```sql
-- إنشاء دور المسؤول
CREATE USER 'zahraah_admin'@'localhost' 
    IDENTIFIED BY 'very_strong_password'
    REQUIRE SSL;

-- منح جميع الصلاحيات
GRANT ALL PRIVILEGES ON zahraah_db.* TO 'zahraah_admin'@'localhost';

-- صلاحيات إضافية
GRANT SUPER, PROCESS, RELOAD ON *.* TO 'zahraah_admin'@'localhost';

FLUSH PRIVILEGES;
```

**الصلاحيات**:
- ✅ كامل: SELECT، INSERT، UPDATE، DELETE
- ✅ DDL: CREATE، ALTER، DROP
- ✅ إدارة: GRANT، REVOKE
- ✅ صيانة: OPTIMIZE، ANALYZE

**الاستخدام**: مديرو قواعد البيانات فقط، مصادقة 2FA إلزامية.

---

#### **Application (قراءة/كتابة)**

```sql
-- حساب التطبيق الرئيسي
CREATE USER 'zahraah_app'@'%' 
    IDENTIFIED BY 'app_strong_password'
    REQUIRE SSL;

-- صلاحيات CRUD فقط
GRANT SELECT, INSERT, UPDATE, DELETE 
    ON zahraah_db.* 
    TO 'zahraah_app'@'%';

-- لا DDL، لا GRANT
-- لا TRUNCATE، لا DROP

FLUSH PRIVILEGES;
```

**الصلاحيات**:
- ✅ SELECT، INSERT، UPDATE، DELETE
- ❌ CREATE، ALTER، DROP
- ❌ GRANT، SUPER

**الاستخدام**: تطبيق Flutter/API الخلفي.

---

#### **ReadOnly (قراءة فقط)**

```sql
-- حساب القراءة فقط
CREATE USER 'zahraah_readonly'@'%' 
    IDENTIFIED BY 'readonly_password'
    REQUIRE SSL;

-- قراءة فقط
GRANT SELECT ON zahraah_db.* TO 'zahraah_readonly'@'%';

-- أو استخدم Views مخصصة
GRANT SELECT ON zahraah_db.vw_* TO 'zahraah_readonly'@'%';

FLUSH PRIVILEGES;
```

**الصلاحيات**:
- ✅ SELECT فقط
- ❌ جميع عمليات الكتابة

**الاستخدام**: 
- التقارير والتحليلات
- BI tools (Metabase، Looker)
- لوحات المعلومات
- phpMyAdmin في الإنتاج

---

#### **CustomerService (مقنّع)**

```sql
-- حساب خدمة العملاء
CREATE USER 'zahraah_cs'@'%' 
    IDENTIFIED BY 'cs_password'
    REQUIRE SSL;

-- الوصول إلى Views مقنّعة فقط
GRANT SELECT ON zahraah_db.vw_customers_masked TO 'zahraah_cs'@'%';
GRANT SELECT ON zahraah_db.vw_orders_cs TO 'zahraah_cs'@'%';
GRANT UPDATE ON zahraah_db.orders TO 'zahraah_cs'@'%';  -- تحديث الحالة فقط

FLUSH PRIVILEGES;
```

**الصلاحيات**:
- ✅ SELECT على Views مقنّعة
- ✅ UPDATE محدود (حالات الطلب، ملاحظات)
- ❌ الوصول لبيانات الدفع الكاملة

---

#### **Finance (مالية)**

```sql
-- حساب الفريق المالي
CREATE USER 'zahraah_finance'@'%' 
    IDENTIFIED BY 'finance_password'
    REQUIRE SSL;

-- قراءة البيانات المالية
GRANT SELECT ON zahraah_db.orders TO 'zahraah_finance'@'%';
GRANT SELECT ON zahraah_db.payments TO 'zahraah_finance'@'%';
GRANT SELECT ON zahraah_db.refunds TO 'zahraah_finance'@'%';
GRANT SELECT ON zahraah_db.wallet_transactions TO 'zahraah_finance'@'%';

FLUSH PRIVILEGES;
```

---

#### **Marketing/Analyst (تحليلات)**

```sql
-- حساب التسويق والتحليلات
CREATE USER 'zahraah_marketing'@'%' 
    IDENTIFIED BY 'marketing_password'
    REQUIRE SSL;

-- وصول محدود للتحليلات
GRANT SELECT ON zahraah_db.vw_marketing_analytics TO 'zahraah_marketing'@'%';
GRANT SELECT ON zahraah_db.vw_customer_segments TO 'zahraah_marketing'@'%';
GRANT SELECT ON zahraah_db.orders TO 'zahraah_marketing'@'%';

-- لا وصول للبيانات الشخصية الكاملة

FLUSH PRIVILEGES;
```

---

### **مصفوفة الصلاحيات | Permissions Matrix**

| الدور Role | العملاء | المنتجات | الطلبات | المدفوعات | المخزون | التحليلات |
|-----------|----------|----------|---------|-----------|---------|-----------|
| **Admin** | كامل Full | كامل | كامل | كامل | كامل | كامل |
| **App** | R/W | R/W | R/W | R/W | R/W | R |
| **ReadOnly** | R | R | R | R | R | R |
| **CS** | R (مقنّع) | R | R/W (محدود) | R (مقنّع) | R | - |
| **Finance** | R (مقنّع) | - | R | R | - | R |
| **Marketing** | R (مقنّع) | R | R | - | - | R |

**الرموز**: R = قراءة، W = كتابة، - = لا وصول

---

## 2. إخفاء البيانات الشخصية PII | PII Masking {#pii-masking}

### **تصنيف PII | PII Classification**

| المستوى Level | الأمثلة Examples | الحماية Protection |
|-------------|-----------------|-------------------|
| **عالي الحساسية** | بيانات بطاقة الدفع، كلمات المرور | ترميز، تشفير عمودي |
| **متوسط الحساسية** | رقم الهاتف، البريد الإلكتروني، العنوان | إخفاء، تشفير |
| **منخفض الحساسية** | الاسم، المدينة | إخفاء في بعض السياقات |
| **غير حساس** | المعرّفات، التواريخ، المبالغ | لا حماية إضافية |

---

### **Views مقنّعة | Masked Views**

#### **View للعملاء المقنّع**

```sql
CREATE VIEW vw_customers_masked AS
SELECT 
    customer_id,
    
    -- إخفاء الهاتف: +966501234567 → +966******567
    CONCAT(
        LEFT(phone, 4),
        REPEAT('*', LENGTH(phone) - 7),
        RIGHT(phone, 3)
    ) AS phone_masked,
    
    -- إخفاء البريد: test@example.com → t***@example.com
    CONCAT(
        LEFT(email, 1),
        REPEAT('*', LENGTH(SUBSTRING_INDEX(email, '@', 1)) - 1),
        '@',
        SUBSTRING_INDEX(email, '@', -1)
    ) AS email_masked,
    
    first_name,
    last_name,
    country,
    city,  -- غير مقنّع
    
    registration_date,
    last_activity_at,
    total_orders,
    
    created_at,
    updated_at
FROM customers
WHERE archived_at IS NULL;
```

---

#### **View للطلبات لخدمة العملاء**

```sql
CREATE VIEW vw_orders_cs AS
SELECT 
    o.order_id,
    o.order_no,
    o.customer_id,
    
    -- معلومات مقنّعة
    c.first_name,
    CONCAT(LEFT(c.phone, 4), '***', RIGHT(c.phone, 3)) AS phone_masked,
    
    o.total,
    o.currency,
    o.status,
    o.payment_method,
    
    -- لا تفاصيل الدفع الحساسة
    
    o.created_at,
    o.delivered_at
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.archived_at IS NULL;
```

---

#### **View للتحليلات المجهولة**

```sql
CREATE VIEW vw_marketing_analytics AS
SELECT 
    customer_id,  -- معرّف داخلي فقط
    -- لا أسماء، لا هواتف، لا بريد
    
    country,
    city,
    preferred_language,
    
    registration_date,
    last_activity_at,
    total_orders,
    aov,
    ltv,
    
    first_source,
    first_medium,
    first_campaign
FROM customers
WHERE archived_at IS NULL;
```

---

### **دالات الإخفاء | Masking Functions**

```sql
-- دالة لإخفاء الهاتف
DELIMITER //
CREATE FUNCTION mask_phone(phone VARCHAR(20))
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF phone IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN CONCAT(
        LEFT(phone, 4),
        REPEAT('*', GREATEST(0, LENGTH(phone) - 7)),
        RIGHT(phone, 3)
    );
END//
DELIMITER ;

-- الاستخدام
SELECT mask_phone(phone) FROM customers;
```

---

## 3. التشفير | Encryption {#encryption}

### **التشفير في الراحة | Encryption at Rest**

```ini
# في my.cnf
[mysqld]
# تفعيل التشفير الشفاف للبيانات (TDE)
early-plugin-load = keyring_file.so
keyring_file_data = /var/lib/mysql-keyring/keyring

# تشفير جميع الجداول الجديدة
default_table_encryption = ON
```

```sql
-- تشفير جدول موجود
ALTER TABLE customers ENCRYPTION = 'Y';

-- التحقق من حالة التشفير
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    CREATE_OPTIONS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'zahraah_db'
  AND CREATE_OPTIONS LIKE '%ENCRYPTION%';
```

---

### **التشفير في النقل | Encryption in Transit**

```ini
# إجبار SSL/TLS لجميع الاتصالات
[mysqld]
require_secure_transport = ON

# مسارات الشهادات
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem
```

**التحقق**:
```sql
-- التحقق من حالة SSL
SHOW STATUS LIKE 'Ssl_cipher';

-- التحقق من اتصالات SSL
SHOW STATUS LIKE 'Ssl%';
```

---

### **تشفير على مستوى العمود | Column-Level Encryption**

```sql
-- للبيانات الحساسة جداً (نادر الاستخدام)
CREATE TABLE payment_methods (
    method_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    
    -- بيانات مشفرة
    card_token VARCHAR(255),  -- من مزود الدفع (مُرمز)
    
    -- لا تخزن أبداً تفاصيل البطاقة الكاملة!
    -- استخدم الترميز (Tokenization) من مزود الدفع
    
    created_at DATETIME NOT NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

⚠️ **تحذير**: لا تخزن أبداً:
- ❌ أرقام بطاقات الائتمان الكاملة
- ❌ CVV
- ❌ PINs
- ❌ كلمات المرور بنص عادي

استخدم **Tokenization** من مزود الدفع (Moyasar، Tap، إلخ).

---

## 4. سجلات التدقيق | Audit Logs {#audit-logs}

### **جدول التدقيق | Audit Table**

```sql
CREATE TABLE audit_log (
    audit_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- من Who
    user_id BIGINT,
    user_type ENUM('customer', 'staff', 'admin', 'system') NOT NULL,
    user_email VARCHAR(255),
    
    -- ماذا What
    table_name VARCHAR(100) NOT NULL,
    action_type ENUM('INSERT', 'UPDATE', 'DELETE', 'SELECT') NOT NULL,
    record_id BIGINT,
    
    -- التفاصيل Details
    old_values JSON,  -- القيم القديمة (قبل التغيير)
    new_values JSON,  -- القيم الجديدة (بعد التغيير)
    
    -- متى When
    action_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- أين Where
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    
    -- السياق Context
    request_id VARCHAR(100),  -- لتتبع الطلبات
    session_id VARCHAR(100),
    
    INDEX idx_table_record (table_name, record_id, action_timestamp),
    INDEX idx_user_timestamp (user_id, action_timestamp),
    INDEX idx_action_timestamp (action_timestamp)
) ENGINE=InnoDB;
```

---

### **تسجيل التغييرات | Logging Changes**

#### **باستخدام Triggers**

```sql
-- Trigger لتسجيل تحديثات العملاء
DELIMITER //
CREATE TRIGGER trg_customers_audit_update
AFTER UPDATE ON customers
FOR EACH ROW
BEGIN
    IF OLD.phone != NEW.phone 
       OR OLD.email != NEW.email 
       OR OLD.first_name != NEW.first_name THEN
        
        INSERT INTO audit_log (
            user_id,
            user_type,
            table_name,
            action_type,
            record_id,
            old_values,
            new_values,
            action_timestamp
        ) VALUES (
            @current_user_id,  -- متغير جلسة
            'staff',
            'customers',
            'UPDATE',
            NEW.customer_id,
            JSON_OBJECT(
                'phone', OLD.phone,
                'email', OLD.email,
                'first_name', OLD.first_name
            ),
            JSON_OBJECT(
                'phone', NEW.phone,
                'email', NEW.email,
                'first_name', NEW.first_name
            ),
            NOW()
        );
    END IF;
END//
DELIMITER ;
```

---

#### **باستخدام Application Code (موصى به)**

```python
# في التطبيق
def update_customer(customer_id, new_data, user_id):
    # جلب القيم القديمة
    old_data = db.query("SELECT * FROM customers WHERE customer_id = %s", customer_id)
    
    # تحديث العميل
    db.execute("UPDATE customers SET ... WHERE customer_id = %s", ...)
    
    # تسجيل التدقيق
    db.execute("""
        INSERT INTO audit_log (user_id, user_type, table_name, action_type, 
                               record_id, old_values, new_values)
        VALUES (%s, 'staff', 'customers', 'UPDATE', %s, %s, %s)
    """, (user_id, customer_id, json.dumps(old_data), json.dumps(new_data)))
```

---

### **الإجراءات المُدققة | Audited Actions**

**يجب تدقيقها**:
- ✅ تغييرات بيانات العملاء (هاتف، بريد، عنوان)
- ✅ جميع معاملات الدفع والاسترداد
- ✅ تغييرات حالة الطلب (خاصة الإلغاء)
- ✅ حركات المخزون اليدوية
- ✅ تغييرات الأذونات والأدوار
- ✅ تصدير البيانات (PII)
- ✅ محاولات الوصول الفاشلة

**لا حاجة للتدقيق**:
- ❌ استعلامات SELECT العادية
- ❌ تحديثات الجلسة
- ❌ البيانات الوصفية غير الحساسة

---

## 5. إدارة الأسرار | Secret Management {#secret-management}

### **تخزين الأسرار | Storing Secrets**

⚠️ **حاسم**: لا تخزن الأسرار في الكود أبداً!

**الطرق الموصى بها**:

#### **متغيرات البيئة | Environment Variables**

```bash
# في .env (لا تُرفع للمستودع!)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=zahraah_db
DB_USER=zahraah_app
DB_PASSWORD=very_strong_password_here
DB_SSL_CA=/path/to/ca.pem
```

```python
# في التطبيق
import os
from sqlalchemy import create_engine

db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)
```

---

#### **مدير الأسرار السحابي | Cloud Secret Manager**

```python
# مثال: AWS Secrets Manager
import boto3
import json

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = client.get_secret_value(SecretId='zahraah/db/prod')
    return json.loads(secret['SecretString'])

credentials = get_db_credentials()
db_url = f"mysql+pymysql://{credentials['username']}:{credentials['password']}@..."
```

---

### **تدوير كلمات المرور | Password Rotation**

```sql
-- تدوير كلمة مرور التطبيق
ALTER USER 'zahraah_app'@'%' 
    IDENTIFIED BY 'new_strong_password';

-- إجبار انتهاء صلاحية كلمة المرور
ALTER USER 'zahraah_app'@'%' 
    PASSWORD EXPIRE INTERVAL 90 DAY;

-- التحقق من صلاحية كلمات المرور
SELECT 
    user,
    host,
    password_expired,
    password_lifetime,
    password_last_changed
FROM mysql.user
WHERE user LIKE 'zahraah%';
```

**الجدول الزمني للتدوير**:
- Admin/DBA: كل 60 يومًا
- Application: كل 90 يومًا
- ReadOnly: كل 180 يومًا

---

## 6. الامتثال GDPR | GDPR Compliance {#gdpr-compliance}

### **حقوق العملاء | Customer Rights**

#### **الحق في الوصول | Right to Access**

```sql
-- API لتصدير بيانات العميل
CREATE PROCEDURE sp_export_customer_data(IN p_customer_id BIGINT)
BEGIN
    -- معلومات الملف الشخصي
    SELECT * FROM customers WHERE customer_id = p_customer_id;
    
    -- العناوين
    SELECT * FROM addresses WHERE customer_id = p_customer_id;
    
    -- الطلبات
    SELECT * FROM orders WHERE customer_id = p_customer_id;
    
    -- المحفظة
    SELECT * FROM wallet_transactions WHERE wallet_id IN (
        SELECT wallet_id FROM wallets WHERE customer_id = p_customer_id
    );
    
    -- الموافقات
    SELECT * FROM consents WHERE customer_id = p_customer_id;
END;
```

---

#### **الحق في المحو | Right to Erasure**

```sql
-- إجراء إخفاء هوية العميل
CREATE PROCEDURE sp_anonymize_customer(IN p_customer_id BIGINT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Anonymization failed';
    END;
    
    START TRANSACTION;
    
    -- إخفاء البيانات الشخصية
    UPDATE customers SET
        phone = CONCAT('DELETED_', customer_id),
        email = CONCAT('deleted_', customer_id, '@deleted.local'),
        first_name = 'Deleted',
        last_name = 'User',
        archived_at = NOW()
    WHERE customer_id = p_customer_id;
    
    -- إخفاء العناوين
    UPDATE addresses SET
        full_name = 'Deleted User',
        phone = 'DELETED',
        address_line1 = 'DELETED',
        address_line2 = NULL,
        archived_at = NOW()
    WHERE customer_id = p_customer_id;
    
    -- الاحتفاظ بالطلبات للسجلات المالية (مطلوب قانونًا)
    -- لكن مع إخفاء البيانات الشخصية
    
    -- تسجيل الإجراء
    INSERT INTO audit_log (user_id, user_type, table_name, action_type, record_id)
    VALUES (NULL, 'system', 'customers', 'ANONYMIZE', p_customer_id);
    
    COMMIT;
END;
```

**متى يتم الإخفاء**:
- بعد 7 سنوات من آخر نشاط (متطلبات قانونية)
- عند طلب العميل (30 يومًا SLA)
- الاحتفاظ بالطلبات للسجلات الضريبية (مخفاة الهوية)

---

### **موافقات التسويق | Marketing Consents**

```sql
-- تتبع الموافقات
CREATE TABLE consent_log (
    consent_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    
    -- الموافقات
    consent_sms BOOLEAN NOT NULL,
    consent_email BOOLEAN NOT NULL,
    consent_push BOOLEAN NOT NULL,
    consent_whatsapp BOOLEAN NOT NULL,
    
    -- التفاصيل
    consent_source VARCHAR(50),  -- registration، profile_update، campaign
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    
    recorded_at DATETIME NOT NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    INDEX idx_customer_recorded (customer_id, recorded_at)
);
```

---

## 7. اختبار الأمان | Security Testing {#security-testing}

### **منع SQL Injection | Prevent SQL Injection**

⚠️ **حاسم**: استخدم Prepared Statements دائماً.

```python
# سيء - عرضة لـ SQL Injection ❌
customer_id = request.get('customer_id')
query = f"SELECT * FROM customers WHERE customer_id = {customer_id}"
cursor.execute(query)

# جيد - آمن ✅
customer_id = request.get('customer_id')
query = "SELECT * FROM customers WHERE customer_id = %s"
cursor.execute(query, (customer_id,))
```

```php
// PHP - سيء ❌
$query = "SELECT * FROM customers WHERE email = '" . $_POST['email'] . "'";

// PHP - جيد ✅
$stmt = $pdo->prepare("SELECT * FROM customers WHERE email = ?");
$stmt->execute([$_POST['email']]);
```

---

### **التحقق من صحة المدخلات | Input Validation**

```sql
-- قيود CHECK للتحقق من صحة البيانات
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    
    -- التحقق من تنسيق الهاتف (E.164)
    phone VARCHAR(20) NOT NULL,
    CONSTRAINT chk_phone_format 
        CHECK (phone REGEXP '^\\+[1-9][0-9]{1,14}$'),
    
    -- التحقق من تنسيق البريد الإلكتروني
    email VARCHAR(255),
    CONSTRAINT chk_email_format 
        CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$')
);
```

---

## 8. أمان الشبكة | Network Security {#network-security}

### **تقييد IP | IP Restriction**

```sql
-- السماح من IPs محددة فقط
-- في حساب المستخدم
CREATE USER 'zahraah_app'@'10.0.1.%'     -- شبكة داخلية
    IDENTIFIED BY 'password';

CREATE USER 'zahraah_admin'@'192.168.1.100'  -- IP محدد
    IDENTIFIED BY 'password';

-- منع الوصول من الإنترنت العام
-- لا تنشئ مستخدمين بـ '%' في الإنتاج
```

---

### **VPN/Bastion Host**

```
┌─────────────┐
│  Internet   │
└──────┬──────┘
       │
       ↓ (VPN فقط)
┌─────────────┐
│ Bastion     │
│ Host        │
└──────┬──────┘
       │
       ↓ (شبكة خاصة)
┌─────────────┐
│   MySQL     │
│  Database   │
└─────────────┘
```

**التكوين**:
1. ✅ MySQL في شبكة خاصة فقط
2. ✅ الوصول عبر VPN أو Bastion Host
3. ✅ لا منافذ عامة (لا 3306 مكشوف للإنترنت)
4. ✅ جدار حماية مع قواعد صارمة

---

## 🔗 **التنقل | Navigation**

[← السابق: 05. الفهارس والأداء | Previous: Indexes & Performance](05_Indexes_Performance.md)

[التالي: 07. النسخ الاحتياطي والاستعادة | Next: Backup & Recovery →](07_Backup_Recovery.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
