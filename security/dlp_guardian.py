"""
DLP Guardian
Data Loss Prevention for AI workloads
"""

from typing import Dict, List
import re


class DLPGuardian:
    """
    Data Loss Prevention Guardian
    
    Detects and prevents sensitive data leakage
    """
    
    # Saudi-specific PII patterns
    IQAMA_PATTERN = r'\b[12]\d{9}\b'
    NATIONAL_ID_PATTERN = r'\b[1-2]\d{9}\b'
    
    def __init__(self):
        self.scan_count = 0
    
    def scan(self, text: str) -> Dict:
        """Scan text for sensitive data"""
        
        self.scan_count += 1
        findings = []
        
        # Check for Iqama
        if re.search(self.IQAMA_PATTERN, text):
            findings.append("Iqama number detected")
        
        # Check for National ID
        if re.search(self.NATIONAL_ID_PATTERN, text):
            findings.append("National ID detected")
        
        return {
            "has_pii": len(findings) > 0,
            "findings": findings,
            "safe_to_process": len(findings) == 0
        }
    
    def mask(self, text: str) -> str:
        """Mask sensitive data"""
        
        # Mask Iqama
        text = re.sub(self.IQAMA_PATTERN, "***IQAMA***", text)
        
        # Mask National ID
        text = re.sub(self.NATIONAL_ID_PATTERN, "***ID***", text)
        
        return text
