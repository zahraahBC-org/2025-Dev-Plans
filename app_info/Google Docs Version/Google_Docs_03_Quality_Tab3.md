# TAB 3: الأمان والخصوصية | Security & Privacy

## 13. الأمان والخصوصية
### Security & Privacy

---

## 🎯 **الهدف | Objective**
تطبيق تدابير أمان وخصوصية شاملة لتطبيق Flutter للتجارة الإلكترونية قوي وقابل للصيانة.

## 📋 **القاعدة | Rule**
**العربية**: خزّن الرموز في flutter_secure_storage، لا تسجّل بيانات حسّاسة، وفكّر في TLS pinning  
**English**: Store tokens in flutter_secure_storage, don't log sensitive data, consider TLS pinning

## 💡 **الفوائد | Benefits**
- **حماية البيانات | Data Protection**: تخزين آمن للمعلومات الحساسة
- **الامتثال للخصوصية | Privacy Compliance**: تلبية لوائح الخصوصية
- **ثقة المستخدم | User Trust**: بناء ثقة المستخدم
- **أفضل ممارسات الأمان | Security Best Practices**: اتباع معايير الصناعة
- **تخفيف المخاطر | Risk Mitigation**: تقليل نقاط الضعف الأمنية
- **جاهزية التدقيق | Audit Readiness**: تلبية متطلبات الامتثال

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع تخزين البيانات واتصالات API ومصادقة المستخدم
- **كيفية التطبيق**:
  - استخدام flutter_secure_storage للرموز
  - تطبيق تشفير البيانات المناسب
  - إضافة TLS pinning لاستدعاءات API
  - إزالة البيانات الحساسة من السجلات
  - تطبيق إدارة جلسة مناسبة
- **النتيجة**: تطبيق آمن ومتوافق مع الخصوصية

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بالأمان والخصوصية | Security & Privacy Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: تطبيق تخزين رموز آمن
- **🔴 حرج**: إضافة تشفير وحماية البيانات
- **🟠 عالي**: إعداد TLS pinning والتواصل الآمن

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تطبيق أمان السجلات الشامل
- **🟠 عالي**: إضافة تدابير الامتثال للخصوصية
- **🟡 متوسط**: تطبيق ميزات أمان متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: مراقبة أمان متقدمة
- **🟡 متوسط**: تحليل أمان مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: تدابير أمان تنبؤية

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بالأمان والخصوصية | Security & Privacy Specific Metrics:**
- **درجة الأمان | Security Score**: 100% security audit compliance
- **حماية البيانات | Data Protection**: 100% sensitive data encrypted
- **الامتثال للخصوصية | Privacy Compliance**: 100% privacy regulation compliance
- **معدل الثغرات | Vulnerability Rate**: Zero critical vulnerabilities
- **خرق البيانات | Data Breach**: Zero data breaches
- **ثقة المستخدم | User Trust**: >95% user trust rating

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بالأمان والخصوصية | Security & Privacy Specific Pitfalls:**
- **تجنب | Avoid**: تخزين البيانات الحساسة كنص عادي
- **تجنب | Avoid**: تسجيل المعلومات الحساسة
- **تجنب | Avoid**: تواصل API غير آمن
- **تجنب | Avoid**: إدارة جلسة ضعيفة
- **تجنب | Avoid**: عدم وجود امتثال للخصوصية

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: تخزين آمن للبيانات الحساسة
- **استخدم | Use**: تشفير بيانات مناسب
- **استخدم | Use**: TLS pinning لاستدعاءات API
- **استخدم | Use**: ممارسات تسجيل آمنة
- **استخدم | Use**: تدابير الامتثال للخصوصية

## 🔐 **Secure Storage | التخزين الآمن**

### **1. Token Storage | تخزين الرموز**
```dart
// lib/core/security/secure_storage.dart
class SecureStorageService {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
    ),
    iOptions: IOSOptions(
      accessibility: KeychainAccessibility.first_unlock_this_device,
    ),
  );
  
  static Future<void> storeToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
  }
  
  static Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }
  
  static Future<void> deleteToken() async {
    await _storage.delete(key: 'auth_token');
  }
  
  static Future<void> storeRefreshToken(String refreshToken) async {
    await _storage.write(key: 'refresh_token', value: refreshToken);
  }
  
  static Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'refresh_token');
  }
  
  static Future<void> deleteRefreshToken() async {
    await _storage.delete(key: 'refresh_token');
  }
  
  static Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
```

### **2. Data Encryption | تشفير البيانات**
```dart
// lib/core/security/encryption.dart
class EncryptionService {
  static const String _key = 'your-32-character-secret-key';
  
  static String encrypt(String plainText) {
    final key = Key.fromBase64(_key);
    final iv = IV.fromSecureRandom(16);
    final encrypter = Encrypter(AES(key));
    final encrypted = encrypter.encrypt(plainText, iv: iv);
    return '${iv.base64}:${encrypted.base64}';
  }
  
  static String decrypt(String encryptedText) {
    final parts = encryptedText.split(':');
    final iv = IV.fromBase64(parts[0]);
    final encrypted = Encrypted.fromBase64(parts[1]);
    final key = Key.fromBase64(_key);
    final encrypter = Encrypter(AES(key));
    return encrypter.decrypt(encrypted, iv: iv);
  }
}
```

## 🌐 **Secure Communication | التواصل الآمن**

### **1. TLS Pinning | تثبيت TLS**
```dart
// lib/core/network/secure_http_client.dart
class SecureHttpClient {
  static Dio createSecureClient() {
    final dio = Dio();
    
    // Add TLS pinning
    (dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = (client) {
      client.badCertificateCallback = (cert, host, port) {
        // Implement certificate pinning
        return _verifyCertificate(cert, host);
      };
      return client;
    };
    
    // Add security headers
    dio.interceptors.add(SecurityInterceptor());
    
    return dio;
  }
  
  static bool _verifyCertificate(X509Certificate cert, String host) {
    // Implement certificate pinning logic
    final expectedCert = 'your-expected-certificate-hash';
    final actualCert = cert.sha1.toString();
    return actualCert == expectedCert;
  }
}

class SecurityInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    // Add security headers
    options.headers['X-Content-Type-Options'] = 'nosniff';
    options.headers['X-Frame-Options'] = 'DENY';
    options.headers['X-XSS-Protection'] = '1; mode=block';
    options.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains';
    
    handler.next(options);
  }
}
```

### **2. API Security | أمان API**
```dart
// lib/core/network/api_security.dart
class ApiSecurityService {
  static String generateApiSignature({
    required String method,
    required String url,
    required Map<String, dynamic> params,
    required String timestamp,
  }) {
    final sortedParams = Map.fromEntries(
      params.entries.toList()..sort((a, b) => a.key.compareTo(b.key)),
    );
    
    final queryString = sortedParams.entries
        .map((e) => '${e.key}=${e.value}')
        .join('&');
    
    final signatureString = '$method$url$queryString$timestamp';
    final signature = sha256.convert(utf8.encode(signatureString)).toString();
    
    return signature;
  }
  
  static Map<String, String> getSecurityHeaders({
    required String method,
    required String url,
    required Map<String, dynamic> params,
  }) {
    final timestamp = DateTime.now().millisecondsSinceEpoch.toString();
    final signature = generateApiSignature(
      method: method,
      url: url,
      params: params,
      timestamp: timestamp,
    );
    
    return {
      'X-API-Timestamp': timestamp,
      'X-API-Signature': signature,
      'X-API-Version': '1.0',
    };
  }
}
```

## 🔒 **Authentication Security | أمان المصادقة**

### **1. Secure Authentication | المصادقة الآمنة**
```dart
// lib/features/auth/data/datasources/auth_remote_datasource.dart
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio _dio;
  final SecureStorageService _secureStorage;
  
  AuthRemoteDataSourceImpl({
    required Dio dio,
    required SecureStorageService secureStorage,
  }) : _dio = dio, _secureStorage = secureStorage;
  
  @override
  Future<Result<AuthResponse>> login({
    required String email,
    required String password,
  }) async {
    try {
      // Hash password before sending
      final hashedPassword = _hashPassword(password);
      
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': hashedPassword,
        },
        options: Options(
          headers: ApiSecurityService.getSecurityHeaders(
            method: 'POST',
            url: '/auth/login',
            params: {'email': email},
          ),
        ),
      );
      
      if (response.statusCode == 200) {
        final authResponse = AuthResponse.fromJson(response.data);
        
        // Store tokens securely
        await _secureStorage.storeToken(authResponse.accessToken);
        await _secureStorage.storeRefreshToken(authResponse.refreshToken);
        
        return Success(authResponse);
      } else {
        return Failure(ServerError('Login failed'));
      }
    } catch (e) {
      return Failure(NetworkError('Login failed: $e'));
    }
  }
  
  String _hashPassword(String password) {
    // Implement secure password hashing
    final bytes = utf8.encode(password);
    final digest = sha256.convert(bytes);
    return digest.toString();
  }
}
```

### **2. Session Management | إدارة الجلسات**
```dart
// lib/core/security/session_manager.dart
class SessionManager {
  static Timer? _sessionTimer;
  static const Duration _sessionTimeout = Duration(minutes: 30);
  
  static void startSession() {
    _sessionTimer?.cancel();
    _sessionTimer = Timer(_sessionTimeout, () {
      _handleSessionTimeout();
    });
  }
  
  static void refreshSession() {
    startSession();
  }
  
  static void endSession() {
    _sessionTimer?.cancel();
    SecureStorageService.clearAll();
  }
  
  static void _handleSessionTimeout() {
    // Handle session timeout
    endSession();
    // Navigate to login screen
    AppRouter.router.go('/login');
  }
}
```

## 📝 **Secure Logging | التسجيل الآمن**

### **1. Secure Logger | مسجل آمن**
```dart
// lib/core/logging/secure_logger.dart
class SecureLogger {
  static void logInfo(String message) {
    if (kDebugMode) {
      print('INFO: $message');
    }
  }
  
  static void logError(String message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) {
      print('ERROR: $message');
      if (error != null) {
        print('Error: $error');
      }
      if (stackTrace != null) {
        print('Stack trace: $stackTrace');
      }
    }
    
    // Send to crash reporting service (without sensitive data)
    FirebaseCrashlytics.instance.recordError(
      _sanitizeError(error),
      stackTrace,
      fatal: false,
    );
  }
  
  static void logSecurityEvent(String event, Map<String, dynamic>? data) {
    final sanitizedData = _sanitizeData(data);
    
    if (kDebugMode) {
      print('SECURITY: $event - $sanitizedData');
    }
    
    // Send to security monitoring service
    _sendSecurityEvent(event, sanitizedData);
  }
  
  static dynamic _sanitizeError(dynamic error) {
    if (error is String) {
      return _sanitizeString(error);
    }
    return error;
  }
  
  static Map<String, dynamic>? _sanitizeData(Map<String, dynamic>? data) {
    if (data == null) return null;
    
    final sanitized = <String, dynamic>{};
    for (final entry in data.entries) {
      if (_isSensitiveKey(entry.key)) {
        sanitized[entry.key] = '[REDACTED]';
      } else {
        sanitized[entry.key] = _sanitizeValue(entry.value);
      }
    }
    return sanitized;
  }
  
  static String _sanitizeString(String input) {
    // Remove sensitive patterns
    return input
        .replaceAll(RegExp(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'), '[CARD]')
        .replaceAll(RegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[EMAIL]')
        .replaceAll(RegExp(r'\b\d{3}-\d{2}-\d{4}\b'), '[SSN]');
  }
  
  static bool _isSensitiveKey(String key) {
    final sensitiveKeys = [
      'password',
      'token',
      'secret',
      'key',
      'ssn',
      'credit_card',
      'email',
      'phone',
    ];
    return sensitiveKeys.any((sensitive) => key.toLowerCase().contains(sensitive));
  }
  
  static dynamic _sanitizeValue(dynamic value) {
    if (value is String) {
      return _sanitizeString(value);
    }
    return value;
  }
  
  static void _sendSecurityEvent(String event, Map<String, dynamic>? data) {
    // Send to security monitoring service
    // Implementation depends on your security monitoring solution
  }
}
```

## 🛡️ **Privacy Compliance | الامتثال للخصوصية**

### **1. Privacy Manager | مدير الخصوصية**
```dart
// lib/core/privacy/privacy_manager.dart
class PrivacyManager {
  static Future<void> requestPermissions() async {
    // Request necessary permissions
    await Permission.camera.request();
    await Permission.storage.request();
    await Permission.location.request();
  }
  
  static Future<void> handleDataDeletion(String userId) async {
    // Delete user data
    await _deleteUserData(userId);
    await _deleteUserFiles(userId);
    await _deleteUserCache(userId);
  }
  
  static Future<void> handleDataExport(String userId) async {
    // Export user data
    final userData = await _exportUserData(userId);
    // Send to user
  }
  
  static Future<void> _deleteUserData(String userId) async {
    // Delete user data from database
  }
  
  static Future<void> _deleteUserFiles(String userId) async {
    // Delete user files
  }
  
  static Future<void> _deleteUserCache(String userId) async {
    // Delete user cache
  }
  
  static Future<Map<String, dynamic>> _exportUserData(String userId) async {
    // Export user data
    return {};
  }
}
```

### **2. Privacy Policy | سياسة الخصوصية**
```dart
// lib/features/privacy/presentation/pages/privacy_policy_page.dart
class PrivacyPolicyPage extends StatelessWidget {
  const PrivacyPolicyPage({super.key});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy Policy'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Privacy Policy',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            const Text(
              'Last updated: ${DateTime.now().toString().split(' ')[0]}',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            const Text(
              '1. Information We Collect',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'We collect information you provide directly to us, such as when you create an account, make a purchase, or contact us for support.',
            ),
            const SizedBox(height: 16),
            const Text(
              '2. How We Use Your Information',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'We use the information we collect to provide, maintain, and improve our services.',
            ),
            const SizedBox(height: 16),
            const Text(
              '3. Data Security',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'We implement appropriate security measures to protect your personal information.',
            ),
            const SizedBox(height: 16),
            const Text(
              '4. Your Rights',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'You have the right to access, update, or delete your personal information.',
            ),
          ],
        ),
      ),
    );
  }
}
```

## 🔍 **Security Testing | اختبار الأمان**

### **1. Security Test Suite | مجموعة اختبارات الأمان**
```dart
// test/security/security_test.dart
void main() {
  group('Security Tests', () {
    test('should store tokens securely', () async {
      const token = 'test-token';
      
      await SecureStorageService.storeToken(token);
      final retrievedToken = await SecureStorageService.getToken();
      
      expect(retrievedToken, equals(token));
    });
    
    test('should encrypt sensitive data', () {
      const plainText = 'sensitive-data';
      
      final encrypted = EncryptionService.encrypt(plainText);
      final decrypted = EncryptionService.decrypt(encrypted);
      
      expect(decrypted, equals(plainText));
      expect(encrypted, isNot(equals(plainText)));
    });
    
    test('should sanitize sensitive data in logs', () {
      const sensitiveData = 'user@example.com';
      
      final sanitized = SecureLogger._sanitizeString(sensitiveData);
      
      expect(sanitized, equals('[EMAIL]'));
    });
  });
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. التخزين الآمن | Secure Storage**
- [ ] تطبيق تخزين رموز آمن
- [ ] إضافة تشفير البيانات
- [ ] إعداد إدارة جلسة آمنة
- [ ] اختبار وظائف التخزين الآمن

### **2. التواصل الآمن | Secure Communication**
- [ ] تطبيق TLS pinning
- [ ] إضافة رؤوس أمان
- [ ] إعداد أمان API
- [ ] اختبار التواصل الآمن

### **3. أمان المصادقة | Authentication Security**
- [ ] تطبيق مصادقة آمنة
- [ ] إضافة تشفير كلمات المرور
- [ ] إعداد إدارة الجلسة
- [ ] اختبار أمان المصادقة

### **4. التسجيل الآمن | Secure Logging**
- [ ] تطبيق تسجيل آمن
- [ ] إضافة تنظيف البيانات
- [ ] إعداد تسجيل أحداث الأمان
- [ ] اختبار أمان التسجيل

### **5. الامتثال للخصوصية | Privacy Compliance**
- [ ] تطبيق مدير الخصوصية
- [ ] إضافة وظائف حذف البيانات
- [ ] إعداد سياسة الخصوصية
- [ ] اختبار الامتثال للخصوصية

---

**Next Tab**: Monitoring & Analytics | المراقبة والتحليلات

