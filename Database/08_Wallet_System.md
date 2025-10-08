# 08. نظام المحفظة | Wallet System
## التنفيذ الكامل مع المعاملات ودفتر اليومية | Complete Implementation with Transactions and Ledger

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد التنفيذ الكامل لنظام محفظة العملاء  
**Purpose**: Define complete implementation of customer wallet system

**الجمهور**: مطورو الواجهة الخلفية، مهندسو الدفع، منطق الأعمال  
**Audience**: Backend developers, payment engineers, business logic

**النطاق**: المحفظة، المعاملات، الحجز، بطاقات الهدايا، الاسترداد النقدي  
**Scope**: Wallet, transactions, holds, gift cards, cashback

---

## 🎯 **نظرة عامة | Overview**

نظام المحفظة يوفر رصيد متجر رقمي للعملاء، يمكن استخدامه في المشتريات، واسترداد المبالغ، وبرامج الولاء. النظام مصمم لضمان السلامة المالية، منع الأرصدة السالبة، والتكامل السلس مع نظام الطلبات.

**الأهداف الرئيسية**:
- ✅ **رصيد متجر آمن** للاستخدام في الشراء والاسترداد
- ✅ **تقليل زمن الإغلاق المالي** لحالات RMA و COD
- ✅ **تحفيز الولاء** عبر Cashback وبطاقات الهدايا
- ✅ **منع الاحتيال** عبر حدود وقواعد صارمة

---

## 📑 **جدول المحتويات | Table of Contents**

1. [معمارية المحفظة | Wallet Architecture](#wallet-architecture)
2. [مخطط قاعدة البيانات | Database Schema](#database-schema)
3. [أنواع المعاملات | Transaction Types](#transaction-types)
4. [نمط Ledger | Ledger Pattern](#ledger-pattern)
5. [حجز وإطلاق الأموال | Hold & Release](#hold-release)
6. [بطاقات الهدايا | Gift Cards](#gift-cards)
7. [الاسترداد النقدي Cashback | Cashback](#cashback)
8. [التسوية المحاسبية | Accounting Reconciliation](#accounting-reconciliation)
9. [الحالات الحدية | Edge Cases](#edge-cases)
10. [مؤشرات الأداء | KPIs](#kpis)

---

## 1. معمارية المحفظة | Wallet Architecture {#wallet-architecture}

### **نمط دفتر اليومية | Ledger Pattern**

⚠️ **مبدأ أساسي**: المحفظة تستخدم **نمط Ledger** - جميع المعاملات append-only، الرصيد يُحسب بالتجميع.

```
┌─────────────────────────────────────────────────┐
│           Wallet Account (حساب المحفظة)        │
│  - customer_id                                  │
│  - currency                                     │
│  - balance (محسوب)                             │
│  - status                                       │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│      Wallet Transactions (معاملات المحفظة)     │
│  - transaction_id                               │
│  - type: Credit/Debit/Hold/Release              │
│  - amount                                       │
│  - source: Refund/Cashback/Gift/TopUp           │
│  - balance_before / balance_after               │
│  - created_at                                   │
└─────────────────────────────────────────────────┘
```

---

## 2. مخطط قاعدة البيانات | Database Schema {#database-schema}

### **جدول المحافظ | Wallets Table**

```sql
CREATE TABLE wallets (
    wallet_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT UNIQUE NOT NULL,  -- محفظة واحدة لكل عميل
    
    -- العملة
    currency CHAR(3) NOT NULL DEFAULT 'SAR',
    
    -- الأرصدة
    balance_available DECIMAL(10,2) NOT NULL DEFAULT 0.00,  -- قابل للاستخدام
    balance_on_hold DECIMAL(10,2) NOT NULL DEFAULT 0.00,     -- محجوز
    
    -- إجمالي الرصيد = available + on_hold
    
    -- الحالة
    status ENUM('active', 'frozen', 'closed') NOT NULL DEFAULT 'active',
    
    -- البيانات الوصفية
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    -- القيود
    CONSTRAINT chk_balance_non_negative CHECK (balance_available >= 0),
    CONSTRAINT chk_hold_non_negative CHECK (balance_on_hold >= 0),
    
    INDEX idx_customer (customer_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

**حالات المحفظة**:
- `active`: طبيعية، يمكن الإضافة والخصم
- `frozen`: لا خصم، الإضافة مسموحة (مؤقت)
- `closed`: لا معاملات (حساب مغلق)

---

### **جدول معاملات المحفظة | Wallet Transactions Table**

```sql
CREATE TABLE wallet_transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    wallet_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,  -- للفهرسة السريعة
    
    -- نوع المعاملة
    type ENUM('credit', 'debit', 'hold', 'release', 'hold_capture', 'reversal') NOT NULL,
    
    -- المبلغ (دائماً موجب)
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    
    -- المصدر والمرجع
    source ENUM(
        'refund',       -- استرداد من RMA
        'cashback',     -- استرداد نقدي ترويجي
        'gift_card',    -- بطاقة هدايا
        'top_up',       -- تعبئة من العميل
        'purchase',     -- استخدام في طلب
        'promo',        -- اعتماد ترويجي
        'loyalty',      -- مكافأة ولاء
        'adjustment',   -- تعديل يدوي
        'compensation'  -- تعويض
    ) NOT NULL,
    
    reference_type VARCHAR(50),  -- order، rma، gift_card، etc
    reference_id BIGINT,
    
    -- الحالة
    status ENUM('pending', 'posted', 'reversed', 'expired') NOT NULL DEFAULT 'pending',
    
    -- الأرصدة (للتدقيق)
    balance_before DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(10,2) NOT NULL,
    
    -- السياق
    reason_code VARCHAR(100),  -- سبب مفصل
    notes TEXT,
    performed_by BIGINT,  -- user_id (نظام/موظف)
    performed_by_type ENUM('system', 'staff', 'customer') NOT NULL,
    
    -- الطوابع الزمنية
    transaction_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted_at DATETIME,  -- متى تم الترحيل
    expires_at DATETIME,  -- للكاش باك ذو الصلاحية
    
    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    -- القيود
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    
    INDEX idx_wallet_date (wallet_id, transaction_date DESC),
    INDEX idx_customer_date (customer_id, transaction_date DESC),
    INDEX idx_reference (reference_type, reference_id),
    INDEX idx_status (status),
    INDEX idx_expires (expires_at)
) ENGINE=InnoDB;
```

---

### **جدول حجوزات المحفظة | Wallet Holds Table**

```sql
CREATE TABLE wallet_holds (
    hold_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    wallet_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    
    -- المبلغ المحجوز
    amount DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    
    -- المرجع (عادةً cart أو order)
    reference_type VARCHAR(50) NOT NULL,  -- cart، order
    reference_id BIGINT NOT NULL,
    
    -- الحالة
    status ENUM('active', 'captured', 'released', 'expired') NOT NULL DEFAULT 'active',
    
    -- الطوابع الزمنية
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,  -- الإطلاق التلقائي
    captured_at DATETIME,
    released_at DATETIME,
    
    -- معرّف المعاملة المرتبطة
    transaction_id BIGINT,  -- FK إلى wallet_transactions
    
    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (transaction_id) REFERENCES wallet_transactions(transaction_id),
    
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    
    INDEX idx_wallet_status (wallet_id, status),
    INDEX idx_reference (reference_type, reference_id),
    INDEX idx_expires (expires_at)
) ENGINE=InnoDB;
```

---

## 3. أنواع المعاملات | Transaction Types {#transaction-types}

### **Credit (إضافة رصيد)**

**الأسباب**:
- استرداد من RMA
- استرداد نقدي Cashback
- بطاقة هدايا
- تعبئة من العميل
- تعويض من خدمة العملاء

```sql
-- مثال: إضافة رصيد من RMA
START TRANSACTION;

-- 1. قفل المحفظة
SELECT balance_available INTO @current_balance
FROM wallets
WHERE customer_id = 123
FOR UPDATE;

-- 2. إنشاء معاملة Credit
INSERT INTO wallet_transactions (
    wallet_id,
    customer_id,
    type,
    amount,
    currency,
    source,
    reference_type,
    reference_id,
    status,
    balance_before,
    balance_after,
    reason_code,
    performed_by_type,
    transaction_date
) VALUES (
    1,                      -- wallet_id
    123,                    -- customer_id
    'credit',
    50.00,
    'SAR',
    'refund',
    'rma',
    456,                    -- rma_id
    'posted',
    @current_balance,
    @current_balance + 50.00,
    'rma_refund',
    'system',
    NOW()
);

-- 3. تحديث رصيد المحفظة
UPDATE wallets
SET balance_available = balance_available + 50.00,
    updated_at = NOW()
WHERE customer_id = 123;

COMMIT;
```

---

### **Debit (خصم رصيد)**

**الأسباب**:
- دفع طلب
- انتهاء صلاحية
- تعديل يدوي (نادر)

```sql
-- مثال: خصم رصيد لطلب
START TRANSACTION;

-- 1. التحقق من الرصيد المتاح
SELECT balance_available INTO @current_balance
FROM wallets
WHERE customer_id = 123
FOR UPDATE;

IF @current_balance < 100.00 THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Insufficient wallet balance';
END IF;

-- 2. إنشاء معاملة Debit
INSERT INTO wallet_transactions (
    wallet_id,
    customer_id,
    type,
    amount,
    currency,
    source,
    reference_type,
    reference_id,
    status,
    balance_before,
    balance_after,
    reason_code,
    performed_by_type,
    transaction_date
) VALUES (
    1,
    123,
    'debit',
    100.00,
    'SAR',
    'purchase',
    'order',
    789,                    -- order_id
    'posted',
    @current_balance,
    @current_balance - 100.00,
    'order_payment',
    'system',
    NOW()
);

-- 3. تحديث رصيد المحفظة
UPDATE wallets
SET balance_available = balance_available - 100.00,
    updated_at = NOW()
WHERE customer_id = 123;

COMMIT;
```

---

### **Hold (حجز رصيد)**

**الاستخدام**: حجز أموال مؤقت عند بدء الدفع.

```sql
-- عند بدء الدفع
START TRANSACTION;

-- 1. التحقق من الرصيد
SELECT balance_available INTO @available
FROM wallets
WHERE customer_id = 123
FOR UPDATE;

IF @available < 100.00 THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Insufficient funds for hold';
END IF;

-- 2. إنشاء Hold
INSERT INTO wallet_holds (
    wallet_id,
    customer_id,
    amount,
    currency,
    reference_type,
    reference_id,
    status,
    expires_at
) VALUES (
    1,
    123,
    100.00,
    'SAR',
    'cart',
    456,
    'active',
    DATE_ADD(NOW(), INTERVAL 30 MINUTE)  -- انتهاء بعد 30 دقيقة
);

-- 3. تحديث balance_on_hold
UPDATE wallets
SET balance_on_hold = balance_on_hold + 100.00,
    balance_available = balance_available - 100.00,
    updated_at = NOW()
WHERE customer_id = 123;

COMMIT;
```

---

### **Hold Capture (التقاط الحجز)**

**الاستخدام**: تحويل الحجز إلى خصم فعلي عند تأكيد الطلب.

```sql
-- عند تأكيد الطلب
START TRANSACTION;

-- 1. الحصول على Hold
SELECT * INTO @hold
FROM wallet_holds
WHERE hold_id = 789
  AND status = 'active'
FOR UPDATE;

-- 2. إنشاء معاملة Debit (التقاط)
INSERT INTO wallet_transactions (
    wallet_id,
    customer_id,
    type,
    amount,
    currency,
    source,
    reference_type,
    reference_id,
    status,
    balance_before,
    balance_after,
    reason_code,
    performed_by_type,
    transaction_date
) VALUES (
    1,
    123,
    'hold_capture',
    100.00,
    'SAR',
    'purchase',
    'order',
    789,
    'posted',
    @current_balance,
    @current_balance - 100.00,
    'order_payment_from_hold',
    'system',
    NOW()
);

-- 3. تحديث Hold
UPDATE wallet_holds
SET status = 'captured',
    captured_at = NOW(),
    transaction_id = LAST_INSERT_ID()
WHERE hold_id = 789;

-- 4. تحديث المحفظة (نقل من hold إلى منخفض)
UPDATE wallets
SET balance_on_hold = balance_on_hold - 100.00,
    -- balance_available بقي منخفضاً من Hold
    updated_at = NOW()
WHERE customer_id = 123;

COMMIT;
```

---

### **Release (إطلاق الحجز)**

**الاستخدام**: إلغاء الحجز إذا ألغى العميل الطلب.

```sql
-- عند إلغاء الطلب
START TRANSACTION;

-- 1. الحصول على Hold
SELECT amount INTO @hold_amount
FROM wallet_holds
WHERE hold_id = 789
  AND status = 'active'
FOR UPDATE;

-- 2. تحديث Hold
UPDATE wallet_holds
SET status = 'released',
    released_at = NOW()
WHERE hold_id = 789;

-- 3. إعادة الرصيد
UPDATE wallets
SET balance_on_hold = balance_on_hold - @hold_amount,
    balance_available = balance_available + @hold_amount,
    updated_at = NOW()
WHERE customer_id = 123;

COMMIT;
```

---

## 4. نمط Ledger | Ledger Pattern {#ledger-pattern}

### **حساب الرصيد | Balance Calculation**

الرصيد **لا يُحفظ مباشرة**، بل يُحسب من دفتر اليومية:

```sql
-- حساب الرصيد من المعاملات
SELECT 
    customer_id,
    SUM(
        CASE 
            WHEN type IN ('credit', 'release') THEN amount
            WHEN type IN ('debit', 'hold', 'hold_capture') THEN -amount
            ELSE 0
        END
    ) AS calculated_balance
FROM wallet_transactions
WHERE customer_id = 123
  AND status = 'posted'
GROUP BY customer_id;

-- التحقق من التطابق مع wallets.balance_available
SELECT 
    w.customer_id,
    w.balance_available AS wallet_balance,
    COALESCE(SUM(
        CASE 
            WHEN wt.type IN ('credit', 'release') THEN wt.amount
            WHEN wt.type IN ('debit', 'hold', 'hold_capture') THEN -wt.amount
            ELSE 0
        END
    ), 0) AS ledger_balance,
    w.balance_available - COALESCE(SUM(...), 0) AS difference
FROM wallets w
LEFT JOIN wallet_transactions wt ON w.wallet_id = wt.wallet_id AND wt.status = 'posted'
WHERE w.customer_id = 123
GROUP BY w.customer_id, w.balance_available;
```

**تسوية يومية**: وظيفة تُشغل يومياً للتحقق من تطابق الأرصدة.

---

## 5. حجز وإطلاق الأموال | Hold & Release {#hold-release}

### **تدفق الحجز | Hold Flow**

```
العميل في الدفع
     ↓
بدء الدفع (Begin Checkout)
     ↓
إنشاء Hold (حجز 100 ريال)
     ↓
     ├─→ نجح الطلب → Capture (التقاط الحجز)
     │                      ↓
     │                  Debit من الرصيد
     │
     └─→ ألغى/فشل → Release (إطلاق الحجز)
                           ↓
                       إعادة للرصيد المتاح
```

### **انتهاء الحجز التلقائي | Auto-Expiry**

```sql
-- وظيفة تُشغل كل 5 دقائق
-- إطلاق الحجوزات المنتهية

START TRANSACTION;

-- البحث عن حجوزات منتهية
SELECT hold_id, wallet_id, customer_id, amount
FROM wallet_holds
WHERE status = 'active'
  AND expires_at < NOW()
FOR UPDATE;

-- إطلاق كل حجز
UPDATE wallet_holds
SET status = 'expired',
    released_at = NOW()
WHERE status = 'active'
  AND expires_at < NOW();

-- تحديث المحافظ
UPDATE wallets w
JOIN (
    SELECT 
        wallet_id,
        SUM(amount) as total_expired
    FROM wallet_holds
    WHERE status = 'expired'
      AND released_at BETWEEN DATE_SUB(NOW(), INTERVAL 5 MINUTE) AND NOW()
    GROUP BY wallet_id
) h ON w.wallet_id = h.wallet_id
SET w.balance_on_hold = w.balance_on_hold - h.total_expired,
    w.balance_available = w.balance_available + h.total_expired;

COMMIT;
```

---

## 6. بطاقات الهدايا | Gift Cards {#gift-cards}

### **جدول بطاقات الهدايا | Gift Cards Table**

```sql
CREATE TABLE gift_cards (
    gift_card_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,  -- رمز فريد
    
    -- القيم
    initial_value DECIMAL(10,2) NOT NULL,
    remaining_value DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'SAR',
    
    -- الحالة
    status ENUM('active', 'redeemed', 'expired', 'cancelled') NOT NULL DEFAULT 'active',
    
    -- الصلاحية
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    
    -- من ولمن
    purchased_by BIGINT,  -- customer_id الشاري
    redeemed_by BIGINT,   -- customer_id المستفيد
    
    -- الطوابع الزمنية
    purchased_at DATETIME NOT NULL,
    redeemed_at DATETIME,
    
    -- البيانات الوصفية
    usage_count INT DEFAULT 0,
    max_usage_count INT DEFAULT 1,  -- عادةً مرة واحدة
    
    notes TEXT,
    
    FOREIGN KEY (purchased_by) REFERENCES customers(customer_id),
    FOREIGN KEY (redeemed_by) REFERENCES customers(customer_id),
    
    CONSTRAINT chk_remaining_valid CHECK (remaining_value >= 0),
    CONSTRAINT chk_remaining_lte_initial CHECK (remaining_value <= initial_value),
    
    INDEX idx_code (code),
    INDEX idx_status_valid (status, valid_until),
    INDEX idx_purchased_by (purchased_by),
    INDEX idx_redeemed_by (redeemed_by)
) ENGINE=InnoDB;
```

### **استرداد بطاقة هدايا | Redeem Gift Card**

```sql
-- إجراء استرداد بطاقة هدايا
DELIMITER //
CREATE PROCEDURE sp_redeem_gift_card(
    IN p_code VARCHAR(50),
    IN p_customer_id BIGINT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_gift_card_id BIGINT;
    DECLARE v_remaining_value DECIMAL(10,2);
    DECLARE v_wallet_id BIGINT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'عملية الاسترداد فشلت';
    END;
    
    START TRANSACTION;
    
    -- 1. التحقق من بطاقة الهدايا
    SELECT 
        gift_card_id,
        remaining_value
    INTO v_gift_card_id, v_remaining_value
    FROM gift_cards
    WHERE code = p_code
      AND status = 'active'
      AND NOW() BETWEEN valid_from AND valid_until
    FOR UPDATE;
    
    IF v_gift_card_id IS NULL THEN
        SET p_success = FALSE;
        SET p_message = 'بطاقة غير صالحة أو منتهية';
        ROLLBACK;
    ELSE
        -- 2. الحصول على المحفظة
        SELECT wallet_id INTO v_wallet_id
        FROM wallets
        WHERE customer_id = p_customer_id
        FOR UPDATE;
        
        -- 3. إنشاء معاملة Credit
        INSERT INTO wallet_transactions (
            wallet_id, customer_id, type, amount, currency,
            source, reference_type, reference_id,
            status, balance_before, balance_after,
            reason_code, performed_by_type, transaction_date
        )
        SELECT 
            v_wallet_id,
            p_customer_id,
            'credit',
            v_remaining_value,
            currency,
            'gift_card',
            'gift_card',
            v_gift_card_id,
            'posted',
            balance_available,
            balance_available + v_remaining_value,
            'gift_card_redemption',
            'customer',
            NOW()
        FROM wallets
        WHERE wallet_id = v_wallet_id;
        
        -- 4. تحديث المحفظة
        UPDATE wallets
        SET balance_available = balance_available + v_remaining_value
        WHERE wallet_id = v_wallet_id;
        
        -- 5. تحديث بطاقة الهدايا
        UPDATE gift_cards
        SET status = 'redeemed',
            remaining_value = 0,
            redeemed_by = p_customer_id,
            redeemed_at = NOW(),
            usage_count = usage_count + 1
        WHERE gift_card_id = v_gift_card_id;
        
        SET p_success = TRUE;
        SET p_message = 'تم استرداد بطاقة الهدايا بنجاح';
        
        COMMIT;
    END IF;
END//
DELIMITER ;
```

---

## 7. الاسترداد النقدي Cashback | Cashback {#cashback}

### **جدول قواعد Cashback | Cashback Rules Table**

```sql
CREATE TABLE cashback_rules (
    rule_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rule_code VARCHAR(50) UNIQUE NOT NULL,
    
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- نوع الاسترداد
    type ENUM('percentage', 'fixed') NOT NULL,
    value DECIMAL(10,2) NOT NULL,  -- نسبة مئوية أو مبلغ ثابت
    
    -- الحدود
    min_order_value DECIMAL(10,2),  -- الحد الأدنى للطلب
    max_cashback DECIMAL(10,2),     -- الحد الأقصى للاسترداد
    
    -- الأهلية
    eligible_categories JSON,  -- فئات مؤهلة
    eligible_brands JSON,      -- علامات مؤهلة
    
    -- الصلاحية
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    
    -- فترة القفل
    lock_days INT DEFAULT 0,  -- أيام بعد التوصيل قبل الإتاحة
    cashback_expires_days INT DEFAULT 90,  -- صلاحية الرصيد
    
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_active_dates (is_active, valid_from, valid_until)
) ENGINE=InnoDB;
```

---

### **منح Cashback | Grant Cashback**

```sql
-- وظيفة تُشغل بعد التوصيل + فترة المرتجع
DELIMITER //
CREATE PROCEDURE sp_grant_cashback(IN p_order_id BIGINT)
BEGIN
    DECLARE v_customer_id BIGINT;
    DECLARE v_order_total DECIMAL(10,2);
    DECLARE v_cashback_amount DECIMAL(10,2);
    DECLARE v_wallet_id BIGINT;
    
    START TRANSACTION;
    
    -- 1. الحصول على تفاصيل الطلب
    SELECT customer_id, total
    INTO v_customer_id, v_order_total
    FROM orders
    WHERE order_id = p_order_id
      AND status = 'delivered'
      AND delivered_at < DATE_SUB(NOW(), INTERVAL 7 DAY)  -- بعد فترة المرتجع
    FOR UPDATE;
    
    -- 2. حساب Cashback (مثال: 5% من إجمالي الطلب)
    SET v_cashback_amount = v_order_total * 0.05;
    
    -- تطبيق الحد الأقصى
    IF v_cashback_amount > 50.00 THEN
        SET v_cashback_amount = 50.00;
    END IF;
    
    -- 3. الحصول على المحفظة
    SELECT wallet_id INTO v_wallet_id
    FROM wallets
    WHERE customer_id = v_customer_id
    FOR UPDATE;
    
    -- 4. إنشاء معاملة Cashback
    INSERT INTO wallet_transactions (
        wallet_id,
        customer_id,
        type,
        amount,
        currency,
        source,
        reference_type,
        reference_id,
        status,
        balance_before,
        balance_after,
        reason_code,
        performed_by_type,
        transaction_date,
        expires_at
    )
    SELECT 
        v_wallet_id,
        v_customer_id,
        'credit',
        v_cashback_amount,
        'SAR',
        'cashback',
        'order',
        p_order_id,
        'posted',
        balance_available,
        balance_available + v_cashback_amount,
        'order_cashback_5pct',
        'system',
        NOW(),
        DATE_ADD(NOW(), INTERVAL 90 DAY)  -- صلاحية 90 يوم
    FROM wallets
    WHERE wallet_id = v_wallet_id;
    
    -- 5. تحديث الرصيد
    UPDATE wallets
    SET balance_available = balance_available + v_cashback_amount
    WHERE wallet_id = v_wallet_id;
    
    COMMIT;
END//
DELIMITER ;
```

---

## 8. التسوية المحاسبية | Accounting Reconciliation {#accounting-reconciliation}

### **تقرير التسوية اليومي | Daily Reconciliation Report**

```sql
-- تسوية يومية للمحفظة
SELECT 
    DATE(transaction_date) AS report_date,
    
    -- الإضافات
    SUM(CASE WHEN type IN ('credit', 'release') AND status = 'posted' 
             THEN amount ELSE 0 END) AS total_credits,
    
    -- الخصومات
    SUM(CASE WHEN type IN ('debit', 'hold_capture') AND status = 'posted' 
             THEN amount ELSE 0 END) AS total_debits,
    
    -- الصافي
    SUM(CASE 
            WHEN type IN ('credit', 'release') AND status = 'posted' THEN amount
            WHEN type IN ('debit', 'hold_capture') AND status = 'posted' THEN -amount
            ELSE 0
        END) AS net_change,
    
    -- عدد المعاملات
    COUNT(*) AS transaction_count
FROM wallet_transactions
WHERE DATE(transaction_date) = CURDATE() - INTERVAL 1 DAY
GROUP BY DATE(transaction_date);

-- التحقق من إجمالي الأرصدة
SELECT 
    SUM(balance_available) AS total_available,
    SUM(balance_on_hold) AS total_on_hold,
    SUM(balance_available + balance_on_hold) AS total_balance,
    COUNT(*) AS wallet_count
FROM wallets
WHERE status = 'active';
```

---

## 9. الحالات الحدية | Edge Cases {#edge-cases}

### **منع الرصيد السالب | Prevent Negative Balance**

```sql
-- استخدام FOR UPDATE + التحقق
START TRANSACTION;

SELECT balance_available INTO @balance
FROM wallets
WHERE customer_id = 123
FOR UPDATE;

IF @balance < @debit_amount THEN
    ROLLBACK;
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'رصيد غير كافٍ';
END IF;

-- ... تابع الخصم

COMMIT;
```

---

### **معاملات متزامنة | Concurrent Transactions**

```sql
-- استخدام قفل تفاؤلي Optimistic Locking
UPDATE wallets
SET balance_available = balance_available - 50.00,
    updated_at = NOW()
WHERE customer_id = 123
  AND balance_available >= 50.00  -- التحقق الذري
  AND updated_at = @last_known_updated_at;

-- إذا affected_rows = 0، كرر المحاولة
```

---

### **عكس المعاملة | Reverse Transaction**

```sql
-- عكس معاملة خاطئة
START TRANSACTION;

-- 1. الحصول على المعاملة الأصلية
SELECT * INTO @original
FROM wallet_transactions
WHERE transaction_id = 123
FOR UPDATE;

-- 2. إنشاء معاملة عكسية
INSERT INTO wallet_transactions (
    wallet_id,
    customer_id,
    type,
    amount,
    currency,
    source,
    reference_type,
    reference_id,
    status,
    balance_before,
    balance_after,
    reason_code,
    performed_by_type,
    transaction_date
) VALUES (
    @original.wallet_id,
    @original.customer_id,
    'reversal',
    @original.amount,
    @original.currency,
    @original.source,
    'reversal',
    @original.transaction_id,  -- مرجع للمعاملة الأصلية
    'posted',
    -- عكس balance_before/after
    @original.balance_after,
    @original.balance_before,
    'transaction_reversal',
    'staff',
    NOW()
);

-- 3. تحديث الرصيد
UPDATE wallets
SET balance_available = @original.balance_before
WHERE wallet_id = @original.wallet_id;

-- 4. وضع علامة على المعاملة الأصلية
UPDATE wallet_transactions
SET status = 'reversed'
WHERE transaction_id = 123;

COMMIT;
```

---

## 10. مؤشرات الأداء | KPIs {#kpis}

### **مؤشرات الاستخدام | Usage KPIs**

```sql
-- % الطلبات التي استخدمت المحفظة
SELECT 
    COUNT(DISTINCT CASE WHEN payment_method = 'wallet' 
                         OR payment_method = 'wallet_mixed' 
                        THEN order_id END) * 100.0 / COUNT(*) AS wallet_usage_pct
FROM orders
WHERE created_at >= CURDATE() - INTERVAL 30 DAY;

-- متوسط قيمة الرصيد المستخدم
SELECT 
    AVG(amount) AS avg_wallet_amount
FROM wallet_transactions
WHERE type = 'debit'
  AND source = 'purchase'
  AND created_at >= CURDATE() - INTERVAL 30 DAY;

-- معدل التكرار (العملاء الذين استخدموا المحفظة)
SELECT 
    CASE WHEN used_wallet THEN 'مع محفظة' ELSE 'بدون محفظة' END AS segment,
    AVG(order_count) AS avg_orders,
    COUNT(*) AS customer_count
FROM (
    SELECT 
        c.customer_id,
        EXISTS(
            SELECT 1 FROM wallet_transactions wt
            WHERE wt.customer_id = c.customer_id
              AND wt.source = 'purchase'
        ) AS used_wallet,
        COUNT(o.order_id) AS order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.created_at >= CURDATE() - INTERVAL 90 DAY
    GROUP BY c.customer_id
) subq
GROUP BY used_wallet;
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 07. النسخ الاحتياطي والاستعادة | Previous: Backup & Recovery](07_Backup_Recovery.md)

[التالي: 09. سياسة التحليلات | Next: Analytics Policy →](09_Analytics_Policy.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
