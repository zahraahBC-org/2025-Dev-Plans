# 04. معايير تصميم المخطط | Schema Design Standards
## اصطلاحات التسمية، أنواع البيانات، والقيود | Naming Conventions, Data Types, and Constraints

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد معايير موحدة لتصميم مخطط قاعدة البيانات  
**Purpose**: Define unified standards for database schema design

**الجمهور**: مطورو الواجهة الخلفية، مصممو قواعد البيانات، القادة التقنيون  
**Audience**: Backend developers, database designers, technical leads

**النطاق**: التسمية، أنواع البيانات، القيود، التطبيع  
**Scope**: Naming, data types, constraints, normalization

---

## 🎯 **نظرة عامة | Overview**

توفر هذه الوثيقة معايير شاملة لتصميم مخطط قاعدة البيانات، مما يضمن الاتساق، قابلية الصيانة، والجودة عبر جميع الجداول والأعمدة.

**المبادئ الأساسية**:
- **الوضوح**: أسماء واضحة وصفية
- **الاتساق**: اصطلاحات موحدة عبر المخطط
- **السلامة**: قيود قوية لمنع البيانات غير الصالحة
- **الأداء**: أنواع البيانات المُحسّنة
- **قابلية الصيانة**: سهولة الفهم والتحديث

---

## 📑 **جدول المحتويات | Table of Contents**

1. [اصطلاحات التسمية | Naming Conventions](#naming-conventions)
2. [المفاتيح الأساسية | Primary Keys](#primary-keys)
3. [المفاتيح الخارجية | Foreign Keys](#foreign-keys)
4. [أنواع البيانات القياسية | Standard Data Types](#standard-data-types)
5. [التطبيع | Normalization](#normalization)
6. [إلغاء التطبيع الاستراتيجي | Strategic Denormalization](#strategic-denormalization)
7. [القيود | Constraints](#constraints)
8. [الحذف الناعم | Soft Delete](#soft-delete)
9. [أعمدة التدقيق | Audit Columns](#audit-columns)
10. [مفاتيح عدم التكرار | Idempotency Keys](#idempotency-keys)

---

## 1. اصطلاحات التسمية | Naming Conventions {#naming-conventions}

### **أسماء الجداول | Table Names**

**القواعد**:
- ✅ استخدم **snake_case** (أحرف صغيرة مع شرطة سفلية)
- ✅ استخدم **صيغة المفرد** (customer وليس customers)
- ✅ أسماء **واضحة وصفية** (order_item وليس oi)
- ❌ لا تستخدم **بادئات** عشوائية (tbl_ أو tb_)
- ❌ تجنب **الكلمات المحجوزة** في SQL

**أمثلة جيدة**:
```sql
customer          -- واضح، مفرد
order_item        -- مركب واضح
payment_attempt   -- وصفي
inventory_ledger  -- يصف الغرض
```

**أمثلة سيئة**:
```sql
tbl_customer      -- بادئة غير ضرورية
customers_table   -- لاحقة غير ضرورية
OrderItem         -- CamelCase (غير قياسي)
oi                -- اختصار غامض
order             -- كلمة محجوزة SQL
```

---

### **أسماء الأعمدة | Column Names**

**القواعد**:
- ✅ استخدم **snake_case**
- ✅ أضف **اللاحقة المناسبة** للمعرّفات (_id، _no، _code)
- ✅ استخدم **أسماء واضحة** (created_at وليس cdate)
- ✅ كن **متسقاً** عبر الجداول (نفس الحقل = نفس الاسم)
- ❌ تجنب **الاختصارات** الغامضة

**معايير اللواحق**:

| اللاحقة Suffix | الاستخدام Use | مثال Example |
|---------------|--------------|--------------|
| `_id` | المفاتيح الأساسية والخارجية | customer_id، order_id |
| `_no` | أرقام قابلة للقراءة | order_no، invoice_no |
| `_code` | رموز فريدة قصيرة | coupon_code، sku |
| `_at` | الطوابع الزمنية | created_at، updated_at |
| `_date` | التواريخ فقط | birth_date، due_date |
| `_count` | العدادات | usage_count، view_count |
| `_amount` | القيم النقدية | discount_amount، tax_amount |
| `_rate` | النسب/المعدلات | tax_rate، conversion_rate |
| `_flag` | القيم المنطقية | is_active، has_discount |

**أمثلة**:
```sql
-- جيد
customer_id
order_no
created_at
is_active
base_price

-- سيء
custId          -- CamelCase
ord_num         -- اختصار
creation_date   -- غير متسق مع created_at
active          -- غامض (boolean؟)
```

---

### **أسماء الفهارس | Index Names**

**التنسيق القياسي**:
```
idx_{table}_{column(s)}
uk_{table}_{column(s)}   # للفريد UNIQUE
fk_{table}_{ref_table}   # للمفاتيح الخارجية
```

**أمثلة**:
```sql
-- فهارس عادية
idx_orders_customer_id
idx_orders_status_created
idx_products_category_brand

-- فهارس فريدة
uk_customers_phone
uk_products_sku
uk_orders_order_no

-- فهارس المفاتيح الخارجية
fk_orders_customers
fk_order_items_orders
fk_order_items_variants
```

---

### **أسماء القيود | Constraint Names**

```sql
-- قيود CHECK
chk_{table}_{column}_{condition}

-- أمثلة
chk_orders_total_positive
chk_customers_age_adult
chk_prices_valid_range
```

---

## 2. المفاتيح الأساسية | Primary Keys {#primary-keys}

### **الخيارات | Options**

#### **الخيار 1: AUTO_INCREMENT (بسيط)**

```sql
customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
```

**المزايا**:
- ✅ بسيط وواضح
- ✅ أداء ممتاز للإدراج
- ✅ حجم صغير (8 bytes)
- ✅ ترتيب طبيعي

**العيوب**:
- ❌ قابل للتخمين
- ❌ مشاكل في الأنظمة الموزعة
- ❌ قد يكشف حجم الأعمال

**الاستخدام الموصى به**: للجداول الداخلية وغير الموزعة

---

#### **الخيار 2: UUID (موزع)**

```sql
customer_id CHAR(36) PRIMARY KEY  -- '123e4567-e89b-12d3-a456-426614174000'
-- أو
customer_id BINARY(16) PRIMARY KEY  -- أكثر كفاءة
```

**المزايا**:
- ✅ فريد عالميًا
- ✅ آمن (غير قابل للتخمين)
- ✅ يعمل في الأنظمة الموزعة
- ✅ يمكن توليده في التطبيق

**العيوب**:
- ❌ حجم أكبر (36 bytes نص، 16 bytes ثنائي)
- ❌ أداء إدراج أقل قليلاً
- ❌ فهارس أكبر

**الاستخدام الموصى به**: للجداول الموزعة أو المعرضة للعميل

---

#### **الخيار 3: ULID/UUIDv7 (أفضل ما في العالمين)**

```sql
-- ULID: قابل للفرز زمنياً + فريد عالمياً
customer_id BINARY(16) PRIMARY KEY

-- مثال توليد في التطبيق:
-- ULID: 01ARYZ6S41TSV4RRFFQ69G5FAV
-- يحول إلى BINARY(16) للتخزين
```

**المزايا**:
- ✅ فريد عالميًا
- ✅ قابل للفرز زمنياً (أداء أفضل)
- ✅ أكثر إحكاماً من UUID نص
- ✅ يتجنب تجزئة الفهرس

**الاستخدام الموصى به**: **الخيار المفضل** للمشاريع الجديدة

---

### **التوصية لمنصة زهراء | Recommendation for Zahraah**

```sql
-- للجداول الأساسية: BIGINT AUTO_INCREMENT
customers (
    customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
);

-- للمعاملات المعرضة: UUID/ULID
orders (
    order_id BINARY(16) PRIMARY KEY,
    order_no VARCHAR(20) UNIQUE NOT NULL  -- للعرض البشري
);

payments (
    payment_id BINARY(16) PRIMARY KEY
);
```

---

## 3. المفاتيح الخارجية | Foreign Keys {#foreign-keys}

### **القواعد الإلزامية | Mandatory Rules**

⚠️ **حاسم**: استخدم قيود المفاتيح الخارجية لجميع العلاقات.

```sql
-- بناء الجملة
FOREIGN KEY (column_name) 
    REFERENCES parent_table(parent_column)
    ON DELETE {RESTRICT | CASCADE | SET NULL | NO ACTION}
    ON UPDATE {RESTRICT | CASCADE | SET NULL | NO ACTION}
```

### **سياسات ON DELETE | ON DELETE Policies**

| السياسة Policy | الوصف Description | الاستخدام Use Case |
|---------------|-------------|----------------|
| `RESTRICT` | **منع الحذف** إذا كانت هناك سجلات مرتبطة | **الافتراضي** - معظم الحالات |
| `CASCADE` | **حذف تتالي** للسجلات المرتبطة | جداول الربط، السجلات التابعة |
| `SET NULL` | **تعيين NULL** للمفتاح الخارجي | عند السماح بـ NULL |
| `NO ACTION` | نفس RESTRICT | استخدم RESTRICT بدلاً منه |

**أمثلة**:

```sql
-- RESTRICT: المنتج لا يُحذف إذا كان له طلبات
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    variant_id BIGINT NOT NULL,
    
    FOREIGN KEY (variant_id) 
        REFERENCES product_variants(variant_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- CASCADE: حذف عناصر الطلب عند حذف الطلب
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    
    FOREIGN KEY (order_id) 
        REFERENCES orders(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- SET NULL: إذا حُذف العنوان، اجعل الحقل NULL
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    shipping_address_id BIGINT,
    
    FOREIGN KEY (shipping_address_id) 
        REFERENCES addresses(address_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

### **سياسات ON UPDATE | ON UPDATE Policies**

**التوصية**: استخدم `CASCADE` دائماً تقريباً لـ ON UPDATE.

```sql
-- إذا تغير customer_id، حدّث تلقائياً في جميع الجداول المرتبطة
FOREIGN KEY (customer_id) 
    REFERENCES customers(customer_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
```

---

## 4. أنواع البيانات القياسية | Standard Data Types {#standard-data-types}

### **الأعداد الصحيحة | Integers**

| النوع Type | الحجم Bytes | النطاق Range | الاستخدام Use Case |
|----------|-----------|--------------|-----------------|
| `TINYINT` | 1 | -128 إلى 127 | الحالات، الأعلام، العمر |
| `SMALLINT` | 2 | -32,768 إلى 32,767 | الكميات الصغيرة، السنوات |
| `INT` | 4 | -2B إلى 2B | العدادات، الأرقام العامة |
| `BIGINT` | 8 | -9Q إلى 9Q | المعرّفات الأساسية، الأرقام الكبيرة |

**أمثلة**:
```sql
-- TINYINT
age TINYINT UNSIGNED,          -- 0-255 سنة
status TINYINT,                -- كود الحالة
is_active BOOLEAN,             -- فعلياً TINYINT(1)

-- SMALLINT
birth_year SMALLINT UNSIGNED,  -- 0-65535
quantity SMALLINT UNSIGNED,    -- كميات الطلب

-- INT
view_count INT UNSIGNED DEFAULT 0,
usage_count INT UNSIGNED DEFAULT 0,

-- BIGINT
customer_id BIGINT UNSIGNED,   -- المعرّفات
order_id BIGINT UNSIGNED,
total_views BIGINT UNSIGNED,   -- عدادات كبيرة
```

---

### **الأعداد العشرية | Decimal Numbers**

⚠️ **حاسم**: استخدم `DECIMAL` للأموال، **لا تستخدم FLOAT أبداً**.

```sql
-- للأموال (موصى به)
DECIMAL(10, 2)  -- 8 أرقام قبل الفاصلة، 2 بعد
                -- يدعم حتى 99,999,999.99

-- للمبالغ الكبيرة
DECIMAL(12, 2)  -- 10 أرقام قبل الفاصلة
                -- يدعم حتى 9,999,999,999.99

-- للنسب والمعدلات
DECIMAL(5, 2)   -- يدعم 0.00 إلى 999.99
DECIMAL(3, 2)   -- يدعم 0.00 إلى 9.99 (للنسب المئوية)
```

**أمثلة**:
```sql
CREATE TABLE products (
    -- التسعير
    base_price DECIMAL(10,2) NOT NULL,
    discounted_price DECIMAL(10,2),
    
    -- النسب
    tax_rate DECIMAL(4,2) NOT NULL,    -- 0.00-99.99
    discount_rate DECIMAL(5,2),        -- 0.00-999.99
    
    -- الوزن
    weight_kg DECIMAL(6,3) NOT NULL,   -- 3 منازل عشرية
    
    -- التقييم
    avg_rating DECIMAL(3,2)            -- 0.00-9.99
);
```

**لماذا لا FLOAT**:
```sql
-- مشكلة FLOAT
SELECT 0.1 + 0.2;  -- قد ينتج 0.30000000000000004

-- DECIMAL دقيق
SELECT CAST(0.1 AS DECIMAL(10,2)) + CAST(0.2 AS DECIMAL(10,2));  -- 0.30
```

---

### **النصوص | Text**

| النوع Type | الحد الأقصى Max | الاستخدام Use Case |
|----------|--------------|-----------------|
| `CHAR(n)` | 255 حرف | طول ثابت (رموز ISO، أعلام) |
| `VARCHAR(n)` | 65,535 حرف | طول متغير (أسماء، أوصاف قصيرة) |
| `TEXT` | 65,535 حرف | أوصاف متوسطة |
| `MEDIUMTEXT` | 16 مليون | محتوى كبير |
| `LONGTEXT` | 4 جيجابايت | محتوى ضخم جدًا |

**أمثلة**:
```sql
-- CHAR - طول ثابت
country CHAR(2),              -- ISO 3166-1 (SA، AE)
currency CHAR(3),             -- ISO 4217 (SAR، AED)
language CHAR(2),             -- ISO 639-1 (ar، en)

-- VARCHAR - طول متغير
phone VARCHAR(20),            -- E.164: +966501234567
email VARCHAR(255),
product_name VARCHAR(255),
sku VARCHAR(50),

-- TEXT - محتوى متوسط
description TEXT,
care_instructions TEXT,
terms_conditions TEXT,

-- MEDIUMTEXT/LONGTEXT - نادر الاستخدام
product_content_html MEDIUMTEXT
```

**نصائح الأداء**:
- ✅ استخدم `VARCHAR` مع حد مناسب (لا تبالغ)
- ✅ استخدم `CHAR` للحقول ذات الطول الثابت
- ⚠️ `TEXT` لا يمكن فهرسته بالكامل (فقط prefix)
- ⚠️ تجنب `LONGTEXT` إلا للضرورة القصوى

---

### **التواريخ والأوقات | Dates and Times**

| النوع Type | التنسيق Format | الاستخدام Use Case |
|----------|---------------|-----------------|
| `DATE` | YYYY-MM-DD | التواريخ فقط (بدون وقت) |
| `DATETIME` | YYYY-MM-DD HH:MM:SS | الطوابع الزمنية |
| `DATETIME(3)` | مع مللي ثانية | دقة عالية |
| `TIMESTAMP` | كـ DATETIME | auto-update (أقل استخداماً) |

**التوصية**: استخدم `DATETIME` أو `DATETIME(3)` بدلاً من `TIMESTAMP`.

```sql
-- تواريخ فقط
birth_date DATE,
due_date DATE,
valid_from DATE,

-- طوابع زمنية قياسية
created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

-- دقة عالية (مللي ثانية)
payment_attempted_at DATETIME(3),
event_timestamp DATETIME(3),

-- أمثلة كاملة
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME,
    shipped_at DATETIME,
    delivered_at DATETIME,
    
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**قاعدة ذهبية**: 
- ✅ خزّن دائماً بـ **UTC**
- ✅ احول إلى المنطقة الزمنية المحلية في **التطبيق**

---

### **JSON**

```sql
-- للبيانات الوصفية المرنة
metadata JSON,
utm_params JSON,
attributes JSON
```

**متى تستخدم JSON**:
- ✅ بيانات وصفية مرنة
- ✅ الخصائص الاختيارية
- ✅ البيانات شبه المنظمة

**متى لا تستخدم JSON**:
- ❌ لا تستبدل التصميم العلائقي
- ❌ لا للبيانات التي يتم الاستعلام عنها بكثرة
- ❌ لا للبيانات الحرجة التي تتطلب قيود

**أمثلة**:
```sql
-- جيد
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    badges JSON,  -- ["new", "sale", "trending"]
    seo_keywords JSON
);

-- سيء - استخدم أعمدة عادية
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    profile JSON  -- { "name": "...", "email": "..." }
                  -- يجب أن تكون أعمدة منفصلة!
);
```

---

### **ENUM مقابل جداول البحث | ENUM vs Lookup Tables**

#### **استخدم ENUM للقيم الثابتة جداً**

```sql
-- جيد: قيم ثابتة نادرة التغيير
gender ENUM('male', 'female', 'prefer_not_to_say'),
payment_method ENUM('cod', 'online', 'wallet'),
carrier_service ENUM('standard', 'express', 'same_day')
```

#### **استخدم جداول البحث للقيم الديناميكية**

```sql
-- جيد: قيم قد تتغير أو تتوسع
CREATE TABLE order_statuses (
    status_id TINYINT PRIMARY KEY,
    status_code VARCHAR(50) UNIQUE NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    display_order INT
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    status_id TINYINT NOT NULL,
    FOREIGN KEY (status_id) REFERENCES order_statuses(status_id)
);
```

**متى تستخدم كل منهما**:

| ENUM | جدول البحث |
|------|------------|
| < 10 قيم | > 10 قيم |
| ثابتة | ديناميكية |
| نادرة التغيير | تتغير بشكل متكرر |
| لا تحتاج ترجمات | تحتاج ترجمات |

---

## 5. التطبيع | Normalization {#normalization}

### **الشكل الطبيعي الثالث (3NF) | Third Normal Form (3NF)**

⚠️ **القاعدة الأساسية**: ابدأ دائماً بـ **3NF**، ثم قم بإلغاء التطبيع فقط عند الضرورة مع التوثيق.

### **قواعد التطبيع | Normalization Rules**

#### **الشكل الطبيعي الأول (1NF)**
- ✅ لا قيم متعددة في عمود واحد
- ✅ كل عمود قيمة ذرية واحدة
- ✅ صفوف فريدة

```sql
-- سيء (ليس 1NF)
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    items VARCHAR(500)  -- "item1,item2,item3" ❌
);

-- جيد (1NF)
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY
);

CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    variant_id BIGINT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

---

#### **الشكل الطبيعي الثاني (2NF)**
- ✅ يحقق 1NF
- ✅ لا تبعيات جزئية (كل عمود يعتمد على المفتاح الأساسي بالكامل)

```sql
-- سيء (ليس 2NF) - product_name يعتمد جزئياً
CREATE TABLE order_items (
    order_id BIGINT,
    variant_id BIGINT,
    product_name VARCHAR(255),  -- يعتمد على variant_id فقط ❌
    PRIMARY KEY (order_id, variant_id)
);

-- جيد (2NF)
CREATE TABLE order_items (
    order_id BIGINT,
    variant_id BIGINT,
    -- product_name يُجلب من join مع product_variants
    PRIMARY KEY (order_id, variant_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
);
```

---

#### **الشكل الطبيعي الثالث (3NF)**
- ✅ يحقق 2NF
- ✅ لا تبعيات انتقالية (كل عمود يعتمد فقط على المفتاح الأساسي)

```sql
-- سيء (ليس 3NF) - category_name يعتمد على product_id عبر category_id
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    category_id BIGINT,
    category_name VARCHAR(100)  -- تبعية انتقالية ❌
);

-- جيد (3NF)
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    category_id BIGINT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE categories (
    category_id BIGINT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL
);
```

---

## 6. إلغاء التطبيع الاستراتيجي | Strategic Denormalization {#strategic-denormalization}

### **متى تلغي التطبيع | When to Denormalize**

⚠️ **قاعدة**: لا تلغِ التطبيع إلا بعد قياس الأداء وتوثيق السبب.

**أسباب صحيحة**:
1. ✅ تحسين أداء الاستعلامات الحرجة المثبت
2. ✅ تقليل JOINs المعقدة (5+ جداول)
3. ✅ لقطات تاريخية (نمط Snapshot)

**أسباب سيئة**:
1. ❌ "قد يكون أسرع" بدون قياس
2. ❌ تجنب JOINs بدون سبب
3. ❌ الراحة في البرمجة

---

### **نمط اللقطة | Snapshot Pattern**

⚠️ **مبدأ أساسي**: خزّن لقطة من البيانات وقت الحدث لحماية من التغييرات المستقبلية.

```sql
-- لقطة السعر في الطلب
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    variant_id BIGINT NOT NULL,
    
    -- لقطة وقت الطلب (غير قابل للتغيير)
    unit_price DECIMAL(10,2) NOT NULL,        -- السعر الفعلي المدفوع
    discount_per_unit DECIMAL(10,2) NOT NULL,
    tax_per_unit DECIMAL(10,2) NOT NULL,
    
    -- الأسماء للقراءة السريعة (اختياري)
    product_name_ar VARCHAR(255),
    product_name_en VARCHAR(255),
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
);
```

**الفوائد**:
- ✅ سجل دقيق لما دفعه العميل
- ✅ لا يتأثر بتغييرات الأسعار اللاحقة
- ✅ تقارير مالية صحيحة

---

### **الأعمدة المشتقة | Derived Columns**

```sql
-- أعمدة محسوبة مُخزنة (MySQL 8.0+)
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    
    subtotal DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    shipping_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    
    -- عمود مشتق مُخزن
    total DECIMAL(10,2) AS (
        subtotal - discount_amount + tax_amount + shipping_fee
    ) STORED,
    
    -- أو محسوب ديناميكياً
    total_virtual DECIMAL(10,2) AS (
        subtotal - discount_amount + tax_amount + shipping_fee
    ) VIRTUAL
);
```

**STORED مقابل VIRTUAL**:
- `STORED`: يُحفظ فعلياً، يمكن فهرسته، يستهلك مساحة
- `VIRTUAL`: يُحسب عند القراءة، لا مساحة إضافية، لا يمكن فهرسته

---

## 7. القيود | Constraints {#constraints}

### **NOT NULL**

```sql
-- استخدم NOT NULL للحقول المطلوبة
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,           -- إلزامي
    email VARCHAR(255),                   -- اختياري
    first_name VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL
);
```

---

### **UNIQUE**

```sql
-- قيود UNIQUE لمنع التكرار
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    
    -- أو
    CONSTRAINT uk_customers_phone UNIQUE (phone),
    CONSTRAINT uk_customers_email UNIQUE (email)
);

-- UNIQUE مركب
CREATE TABLE product_variants (
    variant_id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    color_id BIGINT,
    size_id BIGINT,
    
    CONSTRAINT uk_product_color_size 
        UNIQUE (product_id, color_id, size_id)
);
```

---

### **CHECK (MySQL 8.0.16+)**

```sql
-- قيود CHECK للتحقق من القيم
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    
    base_price DECIMAL(10,2) NOT NULL,
    discounted_price DECIMAL(10,2),
    
    -- التحقق من صحة الأسعار
    CONSTRAINT chk_base_price_positive 
        CHECK (base_price > 0),
    
    CONSTRAINT chk_discount_less_than_base 
        CHECK (discounted_price IS NULL OR discounted_price < base_price),
    
    tax_rate DECIMAL(4,2) NOT NULL,
    CONSTRAINT chk_tax_rate_range 
        CHECK (tax_rate >= 0 AND tax_rate <= 1)
);

-- التحقق من الكميات
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    quantity SMALLINT NOT NULL,
    
    CONSTRAINT chk_quantity_positive 
        CHECK (quantity > 0)
);

-- التحقق من التواريخ
CREATE TABLE promotions (
    promotion_id BIGINT PRIMARY KEY,
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    
    CONSTRAINT chk_valid_date_range 
        CHECK (valid_until > valid_from)
);

-- التحقق من العملات المسموحة
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY,
    currency CHAR(3) NOT NULL,
    
    CONSTRAINT chk_currency_allowed 
        CHECK (currency IN ('SAR', 'AED', 'KWD', 'BHD', 'OMR', 'QAR'))
);
```

---

## 8. الحذف الناعم | Soft Delete {#soft-delete}

### **نمط archived_at | archived_at Pattern**

```sql
-- إضافة عمود للحذف الناعم
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    -- ... حقول أخرى
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    archived_at DATETIME,  -- NULL = نشط، NOT NULL = محذوف
    
    INDEX idx_archived (archived_at)
);
```

### **الاستخدام | Usage**

```sql
-- "حذف" سجل (soft delete)
UPDATE customers 
SET archived_at = NOW() 
WHERE customer_id = 123;

-- استعادة سجل
UPDATE customers 
SET archived_at = NULL 
WHERE customer_id = 123;

-- الاستعلام عن السجلات النشطة فقط
SELECT * FROM customers 
WHERE archived_at IS NULL;

-- الاستعلام عن السجلات المحذوفة
SELECT * FROM customers 
WHERE archived_at IS NOT NULL;
```

### **الفهارس مع الحذف الناعم | Indexes with Soft Delete**

```sql
-- تضمين archived_at في الفهارس
CREATE INDEX idx_customers_phone_active 
    ON customers(phone, archived_at);

CREATE INDEX idx_orders_customer_status 
    ON orders(customer_id, status, archived_at);
```

---

## 9. أعمدة التدقيق | Audit Columns {#audit-columns}

### **الأعمدة القياسية | Standard Columns**

```sql
-- أضف لجميع الجداول
CREATE TABLE table_name (
    id BIGINT PRIMARY KEY,
    
    -- ... أعمدة البيانات
    
    -- أعمدة التدقيق
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by BIGINT,  -- FK إلى المستخدمين/الموظفين
    updated_by BIGINT,  -- FK إلى المستخدمين/الموظفين
    archived_at DATETIME,  -- للحذف الناعم
    
    INDEX idx_created (created_at),
    INDEX idx_updated (updated_at),
    INDEX idx_archived (archived_at)
);
```

### **مع FK إلى المستخدمين | With FK to Users**

```sql
CREATE TABLE staff_users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    -- ... أعمدة البيانات
    
    created_by BIGINT NOT NULL,
    updated_by BIGINT NOT NULL,
    
    FOREIGN KEY (created_by) REFERENCES staff_users(user_id),
    FOREIGN KEY (updated_by) REFERENCES staff_users(user_id)
);
```

---

## 10. مفاتيح عدم التكرار | Idempotency Keys {#idempotency-keys}

### **الهدف | Purpose**
منع المعاملات المكررة في العمليات الحرجة (خاصة المدفوعات).

```sql
-- مفتاح عدم التكرار للمدفوعات
CREATE TABLE payments (
    payment_id BINARY(16) PRIMARY KEY,
    order_id BIGINT NOT NULL,
    
    -- مفتاح عدم التكرار
    idempotency_key VARCHAR(100) UNIQUE NOT NULL,
    
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'failed') NOT NULL,
    
    created_at DATETIME NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    
    INDEX idx_idempotency (idempotency_key)
);
```

### **الاستخدام | Usage**

```python
# في التطبيق
import uuid

def process_payment(order_id, amount):
    # توليد مفتاح عدم التكرار
    idempotency_key = f"payment_{order_id}_{uuid.uuid4()}"
    
    # محاولة الإدراج
    try:
        cursor.execute("""
            INSERT INTO payments (payment_id, order_id, idempotency_key, amount, status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (payment_id, order_id, idempotency_key, amount))
        
        # معالجة الدفع...
        
    except IntegrityError:
        # مفتاح موجود - تم معالجة الدفع سابقاً
        print("Payment already processed")
```

---

## 11. Laravel Migrations | هجرات Laravel {#laravel-migrations}

### **نظرة عامة | Overview**

Laravel Migrations توفر طريقة منظمة لإدارة تغييرات قاعدة البيانات باستخدام PHP بدلاً من SQL الخام، مع دعم التحكم في الإصدار (Version Control).

### **11.1 Create Orders Table Migration | هجرة إنشاء جدول الطلبات**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * تشغيل الهجرة
     * Run the migrations
     */
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            // المفتاح الأساسي | Primary Key
            $table->id();
            
            // رقم الطلب | Order Number
            $table->string('order_no', 20)->unique()->comment('رقم الطلب الفريد');
            
            // المفاتيح الخارجية | Foreign Keys
            $table->foreignId('customer_id')
                ->constrained('customers')
                ->onDelete('cascade')
                ->comment('معرف العميل');
            
            $table->foreignId('shipping_address_id')
                ->constrained('addresses')
                ->onDelete('restrict')
                ->comment('عنوان الشحن');
            
            $table->foreignId('warehouse_id')
                ->constrained('warehouses')
                ->onDelete('restrict')
                ->comment('المستودع');
            
            // المبالغ | Amounts
            $table->decimal('subtotal', 10, 2)->comment('المجموع الفرعي');
            $table->decimal('discount_amount', 10, 2)->default(0)->comment('مبلغ الخصم');
            $table->decimal('tax_amount', 10, 2)->default(0)->comment('مبلغ الضريبة');
            $table->decimal('shipping_fee', 10, 2)->default(0)->comment('رسوم الشحن');
            $table->decimal('total', 10, 2)->comment('الإجمالي');
            $table->char('currency', 3)->default('SAR')->comment('العملة');
            
            // الحالة | Status
            $table->enum('status', [
                'created', 'paid', 'confirmed', 'packed', 
                'shipped', 'out_for_delivery', 'delivered',
                'cancelled', 'failed', 'returned'
            ])->default('created')->comment('حالة الطلب');
            
            // الدفع | Payment
            $table->enum('payment_method', ['cod', 'online', 'wallet'])
                ->comment('طريقة الدفع');
            
            $table->enum('payment_status', [
                'pending', 'authorized', 'captured', 'settled', 'refunded', 'failed'
            ])->default('pending')->comment('حالة الدفع');
            
            // إسناد التسويق | Marketing Attribution
            $table->string('utm_source', 50)->nullable()->comment('مصدر UTM');
            $table->string('utm_medium', 50)->nullable()->comment('وسيط UTM');
            $table->string('utm_campaign', 100)->nullable()->comment('حملة UTM');
            $table->string('utm_term', 100)->nullable()->comment('مصطلح UTM');
            $table->string('utm_content', 100)->nullable()->comment('محتوى UTM');
            
            // الطوابع الزمنية | Timestamps
            $table->timestamp('paid_at')->nullable()->comment('وقت الدفع');
            $table->timestamp('confirmed_at')->nullable()->comment('وقت التأكيد');
            $table->timestamp('packed_at')->nullable()->comment('وقت التعبئة');
            $table->timestamp('shipped_at')->nullable()->comment('وقت الشحن');
            $table->timestamp('delivered_at')->nullable()->comment('وقت التوصيل');
            $table->timestamp('cancelled_at')->nullable()->comment('وقت الإلغاء');
            
            // أعمدة التدقيق القياسية | Standard Audit Columns
            $table->timestamps();
            $table->softDeletes();
            
            // الفهارس | Indexes
            $table->index(['customer_id', 'created_at'], 'idx_customer_created');
            $table->index(['status', 'created_at'], 'idx_status_created');
            $table->index('payment_status', 'idx_payment_status');
            $table->index('order_no', 'idx_order_no');
            $table->index('created_at', 'idx_created_at');
            
            // فهرس نصي كامل | Full-text Index
            $table->fullText(['order_no'], 'ft_order_no');
        });
        
        // إضافة تعليق للجدول | Add table comment
        DB::statement("ALTER TABLE orders COMMENT = 'جدول الطلبات - Orders Table'");
    }

    /**
     * عكس الهجرة
     * Reverse the migrations
     */
    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
};
```

### **11.2 Create Inventory Ledger Migration | هجرة دفتر المخزون**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('inventory_ledger', function (Blueprint $table) {
            $table->id('movement_id');
            
            // المفاتيح الخارجية | Foreign Keys
            $table->foreignId('variant_id')
                ->constrained('product_variants')
                ->onDelete('restrict')
                ->comment('معرف النسخة');
            
            $table->foreignId('warehouse_id')
                ->constrained('warehouses')
                ->onDelete('restrict')
                ->comment('المستودع');
            
            // نوع الحركة | Movement Type
            $table->enum('movement_type', [
                'purchase_receipt',    // استلام من المورد
                'adjustment',          // تعديل يدوي
                'reservation',         // حجز لطلب
                'release',             // إلغاء حجز
                'shipment_captured',   // شحن للعميل
                'rto_received',        // استلام إرجاع إلى المنشأ
                'rma_returned',        // استلام مرتجع
                'damage',              // تلف
                'theft',               // سرقة
                'inventory_count'      // جرد فعلي
            ])->comment('نوع حركة المخزون');
            
            // الكمية | Quantity
            $table->integer('quantity')->comment('الكمية (موجب = زيادة، سالب = نقص)');
            
            // المرجع | Reference
            $table->string('reference_type', 50)->nullable()->comment('نوع المرجع');
            $table->unsignedBigInteger('reference_id')->nullable()->comment('معرف المرجع');
            
            // البيانات الوصفية | Metadata
            $table->string('reason', 255)->nullable()->comment('السبب');
            $table->text('notes')->nullable()->comment('ملاحظات');
            $table->unsignedBigInteger('performed_by')->nullable()->comment('المستخدم المنفذ');
            
            // التواريخ | Dates
            $table->timestamp('movement_date')->comment('تاريخ الحركة');
            $table->timestamp('created_at')->comment('تاريخ التسجيل');
            
            // الفهارس | Indexes
            $table->index(['variant_id', 'movement_date'], 'idx_variant_date');
            $table->index(['warehouse_id', 'movement_date'], 'idx_warehouse_date');
            $table->index(['reference_type', 'reference_id'], 'idx_reference');
            $table->index('movement_type', 'idx_movement_type');
            $table->index('movement_date', 'idx_movement_date');
        });
        
        DB::statement("ALTER TABLE inventory_ledger COMMENT = 'دفتر يومية المخزون - Inventory Ledger (Event Sourcing)'");
    }

    public function down(): void
    {
        Schema::dropIfExists('inventory_ledger');
    }
};
```

### **11.3 Create Wallet Transactions Migration | هجرة معاملات المحفظة**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('wallet_transactions', function (Blueprint $table) {
            $table->uuid('transaction_id')->primary();
            
            // المفاتيح الخارجية | Foreign Keys
            $table->foreignId('wallet_id')
                ->constrained('wallets')
                ->onDelete('cascade');
            
            $table->foreignId('customer_id')
                ->constrained('customers')
                ->onDelete('cascade');
            
            // نوع المعاملة | Transaction Type
            $table->enum('type', ['credit', 'debit', 'hold', 'release'])
                ->comment('نوع المعاملة');
            
            // المبلغ | Amount
            $table->decimal('amount', 10, 2)->comment('مبلغ المعاملة');
            $table->char('currency', 3)->default('SAR');
            
            // المصدر | Source
            $table->enum('source', [
                'refund', 'cashback', 'gift', 'topup', 
                'purchase', 'promo', 'loyalty'
            ])->comment('مصدر المعاملة');
            
            // المرجع | Reference
            $table->string('reference_type', 50)->nullable();
            $table->unsignedBigInteger('reference_id')->nullable();
            
            // الحالة | Status
            $table->enum('status', ['pending', 'posted', 'cancelled'])
                ->default('pending')
                ->comment('حالة المعاملة');
            
            // الأرصدة | Balances (للتدقيق)
            $table->decimal('balance_before', 10, 2)->comment('الرصيد قبل المعاملة');
            $table->decimal('balance_after', 10, 2)->comment('الرصيد بعد المعاملة');
            
            // البيانات الوصفية | Metadata
            $table->string('reason_code', 50)->nullable();
            $table->text('notes')->nullable();
            $table->enum('performed_by_type', ['system', 'admin', 'customer'])->default('system');
            $table->unsignedBigInteger('performed_by_id')->nullable();
            
            // التواريخ | Dates
            $table->timestamp('transaction_date')->comment('تاريخ المعاملة');
            $table->timestamp('posted_at')->nullable()->comment('تاريخ الترحيل');
            $table->timestamp('created_at');
            
            // الفهارس | Indexes
            $table->index(['wallet_id', 'transaction_date'], 'idx_wallet_date');
            $table->index(['customer_id', 'transaction_date'], 'idx_customer_date');
            $table->index(['reference_type', 'reference_id'], 'idx_reference');
            $table->index('type', 'idx_type');
            $table->index('status', 'idx_status');
        });
        
        DB::statement("ALTER TABLE wallet_transactions COMMENT = 'معاملات المحفظة - Wallet Transactions (Ledger Pattern)'");
    }

    public function down(): void
    {
        Schema::dropIfExists('wallet_transactions');
    }
};
```

### **11.4 Add Column Migration | هجرة إضافة عمود**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * إضافة عمود discount_percentage إلى جدول orders
     * Add discount_percentage column to orders table
     */
    public function up(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->decimal('discount_percentage', 5, 2)
                ->after('discount_amount')
                ->nullable()
                ->comment('نسبة الخصم المطبقة');
        });
    }

    public function down(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->dropColumn('discount_percentage');
        });
    }
};
```

### **11.5 Modify Column Migration | هجرة تعديل عمود**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * زيادة طول عمود order_no
     * Increase order_no column length
     */
    public function up(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->string('order_no', 30)->change();
        });
    }

    public function down(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->string('order_no', 20)->change();
        });
    }
};
```

### **11.6 Create Index Migration | هجرة إنشاء فهرس**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * إضافة فهرس مركب على orders
     * Add composite index on orders
     */
    public function up(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->index(
                ['customer_id', 'status', 'created_at'],
                'idx_customer_status_created'
            );
        });
    }

    public function down(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->dropIndex('idx_customer_status_created');
        });
    }
};
```

### **11.7 أفضل ممارسات Laravel Migrations | Migration Best Practices**

#### **✅ Do's | افعل**

```php
// 1. استخدم أسماء واضحة للهجرات
// Use descriptive migration names
php artisan make:migration create_orders_table
php artisan make:migration add_discount_to_orders_table
php artisan make:migration create_customer_segments_pivot_table

// 2. أضف تعليقات للأعمدة
$table->string('order_no')->comment('رقم الطلب الفريد');

// 3. حدد القيود بوضوح
$table->foreignId('customer_id')
    ->constrained()
    ->onDelete('cascade')
    ->onUpdate('cascade');

// 4. استخدم الأنواع المناسبة
$table->decimal('total', 10, 2);  // للأموال
$table->enum('status', ['active', 'inactive']);  // للحالات المحدودة
$table->json('metadata');  // للبيانات المنظمة

// 5. أضف الفهارس للأعمدة المستخدمة في WHERE و JOIN
$table->index('email');
$table->index(['customer_id', 'created_at']);

// 6. استخدم softDeletes() للحذف الناعم
$table->softDeletes();

// 7. دائماً قدم down() method
public function down(): void
{
    Schema::dropIfExists('orders');
}
```

#### **❌ Don'ts | لا تفعل**

```php
// 1. لا تعدل هجرات تم تشغيلها في الإنتاج
// DON'T modify migrations already run in production

// 2. لا تستخدم Model في الهجرات
// DON'T use Models in migrations
public function up()
{
    Order::create([...]); // ❌ BAD
    DB::table('orders')->insert([...]); // ✅ GOOD
}

// 3. لا تنسى Foreign Key Constraints
$table->unsignedBigInteger('customer_id'); // ❌ Missing constraint
$table->foreignId('customer_id')->constrained(); // ✅ Good

// 4. لا تستخدم الأنواع الخاطئة
$table->float('price'); // ❌ لا تستخدم float للأموال
$table->decimal('price', 10, 2); // ✅ استخدم decimal

// 5. لا تترك الهجرات بدون rollback
public function down()
{
    // ❌ Empty or missing
}
```

### **11.8 تشغيل الهجرات | Running Migrations**

```bash
# تشغيل جميع الهجرات الجديدة
# Run all pending migrations
php artisan migrate

# التراجع عن آخر دفعة من الهجرات
# Rollback last batch of migrations
php artisan migrate:rollback

# التراجع عن آخر X دفعة
# Rollback last X batches
php artisan migrate:rollback --step=2

# إعادة تشغيل جميع الهجرات (خطير!)
# Refresh all migrations (DANGEROUS!)
php artisan migrate:refresh

# التحقق من حالة الهجرات
# Check migration status
php artisan migrate:status

# تشغيل الهجرات في الإنتاج (يتطلب تأكيد)
# Run migrations in production (requires confirmation)
php artisan migrate --force
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 03. إعدادات MySQL | Previous: MySQL Configuration](03_MySQL_Configuration.md)

[التالي: 05. الفهارس والأداء | Next: Indexes & Performance →](05_Indexes_Performance.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
