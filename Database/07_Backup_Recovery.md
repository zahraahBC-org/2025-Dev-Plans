# 07. النسخ الاحتياطي والاستعادة | Backup & Recovery
## استراتيجيات النسخ الاحتياطي والتعافي من الكوارث | Backup Strategies and Disaster Recovery

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد استراتيجيات النسخ الاحتياطي والاستعادة  
**Purpose**: Define backup and recovery strategies

**الجمهور**: مهندسو DevOps، مديرو قواعد البيانات، فريق البنية التحتية  
**Audience**: DevOps engineers, DBAs, infrastructure team

**النطاق**: النسخ الاحتياطي، الاستعادة، RPO/RTO، التعافي من الكوارث  
**Scope**: Backup, recovery, RPO/RTO, disaster recovery

---

## 🎯 **الأهداف | Objectives**

### **أهداف الاستعادة | Recovery Objectives**

| المقياس Metric | الهدف Target | الوصف Description |
|--------------|-------------|------------------|
| **RPO** | ≤ 15 دقيقة | نقطة الاستعادة Recovery Point Objective - أقصى فقد بيانات مقبول |
| **RTO** | ≤ 60 دقيقة | وقت الاستعادة Recovery Time Objective - وقت استعادة الخدمة |
| **تكرار النسخ** | يومي + Binlog مستمر | النسخ الكامل يومياً، binlog كل دقيقة |
| **الاحتفاظ** | 7/14/30 يوم | 7 أيام يومي، 14 يوم أسبوعي، 30 يوم شهري |
| **اختبار الاستعادة** | ربع سنوي | اختبار استعادة كاملة كل 3 أشهر |

---

## 📑 **جدول المحتويات | Table of Contents**

1. [استراتيجية النسخ الاحتياطي | Backup Strategy](#backup-strategy)
2. [النسخ الاحتياطي الكامل | Full Backup](#full-backup)
3. [النسخ الاحتياطي التزايدي | Incremental Backup](#incremental-backup)
4. [استعادة النقطة الزمنية PITR | Point-in-Time Recovery](#pitr)
5. [التعافي من الكوارث DR | Disaster Recovery](#disaster-recovery)
6. [اختبار الاستعادة | Recovery Testing](#recovery-testing)
7. [التخزين والاحتفاظ | Storage & Retention](#storage-retention)
8. [كتب الإجراءات Runbooks | Runbooks](#runbooks)

---

## 1. استراتيجية النسخ الاحتياطي | Backup Strategy {#backup-strategy}

### **نهج متعدد الطبقات | Multi-Layered Approach**

```
┌──────────────────────────────────────────────────┐
│  الطبقة 1: نسخ كامل يومي                        │
│  Layer 1: Daily Full Backup                      │
│  - يومياً عند 2:00 صباحاً                       │
│  - الاحتفاظ: 7 أيام                             │
└──────────────────────────────────────────────────┘
                    +
┌──────────────────────────────────────────────────┐
│  الطبقة 2: Binary Logs مستمر                    │
│  Layer 2: Continuous Binary Logs                │
│  - مستمر (كل دقيقة)                             │
│  - RPO: 15 دقيقة                                │
└──────────────────────────────────────────────────┘
                    +
┌──────────────────────────────────────────────────┐
│  الطبقة 3: نسخ أسبوعي/شهري                     │
│  Layer 3: Weekly/Monthly Archives                │
│  - أسبوعي: كل أحد                               │
│  - شهري: أول يوم من الشهر                       │
└──────────────────────────────────────────────────┘
```

---

## 2. النسخ الاحتياطي الكامل | Full Backup {#full-backup}

### **باستخدام mysqldump | Using mysqldump**

#### **نسخ احتياطي كامل بسيط**

```bash
#!/bin/bash
# backup-full.sh

# المتغيرات
DB_NAME="zahraah_db"
DB_USER="zahraah_backup"
DB_PASS="backup_password"
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/full_${DB_NAME}_${DATE}.sql.gz"

# إنشاء مجلد النسخ الاحتياطي
mkdir -p $BACKUP_DIR

# تنفيذ النسخ الاحتياطي
mysqldump \
    --user=$DB_USER \
    --password=$DB_PASS \
    --host=localhost \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --set-gtid-purged=ON \
    --master-data=2 \
    --flush-logs \
    $DB_NAME | gzip > $BACKUP_FILE

# التحقق من النجاح
if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_FILE"
    
    # حساب checksum
    sha256sum $BACKUP_FILE > ${BACKUP_FILE}.sha256
    
    # رفع إلى S3
    aws s3 cp $BACKUP_FILE s3://zahraah-backups/mysql/full/
    aws s3 cp ${BACKUP_FILE}.sha256 s3://zahraah-backups/mysql/full/
else
    echo "Backup failed!"
    # إرسال تنبيه
    exit 1
fi

# حذف النسخ القديمة (أكثر من 7 أيام)
find $BACKUP_DIR -name "full_*.sql.gz" -mtime +7 -delete
```

**الخيارات المهمة**:
- `--single-transaction`: نسخ احتياطي متسق بدون قفل الجداول
- `--master-data=2`: يحفظ موضع binlog
- `--flush-logs`: يبدأ binlog جديد بعد النسخ
- `--set-gtid-purged=ON`: للاستعادة مع GTID

---

### **باستخدام Percona XtraBackup | Using Percona XtraBackup**

للقواعد الكبيرة (> 100GB):

```bash
#!/bin/bash
# backup-xtrabackup.sh

BACKUP_DIR="/backups/xtrabackup"
DATE=$(date +%Y%m%d_%H%M%S)

# نسخ احتياطي كامل
xtrabackup \
    --backup \
    --user=zahraah_backup \
    --password=backup_password \
    --target-dir=$BACKUP_DIR/full_$DATE \
    --compress \
    --compress-threads=4

# التحضير للاستعادة
xtrabackup \
    --prepare \
    --target-dir=$BACKUP_DIR/full_$DATE

# رفع إلى S3
aws s3 sync $BACKUP_DIR/full_$DATE s3://zahraah-backups/xtrabackup/full_$DATE/
```

**المزايا**:
- ✅ أسرع للقواعد الكبيرة
- ✅ نسخ احتياطي ساخن (لا توقف)
- ✅ استعادة أسرع
- ✅ دعم النسخ التزايدي

---

## 3. النسخ الاحتياطي التزايدي | Incremental Backup {#incremental-backup}

### **نسخ Binary Logs | Binary Log Backup**

```bash
#!/bin/bash
# backup-binlog.sh (يُشغل كل ساعة)

BINLOG_DIR="/var/lib/mysql"
BACKUP_DIR="/backups/binlog"
DATE=$(date +%Y%m%d_%H%M%S)

# نسخ binary logs
mysqlbinlog \
    --read-from-remote-server \
    --host=localhost \
    --user=zahraah_backup \
    --password=backup_password \
    --raw \
    --result-file=$BACKUP_DIR/binlog_$DATE \
    mysql-bin.000001

# ضغط
gzip $BACKUP_DIR/binlog_$DATE*

# رفع إلى S3
aws s3 sync $BACKUP_DIR s3://zahraah-backups/binlog/

# حذف binlogs المحلية القديمة (> 2 أيام)
find $BACKUP_DIR -name "binlog_*.gz" -mtime +2 -delete
```

---

### **جدولة النسخ | Backup Schedule**

```cron
# في crontab
# نسخ كامل يومياً عند 2:00 صباحاً
0 2 * * * /scripts/backup-full.sh >> /var/log/backup-full.log 2>&1

# نسخ binlog كل ساعة
0 * * * * /scripts/backup-binlog.sh >> /var/log/backup-binlog.log 2>&1

# نسخ أسبوعي كل أحد
0 3 * * 0 /scripts/backup-weekly.sh >> /var/log/backup-weekly.log 2>&1

# نسخ شهري في أول يوم
0 4 1 * * /scripts/backup-monthly.sh >> /var/log/backup-monthly.log 2>&1
```

---

## 4. استعادة النقطة الزمنية PITR | Point-in-Time Recovery {#pitr}

### **السيناريو | Scenario**
حدث خطأ (حذف بيانات خاطئ) في 2025-01-08 الساعة 14:30. نحتاج للاستعادة إلى 14:25.

### **خطوات الاستعادة | Recovery Steps**

#### **الخطوة 1: استعادة النسخ الكامل**

```bash
# إيقاف MySQL
systemctl stop mysql

# استعادة من آخر نسخ كامل (قبل الحادث)
# النسخ الكامل من 2025-01-08 الساعة 02:00
gunzip < /backups/mysql/full_zahraah_db_20250108_020000.sql.gz | \
    mysql -u root -p zahraah_db

# بدء MySQL
systemctl start mysql
```

---

#### **الخطوة 2: تطبيق Binary Logs**

```bash
# إيجاد binlogs بين 02:00 و 14:25
ls -la /backups/binlog/

# تطبيق binlogs
mysqlbinlog \
    --start-datetime="2025-01-08 02:00:00" \
    --stop-datetime="2025-01-08 14:25:00" \
    /backups/binlog/mysql-bin.000050 \
    /backups/binlog/mysql-bin.000051 \
    | mysql -u root -p zahraah_db

# التحقق من البيانات
mysql -u root -p -e "SELECT COUNT(*) FROM zahraah_db.orders WHERE created_at < '2025-01-08 14:25:00';"
```

---

#### **الخطوة 3: التحقق | Verification**

```sql
-- التحقق من سلامة البيانات
-- 1. عدد الصفوف
SELECT 
    TABLE_NAME,
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'zahraah_db'
ORDER BY TABLE_NAME;

-- 2. آخر سجل
SELECT MAX(created_at) FROM orders;
SELECT MAX(created_at) FROM payments;
SELECT MAX(movement_date) FROM inventory_ledger;

-- 3. checksums
CHECKSUM TABLE customers, orders, payments;
```

---

## 5. التعافي من الكوارث DR | Disaster Recovery {#disaster-recovery}

### **معمارية DR | DR Architecture**

```
┌─────────────────┐         النسخ المتماثل         ┌─────────────────┐
│  Primary Site   │ ─────── Replication ────────→  │  DR Site        │
│  (إنتاج)       │         (غير متزامن)           │  (احتياطي)     │
│                 │                                 │                 │
│  MySQL Primary  │                                 │  MySQL Replica  │
│  - قراءة/كتابة │                                 │  - قراءة فقط   │
│  - الإنتاج     │                                 │  - جاهز للتبديل│
└─────────────────┘                                 └─────────────────┘
```

### **إعداد النسخ المتماثل | Replication Setup**

#### **في Primary Server**

```sql
-- تكوين Primary
-- في my.cnf
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON

-- إنشاء مستخدم النسخ المتماثل
CREATE USER 'repl_user'@'dr_site_ip' 
    IDENTIFIED BY 'replication_password'
    REQUIRE SSL;

GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'dr_site_ip';
FLUSH PRIVILEGES;

-- الحصول على موضع Primary
SHOW MASTER STATUS;
```

---

#### **في DR Server (Replica)**

```sql
-- تكوين Replica
-- في my.cnf
[mysqld]
server-id = 2
read_only = ON
relay_log = /var/log/mysql/relay-bin
gtid_mode = ON
enforce_gtid_consistency = ON

-- إعداد النسخ المتماثل
CHANGE MASTER TO
    MASTER_HOST = 'primary_server_ip',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'replication_password',
    MASTER_AUTO_POSITION = 1,  -- استخدام GTID
    MASTER_SSL = 1;

-- بدء النسخ المتماثل
START SLAVE;

-- التحقق من الحالة
SHOW SLAVE STATUS\G
```

---

### **مراقبة النسخ المتماثل | Monitor Replication**

```sql
-- التحقق من التأخير
SHOW SLAVE STATUS\G

-- المؤشرات المهمة:
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
-- Seconds_Behind_Master: < 60  (التأخير بالثواني)

-- استعلام مراقبة
SELECT 
    IF(Slave_IO_Running = 'Yes' AND Slave_SQL_Running = 'Yes', 
       'OK', 
       'ERROR') AS replication_status,
    Seconds_Behind_Master AS lag_seconds
FROM 
    (SHOW SLAVE STATUS) AS status;
```

**التنبيهات**:
- ⚠️ إذا Slave_IO_Running = No
- ⚠️ إذا Slave_SQL_Running = No
- ⚠️ إذا Seconds_Behind_Master > 300 (5 دقائق)

---

### **التبديل للـ DR | Failover to DR**

#### **التبديل المخطط | Planned Failover**

```bash
# 1. إيقاف الكتابة على Primary
# في التطبيق: تفعيل وضع الصيانة

# 2. التحقق من مزامنة Replica
mysql -h dr_server -e "SHOW SLAVE STATUS\G" | grep "Seconds_Behind_Master"

# 3. إيقاف النسخ المتماثل على Replica
mysql -h dr_server -e "STOP SLAVE;"

# 4. ترقية Replica ليصبح Primary
mysql -h dr_server -e "SET GLOBAL read_only = OFF;"

# 5. تحديث DNS/Load Balancer للإشارة إلى DR

# 6. اختبار الكتابة
mysql -h dr_server -e "INSERT INTO test_table VALUES (...);"
```

---

#### **التبديل الطارئ | Emergency Failover**

```bash
# إذا فشل Primary بشكل كامل

# 1. تحقق من آخر GTID على Replica
mysql -h dr_server -e "SELECT @@GLOBAL.gtid_executed;"

# 2. ترقية Replica فوراً
mysql -h dr_server -e "
    STOP SLAVE;
    RESET SLAVE ALL;
    SET GLOBAL read_only = OFF;
"

# 3. تحديث DNS فوراً

# 4. إشعار الفريق
```

---

## 6. اختبار الاستعادة | Recovery Testing {#recovery-testing}

### **الجدول الزمني | Testing Schedule**

| التكرار Frequency | النطاق Scope | الهدف Goal |
|------------------|-------------|-----------|
| **شهري** | استعادة جدول واحد | التحقق من إجراءات الاستعادة |
| **ربع سنوي** | استعادة قاعدة بيانات كاملة | التحقق من RPO/RTO |
| **نصف سنوي** | تمرين تبديل DR كامل | التحقق من استمرارية الأعمال |

---

### **اختبار الاستعادة الربع سنوي | Quarterly Recovery Test**

```bash
#!/bin/bash
# test-recovery.sh

# 1. إنشاء قاعدة بيانات اختبار
mysql -u root -p -e "CREATE DATABASE zahraah_test;"

# 2. استعادة آخر نسخ كامل
gunzip < /backups/mysql/full_zahraah_db_latest.sql.gz | \
    mysql -u root -p zahraah_test

# 3. تطبيق binlogs
mysqlbinlog /backups/binlog/mysql-bin.* | \
    mysql -u root -p zahraah_test

# 4. التحقق من البيانات
mysql -u root -p zahraah_test -e "
    SELECT 
        (SELECT COUNT(*) FROM customers) as customer_count,
        (SELECT COUNT(*) FROM orders) as order_count,
        (SELECT COUNT(*) FROM payments) as payment_count,
        (SELECT MAX(created_at) FROM orders) as last_order;
"

# 5. مقارنة مع الإنتاج
# (عدد الصفوف، checksums، إلخ)

# 6. التنظيف
mysql -u root -p -e "DROP DATABASE zahraah_test;"

# 7. توثيق النتائج
echo "Recovery test completed at $(date)" >> /var/log/recovery-test.log
```

---

### **قائمة فحص الاستعادة | Recovery Checklist**

- [ ] النسخ الاحتياطي موجود وغير تالف
- [ ] checksum يتطابق
- [ ] استعادة النسخ الكامل نجحت
- [ ] binlogs متوفرة للفترة المطلوبة
- [ ] تطبيق binlogs نجح
- [ ] عدد الصفوف يتطابق
- [ ] checksums الجداول تتطابق
- [ ] آخر سجل في الوقت الصحيح
- [ ] القيود والفهارس سليمة
- [ ] التطبيق يتصل بنجاح
- [ ] اختبار وظيفي نجح (إنشاء طلب، إلخ)

---

## 7. التخزين والاحتفاظ | Storage & Retention {#storage-retention}

### **سياسة الاحتفاظ | Retention Policy**

| نوع النسخ Backup Type | الاحتفاظ Retention | التخزين Storage | التكلفة Cost |
|---------------------|------------------|----------------|-------------|
| **يومي كامل** | 7 أيام | S3 Standard | متوسط |
| **أسبوعي** | 4 أسابيع (شهر) | S3 Standard | متوسط |
| **شهري** | 12 شهر (سنة) | S3 Glacier | منخفض |
| **سنوي** | 7 سنوات | S3 Deep Archive | منخفض جداً |
| **Binary Logs** | 14 يوم | S3 Standard | متوسط |

---

### **التخزين على S3 | S3 Storage**

```bash
# هيكل المجلدات
s3://zahraah-backups/
├── mysql/
│   ├── full/
│   │   ├── full_zahraah_db_20250108_020000.sql.gz
│   │   ├── full_zahraah_db_20250108_020000.sql.gz.sha256
│   │   └── ...
│   ├── weekly/
│   │   ├── weekly_zahraah_db_20250105.sql.gz
│   │   └── ...
│   └── monthly/
│       ├── monthly_zahraah_db_202501.sql.gz
│       └── ...
└── binlog/
    ├── binlog_20250108_000000.gz
    └── ...
```

---

### **دورة حياة S3 | S3 Lifecycle**

```json
{
  "Rules": [
    {
      "Id": "DailyBackupLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "mysql/full/"
      },
      "Expiration": {
        "Days": 7
      }
    },
    {
      "Id": "WeeklyToGlacier",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "mysql/weekly/"
      },
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "MonthlyToDeepArchive",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "mysql/monthly/"
      },
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 2555
      }
    }
  ]
}
```

---

## 8. كتب الإجراءات Runbooks | Runbooks {#runbooks}

### **Runbook: تلف قاعدة البيانات | Database Corruption**

**الأعراض**:
- أخطاء في سجل MySQL
- استعلامات تفشل
- جداول غير قابلة للقراءة

**الإجراءات**:

```bash
# 1. التحقق من حالة الجداول
mysqlcheck -u root -p --all-databases

# 2. إصلاح الجداول التالفة
mysqlcheck -u root -p --auto-repair zahraah_db

# 3. إذا فشل الإصلاح، استعد من النسخ الاحتياطي
# (اتبع خطوات PITR من أعلاه)

# 4. التحقق بعد الاستعادة
mysqlcheck -u root -p --check --extended zahraah_db
```

---

### **Runbook: فشل النسخ الاحتياطي | Backup Failure**

**الأعراض**:
- سكريبت النسخ الاحتياطي فشل
- لا يوجد ملف نسخ احتياطي جديد
- تنبيه من نظام المراقبة

**الإجراءات**:

```bash
# 1. التحقق من السجلات
tail -100 /var/log/backup-full.log

# 2. التحقق من المساحة
df -h /backups

# 3. التحقق من أذونات المستخدم
mysql -u zahraah_backup -p -e "SHOW GRANTS;"

# 4. محاولة يدوية
/scripts/backup-full.sh

# 5. إخطار الفريق إذا فشل
```

---

### **Runbook: استعادة طارئة كاملة | Full Emergency Recovery**

**السيناريو**: فشل خادم قاعدة البيانات بالكامل.

**الإجراءات**:

```bash
# 1. تجهيز خادم جديد
# (اتبع خطوات الإعداد من 03_MySQL_Configuration.md)

# 2. استعادة آخر نسخ كامل
gunzip < /backups/mysql/full_zahraah_db_latest.sql.gz | \
    mysql -u root -p

# 3. تطبيق جميع binlogs منذ آخر نسخ كامل
mysqlbinlog /backups/binlog/mysql-bin.* | mysql -u root -p

# 4. التحقق من البيانات
# (اتبع قائمة الفحص من أعلاه)

# 5. تحديث DNS للإشارة إلى الخادم الجديد

# 6. اختبار التطبيق

# 7. توثيق الحادث
```

**الوقت المتوقع**: 45-60 دقيقة (RTO)

---

## 🔗 **التنقل | Navigation**

[← السابق: 06. الأمان والخصوصية | Previous: Security & Privacy](06_Security_Privacy.md)

[التالي: 08. نظام المحفظة | Next: Wallet System →](08_Wallet_System.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
