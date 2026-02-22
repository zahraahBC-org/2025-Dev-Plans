# الإطلاق وCI/CD — Deployment & CI/CD

---

## **GitHub Actions Example**

```yaml
# GitHub Actions - API CI/CD
name: API CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
      - run: composer install
      - run: php artisan test --coverage --min=70
      - run: vendor/bin/phpstan analyse
  
  deploy:
    needs: test
    steps:
      - run: php artisan migrate --force
      - run: php artisan config:cache
```

---

## **Deployment Checklist**

### **Pre-deployment:**
- [ ] Tests pass
- [ ] APP_DEBUG=false
- [ ] Migrations tested
- [ ] Env variables set

### **Post-deployment:**
- [ ] Health check /health
- [ ] Monitor errors
- [ ] Check logs

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
