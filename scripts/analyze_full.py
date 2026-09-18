import re
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()

text_flat = re.sub(r'\s+', ' ', text).strip()

# --- Sentences ---
sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
raw_sentences = sentence_endings.split(text_flat)
sentences = [s.strip() for s in raw_sentences if s.strip()]
sentence_count = len(sentences)

# --- Words ---
word_pattern = re.compile(r"[A-Za-z']+")
words_raw = word_pattern.findall(text_flat)
words = [w.strip("'").lower() for w in words_raw if w.strip("'")]
word_count = len(words)

# --- Word frequency ---
word_freq = Counter(words)

# --- Stopwords (for filtering meaningless combos where needed) ---
stopwords = set("""a an the and or but if then so because as of at by for with about
against between into through during before after above below to from up down in out on off
over under again further once here there when where why how all any both each few more most
other some such no nor not only own same than too very s t can will just don should now i me
my myself we our ours ourselves you your yours yourself yourselves he him his himself she her
hers herself it its itself they them their theirs themselves what which who whom this that these
those am is are was were be been being have has had having do does did doing would could
ll re ve d m""".split())

def ngrams(tokens, n):
    return zip(*[tokens[i:] for i in range(n)])

bigrams = Counter(ngrams(words, 2))
trigrams = Counter(ngrams(words, 3))

# "Обороты речи" -- recurring longer speech patterns (4-6 word chains), min freq threshold
def top_ngrams(tokens, n, min_count=4, top=60):
    c = Counter(ngrams(tokens, n))
    items = [(k, v) for k, v in c.items() if v >= min_count]
    items.sort(key=lambda x: -x[1])
    return items[:top]

fourgrams = top_ngrams(words, 4, min_count=4, top=80)
fivegrams = top_ngrams(words, 5, min_count=3, top=60)
sixgrams = top_ngrams(words, 6, min_count=3, top=40)

# --- Sentence frequency (exact duplicate sentences) ---
norm_sentences = [re.sub(r'[^a-z0-9 ]', '', s.lower()).strip() for s in sentences]
norm_sentences = [re.sub(r'\s+', ' ', s) for s in norm_sentences]
sent_freq = Counter(s for s in norm_sentences if s)

# Map back to a nicely-cased representative for display
rep_sentence = {}
for orig, norm in zip(sentences, norm_sentences):
    if norm not in rep_sentence:
        rep_sentence[norm] = orig

# ================= Write report =================
out_path = "/home/claude/sql_course/sql_course_speech_report.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# Языковой анализ курса «SQL Full Course for Beginners»\n\n")
    f.write(f"- Всего слов: **{word_count}**\n")
    f.write(f"- Всего предложений: **{sentence_count}**\n")
    f.write(f"- Уникальных слов: **{len(word_freq)}**\n\n")

    f.write("## 1. Частота слов (топ-150)\n\n")
    f.write("| # | Слово | Кол-во |\n|---|---|---|\n")
    for i, (w, c) in enumerate(word_freq.most_common(150), 1):
        f.write(f"| {i} | {w} | {c} |\n")

    f.write("\n## 2. Частота словосочетаний\n\n")
    f.write("### Биграммы (топ-100)\n\n")
    f.write("| # | Словосочетание | Кол-во |\n|---|---|---|\n")
    for i, (bg, c) in enumerate(bigrams.most_common(100), 1):
        f.write(f"| {i} | {' '.join(bg)} | {c} |\n")

    f.write("\n### Триграммы (топ-80)\n\n")
    f.write("| # | Словосочетание | Кол-во |\n|---|---|---|\n")
    for i, (tg, c) in enumerate(trigrams.most_common(80), 1):
        f.write(f"| {i} | {' '.join(tg)} | {c} |\n")

    f.write("\n## 3. Обороты речи (устойчивые фразы из 4-6 слов, повторяющиеся ≥3-4 раз)\n\n")
    f.write("### 4 слова\n\n")
    f.write("| # | Оборот | Кол-во |\n|---|---|---|\n")
    for i, (ng, c) in enumerate(fourgrams, 1):
        f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

    f.write("\n### 5 слов\n\n")
    f.write("| # | Оборот | Кол-во |\n|---|---|---|\n")
    for i, (ng, c) in enumerate(fivegrams, 1):
        f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

    f.write("\n### 6 слов\n\n")
    f.write("| # | Оборот | Кол-во |\n|---|---|---|\n")
    for i, (ng, c) in enumerate(sixgrams, 1):
        f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

    f.write("\n## 4. Частота предложений (повторяющиеся дословно, топ-100)\n\n")
    f.write("| # | Предложение | Кол-во |\n|---|---|---|\n")
    repeated = [(s, c) for s, c in sent_freq.items() if c > 1]
    repeated.sort(key=lambda x: -x[1])
    for i, (s, c) in enumerate(repeated[:100], 1):
        display = rep_sentence.get(s, s)
        display = display.replace("|", "/")
        f.write(f"| {i} | {display} | {c} |\n")

print("DONE")
print("word_count", word_count)
print("sentence_count", sentence_count)
print("unique_words", len(word_freq))
print("repeated_sentences", len(repeated))
print("report at", out_path)
