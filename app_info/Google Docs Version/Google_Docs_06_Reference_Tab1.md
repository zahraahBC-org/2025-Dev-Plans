# TAB 1: قوالب الكود | Code Templates

## 26. قوالب الكود والأدوات
### Code Templates & Tools

---

## 🎯 **الهدف | Objective**
تطبيق قوالب الكود لتطبيق Flutter للتجارة الإلكترونية قوي وقابل للصيانة.

## 📋 **Rule | القاعدة**
**Arabic**: قوالب جاهزة للنسخ والاستخدام في المشروع  
**English**: Ready-to-use templates for copying and using in the project

## 💡 **Benefits | الفوائد**
- **Development Speed | سرعة التطوير**: Quick code generation
- **Consistency | الاتساق**: Standardized code patterns
- **Best Practices | أفضل الممارسات**: Built-in best practices
- **Team Onboarding | إدماج الفريق**: Easy for new team members
- **Code Quality | جودة الكود**: Consistent, high-quality code
- **Time Saving | توفير الوقت**: Reduce repetitive coding

## 🛠️ **التطبيق | Implementation**
- **الاستخدام في**: جميع أنشطة التطوير وإنشاء الكود
- **كيفية التطبيق**:
  - إنشاء مكتبة قوالب شاملة
  - توثيق استخدام القوالب
  - تقديم أمثلة وأفضل الممارسات
  - الحفاظ على تحديث القوالب
  - إضافة تكامل IDE
- **النتيجة**: تطوير فعال مع جودة كود متسقة

## 🎯 **الأولويات المحددة | Specific Priorities**

### **أولويات خاصة بقوالب الكود | Code Templates Specific Priorities:**
#### **المرحلة الأولى: الأساس | Phase 1: Foundation**
- **🔴 حرج**: إنشاء مكتبة قوالب شاملة
- **🔴 حرج**: توثيق استخدام القوالب
- **🟠 عالي**: تقديم أمثلة وأفضل الممارسات

#### **المرحلة الثانية: التحسين | Phase 2: Enhancement**
- **🟠 عالي**: الحفاظ على تحديث القوالب
- **🟠 عالي**: إضافة تكامل IDE
- **🟡 متوسط**: إضافة ميزات قوالب متقدمة

#### **المرحلة الثالثة: التحسين | Phase 3: Optimization**
- **🟡 متوسط**: تخصيص قوالب متقدم
- **🟡 متوسط**: إنشاء قوالب مدعوم بالذكاء الاصطناعي
- **🟢 منخفض**: اقتراحات قوالب تنبؤية

## 📈 **Success Metrics | مؤشرات النجاح**

### **مقاييس خاصة بقوالب الكود | Code Templates Specific Metrics:**
- **استخدام القوالب | Template Usage**: >80% template adoption
- **سرعة التطوير | Development Speed**: 50%+ faster development
- **اتساق الكود | Code Consistency**: 100% consistent patterns
- **تغطية القوالب | Template Coverage**: 100% common patterns covered
- **تبني الفريق | Team Adoption**: >90% team adoption
- **تحديثات القوالب | Template Updates**: Monthly template updates

## ⚠️ **Common Pitfalls & Best Practices | الأخطاء الشائعة وأفضل الممارسات**

### **أخطاء شائعة خاصة بقوالب الكود | Code Templates Specific Pitfalls:**
- **تجنب | Avoid**: قوالب قديمة أو غير مكتملة
- **تجنب | Avoid**: توثيق قوالب ضعيف
- **تجنب | Avoid**: عدم وجود أمثلة القوالب
- **تجنب | Avoid**: عدم وجود صيانة القوالب
- **تجنب | Avoid**: تنظيم قوالب ضعيف

### **أفضل الممارسات | Best Practices:**
- **استخدم | Use**: مكتبة قوالب شاملة
- **استخدم | Use**: توثيق قوالب واضح
- **استخدم | Use**: تحديثات قوالب منتظمة
- **استخدم | Use**: وصول سهل للقوالب
- **استخدم | Use**: تحكم إصدار القوالب

## 🏗️ **Architecture Templates | قوالب المعمارية**

### **1. Clean Architecture Template | قالب المعمارية النظيفة**
```dart
// lib/features/[feature_name]/domain/entities/[entity_name].dart
class [EntityName] {
  final String id;
  final String name;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const [EntityName]({
    required this.id,
    required this.name,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory [EntityName].fromJson(Map<String, dynamic> json) {
    return [EntityName](
      id: json['id'] as String,
      name: json['name'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
  
  [EntityName] copyWith({
    String? id,
    String? name,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return [EntityName](
      id: id ?? this.id,
      name: name ?? this.name,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is [EntityName] &&
        other.id == id &&
        other.name == name &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt;
  }
  
  @override
  int get hashCode {
    return id.hashCode ^
        name.hashCode ^
        createdAt.hashCode ^
        updatedAt.hashCode;
  }
  
  @override
  String toString() {
    return '[EntityName](id: $id, name: $name, createdAt: $createdAt, updatedAt: $updatedAt)';
  }
}
```

### **2. Repository Template | قالب المستودع**
```dart
// lib/features/[feature_name]/data/repositories/[repository_name]_repository_impl.dart
class [RepositoryName]RepositoryImpl implements [RepositoryName]Repository {
  final [RepositoryName]DataSource _dataSource;
  final [RepositoryName]Mapper _mapper;
  
  [RepositoryName]RepositoryImpl({
    required [RepositoryName]DataSource dataSource,
    required [RepositoryName]Mapper mapper,
  }) : _dataSource = dataSource,
       _mapper = mapper;
  
  @override
  Future<Result<[EntityName]>> get[EntityName](String id) async {
    try {
      final dto = await _dataSource.get[EntityName](id);
      final entity = _mapper.toEntity(dto);
      return Result.success(entity);
    } catch (e) {
      return Result.failure(RepositoryException('Failed to get [EntityName]: ${e.toString()}'));
    }
  }
  
  @override
  Future<Result<List<[EntityName]>>> getAll[EntityName]s() async {
    try {
      final dtos = await _dataSource.getAll[EntityName]s();
      final entities = dtos.map((dto) => _mapper.toEntity(dto)).toList();
      return Result.success(entities);
    } catch (e) {
      return Result.failure(RepositoryException('Failed to get all [EntityName]s: ${e.toString()}'));
    }
  }
  
  @override
  Future<Result<[EntityName]>> create[EntityName]([EntityName] entity) async {
    try {
      final dto = _mapper.toDto(entity);
      final createdDto = await _dataSource.create[EntityName](dto);
      final createdEntity = _mapper.toEntity(createdDto);
      return Result.success(createdEntity);
    } catch (e) {
      return Result.failure(RepositoryException('Failed to create [EntityName]: ${e.toString()}'));
    }
  }
  
  @override
  Future<Result<[EntityName]>> update[EntityName]([EntityName] entity) async {
    try {
      final dto = _mapper.toDto(entity);
      final updatedDto = await _dataSource.update[EntityName](dto);
      final updatedEntity = _mapper.toEntity(updatedDto);
      return Result.success(updatedEntity);
    } catch (e) {
      return Result.failure(RepositoryException('Failed to update [EntityName]: ${e.toString()}'));
    }
  }
  
  @override
  Future<Result<void>> delete[EntityName](String id) async {
    try {
      await _dataSource.delete[EntityName](id);
      return Result.success(null);
    } catch (e) {
      return Result.failure(RepositoryException('Failed to delete [EntityName]: ${e.toString()}'));
    }
  }
}
```

### **3. Use Case Template | قالب حالة الاستخدام**
```dart
// lib/features/[feature_name]/domain/usecases/[use_case_name]_use_case.dart
class [UseCaseName]UseCase {
  final [RepositoryName]Repository _repository;
  
  [UseCaseName]UseCase({
    required [RepositoryName]Repository repository,
  }) : _repository = repository;
  
  Future<Result<[ReturnType]>> execute([UseCaseName]Params params) async {
    try {
      // Validate parameters
      final validationResult = _validateParams(params);
      if (!validationResult.isValid) {
        return Result.failure(ValidationException(validationResult.errorMessage));
      }
      
      // Execute business logic
      final result = await _executeBusinessLogic(params);
      
      return Result.success(result);
    } catch (e) {
      return Result.failure(UseCaseException('Failed to execute [UseCaseName]: ${e.toString()}'));
    }
  }
  
  ValidationResult _validateParams([UseCaseName]Params params) {
    // Implement parameter validation
    return ValidationResult.valid();
  }
  
  Future<[ReturnType]> _executeBusinessLogic([UseCaseName]Params params) async {
    // Implement business logic
    throw UnimplementedError();
  }
}

class [UseCaseName]Params {
  final String param1;
  final int param2;
  final bool param3;
  
  const [UseCaseName]Params({
    required this.param1,
    required this.param2,
    required this.param3,
  });
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is [UseCaseName]Params &&
        other.param1 == param1 &&
        other.param2 == param2 &&
        other.param3 == param3;
  }
  
  @override
  int get hashCode {
    return param1.hashCode ^ param2.hashCode ^ param3.hashCode;
  }
}
```

## 🎨 **UI Templates | قوالب واجهة المستخدم**

### **1. Screen Template | قالب الشاشة**
```dart
// lib/features/[feature_name]/presentation/pages/[screen_name]_page.dart
class [ScreenName]Page extends StatefulWidget {
  const [ScreenName]Page({super.key});
  
  @override
  State<[ScreenName]Page> createState() => _[ScreenName]PageState();
}

class _[ScreenName]PageState extends State<[ScreenName]Page> {
  late final [ScreenName]Bloc _bloc;
  
  @override
  void initState() {
    super.initState();
    _bloc = context.read<[ScreenName]Bloc>();
    _bloc.add([ScreenName]Initialized());
  }
  
  @override
  void dispose() {
    _bloc.close();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('[Screen Name]'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _bloc.add([ScreenName]Refreshed()),
          ),
        ],
      ),
      body: BlocConsumer<[ScreenName]Bloc, [ScreenName]State>(
        listener: (context, state) {
          if (state is [ScreenName]Error) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(state.message),
                backgroundColor: Colors.red,
              ),
            );
          }
        },
        builder: (context, state) {
          if (state is [ScreenName]Loading) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (state is [ScreenName]Error) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(
                    'حدث خطأ',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    state.message,
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: () => _bloc.add([ScreenName]Refreshed()),
                    child: const Text('إعادة المحاولة'),
                  ),
                ],
              ),
            );
          }
          
          if (state is [ScreenName]Loaded) {
            return _buildLoadedContent(state);
          }
          
          return const SizedBox.shrink();
        },
      ),
    );
  }
  
  Widget _buildLoadedContent([ScreenName]Loaded state) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Add your content here
          Text(
            'Content loaded successfully',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
        ],
      ),
    );
  }
}
```

### **2. Widget Template | قالب العنصر**
```dart
// lib/features/[feature_name]/presentation/widgets/[widget_name]_widget.dart
class [WidgetName]Widget extends StatelessWidget {
  final [DataType] data;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;
  
  const [WidgetName]Widget({
    super.key,
    required this.data,
    this.onTap,
    this.onLongPress,
  });
  
  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: InkWell(
        onTap: onTap,
        onLongPress: onLongPress,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildHeader(),
              const SizedBox(height: 8),
              _buildContent(),
              if (data.hasActions) ...[
                const SizedBox(height: 16),
                _buildActions(),
              ],
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _buildHeader() {
    return Row(
      children: [
        Expanded(
          child: Text(
            data.title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        if (data.isImportant)
          const Icon(
            Icons.star,
            color: Colors.amber,
            size: 20,
          ),
      ],
    );
  }
  
  Widget _buildContent() {
    return Text(
      data.description,
      style: const TextStyle(
        fontSize: 14,
        color: Colors.grey,
      ),
    );
  }
  
  Widget _buildActions() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        TextButton(
          onPressed: onTap,
          child: const Text('عرض'),
        ),
        const SizedBox(width: 8),
        TextButton(
          onPressed: onLongPress,
          child: const Text('تحرير'),
        ),
      ],
    );
  }
}
```

### **3. Form Template | قالب النموذج**
```dart
// lib/features/[feature_name]/presentation/widgets/[form_name]_form.dart
class [FormName]Form extends StatefulWidget {
  final [FormName]Data? initialData;
  final Function([FormName]Data) onSubmit;
  final VoidCallback? onCancel;
  
  const [FormName]Form({
    super.key,
    this.initialData,
    required this.onSubmit,
    this.onCancel,
  });
  
  @override
  State<[FormName]Form> createState() => _[FormName]FormState();
}

class _[FormName]FormState extends State<[FormName]Form> {
  final _formKey = GlobalKey<FormState>();
  final _field1Controller = TextEditingController();
  final _field2Controller = TextEditingController();
  final _field3Controller = TextEditingController();
  
  @override
  void initState() {
    super.initState();
    if (widget.initialData != null) {
      _field1Controller.text = widget.initialData!.field1;
      _field2Controller.text = widget.initialData!.field2;
      _field3Controller.text = widget.initialData!.field3;
    }
  }
  
  @override
  void dispose() {
    _field1Controller.dispose();
    _field2Controller.dispose();
    _field3Controller.dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          _buildField1(),
          const SizedBox(height: 16),
          _buildField2(),
          const SizedBox(height: 16),
          _buildField3(),
          const SizedBox(height: 24),
          _buildButtons(),
        ],
      ),
    );
  }
  
  Widget _buildField1() {
    return TextFormField(
      controller: _field1Controller,
      decoration: const InputDecoration(
        labelText: 'Field 1',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Field 1 is required';
        }
        return null;
      },
    );
  }
  
  Widget _buildField2() {
    return TextFormField(
      controller: _field2Controller,
      decoration: const InputDecoration(
        labelText: 'Field 2',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Field 2 is required';
        }
        return null;
      },
    );
  }
  
  Widget _buildField3() {
    return TextFormField(
      controller: _field3Controller,
      decoration: const InputDecoration(
        labelText: 'Field 3',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Field 3 is required';
        }
        return null;
      },
    );
  }
  
  Widget _buildButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        if (widget.onCancel != null)
          TextButton(
            onPressed: widget.onCancel,
            child: const Text('إلغاء'),
          ),
        const SizedBox(width: 8),
        ElevatedButton(
          onPressed: _submitForm,
          child: const Text('حفظ'),
        ),
      ],
    );
  }
  
  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      final data = [FormName]Data(
        field1: _field1Controller.text,
        field2: _field2Controller.text,
        field3: _field3Controller.text,
      );
      widget.onSubmit(data);
    }
  }
}

class [FormName]Data {
  final String field1;
  final String field2;
  final String field3;
  
  const [FormName]Data({
    required this.field1,
    required this.field2,
    required this.field3,
  });
}
```

## 🔧 **State Management Templates | قوالب إدارة الحالة**

### **1. BLoC Template | قالب BLoC**
```dart
// lib/features/[feature_name]/presentation/bloc/[bloc_name]_bloc.dart
class [BlocName]Bloc extends Bloc<[BlocName]Event, [BlocName]State> {
  final [UseCaseName]UseCase _useCase;
  
  [BlocName]Bloc({
    required [UseCaseName]UseCase useCase,
  }) : _useCase = useCase,
       super([BlocName]Initial()) {
    on<[BlocName]Event>(_onEvent);
  }
  
  Future<void> _onEvent(
    [BlocName]Event event,
    Emitter<[BlocName]State> emit,
  ) async {
    switch (event) {
      case [BlocName]Initialized():
        await _onInitialized(event, emit);
      case [BlocName]Refreshed():
        await _onRefreshed(event, emit);
      case [BlocName]DataRequested():
        await _onDataRequested(event, emit);
    }
  }
  
  Future<void> _onInitialized(
    [BlocName]Initialized event,
    Emitter<[BlocName]State> emit,
  ) async {
    emit([BlocName]Loading());
    
    try {
      final result = await _useCase.execute([UseCaseName]Params(
        param1: event.param1,
        param2: event.param2,
        param3: event.param3,
      ));
      
      if (result.isSuccess) {
        emit([BlocName]Loaded(data: result.data!));
      } else {
        emit([BlocName]Error(message: result.error.toString()));
      }
    } catch (e) {
      emit([BlocName]Error(message: e.toString()));
    }
  }
  
  Future<void> _onRefreshed(
    [BlocName]Refreshed event,
    Emitter<[BlocName]State> emit,
  ) async {
    // Implement refresh logic
  }
  
  Future<void> _onDataRequested(
    [BlocName]DataRequested event,
    Emitter<[BlocName]State> emit,
  ) async {
    // Implement data request logic
  }
}

// Events
abstract class [BlocName]Event extends Equatable {
  const [BlocName]Event();
  
  @override
  List<Object?> get props => [];
}

class [BlocName]Initialized extends [BlocName]Event {
  final String param1;
  final int param2;
  final bool param3;
  
  const [BlocName]Initialized({
    required this.param1,
    required this.param2,
    required this.param3,
  });
  
  @override
  List<Object?> get props => [param1, param2, param3];
}

class [BlocName]Refreshed extends [BlocName]Event {
  const [BlocName]Refreshed();
}

class [BlocName]DataRequested extends [BlocName]Event {
  final String dataId;
  
  const [BlocName]DataRequested({required this.dataId});
  
  @override
  List<Object?> get props => [dataId];
}

// States
abstract class [BlocName]State extends Equatable {
  const [BlocName]State();
  
  @override
  List<Object?> get props => [];
}

class [BlocName]Initial extends [BlocName]State {
  const [BlocName]Initial();
}

class [BlocName]Loading extends [BlocName]State {
  const [BlocName]Loading();
}

class [BlocName]Loaded extends [BlocName]State {
  final [DataType] data;
  
  const [BlocName]Loaded({required this.data});
  
  @override
  List<Object?> get props => [data];
}

class [BlocName]Error extends [BlocName]State {
  final String message;
  
  const [BlocName]Error({required this.message});
  
  @override
  List<Object?> get props => [message];
}
```

### **2. Provider Template | قالب Provider**
```dart
// lib/features/[feature_name]/presentation/providers/[provider_name]_provider.dart
class [ProviderName]Provider extends StateNotifier<[ProviderName]State> {
  final [UseCaseName]UseCase _useCase;
  
  [ProviderName]Provider({
    required [UseCaseName]UseCase useCase,
  }) : _useCase = useCase,
       super(const [ProviderName]State.initial());
  
  Future<void> initialize() async {
    state = const [ProviderName]State.loading();
    
    try {
      final result = await _useCase.execute([UseCaseName]Params(
        param1: 'default',
        param2: 0,
        param3: false,
      ));
      
      if (result.isSuccess) {
        state = [ProviderName]State.loaded(data: result.data!);
      } else {
        state = [ProviderName]State.error(message: result.error.toString());
      }
    } catch (e) {
      state = [ProviderName]State.error(message: e.toString());
    }
  }
  
  Future<void> refresh() async {
    await initialize();
  }
  
  Future<void> requestData(String dataId) async {
    state = const [ProviderName]State.loading();
    
    try {
      final result = await _useCase.execute([UseCaseName]Params(
        param1: dataId,
        param2: 1,
        param3: true,
      ));
      
      if (result.isSuccess) {
        state = [ProviderName]State.loaded(data: result.data!);
      } else {
        state = [ProviderName]State.error(message: result.error.toString());
      }
    } catch (e) {
      state = [ProviderName]State.error(message: e.toString());
    }
  }
}

class [ProviderName]State {
  final [ProviderName]Status status;
  final [DataType]? data;
  final String? errorMessage;
  
  const [ProviderName]State({
    required this.status,
    this.data,
    this.errorMessage,
  });
  
  const [ProviderName]State.initial() : this(status: [ProviderName]Status.initial);
  
  const [ProviderName]State.loading() : this(status: [ProviderName]Status.loading);
  
  const [ProviderName]State.loaded({required [DataType] data}) : this(
    status: [ProviderName]Status.loaded,
    data: data,
  );
  
  const [ProviderName]State.error({required String message}) : this(
    status: [ProviderName]Status.error,
    errorMessage: message,
  );
  
  bool get isLoading => status == [ProviderName]Status.loading;
  bool get isLoaded => status == [ProviderName]Status.loaded;
  bool get isError => status == [ProviderName]Status.error;
}

enum [ProviderName]Status {
  initial,
  loading,
  loaded,
  error,
}
```

## 📋 **Implementation Checklist | قائمة مراجعة التنفيذ**

### **1. قوالب المعمارية | Architecture Templates**
- [ ] إنشاء قوالب الكيانات
- [ ] إنشاء قوالب المستودعات
- [ ] إنشاء قوالب حالات الاستخدام
- [ ] اختبار قوالب المعمارية

### **2. قوالب واجهة المستخدم | UI Templates**
- [ ] إنشاء قوالب الشاشات
- [ ] إنشاء قوالب الويدجت
- [ ] إنشاء قوالب النماذج
- [ ] اختبار قوالب واجهة المستخدم

### **3. قوالب إدارة الحالة | State Management Templates**
- [ ] إنشاء قوالب BLoC
- [ ] إنشاء قوالب Provider
- [ ] إنشاء قوالب الحالة
- [ ] اختبار قوالب إدارة الحالة

### **4. توثيق القوالب | Template Documentation**
- [ ] توثيق استخدام القوالب
- [ ] إضافة أمثلة القوالب
- [ ] إنشاء إرشادات القوالب
- [ ] اختبار توثيق القوالب

### **5. صيانة القوالب | Template Maintenance**
- [ ] إعداد تحكم إصدار القوالب
- [ ] إنشاء عملية تحديث القوالب
- [ ] إضافة التحقق من القوالب
- [ ] اختبار صيانة القوالب

---

**Next Tab**: Troubleshooting | استكشاف الأخطاء
