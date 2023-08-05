from abc import ABC
from dataclasses import dataclass


@dataclass
class Prefix(ABC):
    symbol: str
    power: int
    base = None

    @property
    def factor(self):
        return self.base ** self.power


@dataclass
class MetricPrefix(Prefix):
    base = 10


deca = MetricPrefix("da", 1)
hecto = MetricPrefix("h", 2)

kilo = MetricPrefix("k", 3)
mega = MetricPrefix("M", 6)
giga = MetricPrefix("G", 9)
tera = MetricPrefix("T", 12)
peta = MetricPrefix("P", 15)
exa = MetricPrefix("E", 18)

deci = MetricPrefix("d", -1)
centi = MetricPrefix("c", -2)

milli = MetricPrefix("m", -3)
micro = MetricPrefix("μ", -6)
nano = MetricPrefix("n", -9)
pico = MetricPrefix("p", -12)
femto = MetricPrefix("f", -15)
atto = MetricPrefix("a", -18)


@dataclass
class BinaryPrefix(Prefix):
    base = 1024


kibi = BinaryPrefix("Ki", 1)
mebi = BinaryPrefix("Mi", 2)
gibi = BinaryPrefix("Gi", 3)
tebi = BinaryPrefix("Ti", 4)
pebi = BinaryPrefix("Pi", 5)
exbi = BinaryPrefix("Ei", 6)
