# TAB 4: الإشعارات والروابط العميقة | Notifications & Deep Links

## 19. إدارة الإشعارات والروابط العميقة
### Notifications & Deep Links

---

## 🎯 **الهدف | Objective**
تطبيق نظام إشعارات شامل ووظائف الروابط العميقة لتطبيق Flutter للتجارة الإلكترونية.

## 📋 **Rule | القاعدة**
**Arabic**: جدول روابط عميقة وإشعارات + معالجة المعلمات + سلوك عند فقدان المعلمات  
**English**: Deep links and notifications table + parameter handling + behavior when parameters missing

## 💡 **Benefits | الفوائد**
- **User Engagement | تفاعل المستخدم**: Keep users engaged with notifications
- **Seamless Navigation | تنقل سلس**: Direct users to specific content
- **Marketing | التسويق**: Promote products and offers effectively
- **User Experience | تجربة المستخدم**: Smooth app experience with deep links
- **Retention | الاحتفاظ**: Increase user retention with notifications
- **Conversion | التحويل**: Drive conversions with targeted notifications

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع ميزات التفاعل والتنقل للمستخدم
- **كيفية التطبيق**:
  - إعداد خدمة الإشعارات الفورية
  - تطبيق نظام الروابط العميقة
  - إنشاء قوالب الإشعارات
  - إضافة توجيه الروابط العميقة
  - تطبيق جدولة الإشعارات
- **النتيجة**: نظام إشعارات وروابط عميقة شامل

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بالإشعارات والروابط العميقة | Notifications & Deep Links Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد خدمة الإشعارات الفورية
- **🔴 حرج**: تطبيق نظام الروابط العميقة
- **🟠 عالي**: إنشاء قوالب الإشعارات

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إضافة توجيه الروابط العميقة ومعالجة المعلمات
- **🟠 عالي**: تطبيق جدولة الإشعارات
- **🟡 متوسط**: إضافة ميزات إشعارات متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تخصيص إشعارات متقدم
- **🟡 متوسط**: تحسين إشعارات مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: توقيت إشعارات تنبؤي

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بالإشعارات والروابط العميقة | Notifications & Deep Links Specific Metrics:**
- **تسليم الإشعارات | Notification Delivery**: >95% delivery rate
- **نجاح الروابط العميقة | Deep Link Success**: >98% successful deep links
- **تفاعل المستخدم | User Engagement**: >70% notification open rate
- **معدل التحويل | Conversion Rate**: >15% conversion from notifications
- **التحقق من المعلمات | Parameter Validation**: 100% parameter validation
- **معالجة الأخطاء | Error Handling**: <2% deep link errors

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بالإشعارات والروابط العميقة | Notifications & Deep Links Specific Pitfalls:**
- **تجنب | Avoid**: عدم وجود التحقق من المعلمات
- **تجنب | Avoid**: معالجة أخطاء الروابط العميقة ضعيفة
- **تجنب | Avoid**: تخصيص إشعارات غير كافي
- **تجنب | Avoid**: عدم وجود جدولة الإشعارات
- **تجنب | Avoid**: توجيه الروابط العميقة ضعيف

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: التحقق من المعلمات شامل
- **استخدم | Use**: معالجة أخطاء الروابط العميقة قوية
- **استخدم | Use**: محتوى إشعارات مخصص
- **استخدم | Use**: جدولة إشعارات ذكية
- **استخدم | Use**: توجيه روابط عميقة موثوق

## 🔔 **Push Notifications | الإشعارات الفورية**

### **1. Notification Service | خدمة الإشعارات**
```dart
// lib/core/notifications/notification_service.dart
class NotificationService {
  static final FirebaseMessaging _messaging = FirebaseMessaging.instance;
  
  static Future<void> initialize() async {
    // Request permission
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );
    
    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      // Get FCM token
      final token = await _messaging.getToken();
      await _saveToken(token);
      
      // Set up message handlers
      _setupMessageHandlers();
    }
  }
  
  static Future<void> _saveToken(String? token) async {
    if (token != null) {
      await SecureStorageService.storeToken('fcm_token', token);
      
      // Send token to server
      await _sendTokenToServer(token);
    }
  }
  
  static Future<void> _sendTokenToServer(String token) async {
    try {
      final dio = await DioClient.instance;
      await dio.post('/notifications/token', data: {
        'token': token,
        'platform': Platform.isAndroid ? 'android' : 'ios',
        'user_id': await _getCurrentUserId(),
      });
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'send_fcm_token');
    }
  }
  
  static void _setupMessageHandlers() {
    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);
    
    // Handle background messages
    FirebaseMessaging.onBackgroundMessage(_handleBackgroundMessage);
    
    // Handle notification taps
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);
  }
  
  static Future<void> _handleForegroundMessage(RemoteMessage message) async {
    // Show in-app notification
    await _showInAppNotification(message);
  }
  
  static Future<void> _handleBackgroundMessage(RemoteMessage message) async {
    // Handle background message
    await _processBackgroundMessage(message);
  }
  
  static Future<void> _handleNotificationTap(RemoteMessage message) async {
    // Handle notification tap
    await _processNotificationTap(message);
  }
  
  static Future<void> _showInAppNotification(RemoteMessage message) async {
    // Show in-app notification
    final notification = NotificationData.fromRemoteMessage(message);
    await InAppNotificationService.show(notification);
  }
  
  static Future<void> _processBackgroundMessage(RemoteMessage message) async {
    // Process background message
    final notification = NotificationData.fromRemoteMessage(message);
    await NotificationProcessor.process(notification);
  }
  
  static Future<void> _processNotificationTap(RemoteMessage message) async {
    // Process notification tap
    final notification = NotificationData.fromRemoteMessage(message);
    await DeepLinkService.handleNotification(notification);
  }
  
  static Future<String?> _getCurrentUserId() async {
    // Get current user ID
    return await SecureStorageService.getToken('user_id');
  }
}
```

### **2. Notification Data | بيانات الإشعار**
```dart
// lib/core/notifications/notification_data.dart
class NotificationData {
  final String id;
  final String title;
  final String body;
  final String? imageUrl;
  final Map<String, dynamic>? data;
  final NotificationType type;
  final DateTime timestamp;
  
  NotificationData({
    required this.id,
    required this.title,
    required this.body,
    this.imageUrl,
    this.data,
    required this.type,
    required this.timestamp,
  });
  
  factory NotificationData.fromRemoteMessage(RemoteMessage message) {
    return NotificationData(
      id: message.messageId ?? '',
      title: message.notification?.title ?? '',
      body: message.notification?.body ?? '',
      imageUrl: message.notification?.android?.imageUrl,
      data: message.data,
      type: _parseNotificationType(message.data['type']),
      timestamp: DateTime.now(),
    );
  }
  
  static NotificationType _parseNotificationType(String? type) {
    switch (type) {
      case 'product':
        return NotificationType.product;
      case 'order':
        return NotificationType.order;
      case 'promotion':
        return NotificationType.promotion;
      case 'general':
        return NotificationType.general;
      default:
        return NotificationType.general;
    }
  }
}

enum NotificationType {
  product,
  order,
  promotion,
  general,
}
```

## 🔗 **Deep Links | الروابط العميقة**

### **1. Deep Link Service | خدمة الروابط العميقة**
```dart
// lib/core/deep_links/deep_link_service.dart
class DeepLinkService {
  static final Map<String, DeepLinkHandler> _handlers = {};
  
  static void initialize() {
    _registerHandlers();
    _setupLinkStreams();
  }
  
  static void _registerHandlers() {
    _handlers['product'] = ProductDeepLinkHandler();
    _handlers['order'] = OrderDeepLinkHandler();
    _handlers['category'] = CategoryDeepLinkHandler();
    _handlers['promotion'] = PromotionDeepLinkHandler();
    _handlers['profile'] = ProfileDeepLinkHandler();
  }
  
  static void _setupLinkStreams() {
    // Handle app links
    FirebaseDynamicLinks.instance.onLink.listen(_handleDynamicLink);
    
    // Handle initial link
    FirebaseDynamicLinks.instance.getInitialLink().then(_handleDynamicLink);
  }
  
  static Future<void> _handleDynamicLink(PendingDynamicLinkData? data) async {
    if (data?.link != null) {
      await handleDeepLink(data!.link.toString());
    }
  }
  
  static Future<void> handleDeepLink(String link) async {
    try {
      final uri = Uri.parse(link);
      final path = uri.path;
      final segments = path.split('/').where((s) => s.isNotEmpty).toList();
      
      if (segments.isEmpty) {
        await _handleHomeLink();
        return;
      }
      
      final handlerType = segments[0];
      final handler = _handlers[handlerType];
      
      if (handler != null) {
        await handler.handle(segments, uri.queryParameters);
      } else {
        await _handleUnknownLink(link);
      }
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'deep_link_handling');
    }
  }
  
  static Future<void> _handleHomeLink() async {
    AppRouter.router.go('/');
  }
  
  static Future<void> _handleUnknownLink(String link) async {
    // Handle unknown deep link
    AppRouter.router.go('/');
  }
  
  static Future<void> handleNotification(NotificationData notification) async {
    if (notification.data != null) {
      final link = notification.data!['deep_link'];
      if (link != null) {
        await handleDeepLink(link);
      }
    }
  }
}
```

### **2. Deep Link Handlers | معالجات الروابط العميقة**
```dart
// lib/core/deep_links/handlers/product_deep_link_handler.dart
class ProductDeepLinkHandler implements DeepLinkHandler {
  @override
  Future<void> handle(List<String> segments, Map<String, String> parameters) async {
    if (segments.length < 2) {
      await _handleMissingProductId();
      return;
    }
    
    final productId = segments[1];
    
    if (productId.isEmpty) {
      await _handleMissingProductId();
      return;
    }
    
    // Validate product ID
    if (!_isValidProductId(productId)) {
      await _handleInvalidProductId(productId);
      return;
    }
    
    // Navigate to product page
    AppRouter.router.go('/products/$productId');
  }
  
  Future<void> _handleMissingProductId() async {
    // Handle missing product ID
    AppRouter.router.go('/products');
  }
  
  Future<void> _handleInvalidProductId(String productId) async {
    // Handle invalid product ID
    AppRouter.router.go('/products');
  }
  
  bool _isValidProductId(String productId) {
    // Validate product ID format
    return productId.isNotEmpty && productId.length > 0;
  }
}

// lib/core/deep_links/handlers/order_deep_link_handler.dart
class OrderDeepLinkHandler implements DeepLinkHandler {
  @override
  Future<void> handle(List<String> segments, Map<String, String> parameters) async {
    if (segments.length < 2) {
      await _handleMissingOrderId();
      return;
    }
    
    final orderId = segments[1];
    
    if (orderId.isEmpty) {
      await _handleMissingOrderId();
      return;
    }
    
    // Validate order ID
    if (!_isValidOrderId(orderId)) {
      await _handleInvalidOrderId(orderId);
      return;
    }
    
    // Navigate to order page
    AppRouter.router.go('/orders/$orderId');
  }
  
  Future<void> _handleMissingOrderId() async {
    // Handle missing order ID
    AppRouter.router.go('/orders');
  }
  
  Future<void> _handleInvalidOrderId(String orderId) async {
    // Handle invalid order ID
    AppRouter.router.go('/orders');
  }
  
  bool _isValidOrderId(String orderId) {
    // Validate order ID format
    return orderId.isNotEmpty && orderId.length > 0;
  }
}

abstract class DeepLinkHandler {
  Future<void> handle(List<String> segments, Map<String, String> parameters);
}
```

## 📋 **Deep Link Table | جدول الروابط العميقة**

### **1. Deep Link Configuration | تكوين الروابط العميقة**
```dart
// lib/core/deep_links/deep_link_config.dart
class DeepLinkConfig {
  static const Map<String, DeepLinkInfo> deepLinkMap = {
    'product': DeepLinkInfo(
      pattern: '/product/{id}',
      requiredParams: ['id'],
      optionalParams: [],
      fallbackRoute: '/products',
      validation: ProductValidation(),
    ),
    'order': DeepLinkInfo(
      pattern: '/order/{id}',
      requiredParams: ['id'],
      optionalParams: [],
      fallbackRoute: '/orders',
      validation: OrderValidation(),
    ),
    'category': DeepLinkInfo(
      pattern: '/category/{id}',
      requiredParams: ['id'],
      optionalParams: ['page', 'sort'],
      fallbackRoute: '/products',
      validation: CategoryValidation(),
    ),
    'promotion': DeepLinkInfo(
      pattern: '/promotion/{id}',
      requiredParams: ['id'],
      optionalParams: [],
      fallbackRoute: '/promotions',
      validation: PromotionValidation(),
    ),
    'profile': DeepLinkInfo(
      pattern: '/profile/{section}',
      requiredParams: ['section'],
      optionalParams: [],
      fallbackRoute: '/profile',
      validation: ProfileValidation(),
    ),
  };
}

class DeepLinkInfo {
  final String pattern;
  final List<String> requiredParams;
  final List<String> optionalParams;
  final String fallbackRoute;
  final DeepLinkValidation validation;
  
  DeepLinkInfo({
    required this.pattern,
    required this.requiredParams,
    required this.optionalParams,
    required this.fallbackRoute,
    required this.validation,
  });
}

abstract class DeepLinkValidation {
  bool validate(String value);
}

class ProductValidation implements DeepLinkValidation {
  @override
  bool validate(String value) {
    return value.isNotEmpty && value.length > 0;
  }
}

class OrderValidation implements DeepLinkValidation {
  @override
  bool validate(String value) {
    return value.isNotEmpty && value.length > 0;
  }
}

class CategoryValidation implements DeepLinkValidation {
  @override
  bool validate(String value) {
    return value.isNotEmpty && value.length > 0;
  }
}

class PromotionValidation implements DeepLinkValidation {
  @override
  bool validate(String value) {
    return value.isNotEmpty && value.length > 0;
  }
}

class ProfileValidation implements DeepLinkValidation {
  @override
  bool validate(String value) {
    return ['settings', 'orders', 'favorites', 'addresses'].contains(value);
  }
}
```

## 📅 **Notification Scheduling | جدولة الإشعارات**

### **1. Notification Scheduler | مجدول الإشعارات**
```dart
// lib/core/notifications/notification_scheduler.dart
class NotificationScheduler {
  static Future<void> scheduleNotification({
    required String title,
    required String body,
    required DateTime scheduledTime,
    required NotificationType type,
    Map<String, dynamic>? data,
  }) async {
    try {
      final notification = NotificationData(
        id: _generateNotificationId(),
        title: title,
        body: body,
        data: data,
        type: type,
        timestamp: scheduledTime,
      );
      
      await _scheduleLocalNotification(notification);
      await _scheduleServerNotification(notification);
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'notification_scheduling');
    }
  }
  
  static Future<void> _scheduleLocalNotification(NotificationData notification) async {
    // Schedule local notification
    await LocalNotificationService.schedule(
      notification.id,
      notification.title,
      notification.body,
      notification.timestamp,
    );
  }
  
  static Future<void> _scheduleServerNotification(NotificationData notification) async {
    // Schedule server notification
    final dio = await DioClient.instance;
    await dio.post('/notifications/schedule', data: {
      'notification': notification.toJson(),
    });
  }
  
  static String _generateNotificationId() {
    return 'notification_${DateTime.now().millisecondsSinceEpoch}';
  }
}
```

### **2. Notification Templates | قوالب الإشعارات**
```dart
// lib/core/notifications/notification_templates.dart
class NotificationTemplates {
  static NotificationTemplate getProductNotification({
    required String productName,
    required String productId,
    required double discount,
  }) {
    return NotificationTemplate(
      title: 'خصم خاص على $productName',
      body: 'احصل على خصم ${discount.toStringAsFixed(0)}% على $productName',
      type: NotificationType.product,
      data: {
        'product_id': productId,
        'discount': discount,
        'deep_link': '/product/$productId',
      },
    );
  }
  
  static NotificationTemplate getOrderNotification({
    required String orderId,
    required String status,
  }) {
    return NotificationTemplate(
      title: 'تحديث حالة الطلب',
      body: 'تم تحديث حالة طلبك #$orderId إلى $status',
      type: NotificationType.order,
      data: {
        'order_id': orderId,
        'status': status,
        'deep_link': '/order/$orderId',
      },
    );
  }
  
  static NotificationTemplate getPromotionNotification({
    required String promotionTitle,
    required String promotionId,
    required DateTime expiryDate,
  }) {
    return NotificationTemplate(
      title: 'عرض محدود',
      body: '$promotionTitle - ينتهي في ${expiryDate.toString().split(' ')[0]}',
      type: NotificationType.promotion,
      data: {
        'promotion_id': promotionId,
        'expiry_date': expiryDate.toIso8601String(),
        'deep_link': '/promotion/$promotionId',
      },
    );
  }
}

class NotificationTemplate {
  final String title;
  final String body;
  final NotificationType type;
  final Map<String, dynamic> data;
  
  NotificationTemplate({
    required this.title,
    required this.body,
    required this.type,
    required this.data,
  });
}
```

## 📊 **Notification Analytics | تحليلات الإشعارات**

### **1. Notification Analytics | تحليلات الإشعارات**
```dart
// lib/core/notifications/notification_analytics.dart
class NotificationAnalytics {
  static Future<void> trackNotificationSent(NotificationData notification) async {
    await AnalyticsService.logEvent('notification_sent', {
      'notification_id': notification.id,
      'notification_type': notification.type.name,
      'title': notification.title,
      'timestamp': notification.timestamp.toIso8601String(),
    });
  }
  
  static Future<void> trackNotificationOpened(NotificationData notification) async {
    await AnalyticsService.logEvent('notification_opened', {
      'notification_id': notification.id,
      'notification_type': notification.type.name,
      'title': notification.title,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackNotificationDismissed(NotificationData notification) async {
    await AnalyticsService.logEvent('notification_dismissed', {
      'notification_id': notification.id,
      'notification_type': notification.type.name,
      'title': notification.title,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackDeepLinkOpened(String deepLink) async {
    await AnalyticsService.logEvent('deep_link_opened', {
      'deep_link': deepLink,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackDeepLinkError(String deepLink, String error) async {
    await AnalyticsService.logEvent('deep_link_error', {
      'deep_link': deepLink,
      'error': error,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. الإشعارات الفورية | Push Notifications**
- [ ] إعداد Firebase Cloud Messaging
- [ ] تطبيق خدمة الإشعارات
- [ ] إضافة قوالب الإشعارات
- [ ] اختبار تسليم الإشعارات

### **2. الروابط العميقة | Deep Links**
- [ ] إعداد خدمة الروابط العميقة
- [ ] تطبيق معالجات الروابط العميقة
- [ ] إضافة التحقق من المعلمات
- [ ] اختبار توجيه الروابط العميقة

### **3. جدولة الإشعارات | Notification Scheduling**
- [ ] تطبيق مجدول الإشعارات
- [ ] إضافة قوالب الإشعارات
- [ ] إعداد جدولة الإشعارات
- [ ] اختبار توقيت الإشعارات

### **4. التحليلات | Analytics**
- [ ] إضافة تحليلات الإشعارات
- [ ] تطبيق تحليلات الروابط العميقة
- [ ] إعداد تتبع التحليلات
- [ ] اختبار تقارير التحليلات

### **5. معالجة الأخطاء | Error Handling**
- [ ] إضافة معالجة أخطاء الإشعارات
- [ ] تطبيق معالجة أخطاء الروابط العميقة
- [ ] إضافة آليات الاحتياط
- [ ] اختبار سيناريوهات الأخطاء

---

**Next Tab**: Business Analytics | التحليلات التجارية
