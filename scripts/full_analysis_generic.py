import re, sys, os
from collections import Counter

def analyze(path, out_path, title):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text_flat = re.sub(r'\s+', ' ', text).strip()

    sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
    raw_sentences = sentence_endings.split(text_flat)
    sentences = [s.strip() for s in raw_sentences if s.strip()]
    sentence_count = len(sentences)

    word_pattern = re.compile(r"[A-Za-z']+")
    words_raw = word_pattern.findall(text_flat)
    words = [w.strip("'").lower() for w in words_raw if w.strip("'")]
    word_count = len(words)

    word_freq = Counter(words)

    def ngrams(tokens, n):
        return zip(*[tokens[i:] for i in range(n)])

    bigrams = Counter(ngrams(words, 2))
    trigrams = Counter(ngrams(words, 3))

    def top_ngrams(tokens, n, min_count, top):
        c = Counter(ngrams(tokens, n))
        items = [(k, v) for k, v in c.items() if v >= min_count]
        items.sort(key=lambda x: -x[1])
        return items[:top]

    fourgrams = top_ngrams(words, 4, 3, 60)
    fivegrams = top_ngrams(words, 5, 3, 50)
    sixgrams = top_ngrams(words, 6, 2, 30)

    norm_sentences = [re.sub(r'[^a-z0-9 ]', '', s.lower()).strip() for s in sentences]
    norm_sentences = [re.sub(r'\s+', ' ', s) for s in norm_sentences]
    sent_freq = Counter(s for s in norm_sentences if s)
    rep_sentence = {}
    for orig, norm in zip(sentences, norm_sentences):
        if norm not in rep_sentence:
            rep_sentence[norm] = orig
    repeated = [(s, c) for s, c in sent_freq.items() if c > 1]
    repeated.sort(key=lambda x: -x[1])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Языковой анализ: {title}\n\n")
        f.write(f"- Всего слов: **{word_count}**\n")
        f.write(f"- Всего предложений: **{sentence_count}**\n")
        f.write(f"- Уникальных слов: **{len(word_freq)}**\n\n")

        f.write("## 1. Частота слов (топ-150)\n\n| # | Слово | Кол-во |\n|---|---|---|\n")
        for i, (w, c) in enumerate(word_freq.most_common(150), 1):
            f.write(f"| {i} | {w} | {c} |\n")

        f.write("\n## 2. Частота словосочетаний\n\n### Биграммы (топ-100)\n\n| # | Словосочетание | Кол-во |\n|---|---|---|\n")
        for i, (bg, c) in enumerate(bigrams.most_common(100), 1):
            f.write(f"| {i} | {' '.join(bg)} | {c} |\n")

        f.write("\n### Триграммы (топ-80)\n\n| # | Словосочетание | Кол-во |\n|---|---|---|\n")
        for i, (tg, c) in enumerate(trigrams.most_common(80), 1):
            f.write(f"| {i} | {' '.join(tg)} | {c} |\n")

        f.write("\n## 3. Обороты речи (4-6 слов)\n\n### 4 слова\n\n| # | Оборот | Кол-во |\n|---|---|---|\n")
        for i, (ng, c) in enumerate(fourgrams, 1):
            f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

        f.write("\n### 5 слов\n\n| # | Оборот | Кол-во |\n|---|---|---|\n")
        for i, (ng, c) in enumerate(fivegrams, 1):
            f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

        f.write("\n### 6 слов\n\n| # | Оборот | Кол-во |\n|---|---|---|\n")
        for i, (ng, c) in enumerate(sixgrams, 1):
            f.write(f"| {i} | {' '.join(ng)} | {c} |\n")

        f.write("\n## 4. Частота предложений (повторяющиеся дословно, топ-80)\n\n| # | Предложение | Кол-во |\n|---|---|---|\n")
        for i, (s, c) in enumerate(repeated[:80], 1):
            display = rep_sentence.get(s, s).replace("|", "/")
            f.write(f"| {i} | {display} | {c} |\n")

    return {
        "title": title,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "unique_words": len(word_freq),
        "top_words": word_freq.most_common(30),
        "top_bigrams": bigrams.most_common(20),
        "top_trigrams": trigrams.most_common(20),
        "repeated_count": len(repeated),
        "word_freq": word_freq,
    }

files = {
    "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt": "SQL Full Course for Beginners",
    "/mnt/user-data/uploads/_English__auto-generated___Python_Full_Course_for_Beginners__13_Hours____From_Zero_to_Hero__DownSub_.txt": "Python Full Course for Beginners",
    "/mnt/user-data/uploads/_English__auto-generated___Data_Modeling_in_Power_BI_Full_Course_for_Beginners__5_Hours____From_Zero.txt": "Power BI Data Modeling Full Course",
    "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day1_Introduction___Data_Analytics__DownSub_com.txt": "Databricks Bootcamp Day1",
    "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day2_Data_Engineering__DownSub_com_.txt": "Databricks Bootcamp Day2",
    "/mnt/user-data/uploads/_English__auto-generated___Design_a_Data_Architecture_Like_I_Do_at_Work__Part_2___LIVE__DownSub_com_.txt": "Data Architecture Part2 (Live)",
    "/mnt/user-data/uploads/_English__auto-generated___Intro_to_Data_Architecture__Part_1___LIVE__DownSub_com_.txt": "Intro to Data Architecture Part1 (Live)",
    "/mnt/user-data/uploads/_English__auto-generated___Power_BI_Data_Modeling_Portfolio_Project_End-to-End__Nightmare_Data_Model.txt": "Power BI Portfolio Project",
}

os.makedirs("/home/claude/sql_course/reports", exist_ok=True)
summaries = []
for path, title in files.items():
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', title).strip('_').lower()
    out_path = f"/home/claude/sql_course/reports/{slug}_report.md"
    s = analyze(path, out_path, title)
    summaries.append((slug, out_path, s))
    print(f"{title}: words={s['word_count']} sentences={s['sentence_count']} unique={s['unique_words']} repeated_sent={s['repeated_count']}")

import pickle
with open("/home/claude/sql_course/summaries.pkl", "wb") as f:
    pickle.dump(summaries, f)
