# رفع الملفات والتخزين — File Uploads & Storage
**الأهمية | Importance**: 🟡 متوسطة-عالية

---

## **الهدف | Objective**

تنفيذ رفع وتخزين الملفات (صور، مستندات) بشكل آمن وفعال.

---

## **أنواع الملفات الشائعة | Common File Types**

### **للتطبيقات التجارية:**

```
صور المنتجات:
├── JPG, PNG, WebP
├── Max: 5MB
└── Dimensions: 1200x1200px max

صور المستخدمين (Avatar):
├── JPG, PNG
├── Max: 2MB
└── Dimensions: 500x500px

المستندات:
├── PDF
├── Max: 10MB
└── للفواتير، إثباتات الدفع
```

---

## **التنفيذ | Implementation**

### **1. Configuration**

```php
// config/filesystems.php
'disks' => [
    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
    ],
    
    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
        'url' => env('AWS_URL'),
    ],
],
```

---

### **2. Upload Endpoint Example**

```php
public function upload(Request $request)
{
    $request->validate([
        'file' => ['required', 'file', 'max:5120', 'mimes:jpeg,png,jpg'],
        'type' => 'required|in:product,avatar',
    ]);
    
    $file = $request->file('file');
    $filename = Str::uuid() . '.' . $file->getClientOriginalExtension();
    $path = $file->storeAs("uploads/{$request->type}", $filename, 'public');
    
    $upload = Upload::create([
        'user_id' => auth()->id(),
        'filename' => $filename,
        'path' => $path,
        'mime_type' => $file->getMimeType(),
        'size' => $file->getSize(),
        'type' => $request->type,
    ]);
    
    return response()->json([
        'data' => ['id' => $upload->id, 'url' => Storage::url($path)],
    ], 201);
}

public function destroy(int $id)
{
    $upload = Upload::where('id', $id)->where('user_id', auth()->id())->firstOrFail();
    Storage::disk('public')->delete($upload->path);
    $upload->delete();
    
    return response()->json(['message' => 'Deleted'], 204);
}
```

---

### **3. Model Example**

```php
class Upload extends Model
{
    protected $fillable = ['user_id', 'filename', 'path', 'mime_type', 'size', 'type'];
    protected $appends = ['url'];
    
    public function getUrlAttribute(): string
    {
        return Storage::url($this->path);
    }
    
    // Auto-delete file when record is deleted
    protected static function booted()
    {
        static::deleted(fn($upload) => Storage::disk('public')->delete($upload->path));
    }
}
```

---

### **4. Database Schema**

```php
// Refer to Database plan for full schema
Schema::create('uploads', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->nullable()
        ->constrained()->onDelete('set null');
    $table->string('filename');
    $table->string('path');
    $table->string('type', 50);  // product, avatar, document
    // ... other columns - see Database plan
    $table->timestamps();
});
```

---

## ️ **Image Processing (اختياري)**

```bash
composer require intervention/image
```

```php
use Intervention\Image\Facades\Image;

public function upload(Request $request)
{
    $file = $request->file('file');
    
    if (in_array($file->getMimeType(), ['image/jpeg', 'image/png'])) {
        // Resize & optimize
        $image = Image::make($file)
            ->resize(1200, 1200, function ($constraint) {
                $constraint->aspectRatio();
                $constraint->upsize();
            })
            ->encode('jpg', 85);
        
        // Save optimized
        $filename = Str::uuid() . '.jpg';
        Storage::put("uploads/products/{$filename}", $image);
        
        // Generate thumbnail
        $thumbnail = Image::make($file)
            ->fit(300, 300)
            ->encode('jpg', 75);
        
        Storage::put("uploads/products/thumbs/{$filename}", $thumbnail);
    }
}
```

---

## **Security Best Practices**

### **1. Validation صارم:**

```php
$request->validate([
    'file' => [
        'required',
        'file',
        'max:5120',  // 5MB
        'mimes:jpeg,png,jpg,webp',  // Whitelist only
        
        // Custom validation
        function ($attribute, $value, $fail) {
            // تحقق من الـmagic bytes (حماية من تزوير الامتداد)
            $finfo = finfo_open(FILEINFO_MIME_TYPE);
            $mimeType = finfo_file($finfo, $value->getRealPath());
            
            if (!in_array($mimeType, ['image/jpeg', 'image/png'])) {
                $fail('نوع الملف غير صالح');
            }
        },
    ],
]);
```

---

### **2. Storage خارج public_html:**

**DO:**
- `storage/app/uploads/` (آمن)
- S3 private bucket

**DON'T:**
- `public_html/uploads/` (خطير)

---

### **3. Signed URLs (للتحكم في الوصول):**

```php
// Generate signed URL (valid for 1 hour)
$url = Storage::temporaryUrl(
    $upload->path,
    now()->addHour()
);

return response()->json([
    'url' => $url,
    'expires_at' => now()->addHour(),
]);
```

---

### **4. Virus Scanning (إنتاج):**

```bash
composer require clamav/clamav
```

```php
use ClamAV\Scanner;

$scanner = new Scanner();
$result = $scanner->scan($file->getRealPath());

if ($result->isInfected()) {
    return response()->json([
        'success' => false,
        'message' => 'الملف مصاب بفيروس',
    ], 400);
}
```

---

## **Cleanup Example**

```php
// Delete orphaned files
class CleanupOrphanedFiles extends Command
{
    public function handle(): int
    {
        foreach (Storage::allFiles('uploads') as $file) {
            if (!Upload::where('filename', basename($file))->exists()) {
                Storage::delete($file);
            }
        }
        
        // Delete old temp uploads (>6 months)
        Upload::where('created_at', '<', now()->subMonths(6))
            ->where('type', 'temp')
            ->each->delete();
        
        return 0;
    }
}
```

---

## **Testing Example**

```php
public function test_can_upload_image(): void
{
    Storage::fake('public');
    $file = UploadedFile::fake()->image('product.jpg');
    
    $response = $this->actingAs($user, 'sanctum')
        ->post('/api/v1/uploads', ['file' => $file, 'type' => 'product']);
    
    $response->assertStatus(201)->assertJsonStructure(['data' => ['id', 'url']]);
    
    $filename = $response->json('data.filename');
    Storage::disk('public')->assertExists("uploads/product/{$filename}");
}

public function test_rejects_invalid_file_type(): void
{
    $response = $this->post('/api/v1/uploads', [
        'file' => UploadedFile::fake()->create('doc.exe'),
    ]);
    
    $response->assertStatus(422);
}
```

---

## **Checklist**

### **Setup:**
- [ ] Storage disk محدد (local/s3)
- [ ] Public disk link (`php artisan storage:link`)
- [ ] File size limits محددة
- [ ] Allowed mimes محددة

### **Security:**
- [ ] File validation صارم
- [ ] Magic bytes check
- [ ] Unique filenames (UUID)
- [ ] Storage خارج public (أو S3 private)
- [ ] Virus scanning (production)

### **Features:**
- [ ] Single upload endpoint
- [ ] Batch upload endpoint
- [ ] Delete endpoint
- [ ] Image optimization (optional)
- [ ] Thumbnail generation (optional)

### **Cleanup:**
- [ ] Orphaned files cleanup
- [ ] Old temp files cleanup
- [ ] مجدول (weekly/monthly)

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
