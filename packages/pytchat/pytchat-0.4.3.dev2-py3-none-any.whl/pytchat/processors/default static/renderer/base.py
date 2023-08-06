from datetime import datetime


class Author:
    pass


class BaseRenderer:
    @classmethod
    def init(cls, self, item, chattype):
        cls.renderer = list(item.values())[0]
        self.chattype = chattype
        self.author = Author()

    @classmethod
    def get_snippet(cls, self):
        self.type = self.chattype
        self.id = cls.renderer.get('id')
        timestampUsec = int(cls.renderer.get("timestampUsec", 0))
        self.timestamp = int(timestampUsec / 1000)
        tst = self.renderer.get("timestampText")
        if tst:
            self.elapsedTime = tst.get("simpleText")
        else:
            self.elapsedTime = ""
        self.datetime = self.get_datetime(timestampUsec)
        self.message, self.messageEx = self.get_message(self.renderer)
        self.id = cls.renderer.get('id')
        self.amountValue = 0.0
        self.amountString = ""
        self.currency = ""
        self.bgColor = 0

    @classmethod
    def get_authordetails(cls, self):
        self.author.badgeUrl = ""
        (self.author.isVerified,
         self.author.isChatOwner,
         self.author.isChatSponsor,
         self.author.isChatModerator) = (
            cls.get_badges(cls.renderer)
        )
        self.author.channelId = self.renderer.get("authorExternalChannelId")
        self.author.channelUrl = "http://www.youtube.com/channel/" + self.author.channelId
        self.author.name = self.renderer["authorName"]["simpleText"]
        self.author.imageUrl = self.renderer["authorPhoto"]["thumbnails"][1]["url"]

    @classmethod
    def get_message(cls, self, renderer):
        message = ''
        message_ex = []
        if renderer.get("message"):
            runs = renderer["message"].get("runs")
            if runs:
                for r in runs:
                    if r:
                        if r.get('emoji'):
                            message += r['emoji'].get('shortcuts', [''])[0]
                            message_ex.append({
                                'id': r['emoji'].get('emojiId').split('/')[-1],
                                'txt': r['emoji'].get('shortcuts', [''])[0],
                                'url': r['emoji']['image']['thumbnails'][0].get('url')
                            })
                        else:
                            message += r.get('text', '')
                            message_ex.append(r.get('text', ''))
        return message, message_ex

    @classmethod
    def get_badges(cls, self, renderer):
        self.author.type = ''
        isVerified = False
        isChatOwner = False
        isChatSponsor = False
        isChatModerator = False
        badges = renderer.get("authorBadges")
        if badges:
            for badge in badges:
                if badge["liveChatAuthorBadgeRenderer"].get("icon"):
                    author_type = badge["liveChatAuthorBadgeRenderer"]["icon"]["iconType"]
                    self.author.type = author_type
                    if author_type == 'VERIFIED':
                        isVerified = True
                    if author_type == 'OWNER':
                        isChatOwner = True
                    if author_type == 'MODERATOR':
                        isChatModerator = True
                if badge["liveChatAuthorBadgeRenderer"].get("customThumbnail"):
                    isChatSponsor = True
                    self.author.type = 'MEMBER'
                    cls.get_badgeurl(badge)
        return isVerified, isChatOwner, isChatSponsor, isChatModerator

    @classmethod
    def get_badgeurl(cls, self, badge):
        self.author.badgeUrl = badge["liveChatAuthorBadgeRenderer"]["customThumbnail"]["thumbnails"][0]["url"]

    @classmethod
    def get_datetime(cls, self, timestamp):
        dt = datetime.fromtimestamp(timestamp / 1000000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
