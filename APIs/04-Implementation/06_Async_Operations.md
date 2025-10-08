# 06. العمليات غير المتزامنة | Asynchronous Operations

## 🎯 **نظرة عامة | Overview**

إدارة العمليات الطويلة بشكل غير متزامن لتحسين تجربة المستخدم وأداء النظام.

**الهدف | Purpose**: معالجة غير متزامنة للمهام الطويلة  
**الجمهور | Audience**: مطورو Backend  
**المتطلبات | Prerequisites**: فهم [العمارة](../02-Architecture/01_Architecture_Overview.md)

---

## 📋 **جدول المحتويات | Table of Contents**

1. [متى نستخدم Async](#متى-async)
2. [نمط 202 Accepted](#نمط-202)
3. [Job Status Endpoint](#job-status)
4. [التنفيذ](#التنفيذ)
5. [أمثلة عملية](#أمثلة-عملية)

---

## 1️⃣ متى نستخدم Async | When to Use Async {#متى-async}

### **العمليات المناسبة**

```
✅ يجب Async:
- توليد تقارير (> 10 ثوان)
- معالجة دفعية (bulk operations)
- تحويل صور/فيديو
- إرسال آلاف الإشعارات
- تصدير بيانات كبيرة
- عمليات تكامل طويلة

❌ لا يجب Async:
- CRUD بسيط (< 1 ثانية)
- قراءة بيانات
- عمليات تفاعلية
```

---

## 2️⃣ نمط 202 Accepted {#نمط-202}

### **التدفق الأساسي**

```
1. العميل يُرسل الطلب
   POST /v1/reports/sales
   
2. الخادم يقبل ويُرجع 202
   HTTP/1.1 202 Accepted
   Location: /v1/jobs/job-abc123
   
3. العميل يستعلم عن الحالة
   GET /v1/jobs/job-abc123
   → { "status": "processing", "progress": 45 }
   
4. بعد الاكتمال
   GET /v1/jobs/job-abc123
   → { "status": "completed", "result_url": "..." }
```

---

### **الاستجابة 202**

```http
POST /v1/reports/sales
Authorization: Bearer <token>
{
  "from": "2025-01-01",
  "to": "2025-01-31",
  "format": "pdf"
}

⟶ الاستجابة

HTTP/1.1 202 Accepted
Location: /v1/jobs/job-20250108-abc123
Content-Type: application/json

{
  "job_id": "job-20250108-abc123",
  "status": "pending",
  "created_at": "2025-01-08T12:00:00Z",
  "estimated_completion": "2025-01-08T12:05:00Z",
  "status_url": "/v1/jobs/job-20250108-abc123"
}
```

---

## 3️⃣ Job Status Endpoint {#job-status}

### **حالات Job**

```
pending      - في الانتظار
processing   - قيد المعالجة
completed    - مكتمل
failed       - فشل
cancelled    - ملغي
```

---

### **Endpoint: فحص حالة Job**

```http
GET /v1/jobs/job-20250108-abc123
Authorization: Bearer <token>

⟶ الاستجابة (قيد المعالجة)

HTTP/1.1 200 OK

{
  "job_id": "job-20250108-abc123",
  "status": "processing",
  "progress": 65,
  "message": "معالجة البيانات...",
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T12:03:00Z"
}

⟶ الاستجابة (مكتمل)

HTTP/1.1 200 OK

{
  "job_id": "job-20250108-abc123",
  "status": "completed",
  "progress": 100,
  "result": {
    "file_url": "https://storage.zahraah.com/reports/sales-jan-2025.pdf?signature=...",
    "expires_at": "2025-01-08T13:00:00Z",
    "size_bytes": 245678
  },
  "created_at": "2025-01-08T12:00:00Z",
  "completed_at": "2025-01-08T12:04:32Z"
}

⟶ الاستجابة (فشل)

HTTP/1.1 200 OK

{
  "job_id": "job-20250108-abc123",
  "status": "failed",
  "error": {
    "code": "E7005",
    "message": "فشل توليد التقرير",
    "details": "بيانات غير كافية للفترة المحددة"
  },
  "created_at": "2025-01-08T12:00:00Z",
  "failed_at": "2025-01-08T12:02:15Z"
}
```

---

## 4️⃣ التنفيذ | Implementation {#التنفيذ}

### **جدول Jobs**

```sql
CREATE TABLE jobs (
    id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') NOT NULL,
    progress TINYINT UNSIGNED DEFAULT 0,
    
    -- المدخلات
    input_data JSON NOT NULL,
    
    -- النتائج
    result_data JSON NULL,
    error_message TEXT NULL,
    
    -- الأوقات
    created_at DATETIME NOT NULL,
    started_at DATETIME NULL,
    completed_at DATETIME NULL,
    failed_at DATETIME NULL,
    
    -- TTL
    expires_at DATETIME NOT NULL,
    
    INDEX idx_user_status (user_id, status),
    INDEX idx_created (created_at),
    INDEX idx_expires (expires_at)
);
```

---

### **Controller**

```php
public function generateReport(Request $request)
{
    $validated = $request->validate([
        'from' => 'required|date',
        'to' => 'required|date|after:from',
        'format' => 'required|in:pdf,excel,csv'
    ]);
    
    // إنشاء Job
    $job = Job::create([
        'id' => 'job-' . now()->format('Ymd') . '-' . Str::random(6),
        'user_id' => auth()->id(),
        'type' => 'sales_report',
        'status' => 'pending',
        'input_data' => $validated,
        'expires_at' => now()->addHours(24)
    ]);
    
    // وضع في Queue
    GenerateSalesReport::dispatch($job->id)
        ->onQueue('reports');
    
    // إرجاع 202
    return response()->json([
        'job_id' => $job->id,
        'status' => 'pending',
        'status_url' => route('jobs.show', $job->id),
        'created_at' => $job->created_at->toIso8601String(),
        'estimated_completion' => now()->addMinutes(5)->toIso8601String()
    ], 202)
    ->header('Location', route('jobs.show', $job->id));
}

public function checkStatus(string $jobId)
{
    $job = Job::where('id', $jobId)
              ->where('user_id', auth()->id())
              ->firstOrFail();
    
    return response()->json([
        'job_id' => $job->id,
        'status' => $job->status,
        'progress' => $job->progress,
        'result' => $job->result_data,
        'error' => $job->status === 'failed' ? [
            'message' => $job->error_message
        ] : null,
        'created_at' => $job->created_at,
        'completed_at' => $job->completed_at
    ]);
}
```

---

### **Worker (Job Class)**

```php
<?php

namespace App\Jobs;

use App\Models\Job;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class GenerateSalesReport implements ShouldQueue
{
    use InteractsWithQueue, Queueable;
    
    public function __construct(
        private string $jobId
    ) {}
    
    public function handle()
    {
        $job = Job::find($this->jobId);
        
        try {
            // تحديث الحالة
            $job->update([
                'status' => 'processing',
                'started_at' => now()
            ]);
            
            // المعالجة
            $data = $job->input_data;
            $orders = Order::whereBetween('created_at', [$data['from'], $data['to']])->get();
            
            // تحديث Progress
            $job->update(['progress' => 50]);
            
            // توليد التقرير
            $pdfPath = $this->generatePDF($orders);
            
            // رفع للتخزين
            $url = Storage::disk('s3')->putFile('reports', $pdfPath);
            $signedUrl = Storage::disk('s3')->temporaryUrl($url, now()->addHour());
            
            // تحديث النتيجة
            $job->update([
                'status' => 'completed',
                'progress' => 100,
                'result_data' => [
                    'file_url' => $signedUrl,
                    'expires_at' => now()->addHour(),
                    'size_bytes' => Storage::size($url)
                ],
                'completed_at' => now()
            ]);
            
            // إشعار (اختياري)
            $job->user->notify(new ReportReady($job));
            
        } catch (\Exception $e) {
            $job->update([
                'status' => 'failed',
                'error_message' => $e->getMessage(),
                'failed_at' => now()
            ]);
            
            throw $e;
        }
    }
}
```

---

## ✅ **قائمة التحقق | Checklist**

### **التنفيذ**
- [ ] استجابة 202 Accepted
- [ ] Location header للـ job
- [ ] Job status endpoint
- [ ] حالات واضحة (pending، processing، completed، failed)
- [ ] progress indicator
- [ ] TTL للـ jobs (تنظيف)
- [ ] Authorization check للـ job access
- [ ] Webhook notification (اختياري)

---

## 🔗 **التنقل | Navigation**

[← السابق: الملفات | Previous: Files & Signed URLs](05_Files_Signed_URLs.md)

[التالي: الكاش والأداء | Next: Caching & Performance →](../05-Operations/01_Caching_Performance.md)

[🏠 العودة للفهرس | Back to Index](../index.md)

---

**الإصدار | Version**: 1.0  
**آخر تحديث | Last Updated**: 2025-01-08  
**الحالة | Status**: ✅ مراجع ومعتمد | Reviewed and Approved
