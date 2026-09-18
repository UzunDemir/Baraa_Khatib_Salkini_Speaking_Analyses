import re
from collections import Counter, defaultdict

files = {
    "SQL (rec)": "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt",
    "Python (rec)": "/mnt/user-data/uploads/_English__auto-generated___Python_Full_Course_for_Beginners__13_Hours____From_Zero_to_Hero__DownSub_.txt",
    "PowerBI Modeling (rec)": "/mnt/user-data/uploads/_English__auto-generated___Data_Modeling_in_Power_BI_Full_Course_for_Beginners__5_Hours____From_Zero.txt",
    "Databricks D1 (live)": "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day1_Introduction___Data_Analytics__DownSub_com.txt",
    "Databricks D2 (live)": "/mnt/user-data/uploads/_English__auto-generated___Databricks_Live_Bootcamp__Day2_Data_Engineering__DownSub_com_.txt",
    "DataArch P2 (live)": "/mnt/user-data/uploads/_English__auto-generated___Design_a_Data_Architecture_Like_I_Do_at_Work__Part_2___LIVE__DownSub_com_.txt",
    "DataArch P1 (live)": "/mnt/user-data/uploads/_English__auto-generated___Intro_to_Data_Architecture__Part_1___LIVE__DownSub_com_.txt",
    "PowerBI Portfolio (rec)": "/mnt/user-data/uploads/_English__auto-generated___Power_BI_Data_Modeling_Portfolio_Project_End-to-End__Nightmare_Data_Model.txt",
}

sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
word_pattern = re.compile(r"[A-Za-z']+")

modals = {"can","could","will","would","should","must","might","may","shall"}
fillers = {"well","actually","basically","literally","just","okay","ok","right","kind","sort","obviously","simply"}
pronouns_1s = {"i","i'm","i'll","i've","i'd","me","my","myself"}
pronouns_1p = {"we","we're","we'll","we've","we'd","us","our","ourselves"}
pronouns_2 = {"you","you're","you'll","you've","you'd","your","yourself","yourselves"}
question_openers = {"what","how","why","do","does","did","is","are","can","could","will","would","should","which","who"}

results = {}

for name, path in files.items():
    with open(path, encoding="utf-8") as f:
        text = f.read()
    flat = re.sub(r'\s+', ' ', text).strip()
    sents = [s.strip() for s in sentence_endings.split(flat) if s.strip()]
    n_sents = len(sents)

    words_all = []
    n_questions = 0
    n_imperative = 0
    sentence_lengths = []

    for s in sents:
        toks = [w.strip("'").lower() for w in word_pattern.findall(s) if w.strip("'")]
        words_all.extend(toks)
        sentence_lengths.append(len(toks))
        if s.rstrip().endswith('?'):
            n_questions += 1
        if toks:
            first = toks[0]
            if first in ("let's","go","click","open","create","select","use","check","make","add","remove","try","run","type","write","start","think","imagine","notice","take","look"):
                n_imperative += 1

    wc = len(words_all)
    wf = Counter(words_all)

    modal_count = sum(wf.get(m,0) for m in modals)
    filler_count = sum(wf.get(f,0) for f in fillers)
    p1s = sum(wf.get(p,0) for p in pronouns_1s)
    p1p = sum(wf.get(p,0) for p in pronouns_1p)
    p2 = sum(wf.get(p,0) for p in pronouns_2)
    avg_word_len = sum(len(w) for w in words_all)/wc if wc else 0
    avg_sent_len = sum(sentence_lengths)/n_sents if n_sents else 0

    results[name] = {
        "word_count": wc,
        "sentence_count": n_sents,
        "avg_sentence_len": avg_sent_len,
        "avg_word_len": avg_word_len,
        "modal_per_1000": modal_count/wc*1000,
        "filler_per_1000": filler_count/wc*1000,
        "pron_i_per_1000": p1s/wc*1000,
        "pron_we_per_1000": p1p/wc*1000,
        "pron_you_per_1000": p2/wc*1000,
        "question_pct": n_questions/n_sents*100,
        "imperative_pct": n_imperative/n_sents*100,
    }

for name, r in results.items():
    print(name)
    for k,v in r.items():
        print(f"  {k}: {v:.2f}" if isinstance(v,float) else f"  {k}: {v}")

import json
with open("deep_metrics.json","w") as f:
    json.dump(results, f, indent=2)
