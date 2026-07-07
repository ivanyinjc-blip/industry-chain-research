"""
测试 fetch_quote() 完整数据流
- 用 monkeypatch 替换 http_get,返回模拟东财数据
- 验证修复后茅台 PE 不再是 -14.43
"""
import json
import pytest
from fetch_a_stock import fetch_quote


class TestFetchQuote:
    def test_maotai_quote_pe_fixed(self, sample_a_stock_quote, monkeypatch):
        """v4.1.1 修复验证:茅台 PE 应为 25.6(不再是 -14.43)"""
        def fake_http_get(url, timeout=15, retries=3, encoding="utf-8"):
            return json.dumps({"data": sample_a_stock_quote})
        monkeypatch.setattr("fetch_a_stock.http_get", fake_http_get)

        result = fetch_quote("600519")
        assert result["status"] == "ok"
        d = result["data"]

        # v4.1.1 关键断言
        assert 20 < d["pe_dynamic"] < 30, f"茅台 PE 应在 20-30,实际 {d['pe_dynamic']}"
        assert 5 < d["pb"] < 15, f"茅台 PB 应在 5-15,实际 {d['pb']}"
        assert d["_pe_quality"] == "ok"

    def test_loss_stock_suspect_flag(self, sample_loss_stock_quote, monkeypatch):
        """亏损股 → _pe_quality 应该是 suspect 或 warning"""
        def fake_http_get(url, timeout=15, retries=3, encoding="utf-8"):
            return json.dumps({"data": sample_loss_stock_quote})
        monkeypatch.setattr("fetch_a_stock.http_get", fake_http_get)

        result = fetch_quote("000001")
        assert result["status"] == "ok"
        assert result["data"]["_pe_quality"] in ("suspect", "warning")

    def test_output_has_meta_block(self, sample_a_stock_quote, monkeypatch):
        """输出包含 _meta 字段元数据块"""
        def fake_http_get(url, timeout=15, retries=3, encoding="utf-8"):
            return json.dumps({"data": sample_a_stock_quote})
        monkeypatch.setattr("fetch_a_stock.http_get", fake_http_get)

        result = fetch_quote("600519")
        assert "_meta" in result
        assert result["_meta"]["field_meta_version"] == "4.1.1"
        assert "f191" in result["_meta"]["field_meta"]

    def test_market_cap_in_yi(self, sample_a_stock_quote, monkeypatch):
        """市值正确换算成亿"""
        def fake_http_get(url, timeout=15, retries=3, encoding="utf-8"):
            return json.dumps({"data": sample_a_stock_quote})
        monkeypatch.setattr("fetch_a_stock.http_get", fake_http_get)

        result = fetch_quote("600519")
        # 茅台总市值 1.82 万亿 = 18200 亿
        assert 18000 < result["data"]["market_cap_yi"] < 18500

    def test_price_conversion_from_fen(self, sample_a_stock_quote, monkeypatch):
        """价格从分正确转换为元"""
        def fake_http_get(url, timeout=15, retries=3, encoding="utf-8"):
            return json.dumps({"data": sample_a_stock_quote})
        monkeypatch.setattr("fetch_a_stock.http_get", fake_http_get)

        result = fetch_quote("600519")
        # f43=14500 分 → 145.00 元
        assert result["data"]["price"] == 145.0
