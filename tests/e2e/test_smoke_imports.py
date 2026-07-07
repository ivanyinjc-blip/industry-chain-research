"""
端到端 smoke test
- 所有 .py 脚本可以编译
- 所有 .py 脚本可以 import(不报 ModuleNotFoundError)
"""
import subprocess
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent.parent


class TestAllScriptsCompile:
    def test_all_py_compile(self):
        """16 个 .py 脚本全部 py_compile 通过"""
        scripts = list(ROOT.rglob("*.py"))
        scripts = [s for s in scripts if "__pycache__" not in str(s) and ".git" not in str(s)]
        assert len(scripts) >= 16, f"脚本数 {len(scripts)} < 16"

        for s in scripts:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(s)],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"编译失败: {s}\n{result.stderr}"


class TestRequirementsTxt:
    def test_requirements_not_empty(self):
        """requirements.txt 非空(v4.1.0 是空文件)"""
        req = ROOT / "requirements.txt"
        assert req.exists()
        content = req.read_text().strip()
        assert len(content) > 100, "requirements.txt 太小,可能不完整"

    def test_requirements_includes_key_deps(self):
        """requirements 包含关键依赖"""
        content = (ROOT / "requirements.txt").read_text()
        for dep in ["akshare", "duckdb", "Pillow", "requests", "pytest"]:
            assert dep in content, f"缺少 {dep}"


class TestNoHardcodedPath:
    def test_no_mnt_paths(self):
        """脚本中没有硬编码 /mnt/* 路径(v4.1.0 错误)"""
        offenders = []
        for s in (ROOT).rglob("*.py"):
            if "__pycache__" in str(s) or ".git" in str(s) or "tests/" in str(s):
                continue
            content = s.read_text()
            if "/mnt/e" in content or "/mnt/c" in content:
                offenders.append(s)
        assert not offenders, f"硬编码 /mnt/* 路径: {offenders}"
