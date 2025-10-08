# 03. مواصفة OpenAPI | OpenAPI Specification

## 🎯 **نظرة عامة | Overview**

OpenAPI كمصدر الحقيقة الوحيد لتوثيق وتعريف واجهات الـ API.

**الهدف | Purpose**: استخدام OpenAPI كعقد رسمي  
**الجمهور | Audience**: مطورو Backend، مهندسو API، فرق QA  
**المتطلبات | Prerequisites**: فهم [العمارة](01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [ما هو OpenAPI](#ما-هو-openapi)
2. [البنية الأساسية](#البنية-الأساسية)
3. [Spec-First vs Code-First](#spec-first-vs-code-first)
4. [أدوات التحقق](#أدوات-التحقق)
5. [أفضل الممارسات](#أفضل-الممارسات)

---

## 1️⃣ ما هو OpenAPI | What is OpenAPI {#ما-هو-openapi}

### **التعريف**
مواصفة قياسية لوصف واجهات RESTful API بشكل قابل للقراءة من الآلات والبشر.

### **الفوائد**
- ✅ **توثيق تلقائي**: Swagger UI, Redoc
- ✅ **توليد الأكواد**: SDKs للعملاء
- ✅ **اختبارات العقد**: التحقق التلقائي
- ✅ **Mock Servers**: اختبار بدون Backend
- ✅ **مصدر حقيقة واحد**: لا اختلافات

---

## 2️⃣ البنية الأساسية | Basic Structure {#البنية-الأساسية}

### **ملف OpenAPI كامل**

```yaml
openapi: 3.1.0

# معلومات عامة
info:
  title: Zahraah API
  version: 1.0.0
  description: |
    واجهات RESTful API لمنصة زهراء للتجارة الإلكترونية
  contact:
    name: API Support
    email: api@zahraah.com
    url: https://api.zahraah.com/support
  license:
    name: Proprietary

# الخوادم
servers:
  - url: https://api.zahraah.com/v1
    description: Production
  - url: https://staging-api.zahraah.com/v1
    description: Staging
  - url: http://localhost:8000/v1
    description: Local Development

# الوسوم (للتنظيم)
tags:
  - name: products
    description: إدارة المنتجات
  - name: orders
    description: إدارة الطلبات
  - name: customers
    description: إدارة العملاء
  - name: auth
    description: المصادقة والتخويل

# مخططات الأمان
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT Access Token
    
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API Key للشركاء

# الأمان الافتراضي
security:
  - bearerAuth: []

# المسارات
paths:
  /products:
    get:
      summary: قائمة المنتجات
      tags: [products]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          schema:
            type: string
            enum: [price, -price, created_at, -created_at]
      responses:
        '200':
          description: قائمة المنتجات
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  meta:
                    $ref: '#/components/schemas/PaginationMeta'
        '401':
          $ref: '#/components/responses/Unauthorized'

# المخططات
components:
  schemas:
    Product:
      type: object
      required:
        - id
        - name_ar
        - price
        - currency
      properties:
        id:
          type: integer
          format: int64
          example: 123
        name_ar:
          type: string
          example: "فستان صيفي"
        name_en:
          type: string
          example: "Summer Dress"
        price:
          type: number
          format: decimal
          minimum: 0
          example: 299.00
        currency:
          type: string
          enum: [SAR, AED, USD]
          example: "SAR"
        is_active:
          type: boolean
          default: true
        created_at:
          type: string
          format: date-time
          example: "2025-01-08T12:00:00Z"
    
    Error:
      type: object
      required:
        - code
        - message
        - trace_id
      properties:
        code:
          type: string
          pattern: '^E[0-9]{4}$'
          example: "E3001"
        message:
          type: string
          example: "Resource not found"
        details:
          oneOf:
            - type: string
            - type: array
              items:
                type: object
        trace_id:
          type: string
          format: uuid
          example: "c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m"
  
  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/Error'
```

---

## 3️⃣ Spec-First vs Code-First {#spec-first-vs-code-first}

### **Spec-First (موصى به)**

```
1. كتابة OpenAPI Spec
   ↓
2. مراجعة مع الفريق
   ↓
3. Lint (Spectral)
   ↓
4. توليد Server Stubs
   ↓
5. تنفيذ المنطق
   ↓
6. اختبارات العقد
```

**الفوائد**:
- ✅ توثيق أولاً
- ✅ اتفاق مبكر على العقد
- ✅ العمل المتوازي (Frontend + Backend)

---

### **Code-First (بديل)**

```
1. كتابة الكود مع التعليقات
   ↓
2. توليد OpenAPI من التعليقات
   ↓
3. Lint ومراجعة
   ↓
4. نشر التوثيق
```

**التحذيرات**:
- ⚠️ التوثيق قد يتأخر
- ⚠️ يحتاج انضباط في التعليقات

---

## 4️⃣ أدوات التحقق | Validation Tools {#أدوات-التحقق}

### **1. Spectral - Linting**

```bash
# تثبيت
npm install -g @stoplight/spectral-cli

# تشغيل
spectral lint openapi.yaml

# النتيجة
✅ 0 errors
⚠️ 2 warnings
  - Line 45: Missing example for parameter 'page'
  - Line 120: Missing description for schema 'Order'
```

**قواعد Lint**:
- ✅ جميع paths موثقة
- ✅ جميع schemas لها examples
- ✅ جميع responses موثقة
- ✅ securitySchemes معرفة

---

### **2. oasdiff - فحص التغييرات الكاسرة**

```bash
# تثبيت
go install github.com/tufin/oasdiff@latest

# مقارنة
oasdiff breaking openapi-v1.yaml openapi-v2.yaml

# النتيجة
Breaking Changes:
❌ /products: removed property 'old_field'
❌ /orders: changed property 'status' type from string to enum

Non-Breaking Changes:
✅ /products: added optional property 'new_field'
✅ /reviews: new endpoint added
```

---

### **3. Dredd - اختبارات العقد**

```bash
# تثبيت
npm install -g dredd

# اختبار
dredd openapi.yaml https://api.staging.zahraah.com

# النتيجة
pass: GET /products (200)
pass: GET /products/123 (200)
fail: POST /orders (422) - Response doesn't match schema
```

---

### **4. Prism - Mock Server**

```bash
# تشغيل
npx @stoplight/prism mock openapi.yaml

# استخدام
curl http://localhost:4010/v1/products
⟶ استجابة مُولدة من examples في OpenAPI
```

---

## 5️⃣ أفضل الممارسات | Best Practices {#أفضل-الممارسات}

### ✅ **افعل | Do**

1. **وثّق كل شيء**
   - جميع المسارات
   - جميع المعاملات
   - جميع حالات الاستجابة
   - أمثلة شاملة

2. **استخدم $ref لتجنب التكرار**
   ```yaml
   responses:
     '401':
       $ref: '#/components/responses/Unauthorized'
   ```

3. **أمثلة واقعية**
   ```yaml
   example: "+966501234567"  # وليس "string"
   ```

4. **Lint قبل كل commit**
   ```bash
   spectral lint openapi.yaml
   ```

5. **اختبارات العقد في CI**
   ```yaml
   - name: Contract Tests
     run: dredd openapi.yaml $API_URL
   ```

---

### ❌ **لا تفعل | Don't**

1. **لا تترك OpenAPI قديمًا**
   ```
   الكود يتغير ← OpenAPI يجب أن يتحدث
   ```

2. **لا تنسخ ولصق المخططات**
   ```yaml
   ❌ تكرار schema كامل
   ✅ استخدم $ref
   ```

3. **لا تترك descriptions فارغة**
   ```yaml
   ❌ description: ""
   ✅ description: "معرف المنتج الفريد"
   ```

---

## ✅ **قائمة التحقق | Checklist**

### **OpenAPI جاهز للإنتاج**
- [ ] جميع endpoints موثقة
- [ ] جميع schemas معرفة
- [ ] أمثلة واقعية
- [ ] descriptions واضحة
- [ ] securitySchemes محددة
- [ ] Spectral Lint ينجح
- [ ] لا تغييرات كاسرة غير موثقة
- [ ] Swagger UI يعمل
- [ ] Contract Tests تمر

---

## 🔗 **التنقل | Navigation**

[← السابق: بوابة الـ API | Previous: API Gateway](02_API_Gateway.md)

[التالي: المصادقة | Next: Authentication →](../03-Security/01_Authentication_Authorization.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

## 📚 **المراجع | References**

- [OpenAPI Specification 3.1](https://spec.openapis.org/oas/v3.1.0)
- [Swagger Tools](https://swagger.io/tools/)
- [Stoplight Studio](https://stoplight.io/studio)
- [Spectral Documentation](https://stoplight.io/open-source/spectral)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved