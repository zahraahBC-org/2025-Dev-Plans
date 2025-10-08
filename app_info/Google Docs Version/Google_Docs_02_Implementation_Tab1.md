# TAB 1: إعداد المشروع والتكوين | Project Setup & Configuration

## 7. إعداد المشروع والتكوين | Project Setup & Configuration
### إعداد مشروع Flutter للتجارة الإلكترونية مع تكوين مناسب وتبعيات وبيئة تطوير

---

## 🎯 **الهدف | Objective**
إعداد مشروع Flutter للتجارة الإلكترونية كامل مع تكوين مناسب وتبعيات وبيئة تطوير لتعاون الفريق.

## 📋 **القاعدة | Rule**
**العربية**: Flavors + dart-define، وملف AppConfig يحقن في ProviderScope  
**English**: Flavors + dart-define, and AppConfig file injected in ProviderScope

## 💡 **الفوائد | Benefits**
- **إدارة البيئات | Environment Management**: تبديل سهل بين dev/staging/prod
- **مركزية التكوين | Configuration Centralization**: مصدر واحد للحقيقة لإعدادات التطبيق
- **تعاون الفريق | Team Collaboration**: إعداد متسق عبر أعضاء الفريق
- **الأمان | Security**: معالجة آمنة لمفاتيح API والأسرار
- **سرعة التطوير | Development Speed**: إعداد مشروع سريع والانضمام
- **سهولة الصيانة | Maintainability**: سهولة تحديث التكوينات

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: تهيئة المشروع وتكوين البيئة وانضمام الفريق
- **كيفية التطبيق**:
  - إعداد مشروع Flutter بهيكل مناسب
  - تكوين flavors للبيئات المختلفة
  - تطبيق AppConfig مع حقن التبعية
  - إعداد إدارة التبعيات المناسبة
  - تكوين أدوات التطوير و CI/CD
- **النتيجة**: إعداد مشروع جاهز للإنتاج مع إدارة تكوين مناسبة

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بإعداد المشروع | Project Setup Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد مشروع Flutter مع معمارية نظيفة
- **🔴 حرج**: تكوين flavors لجميع البيئات
- **🟠 عالي**: تطبيق AppConfig مع حقن التبعية

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إعداد أدوات التطوير و CI/CD
- **🟠 عالي**: تكوين إدارة التبعيات المناسبة
- **🟡 متوسط**: إضافة ميزات تكوين متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تحسين الأداء والمراقبة
- **🟡 متوسط**: ميزات أمان متقدمة
- **🟢 منخفض**: تحسين التكوين مدعوم بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **Project Setup Specific Metrics:**
- **Setup Time**: <30 minutes for new developer onboarding
- **Environment Switching**: <5 seconds between environments
- **Configuration Accuracy**: 100% consistent across team
- **Security**: Zero hardcoded secrets in code
- **Build Time**: <5 minutes for full project build
- **Documentation**: 100% setup process documented

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **Project Setup Specific Pitfalls:**
- **Avoid**: Hardcoded configuration values
- **Avoid**: Missing environment-specific settings
- **Avoid**: Inconsistent project structure
- **Avoid**: Poor dependency management
- **Avoid**: Missing security considerations

### **Best Practices:**
- **Use**: Flavors for environment management
- **Use**: AppConfig for centralized configuration
- **Use**: Dependency injection for configuration
- **Use**: Proper project structure and organization
- **Use**: Secure handling of secrets and API keys

## 🏗️ **هيكل المشروع | Project Structure**

### **1. Flutter Project Structure | هيكل مشروع Flutter**
```
lib/
├── core/
│   ├── config/
│   │   ├── app_config.dart
│   │   ├── environment.dart
│   │   └── flavors.dart
│   ├── constants/
│   │   ├── app_constants.dart
│   │   └── api_constants.dart
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   ├── network_info.dart
│   │   └── api_client.dart
│   └── utils/
│       ├── validators.dart
│       └── extensions.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── products/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── orders/
│       ├── data/
│       ├── domain/
│       └── presentation/
├── shared/
│   ├── widgets/
│   ├── themes/
│   └── utils/
└── main.dart
```

### **2. Configuration Files | ملفات التكوين**
```
├── android/
│   ├── app/
│   │   ├── build.gradle
│   │   └── src/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
├── ios/
│   ├── Runner/
│   │   ├── Info.plist
│   │   └── Config/
│   │       ├── dev.xcconfig
│   │       ├── staging.xcconfig
│   │       └── prod.xcconfig
├── pubspec.yaml
├── analysis_options.yaml
├── .gitignore
└── README.md
```

## 🔧 **إعداد مشروع Flutter | Flutter Project Setup**

### **1. Create Flutter Project | إنشاء مشروع Flutter**
```bash
# Create new Flutter project
flutter create zahraah_ecommerce

# Navigate to project directory
cd zahraah_ecommerce

# Initialize git repository
git init
git add .
git commit -m "Initial Flutter project setup"
```

### **2. Update pubspec.yaml | تحديث pubspec.yaml**
```yaml
name: zahraah_ecommerce
description: Zahraah - Women's Fashion E-commerce App
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.10.0"

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3
  
  # Navigation
  go_router: ^12.1.3
  
  # Network
  dio: ^5.3.2
  retrofit: ^4.0.3
  
  # Local Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # UI
  flutter_screenutil: ^5.9.0
  cached_network_image: ^3.3.0
  
  # Utils
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  uuid: ^4.2.1
  
  # Firebase
  firebase_core: ^2.24.2
  firebase_auth: ^4.15.3
  firebase_firestore: ^4.13.6
  firebase_storage: ^11.5.6
  firebase_crashlytics: ^3.4.9
  firebase_analytics: ^10.7.4

dev_dependencies:
  flutter_test:
    sdk: flutter
  
  # Code Generation
  build_runner: ^2.4.7
  freezed: ^2.4.6
  json_serializable: ^6.7.1
  riverpod_generator: ^2.3.9
  retrofit_generator: ^8.0.4
  hive_generator: ^2.0.1
  
  # Testing
  mockito: ^5.4.2
  bloc_test: ^9.1.5
  
  # Linting
  flutter_lints: ^3.0.1

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/icons/
    - assets/fonts/
  
  fonts:
    - family: Cairo
      fonts:
        - asset: assets/fonts/Cairo-Regular.ttf
        - asset: assets/fonts/Cairo-Bold.ttf
          weight: 700
```

## 🌍 **تكوين البيئة | Environment Configuration**

### **1. Environment Enum | تعداد البيئة**
```dart
enum Environment {
  development,
  staging,
  production,
}

extension EnvironmentExtension on Environment {
  String get name {
    switch (this) {
      case Environment.development:
        return 'development';
      case Environment.staging:
        return 'staging';
      case Environment.production:
        return 'production';
    }
  }
  
  bool get isDevelopment => this == Environment.development;
  bool get isStaging => this == Environment.staging;
  bool get isProduction => this == Environment.production;
}
```

### **2. App Configuration | تكوين التطبيق**
```dart
@freezed
class AppConfig with _$AppConfig {
  const factory AppConfig({
    required Environment environment,
    required String appName,
    required String appVersion,
    required String baseUrl,
    required String apiKey,
    required String firebaseProjectId,
    required bool enableLogging,
    required bool enableCrashlytics,
    required bool enableAnalytics,
  }) = _AppConfig;
  
  factory AppConfig.fromJson(Map<String, dynamic> json) => _$AppConfigFromJson(json);
}

class AppConfigProvider {
  static AppConfig get config {
    const environment = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');
    const baseUrl = String.fromEnvironment('BASE_URL');
    const apiKey = String.fromEnvironment('API_KEY');
    const firebaseProjectId = String.fromEnvironment('FIREBASE_PROJECT_ID');
    
    switch (environment) {
      case 'development':
        return AppConfig(
          environment: Environment.development,
          appName: 'Zahraah Dev',
          appVersion: '1.0.0-dev',
          baseUrl: baseUrl.isNotEmpty ? baseUrl : 'https://api-dev.zahraah.com',
          apiKey: apiKey.isNotEmpty ? apiKey : 'dev-api-key',
          firebaseProjectId: firebaseProjectId.isNotEmpty ? firebaseProjectId : 'zahraah-dev',
          enableLogging: true,
          enableCrashlytics: false,
          enableAnalytics: false,
        );
      case 'staging':
        return AppConfig(
          environment: Environment.staging,
          appName: 'Zahraah Staging',
          appVersion: '1.0.0-staging',
          baseUrl: baseUrl.isNotEmpty ? baseUrl : 'https://api-staging.zahraah.com',
          apiKey: apiKey.isNotEmpty ? apiKey : 'staging-api-key',
          firebaseProjectId: firebaseProjectId.isNotEmpty ? firebaseProjectId : 'zahraah-staging',
          enableLogging: true,
          enableCrashlytics: true,
          enableAnalytics: true,
        );
      case 'production':
        return AppConfig(
          environment: Environment.production,
          appName: 'Zahraah',
          appVersion: '1.0.0',
          baseUrl: baseUrl.isNotEmpty ? baseUrl : 'https://api.zahraah.com',
          apiKey: apiKey.isNotEmpty ? apiKey : 'prod-api-key',
          firebaseProjectId: firebaseProjectId.isNotEmpty ? firebaseProjectId : 'zahraah-prod',
          enableLogging: false,
          enableCrashlytics: true,
          enableAnalytics: true,
        );
      default:
        throw Exception('Unknown environment: $environment');
    }
  }
}
```

## 🍰 **تكوين النكهات | Flavors Configuration**

### **1. Android Flavors | نكهات Android**
```gradle
// android/app/build.gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.zahraah.ecommerce"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
    
    flavorDimensions "environment"
    
    productFlavors {
        dev {
            dimension "environment"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
            resValue "string", "app_name", "Zahraah Dev"
            buildConfigField "String", "BASE_URL", '"https://api-dev.zahraah.com"'
            buildConfigField "String", "API_KEY", '"dev-api-key"'
        }
        
        staging {
            dimension "environment"
            applicationIdSuffix ".staging"
            versionNameSuffix "-staging"
            resValue "string", "app_name", "Zahraah Staging"
            buildConfigField "String", "BASE_URL", '"https://api-staging.zahraah.com"'
            buildConfigField "String", "API_KEY", '"staging-api-key"'
        }
        
        prod {
            dimension "environment"
            resValue "string", "app_name", "Zahraah"
            buildConfigField "String", "BASE_URL", '"https://api.zahraah.com"'
            buildConfigField "String", "API_KEY", '"prod-api-key"'
        }
    }
}
```

### **2. iOS Flavors | نكهات iOS**
```xcconfig
// ios/Config/dev.xcconfig
#include "Generated.xcconfig"

PRODUCT_BUNDLE_IDENTIFIER = com.zahraah.ecommerce.dev
DISPLAY_NAME = Zahraah Dev
BASE_URL = https://api-dev.zahraah.com
API_KEY = dev-api-key

// ios/Config/staging.xcconfig
#include "Generated.xcconfig"

PRODUCT_BUNDLE_IDENTIFIER = com.zahraah.ecommerce.staging
DISPLAY_NAME = Zahraah Staging
BASE_URL = https://api-staging.zahraah.com
API_KEY = staging-api-key

// ios/Config/prod.xcconfig
#include "Generated.xcconfig"

PRODUCT_BUNDLE_IDENTIFIER = com.zahraah.ecommerce
DISPLAY_NAME = Zahraah
BASE_URL = https://api.zahraah.com
API_KEY = prod-api-key
```

## 🔌 **إعداد حقن التبعية | Dependency Injection Setup**

### **1. Provider Setup | إعداد Provider**
```dart
// lib/core/di/providers.dart
final appConfigProvider = Provider<AppConfig>((ref) => AppConfigProvider.config);

final networkInfoProvider = Provider<NetworkInfo>((ref) => NetworkInfoImpl());

final dioProvider = Provider<Dio>((ref) {
  final config = ref.read(appConfigProvider);
  final dio = Dio();
  
  dio.options.baseUrl = config.baseUrl;
  dio.options.connectTimeout = const Duration(seconds: 30);
  dio.options.receiveTimeout = const Duration(seconds: 30);
  
  dio.interceptors.addAll([
    AuthInterceptor(),
    LoggingInterceptor(),
    ErrorInterceptor(),
  ]);
  
  return dio;
});

final firebaseProvider = Provider<FirebaseApp>((ref) => Firebase.app());

final crashlyticsProvider = Provider<FirebaseCrashlytics>((ref) => FirebaseCrashlytics.instance);

final analyticsProvider = Provider<FirebaseAnalytics>((ref) => FirebaseAnalytics.instance);
```

### **2. Main App Setup | إعداد التطبيق الرئيسي**
```dart
// lib/main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  // Initialize ScreenUtil
  await ScreenUtil.ensureScreenSize();
  
  runApp(
    ProviderScope(
      overrides: [
        appConfigProvider.overrideWithValue(AppConfigProvider.config),
      ],
      child: const ZahraahApp(),
    ),
  );
}

class ZahraahApp extends ConsumerWidget {
  const ZahraahApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final config = ref.watch(appConfigProvider);
    
    return ScreenUtilInit(
      designSize: const Size(375, 812),
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return MaterialApp.router(
          title: config.appName,
          debugShowCheckedModeBanner: config.isDevelopment,
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          routerConfig: AppRouter.router,
          locale: const Locale('ar', 'SA'),
          supportedLocales: const [
            Locale('ar', 'SA'),
            Locale('en', 'US'),
          ],
        );
      },
    );
  }
}
```

## 🛠️ **إعداد أدوات التطوير | Development Tools Setup**

### **1. Analysis Options | خيارات التحليل**
```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "**/*.config.dart"
  
  strong-mode:
    implicit-casts: false
    implicit-dynamic: false
  
  errors:
    invalid_annotation_target: ignore
    missing_required_param: error
    missing_return: error

linter:
  rules:
    # Error rules
    avoid_print: true
    avoid_unnecessary_containers: true
    avoid_web_libraries_in_flutter: true
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    
    # Style rules
    always_declare_return_types: true
    always_put_control_body_on_new_line: true
    always_specify_types: false
    annotate_overrides: true
    avoid_empty_else: true
    avoid_function_literals_in_foreach_calls: true
    avoid_renaming_method_parameters: true
    avoid_single_cascade_in_expression_statements: true
    avoid_unused_constructor_parameters: true
    cascade_invocations: true
    constant_identifier_names: true
    curly_braces_in_flow_control_structures: true
    empty_catches: true
    empty_constructor_bodies: true
    file_names: true
    flutter_style_todos: true
    implementation_imports: true
    library_names: true
    library_prefixes: true
    non_constant_identifier_names: true
    null_closures: true
    overridden_fields: true
    package_api_docs: true
    package_names: true
    package_prefixed_library_names: true
    prefer_adjacent_string_concatenation: true
    prefer_collection_literals: true
    prefer_conditional_assignment: true
    prefer_contains: true
    prefer_equal_for_default_values: true
    prefer_expression_function_bodies: true
    prefer_final_fields: true
    prefer_final_in_for_each: true
    prefer_final_locals: true
    prefer_for_elements_to_map_fromIterable: true
    prefer_function_declarations_over_variables: true
    prefer_generic_function_type_aliases: true
    prefer_if_elements_to_conditional_expressions: true
    prefer_if_null_operators: true
    prefer_initializing_formals: true
    prefer_inlined_adds: true
    prefer_int_literals: true
    prefer_interpolation_to_compose_strings: true
    prefer_is_empty: true
    prefer_is_not_empty: true
    prefer_is_not_operator: true
    prefer_iterable_whereType: true
    prefer_null_aware_operators: true
    prefer_relative_imports: true
    prefer_single_quotes: true
    prefer_spread_collections: true
    prefer_typing_uninitialized_variables: true
    provide_deprecation_message: true
    recursive_getters: true
    slash_for_doc_comments: true
    sort_child_properties_last: true
    sort_constructors_first: true
    sort_unnamed_constructors_first: true
    type_annotate_public_apis: true
    type_init_formals: true
    unawaited_futures: true
    unnecessary_await_in_return: true
    unnecessary_brace_in_string_interps: true
    unnecessary_const: true
    unnecessary_constructor_name: true
    unnecessary_getters_setters: true
    unnecessary_lambdas: true
    unnecessary_new: true
    unnecessary_null_aware_assignments: true
    unnecessary_null_checks: true
    unnecessary_null_in_if_null_operators: true
    unnecessary_nullable_for_final_variable_declarations: true
    unnecessary_overrides: true
    unnecessary_parenthesis: true
    unnecessary_raw_strings: true
    unnecessary_statements: true
    unnecessary_string_escapes: true
    unnecessary_string_interpolations: true
    unnecessary_this: true
    unrelated_type_equality_checks: true
    use_build_context_synchronously: true
    use_colored_box: true
    use_decorated_box: true
    use_enums: true
    use_full_hex_values_for_flutter_colors: true
    use_function_type_syntax_for_parameters: true
    use_if_null_to_convert_nulls_to_bools: true
    use_is_even_rather_than_modulo: true
    use_key_in_widget_constructors: true
    use_late_for_private_fields_and_variables: true
    use_named_constants: true
    use_raw_strings: true
    use_rethrow_when_possible: true
    use_setters_to_change_properties: true
    use_string_buffers: true
    use_test_throws_matchers: true
    use_to_and_as_if_applicable: true
    valid_regexps: true
    void_checks: true
```

### **2. Build Scripts | سكريبتات البناء**
```bash
#!/bin/bash
# scripts/build_dev.sh
flutter clean
flutter pub get
flutter build apk --flavor dev --dart-define=ENVIRONMENT=development
```

```bash
#!/bin/bash
# scripts/build_staging.sh
flutter clean
flutter pub get
flutter build apk --flavor staging --dart-define=ENVIRONMENT=staging
```

```bash
#!/bin/bash
# scripts/build_prod.sh
flutter clean
flutter pub get
flutter build apk --flavor prod --dart-define=ENVIRONMENT=production
```

## 🧪 **إعداد الاختبار | Testing Setup**

### **1. Test Configuration | تكوين الاختبار**
```dart
// test/test_helpers.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';

class MockAppConfig extends Mock implements AppConfig {}

class MockNetworkInfo extends Mock implements NetworkInfo {}

class MockDio extends Mock implements Dio {}

// Test providers
final testAppConfigProvider = Provider<AppConfig>((ref) => MockAppConfig());
final testNetworkInfoProvider = Provider<NetworkInfo>((ref) => MockNetworkInfo());
final testDioProvider = Provider<Dio>((ref) => MockDio());

// Test setup
void setupTestEnvironment() {
  TestWidgetsFlutterBinding.ensureInitialized();
}

// Test teardown
void tearDownTestEnvironment() {
  // Clean up test resources
}
```

### **2. Test Utilities | أدوات الاختبار**
```dart
// test/utils/test_utils.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class TestWrapper extends StatelessWidget {
  final Widget child;
  final List<Override> overrides;
  
  const TestWrapper({
    super.key,
    required this.child,
    this.overrides = const [],
  });

  @override
  Widget build(BuildContext context) {
    return ProviderScope(
      overrides: overrides,
      child: MaterialApp(
        home: child,
      ),
    );
  }
}

// Test helpers
Widget createTestableWidget(Widget widget, {List<Override> overrides = const []}) {
  return TestWrapper(
    overrides: overrides,
    child: widget,
  );
}

void expectWidgetExists(WidgetTester tester, Type widgetType) {
  expect(find.byType(widgetType), findsOneWidget);
}

void expectTextExists(WidgetTester tester, String text) {
  expect(find.text(text), findsOneWidget);
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Project Setup**
- [ ] Create Flutter project with proper structure
- [ ] Configure pubspec.yaml with dependencies
- [ ] Set up clean architecture folder structure
- [ ] Initialize git repository

### **2. Environment Configuration**
- [ ] Create environment enum and configuration
- [ ] Set up flavors for Android and iOS
- [ ] Implement AppConfig with dependency injection
- [ ] Configure environment-specific settings

### **3. Development Tools**
- [ ] Set up analysis_options.yaml
- [ ] Configure linting rules
- [ ] Create build scripts
- [ ] Set up testing infrastructure

### **4. Dependencies**
- [ ] Add all required dependencies
- [ ] Configure dependency injection
- [ ] Set up providers and overrides
- [ ] Test dependency resolution

### **5. Documentation**
- [ ] Create README.md
- [ ] Document setup process
- [ ] Add team onboarding guide
- [ ] Create troubleshooting guide

---

**Next Tab**: Testing Strategy | استراتيجية الاختبار

