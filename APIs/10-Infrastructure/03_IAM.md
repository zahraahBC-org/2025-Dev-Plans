# 03. إدارة الهوية والوصول | Identity & Access Management (IAM)

## 🎯 **نظرة عامة | Overview**

إدارة شاملة للهويات والصلاحيات على مستوى البنية التحتية والتطبيق.

**الهدف | Purpose**: التحكم الدقيق بالوصول  
**الجمهور | Audience**: Security، SRE، Compliance  
**المتطلبات | Prerequisites**: فهم [المصادقة](../03-Security/01_Authentication_Authorization.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [مبادئ IAM](#مبادئ-iam)
2. [الأدوار](#الأدوار)
3. [الصلاحيات](#الصلاحيات)
4. [Service Accounts](#service-accounts)
5. [Audit](#audit)

---

## 1️⃣ مبادئ IAM | IAM Principles {#مبادئ-iam}

### **المبادئ الأساسية**

```
✅ Least Privilege - أقل صلاحيات ممكنة
✅ Separation of Duties - فصل المسؤوليات
✅ Regular Review - مراجعة ربع سنوية
✅ Time-bound Access - صلاحيات مؤقتة
✅ Audit Everything - تسجيل كل الوصول
```

---

## 2️⃣ الأدوار | Roles {#الأدوار}

### **أدوار التطبيق**

```yaml
roles:
  customer:
    description: "العميل العادي"
    permissions:
      - orders:read:own
      - profile:read:own
      - profile:write:own
  
  support:
    description: "الدعم الفني"
    permissions:
      - customers:read
      - orders:read
      - returns:write
  
  admin:
    description: "المسؤول"
    permissions:
      - "*:*:*"  # كل الصلاحيات
```

---

### **أدوار البنية التحتية (AWS)**

```hcl
# IAM Role للـ API Service
resource "aws_iam_role" "api_service" {
  name = "zahraah-api-service-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

# Policy - الصلاحيات
resource "aws_iam_role_policy" "api_service" {
  name = "api-service-policy"
  role = aws_iam_role.api_service.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::zahraah-uploads/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:*:*:secret:zahraah/*"
      }
    ]
  })
}
```

---

## 3️⃣ الصلاحيات | Permissions {#الصلاحيات}

### **صيغة الصلاحيات**

```
resource:action:scope

أمثلة:
orders:read:own       - قراءة طلباته فقط
orders:read:all       - قراءة كل الطلبات
orders:write:own      - تعديل طلباته
products:write:all    - تعديل كل المنتجات
users:delete:all      - حذف أي مستخدم
```

---

## 4️⃣ Service Accounts | حسابات الخدمة {#service-accounts}

### **أفضل الممارسات**

```yaml
service_accounts:
  api-worker:
    description: "Background jobs processor"
    permissions:
      - orders:read
      - orders:write
      - notifications:send
    rotation: 90d
    
  monitoring:
    description: "Monitoring system"
    permissions:
      - metrics:read
      - logs:read
    rotation: never  # API Key ثابت
```

---

## 5️⃣ Audit | التدقيق {#audit}

### **Audit Logs**

```sql
CREATE TABLE audit_logs (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    
    -- الفاعل
    actor_id BIGINT UNSIGNED,
    actor_type ENUM('user', 'service', 'system'),
    actor_ip VARCHAR(45),
    
    -- الإجراء
    action VARCHAR(50) NOT NULL,  # created, updated, deleted, accessed
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(100),
    
    -- التفاصيل
    changes JSON,  # before/after
    metadata JSON,
    
    -- الوقت
    performed_at DATETIME NOT NULL,
    
    INDEX idx_actor (actor_id, actor_type),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_performed (performed_at)
);
```

---

## ✅ **قائمة التحقق | Checklist**

### **IAM**
- [ ] Least Privilege مطبق
- [ ] RBAC محدد بوضوح
- [ ] Service Accounts لكل خدمة
- [ ] مراجعة ربع سنوية للصلاحيات
- [ ] Audit logs مفعلة
- [ ] 2FA للمسؤولين
- [ ] Key rotation دوري

---

## 🔗 **التنقل | Navigation**

[← السابق: إدارة التكاليف | Previous: Cost Management](02_Cost_Management.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
