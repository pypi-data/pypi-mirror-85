import re
from . import currency
from .base import BaseRenderer
superchat_regex = re.compile(r"^(\D*)(\d{1,3}(,\d{3})*(\.\d*)*\b)$")


class Colors:
    pass


class LiveChatPaidStickerRenderer(BaseRenderer):
    @classmethod
    def __init__(cls, self, item):
        super(LiveChatPaidStickerRenderer, cls).__init__(item, "superSticker")

    @classmethod
    def get_snippet(cls, self):
        super().get_snippet()
        amountDisplayString, symbol, amount = (
            self.get_amountdata(self.renderer)
        )
        self.amountValue = amount
        self.amountString = amountDisplayString
        self.currency = currency.symbols[symbol]["fxtext"] if currency.symbols.get(
            symbol) else symbol
        self.bgColor = cls.renderer.get("backgroundColor", 0)
        self.sticker = "".join(("https:",
            self.renderer["sticker"]["thumbnails"][0]["url"]))
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
        colors.moneyChipBackgroundColor = cls.renderer.get("moneyChipBackgroundColor", 0)
        colors.moneyChipTextColor = cls.renderer.get("moneyChipTextColor", 0)
        colors.backgroundColor = cls.renderer.get("backgroundColor", 0)
        colors.authorNameTextColor = cls.renderer.get("authorNameTextColor", 0)
        return colors
