# 01. البنية التحتية ككود | Infrastructure as Code (IaC)

## 🎯 **نظرة عامة | Overview**

إدارة البنية التحتية بأكواد معلنة قابلة للنسخ والمراجعة والأتمتة.

**الهدف | Purpose**: أتمتة إدارة البنية  
**الجمهور | Audience**: DevOps، SRE، Infrastructure  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [مبادئ IaC](#مبادئ-iac)
2. [Terraform](#terraform)
3. [Docker](#docker)
4. [Kubernetes](#kubernetes)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ مبادئ IaC | IaC Principles {#مبادئ-iac}

### **المبادئ الأساسية**

```
✅ كل شيء في الكود
✅ Declarative (وصف الحالة المطلوبة)
✅ Versioned (في Git)
✅ Reviewable (عبر PRs)
✅ Testable (Dry-run قبل التطبيق)
✅ Repeatable (نفس النتيجة دائمًا)
```

---

## 2️⃣ Terraform | البنية {#terraform}

### **مثال: RDS Database**

```hcl
# modules/database/main.tf

resource "aws_db_instance" "main" {
  identifier = "zahraah-${var.environment}-db"
  
  # المحرك
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = var.instance_class
  
  # التخزين
  allocated_storage     = var.storage_gb
  max_allocated_storage = var.max_storage_gb
  storage_encrypted     = true
  
  # الشبكة
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  
  # النسخ الاحتياطي
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # المراقبة
  enabled_cloudwatch_logs_exports = ["error", "slowquery"]
  performance_insights_enabled    = true
  
  # العلامات
  tags = {
    Environment = var.environment
    Project     = "zahraah"
    ManagedBy   = "terraform"
  }
}

# Read Replica
resource "aws_db_instance" "replica" {
  count = var.enable_replica ? 1 : 0
  
  identifier          = "zahraah-${var.environment}-db-replica"
  replicate_source_db = aws_db_instance.main.identifier
  instance_class      = var.replica_instance_class
  
  tags = {
    Environment = var.environment
    Role        = "replica"
  }
}
```

---

### **Variables**

```hcl
# variables.tf

variable "environment" {
  description = "البيئة (dev/staging/prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "instance_class" {
  description = "نوع Instance"
  type        = string
  default     = "db.t3.medium"
}

variable "storage_gb" {
  description = "حجم التخزين بالـ GB"
  type        = number
  default     = 100
}
```

---

## 3️⃣ Docker | الحاويات {#docker}

### **Dockerfile متعدد المراحل**

```dockerfile
# Dockerfile

# Stage 1: Build
FROM composer:2 AS builder

WORKDIR /app

COPY composer.json composer.lock ./
RUN composer install \
    --no-dev \
    --no-interaction \
    --no-scripts \
    --prefer-dist \
    --optimize-autoloader

COPY . .

# Stage 2: Runtime
FROM php:8.2-fpm-alpine

# Install extensions
RUN apk add --no-cache \
    mysql-client \
    redis \
    && docker-php-ext-install pdo_mysql opcache

# Copy من Builder
COPY --from=builder /app /var/www/html

# User غير root
RUN chown -R www-data:www-data /var/www/html
USER www-data

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD php artisan health:check || exit 1

# Port
EXPOSE 9000

CMD ["php-fpm"]
```

---

## 4️⃣ Kubernetes | التوزيع {#kubernetes}

### **Deployment**

```yaml
# k8s/api-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: zahraah-prod
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: v1.2.0
    spec:
      containers:
      - name: api
        image: ghcr.io/zahraah/api:v1.2.0
        ports:
        - containerPort: 9000
        
        # Resources
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        # Health Probes
        livenessProbe:
          httpGet:
            path: /health
            port: 9000
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /readyz
            port: 9000
          initialDelaySeconds: 5
          periodSeconds: 5
        
        # Environment
        env:
        - name: APP_ENV
          value: "production"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: db-host
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **استخدم Modules**
   ```hcl
   module "database" {
     source = "./modules/database"
     environment = "prod"
   }
   ```

2. **State في Backend آمن**
   ```hcl
   terraform {
     backend "s3" {
       bucket         = "zahraah-terraform-state"
       key            = "prod/terraform.tfstate"
       region         = "us-east-1"
       encrypt        = true
       dynamodb_table = "terraform-locks"
     }
   }
   ```

3. **Tags موحدة**
   ```hcl
   tags = {
     Environment = var.environment
     Project     = "zahraah"
     ManagedBy   = "terraform"
     Owner       = "sre-team"
   }
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **IaC**
- [ ] جميع البنية في الكود
- [ ] State في Backend آمن
- [ ] Modules لإعادة الاستخدام
- [ ] Variables لكل بيئة
- [ ] Tags موحدة
- [ ] Drift detection
- [ ] PR review إلزامي

---

## 🔗 **التنقل | Navigation**

[← السابق: النسخ الاحتياطي | Previous: Backup & Recovery](../09-Governance/03_Backup_Recovery.md)

[التالي: إدارة التكاليف | Next: Cost Management →](02_Cost_Management.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
