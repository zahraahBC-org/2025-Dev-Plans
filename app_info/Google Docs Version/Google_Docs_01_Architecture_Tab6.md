# TAB 6: نظام التصميم | Design System

## 6. نظام التصميم والثيمات | Design System & Theming
### تطبيق نظام تصميم موحد مع ثيمات متسقة ومكونات قابلة لإعادة الاستخدام

---

## 🎯 **الهدف | Objective**
تطبيق نظام تصميم موحد مع ثيمات متسقة ومكونات قابلة لإعادة الاستخدام ودعم RTL كامل لتطبيق التجارة الإلكترونية العربي.

## 📋 **القاعدة | Rule**
**العربية**: Theme واحد + Tokens (ألوان/هوامش/زوايا/Typography) + Widgets مشتركة (Buttons, Cards…)  
**English**: One Theme + Tokens (Colors/Spacing/Radius/Typography) + Shared Widgets (Buttons, Cards…)

## 💡 **الفوائد | Benefits**
- **الاتساق | Consistency**: مظهر وملمس موحد عبر التطبيق بأكمله
- **سهولة الصيانة | Maintainability**: سهولة تحديث التصميم عالمياً بتغيير واحد
- **سرعة التطوير | Development Speed**: المكونات القابلة لإعادة الاستخدام تقلل وقت التطوير
- **الهوية التجارية | Brand Identity**: تمثيل علامة تجارية متسق والاعتراف
- **تجربة المستخدم | User Experience**: أنماط مألوفة وواجهة بديهية
- **إمكانية الوصول | Accessibility**: ميزات إمكانية وصول مدمجة ودعم RTL

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع مكونات UI والشاشات وتفاعلات المستخدم
- **كيفية التطبيق**:
  - إنشاء تكوين ثيم مركزي
  - تعريف design tokens (ألوان، تباعد، طباعة، نصف قطر)
  - بناء مكتبة مكونات قابلة لإعادة الاستخدام
  - تطبيق دعم RTL شامل
  - إضافة ميزات إمكانية الوصول
  - إنشاء توثيق المكونات
- **النتيجة**: نظام UI متسق وقابل للصيانة ويمكن الوصول إليه

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بنظام التصميم | Design System Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إنشاء تكوين ثيم مركزي
- **🔴 حرج**: تعريف design tokens (ألوان، تباعد، طباعة)
- **🟠 عالي**: تطبيق مكونات أساسية قابلة لإعادة الاستخدام

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: إضافة دعم RTL شامل
- **🟠 عالي**: تطبيق ميزات إمكانية الوصول
- **🟡 متوسط**: إنشاء مكتبة مكونات متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تحسين الأداء والرسوم المتحركة
- **🟡 متوسط**: ثيمات متقدمة وتخصيص
- **🟢 منخفض**: تحسين التصميم مدعوم بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **Design System Specific Metrics:**
- **Component Usage**: 80%+ screens use shared components
- **Consistency**: 100% consistent spacing and typography
- **RTL Support**: 100% RTL layout working correctly
- **Accessibility**: WCAG 2.1 AA compliance
- **Maintainability**: Single theme update affects entire app
- **Development Speed**: 50%+ faster UI development

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **Design System Specific Pitfalls:**
- **Avoid**: Inconsistent component usage across screens
- **Avoid**: Hardcoded colors, spacing, and typography
- **Avoid**: RTL layout issues and text direction problems
- **Avoid**: Missing accessibility features
- **Avoid**: Poor component documentation

### **Best Practices:**
- **Use**: Centralized theme configuration
- **Use**: Design tokens for all visual properties
- **Use**: Reusable component library
- **Use**: Comprehensive RTL support
- **Use**: Built-in accessibility features

## 🎨 **رموز التصميم | Design Tokens**

### **1. Color Tokens | رموز الألوان**
```dart
class AppColors {
  // Primary Colors
  static const Color primary = Color(0xFF6B46C1);
  static const Color primaryLight = Color(0xFF9F7AEA);
  static const Color primaryDark = Color(0xFF553C9A);
  
  // Secondary Colors
  static const Color secondary = Color(0xFFF59E0B);
  static const Color secondaryLight = Color(0xFFFCD34D);
  static const Color secondaryDark = Color(0xFFD97706);
  
  // Neutral Colors
  static const Color white = Color(0xFFFFFFFF);
  static const Color black = Color(0xFF000000);
  static const Color gray50 = Color(0xFFF9FAFB);
  static const Color gray100 = Color(0xFFF3F4F6);
  static const Color gray200 = Color(0xFFE5E7EB);
  static const Color gray300 = Color(0xFFD1D5DB);
  static const Color gray400 = Color(0xFF9CA3AF);
  static const Color gray500 = Color(0xFF6B7280);
  static const Color gray600 = Color(0xFF4B5563);
  static const Color gray700 = Color(0xFF374151);
  static const Color gray800 = Color(0xFF1F2937);
  static const Color gray900 = Color(0xFF111827);
  
  // Semantic Colors
  static const Color success = Color(0xFF10B981);
  static const Color warning = Color(0xFFF59E0B);
  static const Color error = Color(0xFFEF4444);
  static const Color info = Color(0xFF3B82F6);
  
  // Background Colors
  static const Color background = Color(0xFFF9FAFB);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceVariant = Color(0xFFF3F4F6);
}
```

### **2. Spacing Tokens | رموز المسافات**
```dart
class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;
  static const double xxxl = 64.0;
  
  // Component specific spacing
  static const double buttonPadding = 12.0;
  static const double cardPadding = 16.0;
  static const double screenPadding = 16.0;
  static const double sectionSpacing = 24.0;
}
```

### **3. Typography Tokens | رموز الطباعة**
```dart
class AppTypography {
  static const String fontFamily = 'Cairo';
  static const String fontFamilyArabic = 'Cairo';
  static const String fontFamilyEnglish = 'Inter';
  
  // Font Sizes
  static const double fontSizeXs = 12.0;
  static const double fontSizeSm = 14.0;
  static const double fontSizeMd = 16.0;
  static const double fontSizeLg = 18.0;
  static const double fontSizeXl = 20.0;
  static const double fontSizeXxl = 24.0;
  static const double fontSizeXxxl = 32.0;
  
  // Font Weights
  static const FontWeight fontWeightLight = FontWeight.w300;
  static const FontWeight fontWeightRegular = FontWeight.w400;
  static const FontWeight fontWeightMedium = FontWeight.w500;
  static const FontWeight fontWeightSemiBold = FontWeight.w600;
  static const FontWeight fontWeightBold = FontWeight.w700;
  
  // Line Heights
  static const double lineHeightTight = 1.2;
  static const double lineHeightNormal = 1.4;
  static const double lineHeightRelaxed = 1.6;
}
```

### **4. Border Radius Tokens | رموز نصف قطر الحدود**
```dart
class AppRadius {
  static const double none = 0.0;
  static const double sm = 4.0;
  static const double md = 8.0;
  static const double lg = 12.0;
  static const double xl = 16.0;
  static const double xxl = 24.0;
  static const double full = 9999.0;
  
  // Component specific radius
  static const double buttonRadius = md;
  static const double cardRadius = lg;
  static const double inputRadius = md;
  static const double avatarRadius = full;
}
```

## 🎭 **تكوين الثيم | Theme Configuration**

### **1. App Theme | ثيم التطبيق**
```dart
class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      fontFamily: AppTypography.fontFamily,
      
      // Color Scheme
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.light,
      ),
      
      // App Bar Theme
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          fontSize: AppTypography.fontSizeLg,
          fontWeight: AppTypography.fontWeightSemiBold,
          color: AppColors.white,
        ),
      ),
      
      // Text Theme
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: AppTypography.fontSizeXxxl,
          fontWeight: AppTypography.fontWeightBold,
          height: AppTypography.lineHeightTight,
        ),
        displayMedium: TextStyle(
          fontSize: AppTypography.fontSizeXxl,
          fontWeight: AppTypography.fontWeightBold,
          height: AppTypography.lineHeightTight,
        ),
        headlineLarge: TextStyle(
          fontSize: AppTypography.fontSizeXl,
          fontWeight: AppTypography.fontWeightSemiBold,
          height: AppTypography.lineHeightNormal,
        ),
        headlineMedium: TextStyle(
          fontSize: AppTypography.fontSizeLg,
          fontWeight: AppTypography.fontWeightSemiBold,
          height: AppTypography.lineHeightNormal,
        ),
        titleLarge: TextStyle(
          fontSize: AppTypography.fontSizeMd,
          fontWeight: AppTypography.fontWeightMedium,
          height: AppTypography.lineHeightNormal,
        ),
        bodyLarge: TextStyle(
          fontSize: AppTypography.fontSizeMd,
          fontWeight: AppTypography.fontWeightRegular,
          height: AppTypography.lineHeightNormal,
        ),
        bodyMedium: TextStyle(
          fontSize: AppTypography.fontSizeSm,
          fontWeight: AppTypography.fontWeightRegular,
          height: AppTypography.lineHeightNormal,
        ),
        labelLarge: TextStyle(
          fontSize: AppTypography.fontSizeSm,
          fontWeight: AppTypography.fontWeightMedium,
          height: AppTypography.lineHeightNormal,
        ),
      ),
      
      // Elevated Button Theme
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.buttonPadding,
            vertical: AppSpacing.sm,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.buttonRadius),
          ),
          textStyle: const TextStyle(
            fontSize: AppTypography.fontSizeMd,
            fontWeight: AppTypography.fontWeightMedium,
          ),
        ),
      ),
      
      // Card Theme
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.cardRadius),
        ),
        margin: const EdgeInsets.all(AppSpacing.sm),
      ),
      
      // Input Decoration Theme
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.inputRadius),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: AppSpacing.sm,
        ),
      ),
    );
  }
  
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      fontFamily: AppTypography.fontFamily,
      brightness: Brightness.dark,
      
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.dark,
      ),
      
      // Similar theme configuration for dark mode
      // ... (similar structure with dark colors)
    );
  }
}
```

## 🧩 **المكونات القابلة لإعادة الاستخدام | Reusable Components**

### **1. App Button | زر التطبيق**
```dart
enum AppButtonType { primary, secondary, outline, text }

class AppButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final AppButtonType type;
  final bool isLoading;
  final IconData? icon;
  final double? width;
  
  const AppButton({
    super.key,
    required this.text,
    this.onPressed,
    this.type = AppButtonType.primary,
    this.isLoading = false,
    this.icon,
    this.width,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return SizedBox(
      width: width,
      child: _buildButton(theme),
    );
  }
  
  Widget _buildButton(ThemeData theme) {
    switch (type) {
      case AppButtonType.primary:
        return ElevatedButton(
          onPressed: isLoading ? null : onPressed,
          child: _buildButtonContent(),
        );
      case AppButtonType.secondary:
        return ElevatedButton(
          onPressed: isLoading ? null : onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.secondary,
          ),
          child: _buildButtonContent(),
        );
      case AppButtonType.outline:
        return OutlinedButton(
          onPressed: isLoading ? null : onPressed,
          child: _buildButtonContent(),
        );
      case AppButtonType.text:
        return TextButton(
          onPressed: isLoading ? null : onPressed,
          child: _buildButtonContent(),
        );
    }
  }
  
  Widget _buildButtonContent() {
    if (isLoading) {
      return const SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(strokeWidth: 2),
      );
    }
    
    if (icon != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 18),
          const SizedBox(width: AppSpacing.sm),
          Text(text),
        ],
      );
    }
    
    return Text(text);
  }
}
```

### **2. App Card | بطاقة التطبيق**
```dart
class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final EdgeInsets? margin;
  final Color? backgroundColor;
  final double? elevation;
  final VoidCallback? onTap;
  
  const AppCard({
    super.key,
    required this.child,
    this.padding,
    this.margin,
    this.backgroundColor,
    this.elevation,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Container(
      margin: margin ?? const EdgeInsets.all(AppSpacing.sm),
      child: Material(
        elevation: elevation ?? 2,
        borderRadius: BorderRadius.circular(AppRadius.cardRadius),
        color: backgroundColor ?? theme.cardColor,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(AppRadius.cardRadius),
          child: Padding(
            padding: padding ?? const EdgeInsets.all(AppSpacing.cardPadding),
            child: child,
          ),
        ),
      ),
    );
  }
}
```

### **3. App Input | حقل الإدخال**
```dart
class AppInput extends StatelessWidget {
  final String? label;
  final String? hint;
  final String? errorText;
  final TextEditingController? controller;
  final TextInputType? keyboardType;
  final bool obscureText;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final String? Function(String?)? validator;
  final void Function(String)? onChanged;
  final bool enabled;
  
  const AppInput({
    super.key,
    this.label,
    this.hint,
    this.errorText,
    this.controller,
    this.keyboardType,
    this.obscureText = false,
    this.prefixIcon,
    this.suffixIcon,
    this.validator,
    this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      keyboardType: keyboardType,
      obscureText: obscureText,
      validator: validator,
      onChanged: onChanged,
      enabled: enabled,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        errorText: errorText,
        prefixIcon: prefixIcon,
        suffixIcon: suffixIcon,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.inputRadius),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.inputRadius),
          borderSide: BorderSide(color: AppColors.gray300),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.inputRadius),
          borderSide: BorderSide(color: AppColors.primary),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadius.inputRadius),
          borderSide: BorderSide(color: AppColors.error),
        ),
      ),
    );
  }
}
```

## 🌍 **دعم الكتابة من اليمين لليسار | RTL Support**

### **1. RTL Configuration | تكوين RTL**
```dart
class RTLConfig {
  static bool isRTL(Locale locale) {
    return locale.languageCode == 'ar';
  }
  
  static TextDirection getTextDirection(Locale locale) {
    return isRTL(locale) ? TextDirection.rtl : TextDirection.ltr;
  }
  
  static EdgeInsets getPadding(EdgeInsets padding, Locale locale) {
    if (isRTL(locale)) {
      return EdgeInsets.only(
        left: padding.right,
        right: padding.left,
        top: padding.top,
        bottom: padding.bottom,
      );
    }
    return padding;
  }
  
  static Alignment getAlignment(Alignment alignment, Locale locale) {
    if (isRTL(locale)) {
      return Alignment(-alignment.x, alignment.y);
    }
    return alignment;
  }
}
```

### **2. RTL Widget | عنصر RTL**
```dart
class RTLWidget extends StatelessWidget {
  final Widget child;
  final Locale locale;
  
  const RTLWidget({
    super.key,
    required this.child,
    required this.locale,
  });

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: RTLConfig.getTextDirection(locale),
      child: child,
    );
  }
}
```

### **3. RTL-Aware Components | مكونات واعية بـ RTL**
```dart
class RTLRow extends StatelessWidget {
  final List<Widget> children;
  final MainAxisAlignment mainAxisAlignment;
  final CrossAxisAlignment crossAxisAlignment;
  final Locale locale;
  
  const RTLRow({
    super.key,
    required this.children,
    required this.locale,
    this.mainAxisAlignment = MainAxisAlignment.start,
    this.crossAxisAlignment = CrossAxisAlignment.center,
  });

  @override
  Widget build(BuildContext context) {
    if (RTLConfig.isRTL(locale)) {
      return Row(
        mainAxisAlignment: mainAxisAlignment,
        crossAxisAlignment: crossAxisAlignment,
        children: children.reversed.toList(),
      );
    }
    
    return Row(
      mainAxisAlignment: mainAxisAlignment,
      crossAxisAlignment: crossAxisAlignment,
      children: children,
    );
  }
}
```

## ♿ **ميزات إمكانية الوصول | Accessibility Features**

### **1. Accessibility Configuration | تكوين إمكانية الوصول**
```dart
class AccessibilityConfig {
  static const double minTouchTargetSize = 44.0;
  static const double minContrastRatio = 4.5;
  
  static Color getAccessibleColor(Color color, Color background) {
    final contrast = _getContrastRatio(color, background);
    if (contrast >= minContrastRatio) {
      return color;
    }
    
    // Adjust color to meet contrast requirements
    return _adjustColorForContrast(color, background);
  }
  
  static double _getContrastRatio(Color color1, Color color2) {
    final luminance1 = color1.computeLuminance();
    final luminance2 = color2.computeLuminance();
    
    final lighter = math.max(luminance1, luminance2);
    final darker = math.min(luminance1, luminance2);
    
    return (lighter + 0.05) / (darker + 0.05);
  }
  
  static Color _adjustColorForContrast(Color color, Color background) {
    // Implementation to adjust color for better contrast
    // This is a simplified version
    return color.withOpacity(0.8);
  }
}
```

### **2. Accessible Components | مكونات قابلة للوصول**
```dart
class AccessibleButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final String? semanticsLabel;
  final String? semanticsHint;
  
  const AccessibleButton({
    super.key,
    required this.text,
    this.onPressed,
    this.semanticsLabel,
    this.semanticsHint,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticsLabel ?? text,
      hint: semanticsHint,
      button: true,
      child: ElevatedButton(
        onPressed: onPressed,
        child: Text(text),
      ),
    );
  }
}
```

## 🧪 **اختبار نظام التصميم | Testing Design System**

### **1. Theme Tests | اختبارات الثيم**
```dart
void main() {
  group('AppTheme', () {
    test('should have consistent colors', () {
      final theme = AppTheme.lightTheme;
      
      expect(theme.colorScheme.primary, AppColors.primary);
      expect(theme.colorScheme.secondary, AppColors.secondary);
      expect(theme.colorScheme.error, AppColors.error);
    });
    
    test('should have consistent typography', () {
      final theme = AppTheme.lightTheme;
      
      expect(theme.textTheme.bodyLarge?.fontSize, AppTypography.fontSizeMd);
      expect(theme.textTheme.headlineLarge?.fontSize, AppTypography.fontSizeXl);
    });
  });
}
```

### **2. Component Tests | اختبارات المكونات**
```dart
void main() {
  group('AppButton', () {
    testWidgets('should render correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: AppButton(
              text: 'Test Button',
              onPressed: () {},
            ),
          ),
        ),
      );
      
      expect(find.text('Test Button'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });
    
    testWidgets('should show loading state', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: AppButton(
              text: 'Test Button',
              isLoading: true,
            ),
          ),
        ),
      );
      
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });
}
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Design Tokens**
- [ ] Create color tokens
- [ ] Define spacing tokens
- [ ] Set up typography tokens
- [ ] Add border radius tokens

### **2. Theme Configuration**
- [ ] Create light theme
- [ ] Create dark theme
- [ ] Configure component themes
- [ ] Test theme consistency

### **3. Reusable Components**
- [ ] Create button components
- [ ] Create card components
- [ ] Create input components
- [ ] Create other UI components

### **4. RTL Support**
- [ ] Implement RTL configuration
- [ ] Create RTL-aware components
- [ ] Test RTL layouts
- [ ] Verify text direction

### **5. Accessibility**
- [ ] Add accessibility features
- [ ] Test contrast ratios
- [ ] Add semantic labels
- [ ] Verify screen reader support

### **6. Testing**
- [ ] Write theme tests
- [ ] Test component rendering
- [ ] Test RTL functionality
- [ ] Test accessibility features

---

**Architecture Document Complete!** ✅

**Next Document**: 02-Implementation | التطبيق

