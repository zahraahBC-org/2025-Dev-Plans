# TAB 2: كتالوج الأخطاء | Error Catalog

## 17. كتالوج الأخطاء الشامل
### Error Catalog

---

## 🎯 **الهدف | Objective**
إنشاء كتالوج أخطاء شامل مع خريطة أخطاء موحدة ورسائل ودية للمستخدم واستراتيجيات معالجة أخطاء مناسبة لتطبيق Flutter للتجارة الإلكترونية.

## 📋 **القاعدة | Rule**
**العربية**: خريطة أخطاء موحّدة تربط HTTP codes → error_code → رسالة مترجمة  
**English**: Unified error map linking HTTP codes → error_code → translated message

## 💡 **الفوائد | Benefits**
- **تجربة مستخدم متسقة | Consistent UX**: رسائل خطأ موحدة عبر جميع الشاشات
- **سهولة الصيانة | Easy Maintenance**: إدارة أخطاء مركزية
- **تصحيح أفضل | Better Debugging**: تصنيف أخطاء واضح وتسجيل
- **صديق للمستخدم | User-Friendly**: رسائل خطأ واضحة وقابلة للتنفيذ
- **تجربة المطور | Developer Experience**: سهولة فهم ومعالجة الأخطاء
- **التعدد اللغوي | Internationalization**: ترجمة رسائل خطأ مناسبة

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع معالجة الأخطاء عبر التطبيق
- **كيفية التطبيق**:
  - إنشاء جدول خريطة أخطاء شامل
  - تطبيق توحيد رموز الأخطاء
  - إضافة ترجمة رسائل ودية للمستخدم
  - إنشاء استراتيجيات استرداد الأخطاء
  - إضافة تسجيل ومراقبة الأخطاء
- **النتيجة**: نظام معالجة أخطاء متسق وودود للمستخدم

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بكتالوج الأخطاء | Error Catalog Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إنشاء جدول خريطة أخطاء شامل
- **🔴 حرج**: تطبيق توحيد رموز الأخطاء
- **🟠 عالي**: إضافة ترجمة رسائل ودية للمستخدم

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تطبيق استراتيجيات استرداد الأخطاء
- **🟠 عالي**: إضافة تسجيل ومراقبة الأخطاء
- **🟡 متوسط**: إضافة ميزات معالجة أخطاء متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تحليلات ورؤى أخطاء متقدمة
- **🟡 متوسط**: التنبؤ بالأخطاء مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: منع الأخطاء التنبؤي

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بكتالوج الأخطاء | Error Catalog Specific Metrics:**
- **تغطية الأخطاء | Error Coverage**: 100% error types mapped
- **ترجمة الرسائل | Message Translation**: 100% messages translated
- **استرداد الأخطاء | Error Recovery**: >90% successful error recovery
- **رضا المستخدم | User Satisfaction**: >95% user satisfaction with error messages
- **إنتاجية المطور | Developer Productivity**: 50%+ faster error handling
- **حل الأخطاء | Error Resolution**: <5 minutes average resolution time

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بكتالوج الأخطاء | Error Catalog Specific Pitfalls:**
- **تجنب | Avoid**: رسائل خطأ غير متسقة عبر الشاشات
- **تجنب | Avoid**: عرض رسائل خطأ تقنية للمستخدمين
- **تجنب | Avoid**: عدم وجود استراتيجيات استرداد الأخطاء
- **تجنب | Avoid**: تصنيف أخطاء ضعيف
- **تجنب | Avoid**: تسجيل أخطاء غير كافي

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: خريطة وتصنيف أخطاء موحد
- **استخدم | Use**: رسائل خطأ ودية وقابلة للتنفيذ
- **استخدم | Use**: استراتيجيات استرداد أخطاء شاملة
- **استخدم | Use**: تسجيل ومراقبة أخطاء مناسبة
- **استخدم | Use**: أنماط معالجة أخطاء متسقة

## 📋 **Error Mapping Table | جدول ربط الأخطاء**

### **1. HTTP Status Codes | رموز حالة HTTP**
```dart
// lib/core/error/error_mapping.dart
class ErrorMapping {
  static const Map<int, ErrorInfo> httpErrorMap = {
    // 4xx Client Errors
    400: ErrorInfo(
      code: 'BAD_REQUEST',
      category: ErrorCategory.client,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Invalid request. Please check your input and try again.',
        'ar': 'طلب غير صحيح. يرجى التحقق من المدخلات والمحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    401: ErrorInfo(
      code: 'UNAUTHORIZED',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Please log in to continue.',
        'ar': 'يرجى تسجيل الدخول للمتابعة.',
      },
      recoveryAction: RecoveryAction.login,
    ),
    403: ErrorInfo(
      code: 'FORBIDDEN',
      category: ErrorCategory.authorization,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'You don\'t have permission to access this resource.',
        'ar': 'ليس لديك صلاحية للوصول إلى هذا المورد.',
      },
      recoveryAction: RecoveryAction.contactSupport,
    ),
    404: ErrorInfo(
      code: 'NOT_FOUND',
      category: ErrorCategory.resource,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'The requested resource was not found.',
        'ar': 'المورد المطلوب غير موجود.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    409: ErrorInfo(
      code: 'CONFLICT',
      category: ErrorCategory.business,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'The request conflicts with the current state.',
        'ar': 'الطلب يتعارض مع الحالة الحالية.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    422: ErrorInfo(
      code: 'UNPROCESSABLE_ENTITY',
      category: ErrorCategory.validation,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Please check your input and try again.',
        'ar': 'يرجى التحقق من المدخلات والمحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    429: ErrorInfo(
      code: 'TOO_MANY_REQUESTS',
      category: ErrorCategory.rateLimit,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Too many requests. Please wait a moment and try again.',
        'ar': 'طلبات كثيرة جداً. يرجى الانتظار قليلاً والمحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.waitAndRetry,
    ),
    
    // 5xx Server Errors
    500: ErrorInfo(
      code: 'INTERNAL_SERVER_ERROR',
      category: ErrorCategory.server,
      severity: ErrorSeverity.critical,
      userMessage: {
        'en': 'Something went wrong. Please try again later.',
        'ar': 'حدث خطأ ما. يرجى المحاولة لاحقاً.',
      },
      recoveryAction: RecoveryAction.retryLater,
    ),
    502: ErrorInfo(
      code: 'BAD_GATEWAY',
      category: ErrorCategory.server,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Service temporarily unavailable. Please try again later.',
        'ar': 'الخدمة غير متاحة مؤقتاً. يرجى المحاولة لاحقاً.',
      },
      recoveryAction: RecoveryAction.retryLater,
    ),
    503: ErrorInfo(
      code: 'SERVICE_UNAVAILABLE',
      category: ErrorCategory.server,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Service temporarily unavailable. Please try again later.',
        'ar': 'الخدمة غير متاحة مؤقتاً. يرجى المحاولة لاحقاً.',
      },
      recoveryAction: RecoveryAction.retryLater,
    ),
    504: ErrorInfo(
      code: 'GATEWAY_TIMEOUT',
      category: ErrorCategory.server,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Request timeout. Please try again.',
        'ar': 'انتهت مهلة الطلب. يرجى المحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
  };
}
```

### **2. Error Information Structure | هيكل معلومات الخطأ**
```dart
// lib/core/error/error_info.dart
class ErrorInfo {
  final String code;
  final ErrorCategory category;
  final ErrorSeverity severity;
  final Map<String, String> userMessage;
  final RecoveryAction recoveryAction;
  final String? technicalMessage;
  final Map<String, dynamic>? metadata;
  
  const ErrorInfo({
    required this.code,
    required this.category,
    required this.severity,
    required this.userMessage,
    required this.recoveryAction,
    this.technicalMessage,
    this.metadata,
  });
}

enum ErrorCategory {
  client,
  server,
  network,
  authentication,
  authorization,
  validation,
  business,
  resource,
  rateLimit,
  unknown,
}

enum ErrorSeverity {
  low,
  medium,
  high,
  critical,
}

enum RecoveryAction {
  retry,
  retryLater,
  waitAndRetry,
  login,
  contactSupport,
  refresh,
  clearCache,
  none,
}
```

## 🌐 **Network Errors | أخطاء الشبكة**

### **1. Network Error Mapping | ربط أخطاء الشبكة**
```dart
// lib/core/error/network_error_mapping.dart
class NetworkErrorMapping {
  static const Map<String, ErrorInfo> networkErrorMap = {
    'CONNECTION_TIMEOUT': ErrorInfo(
      code: 'CONNECTION_TIMEOUT',
      category: ErrorCategory.network,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Connection timeout. Please check your internet connection.',
        'ar': 'انتهت مهلة الاتصال. يرجى التحقق من اتصال الإنترنت.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'SEND_TIMEOUT': ErrorInfo(
      code: 'SEND_TIMEOUT',
      category: ErrorCategory.network,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Request timeout. Please try again.',
        'ar': 'انتهت مهلة الطلب. يرجى المحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'RECEIVE_TIMEOUT': ErrorInfo(
      code: 'RECEIVE_TIMEOUT',
      category: ErrorCategory.network,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Response timeout. Please try again.',
        'ar': 'انتهت مهلة الاستجابة. يرجى المحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'CONNECTION_ERROR': ErrorInfo(
      code: 'CONNECTION_ERROR',
      category: ErrorCategory.network,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'No internet connection. Please check your network settings.',
        'ar': 'لا يوجد اتصال بالإنترنت. يرجى التحقق من إعدادات الشبكة.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'CANCEL': ErrorInfo(
      code: 'REQUEST_CANCELLED',
      category: ErrorCategory.network,
      severity: ErrorSeverity.low,
      userMessage: {
        'en': 'Request was cancelled.',
        'ar': 'تم إلغاء الطلب.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
  };
}
```

### **2. Dio Error Mapping | ربط أخطاء Dio**
```dart
// lib/core/error/dio_error_mapping.dart
class DioErrorMapping {
  static ErrorInfo mapDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
        return NetworkErrorMapping.networkErrorMap['CONNECTION_TIMEOUT']!;
      case DioExceptionType.sendTimeout:
        return NetworkErrorMapping.networkErrorMap['SEND_TIMEOUT']!;
      case DioExceptionType.receiveTimeout:
        return NetworkErrorMapping.networkErrorMap['RECEIVE_TIMEOUT']!;
      case DioExceptionType.badResponse:
        return ErrorMapping.httpErrorMap[error.response?.statusCode] ??
            ErrorMapping.httpErrorMap[500]!;
      case DioExceptionType.cancel:
        return NetworkErrorMapping.networkErrorMap['CANCEL']!;
      case DioExceptionType.connectionError:
        return NetworkErrorMapping.networkErrorMap['CONNECTION_ERROR']!;
      default:
        return ErrorMapping.httpErrorMap[500]!;
    }
  }
}
```

## 🔐 **Authentication Errors | أخطاء المصادقة**

### **1. Auth Error Mapping | ربط أخطاء المصادقة**
```dart
// lib/core/error/auth_error_mapping.dart
class AuthErrorMapping {
  static const Map<String, ErrorInfo> authErrorMap = {
    'INVALID_CREDENTIALS': ErrorInfo(
      code: 'INVALID_CREDENTIALS',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Invalid email or password. Please try again.',
        'ar': 'بريد إلكتروني أو كلمة مرور غير صحيحة. يرجى المحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'ACCOUNT_LOCKED': ErrorInfo(
      code: 'ACCOUNT_LOCKED',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Your account has been locked. Please contact support.',
        'ar': 'تم قفل حسابك. يرجى الاتصال بالدعم.',
      },
      recoveryAction: RecoveryAction.contactSupport,
    ),
    'ACCOUNT_NOT_VERIFIED': ErrorInfo(
      code: 'ACCOUNT_NOT_VERIFIED',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Please verify your email address to continue.',
        'ar': 'يرجى التحقق من عنوان بريدك الإلكتروني للمتابعة.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'TOKEN_EXPIRED': ErrorInfo(
      code: 'TOKEN_EXPIRED',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Your session has expired. Please log in again.',
        'ar': 'انتهت صلاحية جلستك. يرجى تسجيل الدخول مرة أخرى.',
      },
      recoveryAction: RecoveryAction.login,
    ),
    'TOKEN_INVALID': ErrorInfo(
      code: 'TOKEN_INVALID',
      category: ErrorCategory.authentication,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Invalid session. Please log in again.',
        'ar': 'جلسة غير صحيحة. يرجى تسجيل الدخول مرة أخرى.',
      },
      recoveryAction: RecoveryAction.login,
    ),
  };
}
```

## 🛒 **Business Logic Errors | أخطاء منطق الأعمال**

### **1. E-commerce Error Mapping | ربط أخطاء التجارة الإلكترونية**
```dart
// lib/core/error/business_error_mapping.dart
class BusinessErrorMapping {
  static const Map<String, ErrorInfo> businessErrorMap = {
    'PRODUCT_NOT_AVAILABLE': ErrorInfo(
      code: 'PRODUCT_NOT_AVAILABLE',
      category: ErrorCategory.business,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'This product is currently out of stock.',
        'ar': 'هذا المنتج غير متوفر حالياً.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'INSUFFICIENT_STOCK': ErrorInfo(
      code: 'INSUFFICIENT_STOCK',
      category: ErrorCategory.business,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Insufficient stock. Please reduce quantity and try again.',
        'ar': 'مخزون غير كافي. يرجى تقليل الكمية والمحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'CART_EMPTY': ErrorInfo(
      code: 'CART_EMPTY',
      category: ErrorCategory.business,
      severity: ErrorSeverity.low,
      userMessage: {
        'en': 'Your cart is empty. Add some items to continue.',
        'ar': 'سلتك فارغة. أضف بعض العناصر للمتابعة.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'PAYMENT_FAILED': ErrorInfo(
      code: 'PAYMENT_FAILED',
      category: ErrorCategory.business,
      severity: ErrorSeverity.high,
      userMessage: {
        'en': 'Payment failed. Please check your payment method and try again.',
        'ar': 'فشل الدفع. يرجى التحقق من طريقة الدفع والمحاولة مرة أخرى.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
    'ORDER_NOT_FOUND': ErrorInfo(
      code: 'ORDER_NOT_FOUND',
      category: ErrorCategory.business,
      severity: ErrorSeverity.medium,
      userMessage: {
        'en': 'Order not found. Please check your order number.',
        'ar': 'الطلب غير موجود. يرجى التحقق من رقم الطلب.',
      },
      recoveryAction: RecoveryAction.retry,
    ),
  };
}
```

## 🔧 **Error Handler | معالج الأخطاء**

### **1. Unified Error Handler | معالج الأخطاء الموحد**
```dart
// lib/core/error/unified_error_handler.dart
class UnifiedErrorHandler {
  static ErrorInfo handleError(dynamic error) {
    if (error is DioException) {
      return DioErrorMapping.mapDioError(error);
    }
    
    if (error is AuthException) {
      return AuthErrorMapping.authErrorMap[error.code] ??
          ErrorMapping.httpErrorMap[401]!;
    }
    
    if (error is BusinessException) {
      return BusinessErrorMapping.businessErrorMap[error.code] ??
          ErrorMapping.httpErrorMap[400]!;
    }
    
    if (error is ValidationException) {
      return ErrorMapping.httpErrorMap[422]!;
    }
    
    // Default error
    return ErrorMapping.httpErrorMap[500]!;
  }
  
  static String getUserMessage(ErrorInfo errorInfo, String locale) {
    return errorInfo.userMessage[locale] ?? 
           errorInfo.userMessage['en'] ?? 
           'An error occurred. Please try again.';
  }
  
  static String getTechnicalMessage(ErrorInfo errorInfo) {
    return errorInfo.technicalMessage ?? 
           'Technical error: ${errorInfo.code}';
  }
}
```

### **2. Error Recovery | استرداد الأخطاء**
```dart
// lib/core/error/error_recovery.dart
class ErrorRecovery {
  static Future<void> executeRecoveryAction(
    RecoveryAction action,
    BuildContext context,
  ) async {
    switch (action) {
      case RecoveryAction.retry:
        // Retry the failed operation
        break;
      case RecoveryAction.retryLater:
        // Show retry later message
        _showRetryLaterMessage(context);
        break;
      case RecoveryAction.waitAndRetry:
        // Wait and retry
        await Future.delayed(const Duration(seconds: 5));
        break;
      case RecoveryAction.login:
        // Navigate to login
        AppRouter.router.go('/login');
        break;
      case RecoveryAction.contactSupport:
        // Show contact support dialog
        _showContactSupportDialog(context);
        break;
      case RecoveryAction.refresh:
        // Refresh the current screen
        break;
      case RecoveryAction.clearCache:
        // Clear app cache
        await CacheService.deletePattern('*');
        break;
      case RecoveryAction.none:
        // No action required
        break;
    }
  }
  
  static void _showRetryLaterMessage(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Please try again later'),
      ),
    );
  }
  
  static void _showContactSupportDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Contact Support'),
        content: const Text('Please contact our support team for assistance.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}
```

## 📊 **Error Analytics | تحليلات الأخطاء**

### **1. Error Tracking | تتبع الأخطاء**
```dart
// lib/core/error/error_analytics.dart
class ErrorAnalytics {
  static Future<void> trackError(ErrorInfo errorInfo, {
    String? context,
    Map<String, dynamic>? metadata,
  }) async {
    // Log error to analytics
    await AnalyticsService.logEvent('error_occurred', {
      'error_code': errorInfo.code,
      'error_category': errorInfo.category.name,
      'error_severity': errorInfo.severity.name,
      'context': context ?? 'unknown',
      'metadata': metadata ?? {},
    });
    
    // Send to crash reporting
    await CrashlyticsService.recordError(
      errorInfo.code,
      null,
      reason: context,
      fatal: errorInfo.severity == ErrorSeverity.critical,
    );
  }
  
  static Future<void> trackErrorRecovery(
    String errorCode,
    RecoveryAction action,
    bool success,
  ) async {
    await AnalyticsService.logEvent('error_recovery', {
      'error_code': errorCode,
      'recovery_action': action.name,
      'success': success,
    });
  }
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. خريطة الأخطاء | Error Mapping**
- [ ] إنشاء جدول خريطة أخطاء شامل
- [ ] ربط رموز حالة HTTP برموز الأخطاء
- [ ] إضافة خريطة أخطاء الشبكة
- [ ] إضافة خريطة أخطاء المصادقة

### **2. رسائل الأخطاء | Error Messages**
- [ ] إنشاء رسائل خطأ ودية للمستخدم
- [ ] إضافة ترجمات عربية وإنجليزية
- [ ] تطبيق توطين رسائل الأخطاء
- [ ] اختبار عرض رسائل الأخطاء

### **3. معالجة الأخطاء | Error Handling**
- [ ] تطبيق معالج أخطاء موحد
- [ ] إضافة استراتيجيات استرداد الأخطاء
- [ ] إنشاء إجراءات استرداد الأخطاء
- [ ] اختبار تدفق معالجة الأخطاء

### **4. تحليلات الأخطاء | Error Analytics**
- [ ] إضافة تتبع الأخطاء
- [ ] تطبيق تحليلات الأخطاء
- [ ] إعداد مراقبة الأخطاء
- [ ] اختبار تقارير الأخطاء

### **5. اختبار الأخطاء | Error Testing**
- [ ] اختبار جميع سيناريوهات الأخطاء
- [ ] التحقق من عرض رسائل الأخطاء
- [ ] اختبار إجراءات استرداد الأخطاء
- [ ] التحقق من صحة تحليلات الأخطاء

---

**Next Tab**: Performance Monitoring | مراقبة الأداء

