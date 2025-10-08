# 12. خدمات التكامل | Integration Services
## Redis، OpenSearch، وCDC | Redis, OpenSearch, and CDC

### 📋 **معلومات الوثيقة | Document Information**

**الهدف**: تحديد استراتيجيات التكامل مع الخدمات الخارجية  
**Purpose**: Define integration strategies with external services

**الجمهور**: مهندسو البنية التحتية، مطورو الواجهة الخلفية  
**Audience**: Infrastructure engineers, backend developers

**النطاق**: التخزين المؤقت، البحث، Change Data Capture  
**Scope**: Caching, search, change data capture

---

## 🎯 **نظرة عامة | Overview**

هذا المستند يحدد كيفية تكامل قاعدة بيانات MySQL مع خدمات خارجية لتحسين الأداء، البحث، والتحليلات.

**الخدمات المغطاة**:
- **Redis**: للتخزين المؤقت والجلسات
- **OpenSearch/Elasticsearch**: للبحث النصي
- **CDC**: لمزامنة البيانات مع مستودعات التحليلات

---

## 📑 **جدول المحتويات | Table of Contents**

1. [استراتيجية Redis | Redis Strategy](#redis-strategy)
2. [تكامل OpenSearch | OpenSearch Integration](#opensearch-integration)
3. [Change Data Capture (CDC) | CDC](#cdc)
4. [Message Queue | Message Queue](#message-queue)

---

## 1. استراتيجية Redis | Redis Strategy {#redis-strategy}

### **حالات الاستخدام | Use Cases**

#### **1. التخزين المؤقت للمنتجات | Product Caching**

```python
# Cache-Aside Pattern
def get_product(variant_id):
    # 1. محاولة القراءة من Redis
    cache_key = f"variant:{variant_id}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # 2. القراءة من قاعدة البيانات
    product = db.query("""
        SELECT v.*, p.name_ar, p.name_en, p.description_ar
        FROM product_variants v
        JOIN products p ON v.product_id = p.product_id
        WHERE v.variant_id = %s
    """, variant_id)
    
    # 3. التخزين في Redis (TTL: 1 ساعة)
    redis.setex(cache_key, 3600, json.dumps(product))
    
    return product
```

**إبطال الذاكرة المؤقتة | Cache Invalidation**:
```python
# عند تحديث المنتج
def update_product_price(variant_id, new_price):
    # 1. تحديث قاعدة البيانات
    db.execute("""
        UPDATE product_variants 
        SET base_price = %s, updated_at = NOW()
        WHERE variant_id = %s
    """, new_price, variant_id)
    
    # 2. إبطال الذاكرة المؤقتة
    redis.delete(f"variant:{variant_id}")
    redis.delete(f"product_list:category:*")  # قوائم الفئات
```

---

#### **2. المخزون في الوقت الفعلي | Real-time Inventory**

```python
# استخدام Redis للمخزون عالي التزامن
def check_availability(variant_id, requested_qty):
    cache_key = f"stock:{variant_id}"
    
    # القراءة من Redis
    available = redis.get(cache_key)
    
    if available is None:
        # تحميل من قاعدة البيانات
        available = db.query("""
            SELECT available_to_promise 
            FROM stock_snapshot 
            WHERE variant_id = %s
        """, variant_id)
        
        redis.setex(cache_key, 300, available)  # TTL: 5 دقائق
    
    return int(available) >= requested_qty

def reserve_inventory(variant_id, quantity, order_id):
    # 1. خصم ذري من Redis
    cache_key = f"stock:{variant_id}"
    new_stock = redis.decrby(cache_key, quantity)
    
    if new_stock < 0:
        # استعادة وفشل
        redis.incrby(cache_key, quantity)
        raise InsufficientStockError()
    
    # 2. تسجيل في قاعدة البيانات (async)
    queue.enqueue('inventory.reserve', {
        'variant_id': variant_id,
        'quantity': quantity,
        'order_id': order_id
    })
```

---

#### **3. الجلسات | Sessions**

```python
# تخزين جلسات المستخدم
def create_session(user_id):
    session_id = str(uuid.uuid4())
    session_data = {
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'last_activity': datetime.now().isoformat()
    }
    
    # تخزين في Redis (TTL: 30 دقيقة)
    redis.setex(
        f"session:{session_id}",
        1800,
        json.dumps(session_data)
    )
    
    return session_id
```

---

#### **4. Rate Limiting**

```python
def check_rate_limit(user_id, action, limit=100, window=3600):
    """
    حد معدل الطلبات: 100 طلب في الساعة
    """
    key = f"rate_limit:{action}:{user_id}"
    
    # زيادة العداد
    current = redis.incr(key)
    
    # تعيين انتهاء الصلاحية في المرة الأولى
    if current == 1:
        redis.expire(key, window)
    
    # التحقق من الحد
    if current > limit:
        raise RateLimitExceeded(f"تجاوز الحد: {current}/{limit}")
    
    return True
```

---

## 2. تكامل OpenSearch | OpenSearch Integration {#opensearch-integration}

### **مزامنة المنتجات | Product Sync**

#### **مخطط الفهرس | Index Schema**

```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "arabic_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "arabic_normalization", "arabic_stop"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "variant_id": { "type": "long" },
      "sku": { "type": "keyword" },
      "product_id": { "type": "long" },
      "name_ar": { 
        "type": "text", 
        "analyzer": "arabic_analyzer",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "name_en": { "type": "text" },
      "description_ar": { "type": "text", "analyzer": "arabic_analyzer" },
      "description_en": { "type": "text" },
      "brand_id": { "type": "long" },
      "brand_name": { "type": "keyword" },
      "category_id": { "type": "long" },
      "category_path": { "type": "keyword" },
      "base_price": { "type": "double" },
      "discounted_price": { "type": "double" },
      "is_available": { "type": "boolean" },
      "stock_status": { "type": "keyword" },
      "color": { "type": "keyword" },
      "size": { "type": "keyword" },
      "badges": { "type": "keyword" },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" }
    }
  }
}
```

---

#### **مزامنة البيانات | Data Sync**

```python
# مزامنة منتج إلى OpenSearch
def sync_product_to_opensearch(variant_id):
    # 1. جلب البيانات من MySQL
    data = db.query("""
        SELECT 
            v.variant_id,
            v.sku,
            v.product_id,
            p.name_ar,
            p.name_en,
            p.description_ar,
            p.description_en,
            b.brand_id,
            b.name_ar as brand_name,
            c.category_id,
            c.path as category_path,
            v.base_price,
            v.discounted_price,
            v.is_available,
            v.stock_status,
            av1.name_ar as color,
            av2.name_ar as size,
            p.badges,
            v.created_at,
            v.updated_at
        FROM product_variants v
        JOIN products p ON v.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN attribute_values av1 ON v.color_id = av1.value_id
        LEFT JOIN attribute_values av2 ON v.size_id = av2.value_id
        WHERE v.variant_id = %s
    """, variant_id)
    
    # 2. فهرسة في OpenSearch
    opensearch.index(
        index='products',
        id=variant_id,
        body=data
    )
```

---

#### **استعلام البحث | Search Query**

```python
def search_products(query, filters=None, page=1, size=20):
    """
    البحث في المنتجات مع فلاتر
    """
    must_clauses = []
    filter_clauses = []
    
    # البحث النصي
    if query:
        must_clauses.append({
            "multi_match": {
                "query": query,
                "fields": ["name_ar^3", "name_en^2", "description_ar", "description_en"],
                "type": "best_fields",
                "fuzziness": "AUTO"
            }
        })
    
    # الفلاتر
    if filters:
        if 'category_id' in filters:
            filter_clauses.append({"term": {"category_id": filters['category_id']}})
        
        if 'brand_id' in filters:
            filter_clauses.append({"term": {"brand_id": filters['brand_id']}})
        
        if 'price_min' in filters or 'price_max' in filters:
            price_range = {}
            if 'price_min' in filters:
                price_range['gte'] = filters['price_min']
            if 'price_max' in filters:
                price_range['lte'] = filters['price_max']
            filter_clauses.append({"range": {"base_price": price_range}})
    
    # الاستعلام النهائي
    search_body = {
        "query": {
            "bool": {
                "must": must_clauses if must_clauses else [{"match_all": {}}],
                "filter": filter_clauses + [{"term": {"is_available": True}}]
            }
        },
        "from": (page - 1) * size,
        "size": size,
        "sort": [{"_score": "desc"}, {"created_at": "desc"}]
    }
    
    return opensearch.search(index='products', body=search_body)
```

---

## 3. Change Data Capture (CDC) | CDC {#cdc}

### **استخدام Debezium | Using Debezium**

#### **تكوين Debezium | Debezium Configuration**

```json
{
  "name": "zahraah-mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql-primary",
    "database.port": "3306",
    "database.user": "debezium_user",
    "database.password": "${DEBEZIUM_PASSWORD}",
    "database.server.id": "1001",
    "database.server.name": "zahraah_db",
    
    "database.include.list": "zahraah_db",
    "table.include.list": "zahraah_db.orders,zahraah_db.order_items,zahraah_db.customers",
    
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "dbhistory.zahraah",
    
    "snapshot.mode": "initial",
    "snapshot.locking.mode": "minimal",
    
    "transforms": "route",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement": "$3"
  }
}
```

---

#### **معالجة أحداث CDC | CDC Event Processing**

```python
# استهلاك أحداث CDC وإرسالها لـ BigQuery
from kafka import KafkaConsumer
import json

def process_cdc_events():
    consumer = KafkaConsumer(
        'orders',
        'order_items',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        event = message.value
        
        if event['payload']['op'] == 'c':  # Create
            insert_to_bigquery(event['payload']['after'])
        
        elif event['payload']['op'] == 'u':  # Update
            update_in_bigquery(event['payload']['after'])
        
        elif event['payload']['op'] == 'd':  # Delete
            mark_deleted_in_bigquery(event['payload']['before'])
```

---

## 4. Message Queue | Message Queue {#message-queue}

### **RabbitMQ للعمليات غير المتزامنة | RabbitMQ for Async Operations**

```python
# إرسال حدث إلى قائمة الانتظار
def send_order_created_event(order_id):
    message = {
        'event_type': 'order.created',
        'order_id': order_id,
        'timestamp': datetime.now().isoformat()
    }
    
    channel.basic_publish(
        exchange='orders',
        routing_key='order.created',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # رسالة دائمة
            content_type='application/json'
        )
    )
```

---

## 🔗 **التنقل | Navigation**

[← السابق: 11. نظام المشتريات | Previous: Procurement System](11_Procurement_System.md)

[التالي: 13. الميزات المتقدمة | Next: Advanced Features →](13_Advanced_Features.md)

[🏠 العودة إلى فهرس قاعدة البيانات | Back to Database Index](index.md)

---

**إصدار الوثيقة | Document Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مكتمل وجاهز للإنتاج | Complete and Production-Ready
