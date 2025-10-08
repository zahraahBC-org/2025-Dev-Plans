# 03. مرجع سريع | Quick Reference

## 🎯 **نظرة عامة | Overview**

مرجع سريع للمعلومات الأكثر استخدامًا - للرجوع السريع أثناء التطوير.

**الهدف | Purpose**: الوصول السريع للمعلومات الأساسية  
**الجمهور | Audience**: جميع المطورين  
**الاستخدام | Usage**: مرجع يومي

---

## 📋 **المحتويات | Contents**

### **أساليب HTTP | HTTP Methods**
| الأسلوب | الهدف | Idempotent | مثال |
|---------|-------|-----------|------|
| GET | قراءة | ✅ | `/v1/products` |
| POST | إنشاء | ❌ | `/v1/orders` |
| PUT | استبدال كامل | ✅ | `/v1/products/123` |
| PATCH | تحديث جزئي | ⚠️ | `/v1/orders/123` |
| DELETE | حذف | ✅ | `/v1/products/123` |

---

### **حالات HTTP | Status Codes**
| الكود | الاسم | الاستخدام |
|------|------|----------|
| **200** | OK | نجاح عام |
| **201** | Created | مورد جديد |
| **204** | No Content | حذف ناجح |
| **400** | Bad Request | طلب خاطئ |
| **401** | Unauthorized | غير مصادق |
| **403** | Forbidden | غير مصرح |
| **404** | Not Found | غير موجود |
| **409** | Conflict | تعارض |
| **422** | Unprocessable | فشل التحقق |
| **429** | Too Many Requests | تجاوز حد |
| **500** | Internal Error | خطأ خادم |
| **503** | Unavailable | غير متوفر |

---

### **رؤوس الطلب | Request Headers**
```http
Authorization: Bearer <jwt>              ← JWT token
Content-Type: application/json           ← نوع المحتوى
Accept: application/json                 ← نوع الاستجابة المطلوب
Accept-Language: ar                      ← اللغة المفضلة
X-Request-ID: <uuid>                     ← معرف الطلب
Idempotency-Key: <uuid>                  ← منع التكرار
If-Match: "etag-value"                   ← التحقق من النسخة
If-None-Match: "etag-value"              ← التخزين المؤقت
```

---

### **رؤوس الاستجابة | Response Headers**
```http
Content-Type: application/json           ← نوع المحتوى
ETag: "33a64df551425fcc55e"              ← معرف النسخة
Cache-Control: public, max-age=3600      ← سياسة الكاش
Location: /v1/orders/123                 ← مورد جديد
X-Request-ID: <uuid>                     ← معرف الطلب
X-RateLimit-Limit: 100                   ← الحد الأقصى
X-RateLimit-Remaining: 42                ← المتبقي
X-RateLimit-Reset: 1704715200            ← وقت إعادة التعيين
Retry-After: 60                          ← أعد المحاولة بعد
```

---

### **معاملات الاستعلام | Query Parameters**
```
# الترقيم
?page=1&limit=20                         ← Offset
?cursor=abc123&limit=20                  ← Cursor

# الفرز
?sort=price                              ← تصاعدي
?sort=-price                             ← تنازلي
?sort=-created_at,price                  ← متعدد

# التصفية
?filter[category]=dresses                ← بسيط
?filter[price.gte]=100                   ← مع معامل
?filter[status.in]=pending,confirmed     ← قائمة

# اختيار الحقول
?fields=id,name,price                    ← حقول محددة

# توسيع العلاقات
?expand=brand,category                   ← تضمين العلاقات
```

---

### **نموذج الخطأ | Error Format**
```json
{
  "error": {
    "code": "E1001",
    "message": "رسالة واضحة",
    "details": "تفاصيل إضافية أو مصفوفة",
    "trace_id": "c9b1f3a0...",
    "timestamp": "2025-01-08T12:00:00Z"
  }
}
```

---

### **أكواد الأخطاء | Error Codes**
```
E1xxx - أخطاء الطلب
E2xxx - المصادقة/التخويل
E3xxx - الموارد
E4xxx - منطق الأعمال
E5xxx - التحقق
E6xxx - Rate Limiting
E7xxx - الخادم
```

---

### **أمثلة cURL سريعة | Quick cURL Examples**

```bash
# قراءة قائمة
curl -X GET "https://api.zahraah.com/v1/products?page=1&limit=10" \
  -H "Authorization: Bearer $TOKEN"

# قراءة عنصر
curl -X GET "https://api.zahraah.com/v1/products/123" \
  -H "Authorization: Bearer $TOKEN"

# إنشاء
curl -X POST "https://api.zahraah.com/v1/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"customer_id":789,"items":[{"variant_id":123,"quantity":1}]}'

# تحديث
curl -X PATCH "https://api.zahraah.com/v1/orders/ORD-123" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/merge-patch+json" \
  -H "If-Match: \"etag-here\"" \
  -d '{"note":"تحديث الملاحظة"}'

# حذف
curl -X DELETE "https://api.zahraah.com/v1/products/123" \
  -H "Authorization: Bearer $TOKEN" \
  -H "If-Match: \"etag-here\""
```

---

### **SLOs السريعة | Quick SLOs**
```
زمن الاستجابة P95:  ≤ 300ms (قراءة)
                     ≤ 800ms (كتابة)
معدل الأخطاء:        ≤ 0.1% (5xx)
التوفر:             ≥ 99.9% شهريًا
Rate Limit:         100 req/min (عميل)
                    600 req/min (شريك)
```

---

## 🔗 **التنقل | Navigation**

[← السابق: قوائم التحقق | Previous: Checklists](02_Checklists.md)

[التالي: كتالوج الأخطاء | Next: Error Catalog →](04_Error_Catalog.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved