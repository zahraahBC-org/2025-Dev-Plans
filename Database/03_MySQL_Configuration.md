# 03. إعدادات MySQL | MySQL Configuration
## إعداد الخادم والتحسين | Server Setup and Optimization

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: إعداد وتحسين خادم MySQL 8.x للإنتاج  
**Purpose**: Configure and optimize MySQL 8.x server for production

**الجمهور**: مهندسو DevOps، مديرو قواعد البيانات، فريق البنية التحتية  
**Audience**: DevOps engineers, database administrators, infrastructure team

**النطاق**: إعدادات الخادم، الترميز، الأداء، الأمان  
**Scope**: Server settings, encoding, performance, security

---

## 🎯 **نظرة عامة | Overview**

يوفر هذا المستند إعدادات شاملة لخادم MySQL 8.x لمنصة التجارة الإلكترونية **زهراء**. تم تحسين الإعدادات لتحقيق التوازن بين الأداء، السلامة، وقابلية التوسع.

**المبادئ الأساسية**:
- **السلامة أولاً**: ضمان دوام البيانات عبر جميع الإعدادات
- **الأداء**: تحسين للأحمال المتوقعة في التجارة الإلكترونية
- **قابلية التوسع**: دعم النمو من 10K إلى 1M+ مستخدم
- **الأمان**: إعدادات قوية للحماية من الدخول غير المصرح به

---

## 📑 **جدول المحتويات | Table of Contents**

1. [متطلبات الإصدار | Version Requirements](#version-requirements)
2. [محرك التخزين | Storage Engine](#storage-engine)
3. [ترميز الأحرف | Character Encoding](#character-encoding)
4. [المنطقة الزمنية | Time Zone](#time-zone)
5. [وضع SQL | SQL Mode](#sql-mode)
6. [إعدادات InnoDB | InnoDB Settings](#innodb-settings)
7. [Binary Log | Binary Log](#binary-log)
8. [الأداء والتخزين المؤقت | Performance & Caching](#performance-caching)
9. [سجل الاستعلامات البطيئة | Slow Query Log](#slow-query-log)
10. [إدارة الاتصالات | Connection Management](#connection-management)
11. [الأمان والوصول | Security & Access](#security-access)
12. [phpMyAdmin | phpMyAdmin](#phpmyadmin)

---

## 1. متطلبات الإصدار | Version Requirements {#version-requirements}

### **الإصدار الموصى به | Recommended Version**

```ini
# الإصدار المطلوب
MySQL: 8.0.28 أو أحدث (آخر إصدار مستقر)
# أو
MariaDB: 10.6+ (بديل متوافق)
```

**الأسباب**:
- ✅ دعم محسّن لـ JSON
- ✅ Common Table Expressions (CTEs)
- ✅ Window Functions
- ✅ تحسينات أداء كبيرة
- ✅ دعم أفضل لـ utf8mb4
- ✅ ميزات أمان محسّنة

### **التحقق من الإصدار | Version Check**

```sql
-- التحقق من إصدار MySQL
SELECT VERSION();

-- التحقق من محرك التخزين الافتراضي
SHOW ENGINES;

-- التحقق من المتغيرات الحالية
SHOW VARIABLES LIKE '%version%';
```

---

## 2. محرك التخزين | Storage Engine {#storage-engine}

### **InnoDB فقط | InnoDB Only**

⚠️ **مهم**: استخدم **InnoDB فقط** لجميع الجداول. لا تستخدم MyISAM.

```ini
# في my.cnf أو my.ini
[mysqld]
default-storage-engine = InnoDB
```

**الأسباب**:
- ✅ دعم المعاملات ACID
- ✅ قيود المفاتيح الخارجية Foreign Keys
- ✅ استعادة الأعطال Crash Recovery
- ✅ أداء أفضل للقراءة/الكتابة المتزامنة
- ✅ قفل على مستوى الصف Row-Level Locking
- ✅ دعم النسخ الاحتياطي الساخن Hot Backup

### **التحقق من الجداول الحالية | Check Existing Tables**

```sql
-- عرض جميع الجداول ومحركات التخزين
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    ENGINE
FROM information_schema.TABLES
WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
ORDER BY TABLE_SCHEMA, TABLE_NAME;

-- تحويل جدول إلى InnoDB
ALTER TABLE table_name ENGINE = InnoDB;
```

---

## 3. ترميز الأحرف | Character Encoding {#character-encoding}

### **utf8mb4 للدعم الكامل | utf8mb4 for Full Support**

⚠️ **حاسم**: استخدم `utf8mb4` وليس `utf8` القديم لدعم جميع أحرف Unicode بما فيها الإيموجي.

```ini
# في my.cnf
[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# للتوافق مع MySQL 8.0+
character-set-client-handshake = FALSE
```

### **Collation للعربية | Collation for Arabic**

**الخيارات**:

| Collation | الوصف Description | الاستخدام Use Case |
|-----------|-------------|----------------|
| `utf8mb4_unicode_ci` | توافق عام، يدعم اللغات المتعددة | **موصى به** للاستخدام العام |
| `utf8mb4_0900_ai_ci` | MySQL 8.0+ الافتراضي، أسرع | بديل جيد في MySQL 8.0+ |
| `utf8mb4_arabic_ci` | مُحسّن للعربية | للفرز الأبجدي العربي الدقيق |
| `utf8mb4_bin` | حساس لحالة الأحرف | للبحث الدقيق |

**التوصية**: استخدم `utf8mb4_unicode_ci` كإعداد افتراضي.

### **إعداد قاعدة البيانات | Database Setup**

```sql
-- إنشاء قاعدة البيانات بالترميز الصحيح
CREATE DATABASE zahraah_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- التحقق من إعدادات قاعدة البيانات
SHOW CREATE DATABASE zahraah_db;

-- تحويل قاعدة بيانات موجودة
ALTER DATABASE zahraah_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

### **إعداد الاتصال | Connection Setup**

```sql
-- تعيين الترميز لكل جلسة
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- أو في كود التطبيق (مثال: PHP)
-- $pdo = new PDO('mysql:host=localhost;dbname=zahraah_db;charset=utf8mb4');
```

---

## 4. المنطقة الزمنية | Time Zone {#time-zone}

### **UTC دائماً في التخزين | Always Store in UTC**

⚠️ **قاعدة ذهبية**: خزّن جميع الطوابع الزمنية بـ **UTC**، واعرضها بالمنطقة الزمنية المحلية في التطبيق.

```ini
# في my.cnf
[mysqld]
default-time-zone = '+00:00'
```

### **إعداد المناطق الزمنية | Time Zone Setup**

```sql
-- التحقق من المنطقة الزمنية الحالية
SELECT @@global.time_zone, @@session.time_zone;

-- تعيين المنطقة الزمنية العالمية
SET GLOBAL time_zone = '+00:00';

-- تعيين المنطقة الزمنية للجلسة
SET time_zone = '+00:00';
```

### **تحويل المنطقة الزمنية | Time Zone Conversion**

```sql
-- التخزين: دائماً UTC
INSERT INTO orders (created_at) VALUES (UTC_TIMESTAMP());

-- العرض: تحويل إلى +03:00 (السعودية)
SELECT 
    order_id,
    created_at AS utc_time,
    CONVERT_TZ(created_at, '+00:00', '+03:00') AS saudi_time
FROM orders;

-- أو في التطبيق (موصى به)
-- let localTime = new Date(utcTimestamp).toLocaleString('ar-SA', { timeZone: 'Asia/Riyadh' });
```

**المناطق الزمنية الشائعة**:
- السعودية: `+03:00` (Asia/Riyadh)
- الإمارات: `+04:00` (Asia/Dubai)
- مصر: `+02:00` (Africa/Cairo)

---

## 5. وضع SQL | SQL Mode {#sql-mode}

### **وضع صارم للسلامة | Strict Mode for Safety**

```ini
# في my.cnf
[mysqld]
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
```

**شرح كل وضع**:

| الوضع Mode | الوصف Description | الفائدة Benefit |
|------|-------------|-------------|
| `STRICT_TRANS_TABLES` | رفض القيم غير الصالحة في المعاملات | منع إدخال بيانات خاطئة |
| `NO_ZERO_DATE` | منع '0000-00-00' كتاريخ | تواريخ صالحة فقط |
| `NO_ZERO_IN_DATE` | منع '2025-00-01' | أشهر وأيام صالحة |
| `ERROR_FOR_DIVISION_BY_ZERO` | خطأ عند القسمة على صفر | منع حسابات خاطئة |
| `NO_ENGINE_SUBSTITUTION` | خطأ إذا كان المحرك المطلوب غير متاح | ضمان استخدام InnoDB |

### **التحقق والتعيين | Check and Set**

```sql
-- التحقق من وضع SQL الحالي
SELECT @@sql_mode;

-- تعيين وضع SQL للجلسة
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- تعيين وضع SQL عالميًا
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

---

## 6. إعدادات InnoDB | InnoDB Settings {#innodb-settings}

### **Buffer Pool (الأهم) | Buffer Pool (Most Important)**

```ini
# في my.cnf
[mysqld]
# تخصيص 70-80% من RAM على خادم مخصص
innodb_buffer_pool_size = 8G  # مثال: لخادم بذاكرة 12GB

# تقسيم Buffer Pool لأداء أفضل
innodb_buffer_pool_instances = 8  # عدد النوى أو 8 (أيهما أقل)

# تحميل Buffer Pool عند بدء التشغيل
innodb_buffer_pool_dump_at_shutdown = 1
innodb_buffer_pool_load_at_startup = 1
```

**حساب الحجم**:
```
إجمالي RAM    →  Buffer Pool Size
4 GB           →  2.8 GB (70%)
8 GB           →  5.6 GB (70%)
16 GB          →  12 GB (75%)
32 GB          →  24 GB (75%)
64 GB+         →  80% من RAM
```

### **ملفات السجل | Log Files**

```ini
# حجم ملفات Redo Log
innodb_log_file_size = 1G  # أكبر = أداء كتابة أفضل
innodb_log_files_in_group = 2

# حجم Buffer للسجل
innodb_log_buffer_size = 16M

# سياسة مزامنة السجل
innodb_flush_log_at_trx_commit = 1  # أكثر أماناً (موصى به)
# 0 = أسرع لكن أقل أماناً
# 1 = أكثر أماناً (يكتب في كل معاملة)
# 2 = توازن (يكتب كل ثانية)
```

### **إعدادات إضافية | Additional Settings**

```ini
# ملف لكل جدول (موصى به)
innodb_file_per_table = ON

# طريقة مزامنة الملفات
innodb_flush_method = O_DIRECT  # Linux: تجنب التخزين المؤقت المزدوج

# عدد I/O threads
innodb_read_io_threads = 4
innodb_write_io_threads = 4

# حجم الصفحة (افتراضي 16K - جيد لمعظم الحالات)
innodb_page_size = 16K

# قفل الانتظار
innodb_lock_wait_timeout = 50  # ثواني
```

---

## 7. Binary Log | Binary Log {#binary-log}

### **تفعيل Binary Log | Enable Binary Log**

⚠️ **حاسم**: ضروري للنسخ المتماثل واستعادة النقطة الزمنية.

```ini
# في my.cnf
[mysqld]
# تفعيل Binary Log
log_bin = /var/log/mysql/mysql-bin
server-id = 1  # فريد لكل خادم

# تنسيق Binary Log
binlog_format = ROW  # موصى به للتحليلات

# فترة انتهاء صلاحية Binary Logs (أيام)
binlog_expire_logs_seconds = 1209600  # 14 يوم

# حجم ملف Binary Log الأقصى
max_binlog_size = 100M

# مزامنة Binary Log
sync_binlog = 1  # الأكثر أماناً

# حد GTID (لـ MySQL 8.0+)
gtid_mode = ON
enforce_gtid_consistency = ON
```

### **صيانة Binary Logs | Binary Log Maintenance**

```sql
-- عرض Binary Logs الحالية
SHOW BINARY LOGS;

-- حذف Binary Logs القديمة
PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);

-- حذف حتى ملف معين
PURGE BINARY LOGS TO 'mysql-bin.000100';

-- تدوير Binary Logs
FLUSH LOGS;
```

---

## 8. الأداء والتخزين المؤقت | Performance & Caching {#performance-caching}

### **إعدادات الجداول المؤقتة | Temporary Table Settings**

```ini
[mysqld]
# حجم الجداول المؤقتة
tmp_table_size = 64M
max_heap_table_size = 64M

# موقع الجداول المؤقتة
tmpdir = /tmp
```

### **إعدادات الفرز | Sort Settings**

```ini
# حجم buffer للفرز
sort_buffer_size = 2M  # لكل اتصال - لا تفرط

# حجم buffer للقراءة
read_buffer_size = 2M
read_rnd_buffer_size = 4M

# حجم buffer للانضمام
join_buffer_size = 2M
```

### **إعدادات ذاكرة التخزين المؤقت | Cache Settings**

```ini
# ذاكرة التخزين المؤقت للاستعلامات (معطلة افتراضياً في MySQL 8.0)
# لا تفعّلها إلا إذا كان لديك سبب محدد
query_cache_type = 0
query_cache_size = 0

# ذاكرة التخزين المؤقت للجداول
table_open_cache = 4000
table_definition_cache = 2000

# ذاكرة التخزين المؤقت للـ threads
thread_cache_size = 50
```

### **مراقبة الأداء | Performance Monitoring**

```sql
-- عرض حالة Buffer Pool
SHOW STATUS LIKE 'Innodb_buffer_pool%';

-- نسبة إصابة Buffer Pool (يجب أن تكون > 99%)
SELECT 
    (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100 
    AS buffer_pool_hit_rate
FROM 
    (SELECT 
        VARIABLE_VALUE AS Innodb_buffer_pool_reads 
     FROM performance_schema.global_status 
     WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads') reads,
    (SELECT 
        VARIABLE_VALUE AS Innodb_buffer_pool_read_requests 
     FROM performance_schema.global_status 
     WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests') requests;

-- عرض الجداول المؤقتة
SHOW STATUS LIKE 'Created_tmp%';
```

---

## 9. سجل الاستعلامات البطيئة | Slow Query Log {#slow-query-log}

### **تفعيل السجل البطيء | Enable Slow Log**

```ini
# في my.cnf
[mysqld]
# تفعيل سجل الاستعلامات البطيئة
slow_query_log = ON
slow_query_log_file = /var/log/mysql/slow-query.log

# عتبة الوقت (ثواني)
long_query_time = 0.2  # 200ms

# تسجيل الاستعلامات التي لا تستخدم الفهارس
log_queries_not_using_indexes = ON

# حد للاستعلامات بدون فهارس (لتجنب السجل الكبير)
log_throttle_queries_not_using_indexes = 10
```

### **تحليل الاستعلامات البطيئة | Analyze Slow Queries**

```bash
# استخدام mysqldumpslow
mysqldumpslow -s t -t 10 /var/log/mysql/slow-query.log

# الخيارات:
# -s t : فرز حسب الوقت
# -s c : فرز حسب العدد
# -s l : فرز حسب وقت القفل
# -t 10 : أعلى 10
```

```sql
-- تفعيل/تعطيل ديناميكياً
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 0.2;

-- عرض الإعدادات الحالية
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';
```

---

## 10. إدارة الاتصالات | Connection Management {#connection-management}

### **حدود الاتصالات | Connection Limits**

```ini
# في my.cnf
[mysqld]
# الحد الأقصى للاتصالات
max_connections = 500  # اضبط حسب الحاجة

# مهلة الانتظار للاتصال غير النشط
wait_timeout = 600  # 10 دقائق
interactive_timeout = 600

# حد الاتصالات لكل مستخدم
max_user_connections = 100

# حجم حزمة الاتصال الأقصى
max_allowed_packet = 64M
```

### **حساب max_connections | Calculate max_connections**

```
الصيغة التقريبية:
max_connections = (RAM المتاح - Buffer Pool - OS) / حجم الاتصال

حجم الاتصال ≈ sort_buffer + read_buffer + join_buffer + thread_stack
              ≈ 2M + 2M + 2M + 256K ≈ 6-7MB

مثال: خادم 16GB مع 12GB buffer pool:
(4GB * 1024) / 7MB ≈ 585 اتصال
حد آمن: 500 اتصال
```

### **مراقبة الاتصالات | Monitor Connections**

```sql
-- عرض الاتصالات الحالية
SHOW PROCESSLIST;

-- عرض حالة الاتصالات
SHOW STATUS LIKE 'Threads%';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Max_used_connections';

-- قتل اتصال معين
KILL CONNECTION connection_id;
```

---

## 11. الأمان والوصول | Security & Access {#security-access}

### **حسابات المستخدمين | User Accounts**

⚠️ **مهم**: لا تستخدم `root` للتطبيق. أنشئ حسابات مخصصة.

```sql
-- حساب التطبيق (قراءة/كتابة)
CREATE USER 'zahraah_app'@'%' 
    IDENTIFIED BY 'strong_password_here'
    REQUIRE SSL;

GRANT SELECT, INSERT, UPDATE, DELETE 
    ON zahraah_db.* 
    TO 'zahraah_app'@'%';

-- حساب القراءة فقط (للتحليلات)
CREATE USER 'zahraah_readonly'@'%' 
    IDENTIFIED BY 'readonly_password'
    REQUIRE SSL;

GRANT SELECT 
    ON zahraah_db.* 
    TO 'zahraah_readonly'@'%';

-- حساب النسخ الاحتياطي
CREATE USER 'zahraah_backup'@'localhost' 
    IDENTIFIED BY 'backup_password';

GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER 
    ON zahraah_db.* 
    TO 'zahraah_backup'@'localhost';

-- تطبيق التغييرات
FLUSH PRIVILEGES;
```

### **سياسة كلمات المرور | Password Policy**

```sql
-- تعيين سياسة كلمات المرور
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;

-- انتهاء صلاحية كلمة المرور
ALTER USER 'zahraah_app'@'%' 
    PASSWORD EXPIRE INTERVAL 90 DAY;

-- تغيير كلمة المرور
ALTER USER 'zahraah_app'@'%' 
    IDENTIFIED BY 'new_strong_password';
```

### **تشفير الاتصال | Connection Encryption**

```ini
# في my.cnf
[mysqld]
# تفعيل SSL/TLS
require_secure_transport = ON

# مسارات الشهادات
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem
```

### **تقييد IP | IP Restriction**

```sql
-- السماح من IPs محددة فقط
CREATE USER 'zahraah_app'@'10.0.1.%' 
    IDENTIFIED BY 'password';

CREATE USER 'zahraah_app'@'192.168.1.100' 
    IDENTIFIED BY 'password';

-- حذف مستخدم
DROP USER 'username'@'host';
```

---

## 12. phpMyAdmin | phpMyAdmin {#phpmyadmin}

### **تكوين الوصول | Access Configuration**

```ini
# في config.inc.php
$cfg['Servers'][$i]['auth_type'] = 'cookie';
$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = false;

# قيود الإنتاج
$cfg['AllowArbitraryServer'] = false;
$cfg['LoginCookieValidity'] = 1800; # 30 دقيقة
```

### **الأمان | Security**

**للإنتاج**:
1. ✅ وصول VPN/IP allowlist فقط
2. ✅ استخدام حسابات قراءة فقط
3. ✅ تعطيل جميع عمليات DDL/DML
4. ✅ تفعيل 2FA إن أمكن
5. ✅ تسجيل جميع الإجراءات

**للتطوير/التجهيز**:
1. ✅ وصول فريق التطوير فقط
2. ✅ تسجيل التدقيق مفعّل
3. ✅ نسخ احتياطي قبل أي تغيير

### **حساب محدود لـ phpMyAdmin | Limited phpMyAdmin Account**

```sql
-- حساب قراءة فقط للإنتاج
CREATE USER 'phpmyadmin_readonly'@'%' 
    IDENTIFIED BY 'secure_password'
    REQUIRE SSL;

GRANT SELECT, SHOW VIEW 
    ON zahraah_db.* 
    TO 'phpmyadmin_readonly'@'%';

-- حساب كامل للتطوير فقط
CREATE USER 'phpmyadmin_dev'@'dev_ip' 
    IDENTIFIED BY 'dev_password';

GRANT ALL PRIVILEGES 
    ON zahraah_dev_db.* 
    TO 'phpmyadmin_dev'@'dev_ip';
```

---

## 📊 **ملف التكوين الكامل | Complete Configuration File**

```ini
# /etc/mysql/my.cnf أو /etc/my.cnf
# إعدادات MySQL 8.x لمنصة زهراء للتجارة الإلكترونية

[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
# ========================================
# الأساسيات | Basics
# ========================================
server-id = 1
default-storage-engine = InnoDB
default-time-zone = '+00:00'

# ========================================
# الترميز | Character Set
# ========================================
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
character-set-client-handshake = FALSE

# ========================================
# وضع SQL | SQL Mode
# ========================================
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION

# ========================================
# InnoDB
# ========================================
# Buffer Pool (اضبط حسب RAM المتاح)
innodb_buffer_pool_size = 8G
innodb_buffer_pool_instances = 8
innodb_buffer_pool_dump_at_shutdown = 1
innodb_buffer_pool_load_at_startup = 1

# Log Files
innodb_log_file_size = 1G
innodb_log_files_in_group = 2
innodb_log_buffer_size = 16M
innodb_flush_log_at_trx_commit = 1

# إعدادات أخرى
innodb_file_per_table = ON
innodb_flush_method = O_DIRECT
innodb_read_io_threads = 4
innodb_write_io_threads = 4
innodb_lock_wait_timeout = 50

# ========================================
# Binary Log
# ========================================
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
binlog_expire_logs_seconds = 1209600
max_binlog_size = 100M
sync_binlog = 1

# GTID
gtid_mode = ON
enforce_gtid_consistency = ON

# ========================================
# سجل الاستعلامات البطيئة | Slow Query Log
# ========================================
slow_query_log = ON
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 0.2
log_queries_not_using_indexes = ON
log_throttle_queries_not_using_indexes = 10

# ========================================
# الاتصالات | Connections
# ========================================
max_connections = 500
wait_timeout = 600
interactive_timeout = 600
max_user_connections = 100
max_allowed_packet = 64M

# ========================================
# الأداء | Performance
# ========================================
tmp_table_size = 64M
max_heap_table_size = 64M
sort_buffer_size = 2M
read_buffer_size = 2M
read_rnd_buffer_size = 4M
join_buffer_size = 2M
table_open_cache = 4000
table_definition_cache = 2000
thread_cache_size = 50

# ========================================
# الأمان | Security
# ========================================
require_secure_transport = ON
local_infile = OFF

# ========================================
# السجلات | Logging
# ========================================
log_error = /var/log/mysql/error.log
general_log = OFF
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 02. معمارية قاعدة البيانات | Previous: Database Architecture](02_Database_Architecture.md)

[التالي: 04. معايير تصميم المخطط | Next: Schema Design Standards →](04_Schema_Design.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
