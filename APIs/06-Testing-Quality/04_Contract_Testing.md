# 04. اختبارات العقد | Contract Testing

## 🎯 **نظرة عامة | Overview**

التحقق من مطابقة تنفيذ الـ API لمواصفة OpenAPI بشكل آلي ومستمر.

**الهدف | Purpose**: ضمان التوافق مع OpenAPI  
**الجمهور | Audience**: فرق QA، Backend  
**المتطلبات | Prerequisites**: [OpenAPI](../02-Architecture/03_OpenAPI_Specification.md), [أدوات الاختبار](03_Testing_Tools.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [ما هي اختبارات العقد](#ما-هي-عقد)
2. [Dredd](#dredd)
3. [Schemathesis](#schemathesis)
4. [Prism](#prism)
5. [دمج CI/CD](#ci-cd)

---

## 1️⃣ ما هي اختبارات العقد | What is Contract Testing {#ما-هي-عقد}

### **التعريف**
التحقق من أن التنفيذ الفعلي يطابق المواصفة الموثقة (OpenAPI).

### **الفوائد**
- ✅ كشف الاختلافات تلقائيًا
- ✅ منع Breaking Changes غير مقصودة
- ✅ توثيق يبقى محدثًا
- ✅ ثقة أكبر في الـ API

---

## 2️⃣ Dredd {#dredd}

### **التثبيت والإعداد**

```bash
npm install -g dredd

# ملف dredd.yml
dry-run: false
hookfiles: ./dredd-hooks.js
language: nodejs
reporter: [html, markdown]
output: [./reports/dredd.html, ./reports/dredd.md]
header: [
  "Authorization: Bearer $TOKEN"
]
loglevel: info
```

---

### **Hooks للتهيئة**

```javascript
// dredd-hooks.js
const hooks = require('hooks');
let token;

hooks.beforeAll((transactions, done) => {
  // الحصول على Token
  const axios = require('axios');
  axios.post('https://api.staging.zahraah.com/v1/auth/login', {
    phone: '+966501234567',
    otp: '123456'
  })
  .then(response => {
    token = response.data.access_token;
    done();
  });
});

hooks.beforeEach((transaction, done) => {
  // إضافة Token لكل طلب
  transaction.request.headers['Authorization'] = `Bearer ${token}`;
  done();
});

// تهيئة بيانات لـ endpoint محدد
hooks.before('Products > POST /products', (transaction, done) => {
  transaction.request.body = JSON.stringify({
    name_ar: 'منتج اختبار',
    name_en: 'Test Product',
    price: 99.99,
    currency: 'SAR',
    category_id: 1,
    brand_id: 1
  });
  done();
});

// تنظيف بعد الاختبار
hooks.after('Products > POST /products', (transaction, done) => {
  const productId = JSON.parse(transaction.real.body).id;
  // حذف المنتج المؤقت
  axios.delete(`https://api.staging.zahraah.com/v1/products/${productId}`, {
    headers: { Authorization: `Bearer ${token}` }
  }).finally(done);
});
```

---

## 3️⃣ Schemathesis {#schemathesis}

### **التشغيل المتقدم**

```bash
# تثبيت
pip install schemathesis

# اختبار كامل مع Hypothesis
schemathesis run openapi.yaml \
  --base-url=https://api.staging.zahraah.com \
  --header="Authorization: Bearer $TOKEN" \
  --checks all \
  --hypothesis-max-examples=100 \
  --hypothesis-seed=42 \
  --workers=4 \
  --exitfirst

# فحوص محددة
schemathesis run openapi.yaml \
  --base-url=$API_URL \
  --checks=status_code_conformance \
  --checks=content_type_conformance \
  --checks=response_schema_conformance \
  --checks=response_headers_conformance

# مع Replay للفشل
schemathesis run openapi.yaml \
  --base-url=$API_URL \
  --cassette-path=./cassettes/failures.yaml
```

---

## 4️⃣ Prism | Mock & Validation {#prism}

### **كـ Mock Server**

```bash
# تشغيل Mock Server
npx @stoplight/prism mock openapi.yaml --port 4010

# الاستخدام
curl http://localhost:4010/v1/products
# يُرجع بيانات مُولدة من examples في OpenAPI
```

---

### **كـ Validation Proxy**

```bash
# تشغيل Proxy يتحقق من التطابق
npx @stoplight/prism proxy openapi.yaml \
  https://api.staging.zahraah.com \
  --port 4010

# توجيه العميل عبر Proxy
curl http://localhost:4010/v1/products
# Prism يتحقق من الطلب والاستجابة مقابل OpenAPI
```

---

## 5️⃣ دمج CI/CD | CI/CD Integration {#ci-cd}

### **GitHub Actions Workflow**

```yaml
name: Contract Tests

on:
  pull_request:
    paths:
      - 'openapi.yaml'
      - 'app/**'
  schedule:
    - cron: '0 2 * * *'  # يومي 2 صباحًا

jobs:
  contract-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install Dredd
        run: npm install -g dredd
      
      - name: Get Auth Token
        id: auth
        run: |
          TOKEN=$(curl -s -X POST ${{ secrets.STAGING_URL }}/v1/auth/login \
            -H "Content-Type: application/json" \
            -d '{"phone":"${{ secrets.TEST_PHONE }}","otp":"${{ secrets.TEST_OTP }}"}' \
            | jq -r '.access_token')
          echo "token=$TOKEN" >> $GITHUB_OUTPUT
      
      - name: Run Dredd
        env:
          TOKEN: ${{ steps.auth.outputs.token }}
        run: |
          dredd openapi.yaml ${{ secrets.STAGING_URL }} \
            --header="Authorization: Bearer $TOKEN" \
            --reporter=html \
            --output=dredd-report.html \
            --hookfiles=./tests/dredd-hooks.js
      
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: dredd-report
          path: dredd-report.html
      
      - name: Check Results
        run: |
          if grep -q "fail:" dredd-report.html; then
            echo "❌ Contract tests failed"
            exit 1
          fi
          echo "✅ All contract tests passed"
```

---

## ✅ **قائمة التحقق | Checklist**

### **Contract Testing Setup**
- [ ] OpenAPI spec كامل ومحدث
- [ ] Dredd أو Schemathesis مثبت
- [ ] Hooks للتهيئة والتنظيف
- [ ] بيئة Staging جاهزة
- [ ] دمج في CI/CD
- [ ] تقارير تُحفظ كـ Artifacts
- [ ] فشل يوقف Pipeline

---

## 🔗 **التنقل | Navigation**

[← السابق: أدوات الاختبار | Previous: Testing Tools](03_Testing_Tools.md)

[التالي: القوالب | Next: Templates & Examples →](../07-Reference/01_Templates_Examples.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
