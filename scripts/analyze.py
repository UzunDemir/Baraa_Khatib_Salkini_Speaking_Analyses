import re
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()

# Normalize whitespace
text_flat = re.sub(r'\s+', ' ', text).strip()

# --- Sentence split ---
# Split on . ! ? followed by space+capital or end, keep decent heuristic
sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
raw_sentences = sentence_endings.split(text_flat)
sentences = [s.strip() for s in raw_sentences if s.strip()]

# --- Word tokenize ---
word_pattern = re.compile(r"[A-Za-z']+")
words_raw = word_pattern.findall(text_flat)
# clean stray apostrophes at edges
words = [w.strip("'").lower() for w in words_raw if w.strip("'")]

word_count = len(words)
sentence_count = len(sentences)

print("WORD_COUNT", word_count)
print("SENTENCE_COUNT", sentence_count)
print("SAMPLE_SENTENCES")
for s in sentences[:5]:
    print(" -", s)
