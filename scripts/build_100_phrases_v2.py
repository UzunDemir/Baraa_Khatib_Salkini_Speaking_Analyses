import json

with open("all_sent_tokens.json", encoding="utf-8") as f:
    sents = json.load(f)
sent_strings = [' '.join(s) for s in sents]

def find_example(phrase):
    for s in sent_strings:
        if phrase in s:
            return s
    return "(пример не найден)"

# (phrase, translation, category)
phrases = [
 ("going to show you how i usually do it", "покажу вам, как обычно делаю это", "Демонстрация"),
 ("products where the price is higher than the average", "товары, у которых цена выше средней", "Пример-контент"),
 ("so now back to our example where we have", "итак, вернёмся к нашему примеру, где у нас есть", "Возврат к примеру"),
 ("so now let me show you what i mean", "теперь покажу, что я имею в виду", "Объяснение"),
 ("now the next step is that", "следующий шаг — это", "План действия"),
 ("have to group up the data by the", "нужно сгруппировать данные по", "Инструкция"),
 ("now what else do we have we have", "что ещё у нас есть — у нас есть", "Перечисление"),
 ("if the score is greater or equal to", "если значение больше или равно", "Условие"),
 ("they have nothing to do with each others", "они никак не связаны друг с другом", "Объяснение"),
 ("now let's have a quick look to the", "давайте быстро взглянем на", "Переход к действию"),
 ("let's go back to scale in order", "давайте вернёмся к масштабу, чтобы", "Возврат к теме"),
 ("with that you have learned how to", "таким образом, вы научились", "Итог обучения"),
 ("the first name and the last name", "имя и фамилия", "Описание"),
 ("so that's all about the", "вот и всё про", "Итог"),
 ("now what you can do you can", "теперь то, что вы можете сделать — вы можете", "Инструкция"),
 ("go and copy the whole thing and", "скопировать всё целиком и", "Инструкция"),
 ("will get the exact same results so", "получите точно такой же результат, так что", "Демонстрация"),
 ("going to leave it as it is", "оставлю это как есть", "Решение по ходу"),
 ("this is another way on how to", "вот ещё один способ, как", "Альтернатива"),
 ("so let's understand what this means now", "давайте теперь разберёмся, что это значит", "Объяснение"),
 ("so let's see how we can", "давайте посмотрим, как мы можем", "Переход к действию"),
 ("from the lowest to the highest", "от самого низкого к самому высокому", "Описание"),
 ("if you do it like this", "если вы сделаете это так", "Условие"),
 ("go and give it a name", "перейти и дать этому имя", "Инструкция"),
 ("to be very simple we're going", "чтобы было очень просто, мы", "Упрощение"),
 ("so the first one going to", "итак, первый будет", "Перечисление"),
 ("execute it so now in the", "выполнить это, и теперь в", "Демонстрация"),
 ("go and get rid of the", "перейти и избавиться от", "Инструкция"),
 ("the total number of orders so", "общее количество заказов, так что", "Описание результата"),
 ("go and change the data type", "перейти и изменить тип данных", "Инструкция"),
 ("find the total sales for each", "найти общую сумму продаж для каждого", "Постановка задачи"),
 ("since we are talking about the", "раз уж мы говорим о", "Связка тем"),
 ("at the start and at the", "в начале и в", "Описание позиции"),
 ("let's check the syntax of the", "давайте проверим синтаксис", "Переход к действию"),
 ("going to talk about the", "поговорим о", "Анонс темы"),
 ("now we come to the", "теперь мы подходим к", "Переход"),
 ("now let's move to the", "теперь давайте перейдём к", "Переход к действию"),
 ("go and sort the data", "перейти и отсортировать данные", "Инструкция"),
 ("and i can tell you", "и я могу вам сказать", "Личное мнение"),
 ("all right friends so now", "хорошо, друзья, теперь", "Вступление"),
 ("the first thing that we", "первое, что мы", "Перечисление"),
 ("and put it in the", "и поместить это в", "Инструкция"),
 ("it makes no sense to", "нет смысла", "Оценка"),
 ("going to learn how to", "научимся, как", "Анонс темы"),
 ("but in the other hand", "но, с другой стороны", "Контраст"),
 ("have to make sure that", "нужно убедиться, что", "Инструкция"),
 ("we are not done yet", "мы ещё не закончили", "Продолжение"),
 ("can see it's very simple", "видите, это очень просто", "Оценка"),
 ("this is one of the", "это один из", "Описание"),
 ("the data based on the", "данные на основе", "Описание"),
 ("so my friends this is", "итак, друзья, это", "Вступление"),
 ("to be really hard to", "будет действительно сложно", "Оценка сложности"),
 ("can see it is", "видите, это", "Демонстрация"),
 ("and so on so", "и так далее, так что", "Перечисление"),
 ("on the left side", "с левой стороны", "Указание позиции"),
 ("i'm just going to", "я просто собираюсь", "План действия"),
 ("on the right side", "с правой стороны", "Указание позиции"),
 ("that's it let's go", "вот и всё, давайте перейдём", "Итог-переход"),
 ("you don't have to", "вам не нужно", "Отсутствие необходимости"),
 ("of course if you", "конечно, если вы", "Условие"),
 ("we have only one", "у нас есть только один", "Описание"),
 ("we have as well", "у нас также есть", "Добавление"),
 ("and stuff like that", "и тому подобное", "Обобщение"),
 ("the end of the", "конец", "Указание позиции"),
 ("will not go and", "не будем", "Отрицание плана"),
 ("i don't want to", "я не хочу", "Личное мнение"),
 ("that's why we have", "именно поэтому у нас есть", "Причинно-следств."),
 ("to go with the", "пойти с", "Выбор варианта"),
 ("this is of course", "это, конечно,", "Оценка"),
 ("at the same time", "в то же время", "Связка"),
 ("we are using the", "мы используем", "Описание действия"),
 ("the name of the", "имя/название", "Описание"),
 ("we have like a", "у нас есть что-то вроде", "Описание"),
 ("this is going to", "это будет", "Предсказание"),
 ("to be the", "быть", "Служебная связка"),
 ("so we are", "итак, мы", "Связка"),
 ("and if you", "и если вы", "Условие"),
 ("we will get", "мы получим", "Предсказание результата"),
 ("it going to", "это будет", "Предсказание"),
 ("it is not", "это не", "Отрицание"),
 ("we want to", "мы хотим", "Намерение"),
 ("see we have", "видим, у нас есть", "Демонстрация"),
 ("this is a", "это", "Описание"),
 ("can see the", "видим", "Демонстрация"),
 ("let me just", "позвольте мне просто", "Вступление к действию"),
 ("that we are", "что мы", "Связка"),
 ("what is the", "что такое / какой", "Вопрос"),
 ("to get the", "чтобы получить", "Цель"),
 ("so now if", "итак, теперь если", "Условие-переход"),
 ("and we can", "и мы можем", "Добавление"),
 ("so we can", "итак, мы можем", "Связка-возможность"),
 ("and then the", "а затем", "Последовательность"),
 ("now in order", "теперь, чтобы", "Цель"),
 ("you have a", "у вас есть", "Описание"),
 ("i don't know", "я не знаю", "Личное мнение"),
 ("we have two", "у нас есть два", "Описание"),
 ("let's go back to sql in order", "давайте вернёмся к sql, чтобы", "Возврат к теме"),
 ("all what you have to do is to", "всё, что вам нужно сделать, это", "Инструкция"),
 ("the customer id", "id клиента", "Описание"),
 ("this going to", "это будет", "Предсказание"),
]

print("total phrases prepared:", len(phrases))

out = "/home/claude/sql_course/100_phrases_v2.md"
from collections import defaultdict
by_cat = defaultdict(list)
for phrase, trans, cat in phrases:
    ex = find_example(phrase)
    by_cat[cat].append((phrase, trans, ex))

with open(out, "w", encoding="utf-8") as f:
    f.write("# 100 фраз (часть 2) — новые, не пересекаются с первой сотней\n\n")
    f.write("Так же, как и первая сотня — реальные конструкции из объединённого корпуса всех 8 курсов, без повторов с прошлым списком.\n\n")
    n = 1
    for cat, rows in by_cat.items():
        f.write(f"## {cat}\n\n")
        f.write("| # | Фраза | Перевод | Пример из корпуса |\n|---|---|---|---|\n")
        for phrase, trans, ex in rows:
            ex_disp = ex[0].upper() + ex[1:] if ex else ex
            ex_disp = ex_disp.replace("|", "/")
            if len(ex_disp) > 140:
                ex_disp = ex_disp[:140] + "..."
            f.write(f"| {n} | {phrase} | {trans} | {ex_disp}. |\n")
            n += 1
        f.write("\n")

print("saved", out, "phrases written:", n-1)
