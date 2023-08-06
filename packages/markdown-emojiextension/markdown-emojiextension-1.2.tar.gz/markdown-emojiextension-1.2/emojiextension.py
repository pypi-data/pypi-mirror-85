import io
import json
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

EMOJI_RE = r'(::)(.*?)::'

class EmojiExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'emojis': [[], 'List of Emojis.']
        }
        super(EmojiExtension, self).__init__(**kwargs)
        
    def extendMarkdown(self, md, md_globals):
        emojis = self._as_dictionary(self.getConfig('emojis'))
        pattern = EmojiInlinePattern(EMOJI_RE, emojis)
        md.inlinePatterns.add('emoji', pattern,'<not_strong')
        
    def _as_dictionary(self, emojis):
        return dict((emoji['key'], emoji['value']) for emoji in emojis)
    
    @staticmethod
    def create_from_json(filename):
        with io.open(filename, encoding='utf-8') as filehandle:
            data = json.load(filehandle)
            return EmojiExtension(emojis=data)
        
class EmojiInlinePattern(Pattern):
    
    def __init__(self, pattern, emojis):
        super(EmojiInlinePattern, self).__init__(pattern)
        self.emojis = emojis
        
    def handleMatch(self, m):
        emoji_key = m.group(3)
        
        return self.emojis.get(emoji_key, '')


def makeExtension(**kwargs):    # pragma: no cover
    return EmojiExtension.create_from_json(**kwargs)
