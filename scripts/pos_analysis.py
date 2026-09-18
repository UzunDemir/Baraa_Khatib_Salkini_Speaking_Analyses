import re
import json
import gc
import spacy
from collections import Counter, defaultdict

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "lemmatizer"])
nlp.max_length = 3_000_000

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

pos_word_freq = defaultdict(Counter)
pos_totals = Counter()
total_tokens = 0

CHUNK_SIZE = 20000  # characters per chunk

for path in files:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    flat = re.sub(r'\s+', ' ', text).strip()
    # split into chunks on spaces near CHUNK_SIZE boundary
    chunks = []
    start = 0
    while start < len(flat):
        end = min(start + CHUNK_SIZE, len(flat))
        if end < len(flat):
            sp = flat.rfind(' ', start, end)
            if sp > start:
                end = sp
        chunks.append(flat[start:end])
        start = end

    for doc in nlp.pipe(chunks, batch_size=4):
        for tok in doc:
            if tok.is_space or tok.is_punct:
                continue
            word = tok.text.lower()
            if not re.match(r"^[a-z']+$", word):
                continue
            pos_word_freq[tok.pos_][word] += 1
            pos_totals[tok.pos_] += 1
            total_tokens += 1
    print(path.split('/')[-1][:40], "-> running total:", total_tokens)
    gc.collect()

with open("pos_word_freq.json", "w", encoding="utf-8") as f:
    json.dump({pos: c.most_common() for pos, c in pos_word_freq.items()}, f)

print("POS totals:", pos_totals.most_common())
print("total tokens tagged:", total_tokens)
