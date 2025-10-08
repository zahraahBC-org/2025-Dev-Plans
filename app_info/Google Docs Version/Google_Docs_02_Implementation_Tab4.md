# TAB 4: سير عمل Git | Git Workflow

## 10. سير عمل Git والفروع | Git Workflow & Branching
### إنشاء سير عمل Git وفروع فعال لتعاون الفريق وجودة الكود

---

## 🎯 **الهدف | Objective**
إنشاء سير عمل Git واستراتيجية فروع فعالة لتعاون الفريق وجودة الكود وإصدارات موثوقة.

## 📋 **القاعدة | Rule**
**العربية**: Trunk-based بسيط مع main محمي، كل تطوير عبر feature branches  
**English**: Simple trunk-based with protected main, all development via feature branches

## 💡 **الفوائد | Benefits**
- **تعاون الفريق | Team Collaboration**: سير عمل واضح لجميع أعضاء الفريق
- **جودة الكود | Code Quality**: فرع main محمي مع عملية مراجعة
- **إدارة الإصدارات | Release Management**: إصدارات موثوقة وقابلة للتتبع
- **حل التعارضات | Conflict Resolution**: تعارضات دمج قليلة
- **عزل الميزات | Feature Isolation**: تطوير ميزات آمن
- **إمكانية التراجع | Rollback Capability**: سهولة إلغاء التغييرات

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع أنشطة التطوير وعمل الميزات والإصدارات
- **كيفية التطبيق**:
  - إعداد فرع main محمي
  - إنشاء سير عمل فرع الميزات
  - تطبيق عملية مراجعة PR
  - تكوين قواعد حماية الفروع
  - إعداد فحوصات مؤتمتة
- **النتيجة**: سير عمل تطوير فعال وموثوق مع جودة كود عالية

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بسير عمل Git | Git Workflow Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إعداد فرع main محمي
- **🔴 حرج**: إنشاء سير عمل فرع الميزات
- **🟠 عالي**: تطبيق عملية مراجعة PR

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: تكوين قواعد حماية الفروع
- **🟠 عالي**: إعداد فحوصات مؤتمتة و CI/CD
- **🟡 متوسط**: إضافة ميزات سير عمل متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: إدارة إصدارات متقدمة
- **🟡 متوسط**: حل تعارضات مؤتمت
- **🟢 منخفض**: تحسين سير عمل مدعوم بالذكاء الاصطناعي

## 📈 **مؤشرات النجاح | Success Metrics**

### **Git Workflow Specific Metrics:**
- **Branch Protection**: 100% main branch protection
- **PR Coverage**: 100% code reviewed before merge
- **Merge Conflicts**: <5% merge conflicts
- **Release Reliability**: 100% successful releases
- **Team Adoption**: 100% team following workflow
- **Automation**: 100% automated checks passing

## ⚠️ **الأخطاء الشائعة وأفضل الممارسات | Common Pitfalls & Best Practices**

### **Git Workflow Specific Pitfalls:**
- **Avoid**: Direct commits to main branch
- **Avoid**: Long-lived feature branches
- **Avoid**: Missing branch protection rules
- **Avoid**: Inadequate PR review process
- **Avoid**: Poor commit message conventions

### **Best Practices:**
- **Use**: Protected main branch with required reviews
- **Use**: Short-lived feature branches
- **Use**: Clear commit message conventions
- **Use**: Automated checks and CI/CD
- **Use**: Regular branch cleanup

## 🌳 **استراتيجية الفروع | Branching Strategy**

### **1. Branch Structure | هيكل الفروع**
```
main (protected)
├── develop (optional)
├── feature/user-authentication
├── feature/product-catalog
├── feature/shopping-cart
├── hotfix/critical-bug-fix
└── release/v1.0.0
```

### **2. Branch Types | أنواع الفروع**
- **main**: Production-ready code, protected
- **develop**: Integration branch for features
- **feature/**: New feature development
- **hotfix/**: Critical bug fixes
- **release/**: Release preparation

## 🔒 **حماية الفروع | Branch Protection**

### **1. Main Branch Protection | حماية الفرع الرئيسي**
```yaml
# GitHub Branch Protection Rules
main:
  required_status_checks:
    strict: true
    contexts:
      - "ci/quality"
      - "ci/tests"
      - "ci/build"
  
  enforce_admins: true
  
  required_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  
  restrictions:
    users: []
    teams: ["senior-developers"]
```

### **2. Branch Naming Conventions | اتفاقيات تسمية الفروع**
```bash
# Feature branches
feature/user-authentication
feature/product-catalog
feature/shopping-cart

# Bug fixes
bugfix/login-error
bugfix/cart-calculation

# Hotfixes
hotfix/security-vulnerability
hotfix/critical-crash

# Releases
release/v1.0.0
release/v1.1.0
```

## 📝 **اتفاقيات رسائل الالتزام | Commit Message Conventions**

### **1. Commit Message Format | تنسيق رسالة الالتزام**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### **2. Commit Types | أنواع الالتزامات**
```bash
# Types
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code style changes (formatting, etc.)
refactor: Code refactoring
test:     Adding or updating tests
chore:    Maintenance tasks
perf:     Performance improvements
ci:       CI/CD changes
build:    Build system changes
```

### **3. Commit Examples | أمثلة الالتزامات**
```bash
# Feature
feat(auth): add user login functionality

# Bug fix
fix(cart): resolve price calculation error

# Documentation
docs(readme): update installation instructions

# Refactoring
refactor(products): extract product service

# Testing
test(auth): add unit tests for login use case
```

## 🔄 **عملية سير العمل | Workflow Process**

### **1. Feature Development | تطوير الميزات**
```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# 2. Develop feature
git add .
git commit -m "feat(auth): add login form component"

# 3. Push branch
git push origin feature/user-authentication

# 4. Create Pull Request
# 5. Code review and approval
# 6. Merge to main
```

### **2. Hotfix Process | عملية الإصلاح السريع**
```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/security-vulnerability

# 2. Fix the issue
git add .
git commit -m "fix(security): patch authentication vulnerability"

# 3. Push and create PR
git push origin hotfix/security-vulnerability

# 4. Fast-track review and merge
```

### **3. Release Process | عملية الإصدار**
```bash
# 1. Create release branch
git checkout main
git pull origin main
git checkout -b release/v1.0.0

# 2. Update version numbers
git add .
git commit -m "chore(release): bump version to 1.0.0"

# 3. Create release PR
# 4. Final testing and approval
# 5. Merge to main and tag
git tag v1.0.0
git push origin v1.0.0
```

## 🔍 **عملية طلب السحب | Pull Request Process**

### **1. PR Template | قالب طلب السحب**
```markdown
## 📋 **قائمة مراجعة طلب السحب | Pull Request Checklist**

### **Code Quality | جودة الكود**
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is properly commented
- [ ] No hardcoded values or secrets

### **Testing | الاختبار**
- [ ] Unit tests added/updated
- [ ] Widget tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally

### **Documentation | التوثيق**
- [ ] Code is self-documenting
- [ ] Complex logic is commented
- [ ] API documentation updated

### **Performance | الأداء**
- [ ] No performance regressions
- [ ] Memory usage optimized
- [ ] Network calls optimized

---

## 🎯 **الوصف | Description**
Brief description of changes made.

## 🔗 **القضايا ذات الصلة | Related Issues**
Closes #(issue number)

## 📸 **لقطات الشاشة | Screenshots**
If applicable, add screenshots of UI changes.

## 🧪 **تعليمات الاختبار | Testing Instructions**
Steps to test the changes:
1. Step 1
2. Step 2
3. Step 3
```

### **2. Review Process | عملية المراجعة**
```markdown
## 📋 **عملية مراجعة الكود | Code Review Process**

### **Step 1: Self Review | الخطوة 1: المراجعة الذاتية**
- Review your own code before submitting
- Run all tests and quality checks
- Ensure code follows project standards

### **Step 2: Peer Review | الخطوة 2: مراجعة الأقران**
- Assign appropriate reviewers
- Provide clear description and context
- Respond to feedback promptly

### **Step 3: Quality Checks | الخطوة 3: فحوصات الجودة**
- All CI/CD checks must pass
- Code coverage maintained
- Performance benchmarks met

### **Step 4: Approval | الخطوة 4: الموافقة**
- At least 2 approvals required
- All comments addressed
- Final review by senior developer
```

## 🤖 **الأتمتة | Automation**

### **1. GitHub Actions | إجراءات GitHub**
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
      
      - name: Install dependencies
        run: flutter pub get
      
      - name: Run analysis
        run: dart analyze --fatal-infos
      
      - name: Check formatting
        run: dart format --set-exit-if-changed lib/ test/
      
      - name: Run tests
        run: dart test --coverage=coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage/lcov.info
```

### **2. Pre-commit Hooks | خطافات ما قبل الالتزام**
```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "🔍 Running pre-commit checks..."

# Check for TODO/FIXME comments
if git diff --cached --name-only | xargs grep -l "TODO\|FIXME"; then
  echo "❌ Found TODO/FIXME comments. Please resolve them."
  exit 1
fi

# Run dart format
dart format --set-exit-if-changed lib/ test/

# Run dart analyze
dart analyze --fatal-infos

echo "✅ Pre-commit checks passed!"
```

## 📊 **مقاييس سير العمل | Workflow Metrics**

### **1. Git Metrics | مقاييس Git**
```bash
#!/bin/bash
# scripts/git_metrics.sh
echo "📊 Git Workflow Metrics"

# Branch count
echo "🌳 Active branches: $(git branch -r | wc -l)"

# Commit frequency
echo "📝 Commits this week: $(git log --since="1 week ago" --oneline | wc -l)"

# PR metrics
echo "🔀 Open PRs: $(gh pr list --state=open | wc -l)"

# Code review coverage
echo "👥 Review coverage: $(gh pr list --state=merged --json=reviews | jq '.[] | select(.reviews | length > 0)' | wc -l)"
```

### **2. Quality Metrics | مقاييس الجودة**
```bash
#!/bin/bash
# scripts/quality_metrics.sh
echo "📈 Quality Metrics"

# Test coverage
echo "🧪 Test coverage: $(dart test --coverage=coverage && genhtml coverage/lcov.info -o coverage/html && grep -o 'lines.*: [0-9]*%' coverage/html/index.html)"

# Linting issues
echo "🔍 Linting issues: $(dart analyze --no-fatal-infos 2>&1 | grep -c "error\|warning")"

# Code complexity
echo "📊 Code complexity: $(find lib/ -name "*.dart" | xargs wc -l | tail -1)"
```

## 🚀 **إدارة الإصدارات | Release Management**

### **1. Version Strategy | استراتيجية الإصدار**
```yaml
# version.yaml
version: 1.0.0
build_number: 1

# Semantic Versioning
# MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes (backward compatible)
```

### **2. Release Process | عملية الإصدار**
```bash
#!/bin/bash
# scripts/release.sh
VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version>"
  exit 1
fi

# Create release branch
git checkout main
git pull origin main
git checkout -b release/v$VERSION

# Update version
sed -i "s/version: .*/version: $VERSION/" pubspec.yaml
git add pubspec.yaml
git commit -m "chore(release): bump version to $VERSION"

# Push branch
git push origin release/v$VERSION

# Create release PR
gh pr create --title "Release v$VERSION" --body "Release version $VERSION"

echo "✅ Release branch created: release/v$VERSION"
```

## 📋 **قائمة مراجعة التنفيذ | Implementation Checklist**

### **1. Branch Setup**
- [ ] Set up protected main branch
- [ ] Configure branch protection rules
- [ ] Create branch naming conventions
- [ ] Set up branch cleanup automation

### **2. Workflow Process**
- [ ] Create feature branch workflow
- [ ] Implement PR review process
- [ ] Set up commit message conventions
- [ ] Train team on workflow

### **3. Automation**
- [ ] Set up CI/CD checks
- [ ] Configure pre-commit hooks
- [ ] Implement automated testing
- [ ] Set up quality metrics

### **4. Release Management**
- [ ] Create release process
- [ ] Set up version management
- [ ] Configure release automation
- [ ] Test release workflow

### **5. Documentation**
- [ ] Document workflow process
- [ ] Create team guidelines
- [ ] Add troubleshooting guide
- [ ] Maintain workflow documentation

---

**Implementation Document Complete!** ✅

**Next Document**: 03-Quality | الجودة

