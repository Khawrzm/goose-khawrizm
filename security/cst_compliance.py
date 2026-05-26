"""
CST Class C Compliance Validator
Saudi Arabia Communications, Space & Technology Commission compliance
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ComplianceReport:
    compliant: bool
    violations: List[str]
    warnings: List[str]
    score: float


class CSTValidator:
    """
    Saudi CST Class C Compliance Validator
    
    Validates adherence to KSA data sovereignty requirements
    """
    
    SAUDI_DATA_REGIONS = ["riyadh", "jeddah", "ksa-central"]
    
    def __init__(self):
        self.checks_performed = 0
    
    def validate_deployment(self, config: Dict) -> ComplianceReport:
        """Validate deployment configuration"""
        
        self.checks_performed += 1
        violations = []
        warnings = []
        
        # Check data residency
        if config.get("data_region") not in self.SAUDI_DATA_REGIONS:
            violations.append("Data must reside in KSA regions")
        
        # Check encryption
        if not config.get("encryption_at_rest"):
            violations.append("Encryption at rest required")
        
        # Check sovereignty
        if config.get("cross_border_transfer"):
            violations.append("Cross-border data transfer not allowed")
        
        compliant = len(violations) == 0
        score = 1.0 - (len(violations) * 0.2 + len(warnings) * 0.1)
        
        return ComplianceReport(
            compliant=compliant,
            violations=violations,
            warnings=warnings,
            score=max(score, 0.0)
        )
