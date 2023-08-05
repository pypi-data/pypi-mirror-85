import re
import html
import unicodedata
import cleantext
import lxml.html.clean

class Cleaner():
    def __init__(self, language='nl'):
        self.language = language

    def clean(self, text, 
                    lower=False, 
                    clean_html=True,
                    clean_js=True,
                    fix_unicode=True,
                    to_ascii=False,
                    clean_urls=True):
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Return normal form of the unicode string (e.g. remove \xa0 from string)
        if(fix_unicode):
            text = unicodedata.normalize('NFKD', text)
        
        # Remove JS code
        # First remove JS before removing other HTML tags.
        if(clean_js):
            js_cleaner = lxml.html.clean.Cleaner()
            text = js_cleaner.clean_html(text)

        # Remove HTML tags using a simple regex
        if(clean_html):
            text = re.sub('<.*?>', '', text)

        text = cleantext.clean(text, fix_unicode=fix_unicode, to_ascii=to_ascii, lower=lower, no_urls=clean_urls, replace_with_url="")

        return text