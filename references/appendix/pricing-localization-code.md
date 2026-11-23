# 定价本地化 · 工程校验代码（附录）

> 2026-11-23 自 `references/pricing-localization.md` §13 迁出（v72「越界内容拆附录」）。主文件留设计判断、法标清单与 20 条自检；本文件只放可跑代码，**不参与**检索索引、README 资产表与审计章节校验。
>
> 运行：每段存成 `.py` 单独跑，或按 A→F 拼进一个文件：`python -I -X utf8 <file>`。只用标准库（`decimal` / `datetime`）。
>
> 迁移时**未改代码**，也**未重跑**；原主文件记的「6 段实跑通过」未在本次复核。

> 全部只用标准库（`decimal` / `datetime`）。把每段存成 `.py` 单独跑，或拼在一个文件里按顺序执行。

### 段 A · 最小单位与展示位数

```python
from decimal import Decimal, ROUND_HALF_UP

# ISO 4217 List One 实测值（SIX, Pblshd="2026-09-17"）
MINOR_UNITS = {
    "JPY": 0, "KRW": 0, "VND": 0, "ISK": 0, "XOF": 0,
    "KWD": 3, "BHD": 3, "JOD": 3, "OMR": 3, "TND": 3,
    "CLF": 4, "UYW": 4,
    "EUR": 2, "USD": 2, "HUF": 2, "TWD": 2, "IDR": 2,
}
NO_MINOR_UNIT = {"XDR"}  # CcyMnrUnts = "N.A."


def digits_of(currency: str) -> int:
    if currency in NO_MINOR_UNIT:
        raise ValueError(f"{currency} 无最小单位（ISO 4217 N.A.），不可用于价格")
    if currency not in MINOR_UNITS:
        raise KeyError(f"{currency} 未登记，请回 ISO 4217 List One 查 <CcyMnrUnts>")
    return MINOR_UNITS[currency]


def quantize_money(amount, currency: str) -> Decimal:
    d = digits_of(currency)
    return Decimal(str(amount)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)


def render(amount, currency: str) -> str:
    d = digits_of(currency)
    q = quantize_money(amount, currency)
    return f"{q:,.{d}f} {currency}"


assert render("1234.5", "JPY") == "1,235 JPY"      # 0 位：小数被拒绝
assert render("9.99", "USD") == "9.99 USD"
assert render("1234.5", "KWD") == "1,234.500 KWD"  # 3 位
for cur, amt in [("JPY", "1234.5"), ("USD", 9.99), ("KWD", "1234.5")]:
    print(f"{cur:>4} {render(amt, cur)}")
print("段 A OK")
```

### 段 B · 含税反算（零小数币种也要对）

```python
from decimal import Decimal, ROUND_HALF_UP


def split_tax(gross, rate, digits: int):
    q = Decimal(1).scaleb(-digits)
    g = Decimal(str(gross)).quantize(q)
    r = Decimal(str(rate))
    net = (g / (1 + r)).quantize(q, rounding=ROUND_HALF_UP)
    return net, g - net


cases = [
    ("9.99", "0.19", 2, "DE 19%"),
    ("1100", "0.10", 0, "JP 10%"),
    ("1100", "0.08", 0, "JP 8%"),
    ("120.00", "0.20", 2, "UK 20%"),
]
for gross, rate, d, label in cases:
    net, tax = split_tax(gross, rate, d)
    print(f"{label:<7} gross={gross:>7} net={net:>8} tax={tax:>7}")

assert split_tax("1100", "0.10", 0) == (Decimal("1000"), Decimal("100"))
assert split_tax("9.99", "0.19", 2)[0] + split_tax("9.99", "0.19", 2)[1] == Decimal("9.99")
print("段 B OK")
```

### 段 C · 逐行取整 vs 汇总取整的 1 分差

```python
from decimal import Decimal, ROUND_HALF_UP
from itertools import combinations

Q = Decimal("0.01")
RATE = Decimal("0.19")  # 德国标准税率
CATALOG = [Decimal(x) for x in ("3.99", "7.49", "12.99", "19.99", "24.99", "33.33", "44.44")]


def net_of(gross: Decimal) -> Decimal:
    return (gross / (1 + RATE)).quantize(Q, rounding=ROUND_HALF_UP)


def tax_of(gross: Decimal) -> Decimal:
    return gross - net_of(gross)


def audit(cart):
    line_taxes = sum(tax_of(g) for g in cart)
    gross_total = sum(cart)
    tax_on_total = tax_of(gross_total)
    return gross_total, line_taxes, tax_on_total, tax_on_total - line_taxes


# 找出第一个"逐行取整 ≠ 汇总取整"的购物车（真实存在的 1 分差）
for cart in combinations(CATALOG, 3):
    g, lines, whole, delta = audit(cart)
    if delta != 0:
        break

rounding_entry = delta  # 记账金额；负值 = 贷记客户余额
print("购物车:", [str(x) for x in cart])
print("含税合计:", g, " 逐行税额合计:", lines, " 汇总反算:", whole)
print("1 分差额:", delta, "→ 记账行:", rounding_entry, "（Stripe: credit/debit to customer balance）")

assert lines + rounding_entry == whole          # 明细 + 记账行 = 汇总税额
assert rounding_entry != 0                      # 必须真的存在差额，否则这段没演示到东西
print("段 C OK：这 1 分必须有一行会计落点，否则发票明细与总额永远对不上")
```

### 段 D · FX 缓冲定价 + 价格点（两位小数 vs 零小数）

```python
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

COST_USD = Decimal("10")
MARGIN = Decimal("0.40")
BUFFER = Decimal("0.03")


def charm(value: Decimal, digits: int) -> Decimal:
    q = Decimal(1).scaleb(-digits)
    base = value.quantize(q, rounding=ROUND_CEILING)  # 不低于目标价
    if digits == 2:
        cand = base.quantize(Decimal(1), rounding=ROUND_CEILING) - Decimal("0.01")
        return cand if cand >= value else base
    if digits == 0:
        ten = Decimal(10)
        return (value / ten).quantize(Decimal(1), rounding=ROUND_CEILING) * ten
    raise ValueError("本函数只处理 0 位与 2 位币种")


def local_price(fx, digits, cost=COST_USD, margin=MARGIN, buffer=BUFFER):
    target = cost / (1 - margin) * Decimal(fx) * (1 + buffer)
    price = charm(target, digits)
    landed = cost * Decimal(fx)
    return target, price, (price - landed) / price


for fx, digits, cur in [("0.92", 2, "EUR"), ("150", 0, "JPY"), ("1.37", 2, "CAD")]:
    target, price, gm = local_price(fx, digits)
    print(f"{cur}: 目标 {target:.4f} → 价点 {price} | 毛利 {gm:.2%}")
    assert gm >= MARGIN, f"{cur} 毛利跌破下限"

assert charm(Decimal("20.13"), 2) == Decimal("20.99")
assert charm(Decimal("2980.4"), 0) == Decimal("2990")
print("段 D OK")
```

### 段 E · "原价"法定窗口校验（DE 30 日 / CN 7 日）

```python
from datetime import date, timedelta
from decimal import Decimal

# (应用日期, 向消费者实际适用的含税总价)
HISTORY = [
    (date(2026, 9, 20), Decimal("49.90")),
    (date(2026, 10, 5), Decimal("44.90")),
    (date(2026, 10, 18), Decimal("39.90")),
    (date(2026, 10, 30), Decimal("39.90")),
]
TODAY = date(2026, 11, 18)


def lowest_in_window(history, reference, days):
    start = reference - timedelta(days=days)
    seen = [p for d, p in history if start <= d <= reference]
    return min(seen) if seen else None


def admissible(advertised, lowest, fallback):
    legal_ceiling = lowest if lowest is not None else fallback
    return advertised <= legal_ceiling, legal_ceiling


cn_lowest = lowest_in_window(HISTORY, TODAY, 7)
last_price = HISTORY[-1][1]
cn_ok, cn_ceiling = admissible(Decimal("59.90"), cn_lowest, last_price)  # 前 7 日无交易→用最后成交价
de_lowest = lowest_in_window(HISTORY, TODAY, 30)
de_ok, de_ceiling = admissible(Decimal("59.90"), de_lowest, last_price)

print(f"CN 7 日天花板 {cn_ceiling} → 标 59.90 合规? {cn_ok}")
print(f"DE 30 日天花板 {de_ceiling} → 标 59.90 合规? {de_ok}")
assert not cn_ok and not de_ok

print("正确写法：原价 39.90（近 30 天最低价）")
print("段 E OK")
```

### 段 F · Grundpreis（单位价格）与 10g/10ml 豁免

```python
from decimal import Decimal, ROUND_HALF_UP


def unit_price(gross, net_content, unit="kg", digits=2):
    gross = Decimal(str(gross))
    net_content = Decimal(str(net_content))
    base = Decimal(1000) if unit == "kg" else (Decimal(1000) if unit == "ml" else Decimal(1))
    return (gross / net_content * base).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)


def needs_unit_price(content_g=None, volume_ml=None):
    """PAngV §4(3)：净重 <10 g 或净体积 <10 ml 的商品可免标基准价。"""
    g = Decimal(str(content_g)) if content_g is not None else None
    v = Decimal(str(volume_ml)) if volume_ml is not None else None
    if g is not None and v is not None:
        return not (g < 10 and v < 10)
    if g is not None:
        return g >= 10
    if v is not None:
        return v >= 10
    return True


print("2.49 EUR / 250 g →", unit_price("2.49", 250, "kg"), "EUR/kg")
print("1.99 EUR / 750 ml →", unit_price("1.99", 750, "ml"), "EUR/L")
assert unit_price("2.49", 250, "kg") == Decimal("9.96")
assert needs_unit_price(content_g=8) is False      # 8 g 香水小样：豁免
assert needs_unit_price(content_g=250) is True
print("段 F OK")
```
