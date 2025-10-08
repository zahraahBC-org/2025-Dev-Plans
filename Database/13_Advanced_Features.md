# 13. الميزات المتقدمة | Advanced Features
## المجموعات، الباقات، وCOD المتقدم | Collections, Bundles, and Advanced COD

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد الميزات المتقدمة للتجارة الإلكترونية  
**Purpose**: Define advanced e-commerce features

**الجمهور**: مديرو المنتجات، مطورو الواجهة الخلفية  
**Audience**: Product managers, backend developers

**النطاق**: المجموعات، الباقات، إدارة COD المتقدمة  
**Scope**: Collections, product bundles, advanced COD management

---

## 🎯 **نظرة عامة | Overview**

هذا المستند يغطي الميزات المتقدمة التي تعزز تجربة التسوق وتزيد المبيعات.

---

## 📑 **جدول المحتويات | Table of Contents**

1. [المجموعات | Collections](#collections)
2. [باقات المنتجات | Product Bundles](#product-bundles)
3. [عروض BOGO | Buy One Get One](#bogo)
4. [إدارة COD المتقدمة | Advanced COD Management](#advanced-cod)
5. [التوصيات الذكية | Smart Recommendations](#smart-recommendations)

---

## 1. المجموعات | Collections {#collections}

### **جدول المجموعات | Collections Table**

```sql
CREATE TABLE collections (
    collection_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    
    -- الأسماء
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    description_ar TEXT,
    description_en TEXT,
    
    -- النوع
    type ENUM('manual', 'automated') NOT NULL,
    
    -- القواعد التلقائية (للمجموعات الآلية)
    rules JSON,  -- مثال: {"category_id": 5, "badges": ["new"], "created_within_days": 30}
    
    -- العرض
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    banner_image_url VARCHAR(500),
    
    -- الصلاحية
    valid_from DATETIME,
    valid_until DATETIME,
    
    -- الحالة
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    INDEX idx_type_active (type, is_active),
    INDEX idx_featured (is_featured, display_order)
) ENGINE=InnoDB;

-- جدول منتجات المجموعة (للمجموعات اليدوية)
CREATE TABLE collection_products (
    collection_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    display_order INT DEFAULT 0,
    added_at DATETIME NOT NULL,
    
    PRIMARY KEY (collection_id, product_id),
    FOREIGN KEY (collection_id) REFERENCES collections(collection_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    
    INDEX idx_collection_order (collection_id, display_order)
) ENGINE=InnoDB;
```

---

## 2. باقات المنتجات | Product Bundles {#product-bundles}

### **جدول الباقات | Bundles Table**

```sql
CREATE TABLE product_bundles (
    bundle_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bundle_code VARCHAR(50) UNIQUE NOT NULL,
    
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    description_ar TEXT,
    
    -- التسعير
    bundle_price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2) NOT NULL,  -- مجموع أسعار المنتجات الفردية
    savings_amount DECIMAL(10,2) NOT NULL,  -- الوفر
    savings_pct DECIMAL(5,2) NOT NULL,      -- % الوفر
    
    -- الصلاحية
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    
    -- المخزون
    max_quantity INT,  -- الحد الأقصى المتاح
    sold_quantity INT DEFAULT 0,
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    INDEX idx_active_dates (is_active, valid_from, valid_until)
) ENGINE=InnoDB;

-- منتجات الباقة
CREATE TABLE bundle_items (
    bundle_id BIGINT NOT NULL,
    variant_id BIGINT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,  -- كمية كل منتج في الباقة
    
    PRIMARY KEY (bundle_id, variant_id),
    FOREIGN KEY (bundle_id) REFERENCES product_bundles(bundle_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
) ENGINE=InnoDB;
```

---

## 3. عروض BOGO | Buy One Get One {#bogo}

### **جدول عروض BOGO | BOGO Offers Table**

```sql
CREATE TABLE bogo_offers (
    offer_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    offer_code VARCHAR(50) UNIQUE NOT NULL,
    
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    
    -- القاعدة: اشتري X احصل على Y
    buy_quantity INT NOT NULL,      -- اشتري كم
    get_quantity INT NOT NULL,      -- احصل على كم
    get_discount_pct DECIMAL(5,2),  -- بخصم % (0-100، 100=مجاني)
    
    -- الأهلية
    eligible_categories JSON,  -- أي الفئات
    eligible_variants JSON,    -- أي المنتجات
    
    -- الحدود
    max_applications_per_order INT DEFAULT 1,
    min_order_value DECIMAL(10,2),
    
    -- الصلاحية
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    INDEX idx_active_dates (is_active, valid_from, valid_until)
) ENGINE=InnoDB;
```

---

## 4. إدارة COD المتقدمة | Advanced COD Management {#advanced-cod}

### **عتبات الحظر الديناميكية | Dynamic Block Thresholds**

```sql
CREATE TABLE cod_risk_config (
    config_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- عتبات الحظر
    failed_attempts_temp_block INT DEFAULT 2,   -- حظر مؤقت بعد محاولتين
    failed_attempts_perm_block INT DEFAULT 5,   -- حظر دائم بعد 5 محاولات
    
    temp_block_duration_days INT DEFAULT 30,    -- مدة الحظر المؤقت
    
    -- القيود حسب المدينة
    high_risk_cities JSON,  -- ["City1", "City2"]
    max_cod_amount_high_risk DECIMAL(10,2),
    
    -- متطلبات إضافية
    require_address_verification BOOLEAN DEFAULT TRUE,
    require_otp_above_amount DECIMAL(10,2),
    
    is_active BOOLEAN DEFAULT TRUE,
    effective_from DATETIME NOT NULL,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
) ENGINE=InnoDB;
```

---

### **تقارير فشل COD حسب المدينة | COD Failure Reports by City**

```sql
-- تقرير فشل COD حسب المدينة
SELECT 
    a.city,
    COUNT(DISTINCT o.order_id) AS total_cod_orders,
    COUNT(DISTINCT CASE WHEN s.status = 'failed' 
                        THEN o.order_id END) AS failed_deliveries,
    COUNT(DISTINCT CASE WHEN s.status = 'failed' 
                        THEN o.order_id END) * 100.0 / 
    COUNT(DISTINCT o.order_id) AS failure_rate_pct,
    
    -- الأسباب الشائعة
    JSON_OBJECTAGG(
        COALESCE(da.failure_reason, 'unknown'),
        COUNT(da.attempt_id)
    ) AS failure_reasons
FROM orders o
JOIN addresses a ON o.shipping_address_id = a.address_id
JOIN shipments s ON o.order_id = s.order_id
LEFT JOIN delivery_attempts da ON s.shipment_id = da.shipment_id 
    AND da.attempt_status = 'failed'
WHERE o.payment_method = 'cod'
  AND o.created_at >= CURDATE() - INTERVAL 30 DAY
GROUP BY a.city
ORDER BY failure_rate_pct DESC;
```

---

## 5. التوصيات الذكية | Smart Recommendations {#smart-recommendations}

### **المنتجات ذات الصلة | Related Products**

```sql
CREATE TABLE product_relations (
    relation_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    related_product_id BIGINT NOT NULL,
    
    -- نوع العلاقة
    relation_type ENUM(
        'similar',          -- مشابه
        'complementary',    -- مكمل
        'alternative',      -- بديل
        'frequently_bought' -- يُشترى معه
    ) NOT NULL,
    
    -- القوة/التصنيف
    strength_score DECIMAL(5,4),  -- 0-1
    
    -- المصدر
    source ENUM('manual', 'ml_model', 'purchase_history') NOT NULL,
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (related_product_id) REFERENCES products(related_product_id),
    
    UNIQUE KEY uk_product_relation (product_id, related_product_id, relation_type),
    INDEX idx_product_type (product_id, relation_type, strength_score DESC)
) ENGINE=InnoDB;
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 12. خدمات التكامل | Previous: Integration Services](12_Integration_Services.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

[📂 الملاحق | Appendices →](Appendices/)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
