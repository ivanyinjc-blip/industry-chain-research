#!/usr/bin/env python3
"""
chain-verify 周期触发矩阵工具
判断产业周期反证条件是否被触发(借鉴 multi-indicator circuit breaker)

用法:
  from cycle_trigger import CycleTriggerMatrix
  
  matrix = CycleTriggerMatrix()
  matrix.add_indicator("能繁母猪存栏", current=3950, threshold=4000, direction="below", confidence=0.9)
  matrix.add_indicator("猪粮比", current=4.9, threshold=5.0, direction="below", confidence=0.8)
  # ...
  triggered, score = matrix.evaluate(threshold_votes=3)
  if triggered:
      print(f"⚠️ 反证触发,综合得分 {score:.2f}")
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional
import json


Direction = Literal["above", "below", "between"]


@dataclass
class CycleIndicator:
    """单条周期指标"""
    name: str
    current: float
    threshold: float
    direction: Direction = "below"  # below/above/between
    confidence: float = 1.0  # 0-1
    data_status: str = "已核验"
    note: str = ""
    
    def is_triggered(self) -> bool:
        """判断单条指标是否被触发"""
        if self.direction == "below":
            return self.current < self.threshold
        elif self.direction == "above":
            return self.current > self.threshold
        elif self.direction == "between":
            # threshold 是下限,需要再传一个上限
            return False
        return False
    
    def to_dict(self):
        return {
            "name": self.name,
            "current": self.current,
            "threshold": self.threshold,
            "direction": self.direction,
            "triggered": self.is_triggered(),
            "confidence": self.confidence,
            "data_status": self.data_status,
            "note": self.note,
        }


@dataclass
class CycleTriggerMatrix:
    """周期触发矩阵 - 多指标共同触发判断"""
    indicators: List[CycleIndicator] = field(default_factory=list)
    threshold_votes: int = 3  # 默认 ≥ 3 条指标同时触发,才算反证被触发
    cycle_position: str = "未知"  # 当前周期位置
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_indicator(
        self,
        name: str,
        current: float,
        threshold: float,
        direction: Direction = "below",
        confidence: float = 1.0,
        data_status: str = "已核验",
        note: str = "",
    ):
        """添加一条周期指标"""
        ind = CycleIndicator(
            name=name, current=current, threshold=threshold,
            direction=direction, confidence=confidence,
            data_status=data_status, note=note,
        )
        self.indicators.append(ind)
        return ind
    
    def evaluate(self, threshold_votes: Optional[int] = None) -> tuple[bool, float]:
        """
        评估周期反证条件是否被触发
        
        Returns:
            (triggered, weighted_score)
            - triggered: bool,是否触发反证
            - weighted_score: float,加权得分(0-1)
        """
        if threshold_votes is None:
            threshold_votes = self.threshold_votes
        
        if not self.indicators:
            return False, 0.0
        
        triggered_count = sum(1 for ind in self.indicators if ind.is_triggered())
        weighted_score = sum(
            ind.confidence for ind in self.indicators if ind.is_triggered()
        ) / sum(ind.confidence for ind in self.indicators)
        
        triggered = triggered_count >= threshold_votes
        return triggered, weighted_score
    
    def report(self, threshold_votes: Optional[int] = None) -> str:
        """生成可读报告"""
        if threshold_votes is None:
            threshold_votes = self.threshold_votes
        
        triggered, score = self.evaluate(threshold_votes)
        
        lines = []
        lines.append(f"# 周期触发矩阵报告")
        lines.append(f"")
        lines.append(f"- 当前周期位置: {self.cycle_position}")
        lines.append(f"- 触发阈值: ≥ {threshold_votes} 条指标同时触发")
        lines.append(f"- 指标总数: {len(self.indicators)}")
        lines.append(f"- 触发指标数: {sum(1 for ind in self.indicators if ind.is_triggered())}")
        lines.append(f"- 加权得分: {score:.2%}")
        lines.append(f"- **反证状态: {'⚠️ 已触发' if triggered else '✅ 未触发'}**")
        lines.append(f"")
        lines.append(f"## 指标明细")
        lines.append(f"")
        lines.append(f"| 指标 | 当前值 | 阈值 | 方向 | 触发 | 置信度 | 数据状态 |")
        lines.append(f"|---|---|---|---|---|---|---|")
        for ind in self.indicators:
            status = "✓" if ind.is_triggered() else "✗"
            lines.append(
                f"| {ind.name} | {ind.current} | {ind.threshold} | "
                f"{ind.direction} | {status} | {ind.confidence:.0%} | {ind.data_status} |"
            )
        return "\n".join(lines)
    
    def to_dict(self):
        return {
            "cycle_position": self.cycle_position,
            "threshold_votes": self.threshold_votes,
            "indicators": [ind.to_dict() for ind in self.indicators],
            "created_at": self.created_at,
        }


# === 实战示例:猪周期判断 ===

def demo_pig_cycle():
    """猪周期反证矩阵示例(猪肉种猪育种反证条件 RC-1)"""
    print("=" * 60)
    print("实战示例:猪周期反证条件 RC-1")
    print("=" * 60)
    
    matrix = CycleTriggerMatrix(
        cycle_position="底部(2026-07-01)",
        threshold_votes=3,  # 6 类指标中 ≥ 3 条触发,才算反证
    )
    
    # 6 类周期指标(借鉴 chain-cycle)
    matrix.add_indicator(
        name="能繁母猪存栏(万头)",
        current=3950,
        threshold=4000,  # > 4000 万头 = 反证
        direction="above",
        confidence=0.95,
        data_status="已核验",
        note="农业农村部 2026-06 数据"
    )
    matrix.add_indicator(
        name="猪粮比",
        current=5.2,
        threshold=5.0,  # > 5.0 = 养殖盈利,反证底部判断
        direction="above",
        confidence=0.85,
        data_status="已核验",
        note="博亚和讯 2026-07-01"
    )
    matrix.add_indicator(
        name="生猪价格(元/公斤)",
        current=16.0,
        threshold=15.0,  # > 15 元 = 价格上涨,反证底部
        direction="above",
        confidence=0.80,
        data_status="已核验",
        note="全国均价"
    )
    matrix.add_indicator(
        name="头部企业资本开支",
        current=300,  # 牧原 + 温氏合计 300 亿
        threshold=200,  # < 200 亿 = 收缩(底部信号);> 200 = 扩张(反证)
        direction="above",
        confidence=0.75,
        data_status="估算",
        note="半年报披露"
    )
    matrix.add_indicator(
        name="板块 PE 历史分位",
        current=0.30,  # 30% 分位
        threshold=0.40,  # > 40% = 估值偏高,反证底部情绪
        direction="above",
        confidence=0.70,
        data_status="估算",
        note="近 3 年数据"
    )
    matrix.add_indicator(
        name="国家政策",
        current=1,  # 1 = 支持(底部);0 = 中性;−1 = 抑制(反证)
        threshold=0,
        direction="above",
        confidence=0.60,
        data_status="已核验",
        note="种业振兴政策"
    )
    
    print(matrix.report(threshold_votes=3))
    
    triggered, score = matrix.evaluate(threshold_votes=3)
    print()
    if triggered:
        print(f"⚠️ 反证触发(综合 {score:.0%}):猪周期可能已反转,需重新评估")
    else:
        print(f"✅ 反证未触发(综合 {score:.0%}):底部判断维持")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_pig_cycle()
    else:
        print("用法:")
        print("  python3 cycle_trigger.py demo  # 跑猪周期示例")
        print()
        print("或作为模块导入:")
        print("  from cycle_trigger import CycleTriggerMatrix")
