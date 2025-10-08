# ملحق ب: استراتيجية التخزين المؤقت | Appendix B: Cache Strategy
## أنماط Redis والأداء | Redis Patterns and Performance

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: استراتيجيات التخزين المؤقت باستخدام Redis  
**Purpose**: Caching strategies using Redis

**الجمهور**: مطورو الواجهة الخلفية، مهندسو الأداء  
**Audience**: Backend developers, performance engineers

---

## 🎯 **أنماط التخزين المؤقت | Caching Patterns**

### **1. Cache-Aside (الأكثر شيوعاً)**

```python
def get_product_cache_aside(variant_id):
    # القراءة من Cache
    cached = redis.get(f"variant:{variant_id}")
    if cached:
        return json.loads(cached)
    
    # القراءة من DB
    product = db.query("SELECT * FROM product_variants WHERE variant_id = %s", variant_id)
    
    # الكتابة للـ Cache
    redis.setex(f"variant:{variant_id}", 3600, json.dumps(product))
    
    return product
```

---

### **2. Write-Through**

```python
def update_product_write_through(variant_id, new_price):
    # 1. الكتابة للـ DB
    db.execute("UPDATE product_variants SET base_price = %s WHERE variant_id = %s", 
               new_price, variant_id)
    
    # 2. الكتابة للـ Cache فوراً
    product = db.query("SELECT * FROM product_variants WHERE variant_id = %s", variant_id)
    redis.setex(f"variant:{variant_id}", 3600, json.dumps(product))
```

---

### **3. Read-Through**

```python
def get_product_read_through(variant_id):
    # Redis يجلب تلقائياً من DB إذا مفقود
    # (يتطلب Redis Module أو Proxy)
    return redis_with_loader.get(f"variant:{variant_id}")
```

---

## 📊 **البيانات المُخزّنة مؤقتاً | Cached Data**

| النوع | المفتاح Key | TTL | الإبطال Invalidation |
|------|------------|-----|---------------------|
| **معلومات المنتج** | `variant:{id}` | 1 ساعة | عند التحديث |
| **قوائم المنتجات** | `list:category:{id}:page:{n}` | 15 دقيقة | عند تحديث أي منتج |
| **المخزون** | `stock:{id}` | 5 دقائق | عند الحجز/التحرير |
| **السلة** | `cart:{customer_id}` | 24 ساعة | عند التعديل |
| **الجلسة** | `session:{session_id}` | 30 دقيقة | عند النشاط |

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [12. خدمات التكامل | Integration Services](../12_Integration_Services.md)
- [05. الفهارس والأداء | Indexes & Performance](../05_Indexes_Performance.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08
