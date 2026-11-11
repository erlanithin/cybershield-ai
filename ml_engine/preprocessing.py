"""
CyberShield AI - Natural Language Processing & Text Preprocessing Pipeline
"""
import re
import string
import html

# Try importing nltk components; provide resilient fallbacks if downloads fail
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    
    # Download required datasets silently if not present
    for resource in ['stopwords', 'wordnet', 'punkt']:
        try:
            nltk.data.find(f'corpora/{resource}')
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass
    
    STOPWORDS = set(stopwords.words('english'))
    LEMMATIZER = WordNetLemmatizer()
except Exception:
    STOPWORDS = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
        "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
        'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
        'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
        'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
        'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
        'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
        'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all'
    }
    LEMMATIZER = None

# Crucial negation words that must NOT be removed as stopwords because they invert sentiment/toxicity
NEGATION_WORDS = {'not', 'no', 'nor', 'neither', 'never', 'none', 'nobody', 'nothing'}
EFFECTIVE_STOPWORDS = STOPWORDS - NEGATION_WORDS

# Emoji to semantic text mapping for cyberbullying & sentiment signals
EMOJI_MAP = {
    '😡': ' angry ',
    '🤬': ' cursing angry ',
    '👿': ' evil devil ',
    '😈': ' devil ',
    '💀': ' death skull ',
    '☠️': ' death danger ',
    '🔪': ' weapon knife ',
    '🗡️': ' knife stab ',
    '🔫': ' gun shoot ',
    '💣': ' bomb attack ',
    '🖕': ' offensive middle finger ',
    '🤮': ' disgusted vomit ',
    '🤢': ' disgusted sick ',
    '🤡': ' clown mock ',
    '💩': ' poop disgusting ',
    '👊': ' punch fight ',
    '💔': ' heartbroken ',
    '🔥': ' fire ',
    '❤️': ' love ',
    '😊': ' smile happy ',
    '👍': ' thumbs up good ',
    '👎': ' thumbs down bad ',
    '😭': ' crying sad ',
    '😢': ' crying tear ',
}

# Cyberbullying and toxicity lexicon for explainability and highlight detection
TRIGGER_LEXICON = {
    'threat': ['kill', 'murder', 'die', 'shoot', 'stab', 'beat', 'destroy', 'hang', 'choke', 'slaughter', 'hunt', 'dead', 'end you'],
    'hate': ['racist', 'terrorist', 'subhuman', 'filth', 'scum', 'degenerate', 'inbred', 'vermin', 'parasite', 'freak'],
    'harassment': ['ugly', 'loser', 'worthless', 'nobody', 'stalk', 'creep', 'idiot', 'pathetic', 'trash', 'failure', 'loser', 'annoying', 'kys'],
    'toxic': ['stupid', 'dumb', 'moron', 'shut up', 'bitch', 'asshole', 'bastard', 'crap', 'garbage', 'clown', 'suck', 'hate'],
    'sexual': ['send nudes', 'slut', 'whore', 'strip', 'naked', 'sex', 'grope', 'rape', 'pervert', 'horny']
}


def clean_text(text: str) -> str:
    """
    Cleans raw text input:
    - Decodes HTML entities
    - Replaces emojis with descriptive text tokens
    - Strips URLs and hyperlinks
    - Replaces social mentions (@user) and hashtags (#tag)
    - Normalizes repeated consecutive characters (e.g., 'heyyy' -> 'hey', 'looooser' -> 'loser')
    - Strips special symbols and extra whitespaces
    - Lemmatizes tokens while preserving meaningful negation words
    """
    if not text or not isinstance(text, str):
        return ""

    # Decode HTML entities (e.g. &amp; -> &)
    text = html.unescape(text)

    # Convert known emojis to descriptive tokens
    for emoji, token in EMOJI_MAP.items():
        if emoji in text:
            text = text.replace(emoji, token)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs (http, https, www, t.co)
    text = re.sub(r'https?://\S+|www\.\S+|bit\.ly/\S+', ' ', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove user mentions (e.g., @john_doe -> user)
    text = re.sub(r'@[\w_]+', ' ', text)

    # Remove hashtag symbol but keep text
    text = re.sub(r'#(\w+)', r'\1', text)

    # Compress repeated characters (e.g. "sooooo" -> "so", "biiiiitch" -> "biitch")
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Remove punctuation & numbers but keep basic whitespace
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Normalize whitespace
    words = text.split()

    # Filter stopwords and apply lemmatization
    cleaned_tokens = []
    for word in words:
        if word not in EFFECTIVE_STOPWORDS and len(word) > 1:
            if LEMMATIZER:
                try:
                    word = LEMMATIZER.lemmatize(word)
                except Exception:
                    pass
            cleaned_tokens.append(word)

    return " ".join(cleaned_tokens)


def extract_trigger_words(text: str, predicted_category: str = None) -> list:
    """
    Extracts high-impact abusive, toxic, or cyberbullying tokens from text
    for explainability and frontend highlighting.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_triggers = []

    # Check words from all categories
    for cat, keywords in TRIGGER_LEXICON.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                if kw not in found_triggers:
                    found_triggers.append(kw)

    return found_triggers[:8]
