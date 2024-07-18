import re
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

def generate_basic_pattern(input_text):
    escaped_text = re.escape(input_text)
    return escaped_text


typical_patterns = [
    r'\d{4}\s',          # e.g., 1234 
    r'\n<\d{3}>\s',      # e.g., <123> 
    r'=\d{4}=\s',         # e.g., =1234= 
    r'\d{3}\s|\n|\s+'    # e.g, 123 OR 123\n etc.




]


def generate_fuzzy_family_number_pattern(input_text, threshold=90):
    words = input_text.split()
    pattern = ''
    
    for word in words:
        best_match_ratio = 0
        best_pattern = r'\w*\s*'  # Default pattern if no match is found
        
        for typical_pattern in typical_patterns:
            cleaned_pattern = typical_pattern.replace(r'\s', '').replace(r'\d', '').replace('<', '').replace('>', '').replace('=', '')
            match_ratio = fuzz.partial_ratio(word, cleaned_pattern)
            if match_ratio > best_match_ratio:
                best_match_ratio = match_ratio
                best_pattern = typical_pattern
        
        if best_match_ratio > threshold:
            pattern += best_pattern
        else:
            pattern += r'\w*\s*'
    
    return pattern.strip()

def cluster_texts(texts, n_clusters=2):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    model = KMeans(n_clusters=n_clusters)
    model.fit(X)
    return model, vectorizer

def generate_patterns_from_clusters(model, vectorizer, texts):
    clusters = model.predict(vectorizer.transform(texts))
    patterns = {}
    for cluster in range(model.n_clusters):
        cluster_texts = [texts[i] for i in range(len(texts)) if clusters[i] == cluster]
        common_pattern = generate_common_pattern(cluster_texts)
        patterns[cluster] = common_pattern
    return patterns

def generate_common_pattern(texts):
    common_substring = longest_common_substring(texts)
    pattern = re.escape(common_substring)
    pattern = pattern.replace(r'\ ', r'\s*')
    return pattern

def longest_common_substring(texts):
    if not texts:
        return ""
    
    s1 = texts[0]
    longest_substring = ""
    
    for i in range(len(s1)):
        for j in range(i + 1, len(s1) + 1):
            substring = s1[i:j]
            if all(substring in s for s in texts) and len(substring) > len(longest_substring):
                longest_substring = substring

    return longest_substring

def generate_regex_patterns(text, threshold=90):
    basic_pattern = generate_basic_pattern(text)
    fuzzy_family_number_pattern = generate_fuzzy_family_number_pattern(text, threshold)
    advanced_patterns = generate_advanced_patterns(text)
    return {
        'basic_pattern': basic_pattern,
        'fuzzy_family_number_pattern': fuzzy_family_number_pattern,
        'advanced_patterns': advanced_patterns
    }

def generate_advanced_patterns(text):
    patterns = [
        re.compile(r'\n\d{4}\s+'),  # Family number
        re.compile(r'\s\d{4}\s'),  # Year
        re.compile(r'\d{2}\.\d{2}\.\d{4}'),  # dd.mm.yyyy
        re.compile(r'[A-Z][a-z]+(\s[A-Z][a-z]+)*(\s[A-Z]\.)?'),  # Names
        re.compile(r'\d+\s[A-Za-z]+\s(St|Ave|Blvd|Rd|Dr)\.?\s[A-Za-z]+,\s[A-Z]{2}\s\d{5}'),  # Addresses
        re.compile(r'\d{2}/\d{2}/\d{4}'),  # dd/mm/yyyy
        re.compile(r'\d{4}-\d{2}-\d{2}'),  # yyyy-mm-dd
        re.compile(r'\d+\s[A-Za-z]+\s(Street|Avenue|Boulevard|Road|Drive)\.?\s[A-Za-z]+,\s[A-Z]{2}\s\d{5}'),  # Full addresses
        re.compile(r'[A-Z][a-z]+,\s[A-Z][a-z]+,\s[A-Z]{2}'),  # Simplified addresses
        re.compile(r'[A-Z]\.(?:[A-Z]\.)?[a-z]+(\s[a-z]+)*'),    # initial and middle name
        re.compile(r'[A-Z][a-z]+(\s[A-Z][a-z]+)*(\s[A-Z]\.)?(?:\s[Jr|Sr|III|IV|V|VI|VII|VIII|IX|X])?'), #Full name with suffix
        re.compile(r'((?:Dr|Mr|Mrs|Ms|Miss)\.)\s[A-Z][a-z]+(\s[A-Z][a-z]+)*'),
        re.compile(r'[A-Z][a-z]+(\s[A-Z][a-z]+)*(\s[A-Z]\.)?(?:\s[A-Z][a-z]+)'), # name with apostrophes
        re.compile(r'([A-Z]+(?: [A-Z]+)*)\,?\s+([A-Z][a-z]+(\s[A-Z]\.?)?)'), # last name first
        re.compile(r'\n(\d{4})\s+?((?:.|[\n])*?)(?=\n\d{4})') # Chunk from one family number to the next

    ]

    matched_patterns = {}
    for pattern in patterns:
        matches = pattern.findall(text)
        if matches:
            matched_patterns[pattern.pattern] = matches
    return matched_patterns
