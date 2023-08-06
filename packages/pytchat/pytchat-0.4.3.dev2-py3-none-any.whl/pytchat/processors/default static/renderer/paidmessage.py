import re
from . import currency
from .base import BaseRenderer
superchat_regex = re.compile(r"^(\D*)(\d{1,3}(,\d{3})*(\.\d*)*\b)$")


class Colors:
    pass


class LiveChatPaidMessageRenderer(BaseRenderer):
    @classmethod
    def init(cls, self, item):
        super(LiveChatPaidMessageRenderer, cls).init(item, "superChat")

    @classmethod
    def get_snippet(cls, self):
        super().get_snippet()
        amountDisplayString, symbol, amount = (
            cls.get_amountdata(cls.renderer)
        )
        self.amountValue = amount
        self.amountString = amountDisplayString
        self.currency = currency.symbols[symbol]["fxtext"] if currency.symbols.get(
            symbol) else symbol
        self.bgColor = cls.renderer.get("bodyBackgroundColor", 0)
        self.colors = cls.get_colors()

    @classmethod
    def get_amountdata(cls, self, renderer):
        amountDisplayString = renderer["purchaseAmountText"]["simpleText"]
        m = superchat_regex.search(amountDisplayString)
        if m:
            symbol = m.group(1)
            amount = float(m.group(2).replace(',', ''))
        else:
            symbol = ""
            amount = 0.0
        return amountDisplayString, symbol, amount

    @classmethod
    def get_colors(cls, self):
        colors = Colors()
        colors.headerBackgroundColor = cls.renderer.get("headerBackgroundColor", 0)
        colors.headerTextColor = cls.renderer.get("headerTextColor", 0)
        colors.bodyBackgroundColor = cls.renderer.get("bodyBackgroundColor", 0)
        colors.bodyTextColor = cls.renderer.get("bodyTextColor", 0)
        colors.timestampColor = cls.renderer.get("timestampColor", 0)
        colors.authorNameTextColor = cls.renderer.get("authorNameTextColor", 0)
        return colors
