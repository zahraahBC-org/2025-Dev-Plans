# جودة الكود — Code Quality
**الأهمية | Importance**: 🟢 أساسية

---

## **لماذا Code Quality مهم؟**

**Benefits:**
- Maintainability (سهولة الصيانة)
- Scalability (قابلية التوسع)
- Fewer bugs (أخطاء أقل)
- Team collaboration (تعاون أفضل)
- Faster onboarding (تدريب أسرع)

---

## **الأدوات | Tools**

### **1. PHPStan/Larastan - Static Analysis**

```bash
composer require --dev larastan/larastan

# phpstan.neon
includes:
    - vendor/larastan/larastan/extension.neon
parameters:
    level: 6                # 0-9 (6 موصى به، 9 صارم جداً)
    paths:
        - app
        - routes
    excludePaths:
        - app/Console/Kernel.php
    checkMissingIterableValueType: false

# Run
vendor/bin/phpstan analyse

# Output مثال
 ------ -------------------------------------------------------------------
  Line   app/Http/Controllers/API/V1/ProductController.php
 ------ -------------------------------------------------------------------
  45     Method index() return type has no value type specified in iterable type array
  78     Parameter $id of method show() expects int, string given
 ------ -------------------------------------------------------------------
```

**الفوائد:**
- يكتشف type errors قبل Runtime
- يجد dead code
- يكتشف missing return types
- يحلل method signatures

---

### **2. Laravel Pint - Code Formatting**

```bash
composer require --dev laravel/pint

# pint.json (optional)
{
    "preset": "laravel",
    "rules": {
        "array_syntax": {
            "syntax": "short"
        },
        "binary_operator_spaces": {
            "default": "single_space"
        },
        "blank_line_after_namespace": true,
        "blank_line_after_opening_tag": true,
        "concat_space": {
            "spacing": "one"
        },
        "method_chaining_indentation": true,
        "not_operator_with_successor_space": false,
        "ordered_imports": {
            "sort_algorithm": "alpha"
        },
        "phpdoc_align": false,
        "phpdoc_no_empty_return": false,
        "phpdoc_separation": true,
        "phpdoc_to_comment": false
    }
}

# Run - Fix all files
vendor/bin/pint

# Dry-run - Check only
vendor/bin/pint --test

# Specific paths
vendor/bin/pint app/Http/Controllers

# Output مثال
WARN  app/Http/Controllers/ProductController.php
  ⨯ [array_syntax] Arrays should use short syntax
  ⨯ [braces] Opening brace should be on same line

FIXED 1 file in 0.12s
```

---

### **3. PHP CS Fixer - Advanced Formatting**

```bash
composer require --dev friendsofphp/php-cs-fixer

# .php-cs-fixer.php
<?php
$finder = PhpCsFixer\Finder::create()
    ->in([
        __DIR__ . '/app',
        __DIR__ . '/routes',
    ])
    ->name('*.php')
    ->notName('*.blade.php')
    ->ignoreDotFiles(true)
    ->ignoreVCS(true);

return (new PhpCsFixer\Config())
    ->setRules([
        '@PSR12' => true,
        'array_syntax' => ['syntax' => 'short'],
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        'not_operator_with_successor_space' => false,
        'trailing_comma_in_multiline' => true,
        'phpdoc_scalar' => true,
        'unary_operator_spaces' => true,
        'binary_operator_spaces' => true,
        'blank_line_before_statement' => [
            'statements' => ['break', 'continue', 'declare', 'return', 'throw', 'try'],
        ],
        'phpdoc_single_line_var_spacing' => true,
        'phpdoc_var_without_name' => true,
    ])
    ->setFinder($finder);

# Run
vendor/bin/php-cs-fixer fix

# Dry-run
vendor/bin/php-cs-fixer fix --dry-run --diff
```

---

### **4. PHPMD - Mess Detector**

```bash
composer require --dev phpmd/phpmd

# phpmd.xml
<?xml version="1.0"?>
<ruleset name="API Rules">
    <description>PHPMD rules for API</description>
    
    <rule ref="rulesets/cleancode.xml">
        <exclude name="StaticAccess"/>
    </rule>
    
    <rule ref="rulesets/codesize.xml"/>
    
    <rule ref="rulesets/controversial.xml"/>
    
    <rule ref="rulesets/design.xml"/>
    
    <rule ref="rulesets/naming.xml">
        <exclude name="ShortVariable"/>
    </rule>
    
    <rule ref="rulesets/unusedcode.xml"/>
</ruleset>

# Run
vendor/bin/phpmd app text phpmd.xml

# Output مثال
app/Http/Controllers/ProductController.php:45 Method 'index' has cyclomatic complexity of 12
app/Models/Product.php:78 Avoid unused parameters '$request'
```

**يكتشف:**
```
✅ Complex methods (cyclomatic complexity)
✅ Unused variables
✅ Too many parameters
✅ Long methods
✅ God classes
```

---

### **5. PHPInsights - Overall Code Quality**

```bash
composer require --dev nunomaduro/phpinsights

# Run
php artisan insights

# Output مثال
┌─────────────────────────────────────────────────────────┐
│ Code Quality: 92.5%                                     │
│ Complexity: 85.0%                                       │
│ Architecture: 98.0%                                     │
│ Style: 95.0%                                            │
└─────────────────────────────────────────────────────────┘

ISSUES
  • app/Http/Controllers/ProductController.php:45
    ⨯ Method has cyclomatic complexity of 15
  • app/Models/Product.php:12
    ⨯ Missing return type hint
```

---

## **Code Standards Checklist**

### **PSR-12 Compliance:**

```php
// ✅ DO - صحيح
<?php

declare(strict_types=1);

namespace App\Http\Controllers\API\V1;

use App\Models\Product;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $products = Product::paginate(20);
        
        return response()->json([
            'data' => ProductResource::collection($products),
        ]);
    }
}

// ❌ DON'T - خطأ
<?php
namespace App\Http\Controllers\API\V1;
use App\Models\Product;use Illuminate\Http\Request;  // No line breaks!
class ProductController extends Controller {  // Brace on same line!
    function index($request) {  // No types!
        return Product::paginate(20);  // No formatting!
    }
}
```

---

### **Type Hints:**

```php
// ✅ DO
public function createOrder(
    array $data,
    User $user,
    int $quantity
): Order {
    // ...
}

// ❌ DON'T
public function createOrder($data, $user, $quantity) {
    // ...
}
```

---

### **DocBlocks:**

```php
// ✅ DO
/**
 * Create a new product
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\JsonResponse
 * @throws \Illuminate\Validation\ValidationException
 */
public function store(Request $request): JsonResponse
{
    // ...
}

// ❌ DON'T
// Create product
public function store($request) {
    // ...
}
```

---

### **DRY Principle (Don't Repeat Yourself):**

```php
// ❌ DON'T - تكرار
public function getActiveProducts()
{
    return Product::where('is_active', true)
        ->where('stock', '>', 0)
        ->get();
}

public function getFeaturedProducts()
{
    return Product::where('is_active', true)
        ->where('stock', '>', 0)
        ->where('is_featured', true)
        ->get();
}

// ✅ DO - استخدم Query Scopes
// في Model
public function scopeActive($query)
{
    return $query->where('is_active', true)
        ->where('stock', '>', 0);
}

// في Controller
Product::active()->get();
Product::active()->where('is_featured', true)->get();
```

---

### **SOLID Principles:**

#### **Single Responsibility:**

```php
// Single Responsibility Principle

// ❌ Controller doing too much
public function store(Request $request)
{
    $product = Product::create($request->all());
    Mail::send(...);
    Analytics::track(...);
    Cache::forget(...);
    // Too many responsibilities!
}

// ✅ Delegate to service
public function store(StoreProductRequest $request)
{
    $product = $this->productService->create($request->validated());
    return new ProductResource($product);
}
```

---

## **CI/CD Integration**

### **GitHub Actions:**

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.2
          
      - name: Install Dependencies
        run: composer install --prefer-dist --no-progress
      
      - name: Run Pint
        run: vendor/bin/pint --test
      
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse
      
      - name: Run Tests
        run: php artisan test
```

---

## **Checklist**

### **Setup:**
- [ ] PHPStan/Larastan installed
- [ ] Laravel Pint installed
- [ ] phpstan.neon configured
- [ ] pint.json configured

### **Standards:**
- [ ] PSR-12 compliant
- [ ] Type hints على جميع methods
- [ ] DocBlocks على public methods
- [ ] DRY - لا تكرار
- [ ] SOLID principles

### **CI/CD:**
- [ ] Code quality checks في CI
- [ ] Static analysis في CI
- [ ] Linting في CI
- [ ] Tests في CI

### **Regular Maintenance:**
- [ ] Run Pint أسبوعياً
- [ ] Run PHPStan أسبوعياً
- [ ] Review code quality metrics شهرياً
- [ ] Refactor complex code

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
