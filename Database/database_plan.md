data 
1. Customer Master Data
●	Identifiers: customer_id (internal), phone (E.164), email, social_id, device_id
●	Profile: name, gender, birth year/age, city, country, preferred language & currency
●	Acquisition: First Source / Last Source (UTM: source, medium, campaign, term, content)
●	Behavior: registration date, last activity, sessions, devices used
●	Segments: VIP, Active, Inactive, Cart Abandoner, COD High-Risk, New
●	Properties: interests, AOV (average order value), LTV, risk score
●	Privacy: communication consents (SMS, Email, Push, WhatsApp)
 
2. Product & Catalog Data
●	Product Level: product_id, name, description, brand, category/subcategory
●	Variant Level: variant_id, SKU, color, size, material, images, videos
●	Pricing: base price, discounted price, currency, validity dates
●	Inventory: current stock, minimum stock, stock_on_hand, available_to_promise (from ledger)
●	Attributes: SEO keywords, badges (new, best-seller), seasonality tags
●	Analytics: product views, add-to-cart, conversion rate
 
3. Orders
●	Header: order_id, customer_id, created_at, status (Created → Delivered/Returned/Cancelled)
●	Items: order_item_id, variant_id, price, qty, discount, tax
●	Payment: method (COD, Online, Wallet), status (Authorized, Captured, Refunded)
●	Shipping: carrier, tracking number, fee, SLA, status (Shipped, Out for Delivery, Delivered, RTO)
●	Marketing: UTM source/medium/campaign at order level
●	Geo: shipping address, city, region, zip code
●	Timestamps: created, paid, shipped, delivered, cancelled
 
4. Payments
●	Core: payment_id, order_id, method, amount, currency
●	Status: Authorized, Captured, Settled, Refunded, Failed
●	Attempts: log of retries & errors
●	COD Settlement: collected amount, courier, settlement date, bank transfer status
●	Risk Profile: allowed_state (Allowed/Temporarily Blocked), failed_cod_attempts, risk_score
 
5. Shipments
●	Identifiers: shipment_id, order_id
●	Carrier, service type (Standard, Express, Same-Day)
●	Tracking number (AWB)
●	Actual weight, chargeable weight
●	Status: Created, Picked Up, In Transit, Out for Delivery, Delivered, RTO, Failed
●	Delivery attempts (with reason: wrong address, refused, not available)
●	Timestamps: created, picked, first attempt, delivered, RTO
 
6. Returns / RMA
●	Core: rma_id, order_id, order_item_id, customer_id
●	Type: Return, Replace, Refund
●	Reason Codes: defective, wrong size, not satisfied…
●	Resolution: Approved/Rejected/Pending
●	Refund method: cash, wallet, voucher
●	Timestamps: opened, received, inspected, closed
 
7. Wallet & Promotions
●	Wallet: wallet_id, customer_id, balance, credits, debits, holds
●	Sources: RMA refunds, cashback, gift cards, promo codes
●	Coupons: code, type (percentage/fixed), min order value, validity dates, usage count
●	Loyalty Program: points balance, tier (silver/gold/vip)
 
8. Marketing & Analytics
●	GA4/Firebase Events: app_open, view_item, add_to_cart, begin_checkout, purchase
●	Attribution: first_source, last_source, medium, campaign, term, content
●	Cohorts: weekly/monthly (first registration or first purchase)
●	Retention: W1/W4, M1/M3 (activity & purchase retention)
●	Funnel: Visit → Product View → Add to Cart → Checkout → Purchase
●	Cart Abandonment: abandonment rate, recovery rate
●	Reactivation: inactive customers reactivated after campaigns
 
9. Operations KPIs
●	Inventory: turnover ratio, days of supply, out-of-stock %
●	Shipping: SLA adherence %, success rate, RTO %, avg delivery time
●	Payments: COD fail rate, online payment success %, avg refund processing time
●	Customers: CAC, LTV, repeat rate, reactivation rate
●	Marketing: ROAS, CPA, first vs last touch impact
 
10. Advanced Data
●	Logs: app usage, errors, crashes
●	Monitoring: latency, API calls, DB queries
●	Security: audit logs (who changed what, when)
●	Governance: data retention policies (how long to keep, archive, delete)
 
Summary
A strong company must capture full-spectrum data:
1.	Customer Master Data (identity, acquisition, segments).
2.	Product & Inventory (catalog + ledger).
3.	Orders & Payments (transactions + risk).
4.	Shipments & Returns (logistics).
5.	Wallet & Promotions (loyalty).
6.	Marketing & Analytics (attribution, GA4, cohorts, retention).
7.	Operational KPIs (CAC, LTV, ROAS, RTO, SLA).
8.	Advanced/Compliance (logs, security, retention).
 
بنية قاعدة البيانات (MySQL 8 + phpMyAdmin) 
بنية قاعدة البيانات (MySQL 8 + phpMyAdmin)
نطاق العمل: العملاء، الكتالوج، المنتجات/النسخ، المخزون (Ledger)، السلال، الطلبات/المدفوعات/الشحن/المرتجعات، المحفظة والعروض، التحليلات، الحوكمة والأمان.
1) معمارية الطبقات (ERD عالي المستوى)
●	هوية ومرجعية: customers, addresses, devices, consents, segments, brands, categories (هرمية), attributes/media.
●	معاملات: carts/cart_items, orders/order_items, payments/payment_attempts/refunds, shipments/tracking, rmas, promotions/discounts, wallet.
●	المخزون: inventory_ledger (المرجع الوحيد للحركة) + stock_snapshot اختياري للتسريع.
●	تحليلات: events_raw (اختياري), facts/dims (orders, order_items, rma, inventory_movements).
مهم: تفعيل Ledger للمخزون (لا تعديل مباشر للكميات) وربط كل تغيير بسبب واضح (purchase_receipt, reservation, shipment_captured, rto_received, …).
2) قواعد تصميم إلزامية
●	معرّفات لا تُخمن: UUID (CHAR(36)) أو BINARY(16)؛ مفاتيح بديلة للأرقام المتسلسلة إن لزم.
●	Soft delete: عمود archived_at بدل الحذف الفعلي + فهارس تراعيه.
●	أعمدة تدقيق موحّدة: created_at, updated_at, created_by, updated_by.
●	UTC دائماً في الحفظ؛ التحويل للمنطقة الزمنية يتم بالتطبيق/التقارير.
●	عدم تكرار الحقيقة: لقطات تُؤخذ وقت الحدث (مثلاً سعر الشراء داخل order_items).
3) التسمية والأنواع
●	أسلوب التسمية: snake_case, أسماء واضحة غير عامة.
●	النصوص: VARCHAR بـ utf8mb4_unicode_ci.
●	الأموال: DECIMAL(12,2) (عملة تُخزَّن في عمود مستقل).
●	التواريخ: DATETIME(3) مع دقة ملي ثانية إن احتجت تتبّعاً أدق.
●	الحالات/الأكواد: ENUM أو جداول مرجعية Domain (مثال: order_status, payment_state).
4) القيود والعلاقات (سلامة البيانات)
●	FK إلزامية لمنع السجلات اليتيمة (سياسات واضحة ON DELETE/UPDATE).
●	UNIQUE: مثل sku على مستوى النسخة، وphone_e164 على العملاء.
●	CHECK: السعر ≥ 0، الكمية ≥ 0، صيغة الهاتف E.164، مجموعة عملات مسموحة.
●	Idempotency keys لعمليات الدفع/التكرار.

5) الفهارس والأداء (ميزانيات زمنية)
●	قوائم المنتجات: فهرس مركّب مثل (category_id, publish_status, is_visible, created_at) + فهرس على priceللفرز.
●	البحث/الفلاتر: brand_id, (color, size), is_on_sale, is_best_seller.
●	السلال/الطلبات: (customer_id, last_activity_at) للسلال؛ (status, created_at) و(customer_id, created_at) للطلبات؛ order_no.
●	الشحن/المدفوعات/RMA: tracking_no، (order_id)، حالات/مزود.
●	Partial/Covering indexes للاستعلامات الثقيلة عند الحاجة.
●	أهداف أداء مبدئية:
○	قائمة منتجات مفلترة ≤ 300ms على 50K variants
○	إنشاء طلب (confirm→packed) ≤ 2s
○	حدث تتبّع شحنة جديد يظهر ≤ 1 دقيقة من الـ webhook
6) الترحيلات (Migrations) والبيئات
●	كل تغيير عبر Migration قابل للتراجع (لا تعديل يدوي على الإنتاج).
●	مصادقة مراجعة (PR) + تفقد خطة التنفيذ (EXPLAIN) قبل الدمج.
●	بيئات منفصلة: dev/stage/prod وقواعد بيانات منفصلة + بيانات Seed للاختبار.
●	توسيم المخطط: ملف /docs/db.md يشرح التطوير/الاختبار/الاستعادة.
7) الأمان والخصوصية وRBAC
●	Least Privilege: أدوار (Admin, Ops, CS, Finance, Marketing, DevReadOnly) مع Grants دقيقة.
●	PII Masking: هواتف/عناوين تُعرض مقنّعة للأدوار غير المصرّح لها (عبر Views).
●	تشفير: At-rest + In-transit (TLS)، والحساس جداً يمكن تشفيره عمودياً (AES) إن لزم.
●	Audit Logs: عمليات حساسة (مدفوعات، ردّيات، تغيير حالات) سجلّ إضافي append-only.
●	إدارة الأسرار: خارج الكود (بيئة/Secret Manager).
8) النسخ الاحتياطي والتعافي
●	RPO ≤ 15 دقيقة (WAL/Replication)، RTO ≤ 60 دقيقة (بيئة DR دافئة/باردة).
●	اختبار استعادة ربع سنوي مع تقرير نجاح (checksums, counts) وتوثيق كامل.
9) المراقبة والتشغيل
●	لوحات تشغيل: زمن الاستعلامات، أخطاء القيود، أحجام الجداول، بطء/Locks.
●	تنبيهات: ارتفاع 5xx/4xx، بطء ملحوظ، فشل نسخ احتياطي.
●	Runbooks: تباطؤ، قفل جداول، تعارضات، فشل مزوّد دفع/شحن.
10) سياسة استخدام phpMyAdmin
●	إنتاج: قراءة فقط للأدوار غير الإدارية؛ ممنوع أي DDL/DML يدوي—الترحيلات فقط.
●	Stage/Dev: مسموح للمهندسين مع تسجيل Audit للحركات.
●	حماية: وصول خلف VPN/IP allowlist + 2FA لحسابات الإدارة.
●	نظافة البيانات: العمليات الدُفعية/التنظيف تُنفّذ عبر Scripts مُراجعة وليس استعلامات يدوية.
●	الاستعلامات الثقيلة: تُستقصى عبر EXPLAIN وخارج ساعات الذروة.
11) متطلبات وحدات أساسية (اختصار تنفيذي)
●	Customers/Devices/Consents/Segments: هاتف فريد E.164 + OTP، ربط الأجهزة وتوكن الإشعارات، موافقات قنوات دقيقة، عضوية شرائح قابلة للتدقيق.
●	Catalog/Variants/Media/Attributes: قواميس موحّدة للألوان/المقاسات/الخامات قبل أي استيراد كبير.
●	Inventory (Ledger): كل حركة بسبب/مرجع، Job لحساب stock_on_hand وavailable_to_promise لكل نسخة/مخزن.
●	Orders/Payments/Shipments/RMA/Wallet/Promotions: لقطات القيم وقت الحدث، ربط ردّيات الدفع، سياسات RMA واضحة، خصومات مستوى البند/الطلب.
●	Attribution (First/Last): حفظ أول وآخر مصدر على المستخدم والطلب لدقة التقارير خارج GA4.
12) قائمة قبول (Definition of Done)
1.	سلامة المخطط: لا سجلات يتيمة؛ FK/UNIQUE/CHECK مُفعّلة؛ بيانات Seed تمرّ.
2.	3NF كحد أدنى؛ أي إلغاء تطبيع مبرّر ومُوثّق.
3.	فهارس أساسية موجودة وخطط تنفيذ مقبولة للاستعلامات الحرجة.
4.	أداء يحقق الميزانيات المذكورة (قائمة/إنشاء طلب/تتبّع).
5.	أمان/خصوصية: RBAC + Masking + Audit تعمل كما هو متوقّع.
6.	النسخ/الاستعادة: تجربة ناجحة موثّقة مع RPO/RTO.
7.	الترحيلات: كل تغيير عبر Migration مع Rollback مجرَّب.
8.	التوثيق: /docs/db.md محدث ويُمكّن أي مهندس من التشغيل بلا أسئلة.
13) التسليمات المطلوبة
●	ERD مفصّل (صورة + ملف قابل للتعديل) على الطبقات أعلاه.
●	قاموس بيانات + Matrix قيود لكل جدول/حقل.
●	خطة فهارس مبنية على الاستعلامات الفعلية + أمثلة EXPLAIN.
●	سياسة النسخ/الاستعادة بأرقام RPO/RTO وجدولة اختبارات.
●	RBAC/PII/Audit (مصفوفة أذونات + Views مقنّعة).
●	تصميم Ledger المخزون (جداول/أسباب/قواعد الحسبة).
●	سيناريوهات RMA مكتملة وربطها ماليًا ومخزنيًا.
●	/docs/db.md (تشغيل محلي، ترحيلات، اختبارات، استعادة، أفضل الممارسات).
 
مراجعات 
مراجعات
1) الإصدار والإعدادات الأساسية
●	المحرك: InnoDB فقط.
●	الإصدار الموصى به: MySQL 8.x (أو MariaDB ≥ 10.6).
●	SQL Mode: فعّل STRICT_TRANS_TABLES, وامنَع القيم الضمنية غير الصحيحة.
●	المنطقة الزمنية: اضبط الخادم والتطبيق على UTC وخزّن الوقت بUTC، واعرض للمستخدم +03 عند الحاجة.
●	ملف لكل جدول: innodb_file_per_table=ON.
●	Binary Log: فعّله لنسخ احتياطي تفاضلي واسترجاع النقطة الزمنية.
2) الترميز والترتيب (Collation)
●	الترميز: utf8mb4 للجداول وكافة الأعمدة النصية.
●	الترتيب: MySQL 8: استخدم utf8mb4_0900_ai_ci. (إن كان الإصدار أقدم، استخدم utf8mb4_general_ci).
3) أسلوب التسمية والبنية
●	أسماء الجداول: مفردة وsnake_case (مثال: customer, order_item).
●	عدم استخدام بادئات عشوائية مثل tbl_.
●	أعمدة قياسية: id, created_at, updated_at, deleted_at (للـsoft delete عند الحاجة).
4) المفاتيح والمعرّفات
●	Primary Key: BIGINT UNSIGNED AUTO_INCREMENT أو UUIDv7/ULID مخزّن في BINARY(16) للأنظمة الموزعة.
●	العلاقات (FK): استخدم قيودًا صريحة مع قواعد ON UPDATE/DELETE واضحة (غالبًا RESTRICT أو CASCADE عند الجداول الرابط).
●	Unique Constraints: للبريد الإلكتروني، الكوبونات، الأكواد الفريدة.
5) الفهارس (Indexes)
●	قاعدة عامة: فهرس لكل مفتاح خارجي، ولكل عمود يُستعلم عنه في WHERE/ORDER BY بشكل متكرر.
●	المركّبة: احرص على ترتيب الأعمدة حسب الانتقائية والاستخدام ((customer_id, created_at) مثلًا).
●	لا تفرط بالفهارس؛ كل فهرس يُكلف كتابة/تحديثات أبطأ.
6) أنواع البيانات القياسية
●	المال: DECIMAL(12,2)، لا تستخدم FLOAT.
●	الحالات: استخدم TINYINT مع جدول مرجعي أو ENUM محدودة جدًا.
●	JSON: مسموح لـ meta الصغيرة، لكن لا تجعله يحل محل التصميم العلائقي.


7) الأمان والوصول
●	حسابات منفصلة: مستخدم للقراءة/الكتابة للتطبيق، وآخر للقراءة فقط للتحليلات—لا تستخدم root.
●	أقل صلاحيات ممكنة (Least Privilege) عبر GRANT محدد على المخطط.
●	TLS للاتصال بين التطبيق وقاعدة البيانات إن كانت عبر شبكة غير محمية.
●	تقييد IP والوصول للوحة phpMyAdmin عبر VPN أو allowlist.
●	تدقيق: فعّل سجل الاستعلامات البطيئة وراقب الأنماط.
8) الأداء والمراقبة
●	Buffer Pool: اضبط innodb_buffer_pool_size (حتى 60–70% من RAM على خادم مخصص).
●	Slow Query Log: فعّله وحسّن كل استعلام يتجاوز 200–500ms.
●	EXPLAIN/ANALYZE: استخدمها قبل اعتماد أي استعلام ثقيل.
●	التقسيم (Partitioning): فقط للجداول الضخمة (مثل أحداث التحليلات شهريًا).
●	الترقيم: فضّل Keyset Pagination على OFFSET الكبير.
9) النسخ الاحتياطي والاسترجاع
●	خطة عملية:
○	نسخ كامل يومي + تفاضلي عبر binlog كل 15–30 دقيقة.
○	اختبارات استرجاع شهرية (لا تعتبر النسخ صحيحة حتى تُختبَر).
●	أدوات: للمشاريع المتوسطة استخدم mysqldump (مع إغلاق كتابة أو قفل منطقي)، وللضخمة Percona XtraBackup.
●	تخزين خارجي مُشفّر + احتفاظ بإصدارات 7/14/30 يومًا.
10) سياسة التغييرات (Migrations)
●	ممنوع تعديل المخطط يدويًا من phpMyAdmin في بيئة الإنتاج.
●	اعتمد أدوات ترحيل Schema (Flyway/Liquibase أو سكربتات SQL مُرقّمة في مستودع الـAPI) مع مراجعة كود ونسخة احتياطية قبل التنفيذ.
●	بيئات منفصلة: dev / staging / prod مع بيانات اختبار (لا بيانات عملاء حقيقية).

تشغيل يومي عبر phpMyAdmin (بدون مخاطرة)
●	صلاحيات المستخدمين: تأكد أن حساب phpMyAdmin اليومي قراءة فقط في الإنتاج، وأن التغييرات الهيكلية تتم عبر الـmigrations.
●	قوالب استعلامات آمنة: أنشئ مجلد “Saved Queries” للاستعلامات التقارير الشائعة (قراءة فقط).
●	مراجعة الاستعلامات البطيئة أسبوعيًا وتحويل التحسينات إلى تذاكر تقنية.







التحسين السريع
١) إصدار وإعدادات الخادم
●	استخدموا MySQL 8.x (InnoDB فقط) + utf8mb4 افتراضيًا.
●	فعّلوا sql_mode: STRICT_TRANS_TABLES, NO_ZERO_DATE, NO_ZERO_IN_DATE, ERROR_FOR_DIVISION_BY_ZERO.
●	Binlog: ROW + sync_binlog=1 + innodb_flush_log_at_trx_commit=1 لسلامة البيانات.
●	سجّلوا الاستعلامات البطيئة slow_query_log=ON, long_query_time=0.2 لمراقبة الأداء.
٢) الأمن والحوكمة
●	phpMyAdmin خلف VPN/IP allowlist، إيقاف الوصول العام، وتعطيل الدخول بـ root عن بعد.
●	RBAC: حسابات read-only للإنتاج، وتنفيذ DDL/DML فقط عبر migrations.
●	إجبار الاتصال بتشفير TLS، وتدوير كلمات المرور، وتفعيل تدقيق النشاط الحساس.
٣) الترحيلات والعمليات
●	تبنّوا أداة ترحيلات (Flyway أو Liquibase أو ORM migrations) مع Rollback مجرّب.
●	للتغييرات الكبيرة على الجداول استخدموا gh-ost أو pt-online-schema-change لتجنب التوقف.
●	بيئات منفصلة (dev/stage/prod) + بيانات seed + تشغيل فحوصات ما بعد الترحيل.
٤) التوافر والنسخ الاحتياطي
●	نسخ احتياطي يومي + Point-in-Time Recovery (binlog) مع اختبار استعادة ربع سنوي.
●	نسخة قراءة (read-replica) للتقارير، أو خدمة مُدارة (AWS RDS/Aurora) إن أمكن.
٥) الفهارس والأداء (مباشرة لسيناريوكم)
●	الكتالوج/القوائم: فهرس مركّب على (category_id, publish_status, is_visible, created_at) + فهرس للفرز بالسعر.
السلال/الطلبات:
●	Carts: (customer_id, last_activity_at)
●	Orders: (status, created_at) و (customer_id, created_at)، وفهرس فريد لـ order_no.
●	غطّوا الأعمدة المُستخدمة في الفلاتر الشائعة (brand/color/size/is_on_sale).
●	راجعوا EXPLAIN لأثقل 10 استعلامات واعمَلوا Covering Indexes عند الحاجة.
٦) التكامل التحليلي
●	أخرجوا التحليلات الثقيلة من الإنتاج عبر CDC (Debezium/Airbyte) → BigQuery.
●	احفظوا First/Last touch داخل قاعدة البيانات (على مستوى العميل والطلب) لتقارير التسويق.

٧) استخدام phpMyAdmin عمليًا
●	Prod: قراءة فقط (استعلامات تشخيصية خفيفة).
●	Stage/Dev: مسموح مع سجل تدقيق.
●	عمليات تنظيف/تعديل جماعي تُنفَّذ كسكربتات مُراجَعة، ليس يدويًا من الواجهة.
٨) طبقات مساندة
●	Redis للجلسات والكاش والمعدلات (rate limits).
●	طبقة Proxy (مثل ProxySQL/HAProxy) لإدارة الاتصالات وتوزيعها على الـ replicas.
 
بناء قاعدة البيانات MySQL 
بناء قاعدة البيانات MySQL 
الغرض: مرجع تنفيذي موحّد للفريق التقني لضمان أن بنية قاعدة البيانات محكمة، آمنة، قابلة للتوسع، وسهلة التشغيل.
النطاق: MySQL 8.x + InnoDB + phpMyAdmin (كأداة وصول مُقيّدة)، مع تكاملات اختيارية للتحليلات (CDC → BigQuery).
الجمهور: مهندسو البنية الخلفية/البيانات، مسؤول قواعد البيانات، قيادة التقنية.
 
0) TL;DR 
●	استخدموا MySQL 8.x / InnoDB، ترميز utf8mb4، توقيت UTC، وmigrations لكل تغيير.
●	مخزون بنمط Inventory Ledger (لا تعديل مباشر للكميات).
●	FK/UNIQUE/CHECK إلزامية مع فهارس مدروسة.
●	RBAC صارم + PII Masking عبر Views + تدقيق Audit.
●	PITR عبر binlog + اختبار استعادة ربع سنوي.
●	phpMyAdmin في الإنتاج قراءة فقط وخلف VPN.
 
1) الأهداف والنطاق
●	ضمان سلامة البيانات ومنع السجلات اليتيمة.
●	دعم الاستعلامات الحرجة (قوائم المنتجات، إنشاء طلب، تتبع الشحن) بزمن مقبول.
●	تمكين تحليلات دقيقة (First/Last-touch، تقارير المبيعات، المرتجعات، المخزون).
●	سهولة التشغيل والتوسّع (replicas، partitioning عند الحاجة).
النطاق الوظيفي: هوية العملاء، الكتالوج، المتغيرات (SKU)، المخزون، السلال، الطلبات، المدفوعات/الرديات، الشحن/التتبّع، المرتجعات (RMA)، المحفظة/العروض/الكوبونات، التحليلات.
 
2) مواصفات الخادم والإعدادات
●	الإصدار/المحرّك: MySQL 8.x, InnoDB فقط.
●	الترميز والترتيب: utf8mb4 وutf8mb4_unicode_ci افتراضياً.
●	sql_mode: STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO.
●	binlog: صيغة ROW + sync_binlog=1 + innodb_flush_log_at_trx_commit=1 لسلامة المعاملات.
●	الذاكرة: innodb_buffer_pool_size ≈ 70–80% من ذاكرة الخادم.
●	سجل البطيء: slow_query_log=ON, long_query_time=0.2 لمراقبة الاستعلامات.
ملاحظة: استخدموا خدمة مُدارة (مثل RDS) إن أمكن لتبسيط التوفّر والنسخ.

3) معمارية وطبقات البيانات (ERD عالي المستوى)
المرجع/الهوية
●	customers, addresses, devices, consents, segments
●	brands, categories (هرمية), attributes, media_assets
الكتالوج
●	products (SPU)، product_variants (SKU)
●	روابط السمات/الصور: variant_attributes, product_media
المخزون
●	inventory_ledger (المرجع الوحيد للحركة)
●	stock_snapshot (اختياري للتسريع)
التجارة
●	carts, cart_items
●	orders, order_items
●	المدفوعات: payments, payment_attempts, refunds
●	الشحن: shipments, shipment_events, carriers
●	المرتجعات: rmas, rma_items
●	المحفظة/العروض: wallets, wallet_tx, promotions, coupons, coupon_redemptions
التحليلات (اختياري)
●	events_raw (تجميعي)، جداول حقائق/أبعاد: fct_orders, fct_order_items, dim_date, fct_inventory_moves
قاعدة ذهبية: قيّم في order_items وغيره تُخزن كسَـنَـپشوت وقت الحدث (السعر، العملة، الخصم…)
 
4) معايير التصميم والأنواع
●	التسمية: snake_case، أسماء واضحة غير عامة.
●	المعرّفات: UUID (CHAR(36)) أو BINARY(16) حسب التفضيل؛ أرقام تلقائية داخلية مسموحة كمفاتيح بديلة.
●	التواريخ: DATETIME(3) بدقة ملي ثانية؛ UTC دائماً.
●	الأموال: DECIMAL(12,2) + عمود currency.
●	Soft delete: عمود archived_at مع فهارس تراعيه.
●	أعمدة تدقيق: created_at, updated_at, created_by, updated_by.

5) القيود والعلاقات (سلامة البيانات)
●	Foreign Keys إلزامية مع سياسات ON DELETE/UPDATE واضحة.
●	UNIQUE: مثل sku، وphone_e164 للعملاء.
●	CHECK: الأسعار ≥ 0، الكميات ≥ 0، مجموعة عملات مقبولة.
●	Idempotency keys: لمحاولات الدفع أو العمليات الحساسة.
 
6) الفهارس والأداء
أهداف زمنية
●	قوائم/بحث المنتج ≤ 300ms على ~50K متغير.
●	تأكيد طلب → إنشاء السجلات الأساسية ≤ 2s.
●	وصول حدث تتبّع شحنة → انعكاسه ≤ 1m.
إرشادات عامة
●	فهارس مركّبة تُطابق شروط WHERE والفرز ORDER BY.
●	Covering Indexes للاستعلامات الثقيلة المتكررة.
●	مراجعة EXPLAIN لأثقل 10 استعلامات شهرياً.
أمثلة عملية
●	القوائم: (category_id, publish_status, is_visible, created_at) + فهرس على price.
●	البحث بالخصائص: brand_id, (color, size), is_on_sale, is_best_seller.
●	السلال: (customer_id, last_activity_at).
●	الطلبات: (status, created_at) و(customer_id, created_at) + فريد order_no.
●	الشحن/المدفوعات: tracking_no, (order_id)، حالات المزود.
Partitioning (عند الحاجة)
●	جداول ضخمة زمنية مثل events_raw, inventory_ledger عبر RANGE على created_at.
 
7) نموذج المخزون بنمط Ledger
●	كل حركة في inventory_ledger تحمل سببًا (reason) ومرجعًا (reference_id/type):
○	purchase_receipt, adjustment, reservation, shipment_captured, rto_received, rma_returned …
●	حساب stock_on_hand وavailable_to_promise يتم دوريًا (Job خلفي) أو View مادّي.
●	يمنع التعديل المباشر على الرصيد؛ التغيير دائمًا عبر إضافة حركة.

8) الأمان والخصوصية وRBAC
تصنيف البيانات
●	PII: الهاتف، البريد، العنوان؛ حسّاسة: بيانات الدفع (Tokenized فقط)؛ غير حساسة: بيانات الكتالوج.
أذونات الأدوار (مثال)
●	Admin/DBA (كامل)، Ops/Finance (قراءة + إجراءات محددة)، CustomerService (قراءة مقنّعة)، Marketing/Analyst (Views تحليلية)، DevReadOnly (قراءة فقط).
سياسات
●	Least Privilege + مراجعة دورية للصلاحيات.
●	PII Masking عبر Views (إخفاء جزء من الهاتف/العنوان للأدوار غير المصرّح لها).
●	تشفير النقل (TLS) وتخزين الأسرار خارج الكود (Secret Manager).
●	Audit Log لعمليات حساسة (رديات، تغييرات حالة، تسويات مخزون).
 
9) النسخ الاحتياطي والتعافي من الكوارث (DR)
●	RPO ≤ 15m عبر binlog + RTO ≤ 60m (بيئة DR دافئة/باردة).
●	نسخ يومي + احتفاظ بالbinlogs لأسبوعين على الأقل.
●	اختبار استعادة ربع سنوي مع تحقق checksums وأعداد الصفوف.
●	توثيق مسار الاستعادة خطوة بخطوة.
 
10) الترحيلات (Migrations) وCI/CD
●	كل تغيّر Schema عبر Migration (Flyway/Liquibase/ORM) مع Rollback.
●	فحوصات تلقائية: lint للـDDL، مراجعة EXPLAIN للتغييرات المؤثرة.
●	تغييرات كبيرة بلا توقف عبر gh-ost أو pt-online-schema-change.
●	باك-أب قبل الترحيل الإنتاجي + خطة رجوع.
 
11) البيئات والبيانات
●	بيئات منفصلة: dev / stage / prod ببيانات مستقلة.
●	بيانات Seed للاختبار، مع قناع/إخفاء PII عند استخدام عينات من الإنتاج.
●	توليد نسخ تحليلات من خلال CDC بدل تشغيل استعلامات ثقيلة على الإنتاج.

12) المراقبة والتشغيل
●	لوحات: زمن الاستعلامات، بطء/Locks، حجم الجداول، أخطاء القيود.
●	تنبيهات: طفرات في 5xx/4xx، فشل نسخ احتياطي، ازدياد الاستعلامات البطيئة.
●	Runbooks: تباطؤ مفاجئ، تعارضات قفل، فشل مزود دفع/شحن.
 
13) سياسة استخدام phpMyAdmin
●	إنتاج: قراءة فقط للأدوار غير الإدارية؛ لا DDL/DML يدوي—المسموح عبر migrations فقط.
●	Stage/Dev: مسموح للمهندسين مع سجل تدقيق.
●	وصول خلف VPN/IP allowlist + 2FA لحسابات الإدارة.
●	الاستعلامات الثقيلة تُنفذ خارج ساعات الذروة وبعد مراجعة.
 
14) تكامل التحليلات (اختياري موصى به)
●	CDC (Debezium/Airbyte) → Warehouse (BigQuery) لتقارير مرنة دون الضغط على الإنتاج.
●	حفظ First-/Last-touch على مستوى المستخدم والطلب لقياس العائد الإعلاني بدقة.
●	نمذجة حقائق/أبعاد: fct_orders, fct_order_items, fct_inventory_moves, dim_date, dim_customer.
 
15) قوالب جاهزة (انسخ/املأ)
15.1 قالب قاموس بيانات (Data Dictionary)
●	الجدول: …
●	الوصف: …
●	الأعمدة:
○	column_name · النوع · السماحية (NULL/NOT NULL) · الافتراضي · القيود (PK/FK/UNIQUE/CHECK) · الوصف · مثال
●	الفهارس: (الاسم، الأعمدة، الهدف من الاستعلام)
●	ملاحظات الأداء/الأمان: …
15.2 قالب سياسة النسخ والاستعادة
●	RPO/RTO: …
●	نوع النسخ: يومي تزايدي + binlogs
●	التحقق الدوري: checksums، استعادة اختبارية
●	خطوات الاستعادة: …
15.3 قالب مصفوفة الأذونات (RBAC)
●	الدور | الجداول/Views | العمليات (SELECT/INSERT/UPDATE/DELETE) | قيود/ملاحظات
15.4 قالب خطة الفهارس
●	الاستعلام | التواتر | الجدول | اقتراح الفهرس | EXPLAIN قبل/بعد | التحسن
15.5 قالب فحص جودة البيانات
●	التحقق | القيد/القانون | نسبة التغطية | استثناءات | الإجراء التصحيحي
 
16) قوائم تحقق (Checklists)
16.1 أثناء التصميم
16.2 قبل الإطلاق/الترحيل الإنتاجي
16.3 التشغيل الدوري
●	يومي: مراقبة بطء الاستعلامات/الأخطاء/النسخ.
●	أسبوعي: مراجعة الفهارس للأثقل استخدامًا.
●	شهري: اختبار استعادة جزئي + تحسينات أداء.
●	ربع سنوي: اختبار استعادة كامل + مراجعة RBAC.
 
17) ملحق (قاموس حالات موحّد كمثال)
●	order_status: created → confirmed → packed → shipped → delivered → (rto/lost/cancelled)
●	payment_state: pending / authorized / captured / failed / refunded
●	shipment_event: picked_up, in_transit, out_for_delivery, delivered, rto_initiated, rto_received
●	rma_status: requested, approved, received, refunded/denied
 
الحماية والأساسيات التشغيلية 
الحماية والأساسيات التشغيلية
1. الحماية (Security)
●	تطبيق مبدأ Least Privilege مع أدوار واضحة (Admin, Ops, CS, Marketing, ReadOnly).
●	تفعيل MFA لجميع حسابات الإدارة والقاعدة.
●	استخدام Secrets Manager لتخزين المفاتيح والتوكنات وتدويرها بشكل دوري.
●	تشفير البيانات At-Rest و In-Transit (TLS 1.2+).
●	تطبيق PII Masking للهاتف والعنوان في واجهات غير مخوّلة.
●	تفعيل Audit Log لجميع العمليات الحساسة (تعديل بيانات، تغييرات مالية).
●	الحماية من الهجمات: منع SQL Injection/XSS، واستخدام ORM آمن.
●	تفعيل Rate Limiting على عمليات الدخول وOTP والدفع.
2. النسخ الاحتياطي والتعافي (Backup & Recovery)
●	تحديد RPO ≤ 15 دقيقة و RTO ≤ 60 دقيقة.
●	نسخ احتياطي يومي/ساعي مشفّر مع مراقبة حالة النسخ.
●	اختبار استعادة البيانات بشكل ربع سنوي وتوثيق النتائج.
●	خطة Disaster Recovery ببيئة بديلة جاهزة (Warm/Cold).
3. المراقبة والموثوقية (Monitoring & Reliability)
●	مؤشرات أداء مستهدفة (SLOs):
○	استعلام قائمة المنتجات ≤ 300ms (50K variants).
○	إنشاء طلب ≤ 2s.
○	Webhook مزوّد دفع ≤ 1s.
●	تفعيل Logs، Metrics، Traces بشكل منظم.
●	تنبيهات على ارتفاع الأخطاء (5xx/4xx)، محاولات الدخول الفاشلة، وفشل النسخ الاحتياطي.
●	اختبارات Load/Stress دورية للتأكد من تحمل النظام.
4. الخصوصية والامتثال (Privacy & Compliance)
●	تصنيف البيانات (Public / Internal / Confidential / Sensitive).
●	تطبيق سياسة الاحتفاظ بالبيانات (Data Retention) مع جداول زمنية للحذف أو الأرشفة.
●	تقليل تخزين البيانات الحساسة والاكتفاء بالضروري فقط (Data Minimization).
●	حقوق العملاء: تصحيح/حذف بياناتهم عند الطلب مع وجود إجراءات واضحة.
●	اتفاقيات حماية بيانات (DPA) مع المزوّدين الخارجيين (الدفع، الشحن، الرسائل).
5. إدارة التغيير والحوادث (Change & Incident Management)
●	سجل تغييرات (Change Log) قبل أي نشر.
●	Runbooks جاهزة للأحداث الشائعة (فشل الدفع، مشاكل الشحن، توقف خدمة).
●	تطبيق Post-Mortem إلزامي لأي حادثة حرجة (Sev-1/Sev-2) مع خطة منع التكرار. 
NOTE 
الهدف
●	قاعدة بيانات سليمة، متّسقة، قابلة للتوسّع، سهلة التكامل والاختبار، وتحمي الخصوصية.
النطاق
●	العملاء، الكتالوج، المنتجات، الطلبات، السلة، المفضلة، المدفوعات، الشحن، المرتجعات والاستبدال، العروض والخصومات، المشتريات والتوريد، التحليلات، المحفظة  
ما يجب توفره (Outputs)
1.	ERD نهائي يوضّح الجداول والعلاقات واتجاهاتها.
2.	معايير تسمية وحوكمة (أسماء، snake_case، الحقول القياسية مثل created_at/updated_at، سياسة الحذف المنطقي).
3.	قاموس بيانات يحدد النوع والقيود والسماحية لكل حقل.
4.	مصفوفة قيود: مفاتيح خارجية/فريدة/تحقق (FK/UNIQUE/CHECK).
5.	خطة فهارس مبنية على الاستعلامات الأكثر استخدامًا.
6.	خطة ترحيلات (Migrations) لكل تغيير على المخطط مع إمكانية التراجع.
7.	سياسة خصوصية وأمان: تصنيف PII، تشفير/إخفاء، أدوار وصلاحيات وصول، تدقيق (Audit).
8.	سياسة نسخ احتياطي واستعادة مع اختبار استعادة مُوثّق.
9.	خطة اختبار: سلامة/قواعد/تزامن/أداء + بيانات Seed.
10.	توثيق موجز في /docs/db.md يشرح كيف نطوّر/نختبر/نستعيد.
معايير القبول (يجب تحققها قبل الاعتماد)
●	سلامة البيانات: لا سجلات يتيمة؛ جميع العلاقات محمية بـFK؛ قيود CHECK لكل الحدود (سعر ≥ 0، كمية ≥ 0…).
●	اتساق التصميم: تطبيع لا يقل عن 3NF؛ أي إلغاء تطبيع مبرَّر للأداء.
●	اتساق الأسماء والأنواع: لا أعمدة عامة/غامضة؛ وصف واضح لكل حقل.
●	الفهارس: موجودة على أعمدة الفرز/التصفية الشائعة؛ لا فهارس مكررة.
●	الأمن والخصوصية: أقل صلاحيات للوصول (Roles/Grants)، تشفير/إخفاء للـPII، سجل تدقيق للعمليات الحساسة.
●	الأداء: ميزانيات زمنية واضحة للاستعلامات الرئيسية (قائمة، تفاصيل، إنشاء طلب) ضمن حدود متفق عليها.
●	الترحيلات: كل تغيير يمر عبر Migration قابل للتراجع، ولا تعديل يدوي مباشر على الإنتاج.
●	الاختبارات: تغطية CRUD، حالات سلبية وحدّية، تعارضات التزامن، واختبار أداء بسيط—all ناجحة على بيئة تجريبية.
●	التوثيق: محدث وكافٍ لتشغيل وتطوير القاعدة بدون أسئلة إضافية.



مبادئ تصميم إلزامية
●	IDs غير قابلة للتخمين (UUID)، Soft delete عبر archived_at بدل الحذف الفعلي.
●	أعمدة تدقيق موحّدة: created_at/updated_at/by، ومصدر آخر تعديل عند الحاجة.
●	فصل الحسّاس/PII في جداول أو أعمدة مع تشفير/Masking.
●	Ledger لحركة المخزون بدل تعديل كميات مباشرة (traceability).
●	عدم تكرار الحقيقة: كل حقيقة تُخزَّن مرّة واحدة؛ اللقطات تُلتقط عند الحاجة (مثل snapshot لسعر الشراء في order_items).
الاختبار والجودة (بدون أدوات محددة)
●	سلامة المخطط: إدخالات غير صالحة تُرفَض بالقيود، والعلاقات تمنع اليُتم.
●	قواعد العمل: جميع الحالات السلبية تُرجع أخطاء مفهومة (وليس صمتًا).
●	التزامن: تحديثان متوازيان لنفس السجل لا يسببان فقدان بيانات (تفادي السباق).
●	الأداء: الاستعلامات الحرجة تحت الميزانيات المحددة وبخطط تنفيذ (Explain) مقبولة.
●	الاسترجاع: سيناريو استعادة من نسخة احتياطية يثبت إمكانية العودة لوضع سليم.
الأمان والخصوصية
●	Least Privilege: حسابات التطبيق تمتلك أقل صلاحية لازمة فقط.
●	فصل الأسرار: لا أسرار داخل الكود؛ إدارة أسرار خارجية.
●	التدقيق والمراقبة: تسجيل من غيّر ماذا ومتى؛ مؤشرات لأخطاء القيود وزمن الاستعلامات.
المراقبة والتشغيل
●	لوحات مراقبة لزمن الاستعلامات والأخطاء وأحجام الجداول.
●	تنبيهات عند تجاوز عتبات الأداء أو ارتفاع أخطاء القيود.
●	Runbook مختصر: ماذا نفعل عند بطء/قفل/خطأ قيود.
 
أهم الفجوات 
أهم الفجوات  
1) ERD تفصيلي 
المطلوب الآن: إخراج ERD على 3 طبقات: الهوية/المرجعية، المعاملات، التحليلات. (يُسلم بصيغة صورة + mermaid/plantuml اختيارياً) — يشمل:
●	العملاء: customers, addresses, devices, consents, segments (M2M), cod_profile, comms_log. 
●	الكتالوج: brands, products, product_variants, categories (self-parent), product_categories (Lk), attributes/attribute_values/product_attributes/variant_attributes, media, collections (+ rules). 
●	المخزون: warehouses, inventory_ledger (event_time, variant_id, warehouse_id, qty_change, reason, ref_type/ref_id), stock_snapshot (اختياري للتسريع). (المبدأ مذكور ويحتاج تفصيل) 
●	الطلبات: orders, order_items, order_status_history, shipments, shipment_items, tracking_events, payments, payment_attempts, refunds, cod_remittance, promotions, order_discounts, address_snapshot. 
●	السلة: carts, cart_items, cart_coupons.
●	المفضلة: wishlists, wishlist_items.
●	RMA: rmas, rma_items, rma_logistics, rma_resolutions. 
●	التحليلات: events_raw (للاستيعاب إن لزم)، tables للـ RFM/LTV مجمّعة (اختياري لاحقًا).
2) قاموس بيانات + مصفوفة قيود
●	أنواع/قيود إلزامية:
○	UUID/VARCHAR للمعرّفات غير القابلة للتخمين.
○	ENUM/Domain للجداول المرجعية (order_status، payment_state، shipment_state…).
○	CHECK: price ≥ 0، qty ≥ 0، phone بصيغة E.164، currency in {YER,SAR,…}. 
○	UNIQUE: sku على مستوى variant، (product_id, color, size)، phone على customers.
○	FK مع ON DELETE/UPDATE سياسات مدروسة لمنع اليُتم. 
●	Soft-delete: archived_at مع فهارس تراعيه. 
3) فهارس مبنية على الاستعلامات الفعلية
ضع خطة مبدئية (قابلة للتعديل بعد قياس الإنتاج):
●	قوائم المنتجات: idx on (category_id, is_visible, publish_status, created_at), و(price) للفرز.
●	البحث/الفلاتر: فهارس على (brand_id), (color, size), (is_on_sale), (is_best_seller).
●	السلة/الطلب: (customer_id, last_activity_at) للسلة؛ (order_no)، (status, created_at), (customer_id, created_at) للطلبات.
●	الشحن: (tracking_no), (courier_id, mapped_status), (order_id).
●	المدفوعات: (order_id), (state), (provider_ref).
●	RMA: (order_id), (state), (reason_code).
●	تحسين لاحق: partial indexes (publish_status='published'), وcovering indexes للاستعلامات الثقيلة. (الخطة مطلوبة كمتطلب عام) 

4) النسخ الاحتياطي/الاستعادة + RTO/RPO
●	وثّق: RPO ≤ 15 دقيقة (WAL/streaming)، RTO ≤ 1 ساعة (بيئة DR باردة/دافئة).
●	اختبار استعادة فصلي مع تقرير نجاح وإثبات صحة (checksums، counts). (السياسة مطلوبة بالملف وتحتاج أرقامًا وتنفيذ اختبار دوري) 
5) أمن/خصوصية وRBAC مفصّل
●	تصنيف PII (phone, address, comms_log) + Masking لأدوار غير مخوّلة.
●	RBAC: أدوار (Admin, Ops, CS, Finance, Marketing, DevReadOnly) وGrants لكل جدول/عمود.
●	Audit غير قابل للتعديل لعمليات الدفع/الاسترداد/تغيير الحالات. (مذكور كمتطلب ويحتاج مصفوفة أذونات مفصلة) 
6) مشتريات/توريد + تكاليف
●	أضِف جداول: suppliers, purchase_orders, po_items, grn (استلام), supplier_invoices, landed_cost_allocations لاحتساب تكلفة القطعة الواحدة بدقّة وتغذية التسعير/الهامش. (النطاق ذكر “المشتريات والتوريد” دون تفصيل) 
7) Ledger المخزون (تفصيل عملي)
●	inventory_ledger يسجل كل تغيير مع السبب: (purchase_receipt, reservation, shipment_captured, rto_received, rma_returned, adjustment, stocktake).
●	قواعد: لا تعديل مباشر للمخزون؛ فقط عبر أحداث ledger + job تَحسِب stock_on_hand و available_to_promise لكل variant/warehouse. (المبدأ مذكور ويحتاج تصميم جدول واضح) 
8) إكمال RMA
●	أضف حالات واضحة: opened → awaiting_pickup → in_quality_check → approved_refund/approved_exchange → completed; مسارات جانبية: rejected / cancelled.
●	سياسات مالية: ربط Refund بالدفع الأصلي (أونلاين) أو store_credit للمحفظة عند COD. (الإطار موجود ويحتاج إكمال حالات/سياسات) 
9) التحليلات
●	توحيد user_id مع GA4/Firebase وربط UTM على مستوى الطلب (مذكور).
●	طبقة business facts: fact_orders, fact_order_items, fact_rma, fact_inventory_movements + dimensions (date, product, variant, category, city, courier, source/medium).
●	KPIs المذكورة للمنتج/المحتوى تُحسب تلقائيًا في لوحات. 
 





اقتراح هيكل العلاقات (High-level ERD نصّي)
●	customers(1) —< addresses —< orders —< order_items
●	orders(1) —< shipments —< tracking_events
●	orders(1) —< payments —< payment_attempts; payments(1) —< refunds
●	products(1) —< product_variants —< inventory_ledger
●	products( M )—< product_categories >—(1) categories
●	products(1) —< media ; products(M)—< collections_link >—(1) collections
●	customers(1) —< carts —< cart_items
●	customers(1) —< wishlists —< wishlist_items
●	orders(1) —< rmas —< rma_items (ترتبط أيضًا بـ shipments/logistics)
●	promotions ترتبط بـ orders و/أو order_items (خصم سطر/طلب كامل)
 
خطة اختبارات قبول (مبنية على مستندك + إضافات عملية)
1.	سلامة المخطط: محاولات إدخال مخالفات (سعر سالب، SKU مكرر، هاتف غير E.164) تُرفض. 
2.	CRUD أساسي لكل كيان (منتج، نسخة، سلة، طلب، شحنة، دفع، RMA). 
3.	تزامن/تعارض: تحديثان متوازيان لنفس السلة/الطلب لا يفقدان البيانات. 
4.	أداء:
○	قائمة منتجات مصفّاة: ≤ 300ms على 50K variant مع فهرسة مناسبة.
○	إنشاء طلب (confirm→packed): ≤ 2s مع حجز مخزون.
○	تتبع شحنة “out_for_delivery” يظهر خلال ≤ 1 دقيقة من webhook. 
5.	استعادة نسخة احتياطية: محاكاة فشل واسترجاع ناجح موثّق. 
 
تسليمات عمليّة (What we’ll ship)
1.	ERD (صورة + ملف قابل للتعديل) يغطي كل الجداول والعلاقات. 
2.	قاموس بيانات: جدول لكل حقل (النوع/الطول/NULL/DEFAULT/UNIQUE/CHECK/FK). 
3.	Matrix القيود (FK/UNIQUE/CHECK) مجمّعة. 
4.	خطة فهارس مع لائحة الاستعلامات النموذجية وخطط التنفيذ (EXPLAIN). 
5.	سياسة نسخ/استعادة برقم RPO/RTO وجدولة اختبارات. 
6.	RBAC: مصفوفة أدوار × جداول/أعمدة + سياسة Masking للـPII. 
7.	تفصيل Ledger المخزون (جداول، أسباب، روابط). 
8.	RMA مكتمل: حالات، قواعد، تكامل مالي/مخزني ورسائل. 
9.	/docs/db.md: تشغيل محلي، ترحيلات، اختبارات، الاستعادة، والممارسات. 
 
أولويات التنفيذ 
1.	ERD + قاموس بيانات + Matrix قيود.
2.	Ledger المخزون + مشتريات/توريد (مصدر الحقيقة للمخزون والتكلفة).
3.	فهارس + ميزانيات أداء + مراقبة (لوحات زمن الاستعلامات/أحجام الجداول).
4.	RBAC/PII/Audit + سياسة نسخ/استعادة بأرقام RPO/RTO واختبار دوري.
5.	إكمال RMA + ربطه بالمدفوعات/الشحن والمخزون.
6.	توحيد القواميس (ألوان/مقاسات/أقمشة) قبل أي استيراد كبير — لمنع الفوضى النصية في الكتالوج.
7.	طبقة التحليلات (facts/dims) للـ KPIs المذكورة.
 
ملاحظات 
ملاحظات 
1.	تصميم ERD تفصيلي
○	رسم علاقات الجداول الرئيسية (Customers, Orders, Payments, Shipments, RMA, Products, Variants, Inventory Ledger, Wallet).
○	إضافة قيود Primary / Foreign Keys بشكل واضح.
○	إعداد قاموس بيانات (Data Dictionary) يشرح كل جدول وحقل.
2.	Inventory Ledger (دفتر المخزون)
○	تصميم جدول ledger يحوي كل حركات المخزون (شراء، استلام، حجز، شحن، إرجاع، جرد).
○	حساب الكميات (stock_on_hand و available_to_promise) بشكل ديناميكي من الـ ledger فقط.
○	منع التعديل المباشر على المخزون.
3.	RBAC / PII / Audit
○	مصفوفة صلاحيات واضحة تحدد من يقرأ أو يعدل أي بيانات.
○	Masking للهاتف والعنوان عند عرض البيانات لموظفين غير مخوّلين.
○	إنشاء جداول سجل تدقيق (Audit Log) append-only لتوثيق العمليات الحساسة.
4.	خطة النسخ الاحتياطي والاستعادة
○	تحديد أرقام RPO (≤15 دقيقة) وRTO (≤1 ساعة).
○	وضع سياسة اختبار استعادة ربع سنوية والتوثيق الكامل لنتائجها.
5.	خطة الفهارس والأداء
○	فهارس على الحقول الأكثر استخدامًا (sku, phone, order_no, brand, color, size, customer_id, status).
○	استخدام partial وcovering indexes حيث يلزم.
○	إضافة حدود زمنية للأداء (مثال: إنشاء طلب ≤2 ثانية، قائمة منتجات ≤300ms).
6.	توحيد القواميس والمعايير
○	إنشاء جداول مرجعية للألوان، المقاسات، المدن، الخامات، وربطها مع المنتجات.
○	وضع Mapping مع خيارات البحث والفلاتر.
7.	الاختبارات وقبول التسليمات
○	تعريف Definition of Done لكل كيان (CRUD + قيود + سيناريوهات فشل).
○	تضمين حالات edge cases (مثل SKU مكرر، رصيد سلبي، هاتف غير صحيح).
8.	التزامن والمعالجة المتزامنة
○	استخدام أعمدة version أو updated_at للتعامل مع التعارض (Optimistic Locking).
○	تطبيق مفاتيح Idempotency في عمليات الدفع والطلبات لتجنب التكرار.
9.	التحليلات والتقارير
○	إنشاء fact tables (Orders, Payments, Inventory Movements, Traffic).
○	إضافة Materialized Views للـ Funnel، السلات المهجورة، العملاء المتكررين.
○	ربط بيانات UTM مع الطلبات لتتبع الحملات.
10.	المشتريات والتوريد
●	إضافة Vendor KPIs (التأخير، نسب الأخطاء، جودة الشحن).
●	وضع قواعد إعادة الطلب (Reorder Rules) وفق المخزون والدوران.
 
علامة التبويب 2 
فجوات للوصول إلى 95–100% (عملي ومختصر)
1.	خصوصية وأمن: تشفير الهاتف/الحقول الحساسة، إدارة مفاتيح، RBAC (صلاحيات حسب الدور)، Audit Logs للوصول والتعديلات.
2.	امتثال وقيود بيانات: سياسة احتفاظ وحذف، مسارات DSR (تصدير/حذف بيانات العميل)، توثيق دليل الموافقة مع طابع زمني، تكامل قوائم Suppression مع مزودي الرسائل.
3.	حوكمة وجودة البيانات: قاموس بيانات رسمي، قواعد تحقق وإغلاق التكرارات آليًا، فحوص تكامل مرجعي، اختبارات بيانات دورية.
4.	اعتمادية وتشغيل: نسخ احتياطي واستعادة مُختبرة، أهداف RPO/RTO، نهج للهجرات والترحيلات مع تراجع (rollback) واضح.
5.	قابلية المراقبة: لوحات مراقبة زمن/أخطاء واجهات CRUD، تنبيهات، SLO لزمن الاستجابة والأخطاء.
6.	الأداء والتوسّع: فهارس/تقسيم جداول عالية الحجم (contact_log)، خطة أرشفة، اختبارات ضغط (P95).
7.	واجهات واندماجات: Pagination/Search موحَّدة، Rate limiting وIdempotency للواجهات، مخطط أحداث (webhooks) قياسي.
8.	تحليلات متقدمة: ETL ثابت إلى Warehouse (مثلاً BigQuery)، تعريف موحَّد للأحداث والقُمع، Cohorts/Retention قياسية.
9.	تشغيل COD: Runbook لضبط عتبات الحظر/الفكّ، تقارير فشل حسب المدينة/المندوب مع إجراءات تصحيح.
10.	أمن تطبيقي: مراجعة أمنية/اختبار اختراق أساسي، إدارة أسرار مركزية.
 
*معايير قاعدة البيانات ومنع الأخطاء 
Zahraah – معايير قاعدة البيانات ومنع الأخطاء

هدف الملف: أن يكون مرجعًا تنفيذيًا واحدًا يمنع الوقوع في الأخطاء عبر كامل دورة حياة قاعدة البيانات (تصميم → بناء → تشغيل → تحليلات → أمان → نسخ/تعافٍ). النطاق: MySQL 8.x + InnoDB، مع Redis (Cache)، OpenSearch (بحث)، BigQuery/Metabase (تحليل)، وخدمات دفع/شحن خارجية.
 
0) ملخّص آلية العمل والاعتماديات (كيف تتكامل المنظومة)
●	قاعدة البيانات التشغيلية (OLTP) هي مصدر الحقيقة لكل معاملات المتجر (عملاء، كتالوج، عربة، طلبات، دفع، شحن…)، وتُستهلك عبر API/خدمات خلفية.
●	Cache (Redis): لتسريع القراءة والجلسات وRate-Limiting، مع سياسة إبطال دقيقة (Cache-aside) – الحقيقة تبقى في DB.
●	Search (OpenSearch/Elasticsearch): لفهرسة المنتجات والبحث النصّي/المرادفات، مع مزامنة تدريجية من DB.
●	Object Storage: صور وملفات خارج DB (يُخزَّن في DB المسار والميتا فقط).
●	تحليلات/BI: أحداث تطبيق إلى GA4/Firebase؛ وCDC/ETL من MySQL → BigQuery؛ وMetabase/Looker للقراءة من BigQuery/Replica فقط.
●	أمن/حماية: طبقة أذونات دقيقة، أسرار عبر Secret Manager، اتصال TLS، Logging/Audit، نسخ احتياطي + تعافٍ.
أي خلل في طبقة (سكيما/استعلام/كاش/بحث/تحليل/أمان) ينعكس على بقية الطبقات. هذا الملف يضع معايير وقوائم تدقيق لمنع الخطأ قبل ظهوره.
 
1) معايير تصميم السكيما (Schema Standards)
الترميز والتوقيت
●	utf8mb4 + Collation ملائم للعربية (مثل: utf8mb4_0900_ai_ci).
●	كل الأوقات بـUTC في DB؛ التحويل للمناطق الزمنية يتم في الواجهة.
الأنواع (Types)
●	الأموال: DECIMAL(12,2) (أو حسب الحاجة) – ممنوع FLOAT/DOUBLE للأموال.
●	الهاتف/الإيميل/المعرفات الخارجية: VARCHAR مع UNIQUE حيث يلزم.
●	JSON للاحتياجات الاختيارية/المرنة فقط، مع حقول أساسية منظّمة في أعمدة طبيعية.
●	ممنوع تخزين الصور/الملفات داخل DB (BLOB)؛ خزّن المسارات وميتا البيانات فقط.
المفاتيح الأساسية والأولية
●	جداول OLTP الحرجة: BIGINT UNSIGNED AUTO_INCREMENT كمفتاح أساسي.
●	ULID/UUIDv7 عند الحاجة لتكامل بين أنظمة (تجنّب UUID v4 كمفتاح أساسي في InnoDB).
القيود والمرجعيات
●	FK إلزامية مع أفعال ON UPDATE/DELETE مناسبة.
●	Lookup tables بدل ENUM للقيم المتغيّرة (حالات الطلب/الشحن/الدفع…).
●	UNIQUE حيث تتطلب الأعمال (الإيميل، باركود داخلي، رقم الطلب…).
معايير الحقول
●	أعمدة نظامية لكل جدول: id, status, created_at, updated_at, created_by, updated_by, deleted_at NULL.
●	التسمية: snake_case؛ المفاتيح الخارجية تنتهي بـ_id؛ تواريخ بـ*_at.
●	Soft-delete عبر deleted_at + فهارس/Views تراعي الحذف.
●	Partitioning للجداول الضخمة الزمنية (logs/notifications) مع سياسة دوران/أرشفة.
فصل OLTP عن OLAP
●	السكيما التشغيلية للمعاملات فقط؛ التقارير الثقيلة والـBI في BigQuery/Replica.
 
2) نموذج كيانات التجارة الإلكترونية (مختصر تنفيذي)
الهوية/العملاء: users, user_devices, addresses, consents, segments_membership.
الكتالوج والمخزون: categories, brands, products (SPU), attributes/values, skus (SKU), inventory, media, price_lists, sku_prices.
العربة/الطلبات/الدفع/الشحن: carts, cart_items, orders, order_items, payments, refunds, returns/return_items, shipments.
الخصومات والكوبونات: promotions, promotion_rules, promotion_actions, coupons, coupon_redemptions.
التفاعل/الولاء: wishlists, wishlist_items, reviews, loyalty_ledger, notifications_log.
الإسناد التسويقي: attributions أو جداول utm_first_touch وutm_last_touch.
جميع الجداول أعلاه تلتزم بمعايير النوع/المفاتيح/القيود المذكورة في §1.
 
3) الفهارس والاستعلامات (Indexing & Query Patterns)
●	فهرس لكل FK، وفهارس مركّبة لأكثر WHERE/ORDER BY شيوعًا.
●	ترتيب أعمدة الفهرس: من الأكثر انتقائية للأقل، ومطابقة ترتيب الفرز إن أمكن.
●	Covering Index للاستعلامات الحرجة القراءة.
●	ممنوع SELECT *؛ حدّد الأعمدة المطلوبة.
●	ممنوع الدوال على الأعمدة المُفلترة (DATE(col)=…)، استخدم نطاقات (col BETWEEN …).
●	LIKE '%term' يمنع الفهرس؛ استخدم محرك البحث للنصوص.
●	Pagination كبيرة: Keyset pagination بدل OFFSET/LIMIT.
●	معالجة N+1 عبر JOIN/IN/Batch.
●	راجع كل استعلام حرِج بـEXPLAIN قبل الإنتاج.
أنماط فهارس مقترحة
●	منتجات حسب القسم/الظهور: (category_id, is_active, sort_order).
●	طلبات حسب العميل/التاريخ: (user_id, created_at DESC) + فهرس على (created_at) للتقارير.
●	عناصر الطلب: (order_id) و(sku_id).
●	مخزون: (sku_id), وفهارس لمخزون المستودعات إن تعددت.
●	كوبونات: code UNIQUE, واستعلامات coupon_redemptions(user_id, coupon_id).
 
4) المعاملات والقفل (Transactions & Locking)
●	معاملات قصيرة، هدف واحد لكل معاملة.
●	ترتيب ثابت للعمليات الحسّاسة (حجز مخزون → حساب السعر/الخصم → الدفع → تأكيد الطلب).
●	استخدم SELECT … FOR UPDATE عند الحجز/التناقص لمنع Oversell.
●	Idempotency لكل مسارات الدفع/الطلب عبر idempotency_key.
●	انتبه لقراءات الـReplica (Replication Lag)؛ لمسارات “اقرأ بعد كتابة” استخدم الأساس/آليات توكيد.
 
5) الطبقات المساندة (Cache/Search/Storage/Async)
●	Cache-aside مع مفاتيح محدّدة وTTL وسياسة إبطال عند الكتابة/التغيير.
●	Search بمزامنة تدريجية (Change Data Capture/Events) لا إعادة فهرسة كاملة إلا لضرورة.
●	Object Storage للصور/الملفات؛ في DB: المسار/الأبعاد/النوع/الترتيب فقط.
●	مهام ثقيلة (فواتير/PDF/تجميع تقارير) تُنقَل لخدمات غير متزامنة.
 
6) الأمن والامتثال (Security & Compliance)
●	أقلّ صلاحية: مستخدمون منفصلون (admin محدود، app_rw، app_ro، analyst_ro).
●	اتصال TLS، وولوج الإنتاج عبر VPN/Bastion فقط.
●	الأسرار عبر Secret Manager؛ ممنوع تخزينها في الكود/الريبو.
●	Prepared Statements دائمًا لمنع حقن SQL.
●	تصنيف PII (هاتف/إيميل/عنوان) وتقليل الوصول؛ Masking في أدوات التحليل.
●	Audit لتغييرات حسّاسة (الأسعار/الخصومات/النقاط/الموافقات).
●	حماية أي أدوات إدارة (مثل phpMyAdmin) خلف VPN و2FA وقيود IP، وتعطيل العمليات الخطرة للمستخدمين غير الإداريين.
 

7) النسخ الاحتياطي والتعافي (Backup & DR)
●	نسخ كامل يومي + Binlogs لـ7–14 يومًا (PITR).
●	اختبار استعادة ربع سنوي موثّق + تمارين Failover نصف سنوية.
●	تخزين النسخ في موقع منفصل/سحابة مختلفة (Offsite).
●	تعريف واقعي لـRPO/RTO ومراجعة سنوية.
 
8) المراقبة والتشغيل (Observability & Ops)
●	فعّل Slow Query Log, Performance Schema.
●	لوحات مراقبة: QPS, p95/p99 latency, error rate, buffer pool hit ratio, deadlocks, replication lag, connections, table growth.
●	تنبيهات على العتبات، ومسار Incident واضح (On-call/Runbook).
●	جدولة ANALYZE TABLE الدوري للجداول الكبيرة لتحديث الإحصاءات.
 
9) الترقيات والترحيلات (Migrations)
●	كل تغييرات الـSchema/البيانات عبر Flyway/Liquibase فقط.
●	Zero-downtime pattern:
1.	إضافة حقول جديدة اختيارية.
2.	تعبئة خلفية على دفعات.
3.	تحديث التطبيق للقراءة/الكتابة الجديدة.
4.	إزالة القديم لاحقًا.
●	Online DDL للجداول الكبيرة + نافذة صيانة مخططة عند الحاجة.
●	سياسة "أربع عيون" لمراجعة أي ALTER/DELETE/UPDATE واسع.
 
10) الجودة والاختبارات (Quality & Testing)
●	اختبارات وحدة لطبقة الوصول للبيانات، وتكامل على Staging ببيانات قريبة من الإنتاج (مموّهة).
●	اختبارات dbt/SQL: NOT NULL, UNIQUE, FK, نطاقات القيم.
●	Test Cases حرِجة:
○	أموال (تقريب/ضرائب/خصومات)،
○	قفل المخزون ومنع Oversell،
○	Idempotency للدفع،
○	ترميز عربي/رموز/إيموجي،
○	مناطق زمنية،
○	تكرار الإيميل/الهاتف،
○	سلوك N+1،
○	قراءة بعد كتابة مع Replica.
 
11) الاحتفاظ/الأرشفة/الخصوصية (Retention & Archiving)
●	سياسات احتفاظ لكل كيان (مثال: إشعارات 6–12 شهرًا، شحن 24 شهرًا…).
●	عمليات Purging/Archiving مجدولة إلى جداول أرشيف/مخزن بارد.
●	مسارات حذف/إخفاء بيانات العميل عند الطلب (حق النسيان/الامتثال).
 
12) التكامل التحليلي (MySQL → BigQuery/GA4/Metabase)
●	CDC (Debezium/Maxwell أو ETL مُدار) للجداول التشغيلية إلى BigQuery.
●	نموذج نجمي في BI: fact_orders, fact_order_items, dim_customers, dim_products, dim_sku, dim_date, dim_channel…
●	إخفاء/تجزئة PII قبل التحليل؛ عدم قراءة أدوات التحليل من إنتاج مباشرة.
●	أحداث GA4/Firebase تُربَط بـuser_id وUTM (أول/آخر) داخل BigQuery.
 
13) مكافحة الأخطاء الخاصة بالتجارة الإلكترونية
●	Oversell: الحجز/التناقص داخل معاملة مقفلة + ترتيب ثابت + FOR UPDATE.
●	الكوبونات/الخصومات:
○	تثبيت (snapshot) قيمة الخصم عند إنشاء الطلب؛
○	UNIQUE على code؛
○	سجل coupon_redemptions بمنع التكرار حسب القواعد.
●	السعر النهائي: تخزين snapshot للسعر والضرائب والخصومات في order_items.
●	COD Risk: جداول سلوك COD (محاولات فاشلة/عناوين مكررة/حدود)، مع سياسات حظر ذكية.
●	الإسناد التسويقي: حفظ UTM أول/آخر على مستوى الطلب/المستخدم وقت الحدث.
●	العربية والبحث: استخدام محرك بحث مع محلّل عربي ومرادفات؛ لا تعتمد على LIKE فقط.
 
14) إدارة الأداء والكلفة
●	مراجعة فهارس ربع سنوية، وتنظيف الفهارس غير المستخدمة.
●	مراجعة الاستعلامات الأكثر بطئًا شهريًا وتحسينها.
●	ضبط Connection Pool من التطبيق، وmax_allowed_packet حسب الأحجام.
●	تجنّب OPTIMIZE TABLE العشوائي؛ استخدمه فقط عند وجود تجزئة حقيقية وبعد ساعات الذروة.
●	مراقبة نمو الجداول ووضع حدود/تنبيهات مبكرة.
 
15) قوائم تدقيق (Checklists)
A) إنشاء قاعدة بيانات إنتاج جديدة
1.	MySQL 8/InnoDB + utf8mb4 + utf8mb4_0900_ai_ci + UTC.
2.	شبكات: Private Subnet + TLS + قيود IP + VPN/Bastion.
3.	مستخدمون/أدوار: admin (مقفل)، app_rw, app_ro, analyst_ro.
4.	Slow Query Log + Performance Schema مفعّلان.
5.	نسخ كامل يومي + Binlogs (7–14 يومًا) + اختبار استعادة.
6.	إعداد Migrations (Flyway/Liquibase) + سياسة مراجعة.
7.	Replica للقراءة + خطة Failover موثّقة.
8.	مراقبة/لوحات/تنبيهات + Runbooks.
9.	أسرار عبر Secret Manager؛ ممنوع في الكود.
10.	حماية أدوات الإدارة (phpMyAdmin إن وُجد) خلف VPN/2FA.
B) قبل أي إطلاق/ترقية
1.	Migration مُراجَع + خطة رجوع.
2.	EXPLAIN للاستعلامات الحرجة + فهارس مطابقة.
3.	معاملات قصيرة + اختبارات سباق/قفل.
4.	بيانات Staging قريبة من الإنتاج (مموّهة) + اختبارات قبول.
5.	مراقبة لصيقة بعد الإطلاق (p95/p99, deadlocks, lag).
C) التعامل مع حادث أداء
1.	فحص الموارد/الاتصالات/النسخ/التأخير.
2.	استخراج Top slow queries + EXPLAIN.
3.	قرارات: فهرس/إعادة كتابة/Cache/Replica/تقسيم.
4.	توثيق السبب الجذري + متابعة بعد 7 أيام.
D) تغييرات سكيما دون توقف
1.	أضف الجديد كاختياري.
2.	تعبئة خلفية على دفعات.
3.	شغّل القراءة/الكتابة مزدوجين.
4.	أزل القديم لاحقًا.
5.	Online DDL للجداول الكبيرة.
E) أمن الوصول
1.	أقلّ صلاحية + فصل حسابات DDL عن RW.
2.	2FA + تدوير أسرار دوري.
3.	تدقيق (Audit) على العمليات الحساسة.
4.	اختبارات اختراق نصف سنوية على طبقة DB.
F) نسخ/تعافٍ (DR Drill)
1.	استعادة نسخة إلى بيئة معزولة كل ربع.
2.	قياس زمن الاستعادة ومقارنته بـRTO.
3.	تحقق من سلامة البيانات والفهارس.
4.	توثيق مُحدَّث لخطوات الاستعادة.
G) جودة بيانات شهرية
1.	dbt tests (NOT NULL/UNIQUE/FK).
2.	تقارير مفاتيح مكسورة/قيم خارج النطاق.
3.	مراجعة نمو الجداول ومعدلات التكرار.
4.	خطة تنظيف/أرشفة.
 
16) ملحقات سريعة (Cheat Sheets)
تسمية: جداول جمع snake_case (مثل order_items)، أعمدة snake_case، FK تنتهي بـ_id، تواريخ *_at، حالة status.
أعمدة قياسية: id, status, created_at, updated_at, created_by, updated_by, deleted_at, وبالجداول المعروضة slug, is_active, sort_order.
متى أستخدم JSON؟ عندما تكون البيانات اختيارية/متغيرة جدًا ولا تؤثر على استعلامات حرجة. وإلا: نمذجة طبيعية + فهارس.
متى أجزّئ (Partition)؟ جداول زمنية ضخمة (logs/notifications) + حاجة لأرشفة/تنظيف سريع.
متى أستخدم Replica؟ تقارير/قراءات كثيفة غير حرجة للاتساق الفوري؛ تجنّب “اقرأ بعد كتابة” عليها لمسارات حسّاسة.
 
17) قائمة Anti‑Patterns (تجنّبها دائمًا)
●	SELECT *، وLIKE مع بادئة %، وORDER BY RAND() على جداول كبيرة.
●	JSON/EAV بدل نمذجة سليمة لجداول أساسية.
●	ENUM لقيم متغيرة، وأعمدة نصية ضخمة بلا حاجة.
●	تغييرات DDL مباشرة على الإنتاج، أو بدون خطة رجوع.
●	صور/ملفات داخل DB، أو تشغيل تقارير ثقيلة على إنتاج.
●	حساب root للجميع، وأسرار داخل الكود، وغياب TLS/VPN.
●	نسخ بلا اختبارات استعادة، وغياب PITR.
●	تجاهل p95/p99, deadlocks, replication lag في المراقبة.
 
ختام عملي
●	التزم بهذه المعايير والقوائم وستُغطي >95% من فئات الأخطاء الشائعة.
●	أي استثناء يجب أن يُوثَّق بمبررات ومخاطر مخفَّفة.
 
العملاء (Customers) 
العملاء (Customers)
1) الهدف
●	توحيد هوية العميل (هاتف/إيميل/اسم) وربطها بعناوينه وأجهزته وسلوكه.
●	تمكين رسائل CRM ذكية (ترحيب، سلة مهجورة، استرجاع، VIP).
●	تحسين تجربة التوصيل وملف الدفع عند الاستلام (COD) وتقليل الرفض.
●	تجهيز بيانات واضحة للتحليلات والقرار التسويقي (LTV، RFM، الاحتفاظ).
2) النطاق (ما المطلوب بناؤه)
●	العملاء: سجل موحّد لكل عميل + مؤشرات تشغيلية أساسية (عدد الطلبات، آخر طلب، القيمة العمرية…).
●	العناوين: شحن/فوترة بدقة محلية (مدينة/حي/معلم قريب) مع عنوان افتراضي لكل عميل.
●	الأجهزة: ربط أجهزة التطبيق بالعميل + حفظ توكن الإشعارات وإصدار التطبيق .
●	الموافقات: إدارة موافقات القنوات (Push/SMS/WhatsApp/Email) واحترامها في أي إرسال   .
●	الشرائح: تعريف شرائح (VIP، غير نشط، مهجور سلة…) وعضوية العملاء فيها. 
●	ملف COD: حقول بسيطة لمخاطر COD (مسموح/محظور مؤقتًا/عدد محاولات فاشلة/درجة مخاطرة).  
●	سجل التواصل: أرشفة أي رسالة مرسلة للعميل (القناة، الحالة، الوقت) للمتابعة والامتثال. 
●	التحويلات التسويقية: حفظ أول وآخر مصدر تسويقي (source/medium/campaign) للفهم والقياس.  
●	دمج المكررات: آلية لتجميع حسابات مكررة لنفس العميل عند الحاجة.
●	(اختياري) رصيد متجر/بطاقات هدية + تذاكر دعم مرتبطة بالعميل. 
3) العلاقات الرئيسية
●	عميل ↔ عناوين: واحد إلى متعدد.
●	عميل ↔ أجهزة: واحد إلى متعدد.
●	عميل ↔ شرائح: متعدد إلى متعدد.
●	عميل ↔ سجل تواصل/تذاكر دعم: واحد إلى متعدد.
4) قواعد العمل الأساسية
●	الهاتف فريد وبصيغة دولية E.164، والتحقق عبر OTP.
●	عند توثيق الهاتف: ربط أي سلة/جهاز سابق بهذا العميل. 
●	عنوان الطلب لقطة ثابتة داخل الطلب (لا يُحدّث بأثر رجعي إذا غيّر العميل عنوانه لاحقًا).
●	COD: زيادة درجة المخاطرة عند عدم الرد/رفض الاستلام؛ إيقاف COD مؤقتًا عند تجاوز عتبة محددة.
●	احترام الموافقات: العميل الرافض لقناة معيّنة لا يُستهدف بها.
●	تحديث توكن الإشعارات والإصدار عند كل فتح للتطبيق.

5) تدفّقات تشغيل مختصرة
●	تسجيل/تعرّف عميل: يبدأ زائرًا (جهاز فقط) → يوثّق الهاتف → يصبح عميلًا معروفًا، وتُنقل له السلة والجهاز.
●	تحديث العنوان الافتراضي: عنوان واحد افتراضي دائمًا لكل عميل.
●	سلة مهجورة: اكتشاف سلال بلا شراء خلال 7 أيام → استهداف بإشعار/عرض مخصص. 
●	إدارة COD: رفع أو خفض مخاطر العميل بناءً على نتائج الشحن الفعلية.
6) مهام مجدولة (Jobs)
●	بناء الشرائح يوميًا (VIP، غير نشط، مهجور 7 أيام…).
●	تحديث مخاطر COD عند تغيّر حالات الشحن + مراجعة يومية.
●	فحص مكررات العملاء (نفس الهاتف/نفس الجهاز) ووضعها في طابور مراجعة.
7) تكاملات لازمة
●	ربط التطبيق بـ Firebase/GA4 وتعيين user_id = معرف العميل  .
●	إرسال أحداث أساسية: عرض منتج، إضافة للسلة، إكمال شراء، فتح جلسة…
●	استخدام FCM للإشعارات مع روابط عميقة (Deep Links) لفتح السلة/المنتج مباشرة.
8) التقارير والمؤشرات (الحد الأدنى)
●	RFM (حداثة آخر شراء، التكرار، الإنفاق).
●	LTV والقيمة المتوسطة للطلب.
●	معدلات الاحتفاظ (أسبوعي/شهري).  
●	معدلات فشل COD حسب المدينة/شركة الشحن.
●	حجم السلال المهجورة وقيمتها.
9) معايير قبول (يعتبر العمل مكتملًا إذا…)
●	إنشاء وتحديث عميل يعمل مع تحقق الهاتف وتوحيد الهوية.
●	عنوان افتراضي واحد فقط لكل عميل ويُستخدم تلقائيًا في الطلب.
●	الأجهزة مربوطة بالعميل وتُحدَّث معلوماتها وتوكِن الإشعارات باستمرار.
●	الشرائح تُبنى دوريًا ويمكن استهدافها في الحملات.  
●	الموافقات محترمة تلقائيًا في أي إرسال جماعي.
●	ملف COD يتأثر تلقائيًا بنتائج الشحن ويوقف COD عند العتبة.
●	تتوفر تقارير أساسية (RFM/LTV/Retention/COD) للاطلاع.


10) متطلبات جودة البيانات
●	توحيد أسماء المدن/الأحياء بقوائم مقيدة (لتحسين التوصيل والتقارير).
●	طوابع زمنية للإنشاء والتحديث بكل السجلات.
●	خصوصية: عدم إظهار بيانات حساسة لفِرق لا تحتاجها، وتقييد الوصول حسب الدور. 
 ملاحظات قصيرة;
●	ركّز على بساطة الجداول وقابلية التوسّع، ولا تربط التنفيذ بأداة محددة.
●	وفّر نقاط تكامل لاحقة مع الطلبات والسلال بدون كسر التصميم.
●	اجعل الهاتف هو المعرف العملي الأول، مع دعم الدمج عند اكتشاف تكرار. 
 
علامة التبويب 22 
توضيح لنقطة التحويلات ومعرفة من اين جاء العميل
1) الفكرة باختصار
●	First touch: أول قناة وصل منها المستخدم (نحفظها مرة واحدة ولا نبدّلها).
●	Last touch: آخر قناة “مؤهّلة” قبل التحويل (نحدّثها كل ما ظهرّت حملة/UTM جديدة).
●	قاعدة مهمّة: لا نسمح لمصدر direct / (none) أنه يكتب فوق مصدر سابق غير مباشر.
2) الحقول القياسية التي سنجمعها
●	utm_source, utm_medium, utm_campaign (+ اختياري: utm_term, utm_content)
●	معرفات الشبكات: gclid (Google Ads), fbclid (Meta), ttclid (TikTok) … إلخ
●	referrer_domain (مصدر الإحالة إن لم توجد UTM)
●	طابع زمني: first_touch_ts, last_touch_ts
●	قناة موحّدة (Mapping): channel_group (Organic Social, Paid Social, Paid Search, Referral, Direct…).
3) قواعد الإسناد (Recommended)
●	First touch: أوّل زيارة/تنصيب مع UTM/CLID/Referrer ≠ direct → تُحفظ 2 سنة.
●	Last touch: آخر زيارة فيها مصدر مؤهّل خلال نافذة 90 يوم.
●	Direct لا يكتب فوق آخر مصدر غير مباشر خلال 90 يوم.
●	Qualifying touch = وجود أي UTM/CLID أو referrer domain خارجي.
●	Cross-device: عند تسجيل الدخول، نربط first/last بالمستخدم (user_id) ونمنع الازدواجية.
 
4) التنفيذ على الويب (JavaScript)
أ) الالتقاط + التخزين المحلي
●	نحفظ First في Cookies طويلة (730 يوم).
●	نحفظ Last في Cookies 90 يوم، ونحدّثها فقط عند لمسة مؤهّلة.
●	عند عدم وجود UTM لكن في document.referrer دومين خارجي → source=referrer_domain, medium=referral, campaign=(referral).
مثال كود مختصر (مفهومياً):
<script>
function getParams() {
  const u = new URL(location.href);
  const qp = (k) => u.searchParams.get(k);
  const params = {
    utm_source: qp('utm_source'),
    utm_medium: qp('utm_medium'),
    utm_campaign: qp('utm_campaign'),
    gclid: qp('gclid'),
    fbclid: qp('fbclid'),
  };
  // Referrer fallback
  const ref = document.referrer;
  const refDomain = ref ? (new URL(ref)).hostname : '';
  const isDirect = !ref || refDomain === location.hostname;
  if (!params.utm_source && !params.gclid && !params.fbclid && !isDirect) {
    params.utm_source = refDomain;
    params.utm_medium = 'referral';
    params.utm_campaign = '(referral)';
  }
  return { ...params, refDomain };
}

function setCookie(n, v, days) {
  const d = new Date(); d.setTime(d.getTime() + (days*24*60*60*1000));
  document.cookie = `${n}=${encodeURIComponent(v||'')};path=/;expires=${d.toUTCString()};SameSite=Lax`;
}
function getCookie(n) {
  return document.cookie.split('; ').find(r => r.startsWith(n+'='))?.split('=')[1];
}
function hasQualifying(p){ return p.utm_source || p.gclid || p.fbclid; }

(function main(){
  const p = getParams(); if (!p) return;

  // FIRST
  if (!getCookie('ft_source') && hasQualifying(p)) {
    setCookie('ft_source', p.utm_source, 730);
    setCookie('ft_medium', p.utm_medium||'(none)', 730);
    setCookie('ft_campaign', p.utm_campaign||'(none)', 730);
    setCookie('first_touch_ts', Date.now(), 730);
  }

  // LAST (ignore "direct")
  if (hasQualifying(p)) {
    setCookie('lt_source', p.utm_source, 90);
    setCookie('lt_medium', p.utm_medium||'(none)', 90);
    setCookie('lt_campaign', p.utm_campaign||'(none)', 90);
    setCookie('last_touch_ts', Date.now(), 90);
  }
})();
</script>

ب) الإرسال إلى الخادم وGA4
●	عند Sign-Up وCheckout نرسل ft_* وlt_* مع الطلب.
●	في GA4 نضبط user_properties: first_source/medium/campaign (مرة واحدة) وlast_source/medium/campaign(يُحدّث عند كل جلسة مؤهّلة).
●	نُمرّر نفس القيم في حدث purchase.
 
5) التنفيذ على التطبيق (Flutter + Firebase)
أ) الالتقاط (Deferred Deep Links / Dynamic Links)
●	استخدم Firebase Dynamic Links لالتقاط UTM عند التنصيب والفتح.
●	Android: إن توفر Play Install Referrer (اختياري) لالتقاط مصدر التنصيب.
●	خزّن First في SharedPreferences عند أول فتح مؤهّل، وLast تُحدّث عند كل فتح برابط فيه UTM/CLID.
مثال Flutter (مختصر):
// pubspec.yaml: firebase_dynamic_links, shared_preferences, firebase_analytics

Future<Map<String,String>> _extractParams(PendingDynamicLinkData? data) async {
  final uri = data?.link;
  if (uri == null) return {};
  String q(String k)=> uri.queryParameters[k] ?? '';
  return {
    'utm_source': q('utm_source'),
    'utm_medium': q('utm_medium'),
    'utm_campaign': q('utm_campaign'),
    'gclid': q('gclid'),
    'fbclid': q('fbclid'),
  };
}

Future<void> initAttribution() async {
  final prefs = await SharedPreferences.getInstance();

  // Initial link (first open)
  final initData = await FirebaseDynamicLinks.instance.getInitialLink();
  var p = await _extractParams(initData);

  // First touch
  bool firstExists = prefs.containsKey('ft_source');
  bool qualifying = p.values.any((v) => v.isNotEmpty);
  if (!firstExists && qualifying) {
    await prefs.setString('ft_source', p['utm_source'] ?? '');
    await prefs.setString('ft_medium', p['utm_medium'] ?? '(none)');
    await prefs.setString('ft_campaign', p['utm_campaign'] ?? '(none)');
    await prefs.setInt('first_touch_ts', DateTime.now().millisecondsSinceEpoch);
  }

  // Last touch
  if (qualifying) {
    await prefs.setString('lt_source', p['utm_source'] ?? '');
    await prefs.setString('lt_medium', p['utm_medium'] ?? '(none)');
    await prefs.setString('lt_campaign', p['utm_campaign'] ?? '(none)');
    await prefs.setInt('last_touch_ts', DateTime.now().millisecondsSinceEpoch);
  }

  // Listen for future links (app in foreground)
  FirebaseDynamicLinks.instance.onLink.listen((d) async {
    final p2 = await _extractParams(d);
    final q2 = p2.values.any((v)=>v.isNotEmpty);
    if (q2) {
      await prefs.setString('lt_source', p2['utm_source'] ?? '');
      await prefs.setString('lt_medium', p2['utm_medium'] ?? '(none)');
      await prefs.setString('lt_campaign', p2['utm_campaign'] ?? '(none)');
      await prefs.setInt('last_touch_ts', DateTime.now().millisecondsSinceEpoch);
    }
  });
}

ب) إرسالها لــ Firebase Analytics + الخادم
final analytics = FirebaseAnalytics.instance;
Future<void> setUserPropsFromPrefs() async {
  final p = await SharedPreferences.getInstance();
  // set once
  if (p.containsKey('ft_source')) {
    analytics.setUserProperty(name: 'first_source', value: p.getString('ft_source'));
    analytics.setUserProperty(name: 'first_medium', value: p.getString('ft_medium'));
    analytics.setUserProperty(name: 'first_campaign', value: p.getString('ft_campaign'));
  }
  // update-able
  if (p.containsKey('lt_source')) {
    analytics.setUserProperty(name: 'last_source', value: p.getString('lt_source'));
    analytics.setUserProperty(name: 'last_medium', value: p.getString('lt_medium'));
    analytics.setUserProperty(name: 'last_campaign', value: p.getString('lt_campaign'));
  }
}

وعند الشراء:
await analytics.logEvent(
  name: 'purchase',
  parameters: {
    'value': orderTotal,
    'currency': 'YER',
    'first_source': p.getString('ft_source'),
    'first_medium': p.getString('ft_medium'),
    'first_campaign': p.getString('ft_campaign'),
    'last_source': p.getString('lt_source'),
    'last_medium': p.getString('lt_medium'),
    'last_campaign': p.getString('lt_campaign'),
  },
);
// وأرسل نفس الحقول إلى API إنشاء الطلب لتخزينها في الـDB

 
6) الخادم وقاعدة البيانات (مهم جدًا)
أ) في جدول المستخدمين users
●	first_source, first_medium, first_campaign, first_touch_ts
●	last_source, last_medium, last_campaign, last_touch_ts
●	channel_group_first, channel_group_last
نحدّث حقول first لأول مرة فقط.
نحدّث last عند كل جلسة مؤهّلة أو قبل إنشاء الطلب.
ب) في جدول الطلبات orders
●	order_id, user_id, order_ts, value
●	حقول الإسناد المجلوبة وقت الشراء:
○	first_source/medium/campaign
○	last_source/medium/campaign
○	session_source/medium/campaign (اللمسة الحالية إن وُجدت)
○	channel_group_first, channel_group_last, channel_group_session
بهذه الطريقة تقدر تعمل تقارير عبر الزمن بدون الاعتماد فقط على GA4.
 
7) GA4 & BigQuery (تقارير)
●	في GA4: أنشئ Dimensions مخصّصة من user_properties و event parameters (first_, last_, session_*).
●	في BigQuery: ابنِ جدول أبعاد للمستخدم dim_users من أحدث user_properties، وجدول حقائق fact_orders من الـDB أو من purchase events.
استعلام BQ مثال (استخراج user_props من GA4 export):
WITH users AS (
  SELECT
    user_pseudo_id,
    MAX(IF(ukey = 'first_source', uval, NULL)) AS first_source,
    MAX(IF(ukey = 'first_medium', uval, NULL)) AS first_medium,
    MAX(IF(ukey = 'first_campaign', uval, NULL)) AS first_campaign,
    MAX(IF(ukey = 'last_source', uval, NULL))  AS last_source,
    MAX(IF(ukey = 'last_medium', uval, NULL))  AS last_medium,
    MAX(IF(ukey = 'last_campaign', uval, NULL))AS last_campaign
  FROM (
    SELECT
      user_pseudo_id,
      up.key AS ukey,
      COALESCE(up.value.string_value, CAST(up.value.int_value AS STRING)) AS uval
    FROM `project.dataset.events_*`,
    UNNEST(user_properties) up
  )
  GROUP BY user_pseudo_id
)
SELECT * FROM users;

 
8) توحيد القنوات (Channel Grouping)
ابنِ دالة Mapping بسيطة حسب source/medium/clid:
●	إذا gclid → Paid Search (Google Ads)
●	إذا fbclid أو utm_source in (facebook, instagram, meta) → Paid Social
●	إذا utm_medium=organic_social → Organic Social
●	referral → Referral
●	بدون أي شيء ومع referrer فارغ → Direct
خزّن channel_group_first/last/session في نفس الوقت.
 
9) حالات خاصة يجب تغطيتها
●	WhatsApp / Telegram: غالبًا referrer مفقود → استخدم روابط UTM للمنشورات والبايو والبنرات داخل التطبيق.
●	المكالمات/الطلبات الهاتفية (COD): أعطِ الفريق حقلاً attribution_code يربط الإحالة بالطلب.
●	Internal traffic: استبعد دوميناتك من الإحالات.
●	Cross-device: عند تسجيل الدخول اربط السجلات بـ user_id وقم بمزامنة first/last إلى حساب المستخدم مرّة واحدة.
 
10) اختبار وضمان الجودة (QA)
●	سيناريوهات:
1.	دخول عبر Google Ads → تسجيل → شراء: يجب أن تكون first=google/cpc/… وlast=google/cpc/…
2.	دخول Organic Search ثم بعد أسبوع دخول Instagram Ads ثم شراء: first=organic، last=paid social.
3.	دخول via campaign ثم عودة Direct فقط: لا يُسمح لـ Direct أن يكتب فوق last خلال 90 يوم.
●	راقب نسب Direct بعد الإطلاق (يجب أن تنخفض إن كان الالتقاط صحيحًا).
●	قارن الحساب بين orders DB وGA4 يوميًا.
 
11) قائمة تنفيذ سريعة (Checklist)
1.	ويب: كود التقاط UTM+Referrer + Cookies (First/Last) + إرسالها للـAPI وGA4.
2.	تطبيق: Dynamic Links + حفظ First/Last في SharedPreferences + user_properties + تمريرها في purchase.
3.	خادم: حقول في users وorders + منطق عدم الكتابة فوق First وعدم السماح لـ Direct بالكتابة فوق Last.
4.	Channel mapping: دالة موحّدة.
5.	GA4: إنشاء أبعاد مخصّصة من user_properties وEvent params.
6.	BigQuery: بناء جداول dim/fact والاستعلامات.
7.	QA: سيناريوهات، لوحات مراقبة، مقارنة يومية.
 
علامة التبويب 23 
توضيح  ل ربط كل جهاز بعميل معيّن وتخزين توكن الإشعارات (FCM token) وإصدار التطبيق مع بيانات الجهاز بشكل منظّم وآمن، بحيث:
●	نقدر نرسل إشعارات دقيقة (طلبات، عروض، استرجاع سلة…).
●	نراقب الإصدارات ونفرض التحديثات الحرجة عند الحاجة.
●	نتعامل مع تغيّر التوكن تلقائياً وننظّف التوكنات المعطوبة.
1) نموذج البيانات في قاعدة البيانات
جدول devices
●	device_id (UUID, PK)
●	user_id (FK nullable) — يرتبط عند تسجيل الدخول
●	fid (Firebase Installation ID, unique nullable)
●	fcm_token (string, unique index)
●	platform (enum: android/ios)
●	device_model (e.g., “iPhone15,2” أو “SM-A546E”)
●	os_version (e.g., “iOS 17.5”, “Android 14”)
●	app_version_name (e.g., “2.7.3”)
●	app_build_number (int, لفرض الحد الأدنى للإصدار)
●	lang (ISO, مثل ar, en)
●	tz_offset_minutes (int) فرق التوقيت
●	push_permission (bool) هل المستخدم أعطى إذن الإشعارات
●	marketing_opt_in (bool) موافقة تسويقية (اختياري)
●	is_primary (bool) جهاز المستخدم الرئيسي (اختياري)
●	token_status (enum: active/invalid/expired)
●	first_seen_ts (datetime)
●	last_seen_ts (datetime)
●	last_push_sent_ts (datetime, اختياري)
●	last_push_result (string, اختياري)
فهارس مهمّة:
(user_id), (fcm_token UNIQUE), (fid UNIQUE), (last_seen_ts)
جدول أحداث اختياري device_events
●	device_id, event (token_refresh, login, logout, push_failed_unregistered, app_open, update)
●	ts, meta (JSON)
2) تدفّق العمل (Lifecycle)
1.	التثبيت/الفتح الأول: التطبيق يجمع fid, fcm_token, بيانات الجهاز/الإصدار ويرسل Register.
2.	تسجيل الدخول: استدعاء Associate لربط device_id مع user_id.
3.	تحديث التوكن: عند تغيّر FCM token يستدعي Token Refresh (Patch).
4.	نبضة حياة (Heartbeat): عند كل فتح (وأحياناً دوريًا) يحدّث last_seen وapp_version وpush_permission.
5.	تسجيل الخروج: Dissociate (نفصل user_id عن الجهاز لكن نحتفظ بالتوكن لو أردنا إشعارات عامة).
6.	إرسال الإشعار: السيرفر يرسل للتوكنات الفعّالة؛ لو رجع FCM بخطأ NotRegistered نعلّم التوكن invalid ونوقّفه.
3) واجهات الـAPI (مقترحة)
جميعها خلف Auth مناسبة (JWT أو Firebase Auth) + معدل الطلبات (Rate limit).
POST /v1/devices/register
Request
{
  "fid": "abc123...", 
  "fcm_token": "fcm_token_here",
  "platform": "android",
  "device_model": "SM-A546E",
  "os_version": "Android 14",
  "app_version_name": "2.7.3",
  "app_build_number": 20703,
  "lang": "ar",
  "tz_offset_minutes": 180,
  "push_permission": true,
  "marketing_opt_in": false
}

Response
{ "device_id": "b2f0b3f6-...", "token_status": "active" }

Upsert بالاعتماد على fid أو fcm_token. حدّث السجلات بدل تكرارها.
POST /v1/devices/associate
يربط الجهاز بالمستخدم (يُستدعى بعد تسجيل الدخول).
{ "device_id": "b2f0b3f6-...", "user_id": "U12345" }

POST /v1/devices/dissociate
عند تسجيل الخروج:
{ "device_id": "b2f0b3f6-..." }

PATCH /v1/devices/token
عند تحديث التوكن:
{ "device_id": "b2f0b3f6-...", "fcm_token": "new_token_here" }

POST /v1/devices/heartbeat
تحديث دوري/عند الفتح:
{
  "device_id": "b2f0b3f6-...",
  "app_version_name": "2.8.0",
  "app_build_number": 20800,
  "push_permission": true
}

4) تطبيق Flutter (عملي)
الحِزم
●	firebase_core, firebase_messaging
●	package_info_plus (الإصدار/الـbuild)
●	device_info_plus (موديل/OS)
●	(اختياري) firebase_auth لو كنت تعتمد توثيق Firebase
التهيئة + التسجيل الأول
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'dart:io';

Future<void> initPushAndDevice() async {
  await Firebase.initializeApp();

  // iOS: طلب الإذن – Android 13+ أيضاً يحتاج POST_NOTIFICATIONS
  final settings = await FirebaseMessaging.instance.requestPermission(
    alert: true, badge: true, sound: true,
  );
  final pushPermission = settings.authorizationStatus == AuthorizationStatus.authorized ||
                         settings.authorizationStatus == AuthorizationStatus.provisional;

  final fcm = FirebaseMessaging.instance;
  final token = await fcm.getToken(); // قد تكون null لو لم يُمنح الإذن
  final fid = await fcm.getToken(vapidKey: null); // بديل غير دقيق؛ الأفضل استخدام FIS عبر native، لكن نكتفي بالتوكن كمُعرّف
  final pkg = await PackageInfo.fromPlatform();

  final deviceInfo = DeviceInfoPlugin();
  String model, osVer, platform;
  if (Platform.isAndroid) {
    final a = await deviceInfo.androidInfo;
    model = "${a.manufacturer} ${a.model}";
    osVer = "Android ${a.version.release}";
    platform = "android";
  } else {
    final i = await deviceInfo.iosInfo;
    model = i.utsname.machine ?? "iPhone";
    osVer = "iOS ${i.systemVersion}";
    platform = "ios";
  }

  // نادى API register
  await apiPost('/v1/devices/register', {
    "fid": null, // إن توفر لديك طريقة للحصول على FID أصلي أرسله، وإلا اتركه null
    "fcm_token": token,
    "platform": platform,
    "device_model": model,
    "os_version": osVer,
    "app_version_name": pkg.version,
    "app_build_number": int.tryParse(pkg.buildNumber) ?? 0,
    "lang": Platform.localeName.split('_').first,
    "tz_offset_minutes": DateTime.now().timeZoneOffset.inMinutes,
    "push_permission": pushPermission,
    "marketing_opt_in": false
  });

  // استمع لتحديثات التوكن
  FirebaseMessaging.instance.onTokenRefresh.listen((newToken) async {
    await apiPatch('/v1/devices/token', {
      "device_id": await currentDeviceId(), // خزّنه بعد register
      "fcm_token": newToken
    });
  });
}

عند تسجيل الدخول/الخروج
Future<void> onLogin(String userId) async {
  await apiPost('/v1/devices/associate', {
    "device_id": await currentDeviceId(),
    "user_id": userId
  });
}

Future<void> onLogout() async {
  await apiPost('/v1/devices/dissociate', {
    "device_id": await currentDeviceId()
  });
}

نبضة حياة عند الفتح
Future<void> heartbeat() async {
  final pkg = await PackageInfo.fromPlatform();
  await apiPost('/v1/devices/heartbeat', {
    "device_id": await currentDeviceId(),
    "app_version_name": pkg.version,
    "app_build_number": int.tryParse(pkg.buildNumber) ?? 0,
    "push_permission": await hasPushPermission()
  });
}

ملاحظات:
●	Android 13+ يتطلب إذن الإشعارات Runtime — تأكد من إضافته في Manifest وطلبه.
●	توكِن FCM قد يتغيّر في أي وقت: الاستماع لـ onTokenRefresh ضروري.
●	لو رفض الإذن، خزِّن push_permission=false لتجنب إرسال إشعار فاشل.
5) الإرسال من السيرفر + تنظيف التوكنات
(مثال TypeScript مع Firebase Admin)
import { getMessaging } from 'firebase-admin/messaging';

async function sendToUser(userId: string, payload: any) {
  const tokens = await db.tokens.findActiveByUser(userId); // رجّع قائمة FCM tokens
  if (!tokens.length) return;

  const res = await getMessaging().sendEachForMulticast({
    tokens,
    notification: { title: payload.title, body: payload.body },
    data: payload.data ?? {}
  });

  // نظّف التوكنات غير الصالحة
  res.responses.forEach((r, idx) => {
    if (!r.success) {
      const err = r.error?.code;
      if (err === 'messaging/registration-token-not-registered' ||
          err === 'messaging/invalid-registration-token') {
        db.tokens.markInvalid(tokens[idx]); // token_status=invalid
      }
    }
  });
}

●	استخدم سياسة إعادة المحاولة (Exponential backoff) عند quotaExceeded أو internal.
●	حدّس last_push_sent_ts وlast_push_result.
6) السياسات والقواعد
●	تعدّد الأجهزة: اسمح بعدة أجهزة لكل مستخدم. أرسل إشعار الطلب لكل الأجهزة الفعّالة.
●	الخصوصية: لا تحفظ معرّفات إعلانية حسّاسة (IDFA) بدون موافقة. fid وfcm_token كافيان.
●	الأمن: اربط كل استدعاء Device بــ JWT للمستخدم إن وُجد، أو توكن ضيف (Guest) قصير العمر.
●	الحد الأدنى للإصدار: احتفِظ بإعداد مركزي min_supported_build. في كل Heartbeat أو عند أي طلب API، إن كان app_build_number < min_supported_build أرجِع 426 (Upgrade Required) مع رابط المتجر.
●	الاختيارات التسويقية: احترم marketing_opt_in، واستخدم Topics اختيارية (مثل promos, new_arrivals) للمشتركين فقط.
7) اختبار (QA) سريع
●	تثبيت جديد → Register يتم إنجاحه والتوكن محفوظ.
●	رفض الإذن ثم منحه لاحقاً → push_permission يتحدث وonTokenRefresh يشتغل.
●	دخول من جهازين لنفس الحساب → كلاهما يستلم إشعار حالة الطلب.
●	حذف التطبيق/إعادة تثبيت → إرسال إشعار يجب أن يرجع NotRegistered للتوكن القديم ويتم تنظيفه.
●	تحديث إصدار التطبيق → app_version يتحدث في heartbeat.
●	تسجيل خروج → الجهاز ينفصل عن user_id لكن يبقى صالح لإشعارات عامّة (إن رغبت).
 
علامة التبويب 24 
إدارة موافقات القنوات (Push / SMS / WhatsApp / Email)     حسب الغرض (Transactional / Marketing / …) واحترامها قبل أي إرسال. دعم المواضيع (Topics) اختياريًا، وسجل تدقيقي كامل، والتكامل مع جدول الأجهزة (push_permission).
 
1) التعاريف (Definitions)
●	Channel: قناة الإرسال (push, sms, whatsapp, email).
●	Purpose: الغرض من الرسالة (transactional, marketing, survey, security).
●	Topic (اختياري): تصنيف تسويقي دقيق (promos, new_arrivals, …).
●	Status: حالة الموافقة (granted, denied, revoked).
●	Evidence: دليل جمع الموافقة (IP, device_id, النص الظاهر للموافقة، timestamp).
 
2) مخطط البيانات (DDL)
ملاحظة: غيّر أسماء الجداول/المخططات حسب اصطلاحاتك، وثبّت ترميز utf8mb4.
-- 2.1 بيانات تواصل المستخدم (للتحقق قبل الإرسال)
CREATE TABLE user_contacts (
  user_id            BIGINT NOT NULL,
  email              VARCHAR(255),
  email_verified     TINYINT(1) NOT NULL DEFAULT 0,
  email_verified_at  DATETIME NULL,
  phone_e164         VARCHAR(32),            -- +9677xxxxxx
  phone_verified     TINYINT(1) NOT NULL DEFAULT 0,
  phone_verified_at  DATETIME NULL,
  wa_phone_e164      VARCHAR(32) NULL,       -- إن كان رقم واتساب مختلفاً
  created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  UNIQUE KEY uq_contacts_email (email),
  UNIQUE KEY uq_contacts_phone (phone_e164),
  UNIQUE KEY uq_contacts_wa_phone (wa_phone_e164)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2.2 الموافقات الحالية (Effective)
CREATE TABLE user_consents (
  user_id        BIGINT NOT NULL,
  channel        ENUM('push','sms','whatsapp','email') NOT NULL,
  purpose        ENUM('transactional','marketing','survey','security') NOT NULL,
  topic          VARCHAR(64) NULL,   -- NULL = موافقة عامة على الغرض في القناة
  status         ENUM('granted','denied','revoked') NOT NULL,
  source         ENUM('app_checkbox','profile_center','checkout_optin','wa_click_to_chat',
                      'sms_keyword','email_unsubscribe_link','cs_agent','system') NOT NULL,
  evidence       JSON NULL,          -- {ip, device_id, user_agent, text, ts}
  language       CHAR(2) NULL,       -- ar / en
  jurisdiction   VARCHAR(32) NULL,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, channel, purpose, topic),
  KEY idx_consents_user (user_id),
  KEY idx_consents_channel (channel),
  KEY idx_consents_updated (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2.3 سجل تغيّر الموافقات (Audit)
CREATE TABLE user_consent_history (
  id            BIGINT NOT NULL AUTO_INCREMENT,
  user_id       BIGINT NOT NULL,
  channel       ENUM('push','sms','whatsapp','email') NOT NULL,
  purpose       ENUM('transactional','marketing','survey','security') NOT NULL,
  topic         VARCHAR(64) NULL,
  prev_status   ENUM('granted','denied','revoked') NULL,
  new_status    ENUM('granted','denied','revoked') NOT NULL,
  source        ENUM('app_checkbox','profile_center','checkout_optin','wa_click_to_chat',
                     'sms_keyword','email_unsubscribe_link','cs_agent','system') NOT NULL,
  evidence      JSON NULL,
  changed_by    ENUM('user','system','agent') NOT NULL,
  changed_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_hist_user (user_id),
  KEY idx_hist_changed (changed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2.4 تكامل مع الأجهزة (من مواصفة الأجهزة لديك)
-- نضمن وجود push_permission وإصدار التطبيق لإحترام دفع الإشعارات
-- مثال مبسّط للحقلين الأساسيين (جداولك قد تكون أوسع):
-- ALTER TABLE devices ADD COLUMN push_permission TINYINT(1) NOT NULL DEFAULT 0;
-- ALTER TABLE devices ADD COLUMN app_build_number INT NOT NULL DEFAULT 0;
-- فهارسك موجودة مسبقًا (user_id, fcm_token, fid, last_seen_ts ...)

ملاحظات معايير:
●	المفتاح المركّب في user_consents يسمح بموافقة عامة (topic=NULL) وأخرى موضوعية (topic='promos').
●	استخدم JSON في evidence لتخزين تفاصيل قابلة للتوسّع دون تغيير المخطط.
●	جميع الجداول تحمل طوابع زمنية، مع فهارس على updated_at و/أو changed_at لسهولة التقارير.
 
3) سياسات افتراضية (Defaults)
●	افتراضيًا:
1.	Transactional عبر كل قناة = granted (ما لم يلغِ المستخدم قناة بعينها).
2.	Marketing لكل قناة = denied حتى opt-in صريح.
●	Push يتطلب شرطين معًا للإرسال:
1.	موافقة تسويقية/خدمية حسب الرسالة في user_consents.
2.	إذن نظام/جهاز: devices.push_permission = 1 + توكن صالح.
 
4) عمليات الكتابة (Upsert) وأمثلة SQL
4.1 قراءة مصفوفة الموافقات للمستخدم
SELECT channel, purpose, topic, status, source, language, updated_at
FROM user_consents
WHERE user_id = ?;

4.2 Upsert موافقة (عام/Topic)
تطبيقياً: سجّل تغييرًا في user_consent_history قبل أو بعد الـUpsert (اختر نهجًا واحدًا وثبّته).
-- مثال: منح Email Marketing عام (بدون topic)
INSERT INTO user_consents (user_id, channel, purpose, topic, status, source, evidence, language)
VALUES (?, 'email', 'marketing', NULL, 'granted', 'profile_center',
        JSON_OBJECT('ip', ?, 'text', 'I agree to receive marketing emails', 'ts', NOW()), 'ar')
ON DUPLICATE KEY UPDATE
  status = VALUES(status),
  source = VALUES(source),
  evidence = VALUES(evidence),
  language = VALUES(language),
  updated_at = CURRENT_TIMESTAMP;

-- سجل تاريخ:
INSERT INTO user_consent_history (user_id, channel, purpose, topic, prev_status, new_status, source, evidence, changed_by)
VALUES (?, 'email', 'marketing', NULL, ?, 'granted', 'profile_center',
        JSON_OBJECT('ip', ?, 'screen', 'preference_center'), 'user');

4.3 إلغاء اشتراك (Unsubscribe)
-- إلغاء Email Marketing:
INSERT INTO user_consents (user_id, channel, purpose, topic, status, source, evidence)
VALUES (?, 'email', 'marketing', NULL, 'revoked', 'email_unsubscribe_link',
        JSON_OBJECT('reason', 'unsubscribe_link', 'ts', NOW()))
ON DUPLICATE KEY UPDATE
  status     = 'revoked',
  source     = VALUES(source),
  evidence   = VALUES(evidence),
  updated_at = CURRENT_TIMESTAMP;

INSERT INTO user_consent_history (...)
VALUES (..., /* prev_status */ ?, 'revoked', 'email_unsubscribe_link', JSON_OBJECT('message_id', ?), 'user');

 
5) خوارزمية قرار الإرسال (Eligibility)
المدخلات: user_id, channel, message_type (transactional|marketing), topic (اختياري).
المخرجات: allowed (bool), reason (نص قصير).
5.1 قواعد عامة
●	Transactional:
○	مطلوب موافقة القناة نفسها ≠ denied/revoked + وسيلة الاتصال مُتحقَّقة (email_verified/phone_verified).
○	Push: يشترط devices.push_permission=1 وتوكن صالح.
●	Marketing:
○	يشترط status='granted' لنفس القناة والغرض.
○	إن وُجد Topic محدّد: تحترم موافقة الـTopic إن كانت موجودة؛ وإلا تسقط على الموافقة العامة للقناة/الغرض (topic=NULL).
○	لا “Fallback” لقناة أخرى إذا قناة معيّنة مرفوضة (احترام نية المستخدم).
●	قيود تشغيلية: ساعات هادئة، وحدّ التكرار (Frequency Caps)، وتهيئة حد أدنى للإصدار (للـPush إن رغبت).
5.2 Pseudo-code (على الخادم)
function can_send(user_id, channel, msg_type, topic):
  consents = SELECT * FROM user_consents WHERE user_id=? AND channel=?;
  contacts = SELECT * FROM user_contacts WHERE user_id=?;

  if msg_type == 'transactional':
    if channel in ('sms','whatsapp'):
      if channel == 'sms' and contacts.phone_verified == 0: return (false, 'phone_not_verified')
      if channel == 'whatsapp' and (contacts.wa_phone_e164 is null or contacts.phone_verified == 0): 
         return (false, 'wa_not_verified')
    if channel == 'email' and contacts.email_verified == 0: return (false, 'email_not_verified')
    if channel == 'push':
      if NOT exists valid device with push_permission=1 and valid token: return (false, 'push_permission_denied')

    st = effective_status(consents, channel, 'transactional', topic)
    if st in ('denied', 'revoked'): return (false, 'consent_denied')
    return (true, 'ok')

  else if msg_type == 'marketing':
    st = effective_status(consents, channel, 'marketing', topic)
    if st != 'granted': return (false, 'marketing_not_opted_in')
    -- اختياري: تحقق ساعات هادئة وحدود التكرار هنا
    if violates_frequency_caps(user_id, channel): return (false, 'frequency_cap')
    if channel == 'push' and NOT exists valid push device: return (false, 'push_permission_denied')
    if channel == 'email' and contacts.email_verified == 0: return (false, 'email_not_verified')
    if channel in ('sms','whatsapp') and contacts.phone_verified == 0: return (false, 'phone_not_verified')
    return (true, 'ok')

function effective_status(consents, channel, purpose, topic):
  -- أولوية: موافقة topic المحدّد ثم العامة (topic IS NULL)
  row = consents.find(c => c.purpose==purpose && c.topic==topic) 
        || consents.find(c => c.purpose==purpose && c.topic is null)
  if row exists: return row.status else:
    -- افتراضات: transactional=granted, marketing=denied (قابلة للتهيئة)
    return (purpose=='transactional') ? 'granted' : 'denied'

 
6) دمج القنوات (Integrations)
6.1 WhatsApp
●	ممنوع إرسال outbound تسويقي بدون opt-in قابل للإثبات.
●	خزّن نص الموافقة في evidence (مثلاً: “أوافق على استلام رسائل واتساب من زهراء…”).
●	Webhook لإشعارات STOP/الغاء من المستخدم → تحدّث user_consents إلى revoked.
6.2 SMS
●	دعم كلمات مفاتيح: STOP, UNSUB, الغاء, CANCEL, START, موافقة.
●	كل حدث Keyword يُسجّل في user_consent_history ويحدّث user_consents.
6.3 Email
●	Unsubscribe link لكل رسالة تسويقية + ترويسة List-Unsubscribe إن أمكن.
●	Webhook لمزوّد البريد لتحديث revoked عند الإلغاء.
6.4 Push
●	يعتمد على موافقة القناة + إذن الجهاز (من جدول devices).
●	لا ترسل Marketing إن كان push_permission=0 حتى لو status='granted' في user_consents.
 
7) سجل الإرسال (للتدقيق والتقارير)
يوصى بجدول خفيف لتوثيق قرار الإرسال ونتيجته.
CREATE TABLE message_deliveries (
  id                BIGINT NOT NULL AUTO_INCREMENT,
  user_id           BIGINT NOT NULL,
  channel           ENUM('push','sms','whatsapp','email') NOT NULL,
  message_type      ENUM('transactional','marketing','survey','security') NOT NULL,
  topic             VARCHAR(64) NULL,
  decision_allowed  TINYINT(1) NOT NULL,
  decision_reason   VARCHAR(64) NOT NULL,
  provider_message_id VARCHAR(128) NULL,
  provider_code     VARCHAR(64) NULL,      -- NOT_REGISTERED, UNSUBSCRIBED, ...
  send_status       ENUM('queued','sent','failed','skipped') NOT NULL,
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_deliveries_user (user_id),
  KEY idx_deliveries_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

عند الإرسال: خزّن لقطة قرار (decision_allowed/reason) ونتيجة المزوّد.
عند أخطاء مثل UNSUBSCRIBED أو NOT_REGISTERED: حدّث user_consents أو devices.token_status فورًا.
 
8) تدفّقات العمل (Flows) مختصرة
8.1 جمع موافقة Marketing عبر مركز التفضيلات
1.	المستخدم يفعّل خيار القناة (Checkbox).
2.	الخادم:
○	يكتب في user_consents (Upsert).
○	يضيف سجلًا في user_consent_history.
3.	الواجهة تحدّث الحالة بصريًا.
8.2 إلغاء اشتراك Email عبر الرابط
1.	المستخدم يضغط Unsubscribe.
2.	Webhook → تحديث user_consents إلى revoked + سجل في user_consent_history.
3.	أي إرسال لاحق عبر Email/Marketing يُمنع.
8.3 إرسال رسالة
1.	خدمة الإرسال تستدعي can_send(...).
2.	لو allowed=false: تسجّل message_deliveries بـ skipped.
3.	لو allowed=true: ترسل للمزوّد، ثم تحدّث message_deliveries بنتيجة الإرسال.
4.	معالجة الأخطاء: تحديث consent/device عند الحاجة.
 
9) الفهارس والأداء (Indexes & Perf)
●	user_consents: مفتاح مركّب PK + فهرس على updated_at لتقاطعات التقارير.
●	user_consent_history: فهارس على (user_id) و (changed_at) لقراءة سريعة للتدقيق.
●	message_deliveries: فهرس زمني (created_at) للتقارير الدورية.
●	اجعل عمليات الإرسال Bulk-safe (دفعات) مع Exponential Backoff عند أخطاء الحصة.
 
10) الأمان والخصوصية
●	لا تُخزّن بيانات حسّاسة أكثر من اللازم في evidence.
●	كل تغيّر موافقة يجب أن يكون قابلًا للإثبات (من/إلى، ومتى، وكيف).
●	احترم اللغة (AR/EN) عند نصوص الموافقة لتطابق ما رآه المستخدم.
 
11) اختبارات (QA) أساسية
●	Email Marketing revoked ⇒ أي إرسال Email/Marketing → can_send = false.
●	Push permission = 0 رغم موافقة push/marketing=granted ⇒ منع الإرسال التسويقي عبر Push.
●	SMS START/STOP تحدّث user_consents آنيًا.
●	Topic-specific: granted على topic='promos' فقط ⇒ إرسال new_arrivals يُمنع.
●	Transactional مع قناة غير موثّقة (email_verified=0) ⇒ منع وإرجاع سبب واضح.
 
12) قابلية التوسّع (Migration Notes)
●	إضافة قناة جديدة: أضف قيمة إلى ENUMs أو بدّلها إلى جداول مرجعية (channels, purposes) إن رغبت.
●	إضافة Topic جديد: لا لزوم لتغيير المخطط (حقل topic حر).
●	نقل الافتراضات إلى جدول إعدادات (config) إن أردت تخصيص defaults لكل قناة/غرض.
 
13) تنفيذ
1.	إنشاء الجداول الثلاثة + (اختياري) message_deliveries.
2.	ربط مركز التفضيلات UI بــ Endpoints: GET/PUT consents.
3.	وصل Webhooks: email unsubscribe, SMS keywords, WhatsApp opt-in/out.
4.	تنفيذ خدمة can_send(...) واحترامها في كل مسارات الإرسال.
5.	احترام devices.push_permission وfcm_token الصالح للـPush.
6.	إضافة مراقبة (Dashboards): نسب opt-in، معدلات Unsub، أسباب الحجب، أثر الموافقات على الإيراد.
7.	تغطية اختبارات QA المذكورة.
 
علامة التبويب 25 
الشرائح: تعريف شرائح (VIP، غير نشط، مهجور سلة…) وعضوية العملاء فيها.، آلية احتسابها وتخزينها، وقواعد دخول/خروج العميل من كل شريحة بصورة حتمية وقابلة للتدقيق. تُستخدم لاحقًا في الاستهداف، مع احترام الموافقات (consents) عند الإرسال.
 
1) القاموس (Taxonomy) والتعاريف
القيم الزمنية قابلة للتهيئة في جدول إعدادات، الافتراضات أدناه عملية لتجارة أزياء مع دفع عند الاستلام.
A) شرائح دورة الحياة (Lifecycle) — متنافية داخل المجموعة
●	NEW_7D: أول شراء خلال آخر 7 أيام.
●	ACTIVE_30D: آخر شراء خلال آخر 30 يومًا.
●	DORMANT_31_90D: لا يوجد شراء منذ 31–90 يومًا.
●	CHURN_RISK_91_180D: لا يوجد شراء منذ 91–180 يومًا.
●	LOST_180P: لا يوجد شراء منذ >180 يومًا.
B) قيمة العميل (Value)
●	VIP: أعلى 5% من إجمالي الإيراد طيلة العمر أو (≥ 5 طلبات & AOV ≥ P90 آخر 90 يومًا).
●	HIGH_VALUE_NEW: أول طلب بقيمة ≥ P90 من أول طلبات آخر 90 يومًا.
C) السلوك داخل الجلسة/القُمع (Behavioral)
●	CART_ABANDONER_24H: أضاف للسلة ولم يتم الشراء خلال 1–24 ساعة من آخر إضافة.
●	CHECKOUT_ABANDONER_6H: بدأ الدفع ولم يكمل خلال 15 دقيقة–6 ساعات.
●	BROWSE_ABANDONER_24H: ≥3 عرض منتج/تصنيف خلال 24 ساعة دون إضافة سلة.
D) الجودة/المخاطر
●	HIGH_RETURN_RATE: نسبة المرتجعات ≥ 30% خلال 90 يومًا و≥3 طلبات.
●	COD_RISK_HIGH: درجة مخاطرة COD ≥ 0.8 (من نموذجك)، أو ≥2 رفض استلام آخر 90 يومًا.
●	COUPON_HUNTER: ≥70% من الطلبات بخصم خلال 180 يومًا و≥3 طلبات.
ملاحظة: يمكن لعميل أن يكون في عدة شرائح بالتوازي، عدا مجموعة دورة الحياة فهي متنافية ويُختار منها واحدة وفق الأسبقية.
أولوية عرض “الشريحة الأساسية (primary)”
1.	VIP
2.	CHURN_RISK / LOST
3.	ACTIVE / NEW
4.	Abandoners (Cart/Checkout)
5.	باقي الشرائح
 
2) مخطط الجداول (DDL)
-- 2.1 قاموس الشرائح
CREATE TABLE segment_catalog (
  segment_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
  code             VARCHAR(64) NOT NULL UNIQUE,   -- مثال: VIP, CART_ABANDONER_24H
  name_ar          VARCHAR(128) NOT NULL,
  name_en          VARCHAR(128) NOT NULL,
  group_code       ENUM('lifecycle','value','behavior','risk') NOT NULL,
  is_mutually_exclusive  TINYINT(1) NOT NULL DEFAULT 0, -- lifecycle=true
  priority         INT NOT NULL DEFAULT 100, -- للأولوية داخل المجموعة
  criteria_json    JSON NOT NULL,            -- تعريف قابل للقراءة الآلية (نوافذ، حدود…)
  ttl_hours        INT NULL,                 -- صلاحية عضوية تلقائية (مثلاً مهجور سلة 24h)
  is_active        TINYINT(1) NOT NULL DEFAULT 1,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2.2 عضوية العملاء في الشرائح
CREATE TABLE segment_membership (
  user_id          BIGINT NOT NULL,
  segment_id       BIGINT NOT NULL,
  status           ENUM('active','inactive') NOT NULL DEFAULT 'active',
  score            DECIMAL(6,3) NULL,        -- لقيم مثل COD_RISK, RFM score…
  first_join_ts    DATETIME NOT NULL,
  last_enter_ts    DATETIME NOT NULL,
  last_exit_ts     DATETIME NULL,
  evidence         JSON NULL,                -- {rule:'A1', window:'24h', cart_id:..., last_event_ts:...}
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, segment_id),
  KEY idx_segment (segment_id),
  KEY idx_status (status),
  KEY idx_updated (updated_at),
  CONSTRAINT fk_membership_catalog FOREIGN KEY (segment_id) REFERENCES segment_catalog(segment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2.3 مؤشرات مجمّعة لكل عميل (تتحدث يوميًا/شبه لحظي)
CREATE TABLE dim_user_metrics (
  user_id              BIGINT PRIMARY KEY,
  first_order_ts       DATETIME NULL,
  last_order_ts        DATETIME NULL,
  orders_count_365     INT NOT NULL DEFAULT 0,
  revenue_365          DECIMAL(12,2) NOT NULL DEFAULT 0,
  revenue_lifetime     DECIMAL(12,2) NOT NULL DEFAULT 0,
  aov_90d              DECIMAL(12,2) NULL,
  returns_rate_90d     DECIMAL(5,2) NULL,       -- 0..100
  last_session_ts      DATETIME NULL,
  last_add_to_cart_ts  DATETIME NULL,
  last_checkout_ts     DATETIME NULL,
  cart_value_last      DECIMAL(12,2) NULL,
  coupon_usage_rate_180d DECIMAL(5,2) NULL,     -- 0..100
  cod_risk_score       DECIMAL(6,3) NULL,
  city                 VARCHAR(64) NULL,
  updated_at           DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ملاحظات
●	criteria_json يصف القواعد (مثال بالأسفل) لتسهيل توليد SQL/Jobs.
●	ttl_hours يتيح انقضاء عضوية تلقائيًا (مثل مهجور سلة بعد 24h إن لم تتكرر الحالة).
●	يمكن بناء View تُظهر “الشريحة الأساسية” لكل عميل وفق priority وis_mutually_exclusive.
 
3) أمثلة تعريف معيارية (criteria_json)
تُدرج في segment_catalog وقت التهيئة الأولى.
// CART_ABANDONER_24H
{
  "events_required": ["add_to_cart"],
  "window_hours": 24,
  "exit_on": ["purchase"],
  "min_cart_value": 1,
  "mutual_group": "behavior"
}

// CHECKOUT_ABANDONER_6H
{
  "events_required": ["begin_checkout"],
  "window_hours": 6,
  "exit_on": ["purchase"],
  "mutual_group": "behavior"
}

// VIP
{
  "rule": "percentile_or_threshold",
  "percentile": 95,
  "field": "revenue_lifetime",
  "or": {"orders_min": 5, "aov_90d_percentile": 90},
  "mutual_group": "value"
}

// DORMANT_31_90D
{
  "rule": "last_order_between_days",
  "min_days": 31,
  "max_days": 90,
  "mutual_group": "lifecycle",
  "exclusive_group": true
}

 
4) منطق الاحتساب والتحديث (Jobs & Triggers)
A) دفعة يومية (Batch / BigQuery أو MySQL)
1.	تحديث dim_user_metrics من مصادر: orders, returns, events (sessions, add_to_cart, begin_checkout).
2.	توليد عضوية لكل شريحة حَسَب القواعد:
○	دورة الحياة: من last_order_ts.
○	VIP/Value: من revenue_lifetime, aov_90d, percentiles.
○	الجودة/المخاطر: returns_rate_90d, cod_risk_score, coupon_usage_rate_180d.
B) لحظي (Streaming / Near-real-time)
●	تشغيل Functions على أحداث:
○	add_to_cart → إدراج/تحديث CART_ABANDONER_24H (يدخل الآن مع ttl_hours=24).
○	begin_checkout → إدراج/تحديث CHECKOUT_ABANDONER_6H.
○	purchase → إخراج العميل فورًا من شرائح “مهجور” وتحديث دورة الحياة.
C) قواعد الدخول/الخروج
●	عند تحقق شرط الدخول وكان السجل غير موجود → INSERT (active).
●	عند زوال الشرط (شراء، انتهاء نافذة) → UPDATE status='inactive' وlast_exit_ts=NOW().
●	عند إعادة التحقق ودخول جديد → تحديث last_enter_ts.
 
5) أمثلة SQL مختصرة
A) تحديد DORMANT_31_90D (دفعة يومية)
-- افتراض: days_since_last_order = DATEDIFF(CURDATE(), last_order_ts)
INSERT INTO segment_membership (user_id, segment_id, status, first_join_ts, last_enter_ts, evidence)
SELECT m.user_id, sc.segment_id, 'active', NOW(), NOW(),
       JSON_OBJECT('days_since_last_order', DATEDIFF(CURDATE(), m.last_order_ts))
FROM dim_user_metrics m
JOIN segment_catalog sc ON sc.code = 'DORMANT_31_90D' AND sc.is_active=1
WHERE m.last_order_ts IS NOT NULL
  AND DATEDIFF(CURDATE(), m.last_order_ts) BETWEEN 31 AND 90
ON DUPLICATE KEY UPDATE
  status='active',
  last_enter_ts=VALUES(last_enter_ts),
  evidence=VALUES(evidence),
  updated_at=CURRENT_TIMESTAMP;

B) إخراج من CART_ABANDONER_24H عند الشراء (لحظي)
UPDATE segment_membership sm
JOIN segment_catalog sc ON sc.segment_id = sm.segment_id AND sc.code='CART_ABANDONER_24H'
SET sm.status='inactive', sm.last_exit_ts=NOW()
WHERE sm.user_id = ? AND sm.status='active';

C) VIP باستخدام Percentile (يُحسب في BigQuery أو MySQL مؤقتًا)
●	احسب P95 لإجمالي الإيراد، ثم:
INSERT INTO segment_membership (...)
SELECT u.user_id, sc.segment_id, 'active', NOW(), NOW(),
       JSON_OBJECT('revenue_lifetime', m.revenue_lifetime)
FROM dim_user_metrics m
JOIN users u ON u.user_id = m.user_id
JOIN segment_catalog sc ON sc.code='VIP' AND sc.is_active=1
WHERE m.revenue_lifetime >= @p95_revenue
ON DUPLICATE KEY UPDATE status='active', last_enter_ts=NOW();

D) تنظيف الشرائح منتهية الصلاحية (TTL)
UPDATE segment_membership sm
JOIN segment_catalog sc ON sc.segment_id=sm.segment_id
SET sm.status='inactive', sm.last_exit_ts=NOW()
WHERE sm.status='active'
  AND sc.ttl_hours IS NOT NULL
  AND sm.last_enter_ts < (NOW() - INTERVAL sc.ttl_hours HOUR);

 
6) عرض “الشريحة الأساسية” (View اختياري)
CREATE VIEW user_primary_segment AS
SELECT t.user_id, t.segment_id, t.code, t.name_ar, t.group_code
FROM (
  SELECT sm.user_id, sm.segment_id, sc.code, sc.name_ar, sc.group_code,
         ROW_NUMBER() OVER (PARTITION BY sm.user_id ORDER BY
           (sc.group_code='value') DESC,  -- أعطِ VIP أولوية
           sc.priority ASC, sm.last_enter_ts DESC) AS rn
  FROM segment_membership sm
  JOIN segment_catalog sc ON sc.segment_id=sm.segment_id
  WHERE sm.status='active'
) t
WHERE t.rn=1;

 
7) ربط الشرائح بالاستخدامات (قواعد إرسال مبنية على الشرائح)
●	CART_ABANDONER_24H: يسمح برسالة تذكير واحدة خلال 24h (حد تكرار)، قناة وفق موافقات المستخدم.
●	CHECKOUT_ABANDONER_6H: 2 رسائل (6h و24h) مع كود خصم اختياري (تحكم في “COUPON_HUNTER”).
●	VIP: وصول مبكر + حدّ تكرار أعلى، مع احترام consents.
●	DORMANT/CHURN: برامج تنشيط، تفعيل WhatsApp فقط لذوي opt-in واضح.
●	COD_RISK_HIGH: رسائل تحقق قبل الشحن أو منع الدفع عند الاستلام تلقائيًا.
الموافقات لا تغيّر العضوية؛ تُطبَّق فقط عند التنفيذ (can_send).
 
8) مراقبة وجودة البيانات
●	لوحات: حجم كل شريحة، التحويلات لكل شريحة، تداخل الشرائح (overlap)، زمن البقاء.
●	تنبيهات: ارتفاع مفاجئ في CART_ABANDONER أو LOST.
●	اختبارات:
○	شراء ↦ خروج فوري من Abandoners ودخول Lifecycle المناسب.
○	حساب VIP ثابت نسبيًا ولا يقفز يوميًا بدون سبب.
○	TTL يعمل لشرائح السلوك.
 
9)  تنفيذ 
1.	إنشاء الجداول الثلاثة وتعبئة segment_catalog مع criteria_json وpriority.
2.	بناء Job يومي يُحدّث dim_user_metrics ثم يُطبّق قواعد الشرائح (INSERT/UPSERT/EXIT).
3.	Functions لحظية لأحداث add_to_cart, begin_checkout, purchase لتحديث شرائح السلوك فورًا.
4.	بناء View للشريحة الأساسية (اختياري).
5.	ربط محرّك الإرسال بشرائح الاستهداف + خدمة can_send (الموافقات).
6.	إضافة مراقبة وQA (الأحجام، معدلات التحويل، زمن البقاء، التداخل).
 
علامة التبويب 26 
جعل GA4/Firebase يعرّفان كل الأحداث باسم مستخدم واحد موحّد يساوي معرّف العميل في قاعدة البيانات (users.id).
●	دعم الانتقال من ضيف → مسجّل (mapping)، وتوحيد القياس عبر الأجهزة.
●	احترام الخصوصية: عدم استخدام أي PII (بريد/هاتف) كـ user_id.
 
2) المعايير (Standards)
●	صيغة user_id في GA4: نص قصير غير حساس مشتق من users.id (مثلاً: U123456 أو الـUUID كما هو).
○	ثابت/غير قابل لإعادة الاستخدام لعميل آخر.
○	لا تستخدم الهاتف/البريد مباشرة.
●	وقت التعيين:
○	يعيَّن بعد نجاح تسجيل الدخول/التسجيل مباشرة.
○	يُزال عند تسجيل الخروج.
●	الأحداث قبل تسجيل الدخول تُسجَّل على معرّف الجهاز (GA4 user_pseudo_id). بعد تسجيل الدخول، تستمر الجلسة مع user_id.
●	الخصوصية: في حال احتجت إظهار المعرّف خارج الأنظمة الداخلية (تقارير خارجية)، استخدم تجزئة SHA-256 لمعرّف داخلي وليس لبريد/هاتف.
 
3) تعديلات قاعدة البيانات (اختيارية لكن موصى بها)
●	جدول devices:
○	ga_app_instance_id VARCHAR(64) NULL — تخزين App Instance ID (لربط أحداث الخادم إن استخدمت Measurement Protocol).
●	جدول users:
○	لا حاجة لحقل إضافي إن كنت ستستخدم users.id نفسه كـ user_id في GA4، لكن يمكن إضافة ga_user_idVARCHAR(64) إن رغبت في طبقة تجريد.
سياسات: ga_user_id = دالة تحويل موحّدة: ga_user_id = 'U' || users.id.
 
4) تطبيق Flutter (Firebase Analytics)
4.1 الحِزم
●	firebase_core
●	firebase_analytics
●	(اختياري) firebase_auth لإدارة جلسة المستخدم
4.2 التهيئة الأساسية
●	فعّل Analytics في main().
●	على أول تشغيل بعد الإذن/الموافقة (إن طبّقتها)، أبقِ التجميع مفعّلًا:
FirebaseAnalytics.instance.setAnalyticsCollectionEnabled(true);
4.3 تعيين user_id عند تسجيل الدخول
import 'package:firebase_analytics/firebase_analytics.dart';

Future<void> onLogin(String internalUserId) async {
  // حوّل معرف DB إلى GA4 user_id (اختياري إضافة بادئة)
  final gaUserId = 'U$internalUserId';

  // 1) عيّن user_id على Analytics
  await FirebaseAnalytics.instance.setUserId(id: gaUserId);

  // 2) خصائص قياسية (اختياري لكنها مفيدة للتقارير)
  await FirebaseAnalytics.instance.setUserProperty(name: 'app_role', value: 'customer');
  await FirebaseAnalytics.instance.setUserProperty(name: 'market', value: 'YE');

  // 3) أرسل حدث login (اختياري)
  await FirebaseAnalytics.instance.logLogin(loginMethod: 'password'); // أو 'otp', 'social'
}

4.4 إزالة user_id عند تسجيل الخروج
Future<void> onLogout() async {
  // يزيل الربط بالمستخدم الحالي
  await FirebaseAnalytics.instance.setUserId(id: null);

  // مستحسن لمسح الوسوم المرتبطة بالمستخدم السابق
  await FirebaseAnalytics.instance.resetAnalyticsData();
}

4.5 أفضل ممارسات إضافية
●	لا تعيّن user_id قبل التأكد من نجاح التوثيق.
●	لو سمحتِ بتبديل الحساب داخل التطبيق: نفّذ onLogout() ثم onLogin() للحساب الجديد.
●	اربط هذا التدفق مع مواصفاتك السابقة: عند onLogin نفّذ أيضًا /v1/devices/associate.
 
5) الويب (إن وُجد WebView/موقع)
●	مع gtag.js:
<script>
  // بعد نجاح تسجيل الدخول
  gtag('config', 'G-XXXXXXX', {
    'user_id': 'U123456' // نفس صيغة التطبيق
  });

  // لتعيين خصائص مستخدم
  gtag('set', 'user_properties', {
    app_role: 'customer',
    market: 'YE'
  });

  // عند تسجيل الخروج
  // GA4 لا يوفّر "unset" مباشر عبر gtag، لكن بدّلي user_id إلى undefined عبر إعادة config بدون user_id
  gtag('config', 'G-XXXXXXX'); // بدون user_id
</script>

لو كان لديك تدفق مشترك App + Web، احرصي على استخدام نفس صيغة user_id وموحِّد الدخول (SSO) لتحسين الربط عبر القنوات.
 
6) الخادم (Measurement Protocol v2) — اختياري متقدّم
استخدمه فقط إن سترسلين أحداث خادمية (مثل تأكيد الدفع) وتريدين أن تُنسَب لنفس المستخدم والجلسة.
●	لأحداث تطبيقات الموبايل أرسل app_instance_id (من التطبيق) ونفس user_id:
○	خزّن ga_app_instance_id في devices.
○	حمّلي قيمة app_instance_id لمرة واحدة من التطبيق (إن لزم) وارسليها لسيرفرك.
●	لأحداث الويب استخدم client_id (من _ga) ونفس user_id.
هيكل JSON مبسّط:
{
  "api_secret": "XXXX",
  "measurement_id": "G-XXXX",
  "firebase_app_id": "1:123:web:abc",  // لمسارات التطبيقات/الويب حسب نوع الحدث
  "user_id": "U123456",
  "app_instance_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  "events": [{
    "name": "purchase_server",
    "params": {
      "value": 25000,
      "currency": "YER",
      "transaction_id": "ORD-9876"
    }
  }]
}

مهم: لا تُرسل نفس الحدث مرتين (عميل + خادم) بدون إزالة التكرار. إن احتجت الازدواج، أضف event_id/timestamp_micros موحّدين وخصّصي dedup في التحليلات.
 
7) BigQuery: التوافق وربط التقارير
عند تفعيل GA4 BigQuery Export:
●	ستجدي:
○	user_id في المستوى العلوي للسجل.
○	user_pseudo_id (معرّف الجهاز/التثبيت).
●	لربط تقارير الإيراد من DB:
○	اربطي user_id في GA4 بـ users.id (أو ga_user_id) مباشرة.
○	احفظي order_id نفسه كـ transaction_id في حدث purchase (عميل/خادم)، لتسهيل الربط مع جدول orders.
استعلام مثال (تلخيص مشتريات لكل user_id):
SELECT
  user_id,
  COUNTIF(event_name='purchase') AS purchases,
  SUM(CAST(ep.value.int_value AS INT64)) FILTER (WHERE ep.key='value') AS total_value
FROM `project.dataset.events_*`,
UNNEST(event_params) ep
WHERE user_id IS NOT NULL
GROUP BY user_id;

 
8) التكامل مع مواصفاتك السابقة
●	عند onLogin:
○	devices.associate (ربط الجهاز بالمستخدم)
○	analytics.setUserId
○	تحديث user_properties (مثل first_source/last_source إن تحفظينها محليًا)
●	عند purchase:
○	أرسل حدث purchase إلى Firebase Analytics بنفس user_id.
○	خزِّن نفس user_id داخل orders لتطابق 1:1 مع تقارير GA4.
 
9) اختبارات (QA)
1.	تسجيل الدخول → افتحي جلسة، نفّذي onLogin، أطلقي حدث purchase؛ في DebugView يجب أن يظهر user_id=U....
2.	تسجيل الخروج → setUserId(null) + resetAnalyticsData()؛ أحداث ما بعد الخروج لا تحتوي user_id.
3.	تبديل الحساب على نفس الجهاز → ينعكس user_id الجديد على الأحداث التالية فقط.
4.	جهازان لنفس الحساب → كلاهما يسجّل user_id نفسه؛ تقارير GA4 توحّد المستخدم.
5.	خادم + عميل (إن استخدمت MP): تأكدي أن حدث الخادم يحمل نفس user_id و(للتطبيق) app_instance_id لتجنّب تشظّي المستخدم.
 
10) التنفيذ
●	 اعتماد صيغة ga_user_id = تحويل ثابت من users.id (بدون PII).
●	 Flutter: setUserId عند الدخول، وsetUserId(null) + resetAnalyticsData() عند الخروج.
●	 إرسال purchase مع transaction_id = order_id.
●	 (اختياري) حفظ ga_app_instance_id في devices إن ستُرسلين أحداث خادمة عبر MP.
●	 Web (إن وجد): gtag('config', ..., {user_id}) بعد تسجيل الدخول.
●	 BigQuery: بناء لوحات تربط user_id من GA4 بـ users.id وorders.
●	 QA: التحقق عبر DebugView + عينات BigQuery.
 
علامة التبويب 27 
قياس احتفاظ المستخدمين حسب دفعات اكتساب (Cohorts) على أساس تاريخ البدء.
●	دعم نوعين شائعين من “النشاط”:
○	Activity Retention: المستخدم قام بأي تفاعل معتبر.
○	Purchase Retention: المستخدم قام بعملية شراء.
●	عرض مؤشرات: W1/W4/W8 و M1/M3/M6 + WAU/MAU.
2) التعاريف (Standards)
2.1 مرساة الدُفعة (Cohort Anchor)
●	تطبيق الموبايل (مستحسن): حدث first_open من GA4 (أول فتح للتطبيق).
●	الويب (إن وجد): حدث first_visit.
●	تحليل الشراء: يمكن تعريف دفعة بديلة على أساس first_purchase_ts (أول طلب).
احتفظ بالاثنين: Cohort_Acq (first_open/visit) و Cohort_Purch (first_purchase) حسب تقريرك.
2.2 تعريف “نشط”
اختر واحدة (أو اعرض كلاهما بالتوازي):
●	نشاط عام (Activity): وجود أي من الأحداث: session_start, user_engagement, view_item, add_to_cart, begin_checkout, purchase.
●	نشاط شراء (Purchase): وجود حدث purchase فقط.
2.3 أنواع الاحتفاظ
●	Classic Retention (Cohort-aligned):
أسبوع 0 = أسبوع الانضمام، أسبوع 1 = [اليوم 7..13] منذ الانضمام… (نوافذ ثابتة بالنسبة لتاريخ الانضمام).
●	Rolling Retention:
المستخدم يعتبر “محتفَظ به” في الأسبوع k إذا عاد في أي وقت بعد اليوم 7k وحتى الآن. (للتنشيط الكلي—استخدِمه عند الحاجة فقط).
●	Bracket Retention:
نوافذ تقويمية ثابتة (أسابيع ISO أو أشهر تقويمية)؛ مفيد لملاءمة التقارير الشهرية.
الموصى به للتقارير التشغيلية: Classic Retention.
2.4 توحيد المناطق الزمنية
●	GA4 يصدّر UTC؛ استخدم DATETIME(TIMESTAMP_MICROS(event_timestamp), "Asia/Aden") لضبط +03:00.
●	أسبوع ISO يبدأ الاثنين؛ وثّق ذلك في المستند.
 
3) مخطط بيانات مساند (اختياري ولكنه مفيد)
-- dim_users: مرساة الدُفعة
CREATE TABLE dim_users (
  user_key           STRING PRIMARY KEY, -- COALESCE(user_id, user_pseudo_id)
  first_open_ts      DATETIME,           -- من GA4
  first_visit_ts     DATETIME,           -- للويب إن وجد
  first_purchase_ts  DATETIME
);

-- dim_calendar: أبعاد الوقت (يوم/أسبوع ISO/شهر)
-- إن لم تكن موجودة، أنشئها لتبسيط التقارير.

user_key: في GA4/BQ نستخدم COALESCE(user_id, user_pseudo_id) لضمان ربط حسابات مسجّلة مع الضيوف عند التعيين.
 
4) BigQuery (GA4 Export) — SQL أمثلة
بدّلي project.dataset باسم مشروعك.
ضعي مؤشرات منطقية في WHERE حسب قناتك (App/Web).
Activity list قابلة للتعديل.
4.1 استخراج دفعة الاكتساب الأسبوعية (first_open)
DECLARE TZ STRING DEFAULT "Asia/Aden";

WITH firsts AS (
  SELECT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    MIN(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS first_open_dt
  FROM `project.dataset.events_*`
  WHERE event_name = 'first_open'
  GROUP BY 1
),
cohorts AS (
  SELECT
    user_key,
    DATE_TRUNC(DATE(first_open_dt), WEEK(MONDAY)) AS cohort_week
  FROM firsts
),
acts AS (
  -- نشاط معتبر (Activity Retention)
  SELECT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    DATE(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS activity_date
  FROM `project.dataset.events_*`
  WHERE event_name IN ('session_start','user_engagement','view_item','add_to_cart','begin_checkout','purchase')
),
joined AS (
  SELECT
    c.cohort_week,
    a.user_key,
    a.activity_date,
    DATE_DIFF(a.activity_date, c.cohort_week, DAY) AS days_since_cohort
  FROM acts a
  JOIN cohorts c USING (user_key)
),
buckets AS (
  -- حاويات الأسابيع الكلاسيكية: W0/W1/...
  SELECT
    cohort_week,
    user_key,
    CASE
      WHEN days_since_cohort BETWEEN 0 AND 6 THEN 0
      WHEN days_since_cohort BETWEEN 7 AND 13 THEN 1
      WHEN days_since_cohort BETWEEN 14 AND 20 THEN 2
      WHEN days_since_cohort BETWEEN 21 AND 27 THEN 3
      WHEN days_since_cohort BETWEEN 28 AND 34 THEN 4
      ELSE NULL
    END AS w_bucket
  FROM joined
)
SELECT
  cohort_week,
  COUNT(DISTINCT user_key) AS cohort_size,
  SAFE_DIVIDE(COUNT(DISTINCT IF(w_bucket=0, user_key, NULL)), COUNT(DISTINCT user_key)) AS w0_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(w_bucket=1, user_key, NULL)), COUNT(DISTINCT user_key)) AS w1_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(w_bucket=2, user_key, NULL)), COUNT(DISTINCT user_key)) AS w2_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(w_bucket=3, user_key, NULL)), COUNT(DISTINCT user_key)) AS w3_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(w_bucket=4, user_key, NULL)), COUNT(DISTINCT user_key)) AS w4_ret
FROM buckets
GROUP BY cohort_week
ORDER BY cohort_week DESC;

4.2 الاحتفاظ الشهري (Classic) على أساس first_open
DECLARE TZ STRING DEFAULT "Asia/Aden";

WITH firsts AS (
  SELECT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    MIN(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS first_open_dt
  FROM `project.dataset.events_*`
  WHERE event_name='first_open'
  GROUP BY 1
),
cohorts AS (
  SELECT
    user_key,
    DATE_TRUNC(DATE(first_open_dt), MONTH) AS cohort_month
  FROM firsts
),
acts AS (
  SELECT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    DATE(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS activity_date
  FROM `project.dataset.events_*`
  WHERE event_name IN ('session_start','user_engagement','view_item','add_to_cart','begin_checkout','purchase')
),
joined AS (
  SELECT
    c.cohort_month,
    a.user_key,
    a.activity_date,
    DATE_DIFF(a.activity_date, c.cohort_month, DAY) AS days_since_cohort
  FROM acts a
  JOIN cohorts c USING (user_key)
),
mbuckets AS (
  SELECT
    cohort_month,
    user_key,
    CASE
      WHEN days_since_cohort BETWEEN 0 AND 29 THEN 0
      WHEN days_since_cohort BETWEEN 30 AND 59 THEN 1
      WHEN days_since_cohort BETWEEN 60 AND 89 THEN 2
      WHEN days_since_cohort BETWEEN 90 AND 119 THEN 3
      WHEN days_since_cohort BETWEEN 120 AND 149 THEN 4
      ELSE NULL
    END AS m_bucket
  FROM joined
)
SELECT
  cohort_month,
  COUNT(DISTINCT user_key) AS cohort_size,
  SAFE_DIVIDE(COUNT(DISTINCT IF(m_bucket=0, user_key, NULL)), COUNT(DISTINCT user_key)) AS m0_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(m_bucket=1, user_key, NULL)), COUNT(DISTINCT user_key)) AS m1_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(m_bucket=2, user_key, NULL)), COUNT(DISTINCT user_key)) AS m2_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(m_bucket=3, user_key, NULL)), COUNT(DISTINCT user_key)) AS m3_ret,
  SAFE_DIVIDE(COUNT(DISTINCT IF(m_bucket=4, user_key, NULL)), COUNT(DISTINCT user_key)) AS m4_ret
FROM mbuckets
GROUP BY cohort_month
ORDER BY cohort_month DESC;

4.3 احتفاظ الشراء (Purchase Retention) — أسبوعي
بدّلي “acts” ليقتصر على purchase فقط:
...
acts AS (
  SELECT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    DATE(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS activity_date
  FROM `project.dataset.events_*`
  WHERE event_name = 'purchase'
),
...

4.4 مصفوفة Heatmap (Pivot) للاحتفاظ الأسبوعي
WITH ret AS ( -- استخدمي استعلام 4.1 حتى حقل w_bucket
  ... 
)
SELECT
  cohort_week,
  COUNT(DISTINCT user_key) AS cohort_size,
  ROUND(100*COUNT(DISTINCT IF(w_bucket=0, user_key, NULL))/COUNT(DISTINCT user_key),1) AS W0,
  ROUND(100*COUNT(DISTINCT IF(w_bucket=1, user_key, NULL))/COUNT(DISTINCT user_key),1) AS W1,
  ROUND(100*COUNT(DISTINCT IF(w_bucket=2, user_key, NULL))/COUNT(DISTINCT user_key),1) AS W2,
  ROUND(100*COUNT(DISTINCT IF(w_bucket=3, user_key, NULL))/COUNT(DISTINCT user_key),1) AS W3,
  ROUND(100*COUNT(DISTINCT IF(w_bucket=4, user_key, NULL))/COUNT(DISTINCT user_key),1) AS W4
FROM ret
GROUP BY cohort_week
ORDER BY cohort_week DESC;

4.5 WAU/MAU (نسبة المرونة)
DECLARE TZ STRING DEFAULT "Asia/Aden";
DECLARE today DATE DEFAULT CURRENT_DATE(TZ);

WITH acts AS (
  SELECT DISTINCT
    COALESCE(user_id, user_pseudo_id) AS user_key,
    DATE(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) AS d
  FROM `project.dataset.events_*`
  WHERE event_name IN ('session_start','user_engagement','view_item','add_to_cart','begin_checkout','purchase')
    AND DATE(DATETIME(TIMESTAMP_MICROS(event_timestamp), TZ)) BETWEEN DATE_SUB(today, INTERVAL 30 DAY) AND today
)
SELECT
  COUNT(DISTINCT IF(d BETWEEN DATE_SUB(today, INTERVAL 7 DAY) AND today, user_key, NULL)) AS WAU,
  COUNT(DISTINCT user_key) AS MAU,
  SAFE_DIVIDE(
    COUNT(DISTINCT IF(d BETWEEN DATE_SUB(today, INTERVAL 7 DAY) AND today, user_key, NULL)),
    COUNT(DISTINCT user_key)
  ) AS WAU_MAU_ratio
FROM acts;

 
5) تقارير DB داخلية (بدون GA4) — فكرة مختصرة
لو كان لديك جدول أحداث داخلي events_app:
●	أعمدة: user_id, event_date, event_name
●	اتبع نفس منطق التجميع أعلاه مع DATE_DIFF على event_date.
 
6) لوحات ومؤشرات (KPIs)
●	Weekly Retention (Activity): W1, W4 (أساسيان).
●	Monthly Retention (Activity): M1, M3, M6.
●	Purchase Retention: نسبة من cohort تعود وتشتري في W4 / M3.
●	WAU/MAU: يقيس “لزاجة” التطبيق (Stickiness).
●	Median Time-to-2nd Purchase: وسيط الزمن للشراء الثاني (مهم للتنشيط).
 
7) معايير جودة البيانات (QA)
●	الاحتفاظ غير متزايد منطقيًا عبر الأسابيع: W2 ≤ W1 … (راقبيه).
●	تراجع ملحوظ في “Direct” بعد تحسين UTM (من تقارير القنوات) ↦ يعني القياس جيد.
●	تأكدي من المنطقة الزمنية “Asia/Aden” في كل التقارير.
●	الأحداث المكررة (عن طريق العميل والخادم) يجب منع ازدواجها أو تمييزها بـ event_id.
 
8) ربط بالشرائح والموافقات
●	يمكنك تفصيل الاحتفاظ لكل شريحة (VIP, DORMANT…) بضم user_id مع segment_membership (status='active' لحظة الانضمام أو تراكميًا).
●	عند إنشاء حملات “تنشيط”، استخدمي can_send لاحترام الموافقات قبل الإرسال.
 
9) التنفيذ 
1.	اختيار Anchor: first_open (App) / first_visit (Web) + بديل first_purchase.
2.	تعريف “نشط” (Activity vs Purchase) وتثبيته في المستند.
3.	تفعيل GA4 BigQuery Export (إن لم يُفعّل).
4.	بناء استعلامات 4.1–4.5 (كوّني Views أو Scheduled Queries).
5.	ضبط المنطقة الزمنية إلى "Asia/Aden".
6.	إنشاء لوحات Heatmap + بطاقات W1/W4/M1/M3/WAU/MAU.
7.	QA: تحقق من خصائص التناقص، والهوية الموحّدة user_id.
 
الكتالوج (Catalog) 
الكتالوج (Catalog)

1) الهدف
●	تنظيم المنتجات ونسخها (مقاسات/ألوان) ومحتواها لتجربة تسوّق سلسة.
●	دعم البحث والتصفية والفرز بكفاءة.
●	ربط الكتالوج بالمخزون والتسعير والعروض دون تعقيد.
●	رفع معدّل التحويل عبر محتوى بصري ونصي مكتمل.
 
2) نطاق الكتالوج (Scope)
●	العلامات التجارية، المنتجات الأساسية، النسخ (Variants)، التصنيفات متعددة المستويات، الخصائص (Attributes)، الوسائط (صور/فيديو)، الأسعار والعروض، المجموعات (Collections)، أدلة المقاسات والعناية، شارات العرض، SEO، الربط بالمنتجات ذات الصلة.
●	التكاملات: المخزون على مستوى النسخة، العروض/الخصومات، الواجهة الإدارية (لوحة التحكم)، البحث والفلاتر.
 
3) الكيانات الأساسية والحقول
أدناه قائمة الكيانات والحقول المقترحة ووصف مختصر لكل حقل. (لا توجد أكواد؛ التنفيذ وتقنيات التخزين من صلاحية الفريق).
3.1 العلامة التجارية (Brand)
●	brand_id: معرف داخلي.
●	name: اسم العلامة.
●	country_of_origin: بلد المنشأ (اختياري).
●	display_order: ترتيب العرض.
●	status: نشط/مؤرشف.
3.2 المنتج الأساسي (Product)
●	product_id: معرف داخلي.
●	name_ar / name_en: اسم عربي (إلزامي) + إنجليزي (اختياري).
●	short_description / long_description: وصف مختصر وموسع.
●	brand_id: مرجع العلامة.
●	product_type: فستان/أحذية/حقائب/لانجري/بيجامات… (قائمة مضبوطة).
●	collection_code / season: رمز التشكيلة/الموسم (اختياري).
●	country_of_origin: بلد المنشأ (اختياري).
●	badges: شارات عرض (جديد/الأكثر مبيعًا/قريب النفاد) — مع ملاحظة إن كانت تلقائية أم يدوية.
●	publish_status: مسودة/منشور/مؤرشف.
●	slug: رابط ثابت فريد (أساسي في العربية).
●	seo_title / seo_description: تحسين محركات البحث (اختياري).
●	content_score: درجة اكتمال المحتوى (0–100) للحكم على الجاهزية.
●	created_at / updated_at: إدارة زمنية.
3.3 نسخ المنتج (Product Variant)
●	variant_id: معرف داخلي.
●	product_id: مرجع المنتج.
●	sku: رقم صنف فريد (مطلوب فريد عالميًا).
●	barcode: باركود/QR (اختياري).
●	color: اللون (من قاموس ألوان قياسي).
●	size: المقاس (S/M/L/XL أو قياسات رقمية حسب الفئة).
●	material / fabric: الخامة/القماش (اختياري).
●	weight / dimensions: الوزن/الأبعاد (لأغراض شحن اختيارية).
●	regular_price: السعر الأساسي.
●	sale_price: سعر العرض (إن وجد).
●	currency: العملة (YER/SAR…).
●	price_valid_from / price_valid_to: جدول زمني للعرض (اختياري).
●	availability_status: متوفر/غير متوفر/طلب مسبق.
●	is_default: النسخة الافتراضية لعرضها أولًا.
●	created_at / updated_at.
ملاحظة: مستوى النسخة هو مصدر الحقيقة للسعر والتوفر، ويرتبط بالمخزون.
3.4 التصنيفات (Category)
●	category_id: معرف داخلي.
●	parent_id: تصنيف أب (لدعم مستويات متعددة).
●	name_ar / name_en: اسم عربي + إنجليزي.
●	slug: رابط ثابت فريد للتصنيف.
●	display_order: ترتيب العرض.
●	is_visible: الإظهار في الواجهة/الإخفاء.
3.5 ربط المنتج بالتصنيفات (Product–Category Link)
●	product_id, category_id: يسمح بوجود المنتج في أكثر من تصنيف.
3.6 المجموعات (Collections)
●	collection_id: معرف.
●	name: اسم المجموعة (مثل: “وصل حديثًا”، “فساتين سهرة”).
●	type: يدوي/آلي.
●	rule_definition: قواعد المجموعة إن كانت آلية (مثال: فئة = فساتين && سعر ≥ X && شارة = جديد).
●	display_order / is_visible.
●	products_link: ربط المنتجات بالمجموعة عند النوع اليدوي.
3.7 الخصائص (Attributes) والقيم
●	attribute: تعريف الخاصية (مثال: الطول، القصّة، الياقة، نوع الأكمام، النقشة، المناسبة، القماش…).
●	attribute_values: القيم الممكنة لكل خاصية (من قوائم مضبوطة).
●	product_attributes: خصائص على مستوى المنتج (تؤثر على الفلاتر العامة).
●	variant_attributes: خصائص على مستوى النسخة (عادة اللون/المقاس/الخامة).
الهدف: مرونة بدون فوضى؛ خصائص أساسية للأزياء جاهزة منذ البداية.
3.8 الوسائط (Media)
●	media_id: معرف.
●	product_id / variant_id: الربط (الأغلب على مستوى المنتج، ويمكن على مستوى النسخة عند اختلاف الألوان).
●	type: صورة/فيديو.
●	url: رابط الوسيط (يفضّل عبر CDN).
●	alt_text: نص بديل وصفي.
●	sort_order: ترتيب العرض (الأولى غلاف).
●	is_primary: تأكيد الصورة الأساسية عند الحاجة.
●	aspect_ratio / width / height: توصيف اختياري لضبط الجودة.
3.9 أدلة المقاسات والعناية (Size Guide / Care)
●	size_guide_id: مرجع جدول مقاسات لكل فئة/علامة.
●	care_instructions: تعليمات العناية (رموز أو نصوص مختصرة).
●	ربط بالمنتج/الفئة حسب الحاجة.
3.10 العلاقات ذات الصلة (Related / Cross‑sell / Upsell)
●	related_products: منتجات مرتبطة يدويًا.
●	cross_sell / upsell: اقتراحات تكميليّة (حقيبة/حذاء مع فستان).
3.11 شارات العرض (Badges / Flags)
●	is_new: جديد (تلقائي خلال X أيام من النشر أو يدوي).
●	is_best_seller: الأكثر مبيعًا (حسب مبيعات تاريخية/يدوي).
●	is_low_stock: قريب على النفاد (وفق حد مخزون).
●	is_on_sale: ضمن عرض (يتحدد من السعر/الجدولة).
3.12 SEO والتعريب
●	slug فريد لكل منتج وتصنيف (العربية أساس).
●	meta_title / meta_description للمنتج والتصنيف (اختياري).
●	دعم name/description بلغتين (على الأقل AR أساسي + EN اختياري).
 
4) قواعد العمل (Business Rules)
●	لا يُنشَر منتج حتى تتوفر: اسم عربي، تصنيف واحد على الأقل، صورة أساسية، نسخة واحدة على الأقل بسعر فعّال.
●	يمنع تكرار (اللون + المقاس) داخل نفس المنتج.
●	السعر والتوفر يُحدّدان على مستوى النسخة (Variant).
●	أول صورة هي الغلاف؛ جودة وأبعاد موحّدة (نسبة 4:5 أو 3:4) وعدد صور مثالي 5–8.
●	شارات العرض: إما تلقائية بالقواعد أو قابلة للضبط يدويًا مع أولوية واضحة (تلقائي → يدوي أو العكس).
●	“أبلغني عند التوفر”: تُفعّل للنسخ غير المتاحة وتُخزن طلبات الإشعار (خارج نطاق هذا المستند).
●	المنتجات المؤرشفة لا تظهر في البحث ولا في التصنيفات/المجموعات العامة.
 
5) البحث والتصفية (Search & Facets)
●	فلاتر أساسية: المقاس، اللون، السعر (مدى)، التصنيف، العلامة، الخامة/القماش، الطول، القصّة، الأكمام، الياقة، النقشة، المناسبة، بلد المنشأ، التوفر، الخصومات، “وصل حديثًا”.
●	مراتب الفرز: الأحدث، السعر تصاعديًا/تنازليًا، الأكثر مبيعًا، الأكثر مشاهدة/إضافة للسلة.
●	دعم اقتراحات البحث وتصحيح الأخطاء الإملائية لاحقًا (اختياري).


 
6) إدارة المحتوى والتصوير (Content Standards)
●	الصور: خلفية نظيفة، زووم على القماش/التفاصيل، إضاءة ثابتة، أبعاد موحّدة، ضغط مناسب.
●	النصوص: اسم واضح + نقاط مختصرة (القماش/القصّة/الطول/المناسبة/العناية).
●	الألوان: أسماء متسقة + عيّنات لونية (swatches) مطابقة قدر الإمكان.
●	الترجمة: العربية أساس؛ الإنجليزية لتوسيع الأسواق لاحقًا.
 
7) الواجهة الإدارية (لوحة التحكم)
●	إنشاء/تعديل منتج مع عدّة نسخ بسرعة.
●	رفع وترتيب الصور بالسحب والإفلات.
●	استيراد/تحديث جماعي (CSV/Excel) للمنتجات والأسعار والخصائص.
●	تعديلات جماعية: نشر/إلغاء نشر، تعيين تصنيف، تغيير أسعار، نقل لمجموعة.
●	إدارة مجموعات الصفحة الرئيسية: يدويًا أو عبر قواعد آلية.
●	لوحة درجة اكتمال المحتوى (اسم/صور/وصف/خصائص/سعر/تصنيف) لكل منتج.
 
8) الجودة والجاهزية (Catalog Health)
●	درجة اكتمال المحتوى لكل منتج (0–100) مع معايير واضحة لحسابها.
●	نسبة المنتجات المكتملة > 90% كهدف.
●	تغطية المقاسات الأساسية لكل منتج (حسب الفئة).
●	نسبة النسخ غير المتوفرة مستهدفة < 20%.
●	متابعة معدل الإرجاع لكل SKU لتحسين الوصف والمقاسات.
 
9) العلاقات مع الأنظمة الأخرى
●	المخزون: النسخة ترتبط بمخزون الموقع/المستودع. حالة التوفر تُستمد من المخزون.
●	العروض/الخصومات: تُعرض تلقائيًا عند اقتران النسخة بعرض ساري.
●	التوصيات: يمكن ربط واجهة التوصية (AI/قواعد) بقوائم cross‑sell/upsell.
 
10) ضوابط البيانات والخصوصية
●	توحيد قوائم القيم (الألوان/المقاسات/الأقمشة) لتجنّب الفوضى النصية.
●	منع تكرار SKU.
●	استخدام حقول زمنية للإنشاء/التحديث؛ ودعم الأرشفة الناعمة (Soft Archive) للمنتجات.
●	التحكم في الوصول حسب الدور: المحتوى/التسعير/النشر.
 
11) مؤشرات الأداء المطلوبة
●	زمن تحميل قوائم المنتجات وتفاصيل المنتج (للمتابعة عبر Firebase Performance).
●	نسبة النقر إلى تفاصيل المنتج من القوائم.
●	تحويلات إضافة للسلة والشراء لكل فئة/تصنيف.
●	أداء البحث (لا توجد نتائج/استعلامات شائعة/استعلامات تؤدي لمبيعات).
 
12) معايير القبول (Definition of Done)
●	يمكن إنشاء منتج كامل وربط نسخ وصور وتصنيفات ونشره.
●	البحث والفلاتر يعملان بدقة مع فرز موثوق.
●	تظهر خصائص اللون/المقاس بوضوح في تفاصيل المنتج ويُمكن الاختيار بينها بسهولة.
●	الواجهة الإدارية تدعم الاستيراد والتعديلات الجماعية والمجموعات.
●	شارات “جديد/خصم/الأكثر مبيعًا/قريب النفاد” تُعرض وفق القواعد.
●	لوحة صحة الكتالوج تعرض درجة اكتمال المحتوى ونقاط التحسين.
 
13) خارطة الإصدارات (Release Plan)
●	MVP: العلامات، المنتجات، النسخ، التصنيفات، الصور، الأسعار، فلاتر أساسية، مجموعتان (وصل حديثًا/الأكثر مبيعًا)، معايير نشر.
●	المرحلة 2: خصائص موسّعة للأزياء، مجموعات آلية بالقواعد، أدلة مقاسات ديناميكية، فيديو قصير، “أبلغني عند التوفر”.
●	المرحلة 3: تعدد قوائم الأسعار حسب السوق/العملة، توصيات ذكية، تحسين البحث الدلالي.
 
ملاحظات ختامية
●	هذه المتطلبات تصف “ما يلزم” وظيفيًا للكتالوج بدون تقييد التنفيذ بتقنية محددة.
●	يعتمد تحديد أنواع الحقول/الفهارس والقيود التفصيلية على قاعدة البيانات المختارة، مع الحفاظ على القواعد الوظيفية المذكورة أعلاه.
●	يُفضّل توثيق قاموس للخصائص والقيم المسموح بها (Attributes Dictionary) قبل الاستيراد الأول للبيانات لتفادي التضارب لاحقًا.



 كتالوج المنتجات المصمَّمة:
●	تنظيم محكم للبيانات: المنتج الأساسي → نسخ (لون/مقاس) → تصنيفات وخصائص واضحة. النتيجة: إدخال وتحديث أسهل، ومنع تكرار الأكواد (SKU).
●	تجربة تسوّق أسرع ودقيقة: بحث وفلاتر ذكية (مقاس/لون/سعر/مناسبة…) توصّل العميلة لما تريد بسرعة، فترتفع إضافة السلة والتحويل.
●	سعر وتوفر موثوقان: التحديد على مستوى النسخة يضمن أن ما يظهر “متوفر” فعليًا، مع دعم “أبلغني عند التوفر” وتقليل الإحباط.
●	تحكّم تسويقي مرن: مجموعات (Collections) وشارات تلقائية/يدوية (جديد/خصم/الأكثر مبيعًا) لعرض أقسام جذابة وتحديث الواجهة بسرعة.
●	تحسين جودة المحتوى: معيار “درجة اكتمال المحتوى” وصحة الكتالوج يوجّهان الفريق لإكمال الصور/الوصف/الخصائص، ما يرفع التحويل ويقلّل المرتجعات.
●	SEO وصور منظّمة: Slug وعناوين وأوصاف محسّنة + صور مرتبة، ما يزيد الظهور العضوي وجودة الهبوط من الإعلانات.
●	كفاءة تشغيلية: استيراد/تعديلات جماعية وصلاحيات حسب الدور—وقت أقل لإدارة الكتالوج وأخطاء أقل.
●	تكامل سلس مع بقية النظام: ارتباط مباشر بالمخزون والعروض والشحن، فتكون الأسعار والتقارير متسقة ودقيقة.
●	رفع متوسط قيمة الطلب: علاقات “منتجات مرتبطة/تكميليّة” (cross-sell/upsell) تزيد فرص إضافة قطع مكمِّلة.
●	قابلية توسّع بلا فوضى: قواميس ألوان/مقاسات/خصائص موحّدة، مع قابلية لاحقة لأسعار متعددة للأسواق.
●	قياس واتخاذ قرار أفضل: مؤشرات مثل الأكثر مشاهدة، الأكثر إضافة للسلة، وقيمة السلال حسب الفئة—تساعد في التوريد، التسعير، وترتيب الواجهة.
توقعات واقعية (تختلف حسب التنفيذ):
تحسّن معدل التحويل على صفحة المنتج 5–15% مع اكتمال المحتوى، انخفاض المرتجعات 5–10% بفضل أدلة المقاسات والوصف الأدق، وزيادة 3–8% في متوسط قيمة الطلب عبر العروض التكاملية.
الخلاصة: هذا الكتالوج يمنحك قاعدة بيانات نظيفة وقابلة للتوسّع، وتجربة تسوّق أوضح وأسرع، وتحكّم تسويقي وتشغيلي يترجم مباشرة إلى مبيعات أعلى وتكاليف أقل. 
المنتجات (Product) 
المنتجات (Product)
1) الهدف
تجميع كل ما يخص المنتج الأساسي في سجل واحد: الاسم، الوصف، العلامة، التصنيفات، الوسائط، الخصائص العامة، وشارات العرض—مع فصل الأسعار والتوفر على مستوى النسخ (Variant).
2) ما الذي يمثّله “المنتج”
●	“المنتج” = هوية العنصر في المتجر (فستان/حقيبة/حذاء…).
●	تحته تأتي النسخ (لون/مقاس/خامة)، وهي مصدر السعر والتوفر.
●	المنتج يرتبط بتصنيفات متعددة، وخصائص عامة للفلاتر، وصور/فيديو، ومجموعات العرض.
3) أهم الحقول 
●	التعريفات: اسم عربي (أساسي) + إنجليزي (اختياري)، وصف مختصر وموسع، نوع/فئة سلعية (فستان/لانجري/أحذية…)، العلامة التجارية، موسم/تشكيلة (اختياري).
●	العرض: شارات (جديد/خصم/الأكثر مبيعًا/قريب النفاد)، ترتيب العرض، حالة النشر (مسودة/منشور/مؤرشف).
●	التصنيفات: ارتباط بواحد أو أكثر من التصنيفات المتعددة المستويات.
●	الخصائص العامة: (طول/قصّة/ياقة/أكمام/نقشة/مناسبة/قماش… من قوائم مضبوطة).
●	الوسائط: صورة أساسية + صور إضافية مرتّبة، (فيديو اختياري)، نص بديل.
●	SEO والتعريب: رابط ثابت فريد (Slug)، عنوان/وصف SEO (اختياري).
●	جودة المحتوى: درجة اكتمال المحتوى (0–100) تُحسب من توفر الاسم/الصورة/الوصف/الخصائص/التصنيف.
ملاحظة: السعر والتوفر ليسا على مستوى المنتج بل على مستوى النسخة.
4) العلاقات
●	منتج ↔ نسخ: واحد إلى متعدد.
●	منتج ↔ تصنيفات: متعدد إلى متعدد.
●	منتج ↔ مجموعات (Collections): يدوي أو قواعد آلية.
●	منتج ↔ وسائط: واحد إلى متعدد (مع إمكانية ربط صور بألوان النسخ).
●	منتج ↔ منتجات مرتبطة/تكميليّة (Related/Cross-sell/Upsell).


5) قواعد العمل
●	لا يُنشر المنتج إلا عند اكتمال: اسم عربي + تصنيف + صورة أساسية + نسخة واحدة فعّالة بالسعر.
●	داخل المنتج الواحد: لا تتكرر (لون + مقاس) بين النسخ.
●	الشارة “خصم” تظهر إذا كان للنسخة سعر عرض ساري؛ “جديد” خلال X أيام من النشر (أو تُحدَّد يدويًا).
●	المنتج المؤرشف لا يظهر في البحث والتصنيفات.
●	اللون يُعرض بـ عينة لونية (swatch) ويبدّل الصور عند التغيير.
6) معايير المحتوى
●	الاسم: واضح ويشير للفئة والتميّز (مثال: “فستان سهرة ساتان بقصّة ملفوفة”).
●	الوصف: نقاط مختصرة: القماش، القصّة، الطول، المناسبة، تعليمات العناية.
●	الصور: 5–8 صور بجودة موحّدة ونسبة 4:5 أو 3:4 + لقطة قماش قريبة.
●	المقاسات والعناية: ربط بدليل مقاسات مناسب للفئة وتعليمات العناية.
●	التعريب: العربية أساس؛ الإنجليزية اختيارية.
7) إدارة المنتج (لوحة التحكم)
●	إنشاء/تعديل منتج بسرعة مع إدارة النسخ والوسائط والسعر والعروض.
●	استيراد/تعديل جماعي (CSV/Excel) للمنتجات والخصائص والترتيب.
●	إدارة المجموعات (وصل حديثًا/الأكثر مبيعًا…) يدويًا أو عبر قواعد.
●	لوحة “اكتمال المحتوى” لتنبيه الفريق بما ينقص كل منتج.
8) البحث والتصفية (على مستوى المنتج)
●	فلاتر: التصنيف، العلامة، الخصائص العامة (طول/قصّة/…)، “وصل حديثًا”، “ضمن خصم”.
●	الفرز: الأحدث، السعر تصاعد/تنازل، الأكثر مبيعًا، الأكثر مشاهدة/إضافة للسلة.
●	دعم اقتراحات البحث وتصحيح الإملاء لاحقًا.
9) قياس الأداء للقرار التجاري
●	مشاهدات المنتج → نسبة الدخول إلى التفاصيل (CTR من القوائم).
●	إضافة للسلة ونسبة التحويل من صفحة المنتج.
●	أكثر الألوان/المقاسات طلبًا.
●	معدل المرتجعات لكل منتج/نسخة (لتحسين الوصف والمقاسات).
●	نقاط اكتمال المحتوى مقابل التحويل (لاستهداف التحسين).



10) تعريف الاكتمال (Definition of Done)
●	يمكن نشر المنتج ويظهر صحيحًا بالتصنيف والصور والخصائص.
●	النسخ (السعر/التوفر) تعمل وتظهر خيارات اللون/المقاس بوضوح.
●	الشارات تظهر وفق القواعد، والمجموعات تُدار بسهولة.
●	البحث/الفلاتر تُعيد نتائج دقيقة، والفرز موثوق.
●	لوحة “اكتمال المحتوى” تعمل وتُظهر ما ينقص.
الخلاصة: “المنتج” يقدّم الهيكل والمحتوى والعلاقات، بينما “النسخة” تتكفّل بالسعر والتوفر. هذا الفصل يبقي البيانات نظيفة، ويجعل التسعير والمخزون والبحث والفلاتر تعمل بدقة—ويترجم ذلك إلى تجربة شراء أسرع ومبيعات أعلى.
 
الطلبات (Orders) 
الطلبات (Orders) 
1) الهدف
●	تسجيل الطلب بشكل دقيق من لحظة الإنشاء حتى التسليم/الإغلاق.
●	دعم COD بقوة (سوق اليمن) مع تقليل الرفض والتحصيل المتأخر.
●	ربط تلقائي بالمخزون، الشحن، المدفوعات، والمرتجعات.
●	توفير بيانات واضحة التقارير والتحليلات والتسويق.
 
2) ما الذي نحتاج بناؤه (الكيانات الأساسية)
●	الطلب (Order): رأس الطلب، الأرقام، العميل، العناوين، الإجماليات، الحالة.
●	بنود الطلب (Order Items): المنتجات/النسخ والكميات والأسعار والخصومات.
●	تاريخ الحالة (Order Status History): سجل انتقالات الحالة مع الوقت والسبب.
●	الدفع (Payments): مزوّد، حالة الدفع (النقدي/أونلاين)، مبالغ محصّلة/مستردّة.
●	الشحن (Shipments): شركة الشحن، رقم التتبع، حالات الشحن ومحاولات التسليم.
●	العناوين الملتقطة (Address Snapshot): نسخة ثابتة لعنوان الشحن داخل الطلب.
●	الخصومات والقسائم: ربط بالرموز/العروض المستخدمة في الطلب.
●	الارتباطات: المرتجعات/الاستبدالات لاحقًا + مرجع الحملات التسويقية (UTM).
 
3) الحقول الرئيسية في الطلب (مستوى الرأس)
●	المعرفات: رقم طلب مقروء (تسلسلي قصير)، معرف العميل (إن وجد)، قناة الإنشاء (التطبيق/إنستقرام/واتساب).
●	الزمن: تاريخ الإنشاء، التحديث، تواريخ المعالم (التأكيد، الشحن، التسليم).
●	الحالة:
○	حالة الطلب: pending → confirmed → packed → shipped → out_for_delivery → delivered
○	حالات جانبية: cancelled، returned، failed_delivery
●	الدفع: طريقة الدفع (COD/أونلاين)، حالة الدفع (غير مدفوع/مفوّض/محصّل/مسترد جزئيًا/كاملًا).
●	الإجماليات: المجموع قبل الخصم، إجمالي الخصم، رسوم الشحن، رسوم COD (إن وجدت)، الضرائب (إن طبقت)، الإجمالي النهائي، العملة.
●	العناوين: اسم المستلم، هاتف، مدينة/حي/علامة قريبة (دقة محلية)، ملاحظات التوصيل.
●	التسويق: promo code المستخدم، UTM (المصدر/الوسيط/الحملة) إن توفر.
●	ملاحظات: ملاحظة العميل، ملاحظة فريق العمليات.
 
4) بنود الطلب (مستوى السطر)
●	المنتج/النسخة (لون/مقاس) + السعر الملتقط لحظة الطلب (حتى لو تغيّر لاحقًا).
●	الكمية، خصم السطر (إن وجد)، المجموع الصافي للسطر.
●	سياسات: لا تُحجز كمية تتجاوز المخزون المتاح (أو يسمح بالطلب المسبق حسب الإعداد).
 
5) حالات الطلب والانتقالات (الماكينة المنطقية)
●	pending: تم الإنشاء، بانتظار تأكيد (ودفع إن كان أونلاين).
●	confirmed: تأكيد داخلي/آلي، يتم حجز المخزون.
●	packed: جُهّزت الشحنة.
●	shipped: سُلّمت لشركة الشحن ورقم تتبع موجود.
●	out_for_delivery: خرجت للتسليم.
●	delivered: تسليم ناجح (ولـ COD: تحصيل المبلغ).
●	failed_delivery: فشل/عدم رد، تُرفع محاولات التسليم ويُعاد الجدولة أو يُلغى.
●	cancelled: قبل الشحن (تحرير الحجز/الكمية) أو بعده وفق سياسة الاسترجاع.
●	returned: معالجة مرتجع مرتبطة بنفس الطلب.
يُسجَّل كل انتقال مع: من/إلى، الوقت، الفاعل (نظام/موظف/API)، السبب.
 
6) الدفع: اونلاين وCOD 
●	أونلاين: تفويض/تحصيل، فشل، رد جزئي/كامل.
●	COD:
○	أعلام تشغيلية: مسموح COD؟ درجة مخاطر العميل؟
○	عند delivered: تسجيل المبلغ المحصَّل، ثم تسوية مع شركة الشحن (remittance) لاحقًا.
○	في failed_delivery: زيادة عدّاد الفشل للعميل/العنوان لاتخاذ إجراءات مستقبلية.
 
7) المخزون والحجز
●	عند confirm: حجز الكمية (reservation).
●	عند cancelled قبل الشحن: تحرير الحجز.
●	عند delivered: خصم نهائي من المخزون.
●	مهلة حجز (TTL) لعربات/طلبات غير مكتملة لتفادي حبس المخزون بلا داعٍ.
 

8) الشحن والتتبع
●	ربط الطلب بواحدة أو أكثر من الشحنات (يدعم التجزئة عند الحاجة).
●	حقول الشحن: شركة الشحن، رقم التتبع، حالة الشحن، محاولات التسليم، أوقات الشحن/التسليم.
●	موافقة على SLA داخلية:
○	من confirmed → packed خلال X ساعات.
○	من packed → shipped خلال X ساعات.
○	من shipped → delivered خلال Y أيام (حسب المدينة).
 
9) الإلغاء، الاسترجاع، الاستبدال
●	الإلغاء: قبل الشحن مجانًا غالبًا؛ بعد الشحن وفق السياسة.
●	الاسترجاع: نافذة زمنية (مثلاً 7–14 يومًا)، سبب (مقاس/عيب/تأخر)، حالة العنصر المرتجع، طريقة التعويض (استرداد/رصيد متجر/استبدال).
●	الاستبدال: إنشاء طلب جديد مرتبط بالمرتجع الأصلي.
 
10) قواعد التسعير والخصومات
●	الخصم قد يكون على السطر أو على الطلب كاملًا (promo code).
●	تُحفظ القيم الملتقطة لحظة إنشاء الطلب (سعر/خصم/شحن) لضمان الاتساق.
●	سياسة التقريب والكسور واضحة على مستوى العملة.
●	رسوم COD إن طُبّقت تُحسب وتظهر للعميل قبل التأكيد.
 
11) مكافحة الاحتيال والجودة (خصوصًا COD)
●	إشارات تحذير: تكرار إلغاء/فشل تسليم، أرقام مكرّرة، عناوين عالية المخاطر، حجم طلب غير اعتيادي لأول طلب.
●	إجراءات: تأكيد واتساب/اتصال قبل الشحن لطلبات محددة، OTP للتأكيد عند الحاجة.
●	قوائم حظر أو تقييد COD تلقائيًا عند تجاوز عتبات محددة.
 
12) الإشعارات والتواصل مع العميل
●	رسائل عند: إنشاء الطلب، التأكيد، الشحن (برابط تتبع)، الخروج للتسليم، التسليم، الفشل/إعادة الجدولة.
●	القنوات: Push / SMS / واتساب (حسب الموافقات)، مع روابط عميقة لصفحة الطلب.
 
13) التكاملات والتحليلات
●	إرسال أحداث رئيسية إلى Firebase/GA4: begin_checkout, add_payment_info, purchase, وأحداث حالات الشحن.
●	ربط الطلب بـ UTM المصدر/الوسيط/الحملة إن توفر لقياس القنوات.
●	تقارير تشغيلية: نسبة التحويل من confirmed→delivered، معدل فشل COD، متوسط زمن المعالجة، الطلبات حسب المدينة/شركة الشحن/القناة.
 
14) معايير القبول (Definition of Done)
●	إنشاء طلب كامل ببيانات عميل وعنوان ملتقطة وإجماليات صحيحة.
●	حالات الطلب تعمل بانتقالات صحيحة ويُسجل تاريخ الحالة.
●	ربط بنود الطلب بالمنتجات/النسخ بأسعار ملتقطة.
●	دفع COD/أونلاين يعمل مع سيناريوهات الفشل/الرد.
●	الحجز/التحرير للمخزون يعمل دون أخطاء أو حجز دائم.
●	شحنة واحدة على الأقل لكل طلب قابل للشحن، مع رقم تتبع وحالات شحن.
●	إشعارات العميل تُرسل حسب الحالة ووفق موافقات القنوات.
●	لوحات تقارير أساسية متاحة (تحويل، فشل COD، زمن المعالجة).
 
15) سيناريوهات حافة يجب دعمها
●	انقسام الشحنة: صنف غير متوفر يُشحن منفصلًا، مع تحديث الإجماليات والتواصل.
●	استرداد جزئي: مرتجع جزئي بعد التسليم (أونلاين أو رصيد متجر).
●	فشل تحصيل COD مع تسليم: استثناءات نادرة—تسوية داخلية وإجراءات صارمة لاحقة.
●	تعديل عنوان بعد التأكيد: يسمح قبل الشحن فقط ومع تسجيل السبب.
●	إلغاء شركة الشحن بعد محاولات فاشلة: إغلاق الطلب وتحديث ملف مخاطر العميل.
 
16) تشغيلات مختصرة (SOPs)
●	مراجعة يومية للطلبات pending لأكثر من X ساعات.
●	متابعة شحنات out_for_delivery نهاية اليوم (تأكيد نجاح/جدولة إعادة محاولة).
●	تسويات أسبوعية مع شركات الشحن لمبالغ COD.
●	مراجعة أسباب failed_delivery وتصحيحها (عناوين/شركة شحن/تواصل).
 

 
السلة (Cart) 
السلة (Cart) 
لماذا نفصل السلة عن المفضلة؟
●	اختلاف النية: السلة = نية شراء فورية؛ المفضلة = حفظ للاطلاع لاحقًا.
●	الأداء والعمر الافتراضي: السلة لها TTL ومراجعة مخزون/سعر لحظية؛ المفضلة طويلة العمر ولا تحجز موارد.
●	الرسائل والتحويل: تذكير “سلة مهجورة” لا ينطبق على المفضلة.
●	التحليلات: فصل مصدر الحقيقة لمعدلات التحويل والمهجورة عن سلوك “إعجاب”.
●	الصيانة: تغييرات التسعير/المخزون تؤثر على السلة فقط، وتسهل الاختبارات.
 
1) الهدف من السلة
●	تمكين الإضافة والتعديل بسرعة مع سعر وتوفّر دقيقين لحظيًا.
●	دعم الدمج بين الأجهزة عند التوثيق.
●	تجهيز الدخول السلس إلى الدفع (checkout) وتقليل فقدان الطلبات. 
 
2) الكيانات (بدون تفاصيل تقنية)
أ) السلة (Cart) 
●	الهوية: cart_id، customer_id (إن وُجد)، anonymous_id/device_id، القناة (app/…)
●	الحالة: active / converted / abandoned
●	العملة: currency
●	المجاميع التقديرية: subtotal، discount_total، shipping_estimate، tax_estimate (إن وُجد)، cod_fee_estimate (إن وُجد)، grand_total_estimate
●	العنوان (اختياري): مرجع عنوان لإظهار تقدير الشحن
●	الكوبونات: promo_code المطبّق + سبب الرفض إن فشل
●	التواريخ: created_at، last_activity_at، expires_at (إن لزم)
●	ملاحظات: حقل حر (اختياري)
ب) بنود السلة (Cart Items)
●	التعريف: product_id، variant_id (مصدر اللون/المقاس)
●	الكمية: qty (مع حد أقصى لكل صنف إن وُضع) 
●	التسعير: السعر الحالي، والسعر عند الإضافة  (للمقارنة فقط)
●	التوفّر: حالة لحظية تُعاد مراجعتها عند كل فتح سلة/تعديل
●	ملاحظات اختيارية (مثلاً ملاحظة مقاس) 
 
3) قواعد العمل (Business Rules)
●	الإضافة والتعديل
○	لا تُقبل كمية تتجاوز المتاح؛ تُقصّ تلقائيًا لأقصى حد مع تنبيه.
○	عند تغيّر السعر/التوفّر: تُعرض شارة “سعر محدّث/غير متوفر”.
●	التسعير
○	السلة دائمًا تعكس السعر الحالي؛ لا “قفل سعر” إلا عند إنشاء الطلب.
○	العروض تُطبَّق تلقائيًا إن انطبقت قواعدها.
●	الكوبونات
○	التحقّق فور الإدخال وأي تعديل بالسلة.
○	سياسة التراكم واضحة (مثلاً كوبون واحد فقط). 
●	الشحن والضرائب/رسوم COD (تقديرية) 
○	تحتاج مدينة/حي لإظهار تقدير دقيق؛ بدونها يُعرض نطاق/متوسط.
●	الهوية والدمج
○	يبدأ المستخدم ضيفًا؛ عند توثيق الهاتف تُدمَج سلة الضيف بسلة العميل  (تجميع نفس الـvariant).
●	المهلة (TTL) والسلة المهجورة
○	تعتبر السلة مهجورة بعد عدم نشاط لمدة 7 أيام (قابلة للضبط). 
○	تنظيف سلال الضيوف الخاملة دوريًا (مثلاً بعد 30–60 يومًا).
●	الحجز
○	لا حجز مخزون أثناء التصفح. يُسمح بحجز خفيف فقط أثناء الدفع وحتى التأكيد.
 
4) التدفقات التشغيلية
1.	إضافة للسلة: تحقق لحظي من السعر/المخزون → تحديث المجاميع.
2.	بدء الدفع (Begin Checkout): إعادة تحقق شامل (سعر/توفر/كوبون/شحن).
3.	التوثيق/الدخول: دمج سلة الضيف مع سلة العميل فورًا.
4.	إنشاء الطلب: التحقق الأخير + حجز خفيف → عند النجاح تتحول السلة إلى converted.
 
5) التكاملات المطلوبة
●	الكتالوج/المخزون: جلب السعر والتوفر من النسخة (Variant) أثناء كل تعديل.
●	العروض/الكوبونات: تطبيق القواعد فورًا على السلة.
●	الشحن: خدمة تقدير التكلفة حسب الوجهة والوزن/الحجم (إن لزم).
●	المدفوعات: تمرير المجاميع النهائية إلى الدفع (مع رسوم COD إن طُبّقت).
●	التحليلات/الرسائل: إرسال أحداث add_to_cart, begin_checkout; تفعيل تذكير مهجور عبر Push/SMS/WhatsApp حسب الموافقات. 
 
6) مؤشرات الأداء (KPIs)
●	Add-to-Cart من صفحات المنتج والقوائم.
●	Begin Checkout → Purchase Conversion.
●	قيمة وعدد السلال المهجورة حسب القناة/الفئة.
●	أكثر العناصر إضافةً، وأبرز أسباب فشل التحويل (نفاد/سعر/شحن).
 
7) معايير القبول (Definition of Done)
●	إضافة/إزالة/تعديل كميات  تعمل بسلاسة وبدون تضارب مخزون.
●	الأسعار والتوفّر محدّثة دائمًا مع تنبيهات واضحة عند تغيّره ا.
●	دمج سلة الضيف مع سلة العميل عند التوثيق دون فقد عناصر.
●	الكوبونات تُقبل/تُرفض برسائل مفهومة وتؤثّر على المجاميع فورًا.
●	تقدير الشحن/COD يظهر بدقة عند توافر العنوان.
●	التحويل إلى طلب يتم بدون أخطاء، والسلة تُوسَم converted.
 
8) سيناريوهات حافة
●	تغيّر السعر بعد الإضافة: تحديث السعر وعرض شارة تنبيه. 
●	نقص المخزون عند الدفع: تقليل الكمية لأقصى حد متاح مع تنبيه.
●	صنف أزيل/أرشف: يُزال من السلة مع إشعار المستخدم. 
●	سلتان لنفس العميل من جهازين: تُدمج عند أول مزامنة. 
●	تعارض كوبونات: اتباع سياسة ثابتة (مثلاً الأحدث يحل محل السابق). 
 
9) خارطة إصدارات
●	MVP: سلة ضيف/عميل، دمج عند التوثيق، تحقق لحظي سعر/مخزون، كوبون واحد، تقدير شحن أساسي، تذكير مهجور بعد 24–72 ساعة.
●	المرحلة 2: حدود شراء لكل SKU، قواعد كوبونات متقدمة، حفظ سلة أطول للضيوف.
●	المرحلة 3: توصيات داخل السلة (Cross-sell/Bundle)، تقدير شحن دقيق متعدد الشركات، A/B لاختبار رسائل المهجورة.
 
علامة التبويب 28 
الهدف
●	تحديد المنتجات الأكثر إضافةً إلى السلة بدقة (SKU/SPU/فئة).
●	تشخيص أسباب فشل التحويل داخل السلة مع نسب وتأثير مالي (نفاد المخزون، السعر، الشحن).
●	إنتاج لوحة قياس عملية ترتّب “قائمة أولويات الإصلاح”.
مصادر البيانات المطلوبة (ملخّص)
●	سلوك المستخدم: add_to_cart، remove_from_cart، begin_checkout، view_shipping, shipping_quote_shown, apply_coupon, price_view, payment_failed، exit_step.
●	حالة المخزون للحظة التفاعل: available_qty, reserved_qty, backorder_flag, restock_eta.
●	التسعير: list_price، current_price، campaign_price، competitor_gap (إن وُجد)، price_changed_flag.
●	الشحن: shipping_zone, delivery_eta, shipping_fee, cod_allowed, serviceable (y/n).
●	بنية السلة: cart_id، user_id، line_id، sku، qty، timestamps.
I) أكثر العناصر إضافةً (Top Added Items)
التعاريف
●	“إضافة” = كل حدث add_to_cart ناجح (بعد تحقق القيود: المقاس/اللون…).
●	TAI_Units: إجمالي الوحدات المضافة لكل SKU خلال فترة محددة.
●	TAI_Users: عدد المستخدمين الفريدين الذين أضافوا SKU.
●	TAI_Rate: (عدد جلسات أضيف فيها SKU) ÷ (جلسات شاهدت SKU).
●	Net Adds: الإضافات − الإزالات (remove_from_cart) لنفس الفترة.
التقارير الأساسية
1.	قائمة Top-N حسب:
○	TAI_Units (افتراضي)، مع عرض TAI_Users وTAI_Rate وNet Adds.
2.	تفصيل بالبعد:
○	اللون/المقاس، الفئة، المصدر التسويقي، المنطقة.
3.	جودة المخزون لمفضّلات العملاء:
○	%النفاد خلال زيارات السلة لكل SKU، restock_eta المتوسط.
4.	حساسية السعر:
○	نسبة الإزالات بعد price_changed_flag أو بعد عرض الشحن.
قواعد العرض والفرز
●	الفرز الأساسي: TAI_Units ثم TAI_Rate.
●	استبعد SKUs بنشاط احتيالي/اختبارات داخلية (internal traffic).
●	طبّق حدًا أدنى للظهور (≥ 200 مشاهدة SKU أو ≥ 50 إضافة) لتجنّب الضجيج.
II) أسباب فشل التحويل في السلة (نفاد/سعر/شحن)
السبب = أقوى عامل قابل للإثبات “عند آخر تفاعل ذي صلة” قبل الخروج أو قبل فشل الطلب.
1) نفاد المخزون (OOS)
تعريف السبب:
●	المنتج أو أي متغير منه أصبح available_qty ≤ 0 عند:
○	محاولة “التوجّه للدفع” أو
○	تحديث الكمية في السلة أو
○	ظهور رسالة OOS/Not serviceable في الـUI.
●	أو تم تقليص الكمية تلقائيًا (auto-reduce) قبل الدفع.
إثبات الحدث (signals):
●	oos_message_shown=true، أو server_response=“OUT_OF_STOCK”.
●	اختلاف qty قبل/بعد التحديث (مثلاً من 2 إلى 1).
●	restock_eta معروف (اختياري للمعالجة اللاحقة).
مؤشرات تعرض:
●	OOS Rate = عدد سلال شهدت OOS ÷ إجمالي سلال وصلت لمرحلة مراجعة السلة.
●	Lost Units = الفرق بين qty المطلوبة والمتاحة.
●	Lost Revenue (estimate) = Lost Units × current_price.
أولويات الإصلاح:
●	SKUs ذات TAI_Units عالية + OOS Rate مرتفع + restock_eta بعيد.
2) السعر (Price)
تعريف السبب:
●	price_changed_flag بين وقت الإضافة ووقت المراجعة (زيادة).
●	غياب الخصم/القسيمة المتوقعة (coupon_rejected، campaign_not_applied).
●	فجوة سعرية كبيرة مقابل مرجع داخلي (مثلاً أعلى من P90 لفئة مماثلة) أو مقابل منافس إن متاح.
إثبات الحدث:
●	remove_after_price_change خلال ≤ 2 ساعات من price_changed_flag.
●	abandon بعد apply_coupon_failed أو بعد view_price_rules.
●	bounce عند صفحة “المجموع” دون بدء الدفع.
مؤشرات تعرض:
●	Price-Abandon Rate = سلال شهدت price_change أو coupon_failed ثم لم تبدأ الدفع.
●	Net Adds→Removals بعد عرض الرسوم النهائية.
●	Elasticity Proxy: نسبة الإزالات عند زيادات سعرية صغيرة (مثلاً +5%).
أولويات الإصلاح:
●	منتجات “Top Added” مع أعلى Price-Abandon Rate.
●	سيناريوهات “خصم موعود غير مطبّق” (تصحيح قواعد الكوبون/الحملة).
3) الشحن (Shipping)
تعريف السبب:
●	shipping_quote_shown وبعده exit خلال ≤ 10 دقائق بدون بدء الدفع.
●	shipping_fee أعلى من عتبة المنطقة (threshold) أو delivery_eta طويل.
●	المنطقة غير مخدومة (serviceable=false) أو COD غير متاح لعنوان العميل.
إثبات الحدث:
●	provider_code=“ZONE_NOT_SERVICEABLE”/“COD_NOT_ALLOWED”.
●	زيادة واضحة في remove_from_cart بعد عرض رسوم/مدة الشحن.
●	انتقال المستخدم بين طرق شحن ثم خروج (change_shipping_method≥2 ثم exit).
مؤشرات تعرض:
●	Shipping-Abandon Rate = سلال رأت عرض الشحن ثم غادرت قبل begin_checkout.
●	% Non-serviceable by city/zone.
●	تأثير تكلفة الشحن: معامل ارتباط بين shipping_fee وبدء الدفع لكل شريحة.
أولويات الإصلاح:
●	مناطق ذات Non-serviceable أعلى وتأثير إيرادي كبير.
●	SKUs ثقيلة/كبيرة مع أعلى Shipping-Abandon.
أسبقية السبب عند تزامن عوامل متعددة
1.	نفاد المخزون (سبب حتمي يمنع الشراء).
2.	الشحن (عدم الخدمة/تكلفة/مدة تُعدّ مانعًا وظيفيًا).
3.	السعر (عامل قرار، يُسجّل إن لم يوجد 1 أو 2).
سجّل السبب الرئيسي وسببًا ثانويًا إن وُجد، لكن اعتمد الرئيسي في التقارير الافتراضية.
III) لوحة “قائمة أولويات الإصلاح” (Fix Queue)
●	لكل SKU/فئة:
1.	حجم الطلب: TAI_Units وTAI_Users
2.	معدل فشل التحويل لكل سبب (OOS/Price/Shipping)
3.	الإيراد المفقود التقديري لكل سبب
4.	“درجة الأولوية” = تطبيع (0–100) من: حجم الإضافة × (معدل الفشل) × (الإيراد المفقود)
●	فلترة بحسب: مصدر تسويقي، مدينة، جهاز، شريحة (VIP، مهجور سلة).
IV) قراءات قياسية/أهداف
●	OOS Rate في السلة < 2% لمنتجات Top-100.
●	Price-Abandon بعد تغيّر السعر < 10%.
●	Shipping-Abandon بعد عرض الرسوم < 12% (يتفاوت حسب السوق).
●	استعادة 20–30% من مهجوري الشحن عبر بدائل الدفع/الشحن.
V) قرائن مساندة (لتحسين الدقة)
●	استبيان خروج سريع (اختياري): زر “لماذا لم تكملين؟” بخيارات (السعر/الشحن/الوقت/طريقة الدفع)، يُستخدم للمعايرة.
●	دمج بيانات دعم العملاء (Tags: “غالي”، “لا يشحن لمنطقتي”).
●	تتبّع رسائل الخطأ/التنبيهات المعروضة للمستخدم كـ signals رسمية.
VI) جودة البيانات والحوكمة
●	ضبط المنطقة الزمنية “Asia/Aden” لكل المقاييس.
●	منع ازدواج الأحداث (مثلاً add_to_cart المتكرر لنفس line_id).
●	استبعاد حركة داخلية/اختبارات (قائمة allowlist للأجهزة/المستخدمين).
●	مراقبة التناسق: أي SKU يظهر Top Added ثم صفر طلبات أسبوعًا كاملًا ⇒ تحقق من بوابة الشحن/الدفع.
VII) إجراءات سريعة بناءً على النتائج
●	نفاد: رفع نقاط إعادة الطلب، تمكين بدائل/ألوان، إظهار restock_eta، تفعيل “إشعار إعادة التوفر”.
●	السعر: تثبيت تسعير متّسق حتى نهاية الجلسة، مراجعة سياسات القسائم، إبراز القيمة (جودة/خامة/مقارنة).
●	الشحن: تخفيض شحن مناطق رئيسية، تمكين COD انتقائي مع حد قيمة، إضافة خيار “استلام من نقطة تسليم” إن أمكن.
 
علامة التبويب 29 
آلية معيارية لإدارة الكوبونات المدخلة يدويًا والكوبونات التلقائية داخل السلة والدفع،
الهدف
●	تطبيق أفضل خصم ممكن للمستخدم مع وضوح القواعد.
●	منع التعارضات/التكديس غير المرغوب.
●	تسجيل أسباب القبول/الرفض للتدقيق والتحليل.
1) التعاريف
●	Manual Coupon: كود يدخله المستخدم (مثل VIP20).
●	Auto Coupon/Promotion: خصم يُحتسب تلقائيًا إذا تحققت شروط (أول طلب، حد سلة، فئة، شريحة…).
●	Benefit Type: نوع المنفعة (نسبة %، مبلغ ثابت، شحن مجاني، هدية/BxGy، كاش باك).
●	Eligibility: شروط الاستحقاق (قيمة سلة، منتجات/فئات مسموحة/مستثناة، قناة، شريحة، طريقة دفع، مدينة…).
●	Stacking: إمكانية الجمع بين خصمين أو أكثر.
●	Suppression: إيقاف عرض/تطبيق عرض تلقائي عندما يطبَّق عرض أعلى أولوية.
2) قواعد عامة (Policy)
1.	ضمان أفضل سعر: النظام يحسب جميع العروض المؤهَّلة ويختار مجموعة الخصومات المسموح جمعها التي تعطي أقل إجمالي صافٍوفق قواعد التكديس.
2.	أولوية المقصد:
○	(أ) أكواد فريدة/دعوات (Single-use/Referral/Influencer) أعلى أولوية، ولا تتكدّس مع خصومات نقدية أخرى.
○	(ب) الكود اليدوي المُدخل في الجلسة الحالية يسبق العروض التلقائية إن قدّم سعرًا أفضل.
○	(ج) العروض التلقائية تُطبَّق “أفضل خيار تلقائي” عند عدم وجود كود يدوي مؤهَّل أفضل.
3.	مصفوفة التكديس (Combinability Matrix):
○	خصم نقدي (٪ أو مبلغ) ⇢ لا يتكدّس مع خصم نقدي آخر.
○	“شحن مجاني” ⇢ يمكن أن يتكدّس مع خصم نقدي واحد.
○	“هدية/BxGy” ⇢ التكديس مسموح إذا لم تخصم من نفس البنود وبشرط ألا تتجاوز الحد الأقصى للخصم.
○	“كاش باك” ⇢ يمكن تكديسه مع واحد نقدي أو شحن مجاني (اختر واحد نقدي فقط).
4.	الحد الأقصى للخصم (Cap): لكل طلب حد أقصى نسبي/مطلق يقي القيود المالية حتى عند التكديس المسموح.
5.	الأولوية داخل الفئة الواحدة: في العروض التلقائية ذات الطبقات (Threshold Tiers) طبّق أعلى طبقة مؤهَّلة فقط.
6.	شفافية الواجهة: إن وجد كود يدوي أضعف من عرض تلقائي، أظهري للمستخدم خيارين:
○	“استخدام الكود اليدوي” (يُطبّق الكود ويُوقَف التلقائي)
○	“الحفاظ على أفضل خصم” (يُقمع الكود اليدوي ويُحفظ في الحقل لتجربته لاحقاً)
7.	طريقة الدفع/المخاطر: يمكن تقييد خصومات معينة بـ الدفع المسبق فقط أو حجبها عن COD_RISK_HIGH.
8.	عدم الرجعية: بعد إنشاء الطلب، لا يُعاد تسعيره تلقائيًا إذا تغيّر الكوبون/العرض.
3) نموذج البيانات (ملخّص حقول لازمة)
●	promotions: code/null, benefit_type, value, max_discount, start/end, channel, stacking_rule, priority, scope (basket/item/shipping), audience (segment/region/payment), usage_limits(per_user/per_campaign/global), eligible_categories/skus, exclusions, is_unique, owner(influencer/referral).
●	promotion_ledger: سجل محاولات التطبيق: cart_id, code, auto_flag, eligible(y/n), reject_reason, estimated_saving, applied(y/n), suppressed_by.
●	cart_lines snapshot عند التسعير: الأسعار قبل/بعد الخصم، البنود المتأثرة، سبب التغيير.
4) ترتيب التقييم (Evaluation Pipeline)
1.	جمع المرشّحين:
○	الكود اليدوي (إن وُجد) + جميع العروض التلقائية المستوفية للشروط.
2.	التحقق من الأهلية لكل مرشح: الشروط، الحدود، القنوات، الشريحة، طريقة الدفع، المنتجات المستثناة.
3.	تجميع المرشّحين وفق مصفوفة التكديس لتكوين حالات تسعير محتملة (Scenarios).
4.	حساب صافي السلة لكل سيناريو + تطبيق Cap.
5.	اختيار السيناريو الأفضل (أقل إجمالي، مع كسر التعادل بالأولوية priority ثم المنفعة الأشمل “basket > shipping > item”).
6.	القمع/التوضيح: وسم العروض غير المختارة كـ suppressed مع سبب واضح.
7.	تثبيت النتيجة حتى تغيّر جوهري (تبديل كود، تغيير كمية، تغيير شحن/عنوان/طريقة دفع).
5) أسباب الرفض/القمع القياسية (Reason Codes)
●	not_eligible_min_basket (لم يتحقق حد السلة)
●	product_excluded (منتج/فئة خارج النطاق)
●	payment_method_blocked (طريقة الدفع غير مؤهَّلة)
●	region_not_serviceable (المنطقة غير مدعومة/رسوم مخصّصة)
●	usage_limit_reached_user/global
●	coupon_expired/not_started
●	stacking_conflict (تعارض مع خصم نقدي آخر)
●	better_auto_applied (عرض تلقائي أفضل)
●	risk_blocked (حظر بسبب درجة مخاطرة COD)
تُسجَّل في promotion_ledger لكل محاولة، وتُستخدم في التقارير وتحسين الحملات.
6) سيناريوهات معيارية
●	أول طلب 10% (تلقائي) + يدوي 15% ⇢ يطبَّق 15% ويُقمع التلقائي (better_auto_applied=false).
●	يدوي 20% + شحن مجاني تلقائي ⇢ يُسمح بالتكديس (نقدي واحد + شحن مجاني).
●	BxGy تلقائي + يدوي 10% ⇢ إذا كان BxGy يخصم من نفس البنود، اختاري الأفضل فقط؛ إن كانت الهدية على بنود أخرى، يمكن التكديس مع Cap.
●	كود مؤثر (Unique) ⇢ يمنع أي خصم نقدي آخر؛ يبقى الشحن المجاني قابلًا للتكديس إن سمح إعداد الكود.
●	COD_RISK_HIGH ⇢ يمنع خصومات نقدية > X%، ويسمح بشحن مجاني فقط (حسب السياسة).
●	تحويل طريقة الدفع إلى مسبق ⇢ يفتح خصم Payment Boost تلقائيًا ويُعاد التقييم.
7) السلوك في الإرجاع/الإلغاء
●	توزيع الخصم على البنود بنسبة مساهمتها في الإجمالي قبل الخصم.
●	عند الإرجاع الجزئي: يُعاد احتساب الحسم على البنود المعادة، ويُسترد المبلغ المناسب فقط.
●	عند إلغاء كامل: تُزاد عدّادات الاستخدام (usage_limits) إن كانت تُخصم عند إنشاء الطلب.
8) واجهة المستخدم (نقاط إلزامية)
●	شارة “تم تطبيق أفضل خصم تلقائيًا” مع إمكانية “استخدام كود آخر”.
●	عند إدخال كود أضعف: تنبيه “الكود يمنح خصمًا أقل من العرض الحالي” مع خيار الاستبدال.
●	كشف تفصيلي: (الخصم النقدي، الشحن المجاني، هدية) + إجمالي التوفير.
●	رسائل سبب الرفض من Reason Codes أعلاه بصياغة مفهومة.
9) الضبط والحوكمة
●	لوائح Limits افتراضية:
○	لكل مستخدم: حد استخدام/حملة (مثلاً 1–2)
○	لكل طلب: خصم نقدي واحد + شحن مجاني + (اختياري) هدية
○	Cap افتراضي: لا يتجاوز X% من إجمالي السلة
●	استثناءات تُدار عبر priority وis_unique.
●	استبعاد حركة داخلية/اختبار من العدّادات.
10) التقارير والمؤشرات
●	Acceptance Rate لكل كود/حملة (محاولات ⇢ تطبيقات).
●	Suppression Map: ما أكثر العروض التي تُقمع ولماذا (يُرشد لتبسيط القواعد).
●	Avg Discount % / Order وImpact on AOV وGross Margin.
●	Leakage: محاولات رفض بسبب usage_limit_reached أو not_eligible_min_basket.
●	Cross-channel: أداء أكواد المؤثرين مقابل التلقائي لكل مصدر/شريحة.
11) اختبار (QA) مختصر
●	إدخال كود صالح + تلقائي أقوى ⇒ يُحترم الأفضل وتظهر رسالة توضيح.
●	طبقات تلقائية (100/200/300) ⇒ عند تغيّر قيمة السلة تُطبَّق أعلى طبقة فقط.
●	منع جمع خصمين نقديين ⇒ تحقّق من تطبيق Cap وسبب stacking_conflict.
●	تغيير العنوان/المنطقة ⇒ إعادة تقييم الشحن وسبب region_not_serviceable.
●	إرجاع جزئي ⇒ التوزيع النسبي للخصم سليم.
 
Check 
●	 جداول/حقول الحملات مع benefit_type وstacking_rule وpriority وusage_limits.
●	 مسار تقييم موحّد (pipeline) يُعيد السيناريو الأفضل + تفسير (explain) + أسباب الرفض.
●	 تسجيل كامل في promotion_ledger (eligible/applied/suppressed + reasons).
●	 مصفوفة تكديس مطبّقة كما في القسم (3).
●	 سياسات الإرجاع وتوزيع الخصم النسبي مفعّلة.
●	 واجهة رسائل واضحة للمستخدم.
●	 تقارير قبول/قمع وتأثير مالي أسبوعية.
 
المفضّلة (Wishlist) 
المفضّلة (Wishlist)
1) الهدف
●	حفظ المنتجات التي تهم العميلة للعودة لاحقًا.
●	رفع العودة للتطبيق والتحويل عبر إشعارات عودة التوفر وهبوط السعر .
●	دعم مشاركة قوائم مختارة (اختياري) لتحفيز الشراء.
 
2) النطاق
●	قائمة مفضّلة لكل عميلة (واحدة كحد أدنى)، مع خيار عدّة قوائم لاحقًا.
●	عناصر المفضّلة على مستوى المنتج أو النسخة (الأفضل النسخة إذا كان اللون/المقاس مهمّين). 
●	إعدادات إشعارات: عند التوفّر، عند هبوط السعر (اختياري تشغيل/إيقاف لكل عنصر).
●	مشاركة القائمة برابط عام للعرض فقط (اختياري في مرحلة لاحقة). 
 
3) الهوية والربط
●	الافتراضي: المفضّلة للمستخدم المسجّل (مرتبطة بـ customer_id).
●	للضيف: مفضّلة مؤقتة على الجهاز؛ تُدمَج تلقائيًا مع حساب العميلة عند التوثيق (مع إزالة التكرارات). 
●	المزامنة بين الأجهزة بعد الدخول. 
 
4) الحقول (مستوى المفهوم، بدون تفاصيل تقنية)
أ) المفضّلة
●	المعرف، customer_id، الاسم (لعدّة قوائم لاحقًا)، is_default، is_public (اختياري)، رابط مشاركة (token)، أوقات الإنشاء/التحديث، items_count. 
ب) عنصر المفضّلة
●	product_id و/أو variant_id (الأولوية للـ variant عندما يغيّر اللون الصور).
●	added_at، notes (اختياري للعميلة).
●	إعدادات الإشعارات: notify_when_in_stock، notify_on_price_drop. 
●	معلومات مرجعية للعرض: السعر الحالي، حالة التوفّر الحالية (تُحدَّث عند الفتح، ليست حقلًا ثابتًا). 
●	(اختياري) price_at_add لعرض “انخفض السعر منذ الإضافة”. 
 
5) قواعد العمل
●	لا تأثير للمفضّلة على المخزون أو التسعير.
●	منع التكرار: لا يتكرر نفس المنتج/النسخة داخل القائمة. 
●	حد أقصى منطقي لعناصر المفضّلة (مثلاً 500 عنصر للقائمة الواحدة). 
●	العناصر المرتبطة بمنتجات مؤرشفة/محذوفة: تُخفى مع رسالة توضيح، وخيار إزالة سريعة. 
●	المستوى الأفضل للإضافة: variant (حتى تظهر الصور الصحيحة مع اللون).
●	الإشعارات:
○	عودة التوفّر: تُرسل مرة عند الانتقال من غير متاح → متاح، مع فترة تهدئة (مثلاً 7 أيام) لنفس العنصر لنفس العميلة.
○	هبوط السعر: تُرسل عند انخفاض ≥ نسبة محددة (مثلاً 10%) أو قيمة مطلقة، مع فترة تهدئة مشابهة. 
○	تُحترم موافقات القنوات (Push/SMS/WhatsApp).
●	المشاركة: القوائم العامة قراءة فقط عبر رابط، ويمكن للزائر استنساخ العناصر إلى مفضّلته بعد الدخول. 
 
6) التدفقات التشغيلية
1.	إضافة إلى المفضّلة من صفحة المنتج/القائمة (زر قلب).
2.	إزالة/تنظيم: إزالة فردية، إزالة الكل، فرز بحسب “أُضيفت مؤخرًا/السعر/التوفّر” .
3.	نقل إلى السلة: “نقل” أو “إضافة” مع التحقق من اللون/المقاس المتوفر.
4.	دمج الضيف عند الدخول: اتحاد القوائم وإزالة التكرارات.
5.	إشعارات: مهمة يومية/فورية تتحقق من تغيّر التوفّر/السعر وتُرسل رسائل مقيّدة بموافقات القنوات.
6.	مشاركة (اختياري): توليد رابط للقائمة، مع صفحة عرض عامة، وخيار “نسخ إلى مفضلتي”.
 
7) التكاملات
●	الكتالوج/المخزون: قراءة حالة النسخة والتسعير لحظيًا لعرضها داخل المفضّلة.
●	العروض/التسعير: مقارنة السعر الحالي وprice_at_add لتحديد “هبوط السعر”.
●	الرسائل (FCM/SMS/WhatsApp): إرسال الإشعارات مع Deep Links مباشرة إلى المنتج/النسخة.
●	التحليلات (GA4/Firebase): add_to_wishlist, remove_from_wishlist, view_wishlist , share_wishlist , wishlist_to_cart , notif_open_back_in_stock , notif_open_price_drop .


 
8) مؤشرات الأداء
●	نسبة المستخدمين الذين يستخدمون المفضّلة، ومتوسط العناصر لكل مستخدم.
●	تحويل من المفضّلة إلى الشراء (Wishlist → Purchase) وزمن التحويل.  
●	أداء إشعارات عودة التوفّر وهبوط السعر (فتح/نقر/شراء).
●	أكثر العناصر حفظًا، والعناصر التي تُحفظ طويلًا دون شراء.
●	الرفع في AOV عندما تنتقل العناصر من المفضّلة إلى السلة.
 
9) معايير القبول (Definition of Done)
●	عميلة مسجّلة: تملك مفضّلة افتراضية ويمكنها الإضافة/الإزالة والتنظيم.
●	ضيفة: تملك مفضّلة محلية تُدمج دون تكرار عند الدخول.
●	عرض فوري لحالة التوفّر والسعر الحالي داخل المفضّلة.
●	“نقل إلى السلة” يعمل ويطلب اختيار المقاس/اللون عند الحاجة.
●	إشعارات عودة التوفّر/هبوط السعر تعمل، مع احترام الموافقات وفترات التهدئة.
●	(اختياري) مشاركة قائمة تنشئ رابطًا للعرض فقط ويمكن استنساخها بعد الدخول.
 
10) سيناريوهات حافة
●	تغيّر الصور حسب اللون: عند حفظ variant مختلف، يجب تبديل الصور وفق اللون عند العرض.
●	قيود إقليمية/عملة: لو تغيّرت العملة أو السوق، تُعرض الأسعار حسب واجهة السوق الحالي.
●	عناصر اشتريت لاحقًا: خيار “إخفاء العناصر المشتراة” تلقائيًا X يومًا. 
●	قوائم ضخمة: صفحات/تحميل كسول مع بحث داخل المفضّلة .
●	منتج أصبح مؤرشفًا: يظهر كتالي “لم يعد متاحًا” مع زر إزالة. 
 
11) خارطة الإصدارات
●	MVP (موصى به للإطلاق):
○	مفضّلة واحدة خاصة لكل مستخدم مسجّل + مفضّلة ضيف تُدمج عند الدخول.
○	إضافة/إزالة/نقل إلى السلة، عرض السعر والتوفّر الحاليين.
○	إشعار عودة التوفّر (Push) مع Deep Link.
●	المرحلة 2:
○	عدّة قوائم بأسماء (سهرة/يومي/هدايا). 
○	إشعار هبوط السعر مع عتبة ونطاقات تهدئة.
○	مشاركة قائمة برابط للعرض فقط.
●	المرحلة 3:
○	اقتراحات ذكية داخل المفضّلة (تكميلي/بدائل متاحة)، فرز متقدّم، تصفية داخل المفضّلة. 
 
المدفوعات (Payments) — المتطلبات المعتمدة 
المدفوعات (Payments)
1) الهدف
●	قبول المدفوعات أونلاين والدفع عند الاستلام (COD) بكفاءة وأمان.
●	تقليل فشل الدفع ورفع نسبة التحويل.
●	تسوية دقيقة للأموال: بوابة الدفع، وتحصيلات شركات الشحن للـCOD.
●	دعم الاسترداد الجزئي/الكامل والاعتراضات (Chargebacks) عند الحاجة.
 
2) النطاق
●	طرق دفع: بطاقة/محافظ/تحويل محلي  (أونلاين)، وCOD.
●	إدارة دورة الحياة: محاولة دفع → تفويض/تحصيل → استرداد/إلغاء.
●	تسويات: تقارير تسوية بوابة الدفع، ودفعات شركات الشحن للـCOD. 
●	تكامل مع الطلبات، الشحنات، المرتجعات، التقارير، والإشعارات.
 
3) أنواع الدفع المدعومة
●	أونلاين: بطاقات (مع 3-D Secure)، محافظ (Apple/Google/محلي)، تحويل/فوترة بنكية (حسب المتاح). 
●	COD: تحصيل نقد/تحويل عند التسليم عبر شركة الشحن.
●	اختياري لاحقًا: شراء الآن وادفع لاحقًا (BNPL). 
 
4) الكيانات (مفهومية — بدون تفاصيل تقنية)
●	Payment (الدفع): رأس العملية المرتبطة بطلب واحد، يمكن أن يحتوي عدة محاولات.
●	Payment Attempt (محاولة): كل محاولة عبر مزوّد/قناة معيّنة، مع نتيجتها.
●	Payment Method (وسيلة): نوع الوسيلة/المعرّف المرمّز (Token) إن وُجد.
●	Refund (استرداد): استرداد كامل/جزئي مرتبط بدفع ناجح. 
●	COD Remittance (تسوية COD): حركة تحصيل شركة الشحن حتى توريدها لنا (Remit).
●	Dispute/Chargeback (اعتراض): في الأونلاين، إن حدث نزاع. 
●	Settlement Batch (دفعة تسوية): دفعات مجمّعة من المزوّد/شركة الشحن للمطابقة المحاسبية.
 
5) حالات الدفع (State Machine)
أ) أونلاين
●	initiated → authorized (تفويض) → captured (تحصيل)
●	مسارات جانبية: failed (فشل)، voided (إلغاء تفويض)، refunded_partial / refunded_full.
●	ملاحظات:
○	قد نستخدم التحصيل المؤجّل: نفوّض أولًا ثم نُحصّل عند الشحن.
○	في حالة فشل بوست-باك أو انقطاع، يتم الاعتماد على Webhook لإثبات الحالة النهائية. 
ب) COD
●	pending_collection (بانتظار التحصيل) → collected_by_courier (تم التحصيل من العميل) → remitted (تم توريدها لنا) 
●	مسارات جانبية: failed_delivery، discrepancy (فرق توريد)، write_off (معالجة فرق نهائي).
 
6) قواعد العمل (Business Rules)
●	ارتباط الطلب: لا يُوسَم الطلب “مدفوع” إلا بعد captured (أونلاين) أو بعد remitted (COD) إذا أردنا دقة محاسبية، مع إبقاء “مسلم” على مستوى العمليات.
●	محاولات الدفع: حد أقصى X محاولات لكل طلب؛ إظهار رسائل واضحة للأخطاء الشائعة. 
●	التفويض/التحصيل: التفويض صالح N أيام؛ إن فاتت يُعاد التفويض قبل الشحن. 
●	العملة/الصرف: تثبيت سعر الصرف لحظة الدفع/التحصيل وتخزين مصدره.
●	الاسترداد: يسمح بجزئي/كامل؛ في COD يكون نقدًا/تحويلًا أو رصيد متجر.
●	الاعتمادية: كل إنشاء/تحديث دفع يجب أن يكون Idempotent (مفتاح تكرار). 
●	الامتثال: لا تُخزَّن بيانات بطاقة خام؛ استخدام Tokenization فقط، وتفعيل 3DS للمعاملات التي تتطلب SCA.
●	COD والمخاطر: ربط التحصيل بنتيجة الشحن؛ عند failed_delivery تُرفع مؤشرات مخاطر العميل.
 
7) التدفقات التشغيلية
7.1 أونلاين — تفويض ثم تحصيل
1.	العميل يضيف وسيلة دفع → محاولة دفع → 3DS (إن لزم).
2.	عند authorized: نحجز المخزون ونجهّز الشحن.
3.	عند الشحن: نُحوّل إلى captured.
4.	في المرتجعات: استرداد جزئي/كامل حسب بنود المرتجع.
7.2 أونلاين — تحصيل فوري
●	من initiated إلى captured مباشرة عند إتمام الدفع (ملائم للسلع الرقمية/الشحن الفوري).
7.3 COD — التحصيل والتوريد
1.	عند إنشاء الطلب بـCOD: pending_collection.
2.	عند تسليم المندوب: collected_by_courier مع تسجيل المبلغ الفعلي.
3.	عند توريد شركة الشحن أسبوعيًا/دفعات: remitted لكل شحنة/طلب، مع ربط دفعة التسوية.
4.	فروقات التوريد: إن وُجد فرق (زيادة/نقص)، تسجيله في discrepancy ومعالجته. 
7.4 الاسترداد/الإلغاء
●	قبل الشحن: إلغاء التفويض أو عكس التحصيل إن كان فوريًا.
●	بعد التسليم: استرداد عبر البوابة (أونلاين) أو تحويل/رصيد متجر (COD).
7.5 الاعتراضات (Chargebacks)
●	عند استلام إشعار نزاع من البوابة: تحديث حالة الدفع، جمع أدلة (تتبع/تسليم/تواصل)، والرد ضمن المهلة.
 
8) التكاملات
●	الطلبات: تحديث حالة الدفع والإجماليات؛ لقطة الأسعار/العملات لحظة الطلب.
●	الشحنات: تشغيل التحصيل عند الشحن (أونلاين)، وتحديث تحصيلات COD عند التسليم.
●	المرتجعات: إنشاء استرداد متوافق مع بنود المرتجع.
●	بوابة الدفع: صفحات الدفع/SDK + Webhooks موثوقة مع إعادة محاولات واستيثاق توقيع.
●	شركات الشحن (COD): ملف/واجهة تسويات أسبوعية (CSV/API) تتضمّن: رقم الشحنة/الطلب، المبلغ المُحصّل، رسوم الشحن، صافي المبلغ، تاريخ التوريد.
●	المحاسبة: ترحيل إلى دفاتر مزدوجة (إيرادات/خصومات/رسوم/حساب وسيط COD).
●	الإشعارات: رسائل “تم الدفع/فشل الدفع/تم الاسترداد” حسب القناة المصرّح بها.
 
9) التقارير والمؤشرات (KPIs)
●	نسبة نجاح الدفع أونلاين (Authorization Rate / Capture Rate).
●	معدل فشل الدفع حسب الوسيلة/الجهاز/الشبكة.
●	نسبة تحصيل COD ومعدل التوريد خلال ≤7 أيام.
●	فروقات التوريد (Discrepancy Rate) مع شركات الشحن.
●	متوسط زمن التسوية لكل مزوّد/شركة شحن.
●	نسبة الاسترداد والاعتراضات، وقيمتها.
●	تكلفة الدفع (رسوم مزوّد/رسوم COD) لكل طلب.
 
10) معايير القبول (Definition of Done)
●	يمكن إنشاء دفع مرتبط بطلب مع عدة محاولات، وتُعرض الحالات بدقة.
●	دعم تفويض ثم تحصيل وتحصيل فوري للأونلاين.
●	COD يعمل بكامل الدورة: تحصيل عند التسليم → توريد → إغلاق دفعة التسوية.
●	الاسترداد الجزئي/الكامل يعمل ويرتبط بالمرتجع. 
●	التكامل مع Webhooks موثوق مع إعادة محاولات وفحص توقيع. 
●	تقارير تسوية: تطابق إجمالي المعاملات مع دفعات المزوّد/شركة الشحن دون فروقات غير مفسَّرة.
●	إشعارات العميل تُرسل بالحالات الرئيسية.
 
11) سيناريوهات حافة
●	انقطاع بعد الدفع الناجح: يُستعاد الوضع عبر Webhook لاحقًا بدون ازدواج.
●	تفويض منتهي قبل الشحن: إعادة تفويض تلقائي أو طلب إعادة الدفع.
●	تحصيل COD أقل/أكثر من الإجمالي: تسجيل الفرق ومعالجته في التسوية. 
●	استرداد أعلى من المبلغ المحصَّل: منع وإظهار رسالة واضحة.
●	عملة مختلفة: تثبيت الصرف وتوحيد التقارير بعملة الأساس.
●	تجزئة الطلب لشحنتين: تحصيل جزئي مقابل كل شحنة (أونلاين) أو تحصيل COD لكل شحنة. 
 
12) الامتثال والأمان
●	PCI DSS: عدم تخزين بيانات بطاقات خام؛ الاعتماد على Tokenization.
●	3-D Secure / SCA: تفعيل حيث تتطلبه الأنظمة.
●	صلاحيات الوصول (RBAC): فصل أدوار الدعم/المالية/التطوير. 
●	سجلات تدقيق: لعمليات الدفع/الاسترداد/تغيير الحالات (غير قابلة للتعديل).
●	حماية الاحتيال: قواعد للطلبات عالية المخاطر، وحدود للمحاولات، وقوائم منع. 
 
13) خارطة الإصدارات
●	MVP:
○	أونلاين: تحصيل فوري + Webhook موثوق + استرداد كامل.
○	COD: تدفّق كامل حتى remitted مع ملف تسوية أسبوعي.
○	تقارير أساسية (نجاح/فشل/تحصيل/توريد). 
●	المرحلة 2:
○	تفويض ثم تحصيل، استرداد جزئي، اختلاف عملات، تحصيل جزئي للشحنات المجزأة.
○	لوحات تسوية متقدمة وفروقات التوريد.
●	المرحلة 3:
○	BNPL، نزاعات/Chargebacks مدمجة، كشف احتيال أعمق، أتمتة كاملة للتطابق المحاسبي.
 
الخلاصة: بهذه المتطلبات يصبح نظام الدفع لديك متوافقًا مع المعايير، يدعم واقع السوق (COD) دون التضحية بالدقة المحاسبية، ويُحسّن معدل التحويل مع حماية من الفشل والاحتيال—مع تقارير تسوية واضحة يمكن الوثوق بها.
 
الشحن (Shipping) — المتطلبات المعتمدة 
الشحن (Shipping) 
1) الهدف
●	إدارة الشحن من التجهيز حتى التسليم أو الإرجاع بدقة وشفافية.
●	دعم واقع الدفع عند الاستلام (COD) في اليمن مع تقليل فشل التوصيل.
●	توحيد تتبّع الشحنات عبر شركات مختلفة وإظهار حالة واضحة للعميلة.
 
2) النطاق
●	إنشاء شحنة/شحنات للطلب (يدعم تجزئة الطلب) .
●	اختيار شركة الشحن وخدمة التوصيل (نفس اليوم/اليوم التالي/اعتيادي).
●	طباعة/توليد رقم بوليصة (AWB) وملصق شحن.
●	تتبّع الحالات وتلقي التحديثات من شركة الشحن (Webhook/CSV/API). 
●	محاولات التسليم، الفشل، العودة إلى المرسل (RTO)، والاستلام عند المرتجع.
●	تقدير تكلفة الشحن أثناء السلة/الدفع حسب المنطقة/الوزن.
●	ربط تحصيل COD بالشحنة، مع تمرير التوريدات (remittance) للمالية.
 
3) الكيانات (مفهومية—بدون أكواد)
●	Shipment (الشحنة): مرتبطة بطلب واحد وقد تكون هناك عدة شحنات للطلب .
●	Shipment Items (بنود الشحنة): (اختياري) لربط أي بنود تم شحنها في شحنة معيّنة.
●	Courier (شركة الشحن): تعريف الشركة وخدماتها ودعمها لـ COD.
●	Service Level (مستوى الخدمة): نفس اليوم/اليوم التالي/اعتيادي وساعات العمل. 
●	Zones & Rates (المناطق/التسعير): تعريف مناطق المدن/الأحياء وجداول الأسعار حسب الوزن/الشريحة ورسوم COD/الوقود.
●	Tracking Events (أحداث التتبع): طبقة توحيد لحالات الشحن من مختلف الشركات. 
●	Return/RTO (الإرجاع/العودة): تدفق إعادة القطع للمستودع والتقييم.
 
4) الحقول الرئيسية المطلوبة
4.1 الشحنة (Shipment)
●	المعرفات: shipment_id، order_id، warehouse/location_id، courier_id، service_level، tracking_no/AWB.
●	الحالة الموحّدة: ready → shipped → out_for_delivery → delivered
مسارات جانبية: failed_delivery, rto_in_transit, rto_received, cancelled.
●	التواريخ: created_at، ready_at (جاهزة للتسليم للشركة)، shipped_at، out_for_delivery_at، delivered_at، failed_at، rto_received_at. 
●	محاولات التسليم: delivery_attempts (عدد/تواريخ)، last_attempt_reason (لا يرد/عنوان غير واضح…). 
●	العنوان الملتقط: اسم/هاتف/مدينة/حي/علامة مميزة (لقطة من الطلب).
●	الأوزان/الأبعاد: weight_actual، weight_dimensional، chargeable_weight (المحاسبي).
●	التكلفة: base_rate، fuel_surcharge، cod_fee (إن وُجد)، other_fees، shipping_cost_total (للتقارير).
●	COD: cod_amount_expected، cod_amount_collected (يُحدّث عند التسليم)، remittance_batch_ref (يرتبط بالمالية).
●	الملاحظات التشغيلية: handover_method (pickup/dropoff)، packaging_notes، courier_notes، internal_notes. 
4.2 شركة الشحن (Courier) 
●	الهوية: name، contact، supports_cod (نعم/لا)، المدن المغطّاة، ساعات العمل/العطل.
●	الخدمات: service_levels المتاحة وتعريف SLA لكل مستوى.
●	التكامل: نوع التكامل (API/Webhook/CSV يدوي)، مفاتيح/إعدادات (تُخزّن في إعدادات تكامل، لا في جداول عامة).
4.3 التسعير والمناطق (Zones & Rates)
●	المنطقة: country/region/city/district mapping (قوائم مضبوطة).
●	جداول السعر: شريحة وزن (0–1كغ، 1–2كغ…)، سعر أساسي، زيادة لكل كغ، رسوم COD، رسوم نائية/بعيدة (remote area).
4.4 أحداث التتبع (Tracking Events) 
●	مصدر الحدث: courier، raw_status.
●	الحالة الموحّدة: mapped_status (ready/shipped/out_for_delivery/delivered/failed_delivery/rto…).
●	الوقت/الموقع: event_at، event_city، notes.
 
5) قواعد العمل
●	اختيار شركة الشحن تلقائيًا حسب: المدينة/الحي، دعم COD، سعر أقل + نسبة نجاح أعلى (معدّل التسليم من البيانات التاريخية)، وSLA.
●	تجزئة الشحنات: إذا بند غير جاهز/غير متوفر، يُشحن الباقي وتُنشأ شحنة ثانية لاحقًا.
●	تطابق COD: مبلغ COD في الشحنة = إجمالي الشحنة (أو حصة من الطلب عند التجزئة).
●	محاولات التسليم: حد افتراضي 2–3 محاولات؛ بعد آخر محاولة → RTO ما لم يطلب العميل إعادة الجدولة.
●	تعديل العنوان: مسموح قبل shipped. بعد الشحن: طلب تعديل عبر شركة الشحن وتوثيق السبب. 
●	وزن محاسبي: إن غيّرت الشركة الوزن عند الفوترة، نسجّل chargeable_weight وفارق التكلفة. 
●	الإشعارات: آليًا عند shipped، out_for_delivery، delivered، failed_delivery، مع روابط تتبع ووقت تسليم تقريبي.
●	RTO/Returns: عند الاستلام في المستودع: فحص الحالة → قرار إرجاع مخزون أو تخفيض/تلف.
 
6) التدفقات التشغيلية 
6.1 تنفيذ الطلب (Fulfillment)
1.	Pick & Pack: اختيار وتجهيز الأصناف.
2.	توليد AWB وطباعة الملصق.
3.	Ready → Shipped: تسليم للشركة وتأكيد الاستلام.
4.	Out for Delivery: تحديث يوم التسليم.
5.	Delivered / Failed: تحديث الحالة والـCOD.
6.2 فشل التسليم
●	المحاولة 1: لا يرد/عنوان غير واضح → تواصل واتساب/اتصال وتحديث العنوان إن لزم.
●	المحاولة 2: جدولة جديدة.
●	المحاولة 3: إن فشلت → RTO مع سبب واضح.
6.3 RTO (عودة إلى المرسل)
●	عند وصول rto_received:
○	تقييم الصندوق/القطعة.
○	تحديث المخزون (سليم/معيب).
○	تحديث ملف مخاطر العميل (لـCOD) وكتابة سبب الفشل.
6.4 المرتجعات (بعد التسليم)
●	Pick-up من العميل (إن كانت سياسة تسمح بذلك) أو التسليم في نقطة محددة.
●	إنشاء شحنة مرتجع مرتبطة بالطلب الأصلي.
 
7) تقدير تكلفة الشحن (Cart/Checkout)
●	يعتمد على: المدينة/الحي + الوزن المحسوب (فعلي/حجمي) + شركة الشحن المقترحة.
●	عرض سعر دقيق إن توفّر العنوان؛ خلاف ذلك نطاق سعري.
●	إظهار رسوم COD إن طُبقت قبل تأكيد الطلب.
 
8) التكاملات
●	شركات الشحن:
○	API لإنشاء الشحنة/الملصق/التتبّع (أولوية).
○	Webhook لاستلام تحديثات الحالة.
○	بديل: استيراد CSV يومي للحالات إن لم تتوفر Webhooks.
●	المدفوعات: تمرير cod_amount_collected عند delivered وربطه بـ دفعة التوريد (remittance).
●	الطلبات/المخزون: تحديث الحالة والمخزون تلقائيًا عند الشحن/العودة.
●	الإشعارات: Push/SMS/WhatsApp مع Deep Links لصفحة التتبع.
●	لوحة العمليات: لوحة “Dispath/Tracking” لمتابعة الشحنات حسب الحالة/الشركة/المدينة.
 
9) مؤشرات الأداء (KPIs)
●	First-Attempt Delivery Rate (نسبة التسليم من أول محاولة).
●	On-Time Delivery مقابل SLA لكل شركة/مدينة.
●	RTO Rate وأسباب الفشل (لا يرد/عنوان/سعر COD…).
●	COD Collection Rate ومعدل التوريد ≤ 7 أيام.
●	متوسط زمن التسليم (من shipped إلى delivered).
●	تكلفة الشحن لكل طلب وفروق الوزن المحاسبي.
●	نسبة الشحنات بلا تتبّع حديث (>24 ساعة) لاتخاذ إجراء.
 
10) معايير القبول (Definition of Done)
●	إنشاء شحنة مع AWB وخدمة/شركة واضحة، وطباعة ملصق.
●	تتبّع محدث (API/Webhook/CSV) ينعكس على الحالة الموحّدة داخل النظام.
●	محاولات التسليم تُسجَّل مع الأسباب.
●	RTO يعمل: استقبال، تقييم، تحديث مخزون وحالة الطلب.
●	تقدير الشحن يظهر في السلة/الدفع بدقة عند توافر العنوان.
●	إشعارات العميل تعمل بالحالات الرئيسية مع روابط تتبّع.
●	تكاليف الشحن تُسجَّل وتظهر في التقارير، مع معالجة فروق الوزن.
●	ربط COD بالشحنات وتغذية دفعات التوريد للمالية.
 
11) سيناريوهات حافة
●	تجزئة الشحنة: بنود تُشحن لاحقًا، مع COD موزّع.
●	منطقة نائية/غير مغطّاة: اختيار شركة بديلة أو عرض خيار “استلام من نقطة”.
●	زيادة وزن محاسبي بعد الفوترة: تسجيل الفرق وتمريره للتسوية.
●	عطلات/طقس: تمديد SLA وتحديث إشعار العميل.
●	عنوان غير قياسي: اعتماد حقل “علامة قريبة” وإرسال موقع/لوكيشن عند الإمكان.
●	انقطاع تكامل الشركة: التحوّل إلى CSV مؤقتًا دون فقد تتبّع.
 
12) خارطة الإصدارات
●	MVP: شحنة واحدة لكل طلب، شركة واحدة مدمجة API، تتبّع أساسي، محاولتان للتسليم، RTO يدوي، تقدير شحن بالمدينة، إشعارات shipped/out_for_delivery/delivered.
●	المرحلة 2: تعدد الشركات والاختيار الآلي، تجزئة الشحنات، Webhooks متعددة، لوحات تشغيل، RTO مؤتمت، رسوم COD مرِنة.
●	المرحلة 3: تحسين توجيه الشحن (Routing) بالبيانات التاريخية، نوافذ تسليم مواعيد (Time Slots)، نقاط التسلّم/الإرجاع، تسعير ديناميكي.
 
13) ملاحظات تشغيلية للسوق المحلي
●	الاعتماد على المدينة/الحي/المعلم بدل الرمز البريدي، وتأكيد العنوان عبر واتساب قبل الشحن عالي القيمة.
●	تفعيل OTP للتسليم في COD للحماية من تسليم خاطئ.
●	بناء قائمة مناطق موحّدة داخليًا لتقليل فشل العنوان، مع تحديث دوري وفق تجربة الميدان.
 
الخلاصة: بهذه المتطلبات يصبح مسار الشحن واضحًا ومضبوطًا من التجهيز إلى التسليم أو العودة، مع تكامل قوي لـ COD، وتتبع موحّد، واختيار شركة شحن ذكي—ينعكس مباشرة على ارتفاع نسبة التسليم من أول محاولة وخفض معدّل RTO وتكاليف الشحن.
 
المرتجعات والاستبدالات RMA(نقطة مشتركة) 
RMA — المرتجعات والاستبدالات (نقطة مشتركة)
1) الهدف
●	إدارة كل حالات ما بعد البيع في مسار واحد موحّد: استرداد أو استبدال.
●	تقليل زمن المعالجة ورفع رضى العميلة مع تتبّع واضح وشفاف.
●	ضبط الأثر المالي والمخزني بدقة (خصوصًا مع COD).
 
2) النطاق
●	فتح طلب RMA بسبب محدد (مقاس/عيب صناعة/تأخر/تغيير رأي…).
●	خياران للحل: Refund (استرداد) أو Exchange (استبدال).
●	لوجستيات الإرجاع: استلام من العميلة/تسليم لنقطة/ترتيب شركة شحن.
●	فحص القطعة وتحديد التصرف المخزني (يرجع للمخزون/تخفيض/تالف).
●	التكامل مع: الطلبات، المدفوعات، الشحن، المخزون، الإشعارات، التقارير.
 
3) السجلات (مفهومية — بدون أكواد)
●	RMA: رقم، طلب أصلي، عميلة، قناة، سبب، حالة، تواريخ رئيسية.
●	RMA Items: البنود والكميات، حالة العنصر عند الاستلام، قرار التصرف.
●	Resolution: نوع الحل (Refund / Exchange)، الملاحظات.
●	Logistics: طريقة الاستلام/التسليم، شركة الشحن، رقم التتبع، محاولات الاستلام.
●	Refund: المبلغ، الطريقة (بوابة/تحويل/نقد/رصيد متجر)، التواريخ.
●	Exchange: طلب استبدال جديد مرتبط، فروق السعر، رسوم شحن جديدة.
●	Reason Codes: قاموس موحّد للأسباب (مقاس/عيب/تأخر/…).
 
4) قواعد العمل (Business Rules)
●	الأهلية: ضمن نافذة زمنية (مثلاً 30ساعة من التسليم)، مع شرط الحالة (غير مستخدم/بطاقته مثبتة… حسب السياسة).
●	الاسترداد:
○	الأولوية لـ رصيد متجر (يعجّل الإغلاق ويقلّل السيولة الخارجة)، ويُتاح نقد/تحويل/بوابة عند الحاجة.
○	الجزئي/الكامل حسب البنود المقبولة.
●	الاستبدال:
○	إنشاء طلب جديد للبند البديل، وحساب فرق السعر (تحصيل/رد).
○	رسوم الشحن للاستبدال حسب السياسة (مجاني لعيب الصناعة، مدفوع لتغيير الرأي…).
●	المخزون:
○	عند الاستلام والفحص: تحديد مصير كل بند (يعود للمخزون إذا سليم، تخفيض إذا عبوة مفتوحة، تالف إذا غير قابل للبيع).
●	COD:
○	عند الاسترداد: تحويل/نقد/رصيد متجر؛ ربط أي مبالغ مع تسويات شركة الشحن إذا كان التحصيل عبرهم.
●	الإشعارات: تلقائية في كل مرحلة (قبول/رفض/في الطريق/استلمنا/تم الفحص/تم الاسترداد/أُنشئ الاستبدال…).
●	مكافحة سوء الاستخدام: حد أقصى لطلبات RMA لكل عميلة/شهر، ورفع درجة المخاطر عند نمط مسيء.
 
5) سير العمل الموحّد
1.	فتح RMA: اختيار السبب والمسار (استرداد/استبدال) والتحقق من الأهلية.
2.	اللوجستيات: تحديد طريقة الإرجاع (استلام/تسليم لنقطة/شركة شحن) وإنشاء رقم تتبع عند الحاجة.
3.	الاستلام والفحص: تسجيل الحالة، تحديد التصرف المخزني.
4.	القرار:
○	Refund: تنفيذ الاسترداد بالطريقة المناسبة وتأكيده.
○	Exchange: إنشاء طلب استبدال، معالجة فرق السعر، وترتيب شحن جديد.
5.	الإغلاق: تحديث التقارير/المخزون/ملف العميل، وإرسال إشعار نهائي.
 
6) الحالات والانتقالات (Statuses)
requested → approved → in_transit_return → received → inspected → resolved (refunded / exchanged) → closed
مسارات جانبية: rejected (غير مؤهل)، no_item_received، partial.
 
7) التكاملات
●	الطلبات: ربط RMA بالطلب الأصلي وبنوده.
●	المدفوعات: تنفيذ Refund (بوابة/تحويل) أو إضافة Store Credit.
●	الشحن: شحنة مرتجع مع تتبّع موحّد.
●	المخزون: تحديث الكمية/الحالة حسب قرار الفحص.
●	الإشعارات: Push/SMS/WhatsApp وفق موافقات القنوات.
●	التقارير: معدلات RMA، الأسباب، زمن المعالجة، أثرها على العائدات.
 
8) مؤشرات الأداء (KPIs)
●	Return Rate وExchange Rate حسب الفئة/المقاس/المدينة.
●	متوسط زمن المعالجة من الطلب إلى الإغلاق.
●	نسبة الإغلاق ضمن SLA (مثلاً ≤ 7 أيام).
●	أكثر الأسباب تكرارًا (لتعديل وصف/مقاسات/جودة).
●	نسبة الاسترداد كرصيد متجر مقابل نقد/بوابة.
●	أثر RMA على هامش الربح والمخزون.
 
9) معايير القبول (Definition of Done)
●	فتح RMA بمسارَيه (Refund/Exchange) مع تحقّق أهلية واضح.
●	لوجستيات مرتجع تعمل وتتبعها ظاهر للعميلة.
●	فحص دقيق وتصرّف مخزني موثّق لكل بند.
●	تنفيذ الاسترداد أو إنشاء طلب الاستبدال ومعالجة الفروق.
●	إشعارات في كل محطة رئيسية.
●	تقارير تشغيلية جاهزة تغطي KPIs أعلاه.
 
10) سيناريوهات حافة
●	استلام جزئي: قبول بعض البنود ورفض أخرى.
●	مرتجع بلا قطعة: إغلاق no_item_received بعد مهلة/تحقيق.
●	استبدال بديل غير متوفر: اقتراح بديل/رصيد متجر.
●	فرق COD: تحصيل/رد فرق السعر في الاستبدال مع توثيق.
●	ضرر من الشحن: تصنيف كعيب صناعة وتحمّل شركة الشحن/المورّد حسب السياسة.
●	عنوان مرتجع غير صحيح: إعادة جدولة أو تحويل لنقطة استلام.
 
11) خارطة الإصدارات
●	MVP: RMA موحّد، استلام مرتجع يدوي/شركة شحن واحدة، فحص وتصرف مخزني أساسي، Refund رصيد متجر أو بوابة، Exchange بسيط، إشعارات أساسية، تقارير أولية.
●	المرحلة 2: شركات شحن متعددة، سياسات متقدّمة حسب السبب/الفئة، فروق سعر تلقائية، لوحات متابعة SLA، أتمتة رفض/قبول وفق الصور.
●	المرحلة 3: توصيات ذكية لتقليل المرتجعات (مقاسات/بدائل)، تحليلات توقعية للأسباب، أتمتة استرداد لحظي.
 
12) ملاحظات للسوق المحلي (خصوصًا COD)
●	تفضيل رصيد متجر في الاسترداد لتسريع إغلاق الحالات.
●	عند فشل تسليم COD ثم RTO: تحديث مخاطر العميل لمنع تكرار الهدر.
●	توثيق علامة قريبة بمدينة/حي لتسهيل استلام المرتجع.
 
الخلاصة: نقطة RMA الموحّدة تبسّط العمل (واجهات وعمليات وتقارير)، وتجمع 80% من البيانات المشتركة بين الاسترداد والاستبدال في مسار واضح واحد—فتقلّ الأخطاء، ينخفض الزمن، وتتحسّن تجربة العميلة والأثر المالي مع المحافظة على دقة المخزون.
 
العروض والخصومات — المتطلبات المعتمدة 
العروض والخصومات 
1) الهدف
●	تحفيز الشراء وزيادة متوسط قيمة الطلب (AOV) والعودة للشراء.
●	تقديم خصومات دقيقة وعادلة دون تعقيد على المخزون أو المحاسبة.
●	قياس أثر كل عرض على المبيعات والهامش بدقة.
 
2) النطاق
●	أكواد خصم (Promo Codes/Coupons) تُدخلها العميلة يدويًا.
●	عروض تلقائية (Catalog/Cart Rules) تُطبَّق دون كود (مثال: خصم على فئة معينة).
●	شحن مجاني بشرط حد أدنى أو ضمن حملات.
●	(لاحقًا) اشترِ X واحصل على Y، Bundles، خصومات طبقية.
 
3) أنواع العروض المدعومة (المرحلة الأولى)
●	نسبة مئوية (% على الطلب أو على أصناف مؤهلة).
●	قيمة ثابتة (مبلغ يُخصم من الإجمالي أو من أصناف مؤهلة).
●	شحن مجاني (كلي/جزئي أو سقف محدد).
●	تحديد النطاق: على الطلب كاملًا أو على بنود/تصنيفات/علامات تجارية محددة.
 
4) التعريفات والحقول (مستوى المفهوم)
أ) الحملة/الكوبون
●	الاسم، الرمز (لأكواد الخصم)، نوع الخصم وقيمته.
●	الجدولة: تاريخ/وقت بداية ونهاية + المنطقة الزمنية.
●	الشروط: حد أدنى للطلب، عملة، مدينة/منطقة، طريقة دفع (يمكن استثناء COD أو فرض رسوم COD بلا خصم)، قناة (App/Instagram/WhatsApp)، جهاز/إصدار تطبيق (اختياري).
●	النطاق: يشمل/يستبعد فئات، منتجات، علامات تجارية، منتجات مخفّضة مسبقًا (تحديد السياسة).
●	الاستحقاق: عميلة جديدة فقط/كل العملاء، شرائح محددة (VIP، غير نشطين…).
●	التراكم (Stacking): يسمح/لا يسمح بالجمع مع عروض أخرى؛ أولوية/ترتيب التطبيق عند التعارض.
●	حدود الاستخدام: إجمالي مرات الاستخدام، لكل عميلة، لكل يوم، لكل قناة.
●	سقوف: حد أقصى للخصم في الطلب، وحد أقصى للصنف إن كان بنديًّا.
●	الرسائل: نص نجاح/رفض واضح (سبب الرفض)، ملاحظات قانونية مختصرة.
●	التفعيل: حالة (مسودة/منشور/موقوف)، مالك الحملة.
ب) عمليات الاستخدام (Redemptions)
●	عميلة، طلب، قيمة الخصم النهائية، وقت الاستخدام، نتيجة (نجح/فشل) + السبب، القناة/المصدر (UTM إن وجد).
 
5) قواعد العمل (Business Rules)
●	حساب الأهلية قبل الحساب: يتحقق النظام من الشروط أولًا، ثم يطبّق الخصم على الأصناف المؤهلة فقط.
●	الأولوية عند التعارض:
○	القاعدة: “أفضل سعر للعميلة” أو “غير قابل للتجميع” وفق إعداد الحملة.
○	إن كان التجميع ممنوعًا: يُطبّق العرض صاحب الأولوية الأعلى أو الخصم الأكبر حسب السياسة.
●	منتجات مخفّضة مسبقًا: إمّا تُستثنى أو يسمح بتراكم حتى سقف محدد (سياسة واضحة وثابتة).
●	الشحن وCOD: الخصم لا يُطبَّق على رسوم COD افتراضيًا؛ الشحن مجاني قد يلغي رسوم الشحن فقط.
●	التقريب والعملة: قواعد تقريب موحّدة للمجموع الكلي وبنود السطر؛ نفس القواعد عند الاسترداد.
●	الالتقاط في الطلب: تُحفَظ قيمة الخصم النهائية موزَّعة بنِسَب على بنود الطلب (لتسهيل المرتجعات).
●	الإرجاع/الاستبدال: خصم نسبي (pro-rata) يُستعاد مع البند المرتجع فقط؛ لا تُرجَع قيمة خصم تخص بنود لم تُرجَع.
●	منع إساءة الاستخدام: حد محاولات إدخال كود، منع مشاركة أكواد خاصة، ربط الأكواد الفردية بالعميلة عند اللزوم.
 
6) التدفقات التشغيلية
1.	تطبيق الكود في السلة → تحقق شروط/تعارض → رسالة فورية (نجاح/سبب رفض).
2.	عروض تلقائية تظهر فور توفر الشروط (مثال: “أضف 10,000 YER لتحصل على شحن مجاني”).
3.	الدفع: إعادة تحقق نهائي قبل إنشاء الطلب (السعر/المخزون/الخصم).
4.	الطلب: التقاط الخصم وتوزيعه على البنود + تسجيل redeption.
5.	المرتجعات: حساب الاسترداد مع خصم نسبي ومزامنة مع المدفوعات/رصيد المتجر.
 
7) الدمج والتكامل
●	السلة/الدفع: تحقق لحظي، إعادة حساب المجاميع، رسائل واضحة.
●	الطلبات: لقطة نهائية للخصم وتوزيع بنود.
●	المرتجعات: سياسة pro-rata تلقائية.
●	المدفوعات: الشحن/COD لا يتأثران إلا إذا نص العرض.
●	التحليلات (GA4/Firebase): أحداث apply_promo, promo_error, view_promo_banner, purchase مع قيم الخصم.
●	القنوات: إمكانية تقييد كود لقناة أو حملة (UTM) محددة.
 
8) التقارير وKPIs
●	معدل استخدام الكوبونات وعدد الطلبات المتأثرة.
●	الخصم/الإيراد: إجمالي الخصم، نسبة الخصم إلى المبيعات.
●	الأثر الصافي: الرفع في التحويل/AOV مقابل تكلفة الخصم.
●	التسريب: نسبة محاولات الاستخدام الفاشلة وأسبابها.
●	الأداء حسب الشريحة/القناة/الفئة.
●	تكلفة الشحن المجاني وتأثيره على التحويل.
 
9) معايير القبول (Definition of Done)
●	إنشاء وتفعيل حملة/كوبون مع الشروط والحدود والجدولة.
●	تطبيق الخصم بدقة على الأصناف المؤهلة وإظهار السبب عند الرفض.
●	سياسة التراكم/الأولوية تعمل كما هو محدد.
●	توزيع الخصم على بنود الطلب محفوظ؛ المرتجعات تُحسب pro-rata تلقائيًا.
●	الشحن المجاني و/أو استثناء COD يعملان كما في السياسة.
●	تقارير الاستخدام والأثر متاحة للفريق.
●	رسائل العميلة واضحة في كل خطوة (نجاح/سبب الرفض/المتبقي للوصول للعرض).
 
10) سيناريوهات حافة
●	انتهاء صلاحية الكود أثناء الدفع → رسالة واضحة مع بدائل.
●	اختلاف العملة/السوق → الكود صالح لأسواق محددة فقط.
●	كود “عميلة جديدة فقط” مع رقم/جهاز مكرر → رفض برسالة واضحة.
●	سلة فيها منتج مؤرشف/نفد → إعادة تحقق وإزالة الخصم المطبق عليه فقط.
●	BOGO/Bundle (لاحقًا): التعامل مع المرتجعات بحيث يُعاد حساب خصم المجموعة عند فقدان أهلية البند المجاني.
●	أكواد شخصيّة (1-time codes) → ترتبط بحساب العميلة وتُبطل بعد الاستخدام.
 
11) خارطة الإصدارات
●	MVP:
○	أكواد خصم (٪/قيمة ثابتة) + شحن مجاني، حد أدنى للطلب، قيود فئة/منتج، حدود استخدام (إجمالي/لكل عميلة)، جدولة، استثناء COD اختياري، تقرير استخدام أساسي.
●	المرحلة 2:
○	عروض تلقائية ذكية، تلميحات تقدُّمية (“تبقى 3,000 YER للشحن المجاني”), أكواد فردية، شرائح عملاء، قنوات/UTM، A/B لرسائل الخصم.
●	المرحلة 3:
○	BOGO، Bundles، Tiered Discounts، تسعير متعدد الأسواق، توصيات عرض شخصية.
 
12) ملاحظات للسوق المحلي
●	التركيز على حد أدنى للشحن المجاني يرفع AOV بكلفة مفهومة.
●	غالبًا استثناء رسوم COD من الخصم لتفادي تكاليف زائدة غير متوقعة.
●	رسائل عربية بسيطة وواضحة على سبب الرفض والكيفية للوصول للعرض.
 
الخلاصة: بهذه المتطلبات تحصل على نظام عروض مرن وواضح، يطبّق خصومات عادلة بلا تعارض، ويُظهر أثرًا يمكن قياسه—مع جاهزية للتوسّع لاحقًا إلى BOGO والباقات والشرائح المتقدمة، دون تعقيد على الطلبات أو المحاسبة.
 
المشتريات والتوريد (Procurement & Inbound) 
المشتريات والتوريد (Procurement & Inbound)
1) الهدف
●	تأمين توفر المنتجات بالكمّيّات والسعر الصحيحين وفي الوقت المناسب.
●	تتبّع التوريد من أمر الشراء حتى الاستلام والفحص والإدخال للمخزون.
●	احتساب التكلفة الحقيقية (Landed Cost) بدقّة لرفع هامش الربح واتخاذ قرار تسعير صحيح.
●	قياس أداء المورّدين وتقليل زمن النفاد (Stockouts) ومرتجعات المورد.
 
2) النطاق
●	إدارة المورّدين وشروطهم (عملات/مدد توريد/حدود دنيا).
●	أوامر الشراء (PO) وبنودها، والموافقات.
●	شحنات واردة وإشعارات شحن مسبقة (ASN) وتتبع الوصول.
●	الاستلام (GRN) والفحص والجودة ومعالجة الفروقات (نقص/زيادة/ضرر).
●	تكاليف إضافية: شحن/تأمين/جمارك وتوزيعها على البنود (Landed Cost).
●	فواتير المورد والمطابقة الثلاثية (PO ↔ GRN ↔ Invoice).
●	مرتجعات المورد (RTV) ومذكرات الخصم (Debit Notes).
●	التخطيط وإعادة الطلب (Reorder Rules) بصورة خفيفة.
 
3) الكيانات (مفهومية – بدون تفاصيل تقنية)
●	Supplier (مورّد): الاسم، جهة الاتصال، شروط الدفع (مقدم/NET 30)، العملة، مدة التوريد (Lead Time)، الحد الأدنى للطلب (MOQ)، شروط الشحن/إنكوترمز (Incoterms).
●	Purchase Order (PO): رقم، مورد، عملة، تواريخ (الإنشاء/الموافقة/المتوقّع)، حالة (مسودة/موافق/جزئي/مكتمل/ملغى).
●	PO Items: الصنف/النسخة، الكمية، سعر الشراء، الخصم، موعد التوريد المتوقّع لكل بند.
●	Inbound Shipment / ASN: شركة الشحن، رقم بوليصة، حاوية/شحنة، ETA/ETD، ملاحظات جمركية.
●	GRN (إثبات استلام): الكمية المستلمة فعليًا، الفروقات، حالة الجودة.
●	QC (الجودة): نتيجة الفحص (سليم/عيب/تالف)، قرارات التصرف.
●	Landed Cost: شحن/تأمين/جمارك/مناولة… وطريقة توزيعها (بالوزن/الحجم/القيمة/الكمية).
●	Supplier Invoice: رقم، تاريخ، عملة، مبلغ، حالة (مُطابَق/فروقات).
●	RTV (Return to Vendor): سبب الإرجاع، الكميات، مذكّرة خصم، شحنة عكسية.
●	Reorder Rules: نقطة إعادة الطلب، كمية الطلب الاقتصادية، الحد الأدنى للمخزون.
 
4) الحقول عالية المستوى التي نحتاجها
●	Supplier: تقييم أداء، نسبة الالتزام بالمواعيد، نسبة العيوب، متوسط مهلة التوريد الفعلي.
●	PO: إجمالي الأمر بالعملة، سعر الصرف المثبّت لحظة الإنشاء/الفاتورة، حالة الموافقة، مرفقات (عرض سعر/عقد).
●	PO Item: SKU/Variant، الكمية المطلوبة/المستلمة/المتبقية، سعر الشراء قبل وبعد الهبوط/الخصم.
●	Shipment/ASN: شركة الشحن، طريقة الشحن (جوي/بحري/بري)، الوزن/الحجم، رقم تتبع، ETA.
●	GRN/QC: تاريخ الاستلام، مستلم، نتائج الفحص، فروقات (كمّية/جودة)، قرارات (إدخال مخزون/تخفيض/تلف/RTV).
●	Landed Cost: قائمة التكاليف + طريقة التوزيع ونتيجة التكلفة للوحدة.
●	Invoice: مبلغ الفاتورة، ضرائب/رسوم، مطابقة ثلاثية (تطابق السعر/الكمية)، فروقات السعر/الكمية.
●	RTV: سبب، كميات، قيمة، طريقة الشحن العكسي، حالة الإغلاق.
●	Reorder: نقطة إعادة الطلب، Lead Time، Safety Stock.
 
5) قواعد العمل (Business Rules)
●	الموافقات على PO: أوامر فوق حدّ مالي معيّن تتطلب موافقة ثنائية.
●	المُبالغة/النقص (Tolerance): سماحية ±5–10% لكل بند تُقبل تلقائيًا، وما زاد يذهب لمراجعة.
●	الاستلام الجزئي: يسمح باستلام أجزاء من الأمر؛ تبقى الكمية المتبقية مفتوحة أو تُغلق حسب قرار الشراء.
●	مطابقة ثلاثية (3-Way Match): لا تُعتمد فاتورة إلا إن طابقت كمّية وسعر (PO/GRN/Invoice) أو فُسِّرَ الفرق.
●	تثبيت سعر الصرف: يُثبَّت عند الفاتورة أو عند الدفع (سياسة موحّدة) ويُحفظ المصدر.
●	التكلفة القياسية: طريقة التقييم: متوسط متحرّك (Moving Average) أو FIFO – تُعتمد واحدة وتوثَّق.
●	Landed Cost: تُوزَّع قبل إدخال التكلفة النهائية للمخزون؛ أي تعديل لاحق يُسجَّل كتعديل تكلفة.
●	الجودة/العيوب: المعيب لا يدخل مخزون البيع؛ إمّا RTV أو تحويله لتخفيض/تالف.
●	RTV: يُنشأ لأصناف ناقصة/معيبة؛ تُصدر مذكرة خصم أو استبدال.
●	إعادة الطلب: تنبيه تلقائي عندما يصل المخزون إلى Reorder Point آخذًا بالاعتبار Lead Time والطلب التاريخي.
 
6) التدفقات التشغيلية (Workflows)
6.1 تعاقد/إضافة مورّد
إدخال بيانات المورّد + شروط الدفع/العملة/الـIncoterms → توثيق Lead Time وMOQ → تقييم ابتدائي.
6.2 إنشاء PO والموافقة
مشتريات تجمع بنود مطلوبة (احتياج/تخطيط/حملات) → مراجعة الأسعار والخصومات → موافقة حسب الصلاحيات → إرسال للمورّد.
6.3 شحنة واردة & ASN
استلام ASN (رقم بوليصة/حاوية، ETA، محتويات) → ربطها بالـPO → تجهيز الاستلام.
6.4 الاستلام والفحص (GRN & QC)
وصول الشحنة → عدّ فعلي لكل بند → تسجيل GRN والفروقات → QC: سليم/عيب/تالف → قرارات (إدخال/RTV/تخفيض).
6.5 التكاليف الإضافية & Landed Cost
تجميع الشحن/التأمين/الجمارك/المناولة → توزيع على البنود بطريقة مختارة (قيمة/وزن/حجم/كمية) → تحديث تكلفة الوحدة الفعلية.
6.6 فاتورة المورد والمطابقة
استلام الفاتورة → مطابقة ثلاثية مع PO وGRN → قبول/رفض/استثناء مع توثيق → تمرير للحسابات الدائنة.
6.7 مرتجع للمورد (RTV)
إن وُجد عيب/فائض غير مقبول → فتح RTV مع سبب → شحنة عكسية → مذكرة خصم أو استبدال.
6.8 إعادة الطلب (Reorder)
مراقبة مخزون SKU مقابل Reorder Point → توليد اقتراح PO → مراجعة وتوحيد بنود وفق MOQ/شحن → اعتماد.
 
7) التكاملات
●	المخزون: إدخال الكميات السليمة فور GRN، وتعديل حالة المعيب/التلف، وتحديث التكلفة (Moving Average/FIFO).
●	الشحن/التتبع (Inbound): ربط أرقام التتبع والـETA، ودعم حالات الجمارك.
●	المالية/المحاسبة: قيود تلقائية (مخزون، تكلفة بضائع مباعة، حسابات دائنة، فروق عملة، تكاليف شحن وجمارك)، وتسويات المورد.
●	التقارير/التحليلات: أداء المورّدين، زمن التوريد الفعلي، انحراف التكلفة، تغطية المخزون.
●	الإشعارات: تنبيهات تأخّر ASN/ETA، تجاوز تَحمّل الفروقات، وصول مخزون حرج.
 
8) التقارير وKPIs
●	On-Time Delivery % لكل مورد/فئة.
●	Lead Time Accuracy (الفرق بين المتوقع والفعلي).
●	Fill Rate % (نسبة التوريد مقابل المطلوب).
●	Defect Rate % وRTV Rate %.
●	Cost Variance % (فرق سعر/تكلفة هبوط/Landed Cost).
●	Days of Inventory وStockout Days.
●	Inventory Turns وAging (بضائع بطيئة الحركة).
●	Supplier Scorecard شامل (زمن/جودة/تكلفة/تواصل).
 
9) معايير القبول (Definition of Done)
●	إنشاء PO وموافقته وتتبّع حالته حتى الإغلاق.
●	تسجيل ASN/Shipment وربطها بأمر الشراء.
●	GRN مع استلام جزئي وفروقات موثّقة ونتيجة QC.
●	توزيع Landed Cost على البنود وتحديث تكلفة الوحدة.
●	مطابقة ثلاثية تعمل وتظهر الاستثناءات بوضوح.
●	إنشاء RTV وإغلاقه مع مذكّرة خصم أو استبدال.
●	مؤشرات الأداء الأساسية ولوحة Supplier Scorecard متاحة.
 
10) سيناريوهات حافة
●	Short/Over Shipment: أقل/أكثر من المطلوب—تُسجّل وتُقرَّر (قبول/RTV/خصم).
●	ضرر أثناء النقل: يتحملها الشحن/المورّد حسب الـIncoterms—تسجيل مطالبة.
●	رسوم جمركية غير متوقعة: تُضاف للـLanded Cost وتوثَّق كملاحظة.
●	تقلب عملة قوي: فروق تقييم عملة تُسجَّل محاسبيًا؛ سياسة تثبيت واضحة.
●	تجزئة PO على شحنات متعددة: تحديث ETAs ومتابعة استلامات جزئية.
●	استبدال SKU (بديل): قبول بديل مع ربط واضح ووسم “بديل مورّد”.
 
11) خارطة الإصدارات
●	MVP: مورّدون، PO + Items، استلام جزئي (GRN)، QC أساسي، RTV بسيط، تكلفة مخزون متوسط متحرّك، تقارير أساسية.
●	المرحلة 2: ASN مفصّل، Landed Cost بتوزيع مرن، مطابقة ثلاثية، مؤشرات أداء الموردين، تنبيهات تأخّر.
●	المرحلة 3: قواعد Reorder تلقائية، توقّعات طلب (Forecast)، عقود أسعار، مناقصات موردين، تسعير متعدد العملات.
 
12) ملاحظات للسوق المحلي (اليمن وما حولها)
●	التعامل غالبًا بعملات USD/SAR مع تثبيت صرف موثّق عند الفاتورة/الدفع.
●	الاهتمام بنمذجة الجمارك والرسوم بدقة ضمن Landed Cost؛ والاحتفاظ بالمستندات.
●	أولوية للشحن البري/البحري في التكاليف والـETA؛ تأكّد من دعم سيناريو تأخر الميناء.
●	فرق COD في المرتجعات بعد التوريد لا يؤثر على تكلفة الشراء؛ يُعالج ضمن المبيعات/المرتجعات لا ضمن المشتريات.
 
بهذه المتطلبات يصبح مسار التوريد واضحًا من PO إلى الاستلام والتكلفة الفعلية، مع رقابة قوية على الجودة والتكاليف، ومطابقة مالية سليمة، ومؤشرات أداء تمكّنك من تحسين اختيار المورّدين وتقليل نفاد المخزون—وكل ذلك بدون تعقيد تقني زائد.
 
التحليلات (Analytics) — خلاصة تنفيذية 
التحليلات (Analytics) 
1) الهدف
●	إجابة أسئلة العمل بسرعة: التحويل، الاحتفاظ، قيمة العميل، أداء المنتجات، فعالية القنوات، جودة التشغيل (شحن/COD/مرتجعات).
●	توحيد مصدر الحقيقة للأرقام مع تعاريف ثابتة يمكن الوثوق بها.
2) النطاق والبيانات الداخلة
●	أحداث التطبيق (GA4/Firebase): view_item, add_to_cart, begin_checkout, purchase, session_start…
●	المعاملات التشغيلية: الطلبات، بنود الطلب، المدفوعات، الشحنات، COD، المرتجعات.
●	الكتالوج والمخزون: منتجات/نسخ، تصنيفات، لقطة مخزون يومية.
●	العروض والرموز: حملات، استخدام القسائم، الشحن المجاني.
●	التسويق/الإسناد: UTM (source/medium/campaign)، القناة (App/Instagram/WhatsApp).
●	الرسائل: فتح/نقر حملات Push/SMS/WhatsApp (اختياري).
3) نموذج البيانات
الأبعاد (Dimensions):
●	التاريخ، العميل، المنتج، النسخة، التصنيف، المنطقة/المدينة، الجهاز/منصة التطبيق، القناة/الحملة.
الحقائق (Facts):
●	الطلبات (fact_orders)
●	بنود الطلب (fact_order_items)
●	المرتجعات (fact_returns)
●	الشحنات/COD (fact_shipments, fact_cod_collections)
●	جلسات/مستخدمين (fact_sessions)
●	مشاهدات/إضافات للسلة (fact_product_views) تلخيص يومي
●	المخزون اليومي (fact_inventory_daily)
●	استخدام القسائم (fact_promos)
عروض جاهزة (Materialized Views):
●	mv_funnel_daily (عرض → سلة → دفع → شراء)
●	mv_abandoned_carts_7d
●	mv_repeat_purchase_30d (تكرار شراء)
●	mv_top_skus (الأكثر مبيعًا/هامشًا)


4) أهم المؤشرات (KPIs)
●	التحويل: Add-to-Cart %, Checkout %, Purchase %, Conversion Funnel.
●	الإيراد: Revenue, AOV, Discount %, (الهامش إن توفّرت التكلفة).
●	العملاء: LTV، RFM، Cohorts احتفاظ أسبوعي/شهري، تكرار شراء.
●	الكتالوج: الأكثر مشاهدة/إضافة/بيعًا، معدل الإرجاع لكل SKU، اكتمال المحتوى.
●	السلة: حجم وقيمة السلال المهجورة، استرداد المهجورة.
●	الشحن/COD: First-Attempt Delivery %, RTO %, COD Collection %, تسوية ≤7 أيام.
●	التسويق: ROAS/CVR حسب القناة/الحملة، استخدام القسائم وفعاليّتها.
●	البحث: معدل “لا توجد نتائج”، استعلامات الأعلى تحويلًا.
5) لوحات التقارير (Dashboards)
●	نظرة تنفيذية يومية: إيراد/طلبات/AOV/تحويل/خصم/مرتجعات/RTO.
●	تسويق: قنوات/حملات، ROAS، قسائم، Funnel بالقناة.
●	merchandising: أداء الفئات والـSKUs، الهامش، نفاد المخزون.
●	العمليات/الشحن: SLA، محاولات التسليم، COD والتحصيل.
●	العملاء: RFM، Cohorts، LTV، شرائح VIP/غير نشطين.
●	السلة والبحث: مهجورة، نصوص بحث بلا نتائج وتحسيناتها.
6) التحديث والزمنية (Freshness)
●	شبه لحظي (كل 15–60 دقيقة): أحداث التطبيق، مؤشرات المبيعات الأساسية.
●	يومي (Daily): لقطات المخزون، Cohorts، LTV، تقارير الشحن/COD.
●	أسبوعي: لوحات المورد/التكلفة إن لزم.
7) الجودة والحَوْكمة
●	قاموس بيانات موحّد لتعريف كل مؤشر.
●	فحوص صحة دورية: توازن طلبات/مدفوعات/شحنات، ازدواج/فجوات، حدود منطقية.
●	صلاحيات وصول حسب الدور، تقليل بيانات شخصية، احترام الموافقات.
8) تعريف الاكتمال (Definition of Done)
●	تدفّق بيانات من المصادر المذكورة إلى مخزن تحليلي موحّد.
●	طبقة أبعاد/وقائع جاهزة للاستعلام + العروض المادية الأربعة أعلاه.
●	لوحات: تنفيذية، تسويق، Merchandising، عمليات الشحن/COD، عملاء، سلة/بحث.
●	KPIs الأساسية محسوبة ومتطابقة مع الأرقام التشغيلية.
●	تواتر التحديث مفعل (لحظي/ليلي) مع تنبيهات تعطل.


9) خارطة إصدارات مختصرة
●	MVP (أسبوعان): fact_orders/order_items/sessions/product_views + لوحتين (تنفيذية، تسويق) + mv_funnel_daily.
●	المرحلة 2: شحن/COD/مرتجعات/Promos + لوحتي العمليات والكتالوج + abandoned carts.
●	المرحلة 3: Cohorts/LTV/RFM، لوح العملاء، تنبؤ نفاد مخزون، تحسين البحث.

بهذه الطبقة تحصل على مصدر أرقام موثوق، يربط الرحلة من التصفح حتى التسليم، ويُظهر ببساطة أين نكسب وأين نهدر—وبوتيرة تحديث تكفي لاتخاذ قرارات يومية بثقة.
 
المحفظة (Wallet / Store Credit) 
المحفظة (Wallet / Store Credit)
1) الهدف
●	تمكين رصيد متجر آمن وسريع للاستخدام في الشراء، والاسترداد من المرتجعات.
●	تقليل زمن الإغلاق المالي لحالات RMA وطلبات COD.
●	تحفيز التكرار والولاء عبر Cashback وبطاقات هدية قابلة للاسترداد.
 
2) النطاق
●	رصيد متجر للعميل (Store Credit) مرتبط بحسابه.
●	معاملات محفظة: إضافة (Credit) وخصم (Debit) وحجز مؤقت أثناء الدفع.
●	سياسات: صلاحية/انتهاء، حدود استخدام، مكافحة الاحتيال.
●	مصادر الرصيد: مرتجعات، تعويضات، Cashback، (اختياري) تعبئة رصيد/بطاقات هدية.
●	استخدام الرصيد: وسيلة دفع جزئية/كاملة للطلبات، مع الدمج مع بطاقة/COD.
●	(اختياري) بطاقات هدية (Gift Cards) برموز قابلة للنقل.
 
3) الكيانات (مفهومية—بدون تفاصيل تقنية)
●	Wallet Account: لكل عميلة حساب محفظة بعملة العرض (YER أساسًا).
●	Wallet Transaction: حركة مالية بقيَم موجبة/سالبة، مع مصدر/مرجع (طلب/مرتجع/تعويض).
●	Wallet Hold (Authorization): حجز مؤقت عند بدء الدفع، يُحرَّر أو يُخصَم عند إنشاء الطلب.
●	Gift Card (اختياري): بطاقة ذات رمز وقيمة وصلاحية، قابلة لتحويل الرصيد إلى محفظة العميلة عند الاسترداد.
●	Cashback Rule (اختياري): تعريف نسبة/قيمة تُكتسب بعد اكتمال الطلب.
 
4) الحقول الأساسية (مختصرة)
Wallet Account
●	المعرّف، customer_id، العملة، balance_available، balance_on_hold، تواريخ الإنشاء/التحديث.
Wallet Transaction
●	المعرّف، customer_id، النوع (credit/debit/adjustment)، المبلغ (+/-)، العملة.
●	source (refund/cashback/manual/giftcard/recharge)، reference_id (طلب/RMA/كوبون).
●	status (pending/posted/reversed)، reason_code (تعويض/مرتجع/عرض…).
●	الفاعل (نظام/موظف)، ملاحظات، طابع زمني.
Wallet Hold
●	المبلغ المحجوز، مرجع السلة/الدفع، expires_at (مهلة تلقائية)، الحالة (active/released/captured).
Gift Card (اختياري)
●	الرمز، الرصيد الأصلي/المتبقي، العملة، expires_at، الحالة (نشطة/مستردّة/منتهية)، مرات الاستخدام.
Cashback Rule (اختياري)
●	نسبة/قيمة ثابتة، حدود قصوى، أهلية (فئات/قنوات)، lock_period حتى الإتاحة (مثلاً بعد 7–14 يومًا من التسليم).
 
5) قواعد العمل (Business Rules)
●	ترتيب التطبيق في الدفع:
○	سعر البنود − الخصومات/الكوبونات →
○	الشحن ورسوم COD (حسب السياسة) →
○	تطبيق رصيد المحفظة →
○	الباقي يُدفع ببطاقة/COD.
●	يفضّل استثناء رسوم COD من التغطية بالمحفظة لتبقى مفهومة (قرار تجاري).
●	المرتجعات: الافتراضي استرداد إلى المحفظة (أسرع)، مع إمكان تحويل بنكي يدوي عند الطلب.
●	الدمج مع طرق الدفع: يسمح بالدفع المختلط (محفظة + بطاقة أو محفظة + COD).
●	الحجز المؤقت: عند Begin Checkout يُنشأ Hold؛ عند إنشاء الطلب يُحوَّل إلى Debit، وإلا يُحرَّر تلقائيًا عند انتهاء المهلة.
●	الصلاحية: رصيد متجر من المرتجعات لا ينتهي (مستحسن). Cashback/بطاقات هدية قد تنتهي (مثلاً 12 شهرًا).
●	القيود: حد أقصى يومي/شهري للاستخدام، وحد أقصى للرصيد المتراكم (مكافحة إساءة).
●	العملة: المحفظة بعملة السوق النشطة (YER). إن تعددت الأسواق لاحقًا: إمّا محفظة لكل عملة أو تحويل بسعر صرف مثبت لحظة الحركة.
●	مكافحة الاحتيال:
○	تفعيل OTP عند استخدام رصيد كبير أو استرداد بطاقة هدية.
○	قيود سرعة (Velocity) لعمليات الإضافة/الخصم، وتطابق الجهاز.
○	مراجعة يدوية لحركات manual adjustment مع سبب إلزامي.
●	دمج الحسابات: عند دمج عميلَين، تُدمَج المحافظ وحركاتها مع Audit Trail.
●	السجلات والتوافق: جميع الحركات تُسجَّل كسجل غير قابل للتعديل (append-only) مع ربط محاسبي (التزام/ذمم).
 
6) التدفقات التشغيلية (Workflows)
أ) الدفع بالمحفظة
1.	المستخدم يختار “الدفع بالمحفظة” ويحدّد المبلغ → إنشاء Hold.
2.	نجاح الدفع الإضافي (إن وُجد) → إنشاء الطلب → Capture → Debit ويُخصم من الرصيد.
3.	فشل/إلغاء → Release للحجز.

ب) مرتجع → رصيد متجر
1.	إغلاق RMA ببنود مقبولة → إنشاء Credit بالمبلغ المناسب (بعد خصم جزء الخصم pro-rata ورسوم الشحن حسب السياسة).
2.	يظهر الرصيد فورًا في المحفظة.
ج) Cashback (اختياري)
1.	بعد delivered وانتهاء نافذة المرتجع (مثلاً 7 أيام) → إنشاء Credit وفق القاعدة وحدودها.
2.	إشعار العميلة وإظهار تاريخ الانتهاء إن وُجد.
د) بطاقات هدية (اختياري)
●	شراء بطاقة → إنشاء كيان Gift Card برمز يُرسل للمتلقّي.
●	الاسترداد: إدخال الرمز → تحويل الرصيد إلى Wallet Credit مرتبط بالعميلة.
●	الاستخدام جزئي/كلي، وتتبع الرصيد المتبقي.
هـ) تعويض/تعديل يدوي
●	فقط لأدوار مفوّضة، مع سبب إجباري، ومراجعة ثنائية لأكثر من حد محدد.
 
7) التكاملات
●	الطلبات/الدفع: الحجز/الخصم، ترتيب التطبيق، دعم الدفع المختلط، تحديث مبلغ COD المتوقَّع إذا استُخدمت المحفظة.
●	RMA: إنشاء Credits تلقائيًا، وربط الحركة بملف المرتجع.
●	العروض: Cashback مستقل عن الكوبونات (لا يتعارض)، ويظهر في الإيصال.
●	التحليلات: أحداث wallet_credit, wallet_debit, wallet_hold, wallet_release, cashback_earned, giftcard_redeemed.
●	المحاسبة: المحفظة = التزام (Liability)؛ قيود تلقائية عند كل Credit/Debit؛ تقارير تسوية يومية.
 
8) مؤشرات الأداء (KPIs)
●	Wallet Usage %: نسبة الطلبات التي استخدمت المحفظة.
●	Repeat Rate Lift لمن استخدموا المحفظة مقابل من لم يستخدموها.
●	Time-to-Refund: زمن من قبول RMA حتى ظهور الرصيد.
●	Breakage %: رصيد منتهي الصلاحية (للكاش باك/بطاقات الهدايا) مقابل المكتسب.
●	Fraud Flags: محاولات غير طبيعية/ضخمة، تعديلات يدوية فوق الحد.
●	COD Impact: انخفاض المبلغ المُحصَّل نقدًا عند الباب بفضل المحفظة.
 


9) معايير القبول (Definition of Done)
●	لكل عميلة Wallet Account واضح برصيد متاح/محجوز.
●	يمكن الدفع بالمحفظة جزئيًا/كليًا مع Hold/Capture/Release صحيح.
●	المرتجعات تُنشئ Credit تلقائيًا بنِسَب pro-rata للخصومات.
●	Cashback يعمل وفق القواعد بعد التسليم ونهاية مهلة المرتجع.
●	(اختياري) بطاقات هدية قابلة للاسترداد إلى المحفظة برموز فريدة.
●	تقارير تسوية يومية: مجموع الأرصدة = رصيد حساب الالتزامات، دون فروقات.
●	سجلات تدقيق كاملة ومراجعة ثنائية للتعديلات اليدوية.
 
10) سيناريوهات حافة
●	مزج محفظة + بطاقة ثم مرتجع جزئي: تُعاد نسبة الدفع إلى البطاقة والمحفظة pro-rata.
●	شحنة مجزأة: خصم المحفظة عند إنشاء الطلب، وليس عند كل شحنة.
●	فشل دفع خارجي بعد خصم المحفظة: عكس حركة المحفظة تلقائيًا (Reverse) إن لم يُنشأ الطلب.
●	سالب بالخطأ: منع الرصيد السلبي؛ معاملات متسلسلة ضمن قفل/معاملة واحدة.
●	بطاقة هدية مسروقة/مسرّبة: OTP عند الاسترداد + حد يومي + إبطال رمز عند الإبلاغ.
 
11) خارطة الإصدارات
●	MVP: رصيد متجر من المرتجعات/التعويضات + دفع بالمحفظة (Hold/Capture) + تقارير تسوية + أحداث تحليلات أساسية.
●	المرحلة 2: Cashback بقواعد بسيطة + حدود/صلاحيات + إشعارات.
●	المرحلة 3: بطاقات هدية، تعبئة رصيد (Recharge) عبر البوابة، محفظة متعددة العملات، مركز نزاعات.
 
الحوكمة والتكامل (Governance & Integrations) 
الحوكمة والتكامل (Governance & Integrations) 
1) الهدف
●	حماية البيانات وتشغيل النظام بثقة وموثوقية.
●	ضمان جودة الأرقام واتساقها عبر كل الوحدات (كتالوج، عملاء، طلبات…).
●	تكامل آمن ومرن مع مزوّدي الدفع والشحن والرسائل والتحليلات والمحاسبة.
 
2) الحوكمة (Governance)
أ) الأدوار والصلاحيات (RBAC)
●	الأدوار المقترحة: Admin، عمليات الطلبات، الشحن، المالية، خدمة العملاء، المحتوى/الكتالوج، التسويق، التحليلات/BI، المطوّر.
●	مبدأ أقلّ صلاحية: كل دور يرى ويعدّل فقط ما يحتاجه.
●	عمليات حساسة: الاسترداد المالي، تغيير حالة الطلب، تعديل الأسعار—تتطلب صلاحيات عليا وتسجيل تدقيق.
ب) الخصوصية وPII والموافقات
●	تقليل البيانات (مطلوب فقط)، وإخفاء/إخفاء جزئي في واجهات الدعم.
●	الموافقات: احترام قنوات Push/SMS/WhatsApp/Email في كل الإرساليات.
●	طلبات المستخدم (DSR): تصدير/حذف بيانات العميل عند الطلب ضمن SLA داخلي (مثلاً 7 أيام).
ج) جودة البيانات وحَوْكمتها
●	قاموس بيانات يعرف المؤشرات والحقول المحورية (AOV، LTV، RTO…).
●	اختبارات صحة دورية: فراغات/قيم شاذة/اتساق مراجع (FK)، تطابق طلبات↔مدفوعات↔شحنات.
●	سياسات التسمية والقيم المسموح بها للألوان/المقاسات/المدن لتفادي الفوضى.
د) سجلات التدقيق (Audit Logs)
●	لكل تعديل على: الطلبات، المدفوعات، الشحن، RMA، الأسعار، الصلاحيات.
●	غير قابلة للتعديل (append-only) وتُحفظ لمدة لا تقل عن 12 شهرًا.
هـ) الاحتفاظ والحذف (Retention)
●	سجلات التطبيق: 90 يومًا (عمليات)، Audit: 12–24 شهرًا، بيانات تحليلية المجمّعة أطول.
●	حذف/أرشفة السلال والعناصر غير النشطة بعد فترة محددة (مثلاً 60 يومًا للضيوف).


و) الأمن
●	تشفير أثناء النقل (TLS 1.2+) وعند السكون لقواعد البيانات والنسخ.
●	إدارة أسرار مركزية (Vault/KMS)، وتدوير دوري للمفاتيح.
●	2FA للحسابات المميّزة، وقواعد كلمات مرور، وقوائم تحكم بالوصول الشبكي.
●	عدم تخزين بيانات بطاقات (امتثال PCI DSS عبر توكنات مزوّد الدفع).
ز) النسخ الاحتياطي والتعافي من الكوارث (B/DR)
●	أهداف: RPO ≤ 15 دقيقة، RTO ≤ 2 ساعة.
●	نسخ تلقائية (يومي كامل + لقطات دورية)، اختبار استعادة شهري.
ح) إدارة التغييرات (Change Management)
●	مسارات Dev/Staging/Prod، ومراجعة تغييرات، وهجرات قاعدة بيانات متوافقة رجعيًا.
●	Feature flags للتدرّج في الإطلاق والتراجع السريع (rollback).
ط) المراقبة والموثوقية (Observability & SLOs)
●	لوغز + مقاييس + تتبّع: أخطاء، زمن استجابة، ازدحام الطوابير.
●	SLOs مقترحة: Checkout p95 < 800ms، فشل Webhook < 0.5%، تزامن تتبع الشحن < 15 دقيقة.
●	تنبيهات عند: ارتفاع فشل الدفع، زيادة RTO، تعطّل تكامل.
 
3) التكامل (Integrations)
أ) واجهات وخدمات
●	REST API داخلية/خارجية: ترقيم إصدارات، ترقيم صفحات، Rate Limits، Idempotency Keys لعمليات الإنشاء/الدفع.
●	Webhooks للأحداث: توقيع/تحقق، إعادة محاولات بخوارزمية backoff، وDeduplication.
●	حافلة أحداث (Event Bus) داخلية للأحداث الموحّدة.
ب) أهم الأحداث (نماذج أسماء)
●	order.created, order.status_changed
●	payment.authorized, payment.captured, payment.refunded
●	shipment.created, shipment.out_for_delivery, shipment.delivered, shipment.failed
●	cod.collected, cod.remitted
●	rma.requested, rma.resolved
●	cart.abandoned, product.stock_low


ج) مزوّدون نموذجيون والتكامل
●	الدفع: صفحات/SDK + Webhooks لحالات التفويض/التحصيل/الاسترداد. 3DS/SCA مفعّل.
●	الشحن: إنشاء بوليصة/ملصق، تتبّع، Webhooks للحالات، CSV بديل عند تعطل التكامل.
●	الرسائل: FCM (Push)، SMS/WhatsApp (مزود محلي/دولي) مع تتبّع التسليم/النقر.
●	التحليلات: GA4/Firebase (user_id = customer_id)، تدفّق أحداث الشراء.
●	المحاسبة/ERP: ترحيل الإيراد، الخصومات، المرتجعات، وحساب وسيط COD، وتسويات المزوّدين.
●	الإعلانات/الجماهير: مزامنة شرائح (VIP/غير نشطين) عبر Reverse ETL (اختياري).
د) عقود البيانات والمعالجات
●	عقد حقول واضح لكل تكامل (مطلوب/اختياري/أنواع/نطاقات).
●	توحيد المناطق الزمنية (Asia/Aden) والعملات (تثبيت الصرف لحظة الطلب/الدفع).
●	قنوات بديلة عند الفشل (سقوط إلى CSV/Queue) دون فقدان البيانات.
هـ) الاختبار والبيئات
●	Sandboxes لمزوّدي الدفع والشحن.
●	بيانات اختبار مجهولة (لا PII حقيقية).
●	سيناريوهات فشل إجبارية: انقطاع Webhook، اختلاف مبالغ COD، تتبع مفقود.
 
4) مؤشرات الحوكمة والتكامل
●	دقة التطابق بين طلبات↔مدفوعات↔شحنات (اختلاف = 0).
●	زمن معالجة Webhook المتوسط < 2 ثانية؛ نسبة إعادة المحاولات ضمن حد مقبول.
●	نجاح مزامنة جماهير التسويق > 99%.
●	اختبارات استعادة النسخ ناجحة شهريًا.
●	التزام الوصول حسب الدور (لا خروقات صلاحيات).
 
5) تعريف الاكتمال (Definition of Done)
●	أدوار وصلاحيات مُفعّلة، وسجلات تدقيق لكل العمليات الحساسة.
●	سياسات خصوصية/احتفاظ/DSR موثّقة ومجرّبة.
●	نسخ احتياطي قائم مع اختبار استعادة حديث.
●	مراقبة وتنبيهات فعّالة، وSLOs مضبوطة.
●	واجهات/ويبهوكس بإصدار ثابت، Idempotency، توقيع، وإعادة محاولات.
●	تكاملات الدفع/الشحن/الرسائل/التحليلات/المحاسبة تعمل من طرف لطرف مع سيناريوهات الفشل.

بهذه الحزمة تضمن تشغيلًا آمنًا وقابلًا للتوسع، وأرقامًا موثوقة، وتكاملات مستقرة— مع قدرة سريعة على اكتشاف الأعطال والتعافي منها، وامتثال واضح للخصوصية والمالية.
 
Architecture Decisions (ADR) 
●	الترميز/الترتيب
النوع: utf8mb4 مع collation = utf8mb4_0900_ai_ci على مستوى السيرفر/القاعدة/الجداول.
السبب: يدعم الإيموجي واللغات ويعطي فرزًا دقيقًا غير حساس للحركات وحسن الأداء في MySQL 8.
●	المفاتيح الأساسية والمعرّف العام
النوع: BIGINT UNSIGNED AUTO_INCREMENT كـ PK داخلي + حقل public_id = ULID (CHAR(26)).
السبب: أداء عالٍ للـPK المُجمّع، وULID قابل للفرز زمنيًا وآمن للمشاركة خارجيًا.
●	الحذف المنطقي
النوع: عمود deleted_at DATETIME NULL + فهرس + Views/Scopes تستثنيه افتراضيًا.
السبب: اتساق مع الأُطر الشائعة وسهولة الاسترجاع والتدقيق.
●	حجز المخزون
النوع: جدول reservations (sku_id, qty, state, reservation_expires_at, order_id nullable) + Job دوري لتحرير المنتهي.
السبب: يمنع البيع الزائد ويضمن تحرير الحجوزات غير المُتمَّمة.
●	تسويات الدفع عند الاستلام (COD)
النوع: cod_settlements و cod_settlement_items مع ربط للأوامر/المدفوعات/الشحن وحالات (open/submitted/reconciled/closed).
السبب: تتبّع مالي دقيق وقابل للمطابقة البنكية/الناقل.
●	إدارة المرتجعات (RMA)
النوع: rmas و rma_items بحالات واضحة (requested/approved/received/refunded/closed) وربط بأسباب ledger (return_to_stock/damaged/lost).
السبب: ربط محاسبي/مخزني مُحكم وتقليل الفقد.
●	سلسلة التوريد (المشتريات)
النوع: suppliers, purchase_orders, purchase_order_items, asn, grn, qc, landed_cost_allocations.
السبب: مصدر واحد للحقيقة وتوزيع تكلفة الوصول (Landed Cost) بشكل عادل (وزن/قيمة/كمية).
●	سياسات الاحتفاظ والأرشفة
النوع: Orders/RMAs: 5 سنوات – Payments/Settlements: 7 سنوات – Shipments/Fulfillment: 24 شهرًا – Inventory Ledger: 36 شهرًا – App Logs: 12 شهرًا – Raw Analytics: 6 أشهر مع طبقات مجمّعة دائمة.
السبب: توازن امتثال/تكلفة/أداء مع مسار أرشفة واضح.
●	أنواع الحالة/الأكواد
النوع: جداول مرجعية Lookup + مفاتيح خارجية (لا تُستخدم ENUM).
السبب: مرونة التعديل بدون تغييرات مخطط/نشر كود، مع سلامة مرجعية.
●	الفهارس وSLO للأداء
النوع: أهداف p95 لقراءات OLTP الأساسية ≤ 30ms وعمليات الكتابة ≤ 50–80ms، ومراجعة شهرية لأهم 10 استعلامات مع EXPLAIN وخريطة فهارس مُلزمة.
السبب: أداء مُتنبَّأ به وتقليل تضخم الفهارس والاستعلامات المنحرفة.
●	التقسيم (Partitioning)
النوع: inventory_ledger تقسيم RANGE شهريًا على txn_ts؛ نافذة بيانات “حارة” 18 شهرًا مع أرشفة أقدم.
السبب: أحجام كبيرة/كتابة كثيفة واستعلامات زمنية أسرع وصيانة أسهل.

●	الصلاحيات والبيانات الحساسة والتدقيق
النوع: audit_log ملاحق فقط (append-only) مع JSON diff، Views مقنّعة للـPII، تشفير بالحفظ، احتفاظ للتدقيق 5 سنوات، Least-Privilege على مستوى الدور.
السبب: امتثال وتتبع تغييرات غير قابل للعبث وتقليل سطح المخاطر.
●	القاموس البياني وERD
النوع: قاموس بيانات حي (Editable) + ERD مُحدَّث ضمن المستودع مع مصفوفة القيود.
السبب: توحيد الفهم، سهولة الانضمام للفريق، تقليل أخطاء النمذجة.
●	ضوابط الإنتاج
النوع: حظر phpMyAdmin كتابةً في الإنتاج، تغييرات المخطط عبر Migrations فقط، أذون قراءة مُقيّدة عند الحاجة.
السبب: حوكمة تغيير صارمة وتتبّع كامل وتقليل أخطاء بشرية.
 
Operational Controls 
●	ترحيلات مُعَنوَنة
اعتماد أداة migrations مع checksums، وGate في CI يمنع أي DDL خارج الترحيلات.
●	بيانات مرجعية مُصدَّرة
Versioning لـ seed/reference data وترحيلها بين البيئات تلقائيًا.
●	حواجز اتصال قاعدة البيانات
حدود صارمة لـ max connections/queue لكل خدمة + backoff وتوقيت p95 للحماية من الانهيار.
●	مهلات الاستعلام والقتل الآلي
تعريف max_execution_time وسياسة kill للـ long-running (عبر ProxySQL/pt-kill).
●	سياسة القراءة من النسخ المتماثلة
SLO لتأخر النسخ (<2s)، وRead-after-write fallback للـ primary تلقائيًا.
●	خطة تراجع مُختبرة
Point-in-Time Recovery مُجرَّب دوريًا + Playbook واضح بـ RPO/RTO.
●	إخفاء/تجزئة البيانات لغير الإنتاج
Pipeline لتوليد عينات فرعية مع إخفاء حتمي يحافظ على العلاقات.
●	تطبيع اليونيكود
فرض NFC ومنع الأحرف غير المرئية/ثنائية الاتجاه في الإدخال، مع فحص دوري.
●	سياسة المنطقة الزمنية
تخزين UTC فقط على مستوى القاعدة، وتعامل التحويل في طبقة التطبيق.
●	أنماط العمليات الضخمة
Batching (مثلاً 1k صف/معاملة)، chunking حسب PK، واستخدام SKIP LOCKED لتقليل التعارض.
●	ترحيلات عالية الخطورة بأسلوب Blue/Green
جداول/عروض ظلّية (shadow) مع تبديل تدريجي وقياسات قبل/بعد.
●	حراسة جودة البيانات تلقائيًا
Checks يومية: nulls غير متوقعة، ازدواج فريد، أيتام مرجعية، وانحراف مخطط (schema drift) مع تنبيه.
●	نافذة صيانة وخط اتصال
تعريف نافذة صيانة ثابتة، وخطوات تبليغ/تراجع موحدة للفِرق المعنية.
●	سياسة الإجراءات المخزّنة
منع المنطق التجاري داخل SP/Triggers (باستثناء تدقيق/حفظ سلامة بسيطة) مع بدائل واضحة في التطبيق.
 
ملخص آلية العمل واعتمادياتها 
ملخص آلية العمل واعتمادياتها
●	ADR = يحدد “ماذا ولماذا” (قرارات البنية والمعايير).
●	Operational Controls = يحدد “كيف ومتى ومن” (تشغيل/حوكمة/اختبارات).
●	الاعتماديات: CI/CD، أذونات DB، نسخ احتياطي/استعادة، مراقبة (Monitoring)، تنبيهات، نسخ متماثل (إن وُجد).
 
1) اربطها بالتنفيذ (CI/CD)
●	Gate يمنع أي DDL خارج migrations.
●	Checklists في الـCI:
○	فحص collation/charset الافتراضي + أي جدول شاذ.
○	فحص وجود public_id (ULID) لكل الجداول المستهدفة.
○	فحص تغطية deleted_at للجداول التي تتطلب soft-delete.
○	فحص وجود فهارس الحقول الحرجة (FKs/التواريخ/الحالات).
○	فحص سياسة التقسيم للجداول المحددة وإنشاء قسم الشهر القادم مسبقًا.
●	Artifacts إلزامية مع كل نشر: تقرير EXPLAIN لأهم 10 استعلامات + diff للمخطط + نتائج اختبارات الاستعادة.
2) عبِّئ “حقول الإثبات” داخل الوثيقتين
لكل بند رئيسي املأ: المالك (DRI)، SLO/SLA، أداة/آلية التنفيذ، أثر الفشل، دليل تحقق (Evidence)، تاريخ المراجعة.
3) فحص اليوم صفر (Day-0 Validation)
نفّذ هذا التحقق السريع قبل اعتبار المعيار مُعتمدًا:
1.	Collation/Charset: ثابت على مستوى السيرفر/القاعدة/الجداول (لا استثناءات).
2.	PK + public_id: BIGINT PK داخلي + ULID موجود ومفهرس حيث يلزم.
3.	Soft-delete: deleted_at مفهرس + جميع الـViews/Scopes تستثنيه افتراضيًا.
4.	الحجز (Reservations): سيناريو إنشاء/انتهاء مهلة/تحرير تلقائي ناجح.
5.	COD Settlements: دورة حياة كاملة (open→reconciled→closed) مع الربط بالفواتير.
6.	RMA: انتقالات الحالات وتحديث ledger والأرصدة المالية تعمل.
7.	Procurement/Landed Cost: PO→ASN→GRN→QC→Allocation تعمل والأرقام موزعة كما اخترتم (وزن/قيمة/كمية).
8.	Inventory Ledger: يُسجل كل الحركات، والتقسيم مفعل، وأرشفة >18 شهر جاهزة.
9.	RBAC/PII: Views مقنّعة تعمل، وأقل صلاحيات مفروضة فعليًا.
10.	Backups & PITR: استعادة تجريبية ناجحة داخل الزمن الهدف (RTO/RPO).
11.	Replication/Read-policy: تأخر النسخ ضمن الحد + fallback للقراءة من primary مثبت.
12.	Monitoring/Alerts: تنبيهات p95 للأداء، تأخر النسخ، نمو الجدول/القسم، فشل نسخ احتياطي.

4) تعريف “اكتملنا” (Definition of Done)
●	كل بند في ADR له تطبيق مؤكد في البيئة (بدون TODOs).
●	كل بند في Operational Controls له Runbook مختصر + تنبيه عند الانحراف.
●	تقرير واحد من CI يثبت نجاح Day-0 + أسماء الملاّك لكل عنصر.
5) ترتيب التنفيذ (سريع)
●	 تفعيل Gates + فحوص CI + Day-0.
●	اختبار استعادة كامل + تحميل بيانات مرجعية بنسخها + ضبط التنبيهات.
●	مراجعة شهرية للأداء والفهارس + ربع سنوية لسياسات الاحتفاظ.
   

ملخص آلية العمل وروابطها/اعتمادياتها
●	ADR = قرارات البنية (repo).
●	Operational Controls = ضوابط التشغيل (repo + CI/CD + DB + Monitoring).
 
1) في مستودع الكود (Repo)
●	القرارات:
docs/adr/*.md (كل بند رقم/مالك/تاريخ).
●	ضوابط التشغيل/التشغيلية:
docs/runbooks/*.md وdocs/checklists/*.md.
●	المخطط والتوثيق:
docs/erd/ (ERD) + docs/data-dictionary.xlsx.
●	الهجرة (migrations) والبيانات المرجعية:
Laravel: database/migrations/, database/seeders/
(أو Flyway/Liquibase: db/migrations/, db/seeds/).
●	استعلامات الفحص الآلي:
ops/sql/schema_checks/*.sql (فحوص collation/PK/soft-delete/فهارس).
●	اسكربتات اليوم صفر:
ops/day0/*.sh|sql.
2) في CI/CD
●	ملفات الأنابيب:
GitHub Actions: .github/workflows/db-ci.yml
(أو GitLab: .gitlab-ci.yml).
●	Gates إلزامية:
○	منع أي DDL خارج migrations.
○	تشغيل ops/sql/schema_checks/*.sql ضد قاعدة اختبار.
○	توليد تقارير EXPLAIN لأهم 10 استعلامات وحفظها كـ Artifacts.
●	خطوات نشر DB:
○	تشغيل migrations + seeders على Staging ثم Production.
○	نشر جداول التقسيم للشهر القادم مسبقًا.
●	مستند إثبات:
يخرج من الـCI ملف artifacts/db-compliance-report.html.
3) على خادم قاعدة البيانات (MySQL)
●	إعدادات ثابتة (my.cnf):
character_set_server=utf8mb4
collation_server=utf8mb4_0900_ai_ci
default_time_zone='+00:00'
●	صلاحيات/أدوار:
إنشاء أدوار read/write/admin وتطبيق least-privilege للحسابات.
●	نسخ متماثل/تقسيم:
تفعيل تقسيم inventory_ledger (شهري) وخطة أرشفة.
●	مهلات وحدود:
ضبط مهلة الاستعلام والاتصالات (timeouts/limits) حسب الـSLO.
4) في طبقة التطبيق (Jobs/Cron)
●	حجز المخزون:
Job ينفّذ كل دقيقة: تحرير reservations منتهية الصلاحية.
●	أرشفة/Retention:
Jobs لسياسات الاحتفاظ (نقل البارد إلى أرشيف).
●	فحوص جودة البيانات:
Job يومي لفحص nulls/duplicates/orphans وإرسال تنبيه.
5) طبقة البروكسي/الوسيط (اختياري لكن مُستحسن)
●	ProxySQL / pgbouncer-style:
○	توزيع قراءات على Replica مع fallback للـPrimary.
○	قتل الاستعلامات الطويلة تلقائيًا.
○	تحديد connection pooling/limits لكل خدمة.
6) المراقبة والتنبيهات (Monitoring)
●	Grafana/PMM/CloudWatch (حسب بيئتك):
لوحات وAlerts لـ:
○	p95 للقراءة ≤ 30ms والكتابة ≤ 80ms.
○	تأخر النسخ (replication lag).
○	نمو الجداول والأقسام.
○	نجاح/فشل النسخ الاحتياطي وPITR.
○	معدّلات الأخطاء في Jobs التشغيلية.
7) النسخ الاحتياطي والاستعادة (Backups/PITR)
●	Managed (RDS/Aurora) أو Self-hosted (XtraBackup):
○	جدولة نسخ يومية + سجلات للـPITR.
○	اختبار استعادة شهري وتوثيقه في docs/runbooks/restore.md.
8) (Day-0 Validation)
●	تشغيل ops/day0/validate.sh من CI ضد Staging:
○	يختبر collation/charset/UTC/PK/public_id/soft-delete/الفهارس/التقسيم.
○	يختبر دورة RMA وCOD وReservation end-to-end ببيانات عينة.
○	يخرج تقرير نجاح واحد موقّع من Dev/DBA/Ops.
9) أين أضع التنبيهات والملكية (DRI)
●	جدول مُوحّد للملكية: docs/owners.yml
لكل بند (ADR/Control): مالك، SLO/SLA، أداة التحقق، التنبيه، تاريخ المراجعة.
 
تنفيذ سريع (اقتراح)
1.	أضِف المجلدات/الملفات المذكورة في Repo الآن.
2.	أنشئ Workflow واحد للـCI باسم db-ci.yml يطبق Checks + Artifacts.
3.	فعّل إعدادات MySQL في my.cnf وأعد تشغيل الخدمة.
4.	أضف 3 Jobs في التطبيق: reservations, retention, dq-checks.
5.	أنشئ لوحات Grafana وتنبيهاتها، ثم اختبر PITR فعليًا وسجّله في الـRunbook.
قوالب لـ:
●	db-ci.yml،
●	schema_checks.sql،
●	owners.yml,
●	restore.md,
●	reservations_expiry_job (Laravel Command).
 
سياسة حذف (PII Erasure & Transaction Retention) 
سياسة حذف حساب العميل (PII Erasure & Transaction Retention)
ملخص آلية العمل واعتمادياتها
●	المبدأ: حذف/تمويه بيانات التعريف الشخصية (PII) مع الاحتفاظ بالمعاملات (طلبات/شحن/محفظة/فواتير) لأغراض المحاسبة والتدقيق.
●	الاعتماديات: DB (MySQL)، نظام المحفظة/المدفوعات (يشمل COD)، الشحن، نظم الهوية (Firebase/Auth)، التحليلات (GA4/BigQuery)، قنوات الرسائل (Email/SMS/Push)، النسخ الاحتياطي/الاستعادة، CI/CD.
 
1) نطاق السياسة
تنطبق على: users، orders، shipments، invoices، wallet_ledger، rmas، returns، analytics identity وكل ما يخزّن PII (الاسم، الهاتف، الإيميل، العنوان التفصيلي، مُعرّفات الأجهزة/الدفع).
2) قرارات معمارية (ADR مختصرة)
1.	الاحتفاظ بالمعاملات وإخفاء PII: تبقى سجلات الطلبات والدفعات والمرتجعات، مع تمويه حقول الاتصال والعنوان التفصيلي.
2.	استبدال الهوية: بعد الإزالة، يُستبدل الربط بـ anonymized_customer_id بدلاً من user_id في السجلات التاريخية.
3.	شرط التسوية قبل الإزالة: أي طلب/RMA مفتوح أو رصيد محفظة ≠ 0 يوقف الإزالة النهائية حتى التسوية.
4.	عدم الرجوع: تخزين pii_hash (hash مُملّح لقنوات التعريف) لأغراض منع إساءة الاستخدام بدون قابلية استرجاع PII.
5.	حذف المعرّفات التشغيلية: إلغاء الجلسات، OAuth، Push/device IDs، وإصدار طلب حذف لأنظمة الطرف الثالث.

3) تغييرات المخطط المطلوبة (DDL المعياري)
●	جدول anonymized_customers
○	الأعمدة: anonymized_customer_id (ULID), created_at.
●	users
○	أعمدة جديدة: deleted_at, erased_at, erase_job_id, pii_hash, anonymized_customer_id (nullable).
○	تفريغ/تمويه أعمدة PII عند الإزالة (name/email/phone/address*).
●	الجداول المرتبطة بالعميل (orders, shipments, invoices, rmas, wallet_ledger, …)
○	إضافة عمود: anonymized_customer_id (nullable, indexed).
○	قاعدة التكامل: عند الإزالة النهائية: user_id = NULL وanonymized_customer_id مُعبّأ. (يُفرض بقيود تحقق/Triggers خفيفة أو عبر Jobs).
●	wallet_ledger
○	إضافة نوع حركة: wallet_closure لإقفال الرصيد إلى صفر قبل الإزالة.
●	Views/Scopes
○	عروض قراءة تُخفي PII افتراضيًا وتعرض المدن/المناطق فقط إن لزم محاسبيًا.
ملاحظة تصميمية: تُنشأ فهارس على anonymized_customer_id في كل الجداول، وفهرس مركّب على (state, reservation_expires_at) إن وُجدت حجوزات مرتبطة.
4) تمويه/إخفاء PII (معايير)
●	الاسم: يُمسح أو يُستبدل بقيمة ثابتة ([Erased]).
●	الهاتف/الإيميل: تمويه غير قابل للعكس (مثل ****1234 للهاتف وآلية Hash مُملّحة داخليًا للحظر/التحقق دون تخزين الأصل).
●	العنوان: حذف السطور التفصيلية، إبقاء المدينة/المنطقة/الدولة فقط عند الحاجة المحاسبية.
●	المعرّفات التشغيلية: حذف Tokens والجلسات وPush/device IDs والموافـقات التسويقية.
5) تدفق التنفيذ (Runbook مختصر)
A) عند تقديم طلب حذف
1.	فحص مسبق:
○	طلبات/RMAs مفتوحة؟
○	رصيد محفظة موجب/سالب؟
○	نزاعات/Chargebacks؟
2.	لو توجد حالات مفتوحة:
○	تعطيل الحساب فورًا (لا تسجيل دخول، لا تسويق)، وجدولة الإزالة بعد (تسليم/إلغاء/إغلاق RMA).
3.	رصيد محفظة > 0:
○	صرف آلي لنفس وسيلة الدفع إن أمكن؛ وإلا: تسوية بديلة (تحويل بنكي/محفظة جوال/قسيمة).
○	عدم استجابة العميل 14 يومًا ⇒ صرف افتراضي محدّد مسبقًا.
4.	رصيد محفظة < 0:
○	تحصيل/إلغاء وفق السياسات حتى يصل إلى 0، ثم المتابعة.
B) الإزالة النهائية
1.	إنشاء anonymized_customer_id وتعبئته في users وفي كل الجداول التابعة.
2.	تفريغ/تمويه PII في users (واللقطات snapshot في الطلبات/الشحن/الفواتير).
3.	وضع user_id = NULL في الجداول التابعة، وتعبئة anonymized_customer_id.
4.	wallet_ledger: قيد wallet_closure لرصيد = 0 وقفل المحفظة.
5.	طرف ثالث: حذف من Firebase/Auth، إرسال user deletion لـ GA4/BigQuery بالمعرّف، إزالة من Email/SMS/Push.
6.	تسجيل audit_log لا يُمكن التلاعب به (من/متى/ماذا).
6) حالات الحافة
●	COD قيد التسليم: لا إزالة نهائية قبل “مُسلّم/ملغى”.
●	نزاع/احتيال: احتفاظ بالحد الأدنى اللازم للدفاع القانوني لمدة محددة (مثلاً 12–24 شهرًا)، مع PII مُموّهة.
●	عودة العميل لاحقًا: يُعامل كـ “حساب جديد”، لا ربط بالبيانات الممحوة، ويُمنع الربط الالتفافي عبر pii_hash (منع تعدد الحسابات المؤذي).

7) الامتثال والاحتفاظ
●	المعاملات: الاحتفاظ حسب سياسة المؤسسة (مثلاً: طلبات/فواتير 5–7 سنوات).
●	النسخ الاحتياطية: لا تعديل رجعي؛ تُزال PII من الأنظمة الحيّة ويُكتفى بانقضاء فترات الاحتفاظ على النسخ.
●	الوصول: تقييد صارم لأدوار القراءة على السجلات الممحوة/المُمَوّهة.
8) المراقبة وقياس النجاح (KPIs)
●	Pass rate لسيناريو “Erase User” في الـCI/Staging.
●	زمن المعالجة من طلب الحذف حتى الإزالة النهائية ضمن حد أقصى (مثلاً ≤ 30 يومًا لو توجد حالات مفتوحة).
●	% تغييرات DB عبر migrations (هدف 100%).
●	صفر إرسال تسويقي بعد deleted_at.
●	فشل/نجاح مهام صرف المحفظة وإلغاء المعرّفات الطرفية.
9) الملكية والتشغيل
●	DRI: فريق البيانات/المنصّة.
●	Runbooks: موجودة في تبويب Operational Controls (سيناريوهات: طلب حذف، صرف رصيد، إزالة طرف ثالث، استعادة/تراجع).
●	مراجعة دورية: ربع سنوية لتحديث المدد ومعايير التمويه.
10) تعريف 
●	لا أوامر/نزاعات مفتوحة + محفظة = 0.
●	تنفيذ Job الإزالة أنهى: تمويه PII، نقل الهوية إلى anonymized_customer_id، إلغاء Tokens والأطراف الثالثة.
●	سِجِل تدقيق كامل + مؤشرات المراقبة الخضراء.
 
سياسة دمج الحسابات المكررة (Account Merge) 
سياسة دمج الحسابات المكررة (Account Merge)
ملخص آلية العمل واعتمادياتها
●	المبدأ: توحيد السجلات المتكرّرة لنفس العميل دون فقدان أي معاملات أو أرصدة، مع سجّل تدقيق كامل وقابلية تراجع.
●	الاعتماديات: قاعدة البيانات، نظام الهوية (Firebase/Auth)، المحفظة/المدفوعات (يشمل COD)، الشحن، التحليلات (GA4/BigQuery)، قنوات الرسائل، CI/CD والمراقبة.
 
1) نطاق السياسة
تنطبق على: users، addresses، orders، shipments، invoices، wallet_ledger، coupons/loyalty، rmas/returns، consents، sessions/tokens، analytics identity.
2) قرارات معمارية (ADR مختصرة)
1.	حساب مستهدف واحد (Target User): يُحدَّد وفق أعلى ثقة تحقق + أقدمية + نشاط/رصيد المحفظة.
2.	دمج آمن وقابل للتراجع: تنفيذ عبر Job مُراقَب بمرحلة Dry-Run ثم Commit مع account_merge_links وAudit لا يُمكن العبث به.
3.	حماية الخصوصية: لا يُدمَج حسابان دون تحقق هوية (OTP للهاتف أو Proof للـEmail/مزود الدخول).
4.	مبدأ الأقل خطورة: عند تعارضات PII أو عناوين/موافقات، تُحفَظ النسخ ويفوز الحقل المُوثَّق/المُتحقَّق؛ الباقي يُؤرشف.
5.	حماية المحفظة والمعاملات: تُجمَع أرصدة المحفظة وقسائم/نقاط الولاء وتُنقَل جميع العلاقات للـTarget بدون أي فقد.
3) معايير التطابق (Matching Signals)
●	قوية (لازمة للدمج التلقائي): هاتف مُوثّق مطابق، أو بريد مُوثّق مطابق، أو موحِّد خارجي (Firebase UID / Apple/Google).
●	مساندة (ترفع النقاط): تطابق device fingerprint، تكرار عناوين الشحن (مدينة/منطقة + اسم)، طريقة دفع/رمز IBAN متكرر، سجلات طلب لنفس الاسم مع أرقام قريبة، pii_hash مطابق.
●	عتبة قرار: Score ≥ 0.85 ⇒ دمج تلقائي؛ 0.6–0.85 ⇒ قائمة مراجعة بشرية؛ < 0.6 ⇒ رفض.
4) تغييرات المخطط (DDL)
●	account_merge_jobs: حالة الدمج، العتبة، نتائج dry-run، المالك (DRI)، الطوابع الزمنية.
●	account_merge_links: mapping من source_user_id إلى target_user_id مع نسخة PII أرشيفية وتمييز الحقول المتضاربة.
●	users: أعمدة merged_into_user_id (nullable), merge_at, merge_job_id.
●	فهارس: فهارس على merged_into_user_id وعلى مفاتيح الربط المتأثرة لضمان انتقال سريع.
●	قيود تكامل: السماح بإعادة إسناد FK من source→target عبر Job (لا CASCADE تلقائي على الإنتاج؛ التنفيذ مُتحكَّم به).
5) تدفق التنفيذ (Runbook مختصر)
A) اكتشاف المرشحين
●	Job دوري يحسب merge_score وفق الإشارات أعلاه ويُنتج قائمة مرشحين.
●	حالات 0.6–0.85 تُدفع لصف مراجعة بشرية (Backoffice).
B) التحقق
●	إرسال OTP للهاتف/البريد أو التحقق عبر مزود الدخول للحسابين لإثبات الملكية.
●	توثيق الموافقة الداخلية (Tick في النظام) قبل الدمج.
C) الدمج (مرحلتان)
1.	Dry-Run:
○	إحصاء العلاقات التي ستُعاد إسنادها (Orders/Wallet/Shipments/…)، كشف التعارضات (Addresses/Consents/PII).
○	Guardrails: حد أقصى للصفوف المتأثرة/المدة؛ إن تجاوزه → إيقاف للمراجعة.
2.	Commit:
○	نقل جميع العلاقات إلى target (دفعات صغيرة مع معاملات).
○	Wallet: تجميع الأرصدة وتسجيل قيد توضيحي wallet_merge.
○	Loyalty/Coupons: ترحيل الرصيد ووسم القسائم المُكررة كـ منتهية.
○	Sessions/Tokens: إبطال Sessions المصدر وتوحيد Push Tokens في الهدف.
○	تحديث users: وضع merged_into_user_id على المصدر وتعطيله.
○	تحديث مزوّد الهوية: ربط المزوّدين بالـtarget فقط.
D) التراجع (Rollback)
●	ضمن نافذة قصيرة (مثلاً 24–48 ساعة):
○	استخدام account_merge_links لعكس إعادة الإسناد.
○	إعادة الأرصدة كما كانت وتفعيل حساب المصدر.
6) قواعد فضّ النزاعات (Conflict Resolution)
●	PII: يفوز المُوثَّق (Verified). إن كان كلاهما موثّقًا ومختلفًا ⇒ الاحتفاظ بكلا القيمتين مؤرشفتين، ويُطلب اختيار المستخدم لاحقًا.
●	العناوين: إبقاء جميع العناوين ووسم غير النشط منها. العنوان الافتراضي = الأكثر استخدامًا.
●	الموافقات (Consents): تطبيق OR (إن وافق على قناة في أي حساب تُعتبر موافقًا)، مع إرسال إشعار مراجعة للمستخدم.
●	الإعدادات/التفضيلات: آخر تعديل يربح، مع سجل تغييرات.
7) المراقبة وقياس النجاح (KPIs)
●	Duplicate rate شهريًا (قبل/بعد).
●	Merge accuracy (نسبة عدم وجود تراجعات).
●	Avg merge duration p95.
●	Tickets عن دمج خاطئ (يُراد تقليلها إلى صفر).
●	أثر الإيراد/التحويل لزوار كانوا مجزئين عبر حسابات متعددة.
8) حالات الحافة
●	طلبات أو RMAs مفتوحة في المصدر: الدمج مسموح؛ تُنقل الحالة كما هي وتُكمَّل على الهدف.
●	محفظة سالبة/نزاع دفع: الدمج يتطلب موافقة مسؤول مالي؛ وإلا يُؤجَّل.
●	بلدان/عملات مختلفة: الإبقاء على السجلات كما هي؛ لا تحويل عملة آليًا—تُعرض تقارير موحّدة على المستوى التحليلي.
●	حساب مشتبه بالاحتيال: لا دمج تلقائي؛ مسار مراجعة خاصة.
9) الملكية والتشغيل
●	DRI: فريق البيانات/المنصّة.
●	المراجعة: أسبوعية لحالات المراجعة المؤجلة، ورُبع سنوية لمعادلات الـscoring.
●	التوثيق: Runbook مفصّل وPlaybook دعم للتعامل مع بلاغات الدمج الخاطئ.
10) تعريف
●	تنفيذ Dry-Run ثم Commit دون تجاوز الـGuardrails.
●	تحويل كل العلاقات والظهور بحساب واحد فعّال فقط.
●	إبطال جميع Tokens المصدر، وتحديث مزوّدي الهوية.
●	سجلات Audit كاملة، وصفحة Merge Report مرفقة في الـCI Artifacts.
 
سياسات اخرئ 
سياسة اخرئ للحسابات، بشكل مختصر من الضروري التركيز علئ كل سياسة بشكل منفصل

●	النطاق: سياسات تشغيل لح lifecycle حساب العميل.
●	الاعتماديات: قاعدة البيانات، نظام الهوية (Firebase/Auth أو مزود خارجي)، المحفظة/المدفوعات (يشمل COD)، قنوات الرسائل، التحليلات (GA4/BigQuery)، CI/CD والمراقبة.
 
1) سياسة تعطيل الحساب المؤقت (Account Freeze)
الهدف: إيقاف الوصول والطلبات مؤقتًا دون حذف أو كسر التدفق المالي/اللوجستي.
المحفزات: اشتباه احتيال، نزاع مالي، طلب العميل، تحقيق أمني.
الإجراءات:
●	users.status = frozen مع freeze_reason, freeze_until.
●	إبطال الجلسات/التوكينات ومنع تسجيل الدخول، الطلبات، تغييرات PII؛ السماح بردّ الأموال وخدمة العملاء.
●	إيقاف التسويق (consents موقوفة مؤقتًا) وإظهار لافتة في التطبيق.
●	رفع التجميد يدويًا أو تلقائيًا عند freeze_until.
تعريف الاكتمال (DoD): لا إنشاء طلبات أثناء التجميد، كل التوكينات مُبطلة، سجل تدقيق مكتمل.
KPIs: زمن التجميد p95، صفر طلبات/دفعات جديدة خلال التجميد.
 
2) سياسة تصحيح بيانات العميل (Rectification)
الهدف: تصحيح PII بأمان مع أثر تدقيقي كامل وتزامن للأطراف الثالثة.
المحفزات: طلب العميل، خطأ إدخال، مطلب قانوني.
الإجراءات:
●	تحقق هوية (OTP/مزود دخول).
●	تحديث آمن لحقول PII + تحديث pii_hash، وتسجيل diff في audit_log.
●	مزامنة مع Auth/Email/SMS/Analytics، وإعادة تقييم مطابقة/دمج الحسابات إذا تغيّر الهاتف/الإيميل.
DoD: البيانات محدثة ومتسقة في جميع الأنظمة، إشعار نجاح للعميل، سجل تدقيق موجود.
KPIs: SLA ≤ 24 ساعة، معدل أخطاء مزامنة = 0%.
 
3) سياسة تغيير/استرجاع رقم الهاتف الأساسي
الهدف: تغيير الرقم مع حماية قوية من اختطاف الحساب.
المحفزات: فقدان الرقم، تبديل شركة، خطأ سابق.
الإجراءات:
●	تحقق مزدوج: OTP للرقم القديم والجديد (أو بديل هوية إذا القديم غير متاح).
●	نافذة أمان (cool-off) قصيرة لتعطيل العمليات الحساسة.
●	تحديث الهاتف في Auth وDB، تجديد pii_hash، تحديث خرائط التحليلات.
●	حفظ سجل في phone_history، منع إعادة استخدام الرقم لفترة محدودة إذا رُصدت مخاطر.
DoD: الرقم الجديد مُوثق، الجلسات الحرجة مُجدَّدة، لا تنبيهات احتيال.
KPIs: معدل نجاح التحقق، صفر بلاغات استحواذ بعد التغيير.
 
4) سياسة نقل الهوية بين المنصّات (Provider Re-link)
الهدف: ربط/فصل مزود دخول (Apple/Google/Email) بأمان مع الحفاظ على هوية تحليلات موحّدة.
المحفزات: رغبة العميل بتغيير طريقة الدخول، توحيد مزودين، حل مشاكل وصول.
الإجراءات:
●	تحقق ملكية الحساب الحالي والمزود الهدف.
●	تحديث جدول auth_providers (provider, provider_uid) وربط واحد “أساسي”.
●	نقل الجلسات الآمنة، التحقق من عدم وجود حساب مكرر؛ إن وُجد ⇒ دمج حسابات وفق سياسة الدمج.
●	تحديث هوية التحليلات وربط user_id الموحد.
DoD: تسجيل دخول يعمل عبر المزود الجديد فقط، لا حسابات مكررة، سجلات تدقيق مكتملة.
KPIs: نجاح الربط من أول مرة، صفر حالات فقدان وصول، انخفاض الازدواجية.
 
ملخص آلية العمل 
آلية العمل 
●	السياسات: حذف الحساب، دمج المكرّر، تعطيل مؤقت، تصحيح PII، تغيير/استرجاع رقم الهاتف، نقل الهوية بين المنصّات.
●	الاعتماديات: DB (MySQL)، Auth (Firebase/Apple/Google/Email)، Wallet/Payments (يشمل COD)، Notifications، Analytics (GA4/BigQuery)، CI/CD، Monitoring.
 
1) تغييرات قاعدة البيانات (DDL الموحّد)
●	users:
status ENUM('active','frozen','deleted'), deleted_at, erased_at, pii_hash, anonymized_customer_id, merged_into_user_id, merge_at.
●	phone_history(user_id, phone, verified_at, changed_at, reason)
●	auth_providers(user_id, provider, provider_uid, is_primary)
●	account_merge_jobs(id, target_user_id, score, state, dry_run_report, committed_at)
●	account_merge_links(source_user_id, target_user_id, merge_job_id)
●	فهارس على: anonymized_customer_id, merged_into_user_id, و(provider, provider_uid).
DoD (للـDDL): الترحيلات مُعتمدة عبر CI، ولا استثناءات خارج migrations.
 
2) واجهات الـAPI (عقود مختصرة)
●	حذف: POST /account/erase → يتحقق من الرصيد/الطلبات ثم يشغّل Job الإزالة.
●	تجميد/إلغاء: POST /account/freeze, POST /account/unfreeze.
●	تصحيح PII: POST /account/rectify (OTP مسبق).
●	تغيير رقم الهاتف: POST /account/phone/change (OTP للقديم والجديد أو بديل هوية).
●	نقل الهوية: POST /account/identity/relink (تحقق مزوّدين + منع ازدواج).
●	دمج: GET /account/merge/dry-run, POST /account/merge/commit (requires DRI approval).
DoD (للـAPI): مصادقة قوية، أخطاء مفسّرة، جميع العمليات idempotent.
 
3) Jobs/Cron
●	erase_user_job: تمويه PII، فك الربط للطرف الثالث، نقل user_id→anonymized_customer_id.
●	wallet_closure_job: تصفير المحفظة قبل الإغلاق/الحذف/الدمج.
●	merge_executor_job: نقل العلاقات على دفعات + سجل تدقيق + إمكانية rollback خلال 24–48 ساعة.
●	consent_suppression_job: قمع الإرسال لمن حالته frozen/deleted.
DoD: كل Job يكتب نتائج تشغيل قابلة للتدقيق + تنبيه عند الفشل.
 
4) أحداث التحليلات (Analytics Events)
●	account_deleted, account_frozen, account_unfrozen, account_rectified, phone_changed, provider_relinked, account_merged.
●	الخصائص الأساسية: reason, actor (user/agent/system), latency_ms, success.
DoD: الأحداث تظهر في BigQuery خلال ≤ 5 دقائق وتُطابق عدّادات الـDB.
 
5) المراقبة والتنبيهات (Monitoring & Alerts)
●	SLO:
○	p95 تنفيذ erase_user_job ≤ 2m بعد التسوية.
○	p95 دمج الحساب ≤ 5m (بناء على الحجم).
●	تنبيهات: فشل أي Job، ارتفاع merge rollback، رسائل تسويقية خرجت بعد deleted_at, اختلاف العدّ بين GA4 وDB > 3%.
 
6) حوكمة التشغيل (Runbooks مختصرة)
لكل سياسة صفحة 1–2: الهدف، متى تُستخدم، خطوات دقيقة، رسائل جاهزة للعميل، نقاط تراجع (Rollback)، مالك DRI.
 
7) اختبارات “اليوم صفر” (Day-0)
●	Erase: عميل برصيد محفظة>0 + طلب مفتوح ⇒ منع الإزالة حتى التسوية، ثم نجاح التمويه وربط anonymized_customer_id.
●	Merge: حسابان بموفّق قوي (هاتف موثّق) ⇒ Dry-run يعطي diff صحيح ثم Commit ينقل كل العلاقات ويُبطل توكنات المصدر.
●	Freeze/Unfreeze: لا طلبات جديدة أثناء frozen؛ رفع التجميد يُعيد الوصول.
●	Rectify: تغيير بريد/اسم ⇒ يظهر diff في audit ويتزامن مع Auth/تحليلات.
●	Phone Change: OTP مزدوج + نافذة أمان قصيرة + تحديث phone_history.
●	Re-link: ربط Apple→Google ⇒ لا ازدواج، وإلزام دمج إذا اكتُشف حساب آخر.
DoD: جميع سيناريوهات Day-0 “Pass” في Staging وتقرير واحد artifact من الـCI.
 
8) رسائل جاهزة (Customer-Facing)
●	قوالب مختصرة (عربي/إنجليزي) للحذف، التجميد، نجاح الدمج، تغيير الهاتف، نقل الهوية—تُحفظ في docs/runbooks/messages.md.
 
سياسة تنظيف الأجهزة (Device & Session Purge) 
سياسة تنظيف الأجهزة والجلسات (Device & Session Purge)
1) الهدف
إلغاء وصول العميل فورًا عبر مسح/إبطال الجلسات وتوكينات OAuth ورموز الدفع بالإشعارات (Push Tokens) وبصمات الأجهزة، مع سجل تدقيق كامل وإمكانية التكرار بدون آثار جانبية.
2) المحفزات
●	حذف الحساب النهائي، تجميد الحساب، دمج الحسابات، تغيير/استرجاع الهاتف، نقل الهوية بين المنصات.
●	اشتباه استحواذ (ATO)، بلاغ أمن/اختراق، طلب العميل “تسجيل الخروج من كل الأجهزة”.
3) النطاق
●	الطبقات: Auth (جلسات/Refresh Tokens/OAuth)، Push (FCM/APNS/WebPush)، التطبيق (بصمات الأجهزة)، التحليلات (user_pseudo_id عند الحاجة).
●	لا تُغيّر بيانات الطلبات/المعاملات؛ التأثير “وصول فقط”.
 
4) تغييرات قاعدة البيانات (DDL مختصر)
التزم بـ utf8mb4_0900_ai_ci وUTC. المعرّفات ULID (CHAR(26)). استخدم Lookup tables بدل ENUM (مثل: lk_revoke_reason, lk_push_token_status, lk_platform).
●	auth_sessions
session_id, user_id, created_at, expires_at, last_seen_at,
ip, user_agent, revoked_at, revoke_reason_id, revoked_by (system/user/admin).
فهارس: (user_id), (expires_at), (revoked_at).
●	oauth_tokens
token_id, user_id, provider, scope, issued_at, expires_at,
revoked_at, revoke_reason_id, revoked_by.
فهارس: (user_id,provider), (expires_at), (revoked_at).
●	push_devices
device_id, user_id, platform_id, push_token, push_token_status_id,
invalidated_at, invalidated_reason_id, last_notified_at, last_seen_at, app_version, notifications_opt_in.
فهارس: (user_id), (push_token_status_id), (invalidated_at).
●	devices (اختياري لبصمة الجهاز)
device_hash, user_id, first_seen_at, last_seen_at, trust_score, blocked_at, block_reason_id.
فهارس: (user_id), (device_hash UNIQUE).
●	audit_log
يسجل كل عمليات الإبطال/المسح (من/متى/ماذا/لماذا).
●	Retention
حذف سجلات الجلسات/التوكينات المنتهية بعد 90 يومًا (Purging Job) مع بقاء سجل التدقيق لمدة 5 سنوات.
 
5) عقود الـAPI (مختصر وواضح)
●	POST /account/sessions/purge (عميل): يتطلب OTP؛ يُبطل جميع الجلسات/التوكينات/Push Tokens.
●	POST /admin/users/{id}/sessions/purge (مسؤول): مع سبب الإبطال.
●	POST /devices/purge (عميل): مسح الأجهزة المرتبطة وتوكينات الـPush.
●	خصائص مشتركة: idempotent، ردّ يحصي ما أُبطل، يسجّل Audit، يُطلق أحداث Analytics.
 
6) التنفيذ (الترتيب مهم)
1.	Revoke OAuth/Refresh Tokens أولًا (تمنع إصدار جلسات جديدة).
2.	Revoke App/Web Sessions: وضع revoked_at + سبب، ومسح Sessions Cache.
3.	Invalidate Push Tokens: تعيين push_token_status_id = invalid + invalidated_at ومسحها من مزوّد الإرسال.
4.	Purge Devices: مسح/حظر device_hash ذات الثقة المنخفضة، وتصفير trust_score عند ATO.
5.	Third-parties: إبطال عبر SDK/واجهة المزود (قنوات Auth/Push).
6.	Analytics (اختياري حسب السياسة): إعادة تعيين user_pseudo_id إذا كان الهدف قطع التتبع.
7.	Audit & Notify: سجل تدقيق + رسالة قصيرة للعميل (“تم تسجيل خروجك من كل الأجهزة”).
ملاحظة: التنفيذ قابل للتكرار (idempotent). أي سجل مُبطَل مسبقًا يُتجاهل دون خطأ.
 
7) Jobs/Cron
●	purge_expired_sessions_job (كل 15 دقيقة): إبطال/حذف الجلسات/التوكينات المنتهية.
●	push_token_cleanup_job (ساعة): استخدام ردود FCM/APNS (مثل NotRegistered/InvalidToken) لتحديث push_token_status_id.
●	device_quarantine_job (ساعة): حظر الأجهزة ذات أنماط شاذة (Failed OTP متكرر، مواقع متعددة في دقائق).
 
8) المراقبة والتنبيهات
●	SLOs:
○	p95 زمن تنفيذ API/purge ≤ 30 ثانية.
○	p95 زمن استكمال Jobs ≤ 5 دقائق.
●	تنبيهات:
○	فشل Job متكرر، ارتفاع Active Sessions بعد عملية purge > 0 خلال 1 دقيقة،
○	معدل Push Tokens غير الصالحــة،
○	فروقات بين عدّ الـDB وأحداث Analytics > 3%.
 
9) اختبارات Day-0 (على Staging)
●	حساب بثلاث جلسات + Push Token + OAuth:
1.	استدعاء /account/sessions/purge → تتصفر كل الجلسات والتوكينات، وتصبح حالة Push = invalid.
2.	محاولة استدعاء API بالتوكين القديم ⇒ 401.
3.	وصول إشعار Analytics session_revoked, device_invalidated.
4.	تقرير CI يثبت أعداد ما قبل/بعد.
 
10) تعريف
●	جميع الجلسات/التوكينات/Push Tokens revoked/invalid للمستخدم المستهدف خلال ≤ 30 ثانية.
●	لا جلسات نشطة للمستخدم بعد دقيقة واحدة.
●	سجل تدقيق كامل، وتنبيه نجاح في الـCI/Monitoring.
●	عمليات الإبطال idempotent وقابلة للتدقيق.
 
11) حالات الحافة
●	حذف حساب مع طلبات مفتوحة: يُنفَّذ Purge فورًا (الوصول فقط)؛ تبقى المعاملات.
●	دمج حسابات: يُنفَّذ Purge لحساب المصدر، وتُنشأ جلسة واحدة جديدة للهدف فقط عند تسجيل دخوله.
●	تجميد مؤقت: Purge فوري + منع إنشاء جلسات جديدة حتى رفع التجميد.
●	NAT/Shared Devices: لا نحظر IP؛ الاعتماد على device_hash وOTP.
 
12) الملكية وSLA
●	DRI: فريق المنصّة/الأمن.
●	SLA: استجابة API فورية؛ معالجة Jobs ضمن النافذة الزمنية المحددة.
●	مراجعة ربع سنوية لإشارات “device_quarantine” ومعايير الثقة.
 
سياسة إدارة الطلبات (Orders Management) 
سياسة إدارة الطلبات (Orders Management)
1) ملخص آلية العمل واعتمادياتها
●	المبدأ: دورة حياة طلب واضحة وقابلة للتدقيق، تفصل الطلب عن الشحنة/الدفع، وتربط المخزون عبر inventory_ledger وreservations.
●	الاعتماديات: DB (MySQL)، بوابة الدفع/المحفظة (يشمل COD)، الشحن/التتبع، المخزون (PIM/OMS)، التنبيهات، التحليلات، CI/CD والمراقبة.
 
2) نطاق السياسة
تنطبق على: orders, order_items, order_addresses (snapshots), order_payments, shipments, inventory_ledger, reservations, adjustments/discounts, ndr/rto, returns (RMA مذكورة بسياسة منفصلة).
 
3) قرارات معمارية (ADR مختصرة)
1.	فصل المفاهيم: الطلب ≠ الشحنة ≠ الدفع (جداول وروابط منفصلة).
2.	حالات الطلب (lookup لا ENUM): draft, placed, confirmed, allocated, packed, shipped, delivered, closed, cancelled.
3.	الترقيم: order_number مستقل عن PK وبصيغة قابلة للقراءة (سنة/بلد اختياريًا).
4.	Snapshots ثابتة: عنوان/أسعار/ضرائب تُؤخذ لحظة التأكيد؛ لا تتأثر بتغيّر الكتالوج لاحقًا.
5.	المخزون: حجز عند checkout (TTL)، تخصيص عند confirmed/allocated، وخصم عند shipped.
6.	الدفع: prepaid تُلتقط/تُسجّل قبل الشحن؛ COD تُسوّى لاحقًا (سياسة COD).
7.	الإلغاء الذكي: حسب مرحلة المعالجة (تفصيل بالأسفل) مع أثر تلقائي على الحجز/التخصيص/الخصم.
8.	التعديلات: أي خصم/قسيمة/فرق شحن يُسجَّل في order_adjustments (دائن/مدين).
9.	Idempotency: لكل عمليات الكتابة (Header Idempotency-Key).
10.	المرونة التشغيلية: السماح بالشحنات المتعددة (Split), الدمج للشحن فقط (لا دمج طلبات ماليًا).
11.	نوافذ زمنية: تعريف واضحة لـ cancel/change address/ndrsla.
12.	الشفافية: سجل أحداث order_events إلزامي لكل انتقال حالة.
4) تغييرات المخطط (DDL المعياري – مختصر)
●	orders
id (PK), order_number (UNIQUE), user_id|null, anonymized_customer_id|null,
state_id, sub_state_id|null,
placed_at, confirmed_at, allocated_at, packed_at, shipped_at, delivered_at, closed_at, cancelled_at,
مبالغ: subtotal, shipping, tax, discount_total, grand_total, currency, fx_rate,
أعلام: is_cod, is_preorder, is_backorder,
مراجع: shipping_profile_id, payment_profile_id.
فهارس: (state_id), (placed_at), (confirmed_at), (shipped_at).
●	order_items
order_id (FK), sku_id, qty_ordered, qty_allocated, qty_shipped, qty_cancelled,
أسعار لقطة: unit_price, unit_discount, unit_tax.
فهارس: (order_id), (sku_id).
●	order_addresses (Snapshot)
order_id, type ('shipping'/'billing'), name, phone_masked, city, region, country, address_lines (masked).
●	order_payments
order_id, payment_method, provider_txn_id, amount, status, captured_at|refunded_at, wallet_ledger_id|null.
●	order_adjustments
order_id, type (coupon/promo/shipping_diff/price_adjust), amount (+/-), reason, actor.
●	order_events
order_id, event_type, payload(JSON), created_at, actor.
●	shipments / shipment_items (منفصلة)
تربط بـ order_id مع carrier, tracking_no, state.
●	ndr / rto
جداول لحالات فشل التسليم والعودة للمرسل مع سبب/قرار.
●	reservations / inventory_ledger
كما اعتمدتم سابقًا: reservation TTL، ledger لحركات allocate/ship/release/return.
ملاحظة: كل حالات/أنواع تُدار عبر lookup tables + FKs (لا ENUM)، وفهارس زمنية للحالة.
 
5) عقود الـAPI (مختصرة)
●	POST /orders (create draft/placed) — به Idempotency-Key.
●	POST /orders/{id}/confirm — يجمّد الأسعار/العناوين ويبدأ allocate.
●	POST /orders/{id}/cancel — إلغاء ذكي حسب الحالة.
●	POST /orders/{id}/address/change — ضمن نافذة محددة قبل packed.
●	POST /orders/{id}/split — تكوين shipment جزئي.
●	POST /orders/{id}/merge-for-shipping — دمج شحني (لنفس العميل/العنوان/الإطار الزمني).
●	POST /orders/{id}/ndr — تسجيل فشل تسليم مع قرار (إعادة شحن/استرداد).
●	POST /orders/{id}/rto — معالجة عودة للمرسل.
●	POST /orders/{id}/price-adjust — تعديل بعد الشراء بسياسة محكومة.
●	Webhook/Events: order_confirmed/shipped/delivered/cancelled/ndr/rto.
 
6) نوافذ وسياسات التشغيل
6.1 الإلغاء الذكي (Smart Cancel)
●	قبل confirmed: إلغاء فوري → release reservation + عكس أي حجز دفع.
●	بين confirmed وpacked: إلغاء إن لم يبدأ الالتقاط (picking)؛ إن بدأ: إلغاء جزئي حسب items المتاحة.
●	بعد shipped: لا إلغاء؛ يتحول إلى NDR/RTO/RMA.
●	Preorder/Backorder: مسموح حتى X أيام قبل ETA.
6.2 تغيير العنوان
●	مسموح حتى قبل packed؛ بعد ذلك عبر مركز الشحن (إن أمكن) مع فرق كلفة في order_adjustments.
6.3 Split Shipment
●	إذا كانت بعض العناصر جاهزة: يُنشأ shipment جزئي؛ يظل الطلب مفتوحًا للباقي.
6.4 NDR (لم يتم التسليم) / RTO (عاد للمرسل)
●	NDR: تسجيل السبب (لا يجيب، عنوان خاطئ…)، قرار آلي وفق قواعد: إعادة محاولة/تأكيد عنوان/تحويل لـ RTO.
●	RTO: عند العودة، استرجاع للعميل (أصل الدفع أو محفظة) بعد فحص الحالة، وإرجاع المخزون إلى ledger بالسبب المناسب.
6.5 COD
●	محاولات تسليم محدودة (n محاولات). تكرار فشل → قائمة مراقبة/حجب COD لفترة.
●	تسوية السائق/الناقل ترتبط بـ cod_settlements (موجودة في سياساتكم).
6.6 تعديل السعر بعد الشراء
●	نافذة محدودة (مثلاً 72 ساعة) مع حدود قصوى وعدالة (لا تُخالف العروض). تُسجّل في order_adjustments.
 
7) المخزون والدفاتر (Rules)
●	Cart → Reservation (TTL)
●	Confirm → Allocate (تعبئة qty_allocated)
●	Pack/Ship → Ledger: ship (خصم فعلي)
●	Cancel → Ledger: release
●	RTO/Return → Ledger: return_to_stock/damaged حسب الحالة.
8) الاتصالات والتحليلات
●	إشعارات: order_confirmed, order_shipped (مع تتبع), out_for_delivery, delivered, ndr_prompt, rto_refund_issued.
●	Analytics Events: order_created/confirmed/fulfilled/cancelled/ndr/rto/split/price_adjust مع خصائص (latency_ms, reason, cod, preorder).
9) المراقبة وSLO/KPI
●	SLOs:
○	p95 confirm→allocate ≤ 2m، packed SLA ≤ 12h، ship→deliver حسب شركة الشحن.
○	أخطاء API الحرجة < 0.1%.
●	KPIs:
○	Cancel rate قبل الشحن، NDR rate، RTO rate، On-time delivery %، Split ratio، Avg lead time، COD failure rate، Refund TAT.
●	تنبيهات: ارتفاع NDR/RTO فوق العتبة، تأخر تحديث المخزون، انحراف p95.
10) اختبارات Day-0 (على Staging)
1.	Confirm→Allocate→Pack→Ship→Deliver (مسار سعيد) مع تطابق ledger.
2.	Cancel قبل و/أو بعد confirm (تحقق release/partial cancel).
3.	Split Shipment لعنصرين (واحد جاهز/واحد متأخر).
4.	NDR→RTO مع استرداد وقيود ledger المناسبة.
5.	COD فشل مرتين → إدراج في قائمة المراقبة.
6.	Address Change قبل packed ينعكس على الشحنة.
7.	Price Adjust يظهر في adjustments ويؤثر على الإجمالي بدقة.
DoD: كل السيناريوهات Pass، وتقرير CI يضم: حالات قبل/بعد، أرقام ledger، زمنيات SLO.
11) تعريف 
●	حالات الطلب تعمل نهاية إلى نهاية مع سجل أحداث كامل.
●	الحجز/التخصيص/الخصم/الإرجاع في ledger صحّتهم مؤكدة.
●	الانعكاس على الدفع/المحفظة/الشحن يتم تلقائيًا حسب الحالة.
●	SLO/KPI قيد المراقبة مع تنبيهات فعّالة.
12) الملكية والحَوْكمة
●	DRI: فريق العمليات/المنصّة.
●	Runbooks: إلغاء ذكي، NDR/RTO، Split، تغيير عنوان، تسوية COD.
●	مراجعة ربع سنوية: ضبط النوافذ الزمنية، عتبات NDR/RTO، قواعد COD، وأسعار الشحن.
 
سياسة إدارة طلبات المرتجعات والاستبدال (RMA) 
سياسة إدارة طلبات المرتجعات والاستبدال (RMA)
●	المبدأ: معالجة مرتجعات/استبدالات بعدالة وسرعة، مع فصل واضح بين الطلب والشحنة والدفع، وربط محكم بالمخزون عبر inventory_ledger وQC.
●	الاعتماديات: DB (MySQL)، الدفع/المحفظة (يشمل COD)، الشحن والتتبّع، PIM/Inventory، Notifications، Analytics، CI/CD، Monitoring.
 
1) نطاق السياسة
تنطبق على: rmas, rma_items, rma_events, returns, exchanges, order_items, shipments, inventory_ledger, wallet_ledger, coupons/loyalty.
2) قرارات معمارية (ADR مختصرة)
1.	فصل المفاهيم: RMA ككيان مستقل؛ لا تعدّل الطلب الأصلي مباشرة.
2.	حالات RMA (lookup لا ENUM): requested, approved, in_transit_to_dc, received_qc, approved_refund, approved_exchange, rejected, refunded, exchanged, closed.
3.	Snapshots ثابتة: أسعار/ضرائب/خصومات تُلتقط لحظة إنشاء RMA لضمان دقة الحسابات.
4.	المخزون: كل مرتجع يمر عبر QC؛ المقبول الجاهز للبيع → return_to_stock، التالف → damaged/scrap.
5.	الاستبدال: شحنة بديلة بعد استلام/قبول المرتجع، أو Cross-Ship بشروط (مذكورة أدناه).
6.	الماليات: الحسابات Pro-Rata (بنود/كوبونات/شحن) + تسوية الولاء/الكوبونات + أولوية ردّ الأموال على وسيلة الدفع الأصلية ثم المحفظة.
7.	Idempotency & Audit: لكل عمليات الكتابة؛ سجل أحداث إلزامي.
8.	إطارات زمنية قابلة للتهيئة: نوافذ طلب RMA، مهلة شحن المرتجع، سقوف الاسترداد، إلخ.
3) شروط الأهلية وقبول RMA
●	نافذة الطلب: خلال X يومًا من الاستلام (قابلة للتهيئة؛ اقترح 7–14).
●	الحالة: غير مُستخدَم/بقِطعِه وملحقاته وملصقاته.
●	ممنوعات لأسباب صحية: الملابس الداخلية/الجوارب/مستحضرات التجميل المفتوحة (إلا عيب مصنعي موثّق).
●	أدلة: صور/فيديو عند الطلب وسبب واضح (مقاس/عيب/وصف مختلف…).
●	الاستثناءات: العيب المصنعي خارج النافذة الزمنية يُقبل ضمن ضمان الصنع إن وُجد.
4) تغييرات المخطط (DDL مختصر)
●	rmas
id, order_id, user_id|null, anonymized_customer_id|null, state_id, reason_id, created_at, approved_at, received_at, closed_at, resolution ('refund'|'exchange'), notes.
●	rma_items
rma_id, order_item_id, sku_id, qty, item_condition_id ('new','opened','defective','wrong_item'), qc_result_id ('pass','repair','reject'), refund_amount, restock_fee_amount.
●	rma_events
rma_id, event_type, payload(JSON), created_at, actor.
●	returns (شحنة المرتجع)
rma_id, carrier, tracking_no, state_id, label_issued_at, expected_by, received_at.
●	exchanges (البديل)
rma_id, new_sku_id, qty, shipment_id|null, cross_ship(bool), deposit_wallet_ledger_id|null.
●	lookup tables: lk_rma_state, lk_rma_reason, lk_item_condition, lk_qc_result.
●	فهارس أساسية: على state_id, created_at, received_at, وorder_id.
Inventory Ledger: أسباب حركات: rma_return_to_stock, rma_damaged, rma_missing_parts, rma_scrap, exchange_out.
5) عقود الـAPI (مختصر)
●	POST /rma إنشاء RMA (سلة بنود + سبب + صور).
●	POST /rma/{id}/approve / .../reject.
●	POST /rma/{id}/label إصدار ملصق شحن مرتجع (إن متاح).
●	POST /rma/{id}/receive استلام المرتجع وتسجيل QC.
●	POST /rma/{id}/resolve/refund حساب/تنفيذ الاسترداد.
●	POST /rma/{id}/resolve/exchange إنشاء/إرسال البديل.
●	Webhooks/Events: rma_approved/received/qc_pass/qc_fail/refunded/exchanged/rejected/closed.
6) التدفق التنفيذي (مختصر)
1.	طلب RMA: التحقق من الأهلية + إنشاء بنود + التقاط Snapshot الأسعار/الخصومات.
2.	الموافقة وإصدار الملصق (اختياري): حالة approved مع مهلة شحن المرتجع Y يومًا.
3.	الشحن إلى مركز الإرجاع: حالة in_transit_to_dc.
4.	الاستلام وQC: حالة received_qc → لكل بند: qc_result.
5.	قرار:
○	Refund: approved_refund → احتساب استرداد (Pro-Rata) → تنفيذ ردّ الأموال → refunded.
○	Exchange: approved_exchange → تحضير البديل → شحن → exchanged.
○	Reject: لعدم الأهلية/استخدام/ضرر غير مصنعي → إخطار العميل بخيارات (إرجاع على حسابه/إتلاف).
6.	إغلاق: closed بعد اكتمال الماليات/المخزون وإشعارات العميل.
7) قواعد الحساب المالي (مختصر ودقيق)
●	Pro-Rata للخصومات/الكوبونات: توزيع الخصم الإجمالي على البنود حسب قيمة السطر، واسترداد الجزء الموافق للبنود المرتجعة فقط.
●	الشحن:
○	خطأ منّا/عيب مصنعي: ردّ الشحن ذهابًا وإيابًا.
○	تغيير رأي/مقاس: ردّ قيمة السلعة فقط (يمكن خصم الشحن/ملصق المرتجع).
●	COD: الاسترداد إلى المحفظة افتراضيًا؛ بديل تحويل بنكي خلال ≤ Z يومًا.
●	رسوم إعادة التخزين (Restock): % ثابت أو حدّ مقطوع للبنود غير المعيبة (اختياري)، لا تُطبَّق على العيوب.
●	الولاء/القسائم: خصم النقاط/القسائم التي كُسبت من البنود المرتجعة، وإرجاع القسائم المستخدمة وفق شروطها (متاحة/منتهية).
●	الأولوية: نفس وسيلة الدفع → المحفظة → تحويل بنكي.
8) الاستبدال (Exchange)
●	عادي: شحن البديل بعد received_qc (قبول).
●	Cross-Ship (اختياري): شحن البديل قبل الاستلام مقابل تأمين (حجز بطاقة/إيداع محفظة)، وإلا يُحوّل إلى RMA قياسي.
●	فرق السعر: تحصيل/ردّ الفرق عبر order_adjustments.
9) المخزون والدفاتر (Rules)
●	QC Pass: زيادة إلى stock_available عبر ledger: rma_return_to_stock.
●	QC Fail – Damaged: ledger: rma_damaged (مستودع تالِف/سكراب).
●	Missing Parts: ledger: rma_missing_parts + إمكانية خصم restock_fee.
●	Exchange Out: خصم من المخزون البديل ledger: exchange_out.
●	RTO ↔ RMA: إن عاد الطلب للمرسل ثم طلب RMA، تُحسب كـRMA جديدة على البنود المُستلمة.
10) نوافذ وسياسات التشغيل
●	طلب RMA: خلال X يومًا من الاستلام.
●	إرسال المرتجع بعد الموافقة: خلال Y يومًا، وإلا تُغلق تلقائيًا.
●	TAT المعالجة بعد الاستلام: ≤ 2 يوم عمل لـQC، ≤ 5 أيام للاسترداد البنكي.
●	Cross-Ship: مسموح لفئات محدّدة وبحد أقصى N وحدات.
11) مكافحة إساءة الاستخدام
●	كشف نمط High RMA Rate، Wardrobing (استخدام ثم إرجاع)، Size-cycling؛ تطبيق:
○	تقليل حقوق الاسترجاع، أو طلب رسوم شحن/إيداع مسبق، أو حجب COD مؤقتًا.
●	قائمة مراقبة + مراجعة بشرية للحالات الحدّية.
12) الاتصالات والتحليلات
●	إشعارات: rma_approved, label_issued, rma_received_qc, refund_issued, exchange_shipped/ delivered, rma_rejected.
●	Analytics Events: rma_requested/approved/received/refunded/exchanged/rejected بخصائص (reason, items, latency_ms, refund_amount).
13) المراقبة وSLO/KPI
●	SLOs: p95 استلام→QC ≤ 48h، p95 QC→Refund ≤ 24h، أخطاء API < 0.1%.
●	KPIs: RMA rate%، Refund TAT، QC pass%، Resale lead time للمرتجعات المقبولة، Shrinkage% (تالف/مفقود)، Cross-Ship failure%.
●	تنبيهات: ارتفاع RMA rate فوق العتبة، تأخّر الاسترداد، تزايد damaged%.
14) اختبارات Day-0 (Staging)
1.	RMA Refund: بندان مع كوبون مشترك → استرداد Pro-Rata + تحديث الولاء.
2.	RMA Exchange: استبدال مقاس لنفس SKU → خصم/تحصيل فرق إن وُجد.
3.	QC Pass/Fail: بند يمرّ/يفشل → ledger صحيح، ورسوم restock على غير المعيب فقط.
4.	COD Refund: استرداد لمحفظة ثم تحويل بنكي.
5.	Cross-Ship: حجز تأمين، ثم استلام المرتجع؛ في حالة عدم وصول المرتجع خلال المهلة تُحوَّل العملية إلى بيع نهائي.
6.	Reject: بند مستخدم/بدون ملصقات → رفض مُعلّل وخيارات عميل.
15) تعريف 
●	حالات RMA تعمل من الطلب إلى الإغلاق مع audit trail.
●	الحساب المالي/Pro-Rata والولاء/الكوبونات يتطابقان مع الإجماليات.
●	تحديثات inventory_ledger دقيقة لكل نتيجة QC.
●	SLO/KPI قيد المراقبة والتنبيهات مفعّلة.
16) الملكية والحَوْكمة
●	DRI: فريق العمليات/المنصّة.
●	Runbooks: سيناريوهات (Refund/Exchange/Cross-Ship/Reject).
●	مراجعة ربع سنوية: ضبط النوافذ، سياسات الرسوم، عتبات إساءة الاستخدام، وفئات Cross-Ship.
 
سياسة المحفظة (Wallet Policy) 
سياسة المحفظة (Wallet Policy)
●	المبدأ: المحفظة مصدر رصيد آمن وشفاف للعميل، تُدار عبر دفتر قيود Append-Only (wallet_ledger) مع حجز مبالغ (holds) وتسويات صرف (payouts).
●	الاعتماديات: DB (MySQL)، بوابة الدفع، COD، الشحن/RMA، الطلبات، الإشعارات، التحليلات، CI/CD، المراقبة.
 
1) النطاق (Scope – DB)
●	wallet_accounts, wallet_ledger, wallet_holds, wallet_payouts (+ جداول lookup للأسباب/الحالات/الوسائل).
●	الربط مع: orders / rmas / cod_settlements / payment_disputes / audit_log.
 
2) قرارات معمارية (ADR مختصرة)
1.	مصدر الحقيقة = wallet_ledger فقط (Append-Only). يمكن استخدام balance_cached كـ Snapshot يُعاد التحقق منه دوريًا.
2.	Idempotency إلزامي لكل Credit/Debit/Hold/Capture/Payout (مفتاح فريد لكل عملية خارجية).
3.	العملة: حقل currency وfx_rate على مستوى القيد؛ افتراضيًا عملة واحدة، مع دعم متعدّد عند الحاجة.
4.	الرصيد السالب: ممنوع افتراضيًا؛ يُسمح فقط بسيناريوهات Chargeback/Fees مع علم واضح allow_negative=false (إلا إن فُعّل صراحة).
5.	الأولوية في الاسترداد:
○	مدفوعات مسبقة: إلى وسيلة الدفع الأصلية، وإن تعذّر ⇒ المحفظة.
○	COD: إلى المحفظة افتراضيًا، مع خيار تحويل بنكي لاحق.
6.	تمييز الأموال: نقد/مكافآت: أرصدة ترويجية Expirable تُسجَّل بأسباب مميّزة وتنتهي تلقائيًا (TTL).
7.	حجز/تجميد (Holds): عند الحاجة (Cross-Ship/تحقق)، تُحوَّل إلى Capture (Debit) أو Release تلقائيًا مع TTL.
8.	التسوية والصرف (Payouts): تُخصم من المحفظة كـ Debit مع سجل حالة (requested→processing→succeeded|failed) ومطابقة بنكية.
9.	الامتثال والأمان: حدود يومية/شهرية، فحوص سرعات/أجهزة، متطلبات KYC للصرف.
 
3) تغييرات المخطط (DDL مختصر)
●	wallet_accounts
id (PK), user_id|null, anonymized_customer_id|null, status ENUM('active','frozen','closed'),
currency, balance_cached DECIMAL(18,2), allow_negative BOOL DEFAULT 0,
طوابع: created_at, updated_at, closed_at.
فهارس: (user_id), (anonymized_customer_id), (status).
●	wallet_ledger (Append-Only)
id, wallet_id (FK), entry_type ('credit'|'debit'), reason_id (FK lookup),
amount DECIMAL(18,2), currency, fx_rate DECIMAL(12,6),
related_type (order|rma|payout|settlement|dispute|adjustment), related_id,
idempotency_key UNIQUE, actor ('system'|'user'|'admin'), created_at.
فهارس: (wallet_id,created_at), (idempotency_key), (related_type,related_id).
●	wallet_holds
id, wallet_id, amount, reason_id, created_at, expires_at,
captured_at|null, released_at|null, related_type, related_id, idempotency_key UNIQUE.
فهارس: (wallet_id), (expires_at), (captured_at).
●	wallet_payouts
id, wallet_id, method_id (bank|mobile_money|voucher), amount, fee_amount,
status_id (requested|processing|succeeded|failed|reversed),
requested_at, processed_at|null, provider_ref|null, failure_reason|null, idempotency_key UNIQUE.
فهارس: (wallet_id,status_id), (requested_at).
●	lookups: lk_wallet_reason, lk_payout_method, lk_payout_status.
●	audit_log: يسجّل كل عمليات الائتمان/الخصم/الحجز/الصرف والتراجع.
قاعدة: لا UPDATE/DELETE على ledger؛ أي تصحيح يتم بقيد عكسي (Reverse Entry).
 
4) القواعد (Invariants)
●	I-1: مجموع Credits − Debits − Captured Holds = رصيد المحفظة (≈ balance_cached مع إعادة مزامنة).
●	I-2: لا قيود Debit تُسمح إن كان الناتج < 0 (إلا إذا allow_negative=1 والسبب ضمن قائمة مسموحة).
●	I-3: idempotency_key فريد عالميًا لكل عملية خارجية (منع التكرار).
●	I-4: لا Close لمحفظة ورصيدها ≠ 0.
●	I-5: لا Erase Account قبل قيد wallet_closure ورصيد = 0 (متكاملة مع سياسة الحذف).
 
5) التدفقات التشغيلية (Flows)
●	Top-Up (Credit): via بوابة الدفع ⇒ قيد credit:topup بـ idempotency + تحديث balance_cached.
●	Refund In (Credit): من RMA/Order ⇒ credit:refund مع related_type='rma'|'order'.
●	Purchase/Adjustment (Debit): debit:purchase أو debit:adjustment.
●	Holds: إنشاء Hold (TTL) ⇒ لاحقًا Capture (يُنشئ Debit + يغلق الـHold) أو Release عند الإلغاء/الانتهاء.
●	Promotions/Rewards (Credit Expirable): credit:promo مع expires_at; Job يُنشئ debit:promo_expire عند الانتهاء.
●	Payout (Withdrawal): إنشاء سجل في wallet_payouts (requested) + قيد debit:payout؛ عند فشل المزود ⇒ credit:payout_reversal.
●	Chargeback/Dispute (Debit): عند خسارة نزاع دفع ⇒ debit:chargeback وقد ينتج رصيد سالب + تجميد محفظة.
●	COD Refund: إلى المحفظة افتراضيًا؛ طلب تحويل بنكي يخصم debit:payout عند التنفيذ.
 
6) واجهات الـAPI (عقود مختصرة)
●	POST /wallet/topup (idempotent)
●	POST /wallet/refund (من RMA/Order)
●	POST /wallet/hold → POST /wallet/hold/{id}/capture | /release
●	POST /wallet/payout → متابعة /wallet/payout/{id} (status)
●	GET /wallet/ledger (ترشيح حسب التاريخ/النوع)
كل العمليات تتطلب Idempotency-Key وتمر بمعاملة مع SELECT … FOR UPDATE على صف المحفظة لمنع السباق.
 
7) المخاطر والضوابط (Risk & Controls)
●	حدود يومية/شهرية لـ Top-Up/Payout/Refund-In.
●	كشف سرعة/أجهزة: حد لعدد العمليات/جهاز/ساعة؛ ربط بـ device_hash.
●	KYC/AML للصرف: وثائق مطلوبة للمبالغ الكبيرة؛ قوائم حظر.
●	تجميد المحفظة عند رصيد سالب لفترة أو نمط احتيالي.
 
8) المراقبة والمؤشرات (SLO/KPIs)
●	SLOs: p95 تنفيذ عمليات المحفظة ≤ 200ms، p95 معالجة Payout ≤ 2 يوم عمل.
●	KPIs: رصيد مطلوب (Wallet Liability)، Refund TAT، Payout Success%، Dispute Rate، نسبة Expired Promo%، تبنّي المحفظة % من الاستردادات.
 
9) اختبارات Day-0 (Staging)
1.	Idempotency: إرسال Top-Up مكرر بنفس المفتاح ⇒ قيد واحد فقط.
2.	Concurrency: عمليتا Capture متزامنتان على نفس الـHold ⇒ واحدة فقط تنجح.
3.	Refund→Payout: ردّ RMA إلى المحفظة ثم طلب Payout؛ عند فشل المزود تُسجَّل credit:payout_reversal.
4.	Promo Expiry: إنشاء credit:promo مع TTL قصير ⇒ ينشأ debit:promo_expire تلقائيًا.
5.	Negative Guard: Debit يجعل الرصيد سالبًا ⇒ يُرفض إلا مع allow_negative=1 وسبب مسموح.
6.	Erase/Close Gate: محاولة إغلاق/حذف مع رصيد ≠ 0 ⇒ مرفوضة.
DoD: كل السيناريوهات Pass، وتقرير CI يحوي: صحة الرصيد، عدم وجود ازدواج، أزمنة التنفيذ.
 
10) تعريف (Definition of Done)
●	المخطط (DDL) والجداول المرجعية والقيود مُطبّقة، وledger يعمل Append-Only.
●	عمليات API idempotent، وقفل تنافسي صحيح، وتنبيهات مراقبة مفعّلة.
●	ربط كامل مع الطلبات/RMA/COD/Disputes، وسياسة الحذف (Closure قبل Erase).
●	تقارير الـAnalytics تعكس أحداث المحفظة خلال ≤ 5 دقائق.
 
11) حالات الحافة (Edge Cases)
●	دمج حسابات: نقل محفظة المصدر إلى الهدف (wallet_merge قيد توضيحي).
●	تجميد الحساب/Legal Hold: منع Payout/Erase؛ يسمح Refund-In فقط.
●	تغيّر العملة: تُحفظ القيم بالعملة الأصلية + fx_rate; التقارير توحّد عبر تحويل تحليلي.
●	انقطاع مزود الدفع: Queue داخلي وإعادة محاولة مع Backoff وتتبّع idempotency_key.
 
12) الملكية والحَوْكمة
●	DRI: فريق المنصّة/المالية.
●	Runbooks: Top-Up Failures، Payout Reconciliation، Chargeback، Promo Expiry، Wallet Merge/Closure.
●	مراجعة ربع سنوية: حدود/سياسات المخاطر، رسوم الصرف، مدد Expiry.
 
سياسة التحليلات والإحصائيات (Analytics ) 
سياسة التحليلات والإحصائيات (Analytics & Statistics Policy)
●	المبدأ: سلوك المستخدم يُقاس عبر أحداث مُوحّدة وقابلة للتدقيق، مع فصلٍ واضح بين “مصدر الحقيقة المالي” (الـDB) و”تحليلات السلوك” (الحدث/الجلسات).
●	الاعتماديات: DB (MySQL)، SDKs (Firebase/GA4/Web), Server-side Events، BigQuery (Raw/Staging/Marts)، ETL/ELT، Consent/DSAR، CI/CD، Monitoring.
 
1) النطاق (Scope – Data/DB)
●	جمع الأحداث: التطبيق (Firebase), الويب (GA4/gtag), الخادم (server-events).
●	المستودع التحليلي: BigQuery (أو بديله) بثلاث طبقات: raw_*، clean_*، marts_*.
●	جداول الربط مع الـDB: user_identity_map, product_dim, order_fact, rma_fact, wallet_fact, marketing_dim (UTM).
●	حوكمة الخصوصية: consent_logs, dnt_flags, deletion_queue (طلبات erase).
 
2) قرارات معمارية (ADR مختصرة)
1.	مصدر الحقيقة للإيراد/الطلبات = DB (order_fact/wallet_fact). التحليلات لقياس السلوك/القمع (funnels).
2.	هوية موحّدة: استخدام user_id أينما أمكن + ربط user_pseudo_id المجهول عبر user_identity_map (anonymous→known).
3.	Taxonomy للأحداث: قاموس أحداث مُوحّد (أسماء/حقول إلزامية)، لا أحداث خارج القائمة.
4.	Idempotency & De-dup: كل حدث يحمل event_id (ULID)؛ تُزال الازدواجات في clean_*.
5.	الطابع الزمني: الاعتماد على server_timestamp، وتخزين client_timestamp للمعلومة فقط؛ المنطقة الزمنية UTC.
6.	تقسيم/عنقدة (DW): التقسيم بالـdate، العنقدة حسب (event_name, user_pseudo_id, source).
7.	الامتثال: عدم إرسال PII (بريد/هاتف) في الأحداث؛ يُسمح بـ hash مُملّح داخليًا فقط عند الضرورة.
8.	الهوية التسويقية: UTM موحَّدة (lowercase/normalized)، نماذج Attribution محددة (First/Last touch).
 
3) مخطط البيانات (DDL مختصر – Data Warehouse)
صِف المخطط داخل المستند؛ التنفيذ الفعلي في الـDW.
●	raw_events_app / raw_events_web
event_id, event_name, client_ts, server_ts, event_date, user_pseudo_id, device_id, session_id, user_id_nullable, source(app/web), params(JSON)
Partition: event_date — Cluster: (event_name, user_pseudo_id)
●	clean_events
نفس الحقول + is_duplicate, is_bot, schema_valid. تُفلتر الازدواج/الروبوت.
●	sessions
session_id, user_pseudo_id, user_id_nullable, source, start_ts, end_ts, session_duration, screen_views, bounces_flag
●	user_identity_map
user_pseudo_id, user_id, first_seen_ts, last_seen_ts, link_reason (login/purchase/sdk)
●	marketing_dim (utm)
utm_source, utm_medium, utm_campaign, utm_content, utm_term, normalized_flags, first_touch_ts, last_touch_ts, attribution_window_days
●	order_fact / rma_fact / wallet_fact (مأخوذة من الـDB عبر ELT)
مفاتيح الربط: user_id, order_id, … + مبالغ/حالات مع طوابع زمنية.
●	funnels_mart
يومي/أسبوعي: خطوات القمع (view_item → add_to_cart → begin_checkout → add_payment → purchase).
●	kpi_daily
date, users_active, sessions, cvrs, aov, revenue_db, revenue_events, delta_revenue_pct, cac, roas, ndr_rate, rto_rate
●	consent_logs / dnt_flags / deletion_queue
لتطبيق القبول/عدم التتبع وطلبات المحو على المسارات التحليلية.
 
4) قاموس الأحداث (Taxonomy مختصر)
أحداث أساسية (أمثلة وحقول إلزامية):
●	app_open (app_version, os, locale)
●	view_item (sku_id, price, currency)
●	add_to_cart (sku_id, qty, price)
●	begin_checkout (cart_value, items_count)
●	add_payment_info (method_type)
●	purchase (order_id, value, currency, items[]) — يجب إرسالها server-side أيضًا.
●	بعد الشراء: rma_requested/refunded, ndr/rto, wallet_credit/debit, coupon_applied/failed
قاعدة: أي حدث جديد يتطلب تحديث القاموس + اختبار Day-0 قبل الإرسال للإنتاج.
 
5) القواعد (Invariants)
●	I-1: event_id فريد عالميًا في clean_events.
●	I-2: لا PII في params؛ المسموح فقط معرفات داخلية/Hashات غير قابلة للعكس.
●	I-3: purchase.value في الأحداث ≈ إيراد الـDB لنفس الفترة مع إنحراف ≤ 3% (يُفسَّر بالضرائب/الخصومات/الوقت).
●	I-4: كل purchase server-side يولِّد حدثًا مطابقًا client-side أو يُوسم source='server'.
●	I-5: جلسة واحدة لا تتجاوز 30 دقيقة عدم نشاط (sessionization ثابت).
 
6) Attribution (اختصار واضح)
●	First Touch (90d) + Last Non-Direct (7d).
●	تطبيع UTM (قائمة بيضاء للـmedium: cpc, social, email, affiliate, display, direct).
●	التنازع يُحل حسب “آخر لمسة” إن كانت ضمن النافذة؛ وإلا “أول لمسة”.
 
7) الخصوصية والامتثال
●	Consent Mode: لا تُجمع أحداث التسويق أو تُخفَّض الدقة دون موافقة.
●	DNT: عند تفعيل dnt_flags تُوقف الـSDKs وتُحذف هوية التحليلات (identity reset).
●	DSAR/Erase: حذف/إخفاء هوية التحليلات المرتبطة بـ user_id وuser_pseudo_id في clean_*، مع إبقاء المجاميع المجهولة.
●	Non-Prod Masking: عينات مُقنَّعة فقط لبيئات الاختبار.
 
8) جودة البيانات (DQ) والاختبارات
اختبارات يومية تلقائية:
●	Schema Conformance: جميع الأحداث تمرّ بـ JSON schema.
●	Volume Anomaly: إنخفاض/ارتفاع > 20% مقارنة بمتوسط 7 أيام.
●	Join Rates: معدل ربط view_item↔product_dim ≥ 99%، وpurchase↔order_fact ≥ 99.5%.
●	Dedup Ratio: نسبة الازدواج < 1%.
●	Revenue Delta: |revenue_events − revenue_db| / revenue_db ≤ 3%.
 
9) SLO/KPIs والمراقبة
●	SLO Latency: من جمع الحدث إلى توفره في clean_* ≤ 15 دقيقة، وفي marts_* ≤ 60 دقيقة.
●	KPIs: DAU/WAU/MAU، CVR per step، AOV، ROAS، CAC، Retention (D1/D7/D30)، NDR/RTO Rates، Funnel Drop-offs.
●	Alerts: تأخير خط الأنابيب > 30 دقيقة، delta الإيراد > 3%، Join Rate < 98.5%، تكلفة BigQuery خارجة عن الحد، فشل تحميل يومي.
 
10) التدفقات التشغيلية (ELT/Jobs مختصرة)
●	Ingest: Streaming إلى raw_* (idempotent).
●	Clean & Dedup: تحويل إلى clean_* مع قواعد إزالة الروبوت/الازدواج.
●	Sessionization: بناء sessions يوميًا + تحديث تزايدي.
●	Attribution Build: تحديث marketing_dim (first/last touch).
●	Marts: تجميع funnels_mart وkpi_daily.
●	DSAR/Erase: Job يطبّق الحذف على clean_* والخرائط الهووية.
●	Dead-Letter Queue: تخزين أي حدث فاشل المعالجة مع سبب، ومتابعة آلية.
 
11) واجهات/تكاملات (اختصار)
●	Server Events API: نهاية واحدة موحّدة لاستقبال أحداث الخادم (idempotent + توقيع).
●	Exports: لوحات/تقارير (Metabase/Looker) تعتمد جداول marts_*.
●	Row-Level Security: الوصول للمجاميع فقط لغير المصرّح لهم بالبيانات الخام.
 
12) اختبارات (على Staging)
1.	إطلاق سلسلة قمع كاملة (view→add_to_cart→checkout→purchase) ثم التحقق من:
○	وجود الأحداث في clean_* خلال ≤ 15 دقيقة.
○	بناء جلسة صحيحة وUTM منسّق.
○	purchase يرتبط بـ order_fact.
2.	حساب CVR/AOV في marts_* يساوي النتائج اليدوية لنفس الفترة.
3.	تشغيل DSAR لعميل اختباري: اختفاء الهوية من clean_* وبقاء kpi_daily كما هو.
4.	Revenue delta ≤ 3%.
DoD: كل الاختبارات Pass، وتنبيهات المراقبة خضراء، وتقارير الـKPIs تعرض أرقامًا متّسقة مع الـDB.
 
13) القالب المعياري للأحداث
●	الاسم: event_name
●	الهدف: …
●	الحقول الإلزامية: …
●	المصدر: app/web/server
●	الهوية: يتطلب user_id؟ (Y/N) — يحفظ user_pseudo_id دائمًا
●	الملاحظات: حظر PII، وحدود الطول، القيم المسموحة
●	مالِك الحدث (DRI): فريق ××
●	اختبار Day-0: …
 
14) الملكية والحَوْكمة
●	DRI: فريق البيانات/المنصّة.
●	مراجعة ربع سنوية: تحديث القاموس، ضبط نوافذ الـAttribution/Retention، مراجعة التكاليف.
●	CI Gates: منع نشر أحداث غير مُعرفة في القاموس، وفحوص schema قبل الإنتاج.
 
ملاحظات
●	عيّن user_id في SDK فور تسجيل الدخول (مع الاحتفاظ بـ user_pseudo_id).
●	أرسل purchase من الخادم كمرجعية، ويمكن تكراره من العميل مع سمة source.
●	دوّن جميع التعاريف/الصيغ (CVR, AOV, ROAS…) في docs/analytics/metrics.md لضمان اتساق التقارير.
 
علامة التبويب 45 
موجّه لبيئة MySQL/InnoDB مع تكامل BigQuery)
اسم النقطة	أين تُنفّذ	معايير التنفيذ	الهدف	ملاحظات
اختيار محرك التخزين	MySQL (InnoDB)	InnoDB افتراضي؛ تعطيل MyISAM؛ ضبط innodb_buffer_pool_size	اتساق ومعاملات وأداء	راقب IOPS
الترميز والترتيب	MySQL	utf8mb4 + utf8mb4_general_ci أو utf8mb4_ar_0900_ai_ci	دعم العربية/الإيموجي	ثبّت على مستوى DB/جدول
المنطقة الزمنية	DB + تطبيق	تخزين UTC؛ عرض حسب منطقة المستخدم	اتساق الزمن	أعمدة created_at/updated_at
تسمية الجداول/الأعمدة	مخطط DB	معيار snake_case؛ لاحقة _id للمفاتيح	توحيد القراءة	وثّق Glossary
مفاتيح أساسية	كل الجداول	مفاتيح بديلة INT/BIGINT أو UUID؛ لا مفاتيح مركبة للـ PK	بساطة الفهارس	استخدم AUTO INCREMENT بحذر
مفاتيح خارجية	الجداول العلائقية	FK مع ON UPDATE/DELETE (RESTRICT/SET NULL)	نزاهة مرجعية	تجنّب CASCADE الثقيل
التطبيع (3NF/BCNF)	تصميم المخطط	فصل الكيانات؛ إزالة التكرار	اتساق ومرونة	أساس قبل أي denorm
Denormalization موجّهة	جداول قراءة	أعمدة مشتقة؛ تحديث عبر Triggers/Jobs	تسريع القراءة	حدّد مصدر الحقيقة
أنواع البيانات الدقيقة	الأعمدة	DECIMAL للعملات؛ TINYINT لفلاغ؛ DATE/TIMESTAMP	دقة وأداء	تجنّب TEXT عند الإمكان
قيود وصلاحية	DB	NOT NULL, CHECK, UNIQUE	تقليل أخطاء الإدخال	CHECK متاح حديثًا
الفهارس	DB	فهارس مركّبة حسب الاستعلام؛ تغطية (covering)	تسريع القراءة	راقب write amplification
الفحص والتخطيط	Query Layer	EXPLAIN، خطط منفذة، ANALYZE TABLEدوريًا	كشف عنق الزجاجة	لوحة Slow Query
التقسيم Partitioning	جداول كبيرة	Range/Hash حسب التاريخ/المنطقة	إدارة الحجم والأداء	سياسة أرشفة
الشَطر Sharding (عند التوسع)	طبقة الخدمة	تقسيم حسب المستأجر/المنطقة؛ كتالوج توجيه	توسع أفقي	يتطلب طبقة توجيه
النسخ المتماثل	MySQL	Primary→Replicas للقراءة؛ تأخير مراقَب	تخفيف الضغط	GTID مفعّل
إعداد الـ binlog	MySQL	صيغة ROW؛ ضغط؛ دوران بسقف حجمي/زمني	دقة CDC/استرجاع	مساحة تخزين محسوبة
المعاملات والعزل	DB	ACID؛ مستوى العزل REPEATABLE READافتراضي	منع قراءات قذرة	قيّم READ COMMITTEDحسب الحمل
قفل السجلات والازدحام	DB	فهارس مناسبة لتقليل القفل؛ تقسيم عمليات التحديث	منع deadlocks	سجّل واكتشف الأنماط
سياسات الحذف	طبقة الخدمة/DB	Soft delete (deleted_at) للكيانات الحرجة؛ Hard للـ logs	استرجاع/امتثال	فهارس تتجاهل المحذوف
التسلسل/الإصدار	جداول حساسة	Versioning/ETag للأغراض التنافسية	اتساق متفائل	يحل نزاعات التعديل
Triggers بحذر	DB	للسلامة البسيطة فقط؛ لا منطق أعمال معقّد	وضوح السلوك	وثّق سلسلة التأثير
Procedures/Functions	DB	محدودة؛ فضّل منطق التطبيق/الخدمات	قابلية الصيانة	استثناءات للأداء
الهجرة (Migrations)	CI/CD	ترقيم صارم؛ up/down؛ قفل أثناء الترحيل	تغييرات آمنة	تفكيك المهاجرات الكبيرة
بيانات الاختبار/Seed	بيئات غير إنتاج	Masking/توليد بيانات وهمية	خصوصية وواقعية	لا تُهرّب PII
الأمان على مستوى الشبكة	البنية	Private subnets؛ SG/NACL؛ لا وصول عام	تقليل السطح	bastion أو VPN فقط
المصادقة والوصول	DB/إدارة	مبدأ أقل امتياز؛ أدوار للقراءة/الكتابة/التقارير	تقليل المخاطر	مراجعة فصلية للصلاحيات
إدارة الأسرار	المنصة	مخزن أسرار؛ تدوير مفاتيح؛ منع تخزين الأسرار بالكود	حماية الاعتمادات	تنبيه قبل الانتهاء
التشفير	At-rest & In-transit	TDE/KMS للأقراص؛ TLS بين التطبيق وDB	حماية البيانات	تشفير أعمدة للحساس
سجلات التدقيق	جداول حساسة	Audit لا يعبث به؛ ختم سلامة	تتبع المسؤولية	تخزين منفصل/Retention
سياسات الاحتفاظ	جميع الجداول	مدد لكل نوع بيانات؛ purge دوري	امتثال وتقليل التكلفة	جدول عمليات تنظيف
جودة البيانات	طبقة البيانات	قواعد تحقق؛ تقارير اختلاف بين المشتق والأصل	صحة التحليلات	إنذارات عند الانحراف
CDC / التغييرات	Integration	Debezium/Maxwell لالتقاط التغييرات	تغذية DWH/ES	أقل كلفة من Pull
مستودع البيانات	BigQuery/DWH	Star/Snowflake؛ جداول حقائق/أبعاد؛ SCD	تحليلات مرنة	عقود مخطط (Data Contracts)
الجداول المادية/Rollups	DB/DWH	Materialized Views/جداول Rollup بزمن تحديث	تسريع التقارير	تحكّم بالـ staleness
فهرس بحث خارجي	Elasticsearch	Pipeline مزامنة؛ حقول denorm	بحث نصي سريع	لا تجعله مصدر حقيقة
الكاش	Redis/طبقة خدمة	مفاتيح واضحة + TTL؛ Invalidation مضبوط	خفض زمن الاستجابة	لا تفقد الاتساق
الاتصال والتجميع	تطبيق/DB	Connection pooling؛ حدود حدية؛ مهلات	استقرار تحت الحمل	مراقبة pool exhaustion
قياس الأداء	مراقبة	Slow query log، QPS، Latency P95/99	ضبط مستمر	لوحات ومؤشرات
النسخ الاحتياطي	DB/Storage	لقطات يومية/ساعية؛ تشفير؛ اختبار استرجاع	تعافي سريع	وثّق RTO/RPO
DR والتبديل	DNS/بنية	منطقة بديلة؛ است replic.؛ Runbook تمرين	استمرارية	تمارين فصلية
سياسات DSR/الخصوصية	طبقة البيانات	بحث/حذف/إخفاء بيانات العميل خلال SLA	امتثال وثقة	حذف من النسخ الاحتياطية
إدارة التكلفة	سحابة/DB/DWH	مراقبة تكلفة التخزين/الاستعلام؛ أرشفة باردة	خفض المصروف	قواعد إيقاف تسرب
تعدد المستأجرين	تصميم	per-tenant schema أو عمود tenant_id + فهارس	عزل منطقي	اختبارات تسريب
BLOB/Object Storage	خارج DB	الصور/الملفات إلى Object Storage؛ حفظ مفاتيح بالـDB	خفة الجداول	سياسة Lifecycle
الصيانة الدورية	DB	OPTIMIZE/ANALYZE; تحديث إحصاءات؛ ترقية مدروسة	أداء واستقرار	نافذة صيانة معلنة
توثيق المخطط	وثائق	ERD، ADR لقرارات المخطط، Glossary	وضوح واتساق	حدّثه مع كل تغيير
معايير الاستعلام	كود التطبيق	Queries قصيرة؛ Pagination؛ منع N+1	كفاءة وسرعة	استخدم ORM بحذر
حوكمة التغيير	عمليات	RFC/PRD صغير قبل تغييرات المخطط	تقليل المخاطر	مراجعة أمن/أداء مسبقة
قيود الأعمال في DB	DB	CHECK/UNIQUE/Triggers خفيفة	منع بيانات غير صالحة	لا تُبالغ لتتجنب التعقيد


