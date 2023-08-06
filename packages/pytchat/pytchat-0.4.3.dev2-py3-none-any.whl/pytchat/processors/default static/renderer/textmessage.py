from .base import BaseRenderer


class LiveChatTextMessageRenderer(BaseRenderer):
    @classmethod
    def init(cls, self, item):
        super(LiveChatTextMessageRenderer, cls).init(item, "textMessage")
