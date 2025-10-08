# ملحق ج: تكامل البحث | Appendix C: Search Integration
## OpenSearch/Elasticsearch للبحث النصي | OpenSearch/Elasticsearch for Full-Text Search

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: دليل تكامل OpenSearch للبحث النصي  
**Purpose**: OpenSearch integration guide for full-text search

**الجمهور**: مطورو الواجهة الخلفية، مهندسو البحث  
**Audience**: Backend developers, search engineers

---

## 🎯 **نظرة عامة | Overview**

OpenSearch يوفر بحثاً نصياً قوياً مع دعم اللغة العربية، الفلاتر المتقدمة، والاقتراحات.

---

## 📊 **مخطط الفهرس | Index Schema**

### **فهرس المنتجات | Products Index**

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
          "filter": [
            "lowercase",
            "arabic_normalization",
            "arabic_stop",
            "arabic_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "variant_id": { "type": "long" },
      "sku": { "type": "keyword" },
      "name_ar": { 
        "type": "text",
        "analyzer": "arabic_analyzer",
        "fields": {
          "keyword": { "type": "keyword" },
          "suggest": { 
            "type": "completion",
            "analyzer": "arabic_analyzer"
          }
        }
      },
      "name_en": { "type": "text" },
      "description_ar": { 
        "type": "text",
        "analyzer": "arabic_analyzer"
      },
      "brand_name": { 
        "type": "keyword",
        "fields": {
          "text": { "type": "text" }
        }
      },
      "category_path": { "type": "keyword" },
      "price": { "type": "double" },
      "is_available": { "type": "boolean" },
      "color": { "type": "keyword" },
      "size": { "type": "keyword" },
      "badges": { "type": "keyword" },
      "popularity_score": { "type": "double" }
    }
  }
}
```

---

## 🔍 **استعلامات البحث | Search Queries**

### **بحث نصي بسيط**

```json
{
  "query": {
    "multi_match": {
      "query": "فستان صيفي",
      "fields": ["name_ar^3", "description_ar^1"],
      "type": "best_fields",
      "fuzziness": "AUTO"
    }
  }
}
```

---

### **بحث مع فلاتر**

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "فستان",
            "fields": ["name_ar", "description_ar"]
          }
        }
      ],
      "filter": [
        { "term": { "category_id": 5 } },
        { "term": { "brand_id": 3 } },
        { "range": { "price": { "gte": 100, "lte": 500 } } },
        { "term": { "is_available": true } }
      ]
    }
  },
  "sort": [
    { "_score": "desc" },
    { "popularity_score": "desc" }
  ],
  "size": 20
}
```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [12. خدمات التكامل | Integration Services](../12_Integration_Services.md)
- [05. الفهارس والأداء | Indexes & Performance](../05_Indexes_Performance.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08
