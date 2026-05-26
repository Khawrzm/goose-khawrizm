"""
Tests for Arabic intent processing
"""

import pytest
from src.tools import process_arabic_intent


def test_simple_build_intent():
    """Test extracting BUILD intent from Arabic"""
    result = process_arabic_intent("أريد بناء نظام")
    
    assert "ب-ن-ي" in result["roots"]
    assert "BUILD" in result["predicates"]
    assert result["big_tech_api_calls"] == 0
    assert result["processed_locally"] is True


def test_sense_intent():
    """Test extracting SENSE intent"""
    result = process_arabic_intent("استشعار الحركة")
    
    assert "ش-ع-ر" in result["roots"]
    assert "SENSE" in result["predicates"]


def test_combined_intent():
    """Test complex intent with multiple roots"""
    result = process_arabic_intent("بناء نظام استشعار ذكي للمنزل")
    
    # Should extract multiple roots
    assert len(result["roots"]) >= 2
    assert "ب-ن-ي" in result["roots"]  # BUILD
    assert "ش-ع-ر" in result["roots"]  # SENSE
    
    # Should identify entities
    assert "system" in result["entities"] or "home" in result["entities"]
    
    # Zero Big Tech
    assert result["big_tech_api_calls"] == 0


def test_confidence_score():
    """Test confidence scoring"""
    result = process_arabic_intent("بناء نظام")
    
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["confidence"] > 0.9  # Should be high for known words


def test_empty_text():
    """Test handling empty input"""
    result = process_arabic_intent("")
    
    assert result["roots"] == []
    assert result["predicates"] == []
    assert result["confidence"] == 0.0


def test_unknown_words():
    """Test handling unknown Arabic words"""
    result = process_arabic_intent("كلمات غير معروفة تماماً")
    
    # Should handle gracefully without crashing
    assert "roots" in result
    assert "processed_locally" in result
    assert result["big_tech_api_calls"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
