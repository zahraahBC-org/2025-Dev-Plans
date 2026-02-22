# قوالب الكود — Code Templates

---

## **Controller Template**

```php
// Controller Template - Key methods only
class ResourceController extends Controller
{
    public function __construct(private ResourceService $service) {}
    
    public function index()
    {
        return ResourceResource::collection($this->service->getAll(request()->all()));
    }
    
    public function store(StoreResourceRequest $request)
    {
        return (new ResourceResource($this->service->create($request->validated())))
            ->setStatusCode(201);
    }
    
    public function show(int $id)
    {
        return new ResourceResource($this->service->find($id));
    }
}
```

---

**آخر تحديث | Last Updated**: October 20, 2025  
**الإصدار | Version**: 2.0
