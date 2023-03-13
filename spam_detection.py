import html2text
import email
import imaplib
import chardet
import re
from email.header import decode_header
from gensim.corpora import WikiCorpus
from gensim.models.ldamodel import LdaModel
from gensim.test.utils import datapath
from gensim.corpora.dictionary import Dictionary
from gensim import similarities

# wczytanie gotowego modelu LDA
wiki = WikiCorpus("plwiki-latest-pages-articles.xml.bz2")
lda_model = LdaModel(wiki, num_topics=10, id2word=wiki.dictionary)

# próg decyzyjny dla klasyfikacji
threshold = 0.5

imap_server = "imap.wp.pl"
email_address = "krzysztofisthebest@wp.pl"
password = "haslotestowe123"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)

imap.select("Inbox")
_, msgnums = imap.search(None, "ALL")

for msgnum in msgnums[0].split():
    _, data = imap.fetch(msgnum, "(RFC822)")

    message = email.message_from_bytes(data[0][1])

    # konwersja treści HTML na tekst
    content = ''
    for part in message.walk():
        if part.get_content_maintype() == 'text':
            encoding = part.get_content_charset()
            if encoding is None:
                # Użyj modułu chardet do wykrycia kodowania
                encoding = chardet.detect(part.get_payload())['encoding']
            text = part.get_payload(decode=True).decode(encoding, 'ignore')
            text = re.sub(r'<table.*?>.*?</table>', '', text, flags=re.DOTALL)
            content = html2text.html2text(text)

    # konwersja tekstu na wektor bag-of-words
    bow = Dictionary.doc2bow(content.lower().split())

    # klasyfikacja za pomocą modelu LDA
    doc_lda = lda_model[bow]
    if max(doc_lda, key=lambda x: x[1])[1] > threshold:
        print(f"Wiadomość o numerze {msgnum} jest SPAMem")
    else:
        print(f"Wiadomość o numerze {msgnum} jest OK")

imap.close()
