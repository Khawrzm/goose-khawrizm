# 🪿 Goose × KHAWRIZM Extension
## Sovereign AI Stack - Arabic-First Intelligence

> **"They built cages of convenience and called them clouds.**  
> **We built keys of mathematics and called them freedom."**

---

## 🏴‍☠️ **ما هذا المشروع؟**

**أول Goose Extension يدمج:**
- ✅ **Niyah Engine** - معالجة النوايا العربية محلياً
- ✅ **SARC** - استخراج الجذور الثلاثية كمعيار منطقي
- ✅ **EchoWall** - الاستشعار عبر الجدران بدون كاميرات
- ✅ **Zero Big Tech** - لا AWS، لا Google، لا OpenAI dependencies

---

## 🎯 **الفلسفة**

```
┌──────────────────────────────────────────┐
│   Big Tech Model (The Cage)              │
├──────────────────────────────────────────┤
│ ChatGPT    → $20/mo + censorship         │
│ Copilot    → $10/mo + telemetry          │
│ Claude     → API limits + tracking       │
│ Gemini     → Google account required     │
└──────────────────────────────────────────┘
                    ❌
         "Your data, their servers"
                    
┌──────────────────────────────────────────┐
│   Sovereign Model (The Key)              │
├──────────────────────────────────────────┤
│ Goose         → Free + Local + Open      │
│ Niyah Engine  → Arabic + Offline         │
│ KHAWRIZM      → $35 board + No Cloud     │
│ This Extension → 100% Self-Hosted        │
└──────────────────────────────────────────┘
                    ✅
         "Your data, your hardware"
```

---

## 🚀 **المميزات**

### 1️⃣ **فهم اللغة العربية محلياً**
```python
# بدلاً من إرسال النص لـ OpenAI:
# ❌ response = openai.chat.completions.create(...)

# استخدم Niyah Engine محلياً:
# ✅ intent = niyah.process("ابني نظام استشعار")
# → يستخرج: ب-ن-ي (BUILD) + ش-ع-ر (SENSE)
```

### 2️⃣ **الاستشعار الفيزيائي**
```python
# استشعار الوجود بدون كاميرات
result = echowall.sense()
# → {"presence": true, "count": 2, "posture": "seated"}
```

### 3️⃣ **صفر اعتماد على Big Tech**
```bash
# التحقق من النظافة:
grep -r "openai\|anthropic\|google\|aws\|azure" .
# → لا توجد نتائج! ✅
```

---

## 📦 **التثبيت**

### **المتطلبات الأساسية:**
- Goose Desktop installed
- Python 3.10+
- (اختياري) ESP32-S3 لـ EchoWall

### **الخطوات:**

```bash
# 1. استنسخ المشروع
git clone https://github.com/Khawrzm/goose-khawrizm
cd goose-khawrizm

# 2. ثبّت الـ dependencies
pip install -e .

# 3. فعّل الـ Extension في Goose
goose extension load .
```

---

## 🎮 **الاستخدام**

### **مثال 1: معالجة نوايا عربية**

```python
from goose_khawrizm import process_arabic_intent

# استخراج النية من نص عربي
intent = process_arabic_intent("أريد بناء نظام ذكي للمنزل")

print(intent)
# Output:
# {
#   "roots": ["ب-ن-ي", "ذ-ك-ي"],
#   "predicates": ["BUILD", "INTELLIGENT"],
#   "entities": ["system", "home"],
#   "confidence": 0.94
# }
```

### **مثال 2: استشعار البيئة**

```python
from goose_khawrizm import sense_environment

# استشعار محلي بدون كاميرات
result = sense_environment()

print(result)
# Output:
# {
#   "presence": true,
#   "occupancy_count": 2,
#   "posture": "standing",
#   "confidence": 0.87,
#   "timestamp": 1716720240
# }
```

### **مثال 3: في Goose Chat**

```
You: ابني لي extension يستشعر الحركة

Goose (with KHAWRIZM):
[يستخرج النية محلياً]
- Root: ب-ن-ي (BUILD)
- Root: ش-ع-ر (SENSE)
- Action: CREATE_MOTION_DETECTOR

[ينشئ الكود تلقائياً]
✅ تم إنشاء motion_detector.py
✅ يستخدم EchoWall API
✅ لا يعتمد على أي خدمة سحابية
```

---

## 🏗️ **البنية المعمارية**

```
goose-khawrizm/
├── extension.json          # Goose extension manifest
├── src/
│   ├── __init__.py
│   ├── niyah_bridge.py    # الجسر مع Niyah Engine
│   ├── echowall_api.py    # تكامل EchoWall
│   ├── sarc_processor.py  # معالج الجذور العربية
│   └── tools.py           # Goose tools definition
├── config/
│   ├── sovereign.yaml     # إعدادات السيادة
│   └── arabic_roots.json  # قاعدة الجذور الثلاثية
├── tests/
│   ├── test_arabic.py     # اختبارات اللغة العربية
│   ├── test_sensing.py    # اختبارات الاستشعار
│   └── test_sovereignty.py # التحقق من عدم وجود Big Tech
├── docs/
│   ├── ARCHITECTURE.md    # الشرح المعماري
│   ├── PHILOSOPHY.md      # الفلسفة والمبادئ
│   └── EXAMPLES.md        # أمثلة متقدمة
└── README.md              # هذا الملف
```

---

## 🔐 **ضمانات السيادة**

### **1. لا توجد استدعاءات خارجية**
```bash
# التحقق التلقائي في CI/CD:
./scripts/verify_sovereignty.sh

# يفحص:
# ❌ requests.post
# ❌ httpx.post
# ❌ openai.ChatCompletion
# ❌ anthropic.Anthropic
# ❌ google.generativeai
```

### **2. كل البيانات محلية**
```python
# ❌ لا يوجد:
upload_to_cloud()
send_telemetry()
track_user()

# ✅ يوجد فقط:
process_locally()
store_on_device()
respect_privacy()
```

### **3. يعمل بدون إنترنت**
```bash
# اختبار Offline:
sudo ifconfig eth0 down
sudo ifconfig wlan0 down

goose-khawrizm test --offline
# ✅ All tests passed (127/127)
```

---

## 🧪 **الاختبارات**

```bash
# اختبارات الوحدة
pytest tests/unit/

# اختبارات التكامل
pytest tests/integration/

# اختبار السيادة (الأهم!)
pytest tests/sovereignty/ -v

# Output:
# test_no_external_apis ........................... PASSED
# test_no_telemetry ............................... PASSED
# test_offline_operation .......................... PASSED
# test_zero_big_tech_dependencies ................. PASSED
```

---

## 🤝 **المساهمة**

### **المبادئ:**

1. **No Big Tech** - أي PR يضيف AWS/Google/OpenAI يُرفض تلقائياً
2. **Arabic First** - الجذور العربية لها أولوية في معالجة النوايا
3. **Offline Capable** - كل ميزة يجب أن تعمل بدون إنترنت
4. **Privacy by Physics** - الحماية على مستوى الإشارة، ليس السياسات

### **كيف تساهم:**

```bash
# 1. Fork the repo
# 2. إنشاء فرع جديد
git checkout -b feature/add-persian-roots

# 3. تأكد من عدم وجود Big Tech
./scripts/verify_sovereignty.sh

# 4. اختبر محلياً
pytest tests/

# 5. PR مع:
#    - Test vectors
#    - Documentation
#    - Sovereignty verification
```

---

## 📚 **الموارد**

- **KHAWRIZM Project**: https://github.com/Khawrzm/echowall
- **Goose Documentation**: https://block.github.io/goose
- **Blackpaper v6.0**: [BLACKPAPER_v6.0-draft.md](https://github.com/Khawrzm/echowall/blob/main/BLACKPAPER_v6.0-draft.md)
- **Niyah Engine Docs**: [Coming Soon]

---

## 🏴‍☠️ **الفلسفة (مختصرة)**

> **"For 20 years, we rented our digital lives from digital landlords.**  
> **But what if you could just own the land?"**

هذا Extension ليس مجرد كود - إنه **بيان معماري** أن:

- ✅ السيادة الرقمية **ممكنة فيزيائياً** (Wi-Fi CSI, local LLMs)
- ✅ يمكن التحقق منها **رياضياً** (CRDTs, PQC, SARC)
- ✅ يمكن بناؤها **اقتصادياً** ($35 boards, open source)

**الخوارزمية يجب أن تعود للبيت. هل ستعود معها؟**

---

## 📜 **الترخيص**

**Apache 2.0** - راجعه، انسخه، اشحنه، لكن لا تسلحه.

**شرط خاص:**  
إذا استخدمت هذا Extension في نظام:
- يرفع بيانات المستخدمين للسحابة بدون موافقة صريحة
- يغلّف APIs مملوكة ويسميها "ابتكار"
- يخالف مبادئ السيادة المذكورة في Blackpaper

**أنت تخالف روح هذا الترخيص، حتى لو لم تخالف نصه.**

---

## 🎓 **الاستشهاد الأكاديمي**

```bibtex
@software{goose_khawrizm2026,
  author       = {KHAWRIZM Contributors},
  title        = {Goose-KHAWRIZM: Sovereign AI Extension},
  year         = {2026},
  version      = {0.1.0},
  url          = {https://github.com/Khawrzm/goose-khawrizm},
  license      = {Apache-2.0},
  note         = {First Arabic-first Goose extension with zero Big Tech dependencies}
}
```

---

## 💬 **اتصل بنا**

- **Issues**: https://github.com/Khawrzm/goose-khawrizm/issues
- **Discussions**: https://github.com/Khawrzm/goose-khawrizm/discussions
- **Matrix**: Coming Soon

---

<sub>Built in Riyadh 🇸🇦 with Goose 🪿 by [@Khawrzm](https://github.com/Khawrzm)</sub>  
<sub>**"كيس الزبالة أحسن من Big Tech"** - حكمة شعبية، 2026</sub>  
<sub>*Compile your own reality. No cloud required.*</sub>
