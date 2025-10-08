# 05. الملفات والروابط الموقعة | Files & Signed URLs

## 🎯 **نظرة عامة | Overview**

إدارة آمنة لرفع وتنزيل الملفات باستخدام روابط موقعة قصيرة العمر.

**الهدف | Purpose**: رفع/تنزيل ملفات آمن  
**الجمهور | Audience**: مطورو Backend  
**المتطلبات | Prerequisites**: فهم [الأمان](../03-Security/02_Security_Hardening.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [رفع الملفات](#رفع-الملفات)
2. [الروابط الموقعة](#الروابط-الموقعة)
3. [أنواع الملفات المسموحة](#أنواع-الملفات)
4. [الأمان](#الأمان)
5. [أمثلة عملية](#أمثلة-عملية)

---

## 1️⃣ رفع الملفات | File Upload {#رفع-الملفات}

### **تدفق الرفع**

```
1. العميل يطلب رابط رفع موقع
   POST /v1/uploads/presigned
   {
     "file_name": "product-image.jpg",
     "content_type": "image/jpeg",
     "size_bytes": 245678
   }

2. الخادم يُرجع رابط موقع
   {
     "upload_url": "https://storage.zahraah.com/...",
     "file_id": "file_abc123",
     "expires_at": "2025-01-08T12:15:00Z",
     "headers": {
       "Content-Type": "image/jpeg"
     }
   }

3. العميل يرفع مباشرة للتخزين
   PUT https://storage.zahraah.com/...
   [binary data]

4. العميل يؤكد الرفع
   POST /v1/uploads/file_abc123/confirm
   
5. الخادم يحفظ Metadata
```

---

### **Endpoint: طلب رابط رفع**

```http
POST /v1/uploads/presigned
Authorization: Bearer <token>
Content-Type: application/json

{
  "file_name": "summer-dress.jpg",
  "content_type": "image/jpeg",
  "size_bytes": 245678,
  "purpose": "product_image"
}

⟶ الاستجابة

{
  "upload_url": "https://storage.zahraah.com/uploads/tmp/abc123.jpg?signature=...",
  "file_id": "file_abc123",
  "expires_at": "2025-01-08T12:15:00Z",
  "max_size_bytes": 5242880,
  "headers": {
    "Content-Type": "image/jpeg",
    "X-Amz-ACL": "private"
  }
}
```

---

## 2️⃣ الروابط الموقعة | Signed URLs {#الروابط-الموقعة}

### **توليد رابط موقع (Laravel + S3)**

```php
use Illuminate\Support\Facades\Storage;

// رابط رفع
$uploadUrl = Storage::disk('s3')->temporaryUploadUrl(
    "uploads/{$fileId}.jpg",
    now()->addMinutes(15),
    [
        'ContentType' => 'image/jpeg',
        'ACL' => 'private'
    ]
);

// رابط تنزيل
$downloadUrl = Storage::disk('s3')->temporaryUrl(
    "products/{$productId}/image.jpg",
    now()->addMinutes(10)
);
```

---

### **بنية الرابط الموقع**

```
https://storage.zahraah.com/path/to/file.jpg?
  X-Amz-Algorithm=AWS4-HMAC-SHA256&
  X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F...&
  X-Amz-Date=20250108T120000Z&
  X-Amz-Expires=900&
  X-Amz-SignedHeaders=host&
  X-Amz-Signature=abc123...

المكونات:
- Algorithm: خوارزمية التوقيع
- Credential: مفاتيح الوصول
- Date: وقت الإنشاء
- Expires: مدة الصلاحية (بالثواني)
- Signature: التوقيع المحسوب
```

---

## 3️⃣ أنواع الملفات المسموحة | Allowed File Types {#أنواع-الملفات}

### **القائمة البيضاء**

```php
private $allowedMimeTypes = [
    // صور
    'image/jpeg' => ['jpg', 'jpeg'],
    'image/png' => ['png'],
    'image/webp' => ['webp'],
    'image/gif' => ['gif'],
    
    // مستندات
    'application/pdf' => ['pdf'],
    'application/msword' => ['doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' => ['docx'],
    
    // أخرى
    'text/plain' => ['txt'],
];

private $maxSizes = [
    'product_image' => 5 * 1024 * 1024,      // 5MB
    'customer_document' => 10 * 1024 * 1024, // 10MB
    'invoice' => 5 * 1024 * 1024,            // 5MB
];

public function validateFile(UploadedFile $file, string $purpose)
{
    // التحقق من النوع
    if (!in_array($file->getMimeType(), array_keys($this->allowedMimeTypes))) {
        abort(400, 'نوع الملف غير مسموح');
    }
    
    // التحقق من الحجم
    if ($file->getSize() > $this->maxSizes[$purpose]) {
        abort(400, 'حجم الملف كبير جدًا');
    }
    
    // التحقق من الامتداد
    $extension = $file->getClientOriginalExtension();
    $allowedExtensions = $this->allowedMimeTypes[$file->getMimeType()];
    
    if (!in_array($extension, $allowedExtensions)) {
        abort(400, 'امتداد الملف غير مسموح');
    }
    
    return true;
}
```

---

## 4️⃣ الأمان | Security {#الأمان}

### **حماية الرفع**

```php
public function processUpload(UploadedFile $file)
{
    // 1. التحقق من النوع والحجم
    $this->validateFile($file, 'product_image');
    
    // 2. اسم ملف آمن (UUID)
    $fileName = Str::uuid() . '.' . $file->getClientOriginalExtension();
    
    // 3. Scan للفيروسات (اختياري)
    if (config('security.virus_scan')) {
        $this->scanForViruses($file);
    }
    
    // 4. إزالة EXIF للصور (خصوصية)
    if (Str::startsWith($file->getMimeType(), 'image/')) {
        $this->stripExif($file);
    }
    
    // 5. الرفع إلى Storage
    $path = Storage::disk('s3')->putFileAs(
        "products/{$productId}",
        $file,
        $fileName,
        'private'  // ACL
    );
    
    // 6. حفظ Metadata
    $fileRecord = File::create([
        'id' => Str::uuid(),
        'original_name' => $file->getClientOriginalName(),
        'file_name' => $fileName,
        'mime_type' => $file->getMimeType(),
        'size_bytes' => $file->getSize(),
        'path' => $path,
        'owner_id' => auth()->id(),
        'purpose' => 'product_image',
        'checksum_sha256' => hash_file('sha256', $file->getRealPath())
    ]);
    
    return $fileRecord;
}
```

---

### **حماية التنزيل**

```php
public function download(string $fileId)
{
    $file = File::findOrFail($fileId);
    
    // 1. التحقق من الصلاحية
    if ($file->owner_id !== auth()->id() && !auth()->user()->isAdmin()) {
        abort(403, 'غير مصرح بالوصول لهذا الملف');
    }
    
    // 2. توليد رابط موقع قصير العمر
    $url = Storage::disk('s3')->temporaryUrl(
        $file->path,
        now()->addMinutes(5),  // 5 دقائق فقط
        [
            'ResponseContentDisposition' => 'attachment; filename="' . $file->original_name . '"',
            'ResponseContentType' => $file->mime_type
        ]
    );
    
    return response()->json([
        'download_url' => $url,
        'expires_at' => now()->addMinutes(5)->toIso8601String(),
        'file_name' => $file->original_name,
        'size_bytes' => $file->size_bytes
    ]);
}
```

---

## 5️⃣ أمثلة عملية | Practical Examples {#أمثلة-عملية}

### **مثال 1: رفع صورة منتج**

```javascript
// Flutter/JavaScript
async function uploadProductImage(file) {
  // 1. طلب رابط موقع
  const response = await fetch('/v1/uploads/presigned', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      file_name: file.name,
      content_type: file.type,
      size_bytes: file.size,
      purpose: 'product_image'
    })
  });
  
  const { upload_url, file_id } = await response.json();
  
  // 2. رفع مباشر للتخزين
  await fetch(upload_url, {
    method: 'PUT',
    headers: {
      'Content-Type': file.type
    },
    body: file
  });
  
  // 3. تأكيد الرفع
  await fetch(`/v1/uploads/${file_id}/confirm`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return file_id;
}
```

---

### **مثال 2: تنزيل فاتورة**

```javascript
async function downloadInvoice(orderId) {
  // 1. طلب رابط تنزيل موقع
  const response = await fetch(`/v1/orders/${orderId}/invoice`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const { download_url, file_name } = await response.json();
  
  // 2. تنزيل الملف
  const link = document.createElement('a');
  link.href = download_url;
  link.download = file_name;
  link.click();
}
```

---

## ✅ **قائمة التحقق | Checklist**

### **الرفع**
- [ ] القائمة البيضاء للأنواع
- [ ] حد أقصى للحجم
- [ ] اسم ملف آمن (UUID)
- [ ] Virus scan (اختياري)
- [ ] إزالة EXIF
- [ ] حفظ Metadata كامل
- [ ] Checksum للتحقق

### **التنزيل**
- [ ] التحقق من الصلاحية
- [ ] روابط قصيرة العمر (5-10 دقائق)
- [ ] صلاحيات محددة (read-only)
- [ ] Content-Disposition للتنزيل
- [ ] تسجيل الوصول (Audit)

---

## 🔗 **التنقل | Navigation**

[← السابق: التحقق والمخططات | Previous: Validation](04_Validation_Schemas.md)

[التالي: العمليات غير المتزامنة | Next: Async Operations →](06_Async_Operations.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
