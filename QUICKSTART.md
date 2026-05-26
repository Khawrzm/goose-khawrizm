# 🚀 دليل البدء السريع

## التثبيت (دقيقة واحدة)

```bash
# 1. استنسخ المشروع
git clone https://github.com/Khawrzm/goose-khawrizm
cd goose-khawrizm

# 2. جرّب فوراً (بدون تثبيت)
python3 -c "
from src.tools import process_arabic_intent
result = process_arabic_intent('بناء نظام ذكي')
print(result)
"
```

## الاستخدام الأساسي

### 1️⃣ معالجة النوايا العربية

```python
from src.tools import process_arabic_intent

# مثال بسيط
result = process_arabic_intent("أريد بناء نظام استشعار للمنزل")

print(result)
# {
#   "roots": ["ب-ن-ي", "ش-ع-ر"],
#   "predicates": ["BUILD", "SENSE"],
#   "entities": ["system", "home"],
#   "confidence": 0.94,
#   "big_tech_api_calls": 0  ← الأهم!
# }
```

### 2️⃣ استشعار البيئة (محاكاة)

```python
from src.tools import sense_environment

# محاكاة الاستشعار
result = sense_environment(mode="sim")

print(result)
# {
#   "presence": true,
#   "occupancy_count": 2,
#   "posture": "sitting",
#   "confidence": 0.87,
#   "privacy": {
#     "cloud_upload": false,  ← لا رفع للسحابة!
#     "local_only": true
#   }
# }
```

### 3️⃣ التحقق من السيادة

```python
from src.tools import verify_sovereignty

# فحص أي مشروع
result = verify_sovereignty("/path/to/your/project")

print(result)
# {
#   "sovereign": true,
#   "status": "✅ SOVEREIGN",
#   "violations_count": 0,
#   "big_tech_free": true
# }
```

## الاختبار

```bash
# اختبار سريع
python3 -m pytest tests/ -v

# يجب أن ترى:
# ✅ test_arabic.py ......... PASSED
# ✅ test_sovereignty.py .... PASSED
# ✅ test_self_sovereignty .. PASSED  ← الأهم!
```

## التكامل مع Goose Desktop

```bash
# إذا كان Goose مثبتاً:
goose extension load .

# ثم في Goose:
# You: ابني لي نظام استشعار
# Goose: [يستخدم KHAWRIZM extension محلياً]
```

## أمثلة عملية

### مثال 1: استخراج نوايا متعددة

```python
text = """
أريد بناء نظام ذكي للمنزل
يستشعر الحركة ويكتب التقارير
"""

result = process_arabic_intent(text)
print(f"استُخرجت {len(result['roots'])} جذور")
print(f"الأفعال: {result['predicates']}")
# الأفعال: ['BUILD', 'SENSE', 'WRITE']
```

### مثال 2: التحقق من مشروع كامل

```bash
# فحص المشروع الخاص بك
python3 -c "
from src.tools import verify_sovereignty
result = verify_sovereignty('.')
print(result['message'])
"
# ✅ كل شيء نظيف! لا توجد استدعاءات Big Tech
```

## الأسئلة الشائعة

**Q: هل يعمل بدون إنترنت؟**  
A: نعم! 100% محلي.

**Q: هل يحتاج API keys؟**  
A: لا! صفر اعتماد على Big Tech.

**Q: هل يدعم لغات أخرى غير العربية؟**  
A: حالياً العربية فقط. لغات أخرى قريباً.

**Q: كيف أساهم؟**  
A: افتح PR! شرط واحد: No Big Tech!

---

**التالي:** اقرأ [README.md](README.md) للتفاصيل الكاملة
