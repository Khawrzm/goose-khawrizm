"""
Zero Trust AI Validator
Implements Zero Trust principles for AI workloads
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    ALLOW = "allow"
    DENY = "deny"
    CHALLENGE = "challenge"


@dataclass
class ZeroTrustContext:
    user_id: str
    device_posture: str
    data_classification: str
    action_type: str
    risk_score: float


class ZeroTrustValidator:
    """
    Zero Trust AI Architecture Validator
    
    Core Principles:
    1. Never trust, always verify
    2. Assume breach
    3. Verify explicitly
    4. Use least privilege access
    5. Minimize blast radius
    """
    
    def __init__(self):
        self.validation_count = 0
    
    def validate_action(
        self,
        context: ZeroTrustContext,
        prompt: str
    ) -> Dict:
        """Validate if AI action should be allowed"""
        
        self.validation_count += 1
        
        # Calculate risk
        risk = self._calculate_risk(context, prompt)
        
        # Make decision
        decision = self._make_decision(risk, context)
        
        return {
            "decision": decision.value,
            "risk_score": risk,
            "requires_mfa": risk > 0.7,
            "allowed": decision == ValidationResult.ALLOW,
            "context": {
                "user": context.user_id,
                "device": context.device_posture,
                "classification": context.data_classification
            }
        }
    
    def _calculate_risk(
        self,
        context: ZeroTrustContext,
        prompt: str
    ) -> float:
        """Calculate risk score 0.0-1.0"""
        
        risk = 0.0
        
        # Data classification risk
        if context.data_classification == "confidential":
            risk += 0.3
        elif context.data_classification == "restricted":
            risk += 0.5
        
        # Action type risk
        if context.action_type in ["delete", "transfer", "external_share"]:
            risk += 0.3
        
        # Device posture
        if context.device_posture != "compliant":
            risk += 0.2
        
        # Base context risk
        risk += context.risk_score
        
        return min(risk, 1.0)
    
    def _make_decision(
        self,
        risk: float,
        context: ZeroTrustContext
    ) -> ValidationResult:
        """Make allow/deny decision"""
        
        if risk >= 0.8:
            return ValidationResult.DENY
        elif risk >= 0.5:
            return ValidationResult.CHALLENGE
        else:
            return ValidationResult.ALLOW


# Convenience function
def validate_zero_trust(
    user_id: str,
    prompt: str,
    data_class: str = "internal",
    action: str = "read"
) -> Dict:
    """Quick zero trust validation"""
    
    validator = ZeroTrustValidator()
    context = ZeroTrustContext(
        user_id=user_id,
        device_posture="compliant",
        data_classification=data_class,
        action_type=action,
        risk_score=0.0
    )
    
    return validator.validate_action(context, prompt)
