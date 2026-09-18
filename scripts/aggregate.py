import re
from collections import Counter

files = {
    "SQL": "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt",
    "Python": "/mnt/user-data/uploads/_English__auto-generated___Python_Full_Course_for_Beginners__13_Hours____From_Zero_to_Hero__DownSub_.txt",
    "PowerBI_Modeling": "/mnt/user-data/uploads/_English__auto-generated___Data_Modeling_in_Power_BI_Full_Course_for_Beginners__5_Hours____From_Zero.txt",
    "Databricks_Day1": "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day1_Introduction___Data_Analytics__DownSub_com.txt",
    "Databricks_Day2": "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day2_Data_Engineering__DownSub_com_.txt",
    "DataArch_Part2_Live": "/mnt/user-data/uploads/_English__auto-generated___Design_a_Data_Architecture_Like_I_Do_at_Work__Part_2___LIVE__DownSub_com_.txt",
    "DataArch_Part1_Live": "/mnt/user-data/uploads/_English__auto-generated___Intro_to_Data_Architecture__Part_1___LIVE__DownSub_com_.txt",
    "PowerBI_Portfolio": "/mnt/user-data/uploads/_English__auto-generated___Power_BI_Data_Modeling_Portfolio_Project_End-to-End__Nightmare_Data_Model.txt",
}

word_pattern = re.compile(r"[A-Za-z']+")

def load_words(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    flat = re.sub(r'\s+', ' ', text).strip()
    raw = word_pattern.findall(flat)
    return [w.strip("'").lower() for w in raw if w.strip("'")]

def ngrams(tokens, n):
    return list(zip(*[tokens[i:] for i in range(n)]))

per_file_words = {}
per_file_wfreq = {}
per_file_bfreq = {}
per_file_tfreq = {}

total_words = 0
combined_wfreq = Counter()
combined_bfreq = Counter()
combined_tfreq = Counter()

for name, path in files.items():
    words = load_words(path)
    per_file_words[name] = words
    wf = Counter(words)
    bf = Counter(ngrams(words, 2))
    tf = Counter(ngrams(words, 3))
    per_file_wfreq[name] = wf
    per_file_bfreq[name] = bf
    per_file_tfreq[name] = tf
    combined_wfreq.update(wf)
    combined_bfreq.update(bf)
    combined_tfreq.update(tf)
    total_words += len(words)

n_files = len(files)

# Fingerprint words: appear in top-150 of every file
TOPN_W = 150
top_sets_w = {name: set(w for w,_ in wf.most_common(TOPN_W)) for name, wf in per_file_wfreq.items()}
all_words_union = set().union(*top_sets_w.values())
fingerprint_words = [w for w in all_words_union if all(w in s for s in top_sets_w.values())]
fingerprint_words.sort(key=lambda w: -combined_wfreq[w])

# near-fingerprint: appear in top-150 of at least 6/8 files but not all
count_in_top = {w: sum(1 for s in top_sets_w.values() if w in s) for w in all_words_union}
near_fingerprint = [w for w in all_words_union if count_in_top[w] >= 6 and w not in fingerprint_words]
near_fingerprint.sort(key=lambda w: (-count_in_top[w], -combined_wfreq[w]))

# Fingerprint bigrams: top-100 in at least 6/8 files
TOPN_B = 100
top_sets_b = {name: set(b for b,_ in bf.most_common(TOPN_B)) for name, bf in per_file_bfreq.items()}
all_b_union = set().union(*top_sets_b.values())
count_in_top_b = {b: sum(1 for s in top_sets_b.values() if b in s) for b in all_b_union}
fingerprint_bigrams = [b for b in all_b_union if count_in_top_b[b] >= 6]
fingerprint_bigrams.sort(key=lambda b: (-count_in_top_b[b], -combined_bfreq[b]))

TOPN_T = 100
top_sets_t = {name: set(t for t,_ in tf.most_common(TOPN_T)) for name, tf in per_file_tfreq.items()}
all_t_union = set().union(*top_sets_t.values())
count_in_top_t = {t: sum(1 for s in top_sets_t.values() if t in s) for t in all_t_union}
fingerprint_trigrams = [t for t in all_t_union if count_in_top_t[t] >= 5]
fingerprint_trigrams.sort(key=lambda t: (-count_in_top_t[t], -combined_tfreq[t]))

# Topic-specific vocabulary per file: top words in that file's top-100 that appear in FEWEST other files' top-300
TOPN_TOPIC_CHECK = 300
top_sets_w_wide = {name: set(w for w,_ in wf.most_common(TOPN_TOPIC_CHECK)) for name, wf in per_file_wfreq.items()}
topic_words = {}
for name, wf in per_file_wfreq.items():
    candidates = []
    for w, c in wf.most_common(100):
        others_containing = sum(1 for other, s in top_sets_w_wide.items() if other != name and w in s)
        if others_containing <= 1:  # appears (in top300) in at most 1 other file => fairly unique
            candidates.append((w, c, others_containing))
    topic_words[name] = candidates[:20]

# ================ WRITE REPORT ================
out = "/home/claude/sql_course/speaker_fingerprint_report.md"
with open(out, "w", encoding="utf-8") as f:
    f.write("# Сводный речевой профиль спикера (8 курсов)\n\n")
    f.write(f"Проанализировано файлов: **{n_files}**\n\n")
    f.write("| Курс | Слов | Уникальных слов |\n|---|---|---|\n")
    for name, words in per_file_words.items():
        f.write(f"| {name} | {len(words)} | {len(per_file_wfreq[name])} |\n")
    f.write(f"| **Итого** | **{total_words}** | **{len(combined_wfreq)}** |\n\n")

    f.write("## 1. Слова-отпечаток (входят в топ-150 абсолютно каждого из 8 файлов)\n\n")
    f.write("Это ядро его лексики независимо от темы — то, что действительно является личным стилем, а не тематикой курса.\n\n")
    f.write("| # | Слово | Всего употреблений (по всем 8 файлам) |\n|---|---|---|\n")
    for i, w in enumerate(fingerprint_words, 1):
        f.write(f"| {i} | {w} | {combined_wfreq[w]} |\n")

    f.write(f"\n## 2. Почти-отпечаток (топ-150 минимум в 6 из 8 файлов)\n\n")
    f.write("| # | Слово | В скольких файлах из 8 | Всего употреблений |\n|---|---|---|\n")
    for i, w in enumerate(near_fingerprint[:60], 1):
        f.write(f"| {i} | {w} | {count_in_top[w]} | {combined_wfreq[w]} |\n")

    f.write("\n## 3. Словосочетания-отпечаток (биграммы, топ-100 минимум в 6 из 8 файлов)\n\n")
    f.write("| # | Биграмма | В скольких файлах | Всего |\n|---|---|---|---|\n")
    for i, b in enumerate(fingerprint_bigrams[:80], 1):
        f.write(f"| {i} | {' '.join(b)} | {count_in_top_b[b]} | {combined_bfreq[b]} |\n")

    f.write("\n## 4. Устойчивые триграммы-отпечаток (топ-100 минимум в 5 из 8 файлов)\n\n")
    f.write("| # | Триграмма | В скольких файлах | Всего |\n|---|---|---|---|\n")
    for i, t in enumerate(fingerprint_trigrams[:60], 1):
        f.write(f"| {i} | {' '.join(t)} | {count_in_top_t[t]} | {combined_tfreq[t]} |\n")

    f.write("\n## 5. Топ-200 слов по всему корпусу (8 файлов вместе)\n\n")
    f.write("| # | Слово | Кол-во |\n|---|---|---|\n")
    for i, (w, c) in enumerate(combined_wfreq.most_common(200), 1):
        f.write(f"| {i} | {w} | {c} |\n")

    f.write("\n## 6. Топ-100 биграмм по всему корпусу\n\n")
    f.write("| # | Биграмма | Кол-во |\n|---|---|---|\n")
    for i, (b, c) in enumerate(combined_bfreq.most_common(100), 1):
        f.write(f"| {i} | {' '.join(b)} | {c} |\n")

    f.write("\n## 7. Топ-80 триграмм по всему корпусу\n\n")
    f.write("| # | Триграмма | Кол-во |\n|---|---|---|\n")
    for i, (t, c) in enumerate(combined_tfreq.most_common(80), 1):
        f.write(f"| {i} | {' '.join(t)} | {c} |\n")

    f.write("\n## 8. Тематическая (не общая) лексика по каждому курсу\n\n")
    f.write("Слова из топ-100 этого курса, которых почти нет в топ-300 остальных файлов — это словарь конкретной темы, а не речевой почерк.\n\n")
    for name, cands in topic_words.items():
        f.write(f"### {name}\n\n")
        f.write("| Слово | Кол-во в этом файле |\n|---|---|\n")
        for w, c, _ in cands:
            f.write(f"| {w} | {c} |\n")
        f.write("\n")

print("saved:", out)
print("fingerprint words:", len(fingerprint_words))
print("near fingerprint:", len(near_fingerprint))
print("fingerprint bigrams:", len(fingerprint_bigrams))
print("fingerprint trigrams:", len(fingerprint_trigrams))
print("total combined words:", total_words)
print(fingerprint_words[:40])
