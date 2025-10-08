# TAB 2: استراتيجية الاختبار | Testing Strategy

## 8. استراتيجية الاختبار | Testing Strategy
### تطبيق استراتيجية اختبار شاملة لضمان جودة الكود ومنع التراجع

---

## 🎯 **الهدف | Objective**
تطبيق استراتيجية اختبار شاملة لضمان جودة الكود ومنع التراجع والحفاظ على موثوقية عالية عبر جميع ميزات التطبيق.

## 📋 **القاعدة | Rule**
**العربية**: هرَم اختبارات: Unit (Use-cases, Repos), Widget (Screens), Integration (رحلة شراء)  
**English**: Test pyramid: Unit (Use-cases, Repos), Widget (Screens), Integration (purchase journey)

## 💡 **الفوائد | Benefits**
- **ضمان الجودة | Quality Assurance**: اكتشاف الأخطاء قبل وصولها للإنتاج
- **منع التراجع | Regression Prevention**: ضمان أن التغييرات لا تكسر الوظائف الموجودة
- **التوثيق | Documentation**: الاختبارات تخدم كتوثيق حي
- **الثقة | Confidence**: نشر بثقة مع معرفة أن الكود يعمل
- **أمان إعادة الهيكلة | Refactoring Safety**: آمن لإعادة الهيكلة مع تغطية الاختبار
- **تعاون الفريق | Team Collaboration**: توقعات ومعايير واضحة

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع الميزات، خاصة منطق الأعمال الحرج
- **كيفية التطبيق**:
  - اختبارات وحدة لمنطق الأعمال (70% تغطية)
  - اختبارات widget لمكونات UI
  - اختبارات تكامل لرحلات المستخدم
  - اختبارات ذهبية للاتساق البصري
  - اختبارات أداء للمسارات الحرجة
- **النتيجة**: قاعدة كود موثوقة وقابلة للصيانة بثقة عالية

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة باستراتيجية الاختبار | Testing Strategy Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد البنية التحتية للاختبار والأدوات
- **🔴 حرج**: تطبيق اختبارات وحدة لمنطق الأعمال الأساسي
- **🟠 عالي**: إنشاء اختبارات widget لمكونات UI

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إضافة اختبارات تكامل لرحلات المستخدم
- **🟠 عالي**: تطبيق اختبارات ذهبية للاتساق البصري
- **🟡 متوسط**: إضافة اختبارات الأداء وإمكانية الوصول

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: أنماط اختبار متقدمة وأتمتة
- **🟡 متوسط**: توليد اختبارات مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: اختبارات أداء وأمان متقدمة

## 📈 **مؤشرات النجاح | Success Metrics**

### **Testing Strategy Specific Metrics:**
- **Test Coverage**: >90% code coverage
- **Test Execution**: <5 minutes for full test suite
- **Bug Detection**: 95%+ bugs caught before production
- **Test Reliability**: <1% flaky tests
- **Documentation**: 100% test documentation coverage
- **Automation**: 100% automated test execution

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **Testing Strategy Specific Pitfalls:**
- **Avoid**: Testing implementation details instead of behavior
- **Avoid**: Over-mocking and brittle tests
- **Avoid**: Missing edge cases and error scenarios
- **Avoid**: Slow and unreliable tests
- **Avoid**: Poor test organization and maintenance

### **Best Practices:**
- **Use**: Test pyramid approach (70% unit, 20% widget, 10% integration)
- **Use**: Behavior-driven testing (BDD) approach
- **Use**: Comprehensive mocking and test data
- **Use**: Continuous integration and automated testing
- **Use**: Clear test naming and documentation

## 🧪 **هرم الاختبارات | Test Pyramid**

### **1. Test Distribution | توزيع الاختبارات**
```
    /\
   /  \     E2E Tests (5%)
  /____\    - Critical user journeys
 /      \   
/        \  Integration Tests (15%)
/__________\ - API integration
/            \ - Feature integration
/              \
/                \ Widget Tests (20%)
/__________________\ - UI components
/                    \ - User interactions
/                      \
/                        \ Unit Tests (60%)
/__________________________\ - Business logic
                            - Use cases
                            - Repositories
                            - Services
```

### **2. Test Coverage Targets | أهداف تغطية الاختبار**
- **Unit Tests**: 70% coverage (business logic, use cases, repositories)
- **Widget Tests**: 20% coverage (UI components, user interactions)
- **Integration Tests**: 15% coverage (API integration, feature flows)
- **E2E Tests**: 5% coverage (critical user journeys)

## 🔬 **اختبار الوحدة | Unit Testing**

### **1. Use Case Testing | اختبار حالات الاستخدام**
```dart
// test/features/products/domain/usecases/get_products_usecase_test.dart
void main() {
  group('GetProductsUseCase', () {
    late GetProductsUseCase useCase;
    late MockProductRepository mockRepository;

    setUp(() {
      mockRepository = MockProductRepository();
      useCase = GetProductsUseCase(mockRepository);
    });

    test('should return products when repository call is successful', () async {
      // Arrange
      const products = [sampleProduct1, sampleProduct2];
      when(mockRepository.getProducts())
          .thenAnswer((_) async => const Success(products));

      // Act
      final result = await useCase.call();

      // Assert
      expect(result, isA<Success<List<Product>>>());
      expect((result as Success).data, equals(products));
      verify(mockRepository.getProducts());
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return failure when repository call fails', () async {
      // Arrange
      const error = NetworkError('Network error');
      when(mockRepository.getProducts())
          .thenAnswer((_) async => const Failure(error));

      // Act
      final result = await useCase.call();

      // Assert
      expect(result, isA<Failure<List<Product>>>());
      expect((result as Failure).error, equals(error));
      verify(mockRepository.getProducts());
    });

    test('should validate input parameters', () async {
      // Act
      final result = await useCase.call(limit: -1);

      // Assert
      expect(result, isA<Failure<List<Product>>>());
      expect((result as Failure).error, isA<ValidationError>());
      verifyNever(mockRepository.getProducts());
    });
  });
}
```

### **2. Repository Testing | اختبار المستودعات**
```dart
// test/features/products/data/repositories/product_repository_impl_test.dart
void main() {
  group('ProductRepositoryImpl', () {
    late ProductRepositoryImpl repository;
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

    test('should return remote data when network is available', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.getProducts())
          .thenAnswer((_) async => const Success(sampleProducts));

      // Act
      final result = await repository.getProducts();

      // Assert
      expect(result, isA<Success<List<Product>>>());
      expect((result as Success).data, equals(sampleProducts));
      verify(mockRemoteDataSource.getProducts());
      verify(mockLocalDataSource.cacheProducts(sampleProducts));
    });

    test('should return cached data when network is unavailable', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => false);
      when(mockLocalDataSource.getCachedProducts())
          .thenAnswer((_) async => sampleProducts);

      // Act
      final result = await repository.getProducts();

      // Assert
      expect(result, isA<Success<List<Product>>>());
      expect((result as Success).data, equals(sampleProducts));
      verify(mockLocalDataSource.getCachedProducts());
      verifyNever(mockRemoteDataSource.getProducts());
    });
  });
}
```

### **3. Service Testing | اختبار الخدمات**
```dart
// test/core/services/pricing_service_test.dart
void main() {
  group('PricingService', () {
    test('should calculate subtotal correctly', () {
      // Arrange
      const items = [
        OrderItem(productId: '1', price: 100.0, quantity: 2),
        OrderItem(productId: '2', price: 50.0, quantity: 1),
      ];

      // Act
      final subtotal = PricingService.calculateSubtotal(items);

      // Assert
      expect(subtotal, equals(250.0));
    });

    test('should calculate tax correctly', () {
      // Act
      final tax = PricingService.calculateTax(100.0, taxRate: 0.1);

      // Assert
      expect(tax, equals(10.0));
    });

    test('should calculate shipping correctly', () {
      // Act
      final shipping1 = PricingService.calculateShipping(50.0);
      final shipping2 = PricingService.calculateShipping(150.0);

      // Assert
      expect(shipping1, equals(10.0));
      expect(shipping2, equals(0.0));
    });
  });
}
```

## 🖼️ **اختبار العناصر | Widget Testing**

### **1. Component Testing | اختبار المكونات**
```dart
// test/shared/widgets/app_button_test.dart
void main() {
  group('AppButton', () {
    testWidgets('should render button with text', (tester) async {
      // Arrange
      const buttonText = 'Test Button';

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          AppButton(
            text: buttonText,
            onPressed: () {},
          ),
        ),
      );

      // Assert
      expect(find.text(buttonText), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('should show loading state', (tester) async {
      // Act
      await tester.pumpWidget(
        createTestableWidget(
          AppButton(
            text: 'Test Button',
            isLoading: true,
          ),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Test Button'), findsNothing);
    });

    testWidgets('should handle tap events', (tester) async {
      // Arrange
      bool wasTapped = false;
      const buttonText = 'Test Button';

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          AppButton(
            text: buttonText,
            onPressed: () => wasTapped = true,
          ),
        ),
      );

      await tester.tap(find.text(buttonText));
      await tester.pump();

      // Assert
      expect(wasTapped, isTrue);
    });
  });
}
```

### **2. Screen Testing | اختبار الشاشات**
```dart
// test/features/products/presentation/pages/products_page_test.dart
void main() {
  group('ProductsPage', () {
    late MockProductNotifier mockNotifier;

    setUp(() {
      mockNotifier = MockProductNotifier();
    });

    testWidgets('should show loading state initially', (tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(const ProductState(isLoading: true));

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          ProductsPage(),
          overrides: [
            productNotifierProvider.overrideWith((ref) => mockNotifier),
          ],
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Loading products...'), findsOneWidget);
    });

    testWidgets('should show products when loaded', (tester) async {
      // Arrange
      const products = [sampleProduct1, sampleProduct2];
      when(mockNotifier.state).thenReturn(
        ProductState(products: products, isLoading: false),
      );

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          ProductsPage(),
          overrides: [
            productNotifierProvider.overrideWith((ref) => mockNotifier),
          ],
        ),
      );

      // Assert
      expect(find.text(sampleProduct1.name), findsOneWidget);
      expect(find.text(sampleProduct2.name), findsOneWidget);
      expect(find.byType(ProductCard), findsNWidgets(2));
    });

    testWidgets('should show error state when failed', (tester) async {
      // Arrange
      when(mockNotifier.state).thenReturn(
        const ProductState(
          isLoading: false,
          hasError: true,
          errorMessage: 'Failed to load products',
        ),
      );

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          ProductsPage(),
          overrides: [
            productNotifierProvider.overrideWith((ref) => mockNotifier),
          ],
        ),
      );

      // Assert
      expect(find.text('Failed to load products'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });
  });
}
```

## 🔗 **اختبار التكامل | Integration Testing**

### **1. API Integration Tests | اختبارات تكامل API**
```dart
// integration_test/api_integration_test.dart
void main() {
  group('API Integration Tests', () {
    late Dio dio;
    late String baseUrl;

    setUp(() {
      baseUrl = 'https://api-dev.zahraah.com';
      dio = Dio();
      dio.options.baseUrl = baseUrl;
    });

    test('should fetch products from API', () async {
      // Act
      final response = await dio.get('/products');

      // Assert
      expect(response.statusCode, equals(200));
      expect(response.data, isA<List>());
      expect(response.data.isNotEmpty, isTrue);
    });

    test('should handle API errors gracefully', () async {
      // Act & Assert
      expect(
        () => dio.get('/products/invalid-id'),
        throwsA(isA<DioException>()),
      );
    });
  });
}
```

### **2. Feature Integration Tests | اختبارات تكامل الميزات**
```dart
// integration_test/features/product_purchase_flow_test.dart
void main() {
  group('Product Purchase Flow', () {
    testWidgets('should complete purchase journey', (tester) async {
      // Arrange
      await tester.pumpWidget(
        createTestableWidget(
          const ZahraahApp(),
          overrides: [
            productNotifierProvider.overrideWith((ref) => MockProductNotifier()),
            cartNotifierProvider.overrideWith((ref) => MockCartNotifier()),
            orderNotifierProvider.overrideWith((ref) => MockOrderNotifier()),
          ],
        ),
      );

      // Act - Navigate to products
      await tester.pumpAndSettle();
      await tester.tap(find.text('Products'));
      await tester.pumpAndSettle();

      // Act - Select product
      await tester.tap(find.byType(ProductCard).first);
      await tester.pumpAndSettle();

      // Act - Add to cart
      await tester.tap(find.text('Add to Cart'));
      await tester.pumpAndSettle();

      // Act - Go to cart
      await tester.tap(find.byIcon(Icons.shopping_cart));
      await tester.pumpAndSettle();

      // Act - Proceed to checkout
      await tester.tap(find.text('Checkout'));
      await tester.pumpAndSettle();

      // Assert
      expect(find.text('Order Summary'), findsOneWidget);
      expect(find.text('Place Order'), findsOneWidget);
    });
  });
}
```

## 🎨 **اختبارات الذهبية | Golden Tests**

### **1. Visual Regression Testing | اختبار الانحدار البصري**
```dart
// test/golden/app_button_golden_test.dart
void main() {
  group('AppButton Golden Tests', () {
    testWidgets('primary button matches golden file', (tester) async {
      // Arrange
      await tester.pumpWidget(
        createTestableWidget(
          AppButton(
            text: 'Primary Button',
            type: AppButtonType.primary,
            onPressed: () {},
          ),
        ),
      );

      // Act
      await tester.pumpAndSettle();

      // Assert
      await expectLater(
        find.byType(AppButton),
        matchesGoldenFile('goldens/app_button_primary.png'),
      );
    });

    testWidgets('secondary button matches golden file', (tester) async {
      // Arrange
      await tester.pumpWidget(
        createTestableWidget(
          AppButton(
            text: 'Secondary Button',
            type: AppButtonType.secondary,
            onPressed: () {},
          ),
        ),
      );

      // Act
      await tester.pumpAndSettle();

      // Assert
      await expectLater(
        find.byType(AppButton),
        matchesGoldenFile('goldens/app_button_secondary.png'),
      );
    });
  });
}
```

## ⚡ **اختبار الأداء | Performance Testing**

### **1. Performance Benchmarks | معايير الأداء**
```dart
// test/performance/product_list_performance_test.dart
void main() {
  group('Product List Performance', () {
    testWidgets('should render 100 products within 16ms', (tester) async {
      // Arrange
      final products = List.generate(100, (index) => createSampleProduct(index));

      // Act
      await tester.pumpWidget(
        createTestableWidget(
          ProductListWidget(products: products),
        ),
      );

      // Assert
      final stopwatch = Stopwatch()..start();
      await tester.pumpAndSettle();
      stopwatch.stop();

      expect(stopwatch.elapsedMilliseconds, lessThan(16));
    });
  });
}
```

## 🧪 **أدوات الاختبار | Test Utilities**

### **1. Test Data Factory | مصنع بيانات الاختبار**
```dart
// test/utils/test_data_factory.dart
class TestDataFactory {
  static Product createSampleProduct([int index = 0]) {
    return Product(
      id: 'product_$index',
      name: 'Test Product $index',
      description: 'Test Description $index',
      price: 99.99 + index,
      category: 'Electronics',
      images: ['image_$index.jpg'],
      stockQuantity: 10 + index,
      isAvailable: true,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  static List<Product> createSampleProducts(int count) {
    return List.generate(count, (index) => createSampleProduct(index));
  }

  static User createSampleUser([int index = 0]) {
    return User(
      id: 'user_$index',
      email: 'user$index@test.com',
      firstName: 'Test',
      lastName: 'User$index',
      phoneNumber: '+1234567890',
      role: UserRole.customer,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  static Order createSampleOrder([int index = 0]) {
    return Order(
      id: 'order_$index',
      userId: 'user_$index',
      items: [createSampleOrderItem(index)],
      subtotal: 99.99,
      tax: 9.99,
      shipping: 10.0,
      total: 119.98,
      status: OrderStatus.pending,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }
}
```

### **2. Mock Classes | فئات المحاكاة**
```dart
// test/utils/mocks.dart
@GenerateMocks([
  ProductRepository,
  CartRepository,
  OrderRepository,
  NetworkInfo,
  Dio,
])
void main() {}

class MockProductNotifier extends Mock implements ProductNotifier {}
class MockCartNotifier extends Mock implements CartNotifier {}
class MockOrderNotifier extends Mock implements OrderNotifier {}
class MockAuthNotifier extends Mock implements AuthNotifier {}
```

## 📊 **تغطية الاختبار | Test Coverage**

### **1. Coverage Configuration | تكوين التغطية**
```yaml
# test/coverage.yaml
coverage:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "**/*.config.dart"
    - "**/test/**"
    - "**/integration_test/**"
  
  thresholds:
    global:
      statements: 90
      branches: 85
      functions: 90
      lines: 90
```

### **2. Coverage Reporting | تقارير التغطية**
```bash
#!/bin/bash
# scripts/test_coverage.sh
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Testing Infrastructure**
- [ ] Set up testing dependencies and tools
- [ ] Configure test environment and utilities
- [ ] Create test data factories and mocks
- [ ] Set up coverage reporting

### **2. Unit Tests**
- [ ] Test use cases and business logic
- [ ] Test repositories and data sources
- [ ] Test services and utilities
- [ ] Achieve 70%+ coverage

### **3. Widget Tests**
- [ ] Test UI components and widgets
- [ ] Test screen interactions and navigation
- [ ] Test state management integration
- [ ] Achieve 20%+ coverage

### **4. Integration Tests**
- [ ] Test API integration
- [ ] Test feature flows and user journeys
- [ ] Test end-to-end scenarios
- [ ] Achieve 15%+ coverage

### **5. Quality Assurance**
- [ ] Set up continuous integration
- [ ] Configure automated testing
- [ ] Implement test reporting
- [ ] Monitor test performance

---

**Next Tab**: Code Quality Standards | معايير جودة الكود

