# TAB 1: أعلام الميزات | Feature Flags

## 21. نظام Feature Flags
### Feature Flags

---

## 🎯 **الهدف | Objective**
تطبيق نظام Feature Flags للنشر المرن للميزات واختبار A/B والنشر التدريجي في تطبيق Flutter للتجارة الإلكترونية.

## 📋 **Rule | القاعدة**
**Arabic**: Feature Flags لتفعيل/إيقاف ميزات دون إطلاق نسخة جديدة + A/B Testing + Rollout تدريجي  
**English**: Feature Flags to enable/disable features without releasing new version + A/B Testing + Gradual Rollout

## 💡 **Benefits | الفوائد**
- **Flexible Deployment | نشر مرن**: Enable/disable features without app updates
- **Risk Mitigation | تخفيف المخاطر**: Gradual feature rollouts to reduce risk
- **A/B Testing | اختبار A/B**: Test different feature versions with users
- **Quick Rollback | تراجع سريع**: Disable problematic features quickly
- **User Segmentation | تجزئة المستخدمين**: Different features for different user groups
- **Development Speed | سرعة التطوير**: Deploy features when ready, not when app is ready

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: الميزات الجديدة والوظائف التجريبية والنشر التدريجي
- **كيفية التطبيق**:
  - إعداد خدمة التكوين البعيد (Firebase Remote Config)
  - تطبيق إدارة Feature Flags
  - إضافة إطار اختبار A/B
  - إنشاء نظام النشر التدريجي
  - إضافة تحليلات Feature Flags
- **النتيجة**: نظام إدارة ميزات مرن

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بـ Feature Flags | Feature Flags Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد خدمة التكوين البعيد
- **🔴 حرج**: تطبيق إدارة Feature Flags
- **🟠 عالي**: إضافة إطار اختبار A/B

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إنشاء نظام النشر التدريجي
- **🟠 عالي**: إضافة تحليلات Feature Flags
- **🟡 متوسط**: إضافة ميزات Feature Flags متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: قدرات اختبار A/B متقدمة
- **🟡 متوسط**: تحسين ميزات مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: نشر ميزات تنبؤي

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بـ Feature Flags | Feature Flags Specific Metrics:**
- **نجاح نشر الميزات | Feature Rollout Success**: >95% successful rollouts
- **إكمال اختبار A/B | A/B Test Completion**: >90% test completion rate
- **سرعة التراجع | Rollback Speed**: <5 minutes rollback time
- **تبني الميزات | Feature Adoption**: >70% feature adoption rate
- **تجزئة المستخدم | User Segmentation**: 100% accurate segmentation
- **تحديثات التكوين | Configuration Updates**: <30 seconds update time

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بـ Feature Flags | Feature Flags Specific Pitfalls:**
- **تجنب | Avoid**: عدم وجود التحقق من Feature Flags
- **تجنب | Avoid**: تطبيق اختبار A/B ضعيف
- **تجنب | Avoid**: آليات تراجع غير كافية
- **تجنب | Avoid**: عدم وجود تحليلات Feature Flags
- **تجنب | Avoid**: تجزئة مستخدم ضعيفة

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: التحقق من Feature Flags شامل
- **استخدم | Use**: إطار اختبار A/B قوي
- **استخدم | Use**: آليات تراجع موثوقة
- **استخدم | Use**: تحليلات Feature Flags مكتملة
- **استخدم | Use**: تجزئة مستخدم دقيقة

## 🚩 **Feature Flag System | نظام Feature Flags**

### **1. Feature Flag Service | خدمة Feature Flags**
```dart
// lib/core/feature_flags/feature_flag_service.dart
class FeatureFlagService {
  static final FirebaseRemoteConfig _remoteConfig = FirebaseRemoteConfig.instance;
  static final Map<String, FeatureFlag> _flags = {};
  
  static Future<void> initialize() async {
    await _remoteConfig.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(seconds: 30),
      minimumFetchInterval: const Duration(minutes: 1),
    ));
    
    await _fetchAndActivate();
    _setupListeners();
  }
  
  static Future<void> _fetchAndActivate() async {
    try {
      await _remoteConfig.fetchAndActivate();
      _parseFlags();
    } catch (e) {
      ErrorHandler.handleError(e, null, context: 'feature_flag_fetch');
    }
  }
  
  static void _setupListeners() {
    _remoteConfig.onConfigUpdated.listen((_) {
      _fetchAndActivate();
    });
  }
  
  static void _parseFlags() {
    final config = _remoteConfig.getAll();
    
    for (final entry in config.entries) {
      if (entry.key.startsWith('feature_')) {
        final flag = FeatureFlag.fromConfig(entry.key, entry.value);
        _flags[flag.name] = flag;
      }
    }
  }
  
  static bool isEnabled(String flagName, {String? userId}) {
    final flag = _flags[flagName];
    if (flag == null) return false;
    
    return _evaluateFlag(flag, userId);
  }
  
  static String getVariant(String flagName, {String? userId}) {
    final flag = _flags[flagName];
    if (flag == null) return 'default';
    
    return _getFlagVariant(flag, userId);
  }
  
  static bool _evaluateFlag(FeatureFlag flag, String? userId) {
    // Check if flag is enabled
    if (!flag.enabled) return false;
    
    // Check rollout percentage
    if (flag.rolloutPercentage < 100) {
      final userHash = _getUserHash(userId);
      if (userHash > flag.rolloutPercentage) return false;
    }
    
    // Check user segments
    if (flag.userSegments.isNotEmpty) {
      if (!_isUserInSegments(userId, flag.userSegments)) return false;
    }
    
    return true;
  }
  
  static String _getFlagVariant(FeatureFlag flag, String? userId) {
    if (!_evaluateFlag(flag, userId)) return 'default';
    
    if (flag.variants.isEmpty) return 'enabled';
    
    final userHash = _getUserHash(userId);
    final variantIndex = userHash % flag.variants.length;
    return flag.variants[variantIndex];
  }
  
  static int _getUserHash(String? userId) {
    if (userId == null) return 0;
    return userId.hashCode.abs() % 100;
  }
  
  static bool _isUserInSegments(String? userId, List<String> segments) {
    if (userId == null) return false;
    
    // Check if user is in any of the specified segments
    for (final segment in segments) {
      if (_isUserInSegment(userId, segment)) return true;
    }
    
    return false;
  }
  
  static bool _isUserInSegment(String userId, String segment) {
    // Implement user segment logic
    switch (segment) {
      case 'premium_users':
        return _isPremiumUser(userId);
      case 'new_users':
        return _isNewUser(userId);
      case 'high_value_users':
        return _isHighValueUser(userId);
      default:
        return false;
    }
  }
  
  static bool _isPremiumUser(String userId) {
    // Check if user is premium
    return false; // Simplified implementation
  }
  
  static bool _isNewUser(String userId) {
    // Check if user is new (registered within last 30 days)
    return false; // Simplified implementation
  }
  
  static bool _isHighValueUser(String userId) {
    // Check if user is high value (total spent > $500)
    return false; // Simplified implementation
  }
}
```

### **2. Feature Flag Model | نموذج Feature Flag**
```dart
// lib/core/feature_flags/feature_flag.dart
class FeatureFlag {
  final String name;
  final bool enabled;
  final int rolloutPercentage;
  final List<String> userSegments;
  final List<String> variants;
  final Map<String, dynamic> metadata;
  final DateTime lastUpdated;
  
  FeatureFlag({
    required this.name,
    required this.enabled,
    required this.rolloutPercentage,
    required this.userSegments,
    required this.variants,
    required this.metadata,
    required this.lastUpdated,
  });
  
  factory FeatureFlag.fromConfig(String key, RemoteConfigValue value) {
    final config = json.decode(value.asString());
    
    return FeatureFlag(
      name: key.replaceFirst('feature_', ''),
      enabled: config['enabled'] ?? false,
      rolloutPercentage: config['rollout_percentage'] ?? 0,
      userSegments: List<String>.from(config['user_segments'] ?? []),
      variants: List<String>.from(config['variants'] ?? []),
      metadata: Map<String, dynamic>.from(config['metadata'] ?? {}),
      lastUpdated: DateTime.now(),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'enabled': enabled,
      'rollout_percentage': rolloutPercentage,
      'user_segments': userSegments,
      'variants': variants,
      'metadata': metadata,
      'last_updated': lastUpdated.toIso8601String(),
    };
  }
}
```

## 🧪 **A/B Testing Framework | إطار اختبار A/B**

### **1. A/B Test Service | خدمة اختبار A/B**
```dart
// lib/core/feature_flags/ab_test_service.dart
class ABTestService {
  static final Map<String, ABTest> _tests = {};
  
  static Future<void> initialize() async {
    await _loadTests();
  }
  
  static Future<void> _loadTests() async {
    // Load A/B tests from remote config
    final config = FirebaseRemoteConfig.instance.getAll();
    
    for (final entry in config.entries) {
      if (entry.key.startsWith('ab_test_')) {
        final test = ABTest.fromConfig(entry.key, entry.value);
        _tests[test.name] = test;
      }
    }
  }
  
  static String getVariant(String testName, {String? userId}) {
    final test = _tests[testName];
    if (test == null) return 'control';
    
    if (!test.isActive) return 'control';
    
    final userHash = _getUserHash(userId);
    final variantIndex = userHash % test.variants.length;
    return test.variants[variantIndex];
  }
  
  static Future<void> trackEvent(String testName, String event, {
    String? userId,
    Map<String, dynamic>? parameters,
  }) async {
    final variant = getVariant(testName, userId: userId);
    
    await FirebaseAnalyticsService.logEvent('ab_test_event', {
      'test_name': testName,
      'variant': variant,
      'event': event,
      'user_id': userId,
      'parameters': parameters ?? {},
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackConversion(String testName, String conversion, {
    String? userId,
    double? value,
  }) async {
    final variant = getVariant(testName, userId: userId);
    
    await FirebaseAnalyticsService.logEvent('ab_test_conversion', {
      'test_name': testName,
      'variant': variant,
      'conversion': conversion,
      'user_id': userId,
      'value': value,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static int _getUserHash(String? userId) {
    if (userId == null) return 0;
    return userId.hashCode.abs() % 100;
  }
}

class ABTest {
  final String name;
  final bool isActive;
  final List<String> variants;
  final String primaryMetric;
  final DateTime startDate;
  final DateTime endDate;
  final Map<String, dynamic> metadata;
  
  ABTest({
    required this.name,
    required this.isActive,
    required this.variants,
    required this.primaryMetric,
    required this.startDate,
    required this.endDate,
    required this.metadata,
  });
  
  factory ABTest.fromConfig(String key, RemoteConfigValue value) {
    final config = json.decode(value.asString());
    
    return ABTest(
      name: key.replaceFirst('ab_test_', ''),
      isActive: config['is_active'] ?? false,
      variants: List<String>.from(config['variants'] ?? []),
      primaryMetric: config['primary_metric'] ?? 'conversion',
      startDate: DateTime.parse(config['start_date'] ?? DateTime.now().toIso8601String()),
      endDate: DateTime.parse(config['end_date'] ?? DateTime.now().add(const Duration(days: 30)).toIso8601String()),
      metadata: Map<String, dynamic>.from(config['metadata'] ?? {}),
    );
  }
}
```

### **2. A/B Test Widget | عنصر اختبار A/B**
```dart
// lib/core/feature_flags/ab_test_widget.dart
class ABTestWidget extends StatelessWidget {
  final String testName;
  final Widget control;
  final Map<String, Widget> variants;
  final String? userId;
  
  const ABTestWidget({
    super.key,
    required this.testName,
    required this.control,
    required this.variants,
    this.userId,
  });
  
  @override
  Widget build(BuildContext context) {
    final variant = ABTestService.getVariant(testName, userId: userId);
    
    // Track widget view
    ABTestService.trackEvent(testName, 'widget_view', userId: userId);
    
    if (variant == 'control') {
      return control;
    }
    
    final variantWidget = variants[variant];
    if (variantWidget != null) {
      return variantWidget;
    }
    
    return control;
  }
}
```

## 📊 **Gradual Rollout System | نظام النشر التدريجي**

### **1. Rollout Manager | مدير النشر**
```dart
// lib/core/feature_flags/rollout_manager.dart
class RolloutManager {
  static Future<void> startRollout(String flagName, {
    required int initialPercentage,
    required Duration incrementInterval,
    required int incrementPercentage,
    required int maxPercentage,
  }) async {
    final rollout = Rollout(
      flagName: flagName,
      currentPercentage: initialPercentage,
      incrementInterval: incrementInterval,
      incrementPercentage: incrementPercentage,
      maxPercentage: maxPercentage,
      startDate: DateTime.now(),
      status: RolloutStatus.active,
    );
    
    await _saveRollout(rollout);
    await _scheduleRolloutIncrement(rollout);
  }
  
  static Future<void> _scheduleRolloutIncrement(Rollout rollout) async {
    Timer(rollout.incrementInterval, () async {
      await _incrementRollout(rollout);
    });
  }
  
  static Future<void> _incrementRollout(Rollout rollout) async {
    if (rollout.status != RolloutStatus.active) return;
    
    final newPercentage = rollout.currentPercentage + rollout.incrementPercentage;
    
    if (newPercentage >= rollout.maxPercentage) {
      rollout.currentPercentage = rollout.maxPercentage;
      rollout.status = RolloutStatus.completed;
    } else {
      rollout.currentPercentage = newPercentage;
    }
    
    await _saveRollout(rollout);
    await _updateRemoteConfig(rollout);
    
    if (rollout.status == RolloutStatus.active) {
      await _scheduleRolloutIncrement(rollout);
    }
  }
  
  static Future<void> pauseRollout(String flagName) async {
    final rollout = await _getRollout(flagName);
    if (rollout != null) {
      rollout.status = RolloutStatus.paused;
      await _saveRollout(rollout);
    }
  }
  
  static Future<void> resumeRollout(String flagName) async {
    final rollout = await _getRollout(flagName);
    if (rollout != null) {
      rollout.status = RolloutStatus.active;
      await _saveRollout(rollout);
      await _scheduleRolloutIncrement(rollout);
    }
  }
  
  static Future<void> stopRollout(String flagName) async {
    final rollout = await _getRollout(flagName);
    if (rollout != null) {
      rollout.status = RolloutStatus.stopped;
      await _saveRollout(rollout);
    }
  }
  
  static Future<void> _saveRollout(Rollout rollout) async {
    // Save rollout to local storage
    await SecureStorageService.storeData(
      'rollout_${rollout.flagName}',
      json.encode(rollout.toJson()),
    );
  }
  
  static Future<Rollout?> _getRollout(String flagName) async {
    final data = await SecureStorageService.getData('rollout_$flagName');
    if (data != null) {
      return Rollout.fromJson(json.decode(data));
    }
    return null;
  }
  
  static Future<void> _updateRemoteConfig(Rollout rollout) async {
    // Update remote config with new percentage
    await FirebaseRemoteConfig.instance.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(seconds: 30),
      minimumFetchInterval: const Duration(seconds: 0),
    ));
    
    await FirebaseRemoteConfig.instance.fetchAndActivate();
  }
}

class Rollout {
  final String flagName;
  int currentPercentage;
  final Duration incrementInterval;
  final int incrementPercentage;
  final int maxPercentage;
  final DateTime startDate;
  RolloutStatus status;
  
  Rollout({
    required this.flagName,
    required this.currentPercentage,
    required this.incrementInterval,
    required this.incrementPercentage,
    required this.maxPercentage,
    required this.startDate,
    required this.status,
  });
  
  Map<String, dynamic> toJson() {
    return {
      'flag_name': flagName,
      'current_percentage': currentPercentage,
      'increment_interval': incrementInterval.inMilliseconds,
      'increment_percentage': incrementPercentage,
      'max_percentage': maxPercentage,
      'start_date': startDate.toIso8601String(),
      'status': status.name,
    };
  }
  
  factory Rollout.fromJson(Map<String, dynamic> json) {
    return Rollout(
      flagName: json['flag_name'],
      currentPercentage: json['current_percentage'],
      incrementInterval: Duration(milliseconds: json['increment_interval']),
      incrementPercentage: json['increment_percentage'],
      maxPercentage: json['max_percentage'],
      startDate: DateTime.parse(json['start_date']),
      status: RolloutStatus.values.firstWhere(
        (e) => e.name == json['status'],
        orElse: () => RolloutStatus.stopped,
      ),
    );
  }
}

enum RolloutStatus {
  active,
  paused,
  stopped,
  completed,
}
```

## 📈 **Feature Flag Analytics | تحليلات Feature Flags**

### **1. Feature Flag Analytics | تحليلات Feature Flags**
```dart
// lib/core/feature_flags/feature_flag_analytics.dart
class FeatureFlagAnalytics {
  static Future<void> trackFlagEvaluation(String flagName, bool enabled, {
    String? userId,
    String? variant,
  }) async {
    await FirebaseAnalyticsService.logEvent('feature_flag_evaluation', {
      'flag_name': flagName,
      'enabled': enabled,
      'variant': variant,
      'user_id': userId,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackFlagUsage(String flagName, String action, {
    String? userId,
    String? variant,
  }) async {
    await FirebaseAnalyticsService.logEvent('feature_flag_usage', {
      'flag_name': flagName,
      'action': action,
      'variant': variant,
      'user_id': userId,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackRolloutProgress(String flagName, int percentage) async {
    await FirebaseAnalyticsService.logEvent('rollout_progress', {
      'flag_name': flagName,
      'percentage': percentage,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
  
  static Future<void> trackABTestResult(String testName, String variant, {
    required String metric,
    required double value,
    String? userId,
  }) async {
    await FirebaseAnalyticsService.logEvent('ab_test_result', {
      'test_name': testName,
      'variant': variant,
      'metric': metric,
      'value': value,
      'user_id': userId,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }
}
```

## 🎛️ **Feature Flag Dashboard | لوحة تحكم Feature Flags**

### **1. Feature Flag Dashboard | لوحة تحكم Feature Flags**
```dart
// lib/features/feature_flags/presentation/pages/feature_flag_dashboard.dart
class FeatureFlagDashboard extends StatelessWidget {
  const FeatureFlagDashboard({super.key});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Feature Flags Dashboard'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Active Feature Flags',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildFeatureFlagsList(),
            const SizedBox(height: 24),
            const Text(
              'A/B Tests',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildABTestsList(),
            const SizedBox(height: 24),
            const Text(
              'Rollout Progress',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildRolloutProgress(),
          ],
        ),
      ),
    );
  }
  
  Widget _buildFeatureFlagsList() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildFeatureFlagItem('new_checkout_flow', true, 75),
            _buildFeatureFlagItem('dark_mode', true, 100),
            _buildFeatureFlagItem('social_login', false, 0),
            _buildFeatureFlagItem('advanced_search', true, 25),
          ],
        ),
      ),
    );
  }
  
  Widget _buildFeatureFlagItem(String name, bool enabled, int percentage) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(name),
          Text('${percentage}%'),
          Icon(
            enabled ? Icons.check_circle : Icons.cancel,
            color: enabled ? Colors.green : Colors.red,
          ),
        ],
      ),
    );
  }
  
  Widget _buildABTestsList() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildABTestItem('checkout_button_color', 'Active', 'Control vs Red'),
            _buildABTestItem('product_images', 'Completed', 'Single vs Multiple'),
            _buildABTestItem('search_algorithm', 'Active', 'Old vs New'),
          ],
        ),
      ),
    );
  }
  
  Widget _buildABTestItem(String name, String status, String description) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(name),
              Text(description, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
          Text(status),
        ],
      ),
    );
  }
  
  Widget _buildRolloutProgress() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildRolloutItem('new_checkout_flow', 75, 'Active'),
            _buildRolloutItem('dark_mode', 100, 'Completed'),
            _buildRolloutItem('advanced_search', 25, 'Active'),
          ],
        ),
      ),
    );
  }
  
  Widget _buildRolloutItem(String name, int percentage, String status) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(name),
              Text('$percentage%'),
              Text(status),
            ],
          ),
          const SizedBox(height: 4),
          LinearProgressIndicator(value: percentage / 100),
        ],
      ),
    );
  }
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. نظام Feature Flags | Feature Flag System**
- [ ] إعداد Firebase Remote Config
- [ ] تطبيق خدمة Feature Flags
- [ ] إضافة إدارة Feature Flags
- [ ] اختبار وظائف Feature Flags

### **2. اختبار A/B | A/B Testing**
- [ ] تطبيق إطار اختبار A/B
- [ ] إضافة ويدجت اختبار A/B
- [ ] إعداد تتبع اختبار A/B
- [ ] اختبار وظائف اختبار A/B

### **3. النشر التدريجي | Gradual Rollout**
- [ ] تطبيق مدير النشر
- [ ] إضافة جدولة النشر
- [ ] إعداد مراقبة النشر
- [ ] اختبار وظائف النشر

### **4. التحليلات | Analytics**
- [ ] إضافة تحليلات Feature Flags
- [ ] تطبيق تحليلات اختبار A/B
- [ ] إعداد تحليلات النشر
- [ ] اختبار تتبع التحليلات

### **5. لوحة التحكم | Dashboard**
- [ ] إنشاء لوحة Feature Flags
- [ ] إضافة لوحة اختبار A/B
- [ ] تطبيق لوحة النشر
- [ ] اختبار وظائف اللوحة

---

**Next Tab**: Advanced Error Management | إدارة الأخطاء المتقدمة
