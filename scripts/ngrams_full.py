import re
from collections import Counter

files = [
    "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Python_Full_Course_for_Beginners__13_Hours____From_Zero_to_Hero__DownSub_.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Data_Modeling_in_Power_BI_Full_Course_for_Beginners__5_Hours____From_Zero.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day1_Introduction___Data_Analytics__DownSub_com.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day2_Data_Engineering__DownSub_com_.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Design_a_Data_Architecture_Like_I_Do_at_Work__Part_2___LIVE__DownSub_com_.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Intro_to_Data_Architecture__Part_1___LIVE__DownSub_com_.txt",
    "/mnt/user-data/uploads/_English__auto-generated___Power_BI_Data_Modeling_Portfolio_Project_End-to-End__Nightmare_Data_Model.txt",
]

word_pattern = re.compile(r"[A-Za-z']+")
all_words = []
for path in files:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    flat = re.sub(r'\s+', ' ', text).strip()
    raw = word_pattern.findall(flat)
    all_words.extend(w.strip("'").lower() for w in raw if w.strip("'"))

total_words = len(all_words)
vocab = Counter(all_words)
vocab_size = len(vocab)

def ngram_counter(tokens, n):
    return Counter(zip(*[tokens[i:] for i in range(n)]))

out = "/home/claude/sql_course/ngrams_2_10_report.md"
top_n_per_length = {2:100, 3:100, 4:80, 5:60, 6:50, 7:40, 8:30, 9:25, 10:20}

with open(out, "w", encoding="utf-8") as f:
    f.write("# Словарный запас и частотность фраз (n=2..10), корпус из 8 курсов\n\n")
    f.write(f"- Всего слов (токенов) в корпусе: **{total_words}**\n")
    f.write(f"- Общий словарный запас (уникальных слов): **{vocab_size}**\n\n")

    for n in range(2, 11):
        c = ngram_counter(all_words, n)
        total_ngrams = sum(c.values())
        unique_ngrams = len(c)
        top = top_n_per_length[n]
        f.write(f"## Фразы из {n} слов\n\n")
        f.write(f"Всего сочетаний: {total_ngrams}, уникальных: {unique_ngrams}\n\n")
        f.write("| # | Фраза | Кол-во |\n|---|---|---|\n")
        for i, (ng, cnt) in enumerate(c.most_common(top), 1):
            f.write(f"| {i} | {' '.join(ng)} | {cnt} |\n")
        f.write("\n")
        print(f"n={n}: total={total_ngrams} unique={unique_ngrams} top1={c.most_common(1)}")

print("VOCAB_SIZE", vocab_size)
print("TOTAL_WORDS", total_words)
print("saved", out)
