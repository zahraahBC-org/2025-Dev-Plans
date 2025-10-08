# TAB 5: طبقة العرض | Presentation Layer

## 5. طبقة العرض | Presentation Layer
### تطبيق طبقة عرض نظيفة مع تنقل مناسب وإدارة حالة ومكونات UI

---

## 🎯 **الهدف | Objective**
تطبيق طبقة عرض نظيفة مع تنقل مناسب وإدارة حالة ومكونات UI تتبع مبادئ المعمارية النظيفة.

## 📋 **القاعدة | Rule**
**العربية**: استخدم go_router مع Guards للطرق المحمية، وادعم Deep Links & Dynamic Links  
**English**: Use go_router with Guards for protected routes, and support Deep Links & Dynamic Links

## 💡 **الفوائد | Benefits**
- **تنقل نظيف | Clean Navigation**: توجيه مركزي مع أمان الأنواع
- **الروابط العميقة | Deep Linking**: تجربة مستخدم سلسة مع الروابط الخارجية
- **حماية المسارات | Route Protection**: وصول آمن للشاشات المحمية
- **إدارة الحالة | State Management**: فصل مناسب بين UI ومنطق الأعمال
- **الاختبار | Testing**: سهولة اختبار مكونات UI والتنقل
- **سهولة الصيانة | Maintainability**: فصل واضح للاهتمامات

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع شاشات UI وتدفقات التنقل وتفاعلات المستخدم
- **كيفية التطبيق**:
  - إعداد GoRouter مع تكوين مسار مركزي
  - تطبيق حراس المسارات للمصادقة والتفويض
  - إضافة دعم الروابط العميقة لصفحات المنتجات والطلبات
  - استخدام StateNotifier لإدارة حالة UI
  - تطبيق معالجة أخطاء مناسبة وحالات تحميل
- **النتيجة**: طبقة عرض نظيفة وقابلة للصيانة مع تجربة مستخدم ممتازة

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بطبقة العرض | Presentation Layer Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد GoRouter مع تنقل أساسي
- **🔴 حرج**: تطبيق المصادقة وحراس المسارات
- **🟠 عالي**: إضافة دعم الروابط العميقة للميزات الأساسية

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تطبيق إدارة حالة شاملة
- **🟠 عالي**: إضافة معالجة الأخطاء وحالات التحميل
- **🟡 متوسط**: إضافة ميزات تنقل متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تحسين الأداء والرسوم المتحركة
- **🟡 متوسط**: أنماط UI متقدمة وإمكانية الوصول
- **🟢 منخفض**: تخصيص UI مدعوم بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **مؤشرات خاصة بطبقة العرض | Presentation Layer Specific Metrics:**
- **أداء التنقل | Navigation Performance**: <100ms انتقالات المسارات
- **نجاح الروابط العميقة | Deep Link Success**: 100% وظائف الروابط العميقة
- **أمان المسارات | Route Security**: 100% المسارات المحمية مؤمنة
- **استجابة UI | UI Responsiveness**: <16ms عرض الإطارات
- **معالجة الأخطاء | Error Handling**: 100% حالات الأخطاء معالجة
- **إمكانية الوصول | Accessibility**: امتثال WCAG 2.1 AA

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **أخطاء خاصة بطبقة العرض | Presentation Layer Specific Pitfalls:**
- **تجنب**: منطق الأعمال في مكونات UI
- **تجنب**: حراس مسارات مفقودة للشاشات المحمية
- **تجنب**: معالجة أخطاء وحالات تحميل ضعيفة
- **تجنب**: أنماط تنقل غير متسقة
- **تجنب**: دعم روابط عميقة مفقود

### **أفضل الممارسات | Best Practices:**
- **استخدم**: GoRouter للتنقل المركزي
- **استخدم**: حراس المسارات للأمان
- **استخدم**: StateNotifier لإدارة الحالة
- **استخدم**: أنماط معالجة أخطاء مناسبة
- **استخدم**: الروابط العميقة لتجربة مستخدم أفضل

## 🧭 **إعداد التنقل | Navigation Setup**

### **1. تكوين GoRouter | GoRouter Configuration**
```dart
class AppRouter {
  static final GoRouter _router = GoRouter(
    initialLocation: '/',
    routes: [
      // Public routes
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomePage(),
      ),
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterPage(),
      ),
      
      // Product routes
      GoRoute(
        path: '/products',
        name: 'products',
        builder: (context, state) => const ProductsPage(),
        routes: [
          GoRoute(
            path: '/:id',
            name: 'product-detail',
            builder: (context, state) {
              final productId = state.pathParameters['id']!;
              return ProductDetailPage(productId: productId);
            },
          ),
        ],
      ),
      
      // Protected routes
      GoRoute(
        path: '/profile',
        name: 'profile',
        builder: (context, state) => const ProfilePage(),
        redirect: (context, state) => _authGuard(context, state),
      ),
      GoRoute(
        path: '/cart',
        name: 'cart',
        builder: (context, state) => const CartPage(),
        redirect: (context, state) => _authGuard(context, state),
      ),
      GoRoute(
        path: '/orders',
        name: 'orders',
        builder: (context, state) => const OrdersPage(),
        redirect: (context, state) => _authGuard(context, state),
      ),
    ],
    errorBuilder: (context, state) => const ErrorPage(),
  );

  static GoRouter get router => _router;
}
```

### **2. حراس المسارات | Route Guards**
```dart
String? _authGuard(BuildContext context, GoRouterState state) {
  final authState = context.read<AuthNotifier>().state;
  
  if (authState is AuthLoading) {
    return '/loading';
  }
  
  if (authState is AuthUnauthenticated) {
    return '/login';
  }
  
  return null; // Allow navigation
}

class AuthGuard extends ConsumerWidget {
  final Widget child;
  final String redirectTo;

  const AuthGuard({
    super.key,
    required this.child,
    this.redirectTo = '/login',
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authNotifierProvider);

    return authState.when(
      loading: () => const LoadingPage(),
      authenticated: (user) => child,
      unauthenticated: () => const LoginPage(),
      error: (error) => ErrorPage(error: error),
    );
  }
}
```

## 🔗 **الروابط العميقة | Deep Linking**

### **1. تكوين الروابط العميقة | Deep Link Configuration**
```dart
class DeepLinkHandler {
  static void handleDeepLink(String link) {
    final uri = Uri.parse(link);
    
    switch (uri.host) {
      case 'product':
        final productId = uri.pathSegments.last;
        AppRouter.router.go('/products/$productId');
        break;
      case 'order':
        final orderId = uri.pathSegments.last;
        AppRouter.router.go('/orders/$orderId');
        break;
      case 'category':
        final categoryId = uri.pathSegments.last;
        AppRouter.router.go('/products?category=$categoryId');
        break;
      default:
        AppRouter.router.go('/');
    }
  }
}

// Firebase Dynamic Links
class DynamicLinkService {
  static Future<String> createProductLink(String productId) async {
    final parameters = DynamicLinkParameters(
      uriPrefix: 'https://zahraah.page.link',
      link: Uri.parse('https://zahraah.com/product/$productId'),
      androidParameters: const AndroidParameters(
        packageName: 'com.zahraah.app',
        minimumVersion: 1,
      ),
      iosParameters: const IOSParameters(
        bundleId: 'com.zahraah.app',
        minimumVersion: '1.0.0',
      ),
      socialMetaTagParameters: SocialMetaTagParameters(
        title: 'Check out this product on Zahraah',
        description: 'Discover amazing products on Zahraah',
        imageUrl: Uri.parse('https://zahraah.com/images/logo.png'),
      ),
    );

    final shortLink = await FirebaseDynamicLinks.instance.buildShortLink(parameters);
    return shortLink.shortUrl.toString();
  }
}
```

## 🎛️ **إدارة الحالة | State Management**

### **1. تنفيذ StateNotifier | StateNotifier Implementation**
```dart
// Product State
@freezed
class ProductState with _$ProductState {
  const factory ProductState({
    @Default([]) List<Product> products,
    @Default(false) bool isLoading,
    @Default(false) bool hasError,
    String? errorMessage,
    String? selectedCategory,
    String? searchQuery,
  }) = _ProductState;
}

// Product Notifier
class ProductNotifier extends StateNotifier<ProductState> {
  final GetProductsUseCase _getProductsUseCase;

  ProductNotifier(this._getProductsUseCase) : super(const ProductState());

  Future<void> loadProducts({
    String? category,
    String? searchQuery,
  }) async {
    state = state.copyWith(isLoading: true, hasError: false);

    final result = await _getProductsUseCase.call(
      category: category,
      searchQuery: searchQuery,
    );

    result.fold(
      (products) => state = state.copyWith(
        products: products,
        isLoading: false,
        selectedCategory: category,
        searchQuery: searchQuery,
      ),
      (error) => state = state.copyWith(
        isLoading: false,
        hasError: true,
        errorMessage: error.message,
      ),
    );
  }

  void setCategory(String category) {
    state = state.copyWith(selectedCategory: category);
    loadProducts(category: category);
  }

  void setSearchQuery(String query) {
    state = state.copyWith(searchQuery: query);
    loadProducts(searchQuery: query);
  }
}
```

### **2. إعداد Provider | Provider Setup**
```dart
// Providers
final productNotifierProvider = StateNotifierProvider<ProductNotifier, ProductState>(
  (ref) => ProductNotifier(ref.read(getProductsUseCaseProvider)),
);

final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>(
  (ref) => AuthNotifier(ref.read(loginUseCaseProvider)),
);

// Use case providers
final getProductsUseCaseProvider = Provider<GetProductsUseCase>(
  (ref) => GetProductsUseCase(ref.read(productRepositoryProvider)),
);

final productRepositoryProvider = Provider<ProductRepository>(
  (ref) => ProductRepositoryImpl(
    remoteDataSource: ref.read(productRemoteDataSourceProvider),
    localDataSource: ref.read(productLocalDataSourceProvider),
    networkInfo: ref.read(networkInfoProvider),
  ),
);
```

## 🖼️ **مكونات واجهة المستخدم | UI Components**

### **1. مكونات واجهة المستخدم الأساسية | Base UI Components**
```dart
class LoadingWidget extends StatelessWidget {
  final String? message;
  
  const LoadingWidget({super.key, this.message});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(),
          if (message != null) ...[
            const SizedBox(height: 16),
            Text(
              message!,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ],
      ),
    );
  }
}

class ErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;
  
  const ErrorWidget({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.error_outline,
            size: 64,
            color: Theme.of(context).colorScheme.error,
          ),
          const SizedBox(height: 16),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyMedium,
            textAlign: TextAlign.center,
          ),
          if (onRetry != null) ...[
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: onRetry,
              child: const Text('Retry'),
            ),
          ],
        ],
      ),
    );
  }
}
```

### **2. عنصر قائمة المنتجات | Product List Widget**
```dart
class ProductListWidget extends ConsumerWidget {
  const ProductListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productState = ref.watch(productNotifierProvider);

    return productState.when(
      loading: () => const LoadingWidget(message: 'Loading products...'),
      error: (error) => ErrorWidget(
        message: error.message,
        onRetry: () => ref.read(productNotifierProvider.notifier).loadProducts(),
      ),
      data: (products) {
        if (products.isEmpty) {
          return const EmptyStateWidget(
            icon: Icons.shopping_bag_outlined,
            title: 'No products found',
            subtitle: 'Try adjusting your search or filters',
          );
        }

        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 0.7,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
          ),
          itemCount: products.length,
          itemBuilder: (context, index) {
            final product = products[index];
            return ProductCard(product: product);
          },
        );
      },
    );
  }
}
```

## 🎨 **إدارة حالة واجهة المستخدم | UI State Management**

### **1. حالات التحميل | Loading States**
```dart
class ProductDetailPage extends ConsumerWidget {
  final String productId;

  const ProductDetailPage({super.key, required this.productId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productState = ref.watch(productDetailNotifierProvider(productId));

    return Scaffold(
      appBar: AppBar(title: const Text('Product Details')),
      body: productState.when(
        loading: () => const LoadingWidget(message: 'Loading product...'),
        error: (error) => ErrorWidget(
          message: error.message,
          onRetry: () => ref.read(productDetailNotifierProvider(productId).notifier)
              .loadProduct(productId),
        ),
        data: (product) => ProductDetailContent(product: product),
      ),
    );
  }
}
```

### **2. معالجة الأخطاء | Error Handling**
```dart
class ErrorBoundary extends ConsumerWidget {
  final Widget child;
  final Widget Function(AppError error)? errorBuilder;

  const ErrorBoundary({
    super.key,
    required this.child,
    this.errorBuilder,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return child;
  }
}

class GlobalErrorHandler {
  static void handleError(AppError error, {StackTrace? stackTrace}) {
    // Log error
    ErrorLogger.logError(error, stackTrace: stackTrace);
    
    // Show user-friendly message
    // This would typically be handled by a global error handler
    // that shows snackbars or dialogs
  }
}
```

## 🧪 **اختبار طبقة العرض | Testing Presentation Layer**

### **1. اختبارات العناصر | Widget Tests**
```dart
void main() {
  group('ProductListWidget', () {
    testWidgets('should show loading state', (tester) async {
      // Arrange
      final container = ProviderContainer(
        overrides: [
          productNotifierProvider.overrideWith(
            (ref) => MockProductNotifier()..setLoading(true),
          ),
        ],
      );

      // Act
      await tester.pumpWidget(
        ProviderScope(
          parent: container,
          child: const MaterialApp(
            home: ProductListWidget(),
          ),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Loading products...'), findsOneWidget);
    });

    testWidgets('should show products when loaded', (tester) async {
      // Arrange
      final products = [
        Product(
          id: '1',
          name: 'Test Product',
          description: 'Test Description',
          price: 99.99,
          category: 'Electronics',
          images: ['image1.jpg'],
          stockQuantity: 10,
          isAvailable: true,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ),
      ];

      final container = ProviderContainer(
        overrides: [
          productNotifierProvider.overrideWith(
            (ref) => MockProductNotifier()..setProducts(products),
          ),
        ],
      );

      // Act
      await tester.pumpWidget(
        ProviderScope(
          parent: container,
          child: const MaterialApp(
            home: ProductListWidget(),
          ),
        ),
      );

      // Assert
      expect(find.text('Test Product'), findsOneWidget);
      expect(find.text('\$99.99'), findsOneWidget);
    });
  });
}
```

### **2. اختبارات التنقل | Navigation Tests**
```dart
void main() {
  group('Navigation Tests', () {
    testWidgets('should navigate to product detail', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp.router(
          routerConfig: AppRouter.router,
        ),
      );

      // Act
      await tester.tap(find.text('View Product'));
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(ProductDetailPage), findsOneWidget);
    });

    testWidgets('should redirect to login when not authenticated', (tester) async {
      // Arrange
      final container = ProviderContainer(
        overrides: [
          authNotifierProvider.overrideWith(
            (ref) => MockAuthNotifier()..setUnauthenticated(),
          ),
        ],
      );

      await tester.pumpWidget(
        ProviderScope(
          parent: container,
          child: MaterialApp.router(
            routerConfig: AppRouter.router,
          ),
        ),
      );

      // Act
      AppRouter.router.go('/profile');
      await tester.pumpAndSettle();

      // Assert
      expect(find.byType(LoginPage), findsOneWidget);
    });
  });
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Navigation**
- [ ] Set up GoRouter with route configuration
- [ ] Implement route guards for authentication
- [ ] Add deep linking support
- [ ] Test all navigation flows

### **2. State Management**
- [ ] Implement StateNotifier for UI state
- [ ] Set up providers for dependency injection
- [ ] Add proper error handling
- [ ] Test state management logic

### **3. UI Components**
- [ ] Create reusable UI components
- [ ] Implement loading and error states
- [ ] Add proper accessibility support
- [ ] Test all UI components

### **4. Deep Linking**
- [ ] Configure Firebase Dynamic Links
- [ ] Implement deep link handling
- [ ] Test deep link functionality
- [ ] Add proper error handling

### **5. Testing**
- [ ] Write widget tests for UI components
- [ ] Test navigation flows
- [ ] Test state management
- [ ] Achieve high test coverage

---

**Next Tab**: Design System | نظام التصميم

