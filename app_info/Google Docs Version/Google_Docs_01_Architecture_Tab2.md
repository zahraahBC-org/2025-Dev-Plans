# TAB 2: إدارة الحالة وحقن التبعية | State Management & DI

## 2. إدارة الحالة وحقن الاعتماديات | State Management & Dependency Injection
### تطبيق إدارة الحالة وحقن التبعية للتطبيقات القابلة للاختبار والصيانة

---

## 🎯 **الهدف | Objective**
تطبيق إدارة حالة قوية وحقن التبعية لحالة تطبيق Flutter متوقعة وقابلة للاختبار والصيانة.

## 📋 **القاعدة | Rule**
**العربية**: استخدم Riverpod (أو BLoC—اختر واحدًا وثبّته) + DI عبر Providers  
**English**: Use Riverpod (or BLoC—choose one and stick with it) + DI through Providers

## 💡 **الفوائد | Benefits**
- **إعادة بناء ذكية | Smart Rebuilds**: إعادة بناء widgets التي تحتاج تحديث فقط، تحسين الأداء
- **اختبار سهل | Easy Testing**: يمكن اختبار الحالة بشكل مستقل مع المحاكاة المناسبة
- **تجنب Singleton | Avoid Singletons**: إدارة تبعيات أفضل وقابلية اختبار
- **الأداء | Performance**: تقليل إعادة البناء غير الضرورية واستخدام الذاكرة
- **حالة متوقعة | Predictable State**: تدفق حالة واضح وتصحيح أخطاء أسهل
- **تعاون الفريق | Team Collaboration**: أنماط متسقة عبر الفريق

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع الميزات التي تتطلب إدارة الحالة والوصول للبيانات
- **كيفية التطبيق**:
  - إعداد ProviderScope في main.dart
  - إنشاء StateNotifier لكل ميزة
  - استخدام Provider لواجهات المستودع
  - تطبيق التخلص والتنظيف المناسب
  - استخدام Consumer/ConsumerWidget لتحديثات UI
- **النتيجة**: إدارة حالة متوقعة مع أداء أفضل وقابلية اختبار

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بإدارة الحالة وحقن التبعية | State Management & DI Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد Riverpod ProviderScope وتطبيق إدارة الحالة الأساسية
- **🔴 حرج**: إنشاء StateNotifier controllers وتطبيق أنماط DI المناسبة
- **🟠 عالي**: تطبيق تكامل Result pattern ومعالجة الأخطاء

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إضافة أنماط إدارة حالة متقدمة وتحسين الأداء
- **🟠 عالي**: تطبيق اختبار ومراقبة شاملة
- **🟡 متوسط**: إضافة استمرارية الحالة وميزات DI متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: أنماط إدارة حالة متقدمة وتحسين مدعوم بالذكاء الاصطناعي
- **🟡 متوسط**: تحسين الأداء ومراقبة متقدمة
- **🟢 منخفض**: تحليلات متقدمة وإدارة حالة مدعومة بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **مؤشرات خاصة بإدارة الحالة وحقن التبعية | State Management & DI Specific Metrics:**
- **اتساق الحالة | State Consistency**: 100% اتساق الحالة، صفر فساد في الحالة
- **الأداء | Performance**: <100ms متوسط وقت تحديث الحالة، <50ms للتحديثات الحرجة
- **أمان الذاكرة | Memory Safety**: صفر تسريب ذاكرة، <5% عبء ذاكرة
- **تغطية الاختبار | Testing Coverage**: >90% تغطية إدارة الحالة، >95% تغطية DI
- **إدارة الموارد | Resource Management**: 100% تخلص صحيح، <1% تسريب موارد
- **إنتاجية الفريق | Team Productivity**: 50% تطوير أسرع، 60% وقت تصحيح أخطاء أقل

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **أخطاء خاصة بإدارة الحالة وحقن التبعية | State Management & DI Specific Pitfalls:**
- **تجنب**: أنماط إدارة حالة مختلطة في نفس المشروع
- **تجنب**: تسريبات الذاكرة من التخلص غير المناسب
- **تجنب**: التبعيات الدائرية في DI
- **تجنب**: منطق الأعمال في UI widgets
- **تجنب**: حالة عامة للاهتمامات المحلية

### **أفضل الممارسات | Best Practices:**
- **استخدم**: حل إدارة حالة واحد بشكل متسق
- **استخدم**: التخلص والتنظيف المناسب
- **استخدم**: نمط Repository للوصول للبيانات
- **استخدم**: Interfaces لحقن التبعية
- **استخدم**: StateNotifier لإدارة الحالة المعقدة

## 🏗️ **إعداد Riverpod | Riverpod Setup**

### **1. التبعيات | Dependencies**
```yaml
dependencies:
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3

dev_dependencies:
  riverpod_generator: ^2.3.9
  build_runner: ^2.4.7
```

### **2. إعداد التطبيق الرئيسي | Main App Setup**
```dart
void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### **3. مثال StateNotifier | StateNotifier Example**
```dart
@riverpod
class ProductNotifier extends _$ProductNotifier {
  @override
  Future<List<Product>> build() async {
    return await ref.read(productRepositoryProvider).getProducts();
  }

  Future<void> addProduct(Product product) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      await ref.read(productRepositoryProvider).addProduct(product);
      return await ref.read(productRepositoryProvider).getProducts();
    });
  }
}
```

## 🔧 **حقن التبعية | Dependency Injection**

### **1. موفر المستودع | Repository Provider**
```dart
@riverpod
ProductRepository productRepository(ProductRepositoryRef ref) {
  return ProductRepositoryImpl(
    apiService: ref.read(apiServiceProvider),
    localStorage: ref.read(localStorageProvider),
  );
}
```

### **2. موفرو الخدمات | Service Providers**
```dart
@riverpod
ApiService apiService(ApiServiceRef ref) {
  return ApiService(
    dio: ref.read(dioProvider),
    baseUrl: ref.read(configProvider).apiBaseUrl,
  );
}

@riverpod
LocalStorage localStorage(LocalStorageRef ref) {
  return HiveLocalStorage();
}
```

## 🧪 **اختبار إدارة الحالة | Testing State Management**

### **1. اختبارات الوحدة | Unit Tests**
```dart
void main() {
  group('ProductNotifier', () {
    test('should load products successfully', () async {
      final container = ProviderContainer(
        overrides: [
          productRepositoryProvider.overrideWithValue(mockRepository),
        ],
      );

      final notifier = container.read(productNotifierProvider.notifier);
      await notifier.build();

      expect(container.read(productNotifierProvider).value, isA<List<Product>>());
    });
  });
}
```

### **2. اختبارات الواجهة | Widget Tests**
```dart
void main() {
  testWidgets('ProductList displays products', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          productNotifierProvider.overrideWithValue(
            AsyncValue.data(sampleProducts),
          ),
        ],
        child: MaterialApp(home: ProductList()),
      ),
    );

    expect(find.byType(ProductCard), findsNWidgets(3));
  });
}
```

## 📊 **تحسين الأداء | Performance Optimization**

### **1. إعادة البناء الانتقائية | Selective Rebuilds**
```dart
class ProductCard extends ConsumerWidget {
  final String productId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final product = ref.watch(productProvider(productId));
    
    return Card(
      child: Text(product.name),
    );
  }
}
```

### **2. استمرارية الحالة | State Persistence**
```dart
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  Cart build() {
    ref.onDispose(() {
      // Save cart state
      ref.read(localStorageProvider).saveCart(state);
    });
    
    return Cart.empty();
  }
}
```

## 🔄 **أنماط إدارة الحالة | State Management Patterns**

### **1. حالات التحميل | Loading States**
```dart
@riverpod
class ProductListNotifier extends _$ProductListNotifier {
  @override
  AsyncValue<List<Product>> build() async {
    try {
      final products = await ref.read(productRepositoryProvider).getProducts();
      return AsyncValue.data(products);
    } catch (error, stackTrace) {
      return AsyncValue.error(error, stackTrace);
    }
  }
}
```

### **2. معالجة الأخطاء | Error Handling**
```dart
class ProductList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final products = ref.watch(productListNotifierProvider);
    
    return products.when(
      data: (products) => ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) => ProductCard(products[index]),
      ),
      loading: () => CircularProgressIndicator(),
      error: (error, stack) => ErrorWidget(error.toString()),
    );
  }
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. الإعداد | Setup**
- [ ] إضافة تبعيات Riverpod
- [ ] لف التطبيق بـ ProviderScope
- [ ] تكوين توليد الكود

### **2. إدارة الحالة | State Management**
- [ ] إنشاء StateNotifier لكل ميزة
- [ ] تطبيق تحديثات الحالة المناسبة
- [ ] إضافة معالجة الأخطاء
- [ ] استخدام Consumer/ConsumerWidget للـ UI

### **3. حقن التبعية | Dependency Injection**
- [ ] إنشاء موفري المستودع
- [ ] إعداد موفري الخدمات
- [ ] استخدام interfaces للتبسيط
- [ ] تطبيق التخلص المناسب

### **4. الاختبار | Testing**
- [ ] كتابة اختبارات وحدة للـ StateNotifiers
- [ ] اختبار حقن التبعية
- [ ] محاكاة التبعيات الخارجية
- [ ] اختبار سيناريوهات الأخطاء

---

**التبويب التالي**: معالجة أخطاء طبقة البيانات | Data Layer Error Handling
