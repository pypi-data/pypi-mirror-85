import emoji
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

def remove_emoji(text=None):

    if text:
        return emoji.get_emoji_regexp().sub(u'', text)
    else:
        return "Text is None"

