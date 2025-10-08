# ملحق د: أمثلة الكود | Appendix D: Code Examples
## Flutter وPython | Flutter and Python Examples

### 📋 **معلومات الملحق | Appendix Information**

**الهدف**: أمثلة كود عملية للتكامل مع قاعدة البيانات  
**Purpose**: Practical code examples for database integration

**الجمهور**: مطورو Flutter، مطورو الواجهة الخلفية  
**Audience**: Flutter developers, backend developers

---

## 🎯 **نظرة عامة | Overview**

هذا الملحق يوفر أمثلة كود جاهزة للاستخدام للتكامل مع قاعدة البيانات من تطبيق Flutter والواجهة الخلفية.

---

## 📱 **أمثلة Flutter | Flutter Examples**

### **1. تسجيل الدخول مع Firebase Analytics**

```dart
import 'package:firebase_analytics/firebase_analytics.dart';

class AuthService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  
  Future<void> onUserLogin(String userId) async {
    // تعيين user_id في Firebase Analytics
    await _analytics.setUserId(id: userId);
    
    // تسجيل حدث تسجيل الدخول
    await _analytics.logEvent(
      name: 'login',
      parameters: {
        'method': 'phone',
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      },
    );
    
    // حفظ في التخزين المحلي
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_id', userId);
  }
  
  Future<void> onUserLogout() async {
    // إزالة user_id
    await _analytics.setUserId(id: null);
    
    // إعادة تعيين بيانات التحليلات
    await _analytics.resetAnalyticsData();
    
    // حذف من التخزين المحلي
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user_id');
  }
}
```

---

### **2. تتبع أحداث التجارة الإلكترونية**

```dart
class AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  
  // عرض منتج
  Future<void> trackViewItem({
    required String skuId,
    required double price,
    required String currency,
    required String category,
  }) async {
    await _analytics.logEvent(
      name: 'view_item',
      parameters: {
        'sku_id': skuId,
        'price': price,
        'currency': currency,
        'category': category,
      },
    );
  }
  
  // إضافة لسلة
  Future<void> trackAddToCart({
    required String skuId,
    required int quantity,
    required double price,
  }) async {
    await _analytics.logEvent(
      name: 'add_to_cart',
      parameters: {
        'sku_id': skuId,
        'quantity': quantity,
        'price': price,
        'currency': 'SAR',
      },
    );
  }
  
  // بدء الدفع
  Future<void> trackBeginCheckout({
    required double cartValue,
    required int itemsCount,
  }) async {
    await _analytics.logEvent(
      name: 'begin_checkout',
      parameters: {
        'cart_value': cartValue,
        'items_count': itemsCount,
        'currency': 'SAR',
      },
    );
  }
  
  // إتمام الشراء
  Future<void> trackPurchase({
    required String orderId,
    required double value,
    required String currency,
    required List<Map<String, dynamic>> items,
  }) async {
    await _analytics.logEvent(
      name: 'purchase',
      parameters: {
        'order_id': orderId,
        'value': value,
        'currency': currency,
        'transaction_id': orderId,
        'items': items,
      },
    );
  }
}
```

---

## 🐍 **أمثلة Python (Backend) | Python Examples**

### **1. إنشاء طلب**

```python
from decimal import Decimal
import pymysql

def create_order(customer_id, cart_items, shipping_address_id):
    """
    إنشاء طلب جديد مع حجز المخزون
    """
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            # بدء المعاملة
            connection.begin()
            
            # 1. حساب المجاميع
            subtotal = Decimal('0.00')
            for item in cart_items:
                subtotal += item['unit_price'] * item['quantity']
            
            # 2. إنشاء الطلب
            cursor.execute("""
                INSERT INTO orders (
                    order_no, customer_id, shipping_address_id,
                    subtotal, total, currency, status, payment_method
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                generate_order_no(),
                customer_id,
                shipping_address_id,
                subtotal,
                subtotal,  # بعد الخصم والشحن
                'SAR',
                'created',
                'cod'
            ))
            
            order_id = cursor.lastrowid
            
            # 3. إضافة بنود الطلب
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id, variant_id, quantity,
                        unit_price, line_total
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    order_id,
                    item['variant_id'],
                    item['quantity'],
                    item['unit_price'],
                    item['unit_price'] * item['quantity']
                ))
                
                # 4. حجز المخزون
                cursor.execute("""
                    INSERT INTO inventory_ledger (
                        variant_id, warehouse_id, movement_type,
                        quantity, reference_type, reference_id,
                        movement_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (
                    item['variant_id'],
                    1,  # warehouse_id
                    'reservation',
                    -item['quantity'],
                    'order',
                    order_id
                ))
            
            # 5. تأكيد المعاملة
            connection.commit()
            
            return order_id
            
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
```

---

### **2. معالجة دفع بالمحفظة**

```python
def process_wallet_payment(customer_id, order_id, amount):
    """
    معالجة دفع من محفظة العميل
    """
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            connection.begin()
            
            # 1. قفل المحفظة
            cursor.execute("""
                SELECT wallet_id, balance_available
                FROM wallets
                WHERE customer_id = %s
                FOR UPDATE
            """, (customer_id,))
            
            wallet = cursor.fetchone()
            
            if not wallet or wallet['balance_available'] < amount:
                raise InsufficientBalanceError('رصيد غير كافٍ')
            
            # 2. إنشاء معاملة خصم
            cursor.execute("""
                INSERT INTO wallet_transactions (
                    wallet_id, customer_id, type, amount,
                    currency, source, reference_type, reference_id,
                    status, balance_before, balance_after,
                    reason_code, performed_by_type, transaction_date
                ) VALUES (
                    %s, %s, 'debit', %s, 'SAR', 'purchase',
                    'order', %s, 'posted', %s, %s,
                    'order_payment', 'system', NOW()
                )
            """, (
                wallet['wallet_id'],
                customer_id,
                amount,
                order_id,
                wallet['balance_available'],
                wallet['balance_available'] - amount
            ))
            
            # 3. تحديث رصيد المحفظة
            cursor.execute("""
                UPDATE wallets
                SET balance_available = balance_available - %s,
                    updated_at = NOW()
                WHERE wallet_id = %s
            """, (amount, wallet['wallet_id']))
            
            # 4. تحديث حالة الطلب
            cursor.execute("""
                UPDATE orders
                SET payment_status = 'captured',
                    paid_at = NOW()
                WHERE order_id = %s
            """, (order_id,))
            
            connection.commit()
            
            return True
            
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
```

---

## 🔗 **الروابط ذات الصلة | Related Links**

- [08. نظام المحفظة | Wallet System](../08_Wallet_System.md)
- [02. معمارية قاعدة البيانات | Database Architecture](../02_Database_Architecture.md)
- [🏠 الفهرس الرئيسي | Main Index](../index.md)

---

**إصدار الملحق | Appendix Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08
