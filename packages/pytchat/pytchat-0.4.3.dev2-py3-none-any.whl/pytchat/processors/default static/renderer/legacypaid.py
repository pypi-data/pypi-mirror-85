from .base import BaseRenderer


class LiveChatLegacyPaidMessageRenderer(BaseRenderer):
    @classmethod
    def init(cls, self, item):
        super(LiveChatLegacyPaidMessageRenderer, cls).init(item, "newSponsor")

    @classmethod
    def get_authordetails(cls, self):
        super().get_authordetails()
        self.author.isChatSponsor = True

    @classmethod
    def get_message(cls, self, renderer):
        message = (renderer["eventText"]["runs"][0]["text"]
                   ) + ' / ' + (renderer["detailText"]["simpleText"])
        return message, [message]
