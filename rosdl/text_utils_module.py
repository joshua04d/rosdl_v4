# rosdl/core/text_utils_module.py

import os
import re
import string
from typing import List, Union
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Optional imports for reading files
try:
    import docx
except ImportError:
    docx = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Download NLTK resources if not already present
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


class TextUtilities:
    """Utility class for text cleaning, tokenization, stemming, keyword extraction, and text analysis."""

    def __init__(self, language: str = 'english'):
        self.stop_words = set(stopwords.words(language))
        self.stemmer = PorterStemmer()

    # -----------------------------
    # Text Processing Methods
    # -----------------------------
    def clean_text(self, text: str, remove_stopwords: bool = True) -> str:
        """Clean text: lowercase, remove punctuation, numbers, extra spaces, optionally remove stopwords."""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if remove_stopwords:
            words = word_tokenize(text)
            words = [w for w in words if w not in self.stop_words]
            text = ' '.join(words)

        return text

    def tokenize(self, text: str) -> List[str]:
        """Tokenize cleaned text into words."""
        return word_tokenize(text)

    def stem_words(self, words: List[str]) -> List[str]:
        """Stem a list of words."""
        return [self.stemmer.stem(word) for word in words]

    def extract_keywords(self, documents: List[str], top_k: int = 10) -> List[str]:
        """Extract top keywords using TF-IDF from a list of documents."""
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_k)
        X = vectorizer.fit_transform(documents)
        return vectorizer.get_feature_names_out().tolist()

    def get_text_info(self, text: str) -> dict:
        """Return basic statistics about the text."""
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        word_count = len(words)
        unique_words = len(set(words))
        char_count = len(text)
        freq_words = Counter(words).most_common(10)

        return {
            "characters": char_count,
            "words": word_count,
            "unique_words": unique_words,
            "sentences": len(sentences),
            "top_words": freq_words
        }

# -----------------------------
# File Reading Helpers
# -----------------------------
def read_txt_file(filepath: str) -> str:
    """Read text from a .txt file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def read_docx_file(filepath: str) -> str:
    """Read text from a .docx file."""
    if not docx:
        raise ImportError("python-docx is not installed. Install it with: pip install python-docx")
    doc = docx.Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])


def read_pdf_file(filepath: str) -> str:
    """Read text from a PDF file."""
    if not PyPDF2:
        raise ImportError("PyPDF2 is not installed. Install it with: pip install PyPDF2")
    text = []
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text() or '')
    return '\n'.join(text)


# -----------------------------
# Unified Text Loader
# -----------------------------
def load_text(source: Union[str, os.PathLike], file_type: str = None) -> str:
    """
    Load text from a string or file.

    Args:
        source: Either a string of text or a file path.
        file_type: 'txt', 'docx', 'pdf'. If None, inferred from extension if source is a file.

    Returns:
        str: The text content.
    """
    if isinstance(source, str) and os.path.isfile(source):
        ext = (file_type or os.path.splitext(source)[1][1:]).lower()
        if ext == 'txt':
            return read_txt_file(source)
        elif ext == 'docx':
            return read_docx_file(source)
        elif ext == 'pdf':
            return read_pdf_file(source)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    elif isinstance(source, str):
        return source
    else:
        raise ValueError("Source must be a string or file path.")
