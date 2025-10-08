# TAB 4: طبقة المجال | Domain Layer

## 4. طبقة المجال | Domain Layer
### تطبيق طبقة مجال نظيفة مع منطق الأعمال وحالات الاستخدام والكيانات

---

## 🎯 **الهدف | Objective**
تطبيق طبقة مجال نظيفة مع منطق الأعمال وحالات الاستخدام والكيانات تتبع مبادئ Domain-Driven Design لتطبيق Flutter للتجارة الإلكترونية.

## 📋 **القاعدة | Rule**
**العربية**: Use Cases في Domain، Entities مع freezed + json_serializable، Repository interfaces في Domain  
**English**: Use Cases in Domain, Entities with freezed + json_serializable, Repository interfaces in Domain

## 💡 **الفوائد | Benefits**
- **مركزية منطق الأعمال | Business Logic Centralization**: جميع قواعد الأعمال في مكان واحد
- **قابلية الاختبار | Testability**: سهولة اختبار منطق الأعمال بشكل مستقل
- **سهولة الصيانة | Maintainability**: فصل واضح للاهتمامات
- **إعادة الاستخدام | Reusability**: يمكن إعادة استخدام حالات الاستخدام عبر تطبيقات UI مختلفة
- **أمان الأنواع | Type Safety**: فحص وقت التجميع مع كيانات غير قابلة للتغيير
- **معمارية نظيفة | Clean Architecture**: تتبع مبادئ DDD

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع منطق الأعمال ونماذج البيانات وحالات الاستخدام
- **كيفية التطبيق**:
  - إنشاء كيانات المجال مع freezed
  - تطبيق حالات الاستخدام لعمليات الأعمال
  - تعريف واجهات المستودعات
  - إضافة قواعد التحقق من الأعمال
  - تطبيق خدمات المجال
- **النتيجة**: طبقة مجال نظيفة وقابلة للاختبار مع منطق أعمال واضح

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بطبقة المجال | Domain Layer Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إنشاء كيانات المجال مع freezed + json_serializable
- **🔴 حرج**: تطبيق حالات الاستخدام الأساسية لعمليات الأعمال
- **🟠 عالي**: تعريف واجهات المستودعات والعقود

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إضافة قواعد التحقق من الأعمال وخدمات المجال
- **🟠 عالي**: تطبيق اختبار شامل لحالات الاستخدام
- **🟡 متوسط**: إضافة أحداث المجال والتجميعات

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: أنماط مجال متقدمة ومنطق أعمال معقد
- **🟡 متوسط**: أنماط التصميم مدفوع بالمجال
- **🟢 منخفض**: تحسين منطق الأعمال مدعوم بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **مؤشرات خاصة بطبقة المجال | Domain Layer Specific Metrics:**
- **تغطية منطق الأعمال | Business Logic Coverage**: 100% قواعد أعمال في طبقة المجال
- **اكتمال حالات الاستخدام | Use Case Completeness**: 95%+ حالات استخدام مطبقة
- **عدم قابلية تغيير الكيانات | Entity Immutability**: 100% كيانات تستخدم freezed
- **تغطية الاختبار | Testing Coverage**: >90% تغطية اختبار طبقة المجال
- **أمان الأنواع | Type Safety**: صفر أخطاء نوع وقت التشغيل
- **جودة الكود | Code Quality**: >95% مؤشر قابلية الصيانة

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **أخطاء خاصة بطبقة المجال | Domain Layer Specific Pitfalls:**
- **تجنب**: منطق الأعمال في طبقات UI أو البيانات
- **تجنب**: كيانات قابلة للتغيير دون تحقق مناسب
- **تجنب**: حالات استخدام مفقودة للعمليات المعقدة
- **تجنب**: اقتران وثيق بين المجال والطبقات الخارجية
- **تجنب**: قواعد تحقق أعمال مفقودة

### **أفضل الممارسات | Best Practices:**
- **استخدم**: Freezed للكيانات غير القابلة للتغيير
- **استخدم**: حالات الاستخدام لجميع عمليات الأعمال
- **استخدم**: واجهات المستودعات للوصول للبيانات
- **استخدم**: خدمات المجال لمنطق الأعمال المعقد
- **استخدم**: كائنات القيمة لمفاهيم المجال

## 🏗️ **كيانات المجال | Domain Entities**

### **1. كيان المنتج | Product Entity**
```dart
@freezed
class Product with _$Product {
  const factory Product({
    required String id,
    required String name,
    required String description,
    required double price,
    required String category,
    required List<String> images,
    required int stockQuantity,
    required bool isAvailable,
    required DateTime createdAt,
    required DateTime updatedAt,
    String? brand,
    List<String>? tags,
    Map<String, dynamic>? specifications,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);
}
```

### **2. كيان المستخدم | User Entity**
```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String email,
    required String firstName,
    required String lastName,
    required String phoneNumber,
    required UserRole role,
    required DateTime createdAt,
    required DateTime updatedAt,
    String? profileImage,
    Address? defaultAddress,
    List<Address>? addresses,
    UserPreferences? preferences,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

@freezed
class Address with _$Address {
  const factory Address({
    required String id,
    required String street,
    required String city,
    required String state,
    required String country,
    required String postalCode,
    required bool isDefault,
    String? apartment,
    String? landmark,
  }) = _Address;

  factory Address.fromJson(Map<String, dynamic> json) => _$AddressFromJson(json);
}
```

### **3. كيان الطلب | Order Entity**
```dart
@freezed
class Order with _$Order {
  const factory Order({
    required String id,
    required String userId,
    required List<OrderItem> items,
    required double subtotal,
    required double tax,
    required double shipping,
    required double total,
    required OrderStatus status,
    required DateTime createdAt,
    required DateTime updatedAt,
    String? trackingNumber,
    Address? shippingAddress,
    Address? billingAddress,
    PaymentInfo? paymentInfo,
    List<OrderStatusHistory>? statusHistory,
  }) = _Order;

  factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);
}

@freezed
class OrderItem with _$OrderItem {
  const factory OrderItem({
    required String productId,
    required String productName,
    required double price,
    required int quantity,
    required String imageUrl,
    Map<String, dynamic>? productSpecifications,
  }) = _OrderItem;

  factory OrderItem.fromJson(Map<String, dynamic> json) => _$OrderItemFromJson(json);
}
```

## 🔧 **حالات الاستخدام | Use Cases**

### **1. حالة الاستخدام: الحصول على المنتجات | Get Products Use Case**
```dart
class GetProductsUseCase {
  final ProductRepository _repository;

  GetProductsUseCase(this._repository);

  Future<Result<List<Product>>> call({
    String? category,
    String? searchQuery,
    ProductSortBy? sortBy,
    int? limit,
    int? offset,
  }) async {
    try {
      // Business validation
      if (limit != null && (limit <= 0 || limit > 100)) {
        return const Failure(ValidationError('Invalid limit: must be between 1 and 100'));
      }

      if (offset != null && offset < 0) {
        return const Failure(ValidationError('Invalid offset: must be >= 0'));
      }

      // Call repository
      final result = await _repository.getProducts(
        category: category,
        searchQuery: searchQuery,
        sortBy: sortBy,
        limit: limit,
        offset: offset,
      );

      return result;
    } catch (e) {
      return Failure(DomainError('Failed to get products: $e'));
    }
  }
}
```

### **2. حالة الاستخدام: إضافة منتج للسلة | Add Product to Cart Use Case**
```dart
class AddProductToCartUseCase {
  final CartRepository _cartRepository;
  final ProductRepository _productRepository;

  AddProductToCartUseCase(this._cartRepository, this._productRepository);

  Future<Result<void>> call({
    required String userId,
    required String productId,
    required int quantity,
  }) async {
    try {
      // Business validation
      if (quantity <= 0) {
        return const Failure(ValidationError('Quantity must be greater than 0'));
      }

      // Check product availability
      final productResult = await _productRepository.getProductById(productId);
      if (productResult is Failure) {
        return productResult;
      }

      final product = (productResult as Success<Product>).data;
      if (!product.isAvailable) {
        return const Failure(BusinessError('Product is not available'));
      }

      if (product.stockQuantity < quantity) {
        return Failure(BusinessError(
          'Insufficient stock. Available: ${product.stockQuantity}, Requested: $quantity'
        ));
      }

      // Add to cart
      final cartResult = await _cartRepository.addItem(
        userId: userId,
        productId: productId,
        quantity: quantity,
      );

      return cartResult;
    } catch (e) {
      return Failure(DomainError('Failed to add product to cart: $e'));
    }
  }
}
```

### **3. حالة الاستخدام: إنشاء طلب | Create Order Use Case**
```dart
class CreateOrderUseCase {
  final OrderRepository _orderRepository;
  final CartRepository _cartRepository;
  final ProductRepository _productRepository;

  CreateOrderUseCase(
    this._orderRepository,
    this._cartRepository,
    this._productRepository,
  );

  Future<Result<Order>> call({
    required String userId,
    required Address shippingAddress,
    required Address billingAddress,
    required PaymentInfo paymentInfo,
  }) async {
    try {
      // Get cart items
      final cartResult = await _cartRepository.getCart(userId);
      if (cartResult is Failure) {
        return cartResult;
      }

      final cart = (cartResult as Success<Cart>).data;
      if (cart.items.isEmpty) {
        return const Failure(BusinessError('Cart is empty'));
      }

      // Validate all products are still available
      for (final item in cart.items) {
        final productResult = await _productRepository.getProductById(item.productId);
        if (productResult is Failure) {
          return Failure(BusinessError('Product ${item.productName} is no longer available'));
        }

        final product = (productResult as Success<Product>).data;
        if (!product.isAvailable || product.stockQuantity < item.quantity) {
          return Failure(BusinessError(
            'Insufficient stock for ${item.productName}. Available: ${product.stockQuantity}'
          ));
        }
      }

      // Calculate totals
      final subtotal = cart.items.fold(0.0, (sum, item) => sum + (item.price * item.quantity));
      final tax = subtotal * 0.1; // 10% tax
      final shipping = subtotal > 100 ? 0.0 : 10.0; // Free shipping over $100
      final total = subtotal + tax + shipping;

      // Create order
      final order = Order(
        id: const Uuid().v4(),
        userId: userId,
        items: cart.items,
        subtotal: subtotal,
        tax: tax,
        shipping: shipping,
        total: total,
        status: OrderStatus.pending,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        shippingAddress: shippingAddress,
        billingAddress: billingAddress,
        paymentInfo: paymentInfo,
      );

      // Save order
      final orderResult = await _orderRepository.createOrder(order);
      if (orderResult is Failure) {
        return orderResult;
      }

      // Clear cart
      await _cartRepository.clearCart(userId);

      return Success(order);
    } catch (e) {
      return Failure(DomainError('Failed to create order: $e'));
    }
  }
}
```

## 🏪 **واجهات المستودعات | Repository Interfaces**

### **1. واجهة مستودع المنتجات | Product Repository Interface**
```dart
abstract class ProductRepository {
  Future<Result<List<Product>>> getProducts({
    String? category,
    String? searchQuery,
    ProductSortBy? sortBy,
    int? limit,
    int? offset,
  });
  
  Future<Result<Product>> getProductById(String id);
  Future<Result<List<Product>>> getProductsByCategory(String category);
  Future<Result<List<Product>>> searchProducts(String query);
  Future<Result<Product>> createProduct(Product product);
  Future<Result<Product>> updateProduct(Product product);
  Future<Result<void>> deleteProduct(String id);
  Future<Result<List<Product>>> getFeaturedProducts();
  Future<Result<List<Product>>> getRecommendedProducts(String userId);
}
```

### **2. واجهة مستودع السلة | Cart Repository Interface**
```dart
abstract class CartRepository {
  Future<Result<Cart>> getCart(String userId);
  Future<Result<void>> addItem({
    required String userId,
    required String productId,
    required int quantity,
  });
  Future<Result<void>> updateItemQuantity({
    required String userId,
    required String productId,
    required int quantity,
  });
  Future<Result<void>> removeItem({
    required String userId,
    required String productId,
  });
  Future<Result<void>> clearCart(String userId);
  Future<Result<int>> getCartItemCount(String userId);
  Future<Result<double>> getCartTotal(String userId);
}
```

### **3. واجهة مستودع الطلبات | Order Repository Interface**
```dart
abstract class OrderRepository {
  Future<Result<Order>> createOrder(Order order);
  Future<Result<Order>> getOrderById(String id);
  Future<Result<List<Order>>> getOrdersByUserId(String userId);
  Future<Result<Order>> updateOrderStatus(String orderId, OrderStatus status);
  Future<Result<void>> cancelOrder(String orderId);
  Future<Result<List<Order>>> getOrdersByStatus(OrderStatus status);
  Future<Result<Order>> addTrackingNumber(String orderId, String trackingNumber);
}
```

## 🎯 **خدمات المجال | Domain Services**

### **1. خدمة التسعير | Pricing Service**
```dart
class PricingService {
  static double calculateSubtotal(List<OrderItem> items) {
    return items.fold(0.0, (sum, item) => sum + (item.price * item.quantity));
  }

  static double calculateTax(double subtotal, {double taxRate = 0.1}) {
    return subtotal * taxRate;
  }

  static double calculateShipping(double subtotal, {double freeShippingThreshold = 100.0}) {
    return subtotal >= freeShippingThreshold ? 0.0 : 10.0;
  }

  static double calculateTotal(double subtotal, double tax, double shipping) {
    return subtotal + tax + shipping;
  }

  static bool isEligibleForFreeShipping(double subtotal, {double threshold = 100.0}) {
    return subtotal >= threshold;
  }
}
```

### **2. خدمة التحقق | Validation Service**
```dart
class ValidationService {
  static Result<void> validateEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(email)) {
      return const Failure(ValidationError('Invalid email format'));
    }
    return const Success(null);
  }

  static Result<void> validatePhoneNumber(String phoneNumber) {
    final phoneRegex = RegExp(r'^\+?[1-9]\d{1,14}$');
    if (!phoneRegex.hasMatch(phoneNumber)) {
      return const Failure(ValidationError('Invalid phone number format'));
    }
    return const Success(null);
  }

  static Result<void> validatePassword(String password) {
    if (password.length < 8) {
      return const Failure(ValidationError('Password must be at least 8 characters'));
    }
    
    if (!password.contains(RegExp(r'[A-Z]'))) {
      return const Failure(ValidationError('Password must contain at least one uppercase letter'));
    }
    
    if (!password.contains(RegExp(r'[a-z]'))) {
      return const Failure(ValidationError('Password must contain at least one lowercase letter'));
    }
    
    if (!password.contains(RegExp(r'[0-9]'))) {
      return const Failure(ValidationError('Password must contain at least one number'));
    }
    
    return const Success(null);
  }
}
```

## 🧪 **اختبار طبقة المجال | Testing Domain Layer**

### **1. اختبارات الكيانات | Entity Tests**
```dart
void main() {
  group('Product Entity', () {
    test('should create product with required fields', () {
      final product = Product(
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
      );

      expect(product.id, '1');
      expect(product.name, 'Test Product');
      expect(product.price, 99.99);
      expect(product.isAvailable, true);
    });

    test('should serialize and deserialize correctly', () {
      final product = Product(
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
      );

      final json = product.toJson();
      final fromJson = Product.fromJson(json);

      expect(fromJson, equals(product));
    });
  });
}
```

### **2. اختبارات حالات الاستخدام | Use Case Tests**
```dart
void main() {
  group('AddProductToCartUseCase', () {
    late AddProductToCartUseCase useCase;
    late MockCartRepository mockCartRepository;
    late MockProductRepository mockProductRepository;

    setUp(() {
      mockCartRepository = MockCartRepository();
      mockProductRepository = MockProductRepository();
      useCase = AddProductToCartUseCase(mockCartRepository, mockProductRepository);
    });

    test('should add product to cart successfully', () async {
      // Arrange
      const userId = 'user1';
      const productId = 'product1';
      const quantity = 2;
      
      final product = Product(
        id: productId,
        name: 'Test Product',
        description: 'Test Description',
        price: 99.99,
        category: 'Electronics',
        images: ['image1.jpg'],
        stockQuantity: 10,
        isAvailable: true,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      when(mockProductRepository.getProductById(productId))
          .thenAnswer((_) async => Success(product));
      when(mockCartRepository.addItem(
        userId: userId,
        productId: productId,
        quantity: quantity,
      )).thenAnswer((_) async => const Success(null));

      // Act
      final result = await useCase.call(
        userId: userId,
        productId: productId,
        quantity: quantity,
      );

      // Assert
      expect(result, isA<Success<void>>());
      verify(mockProductRepository.getProductById(productId));
      verify(mockCartRepository.addItem(
        userId: userId,
        productId: productId,
        quantity: quantity,
      ));
    });

    test('should return validation error for invalid quantity', () async {
      // Act
      final result = await useCase.call(
        userId: 'user1',
        productId: 'product1',
        quantity: 0,
      );

      // Assert
      expect(result, isA<Failure<void>>());
      expect((result as Failure).error, isA<ValidationError>());
    });
  });
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. الكيانات | Entities**
- [ ] إنشاء كيانات المجال مع freezed
- [ ] إضافة json_serializable للتسلسل
- [ ] تطبيق التحقق المناسب
- [ ] إضافة قواعد الأعمال للكيانات

### **2. حالات الاستخدام | Use Cases**
- [ ] إنشاء حالات الاستخدام لجميع عمليات الأعمال
- [ ] إضافة التحقق المناسب في حالات الاستخدام
- [ ] تطبيق معالجة الأخطاء
- [ ] إضافة اختبار شامل

### **3. واجهات المستودعات | Repository Interfaces**
- [ ] تعريف واجهات المستودعات
- [ ] إضافة توقيعات الطرق المناسبة
- [ ] تضمين جميع العمليات الضرورية
- [ ] توثيق عقود الواجهة

### **4. خدمات المجال | Domain Services**
- [ ] إنشاء خدمات المجال للمنطق المعقد
- [ ] تطبيق حسابات الأعمال
- [ ] إضافة خدمات التحقق
- [ ] اختبار جميع خدمات المجال

### **5. الاختبار | Testing**
- [ ] كتابة اختبارات وحدة للكيانات
- [ ] اختبار جميع حالات الاستخدام
- [ ] اختبار خدمات المجال
- [ ] تحقيق تغطية اختبار عالية

---

**التبويب التالي**: طبقة العرض | Presentation Layer

