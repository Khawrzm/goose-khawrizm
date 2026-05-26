"""
Goose Tools for KHAWRIZM Extension
Implements the three core sovereign capabilities
"""

import os
import re
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path


def process_arabic_intent(text: str) -> Dict[str, Any]:
    """
    استخراج النوايا من النص العربي محلياً
    
    Uses SARC (Semantic Arabic Root Compiler) to extract trilateral roots
    and map them to logical predicates.
    
    Args:
        text: النص العربي المراد معالجته
        
    Returns:
        Dict containing:
        - roots: الجذور الثلاثية المستخرجة
        - predicates: المحمولات المنطقية
        - entities: الكيانات المستخرجة
        - confidence: مستوى الثقة
    """
    
    # Simple trilateral root extraction (مبسط للـ MVP)
    # في النسخة الكاملة، هذا سيستدعي Niyah Engine
    
    # قاعدة بيانات جذور مبسطة
    ROOTS_DB = {
        "بني": {"root": "ب-ن-ي", "predicate": "BUILD", "confidence": 0.95},
        "بناء": {"root": "ب-ن-ي", "predicate": "BUILD", "confidence": 0.95},
        "يبني": {"root": "ب-ن-ي", "predicate": "BUILD", "confidence": 0.95},
        "كتب": {"root": "ك-ت-ب", "predicate": "WRITE", "confidence": 0.95},
        "كاتب": {"root": "ك-ت-ب", "predicate": "WRITE", "confidence": 0.92},
        "ذكي": {"root": "ذ-ك-ي", "predicate": "INTELLIGENT", "confidence": 0.94},
        "شعر": {"root": "ش-ع-ر", "predicate": "SENSE", "confidence": 0.93},
        "استشعار": {"root": "ش-ع-ر", "predicate": "SENSE", "confidence": 0.91},
        "حرك": {"root": "ح-ر-ك", "predicate": "MOVE", "confidence": 0.94},
        "منزل": {"root": "ن-ز-ل", "entity": "home", "confidence": 0.96},
        "نظام": {"root": "ن-ظ-م", "entity": "system", "confidence": 0.95},
    }
    
    # Extract words from Arabic text
    words = re.findall(r'[\u0600-\u06FF]+', text)
    
    roots = []
    predicates = []
    entities = []
    confidences = []
    
    for word in words:
        if word in ROOTS_DB:
            entry = ROOTS_DB[word]
            roots.append(entry["root"])
            if "predicate" in entry:
                predicates.append(entry["predicate"])
            if "entity" in entry:
                entities.append(entry["entity"])
            confidences.append(entry["confidence"])
    
    # Calculate average confidence
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    return {
        "text": text,
        "roots": list(set(roots)),
        "predicates": list(set(predicates)),
        "entities": list(set(entities)),
        "confidence": round(avg_confidence, 2),
        "word_count": len(words),
        "processed_locally": True,
        "big_tech_api_calls": 0,  # ✅ ZERO!
    }


def sense_environment(mode: str = "sim") -> Dict[str, Any]:
    """
    استشعار البيئة المحيطة باستخدام EchoWall
    
    Args:
        mode: 'live' للاستشعار الحقيقي، 'sim' للمحاكاة
        
    Returns:
        Dict containing:
        - presence: وجود أشخاص
        - occupancy_count: عدد الأشخاص
        - posture: الوضعية (standing, sitting, lying)
        - confidence: مستوى الثقة
        - timestamp: وقت القراءة
    """
    
    import time
    import random
    
    if mode == "sim":
        # محاكاة بسيطة - في النسخة الكاملة تتصل بـ EchoWall API
        return {
            "mode": "simulation",
            "presence": True,
            "occupancy_count": random.randint(1, 3),
            "posture": random.choice(["standing", "sitting", "lying"]),
            "breathing_rate": round(random.uniform(12.0, 20.0), 1),
            "confidence": round(random.uniform(0.75, 0.95), 2),
            "timestamp": int(time.time()),
            "hardware": "ESP32-S3 (simulated)",
            "privacy": {
                "raw_data_stored": False,
                "cloud_upload": False,
                "local_only": True,
                "jitter_applied": True
            }
        }
    
    elif mode == "live":
        # في النسخة الكاملة، هذا يتصل بـ EchoWall عبر serial/MQTT
        return {
            "error": "Live mode requires EchoWall hardware",
            "hint": "Connect ESP32-S3 or use mode='sim' for testing",
            "hardware_detected": False
        }
    
    else:
        return {"error": f"Unknown mode: {mode}. Use 'sim' or 'live'"}


def verify_sovereignty(path: str = ".") -> Dict[str, Any]:
    """
    التحقق من عدم وجود اعتماديات على Big Tech
    
    Scans the codebase for:
    - External API calls (OpenAI, Anthropic, Google, AWS, etc.)
    - Telemetry functions
    - Cloud upload functions
    
    Args:
        path: المسار المراد فحصه
        
    Returns:
        Dict containing:
        - sovereign: هل الكود سيادي؟
        - violations: قائمة الانتهاكات
        - files_scanned: عدد الملفات المفحوصة
    """
    
    # Big Tech patterns to detect
    BIG_TECH_PATTERNS = [
        r'openai\.',
        r'anthropic\.',
        r'google\.generativeai',
        r'cohere\.',
        r'aws\.',
        r'azure\.',
        r'requests\.post.*api\.openai',
        r'requests\.post.*api\.anthropic',
        r'httpx\.post.*api\.openai',
        r'upload_to_cloud',
        r'send_telemetry',
        r'track_user',
        r'analytics\.send',
    ]
    
    violations = []
    files_scanned = 0
    
    # Scan Python files
    path_obj = Path(path)
    for py_file in path_obj.rglob("*.py"):
        if ".git" in str(py_file) or "venv" in str(py_file):
            continue
            
        files_scanned += 1
        
        try:
            content = py_file.read_text(encoding='utf-8')
            
            for pattern in BIG_TECH_PATTERNS:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    violations.append({
                        "file": str(py_file),
                        "line": line_num,
                        "pattern": pattern,
                        "matched": match.group()
                    })
        except Exception as e:
            # Skip files that can't be read
            pass
    
    is_sovereign = len(violations) == 0
    
    return {
        "sovereign": is_sovereign,
        "status": "✅ SOVEREIGN" if is_sovereign else "❌ BIG TECH DETECTED",
        "violations": violations,
        "violations_count": len(violations),
        "files_scanned": files_scanned,
        "big_tech_free": is_sovereign,
        "message": (
            "كل شيء نظيف! لا توجد استدعاءات Big Tech" 
            if is_sovereign 
            else f"تم اكتشاف {len(violations)} انتهاك(ات) للسيادة"
        )
    }


# Export functions for Goose
__all__ = [
    "process_arabic_intent",
    "sense_environment",
    "verify_sovereignty",
]
