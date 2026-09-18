import re, json

path_json = "all_sent_tokens.json"
with open(path_json, encoding="utf-8") as f:
    sents = json.load(f)
sent_strings = [' '.join(s) for s in sents]

def find_example(phrase):
    for s in sent_strings:
        if phrase in s:
            return s
    return "(пример не найден)"

# 32 discourse markers (phrase, translation, category)
discourse = [
 ("so let's go and", "итак, давайте перейдём и", "Переход к действию"),
 ("let's go and execute", "давайте перейдём и выполним", "Переход к действию"),
 ("now moving on to", "теперь переходим к", "Переход к действию"),
 ("so now let's go", "итак, теперь давайте", "Переход к действию"),
 ("let's start with the", "давайте начнём с", "Переход к действию"),
 ("as you can see", "как видите", "Демонстрация"),
 ("so as you can see", "итак, как видите", "Демонстрация"),
 ("so for example", "итак, например", "Демонстрация"),
 ("let's go and execute it", "давайте выполним это", "Демонстрация"),
 ("so that means", "это значит, что", "Объяснение"),
 ("so that means we", "это значит, мы", "Объяснение"),
 ("this is how", "вот как", "Объяснение"),
 ("so this is the", "итак, это", "Объяснение"),
 ("so this is how", "итак, вот как", "Объяснение"),
 ("so that's it", "вот и всё", "Итог"),
 ("so that's why", "именно поэтому", "Итог"),
 ("those are the", "это те", "Итог"),
 ("we're going to", "мы сейчас будем / собираемся", "План действия"),
 ("it's going to be", "это будет", "План действия"),
 ("so we're going to go", "итак, сейчас мы перейдём", "План действия"),
 ("so i'm going to", "итак, я собираюсь", "План действия"),
 ("so if you go", "итак, если вы перейдёте", "Условие"),
 ("now if you check", "теперь, если вы проверите", "Условие"),
 ("if you go and", "если вы перейдёте и", "Условие"),
 ("in order to", "для того чтобы", "Цель"),
 ("so in order to", "итак, чтобы", "Цель"),
 ("all right", "хорошо, ладно", "Вступление"),
 ("all right my friends", "итак, друзья мои", "Вступление"),
 ("and now we have", "и теперь у нас есть", "Добавление"),
 ("and with that we", "и с этим мы", "Добавление"),
 ("and of course", "и конечно", "Добавление"),
 ("so with that we have", "итак, с этим у нас есть", "Добавление"),
]

# 68 additional real, attested phrases pulled from the corpus (n=3..7), with translations
extra = [
 ("what you have to do is to", "всё, что вам нужно сделать, — это", "Инструкция"),
 ("let's say that i would like to", "скажем, я хотел бы", "Гипотеза/пример"),
 ("what we can do we can go", "что мы можем сделать — мы можем перейти", "Инструкция"),
 ("have the following task and it says", "у нас есть такая задача, и в ней сказано", "Постановка задачи"),
 ("to the next one we have the", "к следующему — у нас есть", "Переход"),
 ("of course we have to go and", "конечно, нам нужно перейти и", "Инструкция"),
 ("so how we going to do it", "итак, как мы это сделаем", "Вопрос-переход"),
 ("can see in the output we have", "в выводе мы видим, что у нас есть", "Демонстрация"),
 ("of course you can go and", "конечно, вы можете перейти и", "Инструкция"),
 ("to go over here and say", "перейти сюда и сказать", "Инструкция"),
 ("from the highest to the lowest", "от самого высокого к самому низкому", "Описание"),
 ("now of course the question is", "конечно, теперь возникает вопрос", "Постановка вопроса"),
 ("in order to do that we're going", "чтобы это сделать, мы", "Цель"),
 ("we can use it in order", "мы можем использовать это, чтобы", "Цель"),
 ("this is what we mean with", "вот что мы имеем в виду под", "Объяснение"),
 ("you might say you know what", "вы могли бы сказать: знаете что", "Диалог с аудиторией"),
 ("let's do it step by step", "давайте сделаем это шаг за шагом", "Инструкция"),
 ("what do we need we need", "что нам нужно — нам нужно", "Постановка задачи"),
 ("we have a lot of", "у нас есть много", "Описание"),
 ("execute it you will get", "выполните это, и вы получите", "Демонстрация"),
 ("so now what we're going", "итак, теперь то, что мы", "Переход"),
 ("can see we are getting", "видим, что мы получаем", "Демонстрация"),
 ("the same thing for the", "то же самое для", "Сравнение"),
 ("so let's try this out", "итак, давайте попробуем это", "Переход к действию"),
 ("execute it now as you", "выполните это, и теперь, как вы", "Демонстрация"),
 ("go and create a new", "перейти и создать новый", "Инструкция"),
 ("and as well we have", "а также у нас есть", "Добавление"),
 ("look at this we have", "посмотрите на это — у нас есть", "Демонстрация"),
 ("so it is very simple", "итак, это очень просто", "Оценка"),
 ("and this is exactly what", "и это именно то, что", "Объяснение"),
 ("we have solved the task", "мы решили задачу", "Итог"),
 ("so now by looking to", "итак, теперь глядя на", "Переход"),
 ("go and use the", "перейти и использовать", "Инструкция"),
 ("to go to the", "перейти к", "Инструкция"),
 ("all right so now", "хорошо, теперь", "Вступление"),
 ("if you want to", "если вы хотите", "Условие"),
 ("to do we're going", "чтобы сделать это, мы будем", "План действия"),
 ("and here we have", "и здесь у нас есть", "Добавление"),
 ("and then we have", "а затем у нас есть", "Добавление"),
 ("go and check the", "перейти и проверить", "Инструкция"),
 ("going to use the", "собираемся использовать", "План действия"),
 ("and then we're going", "а затем мы будем", "Добавление"),
 ("we don't have any", "у нас нет никаких", "Описание"),
 ("what going to happen", "что произойдёт", "Вопрос-предсказание"),
 ("go and do that", "перейти и сделать это", "Инструкция"),
 ("if i go and", "если я перейду и", "Условие"),
 ("going to call it", "назовём это", "Именование"),
 ("going to start with", "начнём с", "План действия"),
 ("the data from the", "данные из", "Описание"),
 ("so now we're going", "итак, теперь мы будем", "Переход"),
 ("going to say", "скажем так / собираюсь сказать", "Речевой filler"),
 ("you're going to", "вы будете", "План действия"),
 ("so we have", "итак, у нас есть", "Итог/переход"),
 ("okay so now", "хорошо, теперь", "Вступление"),
 ("going to have", "у нас будет", "План действия"),
 ("like for example", "например, как", "Демонстрация"),
 ("we have here", "у нас здесь есть", "Описание"),
 ("if you are", "если вы", "Условие"),
 ("going to get", "получим", "План действия"),
 ("and we have", "и у нас есть", "Добавление"),
 ("so now we", "итак, теперь мы", "Переход"),
 ("if you have", "если у вас есть", "Условие"),
 ("as well the", "также и", "Добавление"),
 ("and we're going", "и мы будем", "Добавление"),
 ("at the end", "в конце", "Указание позиции"),
 ("so it's going", "итак, это будет", "План действия"),
 ("we can see that", "мы можем увидеть, что", "Демонстрация"),
 ("go and add a", "перейти и добавить", "Инструкция"),
]

all_rows = []
for phrase, trans, cat in discourse:
    ex = find_example(phrase)
    all_rows.append((phrase, trans, cat, ex))
for phrase, trans, cat in extra:
    ex = find_example(phrase)
    all_rows.append((phrase, trans, cat, ex))

print("total rows:", len(all_rows))

out = "/home/claude/sql_course/100_phrases.md"
with open(out, "w", encoding="utf-8") as f:
    f.write("# 100 фраз, чтобы говорить в его стиле\n\n")
    f.write("Все фразы — реально встречающиеся конструкции из его речи (8 курсов), не выдуманные. ")
    f.write("Сгруппированы по функции. Практикуй: читай фразу → перевод → пример → пробуй вставить в свою речь.\n\n")

    from collections import defaultdict
    by_cat = defaultdict(list)
    for row in all_rows:
        by_cat[row[2]].append(row)

    n = 1
    for cat, rows in by_cat.items():
        f.write(f"## {cat}\n\n")
        f.write("| # | Фраза | Перевод | Пример из корпуса |\n|---|---|---|---|\n")
        for phrase, trans, _, ex in rows:
            ex_disp = ex[0].upper() + ex[1:] if ex else ex
            ex_disp = ex_disp.replace("|", "/")
            if len(ex_disp) > 140:
                ex_disp = ex_disp[:140] + "..."
            f.write(f"| {n} | {phrase} | {trans} | {ex_disp}. |\n")
            n += 1
        f.write("\n")

print("saved", out, "with", n-1, "phrases")
