# مواصفة OpenAPI — OpenAPI Specification
**المعيار | Standard**: OpenAPI 3.0/3.1

---

## **ما هو OpenAPI؟ | What is OpenAPI?**

**OpenAPI Specification (OAS)** - معيار لتوثيق RESTful APIs بصيغة machine-readable.

### **الفوائد:**

- توثيق تلقائي (Swagger UI)
- Contract testing
- Code generation
- Validation تلقائي
- Mock servers

---

## **OpenAPI Basic Structure**

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: API for internal use
  
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /products:
    get:
      summary: List products
      tags: [Products]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
        '401':
          $ref: '#/components/responses/Unauthorized'
    
    post:
      summary: Create product
      tags: [Products]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProductInput'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    Product:
      type: object
      required: [id, name, price]
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Product Name"
        price:
          type: number
          format: float
          example: 99.99
        created_at:
          type: string
          format: date-time
    
    ProductInput:
      type: object
      required: [name, price]
      properties:
        name:
          type: string
          maxLength: 255
        price:
          type: number
          minimum: 0
        category_id:
          type: integer
    
    Error:
      type: object
      properties:
        success:
          type: boolean
          example: false
        message:
          type: string
        error_code:
          type: string
  
  responses:
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

security:
  - bearerAuth: []
```

---

## **Laravel + OpenAPI**

### **باستخدام L5-Swagger:**

```bash
composer require darkaonline/l5-swagger
php artisan vendor:publish --provider="L5Swagger\L5SwaggerServiceProvider"
```

```php
// Controller with annotations
/**
 * @OA\Get(
 *     path="/api/v1/products",
 *     summary="Get list of products",
 *     tags={"Products"},
 *     @OA\Parameter(
 *         name="page",
 *         in="query",
 *         description="Page number",
 *         @OA\Schema(type="integer", default=1)
 *     ),
 *     @OA\Response(
 *         response=200,
 *         description="Success",
 *         @OA\JsonContent(
 *             @OA\Property(property="success", type="boolean", example=true),
 *             @OA\Property(property="data", type="array",
 *                 @OA\Items(ref="#/components/schemas/Product")
 *             )
 *         )
 *     ),
 *     security={{"bearerAuth":{}}}
 * )
 */
public function index()
{
    // Implementation
}
```

```bash
# Generate documentation
php artisan l5-swagger:generate
```

**الوصول:**  
`http://api.example.com/api/documentation`

---

## **Swagger UI**

### **تفعيل Swagger UI:**

```php
// config/l5-swagger.php
'generate_always' => env('L5_SWAGGER_GENERATE_ALWAYS', false),
'generate_yaml_copy' => true,
'proxy' => false,

'paths' => [
    'docs' => storage_path('api-docs'),
    'docs_json' => 'api-docs.json',
    'docs_yaml' => 'api-docs.yaml',
],

'securityDefinitions' => [
    'bearerAuth' => [
        'type' => 'http',
        'scheme' => 'bearer',
        'bearerFormat' => 'JWT',
    ],
],
```

---

## **Contract Testing**

### **باستخدام Dredd:**

```bash
npm install -g dredd

# Test API مقابل OpenAPI spec
dredd openapi.yaml https://api.example.com
```

```yaml
# dredd.yml
language: nodejs
sandbox: false
server: php artisan serve
server-wait: 3
init: false
names: false
only: []
reporter: []
output: []
header: []
sorted: false
user: null
inline-errors: false
details: false
method: []
color: true
level: info
timestamp: false
silent: false
path: []
hooks-worker-timeout: 5000
hooks-worker-connect-timeout: 1500
hooks-worker-connect-retry: 500
hooks-worker-after-connect-wait: 100
hooks-worker-term-timeout: 5000
hooks-worker-term-retry: 500
hooks-worker-handler-host: 127.0.0.1
hooks-worker-handler-port: 61321
config: ./dredd.yml
hookfiles: null
```

---

## **OpenAPI Best Practices**

### ** DO:**

- استخدم `$ref` لتجنب التكرار
- أمثلة واقعية في كل endpoint
- وصف واضح لكل parameter
- جميع status codes محتملة
- Security schemes واضحة
- Tags لتنظيم endpoints

### ** DON'T:**

- تكرار schemas
- أمثلة غير واقعية
- endpoints بدون وصف
- missing error responses

---

## **أدوات التوليد | Generation Tools**

### **1. من Code → OpenAPI:**

```bash
# L5-Swagger (Laravel)
php artisan l5-swagger:generate

# Scramble (Laravel - أحدث)
composer require dedoc/scramble
php artisan scramble:generate
```

---

### **2. من OpenAPI → Code:**

```bash
# OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generate client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g dart \
  -o ./flutter-client
```

---

## **Validation مقابل OpenAPI**

### **في Laravel:**

```php
use Illuminate\Support\Facades\Validator;
use OpenAPIValidation\PSR7\ValidatorBuilder;

class ValidateAgainstOpenAPI
{
    public function validate(Request $request, Response $response)
    {
        $validator = (new ValidatorBuilder)
            ->fromYamlFile('openapi.yaml')
            ->getServerRequestValidator();
        
        try {
            $validator->validate($request->toPsrRequest());
            $validator->validate($response->toPsrResponse());
        } catch (\Exception $e) {
            Log::warning('OpenAPI validation failed', [
                'error' => $e->getMessage(),
            ]);
        }
    }
}
```

---

## **Checklist**

### **Documentation:**
- [ ] openapi.yaml موجود
- [ ] جميع endpoints موثقة
- [ ] Schemas معرفة
- [ ] Examples واقعية
- [ ] Security schemes واضحة

### **Tools:**
- [ ] Swagger UI مفعل
- [ ] Generation script
- [ ] Validation (CI)
- [ ] Contract tests

### **Maintenance:**
- [ ] تحديث مع كل endpoint جديد
- [ ] Breaking changes موثقة
- [ ] Versioning واضح

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
