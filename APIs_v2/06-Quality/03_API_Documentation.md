# توثيق APIs — API Documentation

---

## **أنواع التوثيق | Documentation Types**

### **1. Code Documentation**
```php
/**
 * Create new product
 *
 * @param  StoreProductRequest  $request
 * @return ProductResource
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function store(StoreProductRequest $request)
{
    // Implementation
}
```

### **2. API Documentation**
- Postman Collection
- OpenAPI/Swagger (optional)
- README with endpoints list

### **3. User Guide**
- Authentication guide
- Error codes catalog
- Rate limits
- Examples

---

## **Postman Collection**

Export collection with:
- All endpoints
- Example requests
- Example responses
- Environment variables

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
