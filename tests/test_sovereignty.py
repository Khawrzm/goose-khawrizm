"""
Sovereignty Tests - Zero Big Tech Verification
The MOST IMPORTANT tests in this entire project!
"""

import pytest
from src.tools import verify_sovereignty
import tempfile
from pathlib import Path


def test_clean_code_is_sovereign():
    """Test that clean code passes sovereignty check"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a clean Python file
        clean_file = Path(tmpdir) / "clean.py"
        clean_file.write_text("""
import numpy as np

def process_local(data):
    return np.mean(data)
""")
        
        result = verify_sovereignty(tmpdir)
        
        assert result["sovereign"] is True
        assert result["violations_count"] == 0
        assert result["big_tech_free"] is True
        assert "✅ SOVEREIGN" in result["status"]


def test_detects_openai_violation():
    """Test that OpenAI usage is detected"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create file with OpenAI
        dirty_file = Path(tmpdir) / "dirty.py"
        dirty_file.write_text("""
import openai

client = openai.ChatCompletion.create()
""")
        
        result = verify_sovereignty(tmpdir)
        
        assert result["sovereign"] is False
        assert result["violations_count"] > 0
        assert result["big_tech_free"] is False
        assert "❌" in result["status"]


def test_detects_anthropic_violation():
    """Test that Anthropic usage is detected"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dirty_file = Path(tmpdir) / "dirty.py"
        dirty_file.write_text("""
from anthropic import Anthropic

client = Anthropic()
""")
        
        result = verify_sovereignty(tmpdir)
        
        assert result["sovereign"] is False
        assert result["violations_count"] > 0


def test_detects_telemetry():
    """Test that telemetry functions are detected"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dirty_file = Path(tmpdir) / "dirty.py"
        dirty_file.write_text("""
def track_user(user_id):
    send_telemetry(user_id)
""")
        
        result = verify_sovereignty(tmpdir)
        
        assert result["sovereign"] is False
        assert result["violations_count"] >= 2  # track_user + send_telemetry


def test_detects_cloud_upload():
    """Test that cloud upload functions are detected"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dirty_file = Path(tmpdir) / "dirty.py"
        dirty_file.write_text("""
def backup_data():
    upload_to_cloud(data)
""")
        
        result = verify_sovereignty(tmpdir)
        
        assert result["sovereign"] is False
        assert any("upload_to_cloud" in v["pattern"] for v in result["violations"])


def test_ignores_git_directory():
    """Test that .git directory is ignored"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .git directory with "violations"
        git_dir = Path(tmpdir) / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("openai.api_key = xxx")
        
        # Create clean main file
        (Path(tmpdir) / "main.py").write_text("print('hello')")
        
        result = verify_sovereignty(tmpdir)
        
        # Should be sovereign (ignoring .git)
        assert result["sovereign"] is True


def test_self_sovereignty():
    """
    The ultimate test: verify THIS extension is sovereign!
    """
    import os
    extension_root = os.path.dirname(os.path.dirname(__file__))
    
    result = verify_sovereignty(extension_root)
    
    # THIS MUST PASS!
    assert result["sovereign"] is True, (
        f"⚠️ SOVEREIGNTY VIOLATION IN OUR OWN CODE!\n"
        f"Violations: {result['violations']}\n"
        f"We became what we swore to destroy!"
    )
    
    assert result["big_tech_free"] is True
    assert result["violations_count"] == 0
    
    print("\n✅ SELF-SOVEREIGNTY VERIFIED")
    print(f"Files scanned: {result['files_scanned']}")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
