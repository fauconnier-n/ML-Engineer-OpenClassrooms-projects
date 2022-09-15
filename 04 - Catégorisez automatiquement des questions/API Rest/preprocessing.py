"""
Fonctions de preprocessing du texte en entrée de l'app
"""
# Imports
import re
import unicodedata
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from bs4 import BeautifulSoup
import spacy
from uncontract import CONTRACTION_MAP


def remove_code(text):
    """
    Retire les parties de code du post marquées par les bornes html <code></code>
    """
    cleaned_text = re.sub('<code>(.*?)</code>', ' ', text, flags=re.MULTILINE|re.DOTALL)

    return cleaned_text

# les fonctions suivantes proviennent de cet article:
# https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72

# éléments nécessaires aux fonctions de preprocessing
nltk.download('stopwords')
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')


def strip_html_tags(text):
    """
    Retire les tags HTML
    """
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


def remove_accented_chars(text):
    """
    Remplace les charactères avec des accents
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    """
    Remplace les expressions anglaises contractées (eg. "I've") par leur forme non contractée (eg. "I have")
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_special_characters(text, remove_digits=False):
    """ 
    Retire les charactères spéciaux
    """
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def lemmatize_text(text):
    """
    Lemmatize le texte
    """
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

def remove_stopwords(text, is_lower_case=False):
    """
    Retire les stopwords
    """
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

def tok(text):
    """
    Tokenize le texte
    """
    tokenizer = ToktokTokenizer()
    return tokenizer.tokenize(text)

def normalize_corpus(doc, code_stripping=True,
                     html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True, 
                     text_lemmatization=True, special_char_removal=True, 
                     stopword_removal=True, remove_digits=True):
    """
    Fonction aggrégeant les différentes fonctions de preprocessing du texte en entrée

    Args:
        corpus (strings): texte à préprocesser
        html_stripping (bool, optional): active le retrait des balises html. Defaults to True.
        contraction_expansion (bool, optional): active l'expansion des formes contractées. Defaults to True.
        accented_char_removal (bool, optional): active le retrait des accents. Defaults to True.
        text_lower_case (bool, optional): active le passage en minuscules. Defaults to True.
        text_lemmatization (bool, optional): active la lemmatization. Defaults to True.
        special_char_removal (bool, optional): active le retrait des charactères spéciaux. Defaults to True.
        stopword_removal (bool, optional): active le retrait des des stopwords. Defaults to True.
        remove_digits (bool, optional): active le retrait des chiffres. Defaults to True.

    Returns:
        string: texte préprocessé
    """
    # Remove the code
    if code_stripping:
        doc = remove_code(doc)
    # strip HTML
    if html_stripping:
        doc = strip_html_tags(doc)
    # remove accented characters
    if accented_char_removal:
        doc = remove_accented_chars(doc)
    # expand contractions    
    if contraction_expansion:
        doc = expand_contractions(doc)
    # lowercase the text    
    if text_lower_case:
        doc = doc.lower()
    # remove extra newlines
    doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
    # lemmatize text
    if text_lemmatization:
        doc = lemmatize_text(doc)
    # remove special characters and\or digits    
    if special_char_removal:
        # insert spaces between special characters to isolate them    
        special_char_pattern = re.compile(r'([{.(-)!}])')
        doc = special_char_pattern.sub(" \\1 ", doc)
        doc = remove_special_characters(doc, remove_digits=remove_digits)  
    # remove extra whitespace
    doc = re.sub(' +', ' ', doc)
    # remove stopwords
    if stopword_removal:
        doc = remove_stopwords(doc, is_lower_case=text_lower_case)

    return doc