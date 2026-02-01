"""
TOMBO NLP Library - Natural language processing
Text processing, tokenization, stemming, sentiment analysis, TF-IDF.
"""

import math
import re
from typing import Dict, List, Tuple, Set, Optional


class Tokenizer:
    """Text tokenization."""
    
    def __init__(self, lowercase: bool = True):
        """Initialize tokenizer.
        
        Args:
            lowercase: Convert to lowercase
        """
        self.lowercase = lowercase
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        if self.lowercase:
            text = text.lower()
        
        # Remove punctuation and split
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        
        return tokens
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]


class StopWords:
    """Common stop words."""
    
    COMMON = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "up", "about", "into", "through", "during",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "should", "may", "might",
        "can", "this", "that", "these", "those", "i", "you", "he", "she", "it",
        "we", "they", "what", "which", "who", "when", "where", "why", "how"
    }
    
    @classmethod
    def is_stop_word(cls, word: str) -> bool:
        """Check if word is stop word."""
        return word.lower() in cls.COMMON
    
    @classmethod
    def remove_stop_words(cls, tokens: List[str]) -> List[str]:
        """Remove stop words from tokens."""
        return [t for t in tokens if not cls.is_stop_word(t)]


class Stemmer:
    """Simple stemmer (removes common suffixes)."""
    
    SUFFIXES = [
        "tion", "sion", "ment", "ness", "ful", "less", "able", "ible",
        "ous", "ive", "ing", "ed", "er", "est", "ly", "al", "ical"
    ]
    
    @classmethod
    def stem(cls, word: str) -> str:
        """Stem word by removing suffix.
        
        Args:
            word: Word to stem
            
        Returns:
            Stemmed word
        """
        word = word.lower()
        
        for suffix in cls.SUFFIXES:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
        
        return word
    
    @classmethod
    def stem_tokens(cls, tokens: List[str]) -> List[str]:
        """Stem list of tokens."""
        return [cls.stem(t) for t in tokens]


class TFIDFVectorizer:
    """TF-IDF vectorization for text documents."""
    
    def __init__(self):
        """Initialize vectorizer."""
        self.vocabulary: Dict[str, int] = {}
        self.idf_scores: Dict[str, float] = {}
        self.num_documents = 0
    
    def fit(self, documents: List[List[str]]):
        """Fit vectorizer on documents.
        
        Args:
            documents: List of tokenized documents
        """
        self.num_documents = len(documents)
        
        # Build vocabulary and calculate IDF
        doc_freq = {}
        
        for doc_idx, doc in enumerate(documents):
            unique_tokens = set(doc)
            
            for token in unique_tokens:
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)
                
                doc_freq[token] = doc_freq.get(token, 0) + 1
        
        # Calculate IDF scores
        for token, df in doc_freq.items():
            idf = math.log(self.num_documents / df) if df > 0 else 0
            self.idf_scores[token] = idf
    
    def transform(self, document: List[str]) -> Dict[int, float]:
        """Transform document to TF-IDF vector.
        
        Args:
            document: Tokenized document
            
        Returns:
            Dictionary mapping token indices to TF-IDF scores
        """
        tf_scores = {}
        
        # Calculate term frequency
        for token in document:
            if token in self.vocabulary:
                idx = self.vocabulary[token]
                tf_scores[idx] = tf_scores.get(idx, 0) + 1
        
        # Apply IDF
        doc_length = len(document)
        tfidf_scores = {}
        
        for idx, tf in tf_scores.items():
            # Get token from vocabulary
            token = [t for t, i in self.vocabulary.items() if i == idx][0]
            idf = self.idf_scores.get(token, 0)
            
            tfidf = (tf / doc_length) * idf if doc_length > 0 else 0
            tfidf_scores[idx] = tfidf
        
        return tfidf_scores


class SentimentAnalyzer:
    """Simple sentiment analysis."""
    
    POSITIVE_WORDS = {
        "good", "great", "awesome", "excellent", "amazing", "wonderful",
        "fantastic", "best", "love", "perfect", "happy", "joy", "glad",
        "brilliant", "beautiful", "wonderful"
    }
    
    NEGATIVE_WORDS = {
        "bad", "terrible", "awful", "horrible", "worst", "hate", "sad",
        "angry", "disgusting", "ugly", "poor", "useless", "dumb", "stupid",
        "annoying", "disappointing"
    }
    
    @classmethod
    def analyze(cls, text: str) -> Dict:
        """Analyze sentiment of text.
        
        Args:
            text: Input text
            
        Returns:
            Dict with sentiment scores
        """
        tokenizer = Tokenizer(lowercase=True)
        tokens = set(tokenizer.tokenize(text))
        
        positive_count = sum(1 for t in tokens if t in cls.POSITIVE_WORDS)
        negative_count = sum(1 for t in tokens if t in cls.NEGATIVE_WORDS)
        total = positive_count + negative_count
        
        if total == 0:
            sentiment_score = 0.5
        else:
            sentiment_score = positive_count / total
        
        # Determine sentiment label
        if sentiment_score >= 0.6:
            label = "positive"
        elif sentiment_score <= 0.4:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "sentiment": label,
            "score": sentiment_score,
            "positive_count": positive_count,
            "negative_count": negative_count
        }


class WordFrequency:
    """Calculate word frequencies in text."""
    
    @classmethod
    def count(cls, tokens: List[str]) -> Dict[str, int]:
        """Count word frequencies.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Dictionary of word frequencies
        """
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        return freq
    
    @classmethod
    def most_common(cls, tokens: List[str], n: int = 10) -> List[Tuple[str, int]]:
        """Get most common words.
        
        Args:
            tokens: List of tokens
            n: Number of top words
            
        Returns:
            List of (word, frequency) tuples
        """
        freq = cls.count(tokens)
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_freq[:n]


class TextProcessingPipeline:
    """Complete text processing pipeline."""
    
    def __init__(self, lowercase: bool = True, remove_stopwords: bool = True, 
                 stem: bool = True):
        """Initialize pipeline.
        
        Args:
            lowercase: Convert to lowercase
            remove_stopwords: Remove stop words
            stem: Apply stemming
        """
        self.tokenizer = Tokenizer(lowercase=lowercase)
        self.remove_stopwords = remove_stopwords
        self.stem = stem
    
    def process(self, text: str) -> List[str]:
        """Process text through pipeline.
        
        Args:
            text: Input text
            
        Returns:
            List of processed tokens
        """
        # Tokenize
        tokens = self.tokenizer.tokenize(text)
        
        # Remove stop words
        if self.remove_stopwords:
            tokens = StopWords.remove_stop_words(tokens)
        
        # Stem
        if self.stem:
            tokens = Stemmer.stem_tokens(tokens)
        
        return tokens


class NGramExtractor:
    """Extract n-grams from text."""
    
    @classmethod
    def extract(cls, tokens: List[str], n: int = 2) -> List[Tuple]:
        """Extract n-grams.
        
        Args:
            tokens: List of tokens
            n: Size of n-gram
            
        Returns:
            List of n-gram tuples
        """
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    @classmethod
    def extract_frequencies(cls, tokens: List[str], n: int = 2) -> Dict:
        """Extract n-gram frequencies.
        
        Args:
            tokens: List of tokens
            n: Size of n-gram
            
        Returns:
            Dictionary of n-gram frequencies
        """
        ngrams = cls.extract(tokens, n)
        freq = {}
        for ngram in ngrams:
            key = " ".join(ngram)
            freq[key] = freq.get(key, 0) + 1
        return freq
