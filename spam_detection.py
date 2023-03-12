import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import imaplib
import email
import re

# Dane do połączenia z serwerem IMAP
IMAP_SERVER = 'imap.wp.pl'
IMAP_PORT = 993
EMAIL_ADDRESS = 'krzysztofisthebest@wp.pl'
EMAIL_PASSWORD = 'haslotestowe123'

# Funkcja do filtrowania emaila


def filter_email(email_text):
    # Usunięcie tagów HTML z emaila
    email_text = re.sub('<[^>]*>', '', email_text)
    # Tokenizacja emaila i usunięcie stop words
    tokens = [token for token in simple_preprocess(
        email_text) if token not in STOPWORDS]
    # Tworzenie tekstu bez stop words
    filtered_email = ' '.join(tokens)
    return filtered_email

# Funkcja do analizy słów


def analyze_words(text):
    # Tokenizacja tekstu
    tokens = simple_preprocess(text)
    # Usunięcie stop words
    filtered_tokens = [token for token in tokens if token not in STOPWORDS]
    # Utworzenie słownika
    dictionary = gensim.corpora.Dictionary([filtered_tokens])
    # Utworzenie korpusu
    corpus = [dictionary.doc2bow(filtered_tokens)]
    # Utworzenie modelu LDA
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus, id2word=dictionary, num_topics=1)
    # Zwrócenie tematu wiadomości
    return lda_model[dictionary.doc2bow(filtered_tokens)][0][0]


# Połączenie z serwerem IMAP
imap = imaplib.IMAP4_SSL(IMAP_SERVER)
imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
imap.select('Inbox')

# Pobranie wiadomości
status, messages = imap.search(None, 'ALL')
messages = messages[0].split(b' ')

# Analiza i filtrowanie wiadomości
for msg_id in messages:
    status, message = imap.fetch(msg_id, '(RFC822)')
    email_body = message[0][1].decode('utf-8')
    print(email_body)
    filtered_email = filter_email(email_body)
    topic = analyze_words(filtered_email)
    if topic == 0:  # temat oznaczony jako "spam"
        print('Email oznaczony jako spam')
        # Oznaczenie emaila jako spam
        # imap.store(msg_id, '+FLAGS', '\Flagged')
    else:
        print('Email nie jest spamem')
    #    # Przeniesienie emaila do folderu "Przetworzone"
        # imap.store(msg_id, '+X-GM-LABELS', '\\Przetworzone')

# Zamknięcie połączenia z serwerem IMAP
imap.close()
imap.logout()
