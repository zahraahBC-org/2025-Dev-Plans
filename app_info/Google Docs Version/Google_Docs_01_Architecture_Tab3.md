# TAB 3: معالجة أخطاء طبقة البيانات | Data Layer Error Handling

## 3. طبقة البيانات ومعالجة الأخطاء | Data Layer & Error Handling
### تطبيق طبقة بيانات قوية مع معالجة شاملة للأخطاء وإدارة آمنة للبيانات

---

## 🎯 **الهدف | Objective**
تطبيق طبقة بيانات قوية مع معالجة شاملة للأخطاء وإدارة آمنة للبيانات وتواصل شبكة موثوق لتطبيق Flutter للتجارة الإلكترونية.

## 📋 **القاعدة | Rule**
**العربية**: لا ترمي Exceptions للأعلى؛ أرجِع Result<Success, Failure> مع معالجة شاملة للأخطاء  
**English**: Don't throw Exceptions upward; return Result<Success, Failure> with comprehensive error handling

## 💡 **الفوائد | Benefits**
- **معالجة موحدة للأخطاء | Unified Error Handling**: إدارة أخطاء متسقة عبر UI
- **أمان الأنواع | Type Safety**: فحص أخطاء وقت التجميع مع Result pattern
- **تجربة مستخدم أفضل | Better UX**: رسائل خطأ ودية للمستخدم والاسترداد
- **سهولة التصحيح | Debugging**: تصنيف أخطاء واضح وتسجيل
- **سهولة الصيانة | Maintainability**: منطق معالجة أخطاء مركزي
- **الاختبار | Testing**: سهولة اختبار سيناريوهات الأخطاء والحالات الحدية

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع عمليات البيانات واستدعاءات API وتفاعلات الخدمات الخارجية
- **كيفية التطبيق**:
  - استخدام Result<T> pattern لجميع عمليات البيانات
  - تطبيق أنواع أخطاء شاملة (Network, Server, Cache, Auth, Validation)
  - إضافة تحويل أخطاء مناسب ورسائل ودية للمستخدم
  - تطبيق منطق إعادة المحاولة مع exponential backoff
  - إضافة تسجيل ومراقبة مناسبة
- **النتيجة**: طبقة بيانات موثوقة مع معالجة ممتازة للأخطاء وتجربة مستخدم

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بطبقة البيانات ومعالجة الأخطاء | Data Layer & Error Handling Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: تطبيق Result pattern ومعالجة شاملة للأخطاء
- **🔴 حرج**: إعداد مصادر البيانات (بعيدة، محلية) ونمط المستودع
- **🟠 عالي**: إضافة فحوصات اتصال الشبكة وتخزين مؤقت أساسي

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تطبيق منطق إعادة المحاولة واسترداد أخطاء متقدم
- **🟠 عالي**: إضافة تسجيل ومراقبة شاملة
- **🟡 متوسط**: إضافة دعم عدم الاتصال ومزامنة البيانات

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: استراتيجيات تخزين مؤقت متقدمة وتحسين الأداء
- **🟡 متوسط**: التنبؤ بالأخطاء والوقاية مدعومة بالذكاء الاصطناعي
- **🟢 منخفض**: تحليلات متقدمة وتحليل اتجاهات الأخطاء

## 📈 **مؤشرات النجاح | Success Metrics**

### **مؤشرات خاصة بطبقة البيانات ومعالجة الأخطاء | Data Layer & Error Handling Specific Metrics:**
- **معدل الأخطاء | Error Rate**: <1% معدل أخطاء لعمليات البيانات، <0.1% للعمليات الحرجة
- **وقت الاسترداد | Recovery Time**: <2 ثانية متوسط استرداد الأخطاء، <5 ثوان للأخطاء المعقدة
- **تجربة المستخدم | User Experience**: 95%+ رضا المستخدم عن معالجة الأخطاء
- **موثوقية النظام | System Reliability**: 99.9%+ وقت التشغيل، <0.1% فقدان بيانات
- **الأداء | Performance**: <500ms متوسط وقت الاستجابة، <1s للعمليات المعقدة
- **المراقبة | Monitoring**: 100% تغطية الأخطاء، تنبيهات فورية

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **أخطاء خاصة بطبقة البيانات ومعالجة الأخطاء | Data Layer & Error Handling Specific Pitfalls:**
- **تجنب**: رمي استثناءات دون معالجة مناسبة
- **تجنب**: رسائل خطأ عامة دون سياق
- **تجنب**: عدم وجود منطق إعادة محاولة لفشل الشبكة
- **تجنب**: عدم وجود دعم عدم الاتصال
- **تجنب**: تسجيل ومراقبة غير كافية

### **أفضل الممارسات | Best Practices:**
- **استخدم**: Result pattern لجميع عمليات البيانات
- **استخدم**: أنواع أخطاء شاملة وتحويل
- **استخدم**: منطق إعادة محاولة مع exponential backoff
- **استخدم**: تسجيل ومراقبة مناسبة
- **استخدم**: دعم عدم الاتصال ومزامنة البيانات

## 🏗️ **تنفيذ نمط النتيجة | Result Pattern Implementation**

### **1. فئة النتيجة | Result Class**
```dart
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

class Failure<T> extends Result<T> {
  final AppError error;
  const Failure(this.error);
}
```

### **2. أنواع الأخطاء | Error Types**
```dart
sealed class AppError {
  final String message;
  final String? code;
  const AppError(this.message, [this.code]);
}

class NetworkError extends AppError {
  const NetworkError(super.message, [super.code]);
}

class ServerError extends AppError {
  final int statusCode;
  const ServerError(super.message, this.statusCode, [super.code]);
}

class CacheError extends AppError {
  const CacheError(super.message, [super.code]);
}

class AuthError extends AppError {
  const AuthError(super.message, [super.code]);
}

class ValidationError extends AppError {
  const ValidationError(super.message, [super.code]);
}
```

## 🔧 **نمط المستودع | Repository Pattern**

### **1. واجهة المستودع | Repository Interface**
```dart
abstract class ProductRepository {
  Future<Result<List<Product>>> getProducts();
  Future<Result<Product>> getProductById(String id);
  Future<Result<Product>> addProduct(Product product);
  Future<Result<void>> updateProduct(Product product);
  Future<Result<void>> deleteProduct(String id);
}
```

### **2. تنفيذ المستودع | Repository Implementation**
```dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final ProductLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Result<List<Product>>> getProducts() async {
    try {
      if (await networkInfo.isConnected) {
        final result = await remoteDataSource.getProducts();
        return result.fold(
          (products) {
            localDataSource.cacheProducts(products);
            return Success(products);
          },
          (error) => Failure(error),
        );
      } else {
        final cachedProducts = await localDataSource.getCachedProducts();
        return Success(cachedProducts);
      }
    } catch (e) {
      return Failure(NetworkError('Failed to fetch products: $e'));
    }
  }
}
```

## 🌐 **طبقة الشبكة | Network Layer**

### **1. خدمة API | API Service**
```dart
class ApiService {
  final Dio dio;
  final String baseUrl;

  ApiService({required this.dio, required this.baseUrl}) {
    dio.options.baseUrl = baseUrl;
    dio.options.connectTimeout = const Duration(seconds: 30);
    dio.options.receiveTimeout = const Duration(seconds: 30);
    
    dio.interceptors.addAll([
      AuthInterceptor(),
      LoggingInterceptor(),
      ErrorInterceptor(),
    ]);
  }

  Future<Result<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    T Function(Map<String, dynamic>)? fromJson,
  }) async {
    try {
      final response = await dio.get(
        path,
        queryParameters: queryParameters,
      );
      
      if (response.statusCode == 200) {
        final data = fromJson?.call(response.data) ?? response.data;
        return Success(data);
      } else {
        return Failure(ServerError(
          'Server error: ${response.statusCode}',
          response.statusCode ?? 0,
        ));
      }
    } on DioException catch (e) {
      return Failure(_handleDioError(e));
    } catch (e) {
      return Failure(NetworkError('Unexpected error: $e'));
    }
  }
}
```

### **2. معالجة الأخطاء | Error Handling**
```dart
AppError _handleDioError(DioException error) {
  switch (error.type) {
    case DioExceptionType.connectionTimeout:
    case DioExceptionType.sendTimeout:
    case DioExceptionType.receiveTimeout:
      return const NetworkError('Connection timeout');
    case DioExceptionType.badResponse:
      return ServerError(
        'Server error: ${error.response?.statusCode}',
        error.response?.statusCode ?? 0,
      );
    case DioExceptionType.cancel:
      return const NetworkError('Request cancelled');
    case DioExceptionType.connectionError:
      return const NetworkError('No internet connection');
    default:
      return NetworkError('Network error: ${error.message}');
  }
}
```

## 💾 **التخزين المحلي | Local Storage**

### **1. مصدر البيانات المحلي | Local Data Source**
```dart
abstract class ProductLocalDataSource {
  Future<List<Product>> getCachedProducts();
  Future<void> cacheProducts(List<Product> products);
  Future<Product?> getCachedProduct(String id);
  Future<void> cacheProduct(Product product);
  Future<void> clearCache();
}

class ProductLocalDataSourceImpl implements ProductLocalDataSource {
  final HiveInterface hive;
  static const String _boxName = 'products';

  ProductLocalDataSourceImpl({required this.hive});

  @override
  Future<List<Product>> getCachedProducts() async {
    try {
      final box = await hive.openBox(_boxName);
      final productsJson = box.get('products') as List<dynamic>?;
      
      if (productsJson == null) return [];
      
      return productsJson
          .map((json) => Product.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw CacheError('Failed to get cached products: $e');
    }
  }

  @override
  Future<void> cacheProducts(List<Product> products) async {
    try {
      final box = await hive.openBox(_boxName);
      final productsJson = products.map((p) => p.toJson()).toList();
      await box.put('products', productsJson);
    } catch (e) {
      throw CacheError('Failed to cache products: $e');
    }
  }
}
```

## 🔄 **منطق إعادة المحاولة | Retry Logic**

### **1. تنفيذ إعادة المحاولة | Retry Implementation**
```dart
class RetryHandler {
  static Future<Result<T>> retry<T>(
    Future<Result<T>> Function() operation, {
    int maxRetries = 3,
    Duration initialDelay = const Duration(seconds: 1),
  }) async {
    int attempts = 0;
    Duration delay = initialDelay;

    while (attempts < maxRetries) {
      final result = await operation();
      
      if (result is Success<T>) {
        return result;
      }
      
      attempts++;
      if (attempts < maxRetries) {
        await Future.delayed(delay);
        delay *= 2; // Exponential backoff
      }
    }
    
    return Failure(NetworkError('Max retries exceeded'));
  }
}
```

## 📊 **المراقبة والتسجيل | Monitoring & Logging**

### **1. مسجل الأخطاء | Error Logger**
```dart
class ErrorLogger {
  static void logError(AppError error, {StackTrace? stackTrace}) {
    // Log to console in development
    if (kDebugMode) {
      print('Error: ${error.message}');
      if (stackTrace != null) {
        print('Stack trace: $stackTrace');
      }
    }
    
    // Send to crash reporting service
    FirebaseCrashlytics.instance.recordError(
      error,
      stackTrace,
      fatal: false,
    );
    
    // Send to analytics
    FirebaseAnalytics.instance.logEvent(
      name: 'error_occurred',
      parameters: {
        'error_type': error.runtimeType.toString(),
        'error_message': error.message,
        'error_code': error.code ?? 'unknown',
      },
    );
  }
}
```

## 🧪 **اختبار طبقة البيانات | Testing Data Layer**

### **1. اختبارات المستودع | Repository Tests**
```dart
void main() {
  group('ProductRepository', () {
    late ProductRepository repository;
    late MockProductRemoteDataSource mockRemoteDataSource;
    late MockProductLocalDataSource mockLocalDataSource;
    late MockNetworkInfo mockNetworkInfo;

    setUp(() {
      mockRemoteDataSource = MockProductRemoteDataSource();
      mockLocalDataSource = MockProductLocalDataSource();
      mockNetworkInfo = MockNetworkInfo();
      
      repository = ProductRepositoryImpl(
        remoteDataSource: mockRemoteDataSource,
        localDataSource: mockLocalDataSource,
        networkInfo: mockNetworkInfo,
      );
    });

    test('should return products from remote when online', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.getProducts())
          .thenAnswer((_) async => const Success(sampleProducts));

      // Act
      final result = await repository.getProducts();

      // Assert
      expect(result, isA<Success<List<Product>>>());
      verify(mockLocalDataSource.cacheProducts(sampleProducts));
    });

    test('should return cached products when offline', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => false);
      when(mockLocalDataSource.getCachedProducts())
          .thenAnswer((_) async => sampleProducts);

      // Act
      final result = await repository.getProducts();

      // Assert
      expect(result, isA<Success<List<Product>>>());
      verifyNever(mockRemoteDataSource.getProducts());
    });
  });
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Result Pattern**
- [ ] إنشاء Result<T> sealed class
- [ ] تعريف أنواع أخطاء شاملة
- [ ] تطبيق دوال تحويل الأخطاء
- [ ] إضافة رسائل خطأ ودية للمستخدم

### **2. Repository Pattern**
- [ ] إنشاء واجهات المستودع
- [ ] تطبيق فئات المستودع
- [ ] إضافة تبسيط مصدر البيانات
- [ ] تطبيق استراتيجيات التخزين المؤقت

### **3. طبقة الشبكة | Network Layer**
- [ ] إعداد Dio مع interceptors
- [ ] تطبيق خدمة API
- [ ] إضافة معالجة الأخطاء
- [ ] تطبيق منطق إعادة المحاولة

### **4. التخزين المحلي | Local Storage**
- [ ] إعداد Hive للتخزين المحلي
- [ ] تطبيق مصادر البيانات المحلية
- [ ] إضافة آليات التخزين المؤقت
- [ ] معالجة سيناريوهات عدم الاتصال

### **5. معالجة الأخطاء | Error Handling**
- [ ] تطبيق أنواع أخطاء شاملة
- [ ] إضافة تسجيل ومراقبة الأخطاء
- [ ] إنشاء آليات استرداد الأخطاء
- [ ] اختبار سيناريوهات الأخطاء

---

**التبويب التالي**: طبقة المجال | Domain Layer

