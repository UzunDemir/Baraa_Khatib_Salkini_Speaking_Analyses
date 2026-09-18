import re, csv, json
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()
text_flat = re.sub(r'\s+', ' ', text).strip()
sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
raw_sentences = sentence_endings.split(text_flat)
sentences = [s.strip() for s in raw_sentences if s.strip()]

def find_example_word(word, min_len=15, max_len=130):
    pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    best=None
    for s in sentences:
        if pattern.search(s):
            if min_len <= len(s) <= max_len:
                return s
            if best is None:
                best = s
    return best or "(пример не найден)"

# general (non-SQL-domain) vocabulary with translations
vocab = {
    "like": "как; нравится (в речи часто как слово-паразит)",
    "order": "в 'in order to' — для того чтобы",
    "use": "использовать",
    "using": "используя",
    "start": "начинать",
    "example": "пример",
    "check": "проверять",
    "means": "означает",
    "next": "следующий",
    "inside": "внутри",
    "new": "новый",
    "step": "шаг",
    "total": "итоговый, общий",
    "last": "последний",
    "find": "находить",
    "another": "другой",
    "everything": "всё",
    "different": "другой, отличающийся",
    "understand": "понимать",
    "really": "действительно, реально",
    "simple": "простой",
    "create": "создавать",
    "task": "задача",
    "lot": "много (a lot)",
    "call": "называть; вызывать",
    "exactly": "точно, именно",
    "result": "результат",
    "always": "всегда",
    "end": "конец",
    "group": "группа; группировать",
    "main": "главный, основной",
    "add": "добавлять",
    "important": "важный",
    "type": "тип",
    "multiple": "множественный, несколько",
    "something": "что-то",
    "whole": "весь, целый",
    "key": "ключ; ключевой",
    "case": "случай",
    "following": "следующий",
    "anything": "что-либо",
    "side": "сторона",
    "equal": "равный",
    "stuff": "вещи, всякое (разговорное)",
    "happen": "происходить",
    "put": "класть, помещать",
    "year": "год",
    "maybe": "может быть",
    "view": "вид; представление",
    "left": "левый; оставшийся",
    "since": "с тех пор как; так как",
    "instead": "вместо",
    "whether": "ли (в косвенных вопросах)",
    "big": "большой",
    "usually": "обычно",
    "part": "часть",
    "highest": "самый высокий",
    "called": "называемый",
    "many": "много (с исчисляемыми)",
    "done": "сделано, готово",
    "change": "менять; изменение",
    "nice": "хороший, приятный",
    "write": "писать",
    "might": "может (возможность)",
    "moving": "переходя, двигаясь",
    "show": "показывать",
    "give": "давать",
    "friends": "друзья (обращение)",
    "saying": "говоря",
    "way": "способ, путь",
    "zero": "ноль",
    "day": "день",
    "cannot": "не могу/не может",
    "details": "детали",
    "still": "всё ещё",
    "specify": "указывать, задавать",
    "types": "типы",
    "filter": "фильтровать",
    "build": "строить, создавать",
    "used": "использованный; привычный (used to)",
    "remove": "удалять",
    "level": "уровень",
    "together": "вместе",
    "without": "без",
    "format": "формат",
    "sure": "уверенный; конечно",
    "back": "назад",
    "comes": "приходит",
    "top": "верхний, топ",
    "working": "работающий, работая",
    "compare": "сравнивать",
    "third": "третий",
    "correct": "правильный",
    "sort": "сортировать; вид",
    "full": "полный",
    "previous": "предыдущий",
    "keep": "держать, продолжать",
    "higher": "выше",
    "must": "должен",
    "error": "ошибка",
    "count": "считать; количество",
    "matching": "совпадающий",
    "already": "уже",
    "work": "работать; работа",
    "try": "пробовать",
    "question": "вопрос",
    "ask": "спрашивать",
    "writing": "написание, письмо",
    "specific": "конкретный",
}

anki_rows = []

# discourse markers
with open("/home/claude/sql_course/discourse_rows.json", encoding="utf-8") as f:
    discourse_rows = json.load(f)
for phrase, trans, ex, tag in discourse_rows:
    anki_rows.append([phrase, trans, ex, tag])

# vocabulary
for w, trans in vocab.items():
    ex = find_example_word(w)
    anki_rows.append([w, trans, ex, "Vocabulary"])

out_csv = "/home/claude/sql_course/anki_deck.csv"
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Front", "Back", "Example", "Tag"])
    for row in anki_rows:
        writer.writerow(row)

print("rows:", len(anki_rows))
print("saved:", out_csv)
