# 11. نظام المشتريات والتوريد | Procurement System
## إدارة الموردين وأوامر الشراء | Supplier Management and Purchase Orders

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد نظام كامل لإدارة المشتريات والتوريد  
**Purpose**: Define complete procurement and inbound management system

**الجمهور**: مديرو المشتريات، فريق المخزون، المحاسبون  
**Audience**: Procurement managers, inventory team, accountants

**النطاق**: الموردين، أوامر الشراء، الاستلام، Landed Cost  
**Scope**: Suppliers, purchase orders, receiving, landed cost

---

## 🎯 **نظرة عامة | Overview**

نظام المشتريات يوفر إدارة كاملة لسلسلة التوريد من اختيار المورد إلى استلام البضائع وإدخالها للمخزون مع حساب التكلفة الفعلية.

**الأهداف الرئيسية**:
- ✅ تأمين توفر المنتجات بالكميات الصحيحة
- ✅ تتبع التوريد من الطلب إلى الاستلام
- ✅ حساب التكلفة الحقيقية Landed Cost
- ✅ قياس أداء الموردين
- ✅ تقليل نفاد المخزون Stockouts

---

## 📑 **جدول المحتويات | Table of Contents**

1. [إدارة الموردين | Supplier Management](#supplier-management)
2. [أوامر الشراء PO | Purchase Orders](#purchase-orders)
3. [الشحنات الواردة ASN | Inbound Shipments](#inbound-shipments)
4. [الاستلام والفحص GRN | Goods Receipt](#goods-receipt)
5. [التكلفة النهائية Landed Cost | Landed Cost](#landed-cost)
6. [المطابقة الثلاثية | 3-Way Matching](#three-way-matching)
7. [مرتجعات الموردين RTV | Return to Vendor](#return-to-vendor)
8. [قواعد إعادة الطلب | Reorder Rules](#reorder-rules)

---

## 1. إدارة الموردين | Supplier Management {#supplier-management}

### **جدول الموردين | Suppliers Table**

```sql
CREATE TABLE suppliers (
    supplier_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    supplier_code VARCHAR(50) UNIQUE NOT NULL,
    
    -- معلومات أساسية
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    
    -- جهة الاتصال
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    country CHAR(2),
    
    -- الشروط التجارية
    payment_terms ENUM('cash', 'net_7', 'net_15', 'net_30', 'net_60') NOT NULL,
    default_currency CHAR(3) NOT NULL DEFAULT 'SAR',
    lead_time_days INT,  -- مدة التوريد المتوقعة
    min_order_quantity INT,  -- MOQ
    incoterms VARCHAR(10),  -- EXW، FOB، CIF، DDP
    
    -- التقييم
    rating DECIMAL(3,2),  -- 0-5
    on_time_delivery_pct DECIMAL(5,2),
    defect_rate_pct DECIMAL(5,2),
    
    -- الحالة
    status ENUM('active', 'inactive', 'blacklisted') NOT NULL DEFAULT 'active',
    
    -- البيانات الوصفية
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    INDEX idx_status (status),
    INDEX idx_rating (rating)
) ENGINE=InnoDB;
```

---

## 2. أوامر الشراء PO | Purchase Orders {#purchase-orders}

### **جدول أوامر الشراء | Purchase Orders Table**

```sql
CREATE TABLE purchase_orders (
    po_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    po_no VARCHAR(20) UNIQUE NOT NULL,  -- PO-20250108-001
    
    supplier_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,  -- المستودع المستلم
    
    -- التواريخ
    order_date DATETIME NOT NULL,
    expected_delivery_date DATE,
    approved_at DATETIME,
    closed_at DATETIME,
    
    -- الحالة
    status ENUM(
        'draft',         -- مسودة
        'submitted',     -- مرسل للمورد
        'approved',      -- موافق عليه
        'partial',       -- استلام جزئي
        'completed',     -- مكتمل
        'cancelled'      -- ملغي
    ) NOT NULL DEFAULT 'draft',
    
    -- المبالغ
    subtotal DECIMAL(12,2) NOT NULL,
    shipping_cost DECIMAL(12,2) DEFAULT 0.00,
    insurance_cost DECIMAL(12,2) DEFAULT 0.00,
    customs_cost DECIMAL(12,2) DEFAULT 0.00,
    other_costs DECIMAL(12,2) DEFAULT 0.00,
    total DECIMAL(12,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    
    -- سعر الصرف (إذا مختلف عن العملة الأساسية)
    exchange_rate DECIMAL(10,6),
    exchange_rate_date DATE,
    
    -- الموافقات
    created_by BIGINT NOT NULL,
    approved_by BIGINT,
    
    -- البيانات الوصفية
    notes TEXT,
    attachments JSON,  -- روابط لملفات (عروض أسعار، عقود)
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    
    INDEX idx_supplier_status (supplier_id, status),
    INDEX idx_order_date (order_date),
    INDEX idx_expected_delivery (expected_delivery_date)
) ENGINE=InnoDB;
```

---

### **جدول بنود أوامر الشراء | PO Items Table**

```sql
CREATE TABLE purchase_order_items (
    po_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    po_id BIGINT NOT NULL,
    variant_id BIGINT NOT NULL,
    
    -- الكميات
    quantity_ordered INT NOT NULL,
    quantity_received INT DEFAULT 0,
    quantity_remaining INT NOT NULL,  -- محسوب
    
    -- التسعير
    unit_cost DECIMAL(10,2) NOT NULL,  -- سعر الشراء
    discount_per_unit DECIMAL(10,2) DEFAULT 0.00,
    net_unit_cost DECIMAL(10,2) NOT NULL,  -- بعد الخصم
    line_total DECIMAL(12,2) NOT NULL,
    
    -- التكلفة النهائية (بعد توزيع Landed Cost)
    landed_cost_per_unit DECIMAL(10,2),
    
    -- التواريخ
    expected_delivery_date DATE,
    
    -- الحالة
    status ENUM('pending', 'partial', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
    
    notes TEXT,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id),
    
    INDEX idx_po (po_id),
    INDEX idx_variant (variant_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

---

## 3. الشحنات الواردة ASN | Inbound Shipments {#inbound-shipments}

### **جدول الشحنات الواردة | Inbound Shipments Table**

```sql
CREATE TABLE inbound_shipments (
    shipment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    shipment_no VARCHAR(20) UNIQUE NOT NULL,  -- ASN-20250108-001
    
    po_id BIGINT NOT NULL,
    supplier_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    
    -- معلومات الشحن
    carrier VARCHAR(100),
    tracking_number VARCHAR(100),
    shipping_method ENUM('air', 'sea', 'land') NOT NULL,
    container_number VARCHAR(50),
    
    -- التواريخ
    shipped_date DATE,
    estimated_arrival DATE,  -- ETA
    actual_arrival DATE,
    
    -- الحالة
    status ENUM(
        'pending',       -- في انتظار الشحن
        'in_transit',    -- في الطريق
        'customs',       -- في الجمارك
        'arrived',       -- وصل المستودع
        'receiving',     -- قيد الاستلام
        'completed'      -- مكتمل
    ) NOT NULL DEFAULT 'pending',
    
    -- القياسات
    total_weight_kg DECIMAL(10,3),
    total_volume_m3 DECIMAL(10,3),
    package_count INT,
    
    notes TEXT,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    
    INDEX idx_po (po_id),
    INDEX idx_tracking (tracking_number),
    INDEX idx_status_eta (status, estimated_arrival)
) ENGINE=InnoDB;
```

---

## 4. الاستلام والفحص GRN | Goods Receipt {#goods-receipt}

### **جدول إثباتات الاستلام | Goods Receipt Notes Table**

```sql
CREATE TABLE goods_receipts (
    grn_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grn_no VARCHAR(20) UNIQUE NOT NULL,  -- GRN-20250108-001
    
    po_id BIGINT NOT NULL,
    shipment_id BIGINT,
    warehouse_id BIGINT NOT NULL,
    
    -- التواريخ
    received_date DATETIME NOT NULL,
    inspected_date DATETIME,
    
    -- الحالة
    status ENUM('pending_inspection', 'inspected', 'posted') NOT NULL DEFAULT 'pending_inspection',
    
    -- المستلم
    received_by BIGINT NOT NULL,
    inspected_by BIGINT,
    
    notes TEXT,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    FOREIGN KEY (shipment_id) REFERENCES inbound_shipments(shipment_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    
    INDEX idx_po (po_id),
    INDEX idx_received_date (received_date),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

---

### **جدول بنود الاستلام | GRN Items Table**

```sql
CREATE TABLE grn_items (
    grn_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grn_id BIGINT NOT NULL,
    po_item_id BIGINT NOT NULL,
    variant_id BIGINT NOT NULL,
    
    -- الكميات
    quantity_ordered INT NOT NULL,  -- من PO
    quantity_received INT NOT NULL,  -- الفعلي
    quantity_accepted INT NOT NULL,  -- بعد QC
    quantity_rejected INT DEFAULT 0,  -- معيب/تالف
    
    -- نتيجة فحص الجودة
    qc_status ENUM('pending', 'pass', 'fail', 'partial') NOT NULL DEFAULT 'pending',
    qc_notes TEXT,
    
    -- التكلفة
    unit_cost DECIMAL(10,2) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL,
    
    -- القرار
    disposition ENUM(
        'accept',        -- قبول وإدخال للمخزون
        'reject',        -- رفض RTV
        'rework',        -- إعادة معالجة
        'discount'       -- قبول بخصم
    ),
    
    FOREIGN KEY (grn_id) REFERENCES goods_receipts(grn_id),
    FOREIGN KEY (po_item_id) REFERENCES purchase_order_items(po_item_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id),
    
    INDEX idx_grn (grn_id),
    INDEX idx_po_item (po_item_id),
    INDEX idx_qc_status (qc_status)
) ENGINE=InnoDB;
```

---

## 5. التكلفة النهائية Landed Cost | Landed Cost {#landed-cost}

### **جدول تكاليف الشحن | Shipping Costs Table**

```sql
CREATE TABLE landed_costs (
    cost_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    po_id BIGINT NOT NULL,
    grn_id BIGINT,
    
    -- نوع التكلفة
    cost_type ENUM(
        'shipping',      -- شحن
        'insurance',     -- تأمين
        'customs',       -- جمارك
        'handling',      -- مناولة
        'other'          -- أخرى
    ) NOT NULL,
    
    -- المبلغ
    amount DECIMAL(12,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    
    -- طريقة التوزيع
    allocation_method ENUM(
        'value',         -- حسب القيمة
        'weight',        -- حسب الوزن
        'volume',        -- حسب الحجم
        'quantity',      -- حسب الكمية
        'manual'         -- يدوي
    ) NOT NULL DEFAULT 'value',
    
    -- البيانات الوصفية
    description VARCHAR(255),
    reference_no VARCHAR(100),  -- رقم فاتورة الشحن مثلاً
    
    created_at DATETIME NOT NULL,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    FOREIGN KEY (grn_id) REFERENCES goods_receipts(grn_id),
    
    INDEX idx_po (po_id),
    INDEX idx_type (cost_type)
) ENGINE=InnoDB;
```

---

### **حساب Landed Cost | Calculate Landed Cost**

```sql
-- توزيع التكاليف الإضافية على البنود
DELIMITER //
CREATE PROCEDURE sp_calculate_landed_cost(IN p_grn_id BIGINT)
BEGIN
    DECLARE v_total_value DECIMAL(12,2);
    DECLARE v_total_additional_costs DECIMAL(12,2);
    
    -- 1. حساب إجمالي قيمة البنود
    SELECT SUM(quantity_accepted * unit_cost)
    INTO v_total_value
    FROM grn_items
    WHERE grn_id = p_grn_id;
    
    -- 2. حساب إجمالي التكاليف الإضافية
    SELECT SUM(amount)
    INTO v_total_additional_costs
    FROM landed_costs
    WHERE grn_id = p_grn_id;
    
    -- 3. توزيع التكاليف على البنود (حسب القيمة)
    UPDATE grn_items gi
    JOIN (
        SELECT 
            grn_item_id,
            unit_cost + (
                (quantity_accepted * unit_cost / v_total_value) * 
                v_total_additional_costs / quantity_accepted
            ) AS calculated_landed_cost
        FROM grn_items
        WHERE grn_id = p_grn_id
    ) calc ON gi.grn_item_id = calc.grn_item_id
    SET gi.landed_cost_per_unit = calc.calculated_landed_cost;
    
    -- 4. تحديث PO items
    UPDATE purchase_order_items poi
    JOIN grn_items gi ON poi.po_item_id = gi.po_item_id
    SET poi.landed_cost_per_unit = gi.landed_cost_per_unit
    WHERE gi.grn_id = p_grn_id;
    
END//
DELIMITER ;
```

---

## 6. المطابقة الثلاثية | 3-Way Matching {#three-way-matching}

### **جدول فواتير الموردين | Supplier Invoices Table**

```sql
CREATE TABLE supplier_invoices (
    invoice_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    invoice_no VARCHAR(50) UNIQUE NOT NULL,
    
    supplier_id BIGINT NOT NULL,
    po_id BIGINT NOT NULL,
    
    -- التواريخ
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    
    -- المبالغ
    subtotal DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    total DECIMAL(12,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    
    -- حالة المطابقة
    match_status ENUM(
        'pending',       -- في انتظار المطابقة
        'matched',       -- مطابق تماماً
        'variance',      -- فروقات ضمن التحمل
        'exception'      -- استثناء يحتاج مراجعة
    ) NOT NULL DEFAULT 'pending',
    
    -- الفروقات
    quantity_variance INT DEFAULT 0,
    price_variance DECIMAL(12,2) DEFAULT 0.00,
    variance_notes TEXT,
    
    -- حالة الدفع
    payment_status ENUM('unpaid', 'partial', 'paid') NOT NULL DEFAULT 'unpaid',
    paid_amount DECIMAL(12,2) DEFAULT 0.00,
    paid_at DATETIME,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    
    INDEX idx_supplier (supplier_id),
    INDEX idx_po (po_id),
    INDEX idx_match_status (match_status),
    INDEX idx_due_date (due_date)
) ENGINE=InnoDB;
```

---

### **إجراء المطابقة الثلاثية | 3-Way Match Procedure**

```sql
-- مطابقة PO ↔ GRN ↔ Invoice
DELIMITER //
CREATE PROCEDURE sp_three_way_match(IN p_invoice_id BIGINT)
BEGIN
    DECLARE v_po_total DECIMAL(12,2);
    DECLARE v_grn_total DECIMAL(12,2);
    DECLARE v_invoice_total DECIMAL(12,2);
    DECLARE v_variance DECIMAL(12,2);
    DECLARE v_tolerance DECIMAL(5,2) DEFAULT 0.05;  -- تحمل 5%
    
    -- 1. الحصول على مجاميع
    SELECT total INTO v_invoice_total
    FROM supplier_invoices
    WHERE invoice_id = p_invoice_id;
    
    SELECT SUM(quantity_ordered * net_unit_cost) INTO v_po_total
    FROM purchase_order_items
    WHERE po_id = (SELECT po_id FROM supplier_invoices WHERE invoice_id = p_invoice_id);
    
    SELECT SUM(quantity_accepted * unit_cost) INTO v_grn_total
    FROM grn_items gi
    JOIN goods_receipts gr ON gi.grn_id = gr.grn_id
    WHERE gr.po_id = (SELECT po_id FROM supplier_invoices WHERE invoice_id = p_invoice_id);
    
    -- 2. حساب الفرق
    SET v_variance = ABS(v_invoice_total - v_grn_total);
    
    -- 3. تحديد حالة المطابقة
    IF v_variance = 0 THEN
        UPDATE supplier_invoices
        SET match_status = 'matched'
        WHERE invoice_id = p_invoice_id;
        
    ELSEIF v_variance / v_grn_total <= v_tolerance THEN
        UPDATE supplier_invoices
        SET match_status = 'variance',
            price_variance = v_variance,
            variance_notes = CONCAT('فرق ضمن التحمل: ', v_variance)
        WHERE invoice_id = p_invoice_id;
        
    ELSE
        UPDATE supplier_invoices
        SET match_status = 'exception',
            price_variance = v_variance,
            variance_notes = CONCAT('فرق كبير يحتاج مراجعة: ', v_variance)
        WHERE invoice_id = p_invoice_id;
    END IF;
    
END//
DELIMITER ;
```

---

## 7. مرتجعات الموردين RTV | Return to Vendor {#return-to-vendor}

### **جدول المرتجعات للموردين | RTV Table**

```sql
CREATE TABLE return_to_vendor (
    rtv_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rtv_no VARCHAR(20) UNIQUE NOT NULL,  -- RTV-20250108-001
    
    supplier_id BIGINT NOT NULL,
    grn_id BIGINT NOT NULL,
    
    -- السبب
    reason ENUM(
        'defective',     -- معيب
        'wrong_item',    -- صنف خاطئ
        'damaged',       -- تالف
        'excess',        -- فائض
        'other'          -- أخرى
    ) NOT NULL,
    
    -- الحالة
    status ENUM(
        'requested',     -- تم الطلب
        'approved',      -- موافق
        'shipped',       -- تم الشحن للمورد
        'credited',      -- تم الإئتمان
        'closed'         -- مغلق
    ) NOT NULL DEFAULT 'requested',
    
    -- المبالغ
    total_value DECIMAL(12,2) NOT NULL,
    credit_note_no VARCHAR(50),  -- رقم مذكرة الخصم
    credit_amount DECIMAL(12,2),
    
    -- التواريخ
    requested_date DATETIME NOT NULL,
    shipped_date DATE,
    credited_date DATE,
    
    notes TEXT,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (grn_id) REFERENCES goods_receipts(grn_id),
    
    INDEX idx_supplier (supplier_id),
    INDEX idx_grn (grn_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

---

## 8. قواعد إعادة الطلب | Reorder Rules {#reorder-rules}

### **جدول قواعد إعادة الطلب | Reorder Rules Table**

```sql
CREATE TABLE reorder_rules (
    rule_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    variant_id BIGINT UNIQUE NOT NULL,
    warehouse_id BIGINT NOT NULL,
    
    -- نقطة إعادة الطلب
    reorder_point INT NOT NULL,  -- عندما يصل المخزون لهذا الحد
    
    -- كمية إعادة الطلب
    reorder_quantity INT NOT NULL,  -- كم نطلب
    
    -- المخزون الآمن
    safety_stock INT NOT NULL,  -- المخزون الاحتياطي
    
    -- مدة التوريد
    lead_time_days INT NOT NULL,
    
    -- المورد المفضل
    preferred_supplier_id BIGINT,
    
    -- الحالة
    is_active BOOLEAN DEFAULT TRUE,
    
    last_calculated_at DATETIME,
    
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (preferred_supplier_id) REFERENCES suppliers(supplier_id),
    
    INDEX idx_variant_warehouse (variant_id, warehouse_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB;
```

---

### **مراقبة إعادة الطلب | Reorder Monitoring**

```sql
-- استعلام لإيجاد المنتجات التي تحتاج إعادة طلب
SELECT 
    rr.variant_id,
    pv.sku,
    pv.name_ar,
    ss.available_to_promise AS current_stock,
    rr.reorder_point,
    rr.reorder_quantity,
    rr.preferred_supplier_id,
    s.name_ar AS supplier_name,
    rr.lead_time_days
FROM reorder_rules rr
JOIN product_variants pv ON rr.variant_id = pv.variant_id
JOIN stock_snapshot ss ON rr.variant_id = ss.variant_id 
    AND rr.warehouse_id = ss.warehouse_id
LEFT JOIN suppliers s ON rr.preferred_supplier_id = s.supplier_id
WHERE rr.is_active = TRUE
  AND ss.available_to_promise <= rr.reorder_point
ORDER BY ss.available_to_promise ASC;
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 10. قائمة أفضل الممارسات | Previous: Best Practices](10_Best_Practices.md)

[التالي: 12. خدمات التكامل | Next: Integration Services →](12_Integration_Services.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
