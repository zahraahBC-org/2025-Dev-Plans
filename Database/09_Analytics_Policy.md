# 09. سياسة التحليلات | Analytics Policy
## معمارية التحليلات وتتبع الأحداث | Analytics Architecture and Event Tracking

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد معمارية التحليلات وتتبع الأحداث  
**Purpose**: Define analytics architecture and event tracking

**الجمهور**: مهندسو البيانات، فريق التحليلات، مديرو المنتجات  
**Audience**: Data engineers, analytics team, product managers

**النطاق**: GA4، Firebase، BigQuery، تصنيف الأحداث  
**Scope**: GA4, Firebase, BigQuery, event taxonomy

---

## 🎯 **نظرة عامة | Overview**

تحدد سياسة التحليلات كيفية قياس وتحليل سلوك المستخدم عبر منصة **زهراء**. المبدأ الأساسي: **قاعدة البيانات هي مصدر الحقيقة المالي**، والتحليلات لقياس السلوك والقمع.

**المبادئ الأساسية**:
- **مصدر الحقيقة**: DB للإيرادات، التحليلات للسلوك
- **هوية موحدة**: user_id + user_pseudo_id
- **قاموس أحداث**: تصنيف موحد لجميع الأحداث
- **جودة البيانات**: تطابق الإيرادات بين DB والأحداث
- **الامتثال**: عدم إرسال PII في الأحداث

---

## 📑 **جدول المحتويات | Table of Contents**

1. [معمارية التحليلات | Analytics Architecture](#analytics-architecture)
2. [تصنيف الأحداث | Event Taxonomy](#event-taxonomy)
3. [تكامل BigQuery | BigQuery Integration](#bigquery-integration)
4. [نماذج الإسناد | Attribution Models](#attribution-models)
5. [تعيين هوية المستخدم | User Identity Mapping](#user-identity-mapping)
6. [إدارة الجلسات | Session Management](#session-management)
7. [جودة البيانات | Data Quality](#data-quality)
8. [الخصوصية والموافقة | Privacy & Consent](#privacy-consent)
9. [تعريفات KPI | KPI Definitions](#kpi-definitions)
10. [تسوية الإيرادات | Revenue Reconciliation](#revenue-reconciliation)

---

## 1. معمارية التحليلات | Analytics Architecture {#analytics-architecture}

### **نظرة عامة على البنية | Architecture Overview**

```
┌──────────────────────────────────────────────────────┐
│           Flutter App + Web                          │
│  Firebase SDK / GA4 SDK                              │
└────────────────┬─────────────────────────────────────┘
                 ↓ (أحداث Events)
┌──────────────────────────────────────────────────────┐
│           Firebase / GA4                             │
│  - جمع الأحداث                                       │
│  - معالجة أولية                                     │
└────────────────┬─────────────────────────────────────┘
                 ↓ (تصدير Export)
┌──────────────────────────────────────────────────────┐
│           BigQuery (Data Warehouse)                  │
│                                                      │
│  ┌────────────┐   ┌────────────┐   ┌─────────────┐ │
│  │ raw_events │ → │clean_events│ → │   marts_*   │ │
│  │            │   │ (dedup)    │   │  (reports)  │ │
│  └────────────┘   └────────────┘   └─────────────┘ │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  order_fact, user_identity_map, marketing_dim  │ │
│  │  (من MySQL عبر CDC/ELT)                        │ │
│  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

### **القرارات المعمارية | Architectural Decisions (ADR)**

1. **مصدر الحقيقة المالي** = قاعدة البيانات (order_fact، wallet_fact)
   - التحليلات لقياس السلوك والقمع
   - التقارير المالية من قاعدة البيانات

2. **هوية موحدة**: استخدام user_id + ربط user_pseudo_id المجهول
   - من مجهول (anonymous) إلى معروف (known) عند تسجيل الدخول

3. **قاموس الأحداث**: قائمة موحدة بالأحداث
   - لا أحداث خارج القائمة
   - حقول إلزامية لكل حدث

4. **Idempotency**: كل حدث يحمل event_id فريد (ULID)
   - إزالة التكرار في طبقة clean_*

5. **الطابع الزمني**: server_timestamp هو المرجع
   - client_timestamp للمعلومة فقط

6. **التقسيم**: حسب event_date
   - العنقدة حسب (event_name، user_pseudo_id)

7. **الامتثال**: عدم إرسال PII في الأحداث
   - معرّفات داخلية فقط

8. **الإسناد**: First Touch (90d) + Last Non-Direct (7d)

---

## 2. تصنيف الأحداث | Event Taxonomy {#event-taxonomy}

### **الأحداث الأساسية | Core Events**

#### **أحداث التطبيق | App Events**

| اسم الحدث Event Name | المحفز Trigger | الحقول الإلزامية Required Fields | الهوية Identity |
|---------------------|----------------|--------------------------------|----------------|
| `app_open` | فتح التطبيق | app_version، os، locale | user_pseudo_id |
| `screen_view` | عرض شاشة | screen_name، screen_class | user_pseudo_id |
| `view_item` | عرض منتج | sku_id، price، currency، category | user_pseudo_id |
| `view_item_list` | عرض قائمة منتجات | category_id، item_count | user_pseudo_id |
| `search` | بحث | search_term، result_count | user_pseudo_id |

---

#### **أحداث السلة | Cart Events**

| اسم الحدث | المحفز | الحقول الإلزامية | الهوية |
|-----------|--------|------------------|--------|
| `add_to_cart` | إضافة لسلة | sku_id، qty، price، currency | user_pseudo_id |
| `remove_from_cart` | إزالة من سلة | sku_id، qty | user_pseudo_id |
| `view_cart` | عرض السلة | cart_value، items_count | user_pseudo_id |

---

#### **أحداث الدفع | Checkout Events**

| اسم الحدث | المحفز | الحقول الإلزامية | الهوية |
|-----------|--------|------------------|--------|
| `begin_checkout` | بدء الدفع | cart_value، items_count، currency | user_id (مطلوب) |
| `add_shipping_info` | إضافة عنوان | shipping_tier | user_id |
| `add_payment_info` | اختيار طريقة دفع | payment_method | user_id |
| `purchase` | إتمام الطلب | order_id، value، currency، items[]، transaction_id | user_id (مطلوب) |

⚠️ **مهم**: أحداث الدفع تتطلب user_id (المستخدم مسجل الدخول).

---

#### **أحداث ما بعد الشراء | Post-Purchase Events**

| اسم الحدث | المحفز | الحقول الإلزامية | المصدر |
|-----------|--------|------------------|--------|
| `refund` | استرداد كامل/جزئي | order_id، value، currency | server-side |
| `rma_requested` | طلب إرجاع | order_id، rma_id، reason | server-side |
| `shipment_delivered` | تم التوصيل | order_id، shipment_id | server-side |
| `shipment_failed` | فشل التوصيل | order_id، shipment_id، reason | server-side |

---

### **معايير الأحداث | Event Standards**

**كل حدث يجب أن يتضمن**:
```json
{
  "event_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",  // ULID فريد
  "event_name": "purchase",
  "event_timestamp": 1704729600000000,  // microseconds
  "user_id": "123456",  // إذا مسجل دخول
  "user_pseudo_id": "ABC123...",  // دائماً
  "session_id": "session_123",
  "device_id": "device_456",
  "platform": "android",  // android, ios, web
  "app_version": "1.2.3",
  "params": {
    // معاملات خاصة بالحدث
  }
}
```

---

## 3. تكامل BigQuery | BigQuery Integration {#bigquery-integration}

### **مخطط البيانات | Data Schema**

#### **raw_events (الأحداث الخام)**

```sql
CREATE TABLE `project.dataset.raw_events_app` (
    event_id STRING NOT NULL,
    event_name STRING NOT NULL,
    
    -- الطوابع الزمنية
    client_timestamp TIMESTAMP,
    server_timestamp TIMESTAMP NOT NULL,
    event_date DATE NOT NULL,
    
    -- الهوية
    user_id STRING,  -- NULL إذا غير مسجل
    user_pseudo_id STRING NOT NULL,
    device_id STRING,
    session_id STRING,
    
    -- السياق
    platform STRING,  -- android, ios, web
    app_version STRING,
    os_version STRING,
    locale STRING,
    
    -- المعاملات (JSON)
    params JSON,
    
    -- البيانات الوصفية
    source STRING DEFAULT 'app',
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY event_date
CLUSTER BY event_name, user_pseudo_id;
```

---

#### **clean_events (الأحداث النظيفة)**

```sql
CREATE TABLE `project.dataset.clean_events` (
    -- جميع حقول raw_events
    -- بالإضافة إلى:
    
    is_duplicate BOOLEAN,  -- حدث مكرر
    is_bot BOOLEAN,        -- روبوت/زاحف
    schema_valid BOOLEAN,  -- يتطابق مع المخطط المتوقع
    
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY event_date
CLUSTER BY event_name, user_pseudo_id;
```

**معالجة التنظيف**:
```sql
-- إزالة التكرار
INSERT INTO clean_events
SELECT DISTINCT ON (event_id) *,
    FALSE AS is_duplicate,
    FALSE AS is_bot,
    TRUE AS schema_valid,
    CURRENT_TIMESTAMP() AS processed_at
FROM raw_events
WHERE event_date = CURRENT_DATE() - 1;
```

---

#### **user_identity_map (خريطة الهوية)**

```sql
CREATE TABLE `project.dataset.user_identity_map` (
    user_pseudo_id STRING NOT NULL,  -- من Firebase
    user_id STRING NOT NULL,          -- من قاعدة البيانات
    
    first_seen_timestamp TIMESTAMP NOT NULL,
    last_seen_timestamp TIMESTAMP NOT NULL,
    
    link_reason STRING,  -- login, purchase, sdk_call
    link_source STRING,  -- app, web, server
    
    PRIMARY KEY (user_pseudo_id, user_id) NOT ENFORCED
);
```

**الاستخدام**:
```sql
-- ربط الأحداث المجهولة بالمستخدم المعروف
SELECT 
    e.event_name,
    COALESCE(e.user_id, m.user_id) AS resolved_user_id,
    e.user_pseudo_id,
    e.event_timestamp
FROM clean_events e
LEFT JOIN user_identity_map m ON e.user_pseudo_id = m.user_pseudo_id
WHERE e.event_date = CURRENT_DATE();
```

---

## 4. نماذج الإسناد | Attribution Models {#attribution-models}

### **إسناد اللمسة الأولى | First-Touch Attribution**

**النافذة**: 90 يومًا  
**القاعدة**: أول تفاعل تسويقي للمستخدم

```sql
-- حساب اللمسة الأولى
WITH first_touch AS (
    SELECT 
        user_id,
        utm_source,
        utm_medium,
        utm_campaign,
        utm_content,
        utm_term,
        MIN(event_timestamp) AS first_touch_ts
    FROM clean_events
    WHERE user_id IS NOT NULL
      AND utm_source IS NOT NULL
      AND utm_source != 'direct'
    GROUP BY user_id, utm_source, utm_medium, utm_campaign, utm_content, utm_term
)
SELECT * FROM first_touch;
```

---

### **إسناد اللمسة الأخيرة | Last-Touch Attribution**

**النافذة**: 7 أيام  
**القاعدة**: آخر تفاعل تسويقي قبل الشراء (استثناء: direct)

```sql
-- حساب اللمسة الأخيرة
WITH purchases AS (
    SELECT 
        user_id,
        CAST(params.value.string_value AS INT64) AS order_id,
        event_timestamp AS purchase_ts
    FROM clean_events,
    UNNEST(params) AS params
    WHERE event_name = 'purchase'
      AND params.key = 'order_id'
),
last_touch AS (
    SELECT 
        p.user_id,
        p.order_id,
        e.utm_source,
        e.utm_medium,
        e.utm_campaign,
        MAX(e.event_timestamp) AS last_touch_ts
    FROM purchases p
    JOIN clean_events e 
        ON p.user_id = e.user_id
        AND e.event_timestamp < p.purchase_ts
        AND e.event_timestamp >= TIMESTAMP_SUB(p.purchase_ts, INTERVAL 7 DAY)
        AND e.utm_source IS NOT NULL
        AND e.utm_source != 'direct'
    GROUP BY p.user_id, p.order_id, e.utm_source, e.utm_medium, e.utm_campaign
)
SELECT * FROM last_touch;
```

---

### **تطبيع UTM | UTM Normalization**

```sql
-- تطبيع قيم UTM
CREATE OR REPLACE FUNCTION normalize_utm_medium(medium STRING)
RETURNS STRING AS (
    CASE LOWER(TRIM(medium))
        WHEN 'cpc' THEN 'cpc'
        WHEN 'ppc' THEN 'cpc'
        WHEN 'paidsearch' THEN 'cpc'
        WHEN 'social' THEN 'social'
        WHEN 'socialmedia' THEN 'social'
        WHEN 'email' THEN 'email'
        WHEN 'newsletter' THEN 'email'
        WHEN 'affiliate' THEN 'affiliate'
        WHEN 'display' THEN 'display'
        WHEN 'banner' THEN 'display'
        WHEN 'organic' THEN 'organic'
        WHEN 'direct' THEN 'direct'
        WHEN '(none)' THEN 'direct'
        ELSE 'other'
    END
);
```

---

## 5. تعيين هوية المستخدم | User Identity Mapping {#user-identity-mapping}

### **ربط المجهول بالمعروف | Link Anonymous to Known**

```sql
-- عند تسجيل الدخول
INSERT INTO user_identity_map (
    user_pseudo_id,
    user_id,
    first_seen_timestamp,
    last_seen_timestamp,
    link_reason,
    link_source
) VALUES (
    'ABC123XYZ',  -- من Firebase SDK
    '123456',     -- من قاعدة البيانات
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP(),
    'login',
    'app'
)
ON DUPLICATE KEY UPDATE
    last_seen_timestamp = CURRENT_TIMESTAMP();
```

---

### **في Flutter App**

```dart
// عند تسجيل الدخول
Future<void> onUserLogin(String userId) async {
  // تعيين user_id في Firebase Analytics
  await FirebaseAnalytics.instance.setUserId(id: userId);
  
  // تسجيل حدث تسجيل الدخول
  await FirebaseAnalytics.instance.logEvent(
    name: 'login',
    parameters: {
      'method': 'phone',  // phone, google, apple
      'user_id': userId,
    },
  );
}

// عند تسجيل الخروج
Future<void> onUserLogout() async {
  // إزالة user_id
  await FirebaseAnalytics.instance.setUserId(id: null);
  
  // إعادة تعيين بيانات التحليلات
  await FirebaseAnalytics.instance.resetAnalyticsData();
}
```

---

## 6. إدارة الجلسات | Session Management {#session-management}

### **تعريف الجلسة | Session Definition**

**قواعد Sessionization**:
- جلسة جديدة: أول حدث في اليوم، أو بعد 30 دقيقة عدم نشاط
- الجلسة تنتهي: بعد 30 دقيقة عدم نشاط، أو عند منتصف الليل

```sql
-- بناء جلسات من الأحداث
CREATE TABLE sessions AS
WITH events_with_gaps AS (
    SELECT 
        user_pseudo_id,
        user_id,
        event_name,
        event_timestamp,
        
        -- حساب الفجوة من الحدث السابق
        TIMESTAMP_DIFF(
            event_timestamp,
            LAG(event_timestamp) OVER (
                PARTITION BY user_pseudo_id 
                ORDER BY event_timestamp
            ),
            MINUTE
        ) AS gap_minutes
    FROM clean_events
    WHERE event_date = CURRENT_DATE() - 1
),
session_starts AS (
    SELECT 
        user_pseudo_id,
        user_id,
        event_timestamp AS session_start,
        
        -- جلسة جديدة إذا:
        -- 1. أول حدث للمستخدم
        -- 2. فجوة > 30 دقيقة
        SUM(
            CASE WHEN gap_minutes IS NULL OR gap_minutes > 30 
                 THEN 1 
                 ELSE 0 
            END
        ) OVER (
            PARTITION BY user_pseudo_id 
            ORDER BY event_timestamp
        ) AS session_number
    FROM events_with_gaps
)
SELECT 
    CONCAT(user_pseudo_id, '_', session_number) AS session_id,
    user_pseudo_id,
    user_id,
    MIN(session_start) AS start_timestamp,
    MAX(session_start) AS end_timestamp,
    TIMESTAMP_DIFF(MAX(session_start), MIN(session_start), MINUTE) AS duration_minutes,
    COUNT(*) AS event_count
FROM session_starts
GROUP BY session_id, user_pseudo_id, user_id, session_number;
```

---

## 7. جودة البيانات | Data Quality {#data-quality}

### **الاختبارات اليومية | Daily Tests**

#### **1. مطابقة المخطط | Schema Conformance**

```sql
-- التحقق من جميع الأحداث تتطابق مع المخطط
SELECT 
    event_name,
    COUNT(*) AS invalid_count
FROM clean_events
WHERE event_date = CURRENT_DATE() - 1
  AND schema_valid = FALSE
GROUP BY event_name
HAVING COUNT(*) > 0;
```

---

#### **2. شذوذ الحجم | Volume Anomaly**

```sql
-- مقارنة بمتوسط 7 أيام
WITH daily_counts AS (
    SELECT 
        event_date,
        event_name,
        COUNT(*) AS event_count
    FROM clean_events
    WHERE event_date >= CURRENT_DATE() - 8
    GROUP BY event_date, event_name
),
averages AS (
    SELECT 
        event_name,
        AVG(event_count) AS avg_count,
        STDDEV(event_count) AS stddev_count
    FROM daily_counts
    WHERE event_date < CURRENT_DATE() - 1
    GROUP BY event_name
)
SELECT 
    d.event_name,
    d.event_count AS today_count,
    a.avg_count AS avg_7day,
    (d.event_count - a.avg_count) / a.avg_count * 100 AS pct_change
FROM daily_counts d
JOIN averages a ON d.event_name = a.event_name
WHERE d.event_date = CURRENT_DATE() - 1
  AND ABS((d.event_count - a.avg_count) / a.avg_count) > 0.20  -- تغيير > 20%
ORDER BY ABS(pct_change) DESC;
```

---

#### **3. معدلات الربط | Join Rates**

```sql
-- معدل ربط view_item مع product_dim
SELECT 
    COUNT(DISTINCT e.event_id) AS total_view_items,
    COUNT(DISTINCT CASE WHEN p.variant_id IS NOT NULL 
                        THEN e.event_id END) AS matched_items,
    COUNT(DISTINCT CASE WHEN p.variant_id IS NOT NULL 
                        THEN e.event_id END) * 100.0 / 
    COUNT(DISTINCT e.event_id) AS match_rate
FROM clean_events e
LEFT JOIN product_variants p 
    ON CAST(JSON_EXTRACT_SCALAR(e.params, '$.sku_id') AS INT64) = p.variant_id
WHERE e.event_name = 'view_item'
  AND e.event_date = CURRENT_DATE() - 1;

-- الهدف: match_rate ≥ 99%
```

---

#### **4. نسبة التكرار | Deduplication Ratio**

```sql
-- نسبة الأحداث المكررة
SELECT 
    COUNT(*) AS total_events,
    SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END) AS duplicate_count,
    SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS duplicate_pct
FROM clean_events
WHERE event_date = CURRENT_DATE() - 1;

-- الهدف: duplicate_pct < 1%
```

---

#### **5. فرق الإيرادات | Revenue Delta**

```sql
-- مقارنة إيرادات الأحداث مع قاعدة البيانات
WITH event_revenue AS (
    SELECT 
        SUM(CAST(JSON_EXTRACT_SCALAR(params, '$.value') AS FLOAT64)) AS revenue
    FROM clean_events
    WHERE event_name = 'purchase'
      AND event_date = CURRENT_DATE() - 1
),
db_revenue AS (
    SELECT 
        SUM(total) AS revenue
    FROM orders
    WHERE DATE(created_at) = CURRENT_DATE() - 1
)
SELECT 
    e.revenue AS event_revenue,
    d.revenue AS db_revenue,
    ABS(e.revenue - d.revenue) / d.revenue * 100 AS delta_pct
FROM event_revenue e, db_revenue d;

-- الهدف: delta_pct ≤ 3%
```

---

## 9. تعريفات KPI | KPI Definitions {#kpi-definitions}

### **مستخدمون نشطون | Active Users**

```sql
-- DAU (مستخدمون نشطون يومياً)
SELECT 
    event_date,
    COUNT(DISTINCT user_pseudo_id) AS dau
FROM clean_events
WHERE event_date >= CURRENT_DATE() - 30
GROUP BY event_date;

-- WAU (مستخدمون نشطون أسبوعياً)
SELECT 
    DATE_TRUNC(event_date, WEEK(MONDAY)) AS week,
    COUNT(DISTINCT user_pseudo_id) AS wau
FROM clean_events
WHERE event_date >= CURRENT_DATE() - 90
GROUP BY week;

-- MAU (مستخدمون نشطون شهرياً)
SELECT 
    DATE_TRUNC(event_date, MONTH) AS month,
    COUNT(DISTINCT user_pseudo_id) AS mau
FROM clean_events
WHERE event_date >= CURRENT_DATE() - 365
GROUP BY month;
```

---

### **معدل التحويل CVR | Conversion Rate**

```sql
-- CVR لكل خطوة في القمع
WITH funnel_steps AS (
    SELECT 
        COUNT(DISTINCT CASE WHEN event_name = 'view_item' 
                            THEN user_pseudo_id END) AS step1_view,
        COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' 
                            THEN user_pseudo_id END) AS step2_cart,
        COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' 
                            THEN user_pseudo_id END) AS step3_checkout,
        COUNT(DISTINCT CASE WHEN event_name = 'add_payment_info' 
                            THEN user_pseudo_id END) AS step4_payment,
        COUNT(DISTINCT CASE WHEN event_name = 'purchase' 
                            THEN user_pseudo_id END) AS step5_purchase
    FROM clean_events
    WHERE event_date = CURRENT_DATE() - 1
)
SELECT 
    step1_view,
    step2_cart,
    step2_cart * 100.0 / step1_view AS cvr_view_to_cart,
    step3_checkout * 100.0 / step2_cart AS cvr_cart_to_checkout,
    step4_payment * 100.0 / step3_checkout AS cvr_checkout_to_payment,
    step5_purchase * 100.0 / step4_payment AS cvr_payment_to_purchase,
    step5_purchase * 100.0 / step1_view AS cvr_overall
FROM funnel_steps;
```

---

### **متوسط قيمة الطلب AOV | Average Order Value**

```sql
-- AOV من الأحداث
SELECT 
    event_date,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' 
                        THEN user_pseudo_id END) AS purchasers,
    SUM(CAST(JSON_EXTRACT_SCALAR(params, '$.value') AS FLOAT64)) / 
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' 
                        THEN user_pseudo_id END) AS aov
FROM clean_events
WHERE event_name = 'purchase'
  AND event_date >= CURRENT_DATE() - 30
GROUP BY event_date;
```

---

## 10. تسوية الإيرادات | Revenue Reconciliation {#revenue-reconciliation}

### **تقرير المطابقة اليومي | Daily Reconciliation Report**

```sql
-- مقارنة الإيرادات: أحداث مقابل قاعدة البيانات
WITH event_revenue AS (
    SELECT 
        event_date,
        SUM(CAST(JSON_EXTRACT_SCALAR(params, '$.value') AS FLOAT64)) AS revenue,
        COUNT(DISTINCT JSON_EXTRACT_SCALAR(params, '$.order_id')) AS order_count
    FROM clean_events
    WHERE event_name = 'purchase'
      AND event_date >= CURRENT_DATE() - 30
    GROUP BY event_date
),
db_revenue AS (
    SELECT 
        DATE(created_at) AS order_date,
        SUM(total) AS revenue,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    WHERE created_at >= CURRENT_DATE() - 30
    GROUP BY order_date
)
SELECT 
    COALESCE(e.event_date, d.order_date) AS date,
    e.revenue AS event_revenue,
    d.revenue AS db_revenue,
    e.order_count AS event_orders,
    d.order_count AS db_orders,
    
    -- الفروقات
    d.revenue - e.revenue AS revenue_diff,
    ABS(d.revenue - e.revenue) / d.revenue * 100 AS revenue_delta_pct,
    d.order_count - e.order_count AS order_diff
FROM event_revenue e
FULL OUTER JOIN db_revenue d ON e.event_date = d.order_date
ORDER BY date DESC;
```

**أسباب الفروقات المقبولة**:
- الضرائب والرسوم (قد تُحسب بشكل مختلف)
- التوقيت (الأحداث قد تتأخر دقائق)
- الاستردادات (تظهر كـ refund منفصل)

**عتبة التنبيه**: delta_pct > 3%

---

## 🔗 **التنقل | Navigation**

[← السابق: 08. نظام المحفظة | Previous: Wallet System](08_Wallet_System.md)

[التالي: 10. قائمة أفضل الممارسات | Next: Best Practices Checklist →](10_Best_Practices.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
