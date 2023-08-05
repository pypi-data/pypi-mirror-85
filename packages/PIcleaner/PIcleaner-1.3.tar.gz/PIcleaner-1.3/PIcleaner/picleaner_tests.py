import pytest
import re
import PIcleaner as pic

@pytest.fixture(scope="module")
def cleaner():
    return pic.Cleaner()

def test_default_language(cleaner):
    language = 'nl'
    assert cleaner.language == language, "Default Language Failed"

# @pytest.mark.parametrize('language', ['bg'])
# def test_non_existing_language(language, capsys):
#     _ = Cleaner(language)
#     captured = capsys.readouterr()
#     assert "Spacy model error: {}_core_news_sm".format(language) in captured.out, "Non-Existing Language Improper Exception"

@pytest.mark.parametrize('text', [r'<img src="https://www.oozo.nl/images/noimage.png" />Heb jij een interessante vraag op het snijvlak van privacy, cybersecurity en recht? Stuur je vraag naar',
                                  r'ING doet aangifte om cyberaanval,<p>ING gaat aangifte doen vanwege de grootschalige cyberaanval van zondagavond op het internet- en mobiel bankieren bij de bank</p>',
                                  r'Oekraïne pakt belangrijke cybercrimineel op,"<p>In Oekra&#239;ne is een belangrijke cybercrimineel opgepakt. Gennadi Kapkanov werd zondag gearresteerd in Kiev, meldde de Oekra&#239;ense politie maandag. Hij zou het Avalanche-netwerk hebben geleid.</p>',
                                  r'Politie rolt ’s werelds grootste DDoS-netwerk op; inval in Scheemda,"<img src=""https://www.oozo.nl/images/noimage.png"" />Driebergen &#8211; De Nederlandse politie heeft dinsdag 24 april de grootste cybercriminele website Webstresser.org opgerold. Webstresser.org was een zogenaamde ‘booter’ of ‘stresser’ dienst: een webs'])
def test_remove_html_tags(cleaner, text):
    result = cleaner.clean(text)
    assert re.search('<.*?>', result) is None, "Cleaned String Contains HTML tags"


@pytest.mark.parametrize('text', [r'<img src="https://www.oozo.nl/images/noimage.png" <script>console.log("test");</script>/>Heb jij een interessante vraag op het snijvlak van privacy, cybersecurity en recht? Stuur je vraag naar',
                                  r'<script>console.log("test");</script> Oekraïne pakt belangrijke cybercrimineel op,"<p>In Oekra&#239;ne is een belangrijke cybercrimineel opgepakt. Gennadi Kapkanov werd zondag gearresteerd in Kiev, meldde de Oekra&#239;ense politie maandag. Hij zou het Avalanche-netwerk hebben geleid.</p>',
                                  r'Politie rolt ’s werelds grootste<script>console.log("test");</script>DDoS-netwerk op; inval in Scheemda,"<img src=""https://www.oozo.nl/images/noimage.png"" />Driebergen &#8211; De Nederlandse politie heeft dinsdag 24 april de grootste cybercriminele website Webstresser.org opgerold. Webstresser.org was een zogenaamde ‘booter’ of ‘stresser’ dienst: een webs'])
def test_remove_js_code(cleaner, text):
    result = cleaner.clean(text)
    assert re.search(r'<script[\s\S]*?>[\s\S]*?<\/script>', result) is None, "Cleaned String Contains JavaScript Code"

def test_remove_urls(cleaner):
    inputs = [r'Bron https://schiedam24.nl/',
                r'Vrouw (18) en man overleden na ongeluk op A27 https://www.gelderlander.nl/brabant/vrouw-18-en-man-overleden-na-ongeluk-op-a27~abbe1d93/',
                r'Bouwgroep Moonen failliet verklaard door de rechtbank in Den Bosch http://brabantn.ws/7P1J',
                r'Drie mannen gearresteerd in Terneuzen voor bedreiging http://feedproxy.google.com/~r/omroepzeeland/~3/O-ItE_J-D6g/Drie-mannen-gearresteerd-in-Terneuzen-voor-bedreiging',
                r'Politie vindt mogelijk drugslab in woning in Zuidlaren https://www.nu.nl/binnenland/5211194/aantal-arrestaties-vondst-drugslab-zuidlaren-komt-zes.html',
                r'Roy L. krijgt 15 jaar voor rol in Belgische kasteelmoord https://www.bd.nl/tilburg/tilburger-roy-l-krijgt-15-jaar-voor-rol-in-belgische-kasteelmoord~a58b7ca41/']
    
    outputs = [r'Bron',
                r'Vrouw (18) en man overleden na ongeluk op A27',
                r'Bouwgroep Moonen failliet verklaard door de rechtbank in Den Bosch',
                r'Drie mannen gearresteerd in Terneuzen voor bedreiging',
                r'Politie vindt mogelijk drugslab in woning in Zuidlaren',
                r'Roy L. krijgt 15 jaar voor rol in Belgische kasteelmoord']

    for text, output in zip(inputs, outputs):
        result = cleaner.clean(text, clean_urls=True)
        assert result == output, "Cleaned String Contains URLs"