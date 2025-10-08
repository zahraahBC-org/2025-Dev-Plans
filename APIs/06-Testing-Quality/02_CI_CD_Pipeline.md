# 02. خط CI/CD | CI/CD Pipeline

## 🎯 **نظرة عامة | Overview**

خط أنابيب CI/CD آمن وفعال لبناء واختبار ونشر واجهات الـ API.

**الهدف | Purpose**: أتمتة Build وTest وDeploy  
**الجمهور | Audience**: مهندسو DevOps، Backend  
**المتطلبات | Prerequisites**: فهم [استراتيجية الاختبار](01_Testing_Strategy.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [استراتيجية Branching](#استراتيجية-branching)
2. [مراحل Pipeline](#مراحل-pipeline)
3. [Health Gates](#health-gates)
4. [أمثلة GitHub Actions](#أمثلة-github-actions)
5. [Rollback](#rollback)

---

## 1️⃣ استراتيجية Branching | Branching Strategy {#استراتيجية-branching}

### **Trunk-Based Development**

```
main (protected)
  │
  ├─ feature/add-product-api
  │    └─ merge via PR
  │
  ├─ hotfix/fix-payment-bug
  │    └─ merge via PR
  │
  └─ release/v1.2.0
       └─ tag: v1.2.0
```

### **القواعد**
- ✅ `main` محمي - يتطلب PR + مراجعة
- ✅ branches قصيرة العمر (< 3 أيام)
- ✅ كل PR يمر عبر CI كامل
- ✅ merge فقط إذا CI أخضر

---

## 2️⃣ مراحل Pipeline | Pipeline Stages {#مراحل-pipeline}

### **المراحل التفصيلية**

```
┌───────────────────────────────────────────────────┐
│ Stage 0: Triggers                                 │
│ - Pull Request to main                            │
│ - Push to main                                    │
│ - Tag v*.*.*                                      │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 1: Lint & Static Analysis                   │
│ ✅ PHPStan (level 6)                              │
│ ✅ PHPCS (PSR-12)                                 │
│ ✅ composer validate                              │
│ ✅ secrets scan (gitleaks)                        │
│ 🚫 Any fail → Stop                                │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 2: Tests & Coverage                         │
│ ✅ Unit Tests (Pest/PHPUnit)                      │
│ ✅ Integration Tests                              │
│ ✅ Coverage ≥ 60%                                 │
│ 🚫 Below threshold → Stop                         │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 3: Build (Docker)                           │
│ ✅ Multi-stage Dockerfile                         │
│ ✅ Tag: sha-<GIT_SHA>                             │
│ ✅ Tag: vX.Y.Z (on release)                       │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 4: Security Scans                           │
│ ✅ composer audit                                 │
│ ✅ Trivy/Grype (container scan)                   │
│ 🚫 Critical/High vulnerabilities → Stop           │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 5: Publish Image                            │
│ ✅ Push to Registry (GHCR/ECR)                    │
│ ✅ Sign image (Cosign)                            │
│ ✅ Generate SBOM                                  │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 6: Deploy to Staging                        │
│ ✅ Run migrations                                 │
│ ✅ Deploy new version                             │
│ ✅ Smoke tests                                    │
│ 🚫 Smoke fail → Rollback                          │
└───────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────┐
│ Stage 7: Canary to Production                     │
│ ✅ Deploy to 5% traffic                           │
│ ✅ Health Gate (10 min)                           │
│ ✅ Deploy to 25% traffic                          │
│ ✅ Health Gate (15 min)                           │
│ ✅ Deploy to 100% traffic                         │
│ 🚫 Any gate fail → Rollback                       │
└───────────────────────────────────────────────────┘
```

---

## 3️⃣ Health Gates | بوابات الصحة {#health-gates}

### **معايير النجاح**

```yaml
health_gates:
  latency:
    p95: 300ms       # max allowed
    p99: 500ms
    
  error_rate:
    threshold: 0.3%  # max 5xx rate
    
  availability:
    threshold: 99.9%
    
  duration:
    observation: 10-15 min per canary step
```

### **سكربت Health Gate**
```bash
#!/bin/bash
# health-gate.sh

API_URL="https://api.zahraah.com"
MAX_5XX_RATE=0.3
MAX_P95=300

# استعلام Prometheus
p95=$(curl -s "$PROM_URL/api/v1/query?query=histogram_quantile(0.95,rate(api_request_duration_seconds_bucket[5m]))" | jq '.data.result[0].value[1]')

error_rate=$(curl -s "$PROM_URL/api/v1/query?query=rate(api_errors_total{status=~\"5..\"}[5m])/rate(api_requests_total[5m])*100" | jq '.data.result[0].value[1]')

# التحقق
if (( $(echo "$p95 > $MAX_P95" | bc -l) )); then
  echo "❌ Health Gate Failed: P95 latency $p95 > $MAX_P95"
  exit 1
fi

if (( $(echo "$error_rate > $MAX_5XX_RATE" | bc -l) )); then
  echo "❌ Health Gate Failed: Error rate $error_rate% > $MAX_5XX_RATE%"
  exit 1
fi

echo "✅ Health Gate Passed"
```

---

## 4️⃣ أمثلة GitHub Actions | GitHub Actions Examples {#أمثلة-github-actions}

### **Workflow كامل**

```yaml
name: API CI/CD

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
    tags: ['v*.*.*']

jobs:
  lint-test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8
        env:
          MYSQL_DATABASE: test
          MYSQL_ROOT_PASSWORD: root
        ports: ['3306:3306']
        options: --health-cmd="mysqladmin ping" --health-interval=10s
    steps:
      - uses: actions/checkout@v4
      
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          coverage: xdebug
      
      - name: Install dependencies
        run: composer install --no-interaction
      
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse
      
      - name: Run Tests
        run: php -d xdebug.mode=coverage vendor/bin/pest --coverage-clover=coverage.xml
      
      - name: Check Coverage
        run: |
          coverage=$(php scripts/parse-coverage.php coverage.xml)
          if (( $(echo "$coverage < 60" | bc -l) )); then
            echo "❌ Coverage $coverage% < 60%"
            exit 1
          fi

  build-scan:
    needs: [lint-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker
        run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
      
      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@0.20.0
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      
      - name: Push to Registry
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy-staging:
    needs: [build-scan]
    runs-on: ubuntu-latest
    environment: STAGING
    steps:
      - name: Deploy
        run: ./scripts/deploy.sh staging ${{ github.sha }}
      
      - name: Smoke Tests
        run: ./scripts/smoke.sh https://staging-api.zahraah.com

  canary-prod:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    environment: PROD
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - name: Deploy 5%
        run: ./scripts/canary.sh prod ${{ github.sha }} 5
      
      - name: Health Gate
        run: ./scripts/health-gate.sh --max-p95=300 --max-5xx=0.3
      
      - name: Deploy 100%
        run: ./scripts/canary.sh prod ${{ github.sha }} 100
```

---

## 5️⃣ Rollback | التراجع {#rollback}

### **استراتيجية Rollback**

```bash
# تلقائي - عند فشل Health Gate
./scripts/rollback.sh prod <LAST_GOOD_TAG>

# يدوي - عند اكتشاف مشكلة
kubectl rollout undo deployment/api-service

# أو Docker
docker service update --image api:v1.1.0 api-service
```

### **متى نتراجع؟**
- ❌ Health Gate فشل
- ❌ ارتفاع معدل 5xx
- ❌ ارتفاع p95 latency
- ❌ فشل Smoke Tests

---

## ✅ **قائمة التحقق | Checklist**

### **CI/CD جاهز**
- [ ] Branching strategy محددة
- [ ] جميع المراحل مهيأة
- [ ] Health Gates مفعلة
- [ ] Secrets آمنة
- [ ] Rollback مجرب
- [ ] Monitoring مدمج

---

## 🔗 **التنقل | Navigation**

[← السابق: استراتيجية الاختبار | Previous: Testing Strategy](01_Testing_Strategy.md)

[التالي: أدوات الاختبار | Next: Testing Tools →](03_Testing_Tools.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved