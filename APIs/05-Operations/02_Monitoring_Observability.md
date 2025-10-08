# 02. المراقبة والملاحظة | Monitoring & Observability

## 🎯 **نظرة عامة | Overview**

نظام مراقبة شامل لتتبع صحة وأداء واجهات الـ API في الوقت الفعلي.

**الهدف | Purpose**: تطبيق مراقبة وتتبع فعال  
**الجمهور | Audience**: مهندسو DevOps، SRE  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [الأعمدة الثلاثة](#الأعمدة-الثلاثة)
2. [السجلات](#السجلات)
3. [المقاييس](#المقاييس)
4. [التتبع الموزع](#التتبع-الموزع)
5. [اللوحات والتنبيهات](#اللوحات-والتنبيهات)

---

## 1️⃣ الأعمدة الثلاثة | Three Pillars of Observability {#الأعمدة-الثلاثة}

```
         Observability
              │
    ┌─────────┼─────────┐
    │         │         │
  Logs     Metrics   Traces
    │         │         │
  ماذا؟     كم؟      أين؟
```

---

## 2️⃣ السجلات | Logging {#السجلات}

### **Structured Logging (JSON)**

```json
{
  "timestamp": "2025-01-08T12:00:00.123Z",
  "level": "INFO",
  "service": "orders-service",
  "environment": "production",
  "trace_id": "c9b1f3a0-1b2c-3d4e-5f6g-7h8i9j0k1l2m",
  "span_id": "5f6g7h8i9j0k1l2m",
  "user_id": 789,
  "method": "POST",
  "path": "/v1/orders",
  "status_code": 201,
  "duration_ms": 145,
  "request_size_bytes": 512,
  "response_size_bytes": 1024,
  "ip": "185.46.212.35",
  "user_agent": "Zahraah/1.0 (iOS 17.2)",
  "message": "Order created successfully",
  "context": {
    "order_id": "ORD-20250108-00123",
    "total": 702.70,
    "items_count": 2
  }
}
```

### **مستويات السجلات**
| المستوى | الاستخدام | البيئة |
|---------|----------|--------|
| **DEBUG** | معلومات تطوير مفصلة | Dev فقط |
| **INFO** | أحداث عادية | جميع البيئات |
| **WARNING** | أحداث غير متوقعة لكن قابلة للإدارة | جميع البيئات |
| **ERROR** | أخطاء تحتاج تدخل | جميع البيئات |
| **CRITICAL** | أعطال تحتاج تدخل فوري | Prod |

---

### **ما يجب تسجيله**
```
✅ كل طلب API (method, path, status, duration)
✅ أخطاء 4xx/5xx مع trace_id
✅ عمليات حرجة (إنشاء طلب، دفع)
✅ تغييرات حالة مهمة
✅ اتصالات خدمات خارجية
✅ Rate Limit events
✅ Authentication failures
```

### **ما لا يجب تسجيله**
```
❌ كلمات المرور
❌ Tokens كاملة
❌ بيانات حساسة (PII)
❌ معلومات بطاقات الدفع
```

---

## 3️⃣ المقاييس | Metrics {#المقاييس}

### **المقاييس الأساسية | Golden Signals**

#### **1. Latency - زمن الاستجابة**
```
Histogram: api_request_duration_seconds

Labels:
- method (GET, POST, ...)
- path (/v1/products, /v1/orders, ...)
- status (200, 400, 500, ...)

Percentiles:
- p50 (median)
- p95 (95th percentile)
- p99 (99th percentile)
```

**مثال Prometheus Query**:
```promql
histogram_quantile(0.95,
  rate(api_request_duration_seconds_bucket[5m])
)
```

---

#### **2. Traffic - حركة المرور**
```
Counter: api_requests_total

Labels:
- method
- path
- status

Rate (requests per second):
rate(api_requests_total[1m])
```

---

#### **3. Errors - الأخطاء**
```
Counter: api_errors_total

Labels:
- error_code (E1001, E2001, ...)
- status (400, 401, 500, ...)

Error Rate:
rate(api_errors_total{status=~"5.."}[5m])
/ rate(api_requests_total[5m])
```

---

#### **4. Saturation - التشبع**
```
Gauge: api_active_connections
Gauge: api_queue_depth
Gauge: api_db_pool_active

Alert when:
- active_connections > 80% of max
- queue_depth > threshold
- db_pool_active > 90%
```

---

### **مقاييس Business**
```
Counter: orders_created_total
Counter: orders_cancelled_total
Gauge: revenue_total_sar
Gauge: active_users_count
```

---

## 4️⃣ التتبع الموزع | Distributed Tracing {#التتبع-الموزع}

### **OpenTelemetry**

```
Request Flow:

API Gateway
  trace_id: c9b1f3a0...
  span_id: 1a2b3c4d...
  │
  ├─► Orders Service
  │     span_id: 2b3c4d5e...
  │     parent: 1a2b3c4d...
  │     │
  │     ├─► Products Service (check stock)
  │     │     span_id: 3c4d5e6f...
  │     │     parent: 2b3c4d5e...
  │     │
  │     └─► Database Query
  │           span_id: 4d5e6f7g...
  │           parent: 2b3c4d5e...
  │
  └─► Payments Service
        span_id: 5e6f7g8h...
        parent: 1a2b3c4d...
```

### **W3C Trace Context**
```http
traceparent: 00-c9b1f3a0...trace_id...-1a2b3c4d...span_id...-01
             ││ └───────────────────┘  └──────────────────┘  └┘
             ││      trace_id               span_id        flags
             │└─ version
             └─ format
```

---

## 5️⃣ اللوحات والتنبيهات | Dashboards & Alerts {#اللوحات-والتنبيهات}

### **لوحات المراقبة | Dashboards**

#### **1. Platform Overview**
```
┌─────────────────────────────────────────────┐
│  Requests/sec:  1,250 req/s                 │
│  Latency P95:   245ms     🟢                │
│  Error Rate:    0.05%     🟢                │
│  Availability:  99.98%    🟢                │
└─────────────────────────────────────────────┘

📊 Requests by Status (Last Hour)
- 2xx: ████████████████████ 95%
- 4xx: ███ 4%
- 5xx: ▌ 1%

📈 Latency (P95) Trend
[graph showing 200-300ms last 24h]
```

---

#### **2. API Gateway Dashboard**
```
- Requests/sec by endpoint
- Rate Limit events
- CORS violations
- Authentication failures
- Cache Hit Ratio
```

---

#### **3. Service-Level Dashboard**
```
Orders Service:
- Request Rate
- Latency (p50, p95, p99)
- Error Rate
- Active DB Connections
- Queue Depth
```

---

### **التنبيهات | Alerts**

#### **تنبيهات حرجة**
```yaml
- name: HighErrorRate
  condition: error_rate > 1%
  duration: 5m
  severity: critical
  notify: pagerduty
  
- name: HighLatency
  condition: p95_latency > 500ms
  duration: 10m
  severity: warning
  notify: slack
  
- name: ServiceDown
  condition: availability < 99%
  duration: 2m
  severity: critical
  notify: pagerduty
```

---

## ✅ **قائمة التحقق | Checklist**

### **عند إعداد المراقبة**
- [ ] Structured Logging مفعل
- [ ] trace_id في كل طلب
- [ ] المقاييس الأساسية تُجمع
- [ ] Distributed Tracing مفعل
- [ ] Dashboards منشورة
- [ ] Alerts مهيأة
- [ ] On-call جاهز

---

## 🔗 **التنقل | Navigation**

[← السابق: استراتيجية الاختبار | Previous: Testing Strategy](../06-Testing-Quality/01_Testing_Strategy.md)

[التالي: دليل العمليات | Next: Operations Playbook →](03_Operations_Playbook.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved