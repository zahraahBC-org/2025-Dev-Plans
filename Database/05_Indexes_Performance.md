# 05. الفهارس والأداء | Indexes & Performance
## تحسين الاستعلامات واستراتيجيات الفهرسة | Query Optimization and Indexing Strategies

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد استراتيجيات الفهرسة وأهداف الأداء  
**Purpose**: Define indexing strategies and performance targets

**الجمهور**: مهندسو الأداء، مطورو الواجهة الخلفية، مديرو قواعد البيانات  
**Audience**: Performance engineers, backend developers, DBAs

**النطاق**: الفهارس، تحسين الاستعلامات، أهداف SLO  
**Scope**: Indexes, query optimization, SLO targets

---

## 🎯 **أهداف الأداء | Performance Targets (SLOs)**

### **أهداف زمن الاستجابة | Response Time Targets**

| السيناريو Scenario | الهدف Target | الأهمية Criticality |
|-------------------|-------------|-------------------|
| **قائمة المنتجات** (50K نسخة مع فلاتر) | ≤ 300ms | حرج - تجربة المستخدم |
| **تأكيد طلب** (إنشاء السجلات الأساسية) | ≤ 2s | حرج - معاملة مالية |
| **فحص المخزون** (لنسخة واحدة) | ≤ 100ms | حرج - منع البيع الزائد |
| **معالجة الدفع** (تفويض + التقاط) | ≤ 1s | حرج - تجربة الدفع |
| **تحديث تتبع الشحنة** (webhook → UI) | ≤ 1 دقيقة | مهم - توقعات العميل |
| **بحث المنتجات** (نص كامل) | ≤ 500ms | مهم - قابلية الاكتشاف |
| **تحميل صفحة الملف الشخصي** | ≤ 200ms | مهم - تجربة المستخدم |
| **السلة → الدفع** (تحويل) | ≤ 1s | حرج - معدل التحويل |

**المنهجية**:
- 🔍 قياس الأداء الفعلي بانتظام
- 📊 مراقبة المئينات (P50، P95، P99)
- ⚠️ تنبيهات عند تجاوز الأهداف
- 🔧 تحسين فوري للاستعلامات البطيئة

---

## 📑 **جدول المحتويات | Table of Contents**

1. [استراتيجية الفهرسة | Indexing Strategy](#indexing-strategy)
2. [فهارس قوائم المنتجات | Product Listing Indexes](#product-listing-indexes)
3. [فهارس السلة والطلبات | Cart & Order Indexes](#cart-order-indexes)
4. [فهارس المخزون | Inventory Indexes](#inventory-indexes)
5. [فهارس الدفع والشحن | Payment & Shipment Indexes](#payment-shipment-indexes)
6. [تحسين الاستعلامات | Query Optimization](#query-optimization)
7. [استراتيجيات الترقيم | Pagination Strategies](#pagination-strategies)
8. [التقسيم | Partitioning](#partitioning)
9. [المراقبة والتنبيهات | Monitoring & Alerts](#monitoring-alerts)

---

## 1. استراتيجية الفهرسة | Indexing Strategy {#indexing-strategy}

### **أنواع الفهارس | Index Types**

#### **فهرس بسيط | Single Column Index**

```sql
-- فهرس على عمود واحد
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_orders_created ON orders(created_at);
```

**الاستخدام**: عندما يتم الاستعلام عن عمود واحد بشكل متكرر.

---

#### **فهرس مركب | Composite Index**

```sql
-- فهرس على عدة أعمدة (الترتيب مهم!)
CREATE INDEX idx_orders_customer_status_date 
    ON orders(customer_id, status, created_at);
```

**قواعد الترتيب**:
1. ✅ **المساواة أولاً** (WHERE col = value)
2. ✅ **النطاق ثانياً** (WHERE col > value)
3. ✅ **الفرز أخيراً** (ORDER BY col)

**مثال**:
```sql
-- الاستعلام
SELECT * FROM orders
WHERE customer_id = 123      -- مساواة
  AND status = 'delivered'   -- مساواة
  AND created_at > '2025-01-01'  -- نطاق
ORDER BY created_at DESC;

-- الفهرس المثالي
CREATE INDEX idx_orders_customer_status_date 
    ON orders(customer_id, status, created_at);
```

---

#### **فهرس تغطية | Covering Index**

```sql
-- فهرس يتضمن جميع الأعمدة المطلوبة
CREATE INDEX idx_orders_covering 
    ON orders(customer_id, status, created_at, total, currency);
```

**الفائدة**: MySQL لا يحتاج للرجوع للجدول (index-only scan).

```sql
-- هذا الاستعلام يُنفذ من الفهرس فقط
SELECT customer_id, status, created_at, total, currency
FROM orders
WHERE customer_id = 123
  AND status = 'delivered';
```

⚠️ **انتباه**: الفهارس التغطية أكبر حجماً، استخدمها للاستعلامات الحرجة فقط.

---

#### **فهرس جزئي | Partial Index**

```sql
-- فهرس على السجلات غير المؤرشفة فقط
CREATE INDEX idx_customers_active 
    ON customers(phone) 
    WHERE archived_at IS NULL;

-- فهرس على الطلبات النشطة فقط
CREATE INDEX idx_orders_active 
    ON orders(status, created_at) 
    WHERE status NOT IN ('delivered', 'cancelled');
```

**الفائدة**: فهرس أصغر، أداء أفضل للاستعلامات المتكررة.

---

#### **فهرس نص كامل | Full-Text Index**

```sql
-- للبحث النصي
CREATE FULLTEXT INDEX idx_products_search 
    ON products(name_ar, name_en, description_ar, description_en);

-- الاستخدام
SELECT * FROM products
WHERE MATCH(name_ar, name_en, description_ar, description_en) 
      AGAINST ('فستان صيفي' IN NATURAL LANGUAGE MODE);
```

---

## 2. فهارس قوائم المنتجات | Product Listing Indexes {#product-listing-indexes}

### **السيناريو الأساسي | Primary Scenario**

**الاستعلام**:
```sql
-- قائمة منتجات حسب الفئة مع فلاتر وترتيب
SELECT 
    p.product_id,
    p.name_ar,
    pv.variant_id,
    pv.sku,
    pv.base_price,
    pv.discounted_price,
    b.name_ar as brand_name
FROM products p
JOIN product_variants pv ON p.product_id = pv.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE p.category_id = 5
  AND p.publish_status = 'published'
  AND p.is_visible = TRUE
  AND pv.is_available = TRUE
  AND p.archived_at IS NULL
ORDER BY p.created_at DESC
LIMIT 20 OFFSET 0;
```

**الفهارس المطلوبة**:

```sql
-- فهرس رئيسي على جدول products
CREATE INDEX idx_products_category_status 
    ON products(category_id, publish_status, is_visible, created_at, archived_at);

-- فهرس على product_variants
CREATE INDEX idx_variants_product_available 
    ON product_variants(product_id, is_available);

-- فهرس على brands
CREATE INDEX idx_brands_id 
    ON brands(brand_id);  -- عادة موجود كـ PK
```

---

### **فلاتر البحث | Search Filters**

```sql
-- فلتر حسب العلامة التجارية
CREATE INDEX idx_products_brand_category 
    ON products(brand_id, category_id, publish_status, is_visible);

-- فلتر حسب السعر
CREATE INDEX idx_variants_price_range 
    ON product_variants(base_price, discounted_price, is_available);

-- فلتر حسب اللون والمقاس
CREATE INDEX idx_variants_attributes 
    ON product_variants(color_id, size_id, is_available);

-- فلتر حسب الشارات
CREATE INDEX idx_products_badges 
    ON products((CAST(badges AS CHAR(100))), publish_status);
```

---

### **الفرز والترتيب | Sorting & Ordering**

```sql
-- الفرز حسب الأحدث
-- الفهرس: idx_products_category_status (من أعلاه)

-- الفرز حسب السعر (من الأقل إلى الأعلى)
SELECT * FROM product_variants
WHERE category_id = 5
  AND is_available = TRUE
ORDER BY base_price ASC;

-- الفهرس المطلوب
CREATE INDEX idx_variants_category_price 
    ON product_variants(category_id, is_available, base_price);

-- الفرز حسب الشعبية
SELECT * FROM product_variants
WHERE category_id = 5
  AND is_available = TRUE
ORDER BY purchase_count DESC;

-- الفهرس المطلوب
CREATE INDEX idx_variants_category_popularity 
    ON product_variants(category_id, is_available, purchase_count DESC);
```

---

## 3. فهارس السلة والطلبات | Cart & Order Indexes {#cart-order-indexes}

### **فهارس السلال | Cart Indexes**

```sql
-- البحث عن سلة العميل النشطة
CREATE INDEX idx_carts_customer_status 
    ON carts(customer_id, status, last_activity_at);

-- السلال المهجورة (للتسويق)
CREATE INDEX idx_carts_abandoned 
    ON carts(status, last_activity_at)
    WHERE status = 'active' 
      AND last_activity_at < DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- عناصر السلة
CREATE INDEX idx_cart_items_cart 
    ON cart_items(cart_id);

CREATE INDEX idx_cart_items_variant 
    ON cart_items(variant_id);
```

---

### **فهارس الطلبات | Order Indexes**

```sql
-- طلبات العميل (الأكثر استخداماً)
CREATE INDEX idx_orders_customer_created 
    ON orders(customer_id, created_at DESC);

-- فلتر حسب الحالة
CREATE INDEX idx_orders_status_created 
    ON orders(status, created_at DESC);

-- البحث بـ order_no
CREATE UNIQUE INDEX uk_orders_order_no 
    ON orders(order_no);

-- الطلبات المعلقة (للعمليات)
CREATE INDEX idx_orders_pending 
    ON orders(status, created_at)
    WHERE status IN ('created', 'paid', 'confirmed');

-- الطلبات الجاهزة للشحن
CREATE INDEX idx_orders_ready_to_ship 
    ON orders(status, warehouse_id, packed_at)
    WHERE status = 'packed';
```

---

### **فهارس عناصر الطلب | Order Items Indexes**

```sql
-- عناصر الطلب
CREATE INDEX idx_order_items_order 
    ON order_items(order_id);

-- تحليلات المنتج
CREATE INDEX idx_order_items_variant_date 
    ON order_items(variant_id, created_at);

-- فهرس تغطية لتقارير المبيعات
CREATE INDEX idx_order_items_sales_report 
    ON order_items(variant_id, created_at, quantity, line_total);
```

---

## 4. فهارس المخزون | Inventory Indexes {#inventory-indexes}

### **فهارس دفتر يومية المخزون | Inventory Ledger Indexes**

```sql
-- حساب المخزون لنسخة
CREATE INDEX idx_ledger_variant_date 
    ON inventory_ledger(variant_id, movement_date DESC);

-- حساب المخزون لمستودع
CREATE INDEX idx_ledger_warehouse_date 
    ON inventory_ledger(warehouse_id, movement_date DESC);

-- البحث حسب المرجع
CREATE INDEX idx_ledger_reference 
    ON inventory_ledger(reference_type, reference_id);

-- تحليلات الحركات
CREATE INDEX idx_ledger_type_date 
    ON inventory_ledger(movement_type, movement_date);

-- فهرس تغطية لحساب المخزون
CREATE INDEX idx_ledger_variant_warehouse_qty 
    ON inventory_ledger(variant_id, warehouse_id, quantity, movement_date);
```

---

### **استعلام حساب المخزون | Stock Calculation Query**

```sql
-- حساب stock_on_hand
SELECT 
    variant_id,
    warehouse_id,
    SUM(quantity) as stock_on_hand
FROM inventory_ledger
WHERE variant_id = 123
  AND warehouse_id = 1
GROUP BY variant_id, warehouse_id;

-- مع الفهرس: idx_ledger_variant_warehouse_qty
-- الأداء المتوقع: < 50ms لـ 10K حركة
```

---

## 5. فهارس الدفع والشحن | Payment & Shipment Indexes {#payment-shipment-indexes}

### **فهارس المدفوعات | Payment Indexes**

```sql
-- البحث حسب الطلب
CREATE INDEX idx_payments_order 
    ON payments(order_id);

-- البحث حسب مفتاح عدم التكرار
CREATE UNIQUE INDEX uk_payments_idempotency 
    ON payments(idempotency_key);

-- المدفوعات المعلقة
CREATE INDEX idx_payments_pending 
    ON payments(status, created_at)
    WHERE status IN ('pending', 'authorized');

-- محاولات الدفع
CREATE INDEX idx_payment_attempts_payment 
    ON payment_attempts(payment_id, attempted_at);
```

---

### **فهارس الشحنات | Shipment Indexes**

```sql
-- البحث حسب رقم التتبع (الأكثر شيوعاً)
CREATE UNIQUE INDEX uk_shipments_tracking 
    ON shipments(tracking_number);

-- البحث حسب الطلب
CREATE INDEX idx_shipments_order 
    ON shipments(order_id);

-- الشحنات النشطة
CREATE INDEX idx_shipments_active 
    ON shipments(status, created_at)
    WHERE status IN ('created', 'picked_up', 'in_transit', 'out_for_delivery');

-- أداء الناقل
CREATE INDEX idx_shipments_carrier_date 
    ON shipments(carrier, shipped_at, delivered_at);

-- أحداث الشحنة
CREATE INDEX idx_shipment_events_shipment_time 
    ON shipment_events(shipment_id, event_time);
```

---

## 6. تحسين الاستعلامات | Query Optimization {#query-optimization}

### **استخدام EXPLAIN | Using EXPLAIN**

```sql
-- تحليل خطة الاستعلام
EXPLAIN SELECT * FROM orders 
WHERE customer_id = 123 
  AND status = 'delivered'
ORDER BY created_at DESC;

-- نسخة مفصلة
EXPLAIN FORMAT=JSON SELECT ...;

-- مع التكاليف الفعلية
EXPLAIN ANALYZE SELECT ...;
```

**ما تبحث عنه في EXPLAIN**:

| المؤشر Indicator | جيد Good | سيء Bad |
|-----------------|---------|---------|
| **type** | const، eq_ref، ref، range | ALL، index |
| **key** | اسم الفهرس | NULL |
| **rows** | قليل (< 1000) | كثير (> 10000) |
| **Extra** | Using index | Using filesort، Using temporary |

---

### **تحسين JOINs | Optimizing JOINs**

```sql
-- سيء: JOIN بدون فهارس
SELECT * 
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.customer_id = 123;

-- جيد: فهارس على أعمدة JOIN
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**نصائح**:
- ✅ تأكد من فهرسة أعمدة JOIN
- ✅ JOIN على أعمدة من نفس النوع والحجم
- ✅ استخدم INNER JOIN بدلاً من WHERE للوضوح
- ⚠️ تجنب JOIN على أكثر من 5-7 جداول

---

### **تحسين WHERE | Optimizing WHERE**

```sql
-- سيء: دالة على العمود (لا يستخدم الفهرس)
SELECT * FROM orders 
WHERE DATE(created_at) = '2025-01-08';

-- جيد: نطاق على العمود
SELECT * FROM orders 
WHERE created_at >= '2025-01-08 00:00:00'
  AND created_at < '2025-01-09 00:00:00';

-- سيء: OR على أعمدة مختلفة
SELECT * FROM customers 
WHERE email = 'test@example.com' 
   OR phone = '+966501234567';

-- جيد: استعلامان منفصلان مع UNION
SELECT * FROM customers WHERE email = 'test@example.com'
UNION
SELECT * FROM customers WHERE phone = '+966501234567';
```

---

### **تحسين ORDER BY | Optimizing ORDER BY**

```sql
-- سيء: الفرز بدون فهرس
SELECT * FROM products
WHERE category_id = 5
ORDER BY created_at DESC;  -- Using filesort

-- جيد: الفهرس يتضمن عمود الفرز
CREATE INDEX idx_products_category_created 
    ON products(category_id, created_at DESC);
```

---

## 7. استراتيجيات الترقيم | Pagination Strategies {#pagination-strategies}

### **OFFSET (بسيط لكن بطيء) | OFFSET (Simple but Slow)**

```sql
-- الصفحة 1
SELECT * FROM products
WHERE category_id = 5
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;

-- الصفحة 2
LIMIT 20 OFFSET 20;

-- الصفحة 100 (بطيء جداً!)
LIMIT 20 OFFSET 2000;
```

⚠️ **المشكلة**: MySQL يجب أن يقرأ ويتخطى جميع الصفوف السابقة.

**الأداء**:
- الصفحة 1: سريع
- الصفحة 10: متوسط
- الصفحة 100+: **بطيء جداً**

---

### **Keyset/Seek (سريع دائماً) | Keyset/Seek (Always Fast)**

```sql
-- الصفحة الأولى
SELECT * FROM products
WHERE category_id = 5
  AND archived_at IS NULL
ORDER BY created_at DESC, product_id DESC
LIMIT 20;

-- الصفحة التالية (استخدم آخر قيم من الصفحة السابقة)
SELECT * FROM products
WHERE category_id = 5
  AND archived_at IS NULL
  AND (created_at, product_id) < ('2025-01-08 12:00:00', 12345)
ORDER BY created_at DESC, product_id DESC
LIMIT 20;
```

**المزايا**:
- ✅ أداء ثابت في جميع الصفحات
- ✅ لا قراءة غير ضرورية
- ✅ مناسب للمجموعات الكبيرة

**العيوب**:
- ❌ لا يمكن القفز للصفحة رقم X مباشرة
- ❌ يتطلب ترتيب ثابت
- ❌ أكثر تعقيداً في التنفيذ

**التوصية**: استخدم Keyset للتطبيقات المحمولة (التمرير اللانهائي).

---

## 8. التقسيم | Partitioning {#partitioning}

### **متى تستخدم التقسيم | When to Use Partitioning**

استخدم التقسيم للجداول:
- ✅ حجمها > 100 مليون صف
- ✅ الاستعلامات تستهدف نطاق زمني محدد
- ✅ الأرشفة الدورية مطلوبة
- ✅ الأداء يتدهور بشكل ملحوظ

### **التقسيم حسب النطاق | Range Partitioning**

```sql
-- تقسيم جدول الأحداث حسب الشهر
CREATE TABLE events_raw (
    event_id BINARY(16) NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    user_id BIGINT,
    params JSON,
    
    created_at DATETIME NOT NULL,
    
    PRIMARY KEY (event_id, event_date)
)
PARTITION BY RANGE (YEAR(event_date) * 100 + MONTH(event_date)) (
    PARTITION p202501 VALUES LESS THAN (202502),
    PARTITION p202502 VALUES LESS THAN (202503),
    PARTITION p202503 VALUES LESS THAN (202504),
    PARTITION p202504 VALUES LESS THAN (202505),
    PARTITION p202505 VALUES LESS THAN (202506),
    PARTITION p202506 VALUES LESS THAN (202507),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

**إدارة الأقسام**:
```sql
-- إضافة قسم جديد
ALTER TABLE events_raw 
    REORGANIZE PARTITION p_future INTO (
        PARTITION p202507 VALUES LESS THAN (202508),
        PARTITION p_future VALUES LESS THAN MAXVALUE
    );

-- حذف قسم قديم (أرشفة)
ALTER TABLE events_raw DROP PARTITION p202401;

-- عرض معلومات الأقسام
SELECT 
    PARTITION_NAME,
    TABLE_ROWS,
    DATA_LENGTH / 1024 / 1024 AS size_mb
FROM information_schema.PARTITIONS
WHERE TABLE_NAME = 'events_raw';
```

---

## 9. المراقبة والتنبيهات | Monitoring & Alerts {#monitoring-alerts}

### **استعلامات المراقبة | Monitoring Queries**

```sql
-- أحجام الجداول
SELECT 
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS size_mb,
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'zahraah_db'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- الفهارس غير المستخدمة
SELECT 
    s.TABLE_NAME,
    s.INDEX_NAME
FROM information_schema.STATISTICS s
LEFT JOIN information_schema.INDEX_STATISTICS i 
    ON s.TABLE_SCHEMA = i.TABLE_SCHEMA
    AND s.TABLE_NAME = i.TABLE_NAME
    AND s.INDEX_NAME = i.INDEX_NAME
WHERE s.TABLE_SCHEMA = 'zahraah_db'
  AND i.INDEX_NAME IS NULL
  AND s.INDEX_NAME != 'PRIMARY';

-- الاستعلامات البطيئة (من slow query log)
-- راجع pt-query-digest أو mysqldumpslow
```

---

### **التنبيهات | Alerts**

إعداد تنبيهات لـ:

| التنبيه Alert | العتبة Threshold | الإجراء Action |
|-------------|-----------------|---------------|
| زمن استعلام P95 | > 500ms | فحص EXPLAIN |
| استعلامات بدون فهارس | > 10/ساعة | إضافة فهارس |
| حجم الجدول | > 80% من Buffer Pool | تقسيم أو أرشفة |
| معدل الأخطاء | > 1% | فحص القيود |
| buffer pool hit rate | < 95% | زيادة buffer_pool_size |

---

## 🔗 **التنقل | Navigation**

[← السابق: 04. معايير تصميم المخطط | Previous: Schema Design Standards](04_Schema_Design.md)

[التالي: 06. الأمان والخصوصية | Next: Security & Privacy →](06_Security_Privacy.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
