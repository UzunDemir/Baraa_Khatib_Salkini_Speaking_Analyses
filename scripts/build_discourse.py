import re, csv
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()
text_flat = re.sub(r'\s+', ' ', text).strip()
sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
raw_sentences = sentence_endings.split(text_flat)
sentences = [s.strip() for s in raw_sentences if s.strip()]

def find_example(phrase, min_len=20, max_len=140):
    plow = phrase.lower()
    best = None
    for s in sentences:
        sl = s.lower()
        if sl.startswith(plow):
            if min_len <= len(s) <= max_len:
                return s
            if best is None:
                best = s
    return best or "(пример не найден)"

# category -> list of (phrase, translation)
categories = {
    "Переход к новому шагу": [
        ("so let's go and", "итак, давайте перейдём и"),
        ("let's go and execute", "давайте перейдём и выполним"),
        ("now moving on to", "теперь переходим к"),
        ("so now let's go", "итак, теперь давайте"),
        ("let's start with the", "давайте начнём с"),
    ],
    "Демонстрация / показ примера": [
        ("as you can see", "как видите"),
        ("so as you can see", "итак, как видите"),
        ("so for example", "итак, например"),
        ("let's go and execute it", "давайте выполним это"),
    ],
    "Объяснение / переформулирование": [
        ("so that means", "это значит, что"),
        ("so that means we", "это значит, мы"),
        ("this is how", "вот как"),
        ("so this is the", "итак, это"),
        ("so this is how", "итак, вот как"),
    ],
    "Итог / завершение мысли": [
        ("so that's it", "вот и всё"),
        ("so that's why", "именно поэтому"),
        ("those are the", "это те"),
    ],
    "План действия / намерение": [
        ("we're going to", "мы собираемся / сейчас будем"),
        ("it's going to be", "это будет"),
        ("so we're going to go", "итак, сейчас мы перейдём"),
        ("so i'm going to", "итак, я собираюсь"),
    ],
    "Условие": [
        ("so if you go", "итак, если вы перейдёте"),
        ("now if you check", "теперь, если вы проверите"),
        ("if you go and", "если вы перейдёте и"),
    ],
    "Цель / порядок действий": [
        ("in order to", "для того чтобы"),
        ("so in order to", "итак, чтобы"),
    ],
    "Обращение / неформальное вступление": [
        ("all right", "хорошо / ладно"),
        ("all right my friends", "итак, друзья мои"),
    ],
    "Добавление / продолжение мысли": [
        ("and now we have", "и теперь у нас есть"),
        ("and with that we", "и с этим мы"),
        ("and of course", "и конечно"),
        ("so with that we have", "итак, с этим у нас есть"),
    ],
}

out = "/home/claude/sql_course/discourse_markers.md"
rows_for_anki = []
with open(out, "w", encoding="utf-8") as f:
    f.write("# Обороты речи спикера (discourse markers)\n\n")
    f.write("Готовые фразы-клише, сгруппированные по функции. Их можно использовать как есть в своей речи.\n\n")
    for cat, items in categories.items():
        f.write(f"## {cat}\n\n")
        f.write("| Фраза | Перевод | Пример из курса |\n|---|---|---|\n")
        for phrase, trans in items:
            ex = find_example(phrase)
            ex_disp = ex.replace("|", "/")
            f.write(f"| {phrase} | {trans} | {ex_disp} |\n")
            rows_for_anki.append((phrase, trans, ex, "Discourse: " + cat))
        f.write("\n")

print("saved", out)
print("total phrases:", len(rows_for_anki))

# save intermediate for reuse in anki step
import json
with open("/home/claude/sql_course/discourse_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows_for_anki, f, ensure_ascii=False, indent=2)
