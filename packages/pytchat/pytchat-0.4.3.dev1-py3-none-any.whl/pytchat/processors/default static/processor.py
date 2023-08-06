import asyncio
import json
import time
from .complex_encoder import ComplexEncoder
from .renderer.textmessage import LiveChatTextMessageRenderer
from .renderer.paidmessage import LiveChatPaidMessageRenderer
from .renderer.paidsticker import LiveChatPaidStickerRenderer
from .renderer.legacypaid import LiveChatLegacyPaidMessageRenderer
from .renderer.membership import LiveChatMembershipItemRenderer
from .. chat_processor import ChatProcessor
from ... import config

logger = config.logger(__name__)


class Chatdata:

    def __init__(self, chatlist: list, timeout: float, parent):
        self.items = chatlist
        self.interval = timeout
        self.parent = parent

    def tick(self):
        if self.interval == 0:
            time.sleep(1)
            return
        time.sleep(self.interval / len(self.items))

    async def tick_async(self):
        if self.interval == 0:
            await asyncio.sleep(1)
            return
        await asyncio.sleep(self.interval / len(self.items))

    def yield_items(self):
        starttime = time.time()

        for c in self.items:
            # print("abs_diff",self.parent.abs_diff)
            next_chattime = c.timestamp / 1000

            if self.parent.first:
                self.parent.abs_diff = time.time() - next_chattime + 3
                # print("abs_diff", self.parent.abs_diff)
                self.parent.first = False
            else:
                tobe_disptime = self.parent.abs_diff + next_chattime
                wait_sec = tobe_disptime - time.time()
                if wait_sec < 0:
                    wait_sec = 0 
                time.sleep(wait_sec)
            
            yield c
        # print("intv", time.time() - starttime)
        time.sleep(max(1, 1 - (time.time() - starttime)))

    def json(self) -> str:
        return json.dumps([vars(a) for a in self.items], ensure_ascii=False, cls=ComplexEncoder)


class DefaultProcessor(ChatProcessor):
    def __init__(self):
        self.first = True
        self.abs_diff = 0

    def process(self, chat_components: list):

        chatlist = []
        timeout = 0

        if chat_components:
            for component in chat_components:
                timeout += component.get('timeout', 0)
                chatdata = component.get('chatdata')
                if chatdata is None:
                    continue
                for action in chatdata:
                    if action is None:
                        continue
                    if action.get('addChatItemAction') is None:
                        continue
                    if action['addChatItemAction'].get('item') is None:
                        continue

                    chat = self._parse(action)
                    if chat:
                        chatlist.append(chat)

        chatdata = Chatdata(chatlist, float(timeout), self)
        # if len(chatlist) > 0 and self.first:
        #     self.first = False
        return chatdata

    def _parse(self, sitem):
        action = sitem.get("addChatItemAction")
        if action is None:
            return None
        item = action.get("item")
        if item is None:
            return None
        try:
            renderer = self._get_renderer(item)
            if renderer is None:
                return None

            renderer.get_snippet()
            renderer.get_authordetails()
        except (KeyError, TypeError) as e:
            logger.error(f"{str(type(e))}-{str(e)} sitem:{str(sitem)}")
            return None
        return renderer

    def _get_renderer(self, item):
        # if item.get("liveChatTextMessageRenderer"):
        #     renderer = LiveChatTextMessageRenderer(item)
        # elif item.get("liveChatPaidMessageRenderer"):
        #     renderer = LiveChatPaidMessageRenderer(item)
        # elif item.get("liveChatPaidStickerRenderer"):
        #     renderer = LiveChatPaidStickerRenderer(item)
        # elif item.get("liveChatLegacyPaidMessageRenderer"):
        #     renderer = LiveChatLegacyPaidMessageRenderer(item)
        # elif item.get("liveChatMembershipItemRenderer"):
        #     renderer = LiveChatMembershipItemRenderer(item)
        # else:
        #     renderer = None
        # return renderer
        if item.get("liveChatTextMessageRenderer"):
            renderer = LiveChatTextMessageRenderer(item)
        elif item.get("liveChatPaidMessageRenderer"):
            renderer = LiveChatPaidMessageRenderer(item)
        elif item.get("liveChatPaidStickerRenderer"):
            renderer = LiveChatPaidStickerRenderer(item)
        elif item.get("liveChatLegacyPaidMessageRenderer"):
            renderer = LiveChatLegacyPaidMessageRenderer(item)
        elif item.get("liveChatMembershipItemRenderer"):
            renderer = LiveChatMembershipItemRenderer(item)
        else:
            renderer = None
        return renderer

