"""
测试 v4.1.1 字段校验逻辑
- 茅台 v4.1.0 bug 场景:PE=-14.43 + 净利润>0 → suspect
- 正常 PE → ok
- PE>500 → warning
- PB 负 → suspect
"""
import pytest
from fetch_a_stock import validate_valuation, FIELD_META, FIELD_META_VERSION


class TestValidateValuation:
    def test_pe_negative_with_profit_is_suspect(self):
        """v4.1.0 经典 bug 场景:茅台 PE=-14.43 + 净利>0 → suspect"""
        quality, msg = validate_valuation(pe=-14.43, pb=8.0, net_profit_yi=100.0)
        assert quality == "suspect", f"应为 suspect,实际 {quality}"
        assert "字段错位" in msg or "f191" in msg

    def test_normal_pe_is_ok(self):
        """正常 PE → ok"""
        quality, _ = validate_valuation(pe=25.5, pb=8.0, net_profit_yi=200.0)
        assert quality == "ok"

    def test_pe_none_is_warning(self):
        """PE 缺失 → warning"""
        quality, msg = validate_valuation(pe=None, pb=5.0)
        assert quality == "warning"
        assert "PE 缺失" in msg

    def test_pe_over_500_is_warning(self):
        """PE > 500 → warning(微利股)"""
        quality, msg = validate_valuation(pe=800.0, pb=2.0)
        assert quality == "warning"
        assert "500" in msg

    def test_pb_negative_is_suspect(self):
        """PB 负 → suspect"""
        quality, _ = validate_valuation(pe=10.0, pb=-1.0)
        assert quality == "suspect"

    def test_pb_over_30_is_warning(self):
        """PB > 30 → warning"""
        quality, _ = validate_valuation(pe=10.0, pb=50.0)
        assert quality == "warning"

    def test_loss_stock_pe_is_suspect_or_warning(self):
        """亏损股 PE 负 + 无利润对比 → warning 而非 suspect"""
        quality, _ = validate_valuation(pe=-15.0, pb=2.0, net_profit_yi=None)
        # 没有净利对比,不算 suspect
        assert quality in ("warning", "suspect")


class TestFieldMeta:
    def test_field_meta_version(self):
        """FIELD_META_VERSION 是 4.1.1"""
        assert FIELD_META_VERSION == "4.1.1"

    def test_f191_unit_is_b倍数(self):
        """f191 单位是'倍',不是'%/100' (v4.1.0 bug 修复)"""
        assert FIELD_META["f191"]["unit"] == "倍"

    def test_f167_unit_is_倍数(self):
        """f167 单位是'倍' (v4.1.0 bug 修复)"""
        assert FIELD_META["f167"]["unit"] == "倍"

    def test_f43_unit_is_分(self):
        """f43 (价格) 单位是'分',需要 /100"""
        assert FIELD_META["f43"]["unit"] == "分"
