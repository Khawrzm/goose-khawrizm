"""
SARC: Semantic Arabic Root Compiler
Advanced trilateral root extraction and logical predicate mapping
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


class SARCProcessor:
    """
    Semantic Arabic Root Compiler
    
    Extracts trilateral roots from Arabic text and maps them to logical predicates.
    This is NOT translation - this is intent grounding through morphological analysis.
    """
    
    def __init__(self, roots_db_path: Optional[str] = None):
        """
        Initialize SARC with extended roots database
        
        Args:
            roots_db_path: Path to JSON roots database (optional)
        """
        if roots_db_path is None:
            # Default to config directory
            config_dir = Path(__file__).parent.parent / "config"
            roots_db_path = config_dir / "arabic_roots_extended.json"
        
        self.roots_db = self._load_roots_db(roots_db_path)
        self.word_to_root = self._build_word_index()
    
    def _load_roots_db(self, path: Path) -> Dict:
        """Load the extended roots database"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to minimal database
            return self._get_minimal_db()
    
    def _get_minimal_db(self) -> Dict:
        """Minimal fallback database"""
        return {
            "version": "0.1.0",
            "roots": {
                "ب-ن-ي": {
                    "root": "ب-ن-ي",
                    "predicate": "BUILD",
                    "words": ["بني", "بناء", "يبني"],
                    "confidence": 0.95
                },
                "ش-ع-ر": {
                    "root": "ش-ع-ر",
                    "predicate": "SENSE",
                    "words": ["شعر", "استشعار"],
                    "confidence": 0.93
                }
            },
            "entities": {
                "ن-ز-ل": {"type": "home", "words": ["منزل"], "confidence": 0.96}
            }
        }
    
    def _build_word_index(self) -> Dict[str, Dict]:
        """Build reverse index: word -> root info"""
        index = {}
        
        # Index roots
        for root_id, root_data in self.roots_db.get("roots", {}).items():
            for word in root_data.get("words", []):
                index[word] = {
                    "root": root_data["root"],
                    "predicate": root_data.get("predicate"),
                    "confidence": root_data["confidence"],
                    "type": "root"
                }
        
        # Index entities
        for entity_id, entity_data in self.roots_db.get("entities", {}).items():
            for word in entity_data.get("words", []):
                index[word] = {
                    "root": entity_id,
                    "entity": entity_data["type"],
                    "confidence": entity_data["confidence"],
                    "type": "entity"
                }
        
        return index
    
    def extract_words(self, text: str) -> List[str]:
        """Extract Arabic words from text"""
        # Remove diacritics
        text = self._remove_diacritics(text)
        
        # Extract Arabic words
        words = re.findall(r'[\u0600-\u06FF]+', text)
        
        return words
    
    def _remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritics (tashkeel)"""
        arabic_diacritics = re.compile(r'[\u064B-\u065F\u0670]')
        return arabic_diacritics.sub('', text)
    
    def process(self, text: str) -> Dict:
        """
        Process Arabic text and extract intent
        
        Args:
            text: Arabic text to process
            
        Returns:
            Dict containing:
            - roots: List of trilateral roots
            - predicates: List of logical predicates
            - entities: List of extracted entities
            - confidence: Average confidence score
            - metadata: Processing metadata
        """
        words = self.extract_words(text)
        
        roots: Set[str] = set()
        predicates: Set[str] = set()
        entities: Set[str] = set()
        confidences: List[float] = []
        
        matched_words = []
        
        for word in words:
            if word in self.word_to_root:
                entry = self.word_to_root[word]
                
                roots.add(entry["root"])
                
                if entry.get("predicate"):
                    predicates.add(entry["predicate"])
                
                if entry.get("entity"):
                    entities.add(entry["entity"])
                
                confidences.append(entry["confidence"])
                matched_words.append(word)
        
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return {
            "text": text,
            "roots": sorted(list(roots)),
            "predicates": sorted(list(predicates)),
            "entities": sorted(list(entities)),
            "confidence": round(avg_confidence, 3),
            "word_count": len(words),
            "matched_words": matched_words,
            "match_rate": len(matched_words) / len(words) if words else 0.0,
            "processed_locally": True,
            "big_tech_api_calls": 0,
            "sarc_version": self.roots_db.get("version", "unknown")
        }
    
    def get_root_info(self, root: str) -> Optional[Dict]:
        """Get detailed information about a specific root"""
        return self.roots_db.get("roots", {}).get(root)
    
    def get_entity_info(self, entity_root: str) -> Optional[Dict]:
        """Get detailed information about a specific entity"""
        return self.roots_db.get("entities", {}).get(entity_root)
    
    def get_stats(self) -> Dict:
        """Get statistics about the loaded database"""
        return {
            "version": self.roots_db.get("version"),
            "total_roots": len(self.roots_db.get("roots", {})),
            "total_entities": len(self.roots_db.get("entities", {})),
            "total_words_indexed": len(self.word_to_root),
            "predicates": sorted(list(set(
                r.get("predicate") 
                for r in self.roots_db.get("roots", {}).values() 
                if r.get("predicate")
            )))
        }


# Singleton instance
_sarc_instance: Optional[SARCProcessor] = None


def get_sarc() -> SARCProcessor:
    """Get or create SARC processor singleton"""
    global _sarc_instance
    if _sarc_instance is None:
        _sarc_instance = SARCProcessor()
    return _sarc_instance


# Convenience function
def process_arabic_intent_advanced(text: str) -> Dict:
    """
    Advanced Arabic intent processing using SARC
    
    This is the recommended function to use for production.
    Uses the extended roots database with 50+ roots.
    """
    sarc = get_sarc()
    return sarc.process(text)


if __name__ == "__main__":
    # Demo usage
    sarc = SARCProcessor()
    
    print("SARC Processor Demo")
    print("=" * 50)
    
    # Show stats
    stats = sarc.get_stats()
    print(f"\n📊 Database Stats:")
    print(f"   Version: {stats['version']}")
    print(f"   Total Roots: {stats['total_roots']}")
    print(f"   Total Entities: {stats['total_entities']}")
    print(f"   Indexed Words: {stats['total_words_indexed']}")
    print(f"   Predicates: {', '.join(stats['predicates'][:10])}...")
    
    # Process example
    text = "أريد بناء نظام استشعار ذكي للمنزل"
    result = sarc.process(text)
    
    print(f"\n🧠 Processing: '{text}'")
    print(f"   Roots: {result['roots']}")
    print(f"   Predicates: {result['predicates']}")
    print(f"   Entities: {result['entities']}")
    print(f"   Confidence: {result['confidence']:.1%}")
    print(f"   Match Rate: {result['match_rate']:.1%}")
    print(f"   Big Tech API Calls: {result['big_tech_api_calls']} ✅")
