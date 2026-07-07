"""
测试 _lib/config.py 路径配置
- 未设环境变量 → 清晰错误
- 路径不存在 → 清晰错误
- 路径存在 → 返回
"""
import os
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "chain-stockmap" / "scripts"))
from _lib.config import get_db_path


class TestGetDbPath:
    def test_no_env_raises_clear_error(self, monkeypatch, capsys):
        """未设 TUSHARE_DB_PATH → FileNotFoundError + stderr 提示"""
        monkeypatch.delenv("TUSHARE_DB_PATH", raising=False)
        with pytest.raises(FileNotFoundError) as exc_info:
            get_db_path()
        assert "TUSHARE_DB_PATH" in str(exc_info.value)

        # stderr 应有可执行提示
        captured = capsys.readouterr()
        assert "export TUSHARE_DB_PATH" in captured.err or "setx" in captured.err

    def test_nonexistent_path_raises(self, monkeypatch, capsys):
        """路径不存在 → FileNotFoundError"""
        monkeypatch.setenv("TUSHARE_DB_PATH", "/tmp/nonexistent_db_xyz.db")
        with pytest.raises(FileNotFoundError) as exc_info:
            get_db_path()
        assert "不存在" in str(exc_info.value)

    def test_existing_path_returns(self, monkeypatch, tmp_path):
        """路径存在 → 返回字符串"""
        db = tmp_path / "test.db"
        db.write_text("test")
        monkeypatch.setenv("TUSHARE_DB_PATH", str(db))
        result = get_db_path()
        assert result == str(db)
