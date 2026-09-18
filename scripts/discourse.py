import re
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()

text_flat = re.sub(r'\s+', ' ', text).strip()
sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
raw_sentences = sentence_endings.split(text_flat)
sentences = [s.strip() for s in raw_sentences if s.strip()]

word_pattern = re.compile(r"[A-Za-z']+")

def tokenize(s):
    return [w.strip("'").lower() for w in word_pattern.findall(s) if w.strip("'")]

# sentence-initial n-grams
starts = {2: Counter(), 3: Counter(), 4: Counter(), 5: Counter()}
start_examples = {2: {}, 3: {}, 4: {}, 5: {}}

for s in sentences:
    toks = tokenize(s)
    for n in (2,3,4,5):
        if len(toks) >= n:
            key = tuple(toks[:n])
            starts[n][key] += 1
            if key not in start_examples[n]:
                start_examples[n][key] = s

for n in (2,3,4,5):
    print(f"--- top start {n}-grams ---")
    for k, c in starts[n].most_common(40):
        print(c, ' '.join(k))
