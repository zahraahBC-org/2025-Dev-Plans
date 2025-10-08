# 03. النسخ الاحتياطي والاستعادة | Backup & Disaster Recovery

## 🎯 **نظرة عامة | Overview**

استراتيجيات النسخ الاحتياطي والاستعادة من الكوارث لضمان استمرارية الأعمال.

**الهدف | Purpose**: حماية البيانات واستمرارية الخدمة  
**الجمهور | Audience**: SRE، DevOps، الإدارة  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [RPO و RTO](#rpo-rto)
2. [استراتيجية النسخ](#استراتيجية-النسخ)
3. [الاستعادة](#الاستعادة)
4. [DR Testing](#dr-testing)
5. [قائمة التحقق](#قائمة-التحقق)

---

## 1️⃣ RPO & RTO {#rpo-rto}

### **التعريفات**

```
RPO (Recovery Point Objective)
= أقصى فقد بيانات مقبول
  
RTO (Recovery Time Objective)  
= أقصى وقت للعودة للخدمة
```

---

### **الأهداف - زهراء**

| المكون | RPO | RTO | الاستراتيجية |
|--------|-----|-----|--------------|
| **Database** | ≤ 1 ساعة | ≤ 4 ساعات | Replicas + Snapshots |
| **Redis** | ≤ 5 دقائق | ≤ 30 دقيقة | RDB + AOF |
| **Files** | ≤ 24 ساعة | ≤ 2 ساعة | S3 Versioning |
| **Logs** | ≤ 5 دقائق | ≤ 1 ساعة | Streaming |
| **Config** | ≤ 0 | ≤ 15 دقيقة | IaC + Git |

---

## 2️⃣ استراتيجية النسخ | Backup Strategy {#استراتيجية-النسخ}

### **Database Backups**

```bash
# نسخ يومية تلقائية
0 2 * * * /usr/local/bin/backup-db.sh

#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="zahraah_db_${DATE}.sql.gz"

# 1. Dump
mysqldump \
  --single-transaction \
  --quick \
  --lock-tables=false \
  zahraah_db | gzip > /tmp/${BACKUP_FILE}

# 2. Encrypt
gpg --encrypt --recipient backup@zahraah.com /tmp/${BACKUP_FILE}

# 3. Upload to S3
aws s3 cp /tmp/${BACKUP_FILE}.gpg \
  s3://zahraah-backups/database/${BACKUP_FILE}.gpg \
  --storage-class GLACIER

# 4. Verify
aws s3 ls s3://zahraah-backups/database/${BACKUP_FILE}.gpg

# 5. Cleanup local
rm /tmp/${BACKUP_FILE}*

# 6. Cleanup old backups (> 90 days)
aws s3 ls s3://zahraah-backups/database/ | \
  awk '{if ($1 < "'$(date -d '90 days ago' +%Y-%m-%d)'") print $4}' | \
  xargs -I {} aws s3 rm s3://zahraah-backups/database/{}
```

---

### **Redis Persistence**

```conf
# redis.conf

# RDB - Snapshots
save 900 1      # بعد 15 دقيقة إذا تغير مفتاح واحد
save 300 10     # بعد 5 دقائق إذا تغير 10 مفاتيح
save 60 10000   # بعد دقيقة إذا تغير 10000 مفتاح

# AOF - Append Only File
appendonly yes
appendfsync everysec  # كل ثانية

# Backup
dir /var/lib/redis
dbfilename dump.rdb
```

---

## 3️⃣ الاستعادة | Recovery {#الاستعادة}

### **Database Restore**

```bash
#!/bin/bash
# restore-db.sh

BACKUP_FILE=$1  # اسم الملف من S3

# 1. Download
aws s3 cp s3://zahraah-backups/database/${BACKUP_FILE} /tmp/

# 2. Decrypt
gpg --decrypt /tmp/${BACKUP_FILE} > /tmp/backup.sql.gz

# 3. Decompress
gunzip /tmp/backup.sql.gz

# 4. Restore
mysql zahraah_db < /tmp/backup.sql

# 5. Verify
mysql -e "SELECT COUNT(*) FROM orders;" zahraah_db

# 6. Cleanup
rm /tmp/backup.sql
```

---

## 4️⃣ DR Testing | اختبار الاستعادة {#dr-testing}

### **جدول الاختبارات**

| الاختبار | التكرار | المدة |
|----------|---------|-------|
| **Restore Test** | شهري | 2 ساعة |
| **Failover Test** | ربع سنوي | 4 ساعات |
| **Full DR Drill** | سنوي | 8 ساعات |

---

### **سيناريو DR Drill**

```markdown
## DR Drill - 2025-Q1

### السيناريو
فقدان كامل لـ Primary Database

### الخطوات
1. إعلان حادث (simulated)
2. تفعيل DR plan
3. Failover إلى Replica
4. التحقق من استعادة الخدمة
5. Restore من آخر Backup
6. مقارنة البيانات
7. Failback إلى Primary
8. Postmortem

### النتائج المتوقعة
- RTO: ≤ 4 ساعات ✅
- RPO: ≤ 1 ساعة ✅
- Data Loss: 0% ✅
```

---

## ✅ **قائمة التحقق | Checklist**

### **النسخ الاحتياطي**
- [ ] نسخ يومية تلقائية
- [ ] تشفير كامل
- [ ] Multi-region storage
- [ ] Verification بعد كل نسخة
- [ ] Retention policy محددة
- [ ] تنظيف تلقائي للقديمة

### **الاستعادة**
- [ ] سكربتات Restore موثقة ومجربة
- [ ] اختبار شهري للاستعادة
- [ ] RPO/RTO محددين
- [ ] Failover إلى Replica جاهز
- [ ] DR plan موثق

---

## 🔗 **التنقل | Navigation**

[← السابق: الخصوصية | Previous: Privacy & Compliance](02_Privacy_Compliance.md)

[التالي: البنية التحتية | Next: Infrastructure as Code →](../10-Infrastructure/01_Infrastructure_as_Code.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
