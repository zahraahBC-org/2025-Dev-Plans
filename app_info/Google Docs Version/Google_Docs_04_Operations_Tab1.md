# TAB 1: تخزين Redis المؤقت | Redis Caching

## 16. إدارة التخزين المؤقت (Redis Caching)
### Redis Caching

---

## 🎯 **الهدف | Objective**
تطبيق نظام تخزين مؤقت Redis لتخزين واسترجاع البيانات عالي الأداء في تطبيق Flutter للتجارة الإلكترونية.

## 📋 **القاعدة | Rule**
**العربية**: Redis للكاش + TTL مناسب + سياسة Stale-While-Revalidate  
**English**: Redis for caching + appropriate TTL + Stale-While-Revalidate policy

## 💡 **الفوائد | Benefits**
- **الأداء | Performance**: وصول أسرع للبيانات وتقليل استدعاءات API
- **قابلية التوسع | Scalability**: التعامل مع حركة مرور عالية مع التخزين المؤقت
- **تقليل التكلفة | Cost Reduction**: تقليل عبء الخادم وتكاليف API
- **تجربة المستخدم | User Experience**: أوقات استجابة أسرع للتطبيق
- **دعم عدم الاتصال | Offline Support**: تقديم البيانات المخزنة مؤقتاً عند عدم الاتصال
- **اتساق البيانات | Data Consistency**: الحفاظ على سلامة البيانات عبر التخزين المؤقت

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع عمليات البيانات التي تتطلب تخزين مؤقت
- **كيفية التطبيق**:
  - إعداد خادم Redis والاتصال
  - تطبيق طبقة تخزين مؤقت مع سياسات TTL
  - استخدام نمط Stale-While-Revalidate
  - إضافة استراتيجيات إبطال التخزين المؤقت
  - مراقبة معدلات ضرب التخزين المؤقت والأداء
- **Result**: High-performance caching system with data consistency

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بتخزين Redis المؤقت | Redis Caching Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد خادم Redis والاتصال
- **🔴 حرج**: تطبيق طبقة تخزين مؤقت أساسية
- **🟠 عالي**: إضافة سياسات TTL وإبطال التخزين المؤقت

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تطبيق نمط Stale-While-Revalidate
- **🟠 عالي**: إضافة استراتيجيات تخزين مؤقت متقدمة
- **🟡 متوسط**: تطبيق مراقبة وتحليلات التخزين المؤقت

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تحسين التخزين المؤقت المتقدم
- **🟡 متوسط**: إدارة التخزين المؤقت مدعومة بالذكاء الاصطناعي
- **🟢 منخفض**: تسخين التخزين المؤقت التنبؤي

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بتخزين Redis المؤقت | Redis Caching Specific Metrics:**
- **معدل ضرب التخزين المؤقت | Cache Hit Rate**: >90% cache hit rate
- **وقت الاستجابة | Response Time**: <10ms cache response time
- **استخدام الذاكرة | Memory Usage**: <80% Redis memory utilization
- **اتساق البيانات | Data Consistency**: 100% cache consistency
- **التوفر | Availability**: >99.9% Redis availability
- **تقليل التكلفة | Cost Reduction**: >50% API cost reduction

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بتخزين Redis المؤقت | Redis Caching Specific Pitfalls:**
- **تجنب | Avoid**: قيم TTL غير مناسبة
- **تجنب | Avoid**: عدم وجود إبطال التخزين المؤقت
- **تجنب | Avoid**: تسريبات الذاكرة والاستخدام المفرط للذاكرة
- **تجنب | Avoid**: تصميم مفاتيح تخزين مؤقت ضعيف
- **تجنب | Avoid**: مراقبة وتنبيه غير كافية

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: قيم TTL مناسبة لأنواع البيانات المختلفة
- **استخدم | Use**: نمط Stale-While-Revalidate لتجربة مستخدم أفضل
- **استخدم | Use**: استراتيجيات إبطال تخزين مؤقت مناسبة
- **استخدم | Use**: مراقبة وتنبيه لأداء التخزين المؤقت
- **استخدم | Use**: استراتيجيات تسخين وتحضير التخزين المؤقت

## 🔧 **Redis Setup | إعداد Redis**

### **1. Redis Configuration | تكوين Redis**
```yaml
# redis.conf
# Network
bind 0.0.0.0
port 6379
protected-mode no

# Memory
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log

# Security
requirepass your_redis_password

# Performance
tcp-keepalive 300
timeout 0
```

### **2. Redis Connection | اتصال Redis**
```dart
// lib/core/cache/redis_client.dart
class RedisClient {
  static Redis? _redis;
  static const String _host = 'localhost';
  static const int _port = 6379;
  static const String _password = 'your_redis_password';
  
  static Future<Redis> get instance async {
    if (_redis == null) {
      _redis = await Redis.connect('redis://$_password@$_host:$_port');
    }
    return _redis!;
  }
  
  static Future<void> disconnect() async {
    await _redis?.close();
    _redis = null;
  }
  
  static Future<bool> isConnected() async {
    try {
      final redis = await instance;
      await redis.ping();
      return true;
    } catch (e) {
      return false;
    }
  }
}
```

## 💾 **Caching Layer | طبقة التخزين المؤقت**

### **1. Cache Service | خدمة التخزين المؤقت**
```dart
// lib/core/cache/cache_service.dart
class CacheService {
  static const Duration _defaultTTL = Duration(minutes: 30);
  static const Duration _shortTTL = Duration(minutes: 5);
  static const Duration _longTTL = Duration(hours: 24);
  
  static Future<T?> get<T>(String key) async {
    try {
      final redis = await RedisClient.instance;
      final value = await redis.get(key);
      
      if (value == null) return null;
      
      return _deserialize<T>(value);
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_get');
      return null;
    }
  }
  
  static Future<void> set<T>(String key, T value, {Duration? ttl}) async {
    try {
      final redis = await RedisClient.instance;
      final serialized = _serialize(value);
      
      if (ttl != null) {
        await redis.setex(key, ttl.inSeconds, serialized);
      } else {
        await redis.set(key, serialized);
      }
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_set');
    }
  }
  
  static Future<void> delete(String key) async {
    try {
      final redis = await RedisClient.instance;
      await redis.del([key]);
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_delete');
    }
  }
  
  static Future<void> deletePattern(String pattern) async {
    try {
      final redis = await RedisClient.instance;
      final keys = await redis.keys(pattern);
      if (keys.isNotEmpty) {
        await redis.del(keys);
      }
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_delete_pattern');
    }
  }
  
  static Future<bool> exists(String key) async {
    try {
      final redis = await RedisClient.instance;
      final result = await redis.exists([key]);
      return result == 1;
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_exists');
      return false;
    }
  }
  
  static String _serialize<T>(T value) {
    return jsonEncode(value);
  }
  
  static T _deserialize<T>(String value) {
    return jsonDecode(value) as T;
  }
}
```

### **2. Cache Keys | مفاتيح التخزين المؤقت**
```dart
// lib/core/cache/cache_keys.dart
class CacheKeys {
  // Product keys
  static String product(String id) => 'product:$id';
  static String products(String category) => 'products:$category';
  static String featuredProducts() => 'products:featured';
  static String searchProducts(String query) => 'products:search:$query';
  
  // User keys
  static String user(String id) => 'user:$id';
  static String userProfile(String id) => 'user:$id:profile';
  static String userCart(String id) => 'user:$id:cart';
  
  // Order keys
  static String order(String id) => 'order:$id';
  static String userOrders(String userId) => 'user:$userId:orders';
  
  // Category keys
  static String categories() => 'categories';
  static String category(String id) => 'category:$id';
  
  // General keys
  static String appConfig() => 'app:config';
  static String appVersion() => 'app:version';
}
```

## ⏰ **TTL Policies | سياسات TTL**

### **1. TTL Configuration | تكوين TTL**
```dart
// lib/core/cache/ttl_policies.dart
class TTLPolicies {
  static const Duration product = Duration(hours: 1);
  static const Duration products = Duration(minutes: 30);
  static const Duration user = Duration(hours: 24);
  static const Duration userProfile = Duration(hours: 12);
  static const Duration userCart = Duration(hours: 2);
  static const Duration order = Duration(days: 7);
  static const Duration categories = Duration(hours: 6);
  static const Duration appConfig = Duration(hours: 1);
  static const Duration searchResults = Duration(minutes: 15);
  static const Duration featuredProducts = Duration(minutes: 30);
  
  static Duration getTTL(String key) {
    if (key.startsWith('product:')) return product;
    if (key.startsWith('products:')) return products;
    if (key.startsWith('user:')) return user;
    if (key.startsWith('order:')) return order;
    if (key.startsWith('categories')) return categories;
    if (key.startsWith('app:')) return appConfig;
    if (key.startsWith('search:')) return searchResults;
    
    return Duration(minutes: 30); // Default TTL
  }
}
```

### **2. Cache Invalidation | إبطال التخزين المؤقت**
```dart
// lib/core/cache/cache_invalidation.dart
class CacheInvalidation {
  static Future<void> invalidateProduct(String productId) async {
    await CacheService.delete(CacheKeys.product(productId));
    await CacheService.deletePattern('products:*');
    await CacheService.delete(CacheKeys.featuredProducts());
  }
  
  static Future<void> invalidateUser(String userId) async {
    await CacheService.delete(CacheKeys.user(userId));
    await CacheService.delete(CacheKeys.userProfile(userId));
    await CacheService.delete(CacheKeys.userCart(userId));
    await CacheService.deletePattern('user:$userId:*');
  }
  
  static Future<void> invalidateOrder(String orderId) async {
    await CacheService.delete(CacheKeys.order(orderId));
  }
  
  static Future<void> invalidateCategories() async {
    await CacheService.delete(CacheKeys.categories());
    await CacheService.deletePattern('category:*');
  }
  
  static Future<void> invalidateAll() async {
    await CacheService.deletePattern('*');
  }
}
```

## 🔄 **Stale-While-Revalidate Pattern | نمط Stale-While-Revalidate**

### **1. SWR Implementation | تنفيذ SWR**
```dart
// lib/core/cache/stale_while_revalidate.dart
class StaleWhileRevalidate<T> {
  final String key;
  final Future<T> Function() fetcher;
  final Duration? ttl;
  
  StaleWhileRevalidate({
    required this.key,
    required this.fetcher,
    this.ttl,
  });
  
  Future<T> get() async {
    // Try to get from cache first
    final cached = await CacheService.get<T>(key);
    
    if (cached != null) {
      // Return cached data immediately
      _refreshInBackground();
      return cached;
    }
    
    // If no cached data, fetch fresh data
    return await _fetchAndCache();
  }
  
  Future<void> _refreshInBackground() async {
    // Refresh data in background without blocking
    Future.microtask(() async {
      try {
        await _fetchAndCache();
      } catch (e) {
        // Log error but don't throw
        ErrorHandler.handleError(e, null, context: 'swr_background_refresh');
      }
    });
  }
  
  Future<T> _fetchAndCache() async {
    final data = await fetcher();
    await CacheService.set(key, data, ttl: ttl);
    return data;
  }
}
```

### **2. SWR Usage | استخدام SWR**
```dart
// lib/features/products/domain/usecases/get_products_usecase.dart
class GetProductsUseCase {
  final ProductRepository _repository;
  
  GetProductsUseCase(this._repository);
  
  Future<Result<List<Product>>> call({
    String? category,
    String? searchQuery,
  }) async {
    try {
      final cacheKey = _getCacheKey(category, searchQuery);
      
      final swr = StaleWhileRevalidate<List<Product>>(
        key: cacheKey,
        fetcher: () => _fetchProducts(category, searchQuery),
        ttl: TTLPolicies.products,
      );
      
      final products = await swr.get();
      return Success(products);
    } catch (e) {
      return Failure(NetworkError('Failed to get products: $e'));
    }
  }
  
  String _getCacheKey(String? category, String? searchQuery) {
    if (searchQuery != null) {
      return CacheKeys.searchProducts(searchQuery);
    } else if (category != null) {
      return CacheKeys.products(category);
    } else {
      return CacheKeys.featuredProducts();
    }
  }
  
  Future<List<Product>> _fetchProducts(String? category, String? searchQuery) async {
    final result = await _repository.getProducts(
      category: category,
      searchQuery: searchQuery,
    );
    
    if (result is Success<List<Product>>) {
      return result.data;
    } else {
      throw Exception('Failed to fetch products');
    }
  }
}
```

## 📊 **Cache Monitoring | مراقبة التخزين المؤقت**

### **1. Cache Metrics | مقاييس التخزين المؤقت**
```dart
// lib/core/cache/cache_metrics.dart
class CacheMetrics {
  static int _hits = 0;
  static int _misses = 0;
  static int _sets = 0;
  static int _deletes = 0;
  
  static int get hits => _hits;
  static int get misses => _misses;
  static int get sets => _sets;
  static int get deletes => _deletes;
  
  static double get hitRate => _hits / (_hits + _misses);
  static double get missRate => _misses / (_hits + _misses);
  
  static void recordHit() {
    _hits++;
    _logMetric('cache_hit');
  }
  
  static void recordMiss() {
    _misses++;
    _logMetric('cache_miss');
  }
  
  static void recordSet() {
    _sets++;
    _logMetric('cache_set');
  }
  
  static void recordDelete() {
    _deletes++;
    _logMetric('cache_delete');
  }
  
  static void _logMetric(String event) {
    AnalyticsService.logEvent(event, {
      'hit_rate': hitRate,
      'miss_rate': missRate,
      'total_operations': _hits + _misses + _sets + _deletes,
    });
  }
  
  static Map<String, dynamic> getMetrics() {
    return {
      'hits': _hits,
      'misses': _misses,
      'sets': _sets,
      'deletes': _deletes,
      'hit_rate': hitRate,
      'miss_rate': missRate,
    };
  }
  
  static void reset() {
    _hits = 0;
    _misses = 0;
    _sets = 0;
    _deletes = 0;
  }
}
```

### **2. Cache Health Check | فحص صحة التخزين المؤقت**
```dart
// lib/core/cache/cache_health.dart
class CacheHealth {
  static Future<Map<String, dynamic>> checkHealth() async {
    final health = <String, dynamic>{};
    
    // Check Redis connection
    health['redis_connected'] = await RedisClient.isConnected();
    
    // Check cache performance
    health['cache_performance'] = await _checkCachePerformance();
    
    // Check memory usage
    health['memory_usage'] = await _checkMemoryUsage();
    
    // Check hit rate
    health['hit_rate'] = CacheMetrics.hitRate;
    
    return health;
  }
  
  static Future<Map<String, dynamic>> _checkCachePerformance() async {
    final stopwatch = Stopwatch()..start();
    
    try {
      await CacheService.set('health_check', 'test');
      await CacheService.get('health_check');
      await CacheService.delete('health_check');
      
      stopwatch.stop();
      
      return {
        'response_time_ms': stopwatch.elapsedMilliseconds,
        'status': 'healthy',
      };
    } catch (e) {
      return {
        'response_time_ms': -1,
        'status': 'unhealthy',
        'error': e.toString(),
      };
    }
  }
  
  static Future<Map<String, dynamic>> _checkMemoryUsage() async {
    try {
      final redis = await RedisClient.instance;
      final info = await redis.info('memory');
      
      // Parse memory info
      final lines = info.split('\n');
      final usedMemory = lines
          .firstWhere((line) => line.startsWith('used_memory:'))
          .split(':')[1]
          .trim();
      
      return {
        'used_memory': usedMemory,
        'status': 'healthy',
      };
    } catch (e) {
      return {
        'used_memory': 'unknown',
        'status': 'unhealthy',
        'error': e.toString(),
      };
    }
  }
}
```

## 🔧 **Cache Optimization | تحسين التخزين المؤقت**

### **1. Cache Warming | تسخين التخزين المؤقت**
```dart
// lib/core/cache/cache_warming.dart
class CacheWarming {
  static Future<void> warmCache() async {
    // Warm up frequently accessed data
    await _warmProducts();
    await _warmCategories();
    await _warmAppConfig();
  }
  
  static Future<void> _warmProducts() async {
    try {
      // Warm up featured products
      final featuredProducts = await _fetchFeaturedProducts();
      await CacheService.set(
        CacheKeys.featuredProducts(),
        featuredProducts,
        ttl: TTLPolicies.featuredProducts,
      );
      
      // Warm up categories
      final categories = await _fetchCategories();
      for (final category in categories) {
        final products = await _fetchProductsByCategory(category.id);
        await CacheService.set(
          CacheKeys.products(category.id),
          products,
          ttl: TTLPolicies.products,
        );
      }
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_warming_products');
    }
  }
  
  static Future<void> _warmCategories() async {
    try {
      final categories = await _fetchCategories();
      await CacheService.set(
        CacheKeys.categories(),
        categories,
        ttl: TTLPolicies.categories,
      );
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_warming_categories');
    }
  }
  
  static Future<void> _warmAppConfig() async {
    try {
      final config = await _fetchAppConfig();
      await CacheService.set(
        CacheKeys.appConfig(),
        config,
        ttl: TTLPolicies.appConfig,
      );
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'cache_warming_config');
    }
  }
  
  // Helper methods
  static Future<List<Product>> _fetchFeaturedProducts() async {
    // Implementation
    return [];
  }
  
  static Future<List<Category>> _fetchCategories() async {
    // Implementation
    return [];
  }
  
  static Future<List<Product>> _fetchProductsByCategory(String categoryId) async {
    // Implementation
    return [];
  }
  
  static Future<Map<String, dynamic>> _fetchAppConfig() async {
    // Implementation
    return {};
  }
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. إعداد Redis | Redis Setup**
- [ ] إعداد خادم Redis
- [ ] تكوين اتصال Redis
- [ ] تطبيق تجميع الاتصالات
- [ ] اختبار اتصالية Redis

### **2. طبقة التخزين المؤقت | Caching Layer**
- [ ] تطبيق خدمة التخزين المؤقت
- [ ] إضافة إدارة مفاتيح التخزين المؤقت
- [ ] إعداد سياسات TTL
- [ ] اختبار وظائف التخزين المؤقت

### **3. أنماط التخزين المؤقت | Cache Patterns**
- [ ] تطبيق Stale-While-Revalidate
- [ ] إضافة إبطال التخزين المؤقت
- [ ] إعداد تسخين التخزين المؤقت
- [ ] اختبار أنماط التخزين المؤقت

### **4. المراقبة | Monitoring**
- [ ] إضافة مقاييس التخزين المؤقت
- [ ] تطبيق فحوصات الصحة
- [ ] إعداد لوحات مراقبة
- [ ] اختبار نظام المراقبة

### **5. التحسين | Optimization**
- [ ] تحسين أداء التخزين المؤقت
- [ ] إضافة تسخين التخزين المؤقت
- [ ] تطبيق تحسين التخزين المؤقت
- [ ] اختبار استراتيجيات التحسين

---

**Next Tab**: Error Catalog | كتالوج الأخطاء

