# 03. أدوات الاختبار | Testing Tools

## 🎯 **نظرة عامة | Overview**

دليل شامل لأفضل أدوات اختبار واجهات الـ API ومتى وكيف تستخدمها.

**الهدف | Purpose**: اختيار واستخدام أدوات الاختبار المناسبة  
**الجمهور | Audience**: فرق QA، مطورو Backend  
**المتطلبات | Prerequisites**: فهم [استراتيجية الاختبار](01_Testing_Strategy.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [اختبارات وظيفية](#اختبارات-وظيفية)
2. [اختبارات العقد](#اختبارات-العقد)
3. [اختبارات الأمان](#اختبارات-الأمان)
4. [اختبارات الأداء](#اختبارات-الأداء)
5. [التكامل مع CI](#التكامل-مع-ci)

---

## 1️⃣ اختبارات وظيفية | Functional Testing {#اختبارات-وظيفية}

### **Postman + Newman**

#### **تنظيم Collections**
```
Zahraah.postman_collection.json
├── 01. Auth
│   ├── Login with OTP
│   ├── Refresh Token
│   └── Logout
├── 02. Products
│   ├── List Products
│   ├── Get Product Details
│   ├── Create Product (Admin)
│   └── Update Product (Admin)
├── 03. Orders
│   ├── Create Order
│   ├── Get Order Status
│   └── Cancel Order
└── 04. Payments
    ├── Process Payment
    └── Check Payment Status
```

#### **تشغيل عبر Newman (CLI)**
```bash
# تثبيت
npm install -g newman

# تشغيل
newman run Zahraah.postman_collection.json \
  --environment staging.postman_environment.json \
  --reporters cli,html \
  --reporter-html-export reports/postman-results.html \
  --bail  # إيقاف عند أول فشل

# مع متغيرات
newman run collection.json \
  -e staging.env.json \
  --env-var "baseUrl=https://staging-api.zahraah.com" \
  --env-var "token=$JWT_TOKEN"
```

---

### **Insomnia + inso**

#### **تشغيل الاختبارات**
```bash
# تثبيت
npm install -g insomnia-inso

# تشغيل اختبارات
inso run test \
  --env "Staging Environment" \
  --workingDir ./api-tests

# تصدير specs
inso export spec zahraah-api \
  --output openapi.yaml
```

---

## 2️⃣ اختبارات العقد | Contract Testing {#اختبارات-العقد}

### **Dredd - OpenAPI Validator**

#### **التثبيت**
```bash
npm install -g dredd
```

#### **التشغيل**
```bash
# بسيط
dredd openapi.yaml https://api.staging.zahraah.com

# مع headers
dredd openapi.yaml https://api.staging.zahraah.com \
  --header "Authorization: Bearer $TOKEN" \
  --header "Accept-Language: ar"

# مع hooks
dredd openapi.yaml https://api.staging.zahraah.com \
  --hookfiles=./dredd-hooks.js \
  --reporter=html \
  --output=reports/dredd.html
```

#### **Hooks Example**
```javascript
// dredd-hooks.js
const hooks = require('hooks');

// قبل كل الاختبارات
hooks.beforeAll((transactions, done) => {
  // الحصول على Token
  // ...
  done();
});

// قبل اختبار محدد
hooks.before('Products > GET /products', (transaction, done) => {
  // تهيئة بيانات
  done();
});

// بعد اختبار
hooks.after('Orders > POST /orders', (transaction, done) => {
  // تنظيف
  done();
});
```

---

### **Schemathesis - Property-Based Testing**

#### **التثبيت**
```bash
pip install schemathesis
```

#### **التشغيل**
```bash
# اختبار كامل
schemathesis run openapi.yaml \
  --base-url=https://api.staging.zahraah.com \
  --header "Authorization: Bearer $TOKEN" \
  --checks all \
  --workers 4

# مع Hypothesis
schemathesis run openapi.yaml \
  --base-url=$API_URL \
  --hypothesis-max-examples=50 \
  --hypothesis-seed=42

# فقط مسارات محددة
schemathesis run openapi.yaml \
  --base-url=$API_URL \
  --endpoint=/products \
  --endpoint=/orders
```

---

## 3️⃣ اختبارات الأمان | Security Testing {#اختبارات-الأمان}

### **OWASP ZAP - API Scan**

#### **التشغيل**
```bash
# باستخدام Docker
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.staging.zahraah.com/openapi.yaml \
  -f openapi \
  -r zap-report.html \
  -J zap-report.json

# مع authentication
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.staging.zahraah.com/openapi.yaml \
  -f openapi \
  -c zap-config.conf \
  --hook=/zap/auth-hook.py
```

#### **ملف التكوين**
```
# zap-config.conf
rules.cookie.ignorelist=session_id
rules.csrf.ignorelist=/v1/public/*
rules.jwt.verify=true
```

---

### **Burp Suite (يدوي/تفاعلي)**
```
الاستخدام:
1. Import OpenAPI spec
2. فحص يدوي للثغرات
3. Active/Passive scanning
4. توليد تقرير
```

---

## 4️⃣ اختبارات الأداء | Performance Testing {#اختبارات-الأداء}

### **k6 - Load Testing**

#### **سكربت بسيط**
```javascript
// simple-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 50 },   // ramp-up
    { duration: '3m', target: 50 },   // steady
    { duration: '1m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],  // 95% < 300ms
    http_req_failed: ['rate<0.01'],    // < 1% errors
  },
};

export default function () {
  const token = __ENV.TOKEN;
  
  let res = http.get('https://api.staging.zahraah.com/v1/products', {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'latency < 300ms': (r) => r.timings.duration < 300,
  });
  
  sleep(1);
}
```

#### **التشغيل**
```bash
# تثبيت
brew install k6  # macOS
# أو
sudo apt install k6  # Ubuntu

# تشغيل
k6 run -e TOKEN=$JWT_TOKEN simple-load.js

# مع خيارات
k6 run \
  --vus 50 \
  --duration 5m \
  --out json=results.json \
  simple-load.js
```

---

### **Artillery - Quick Load Tests**

#### **ملف التكوين**
```yaml
# artillery-config.yml
config:
  target: 'https://api.staging.zahraah.com'
  phases:
    - duration: 60
      arrivalRate: 10
  defaults:
    headers:
      Authorization: 'Bearer {{token}}'
      
scenarios:
  - name: "Browse and Order"
    flow:
      - get:
          url: "/v1/products"
      - get:
          url: "/v1/products/123"
      - post:
          url: "/v1/orders"
          json:
            items: [{ variant_id: 123, quantity: 1 }]
```

#### **التشغيل**
```bash
# تثبيت
npm install -g artillery

# تشغيل سريع
artillery quick \
  --count 20 \
  --num 10 \
  https://api.staging.zahraah.com/v1/products

# مع ملف تكوين
artillery run artillery-config.yml \
  --output report.json

# توليد تقرير HTML
artillery report report.json
```

---

## 5️⃣ التكامل مع CI | CI Integration {#التكامل-مع-ci}

### **GitHub Actions - مثال كامل**

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  functional-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Newman
        run: npm install -g newman
      
      - name: Run Postman Tests
        run: |
          newman run Zahraah.postman_collection.json \
            -e staging.env.json \
            --env-var "token=${{ secrets.API_TOKEN }}" \
            --reporters cli,json \
            --reporter-json-export results.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: newman-results
          path: results.json

  contract-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Dredd
        run: npm install -g dredd
      
      - name: Run Contract Tests
        run: |
          dredd openapi.yaml ${{ secrets.STAGING_URL }} \
            --header "Authorization: Bearer ${{ secrets.API_TOKEN }}" \
            --reporter html \
            --output dredd-report.html
      
      - name: Check Results
        run: |
          if grep -q "fail:" dredd-report.html; then
            echo "❌ Contract tests failed"
            exit 1
          fi

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: ZAP Baseline Scan
        run: |
          docker run -t owasp/zap2docker-stable zap-api-scan.py \
            -t ${{ secrets.STAGING_URL }}/openapi.yaml \
            -f openapi \
            -r zap-report.html
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: zap-report
          path: zap-report.html

  performance-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install k6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6
      
      - name: Run Load Tests
        run: |
          k6 run \
            -e TOKEN=${{ secrets.API_TOKEN }} \
            --out json=k6-results.json \
            load-test.js
      
      - name: Check Thresholds
        run: |
          p95=$(jq '.metrics.http_req_duration.values["p(95)"]' k6-results.json)
          if (( $(echo "$p95 > 300" | bc -l) )); then
            echo "❌ P95 $p95ms > 300ms"
            exit 1
          fi
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند إعداد أدوات الاختبار**
- [ ] Postman Collections محدثة
- [ ] Newman مدمج في CI
- [ ] Dredd/Schemathesis للعقد
- [ ] ZAP للأمان
- [ ] k6/Artillery للأداء
- [ ] جميع التقارير تُحفظ كـ Artifacts

---

## 🔗 **التنقل | Navigation**

[← السابق: خط CI/CD | Previous: CI/CD Pipeline](02_CI_CD_Pipeline.md)

[التالي: قوالب وأمثلة | Next: Templates & Examples →](../07-Reference/01_Templates_Examples.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved