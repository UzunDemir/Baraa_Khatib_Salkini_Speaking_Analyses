"""
Генератор предложений в стиле спикера (Markov-модель, обучена на
8 транскриптах курсов: SQL, Python, Power BI, Databricks, Data Architecture).

Использование:
    python3 generate_speaker_sentences.py            # 10 предложений
    python3 generate_speaker_sentences.py 20         # 20 предложений

Файл trigram_model_top6.json должен лежать рядом с этим скриптом.
"""
import json
import random
import sys
import os

START = "<START>"
END = "<END>"
MAX_LEN = 40

def load_model(path):
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    model = {}
    for key, options in raw.items():
        w1, w2 = key.split("\x01")
        model[(w1, w2)] = options  # list of [word, count]
    return model

def weighted_choice(options):
    words = [o[0] for o in options]
    weights = [o[1] for o in options]
    return random.choices(words, weights=weights, k=1)[0]

def generate_sentence(model):
    ctx = (START, START)
    words = []
    for _ in range(MAX_LEN):
        options = model.get(ctx)
        if not options:
            break
        nxt = weighted_choice(options)
        if nxt == END:
            break
        words.append(nxt)
        ctx = (ctx[1], nxt)
    return format_sentence(words)

def format_sentence(words):
    if not words:
        return ""
    fixed = []
    for w in words:
        if w == "i":
            w = "I"
        elif w == "i'm":
            w = "I'm"
        elif w == "i'll":
            w = "I'll"
        elif w == "i've":
            w = "I've"
        elif w == "i'd":
            w = "I'd"
        fixed.append(w)
    text = " ".join(fixed)
    text = text[0].upper() + text[1:]
    if text[-1] not in ".!?":
        text += "."
    return text

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    here = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(here, "trigram_model_top6.json")
    model = load_model(model_path)
    for i in range(1, n + 1):
        print(f"{i}. {generate_sentence(model)}")

if __name__ == "__main__":
    main()
