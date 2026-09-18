# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                 PageBreak, HRFlowable, KeepTogether)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))

styles = getSampleStyleSheet()

title_style = ParagraphStyle('TitleRU', parent=styles['Title'], fontName='DejaVuSans-Bold', fontSize=24, leading=30, alignment=TA_CENTER, spaceAfter=10)
subtitle_style = ParagraphStyle('SubtitleRU', parent=styles['Normal'], fontName='DejaVuSans-Oblique', fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceAfter=6)
meta_style = ParagraphStyle('MetaRU', parent=styles['Normal'], fontName='DejaVuSans', fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor('#777777'))

h1 = ParagraphStyle('H1RU', parent=styles['Heading1'], fontName='DejaVuSans-Bold', fontSize=17, leading=21, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#1A1A1A'))
h2 = ParagraphStyle('H2RU', parent=styles['Heading2'], fontName='DejaVuSans-Bold', fontSize=13, leading=17, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#2C3E50'))
body = ParagraphStyle('BodyRU', parent=styles['Normal'], fontName='DejaVuSans', fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
body_small = ParagraphStyle('BodySmallRU', parent=styles['Normal'], fontName='DejaVuSans', fontSize=8.5, leading=12, alignment=TA_LEFT)
quote_style = ParagraphStyle('QuoteRU', parent=body, fontName='DejaVuSans-Oblique', leftIndent=14, textColor=colors.HexColor('#333333'))
toc_style = ParagraphStyle('TOCRU', parent=styles['Normal'], fontName='DejaVuSans', fontSize=11, leading=20)
caption_style = ParagraphStyle('CaptionRU', parent=styles['Normal'], fontName='DejaVuSans-Oblique', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor('#666666'), spaceAfter=14)
finding_style = ParagraphStyle('FindingRU', parent=body, leftIndent=10, spaceBefore=4, spaceAfter=10)

def table_style_default():
    return TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F7FA')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])

cell_header_style = ParagraphStyle('CellHeaderRU', parent=styles['Normal'], fontName='DejaVuSans-Bold', fontSize=8.5, leading=11, textColor=colors.white)
cell_body_style = ParagraphStyle('CellBodyRU', parent=styles['Normal'], fontName='DejaVuSans', fontSize=8.5, leading=11)

def wrap_table_data(data):
    """Convert raw string table rows into Paragraph-wrapped cells so text wraps within column width."""
    wrapped = []
    for row_idx, row in enumerate(data):
        style = cell_header_style if row_idx == 0 else cell_body_style
        wrapped.append([Paragraph(str(cell), style) for cell in row])
    return wrapped

story = []

# ============ TITLE PAGE ============
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Речевой профиль спикера", title_style))
story.append(Paragraph("Baraa Khatib Salkini", title_style))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Лингвистический анализ 8 обучающих курсов и live-стримов на английском:<br/>"
                        "почему его речь исключительно легко воспринимается на слух", subtitle_style))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("762 323 слова &middot; 52 583 предложения &middot; 5 749 уникальных слов<br/>"
                        "SQL &middot; Python &middot; Power BI &middot; Databricks &middot; Data Architecture", meta_style))
story.append(Spacer(1, 6*cm))
story.append(Paragraph("Исследование подготовлено Demir &middot; сентябрь 2026", meta_style))
story.append(PageBreak())

# ============ TOC ============
story.append(Paragraph("Оглавление", h1))
toc_items = [
    "1. Предисловие — как и почему возникло это исследование",
    "2. Методология",
    "3. Ключевые находки",
    "&nbsp;&nbsp;&nbsp;3.1. Узкий словарь как объяснение понятности",
    "&nbsp;&nbsp;&nbsp;3.2. Правило 80/20: 207 слов = 80% речи",
    "&nbsp;&nbsp;&nbsp;3.3. Закон Ципфа и формульность речи",
    "&nbsp;&nbsp;&nbsp;3.4. Речевой отпечаток: что общее для всех курсов",
    "&nbsp;&nbsp;&nbsp;3.5. Скелет построения предложения",
    "&nbsp;&nbsp;&nbsp;3.6. We vs I: спикер меняет личность в зависимости от формата",
    "&nbsp;&nbsp;&nbsp;3.7. Recorded vs live: команды против вопросов",
    "4. Визуальная сводка",
    "5. Коммуникационный набор (практическое ядро)",
    "6. Генератор речи спикера",
    "7. Приложения — полный список материалов",
]
for item in toc_items:
    story.append(Paragraph(item, toc_style))
story.append(PageBreak())

# ============ 1. FOREWORD ============
story.append(Paragraph("1. Предисловие", h1))
story.append(Paragraph(
    "Я свободно читаю техническую документацию на английском — библиотеки, фреймворки, статьи по ML и Data Science "
    "не вызывают затруднений вообще. А вот с восприятием речи на слух всё было иначе: сколько бы я ни слушал разных "
    "спикеров, распознавание давалось с большим трудом.", body))
story.append(Paragraph(
    "Я решил закрыть этот пробел и начал целенаправленно тренировать listening — на знакомых темах (SQL, Python, "
    "data engineering), чтобы контекст помогал, а не мешал. Перепробовал нескольких спикеров: где-то было чуть легче, "
    "где-то так же тяжело, как и раньше.", body))
story.append(Paragraph(
    "Всё изменилось, когда я наткнулся на курсы <b>Baraa Khatib Salkini</b>. Я понимал его речь почти на 100% — "
    "без постоянных перемоток и повторов. Такого не было ни разу до этого.", body))
story.append(Paragraph(
    "Это не могло быть случайностью, и я решил не просто пользоваться удачным совпадением, а разобраться, что именно "
    "делает его речь настолько понятной — не на уровне ощущений «хорошая дикция», а на уровне цифр: словарь, частоты, "
    "синтаксис, построение фраз.", body))
story.append(Paragraph(
    "Так родилось это исследование — 8 транскрипций, 762 тысячи слов, и попытка препарировать речь одного конкретного "
    "человека настолько подробно, чтобы понять механику его ясности и перенять её в собственную речь.", body))
story.append(Spacer(1, 0.3*cm))

# ============ 2. METHODOLOGY ============
story.append(Paragraph("2. Методология", h1))
story.append(Paragraph(
    "Материал: транскрипты 8 курсов и стримов — SQL Full Course, Python Full Course, Power BI Data Modeling "
    "(2 курса), Databricks Live Bootcamp (Day 1 и Day 2), Data Architecture (2 live-стрима).", body))

meth_table_data = [
    ["Метод", "Что даёт"],
    ["Токенизация + частотный анализ", "Общий словарный запас, частота слов, словосочетаний (n-граммы 2-10 слов)"],
    ["POS-разметка (spaCy)", "Частота слов по частям речи по отдельности"],
    ["Анализ Парето (80/20)", "Минимальный набор слов, покрывающий 80% речи — по каждой части речи"],
    ["Закон Ципфа", "Проверка, насколько формульно распределены частоты слов"],
    ["Марковские цепи (n=3)", "Модель построения предложений: начала, окончания, генератор новых фраз"],
    ["Межфайловое сравнение", "Что общее для спикера во всех темах (речевой отпечаток), а что специфично для темы"],
    ["Стилометрия (TTR, местоимения, модальность)", "Сравнение live vs recorded форматов"],
]
t = Table(wrap_table_data(meth_table_data), colWidths=[6.5*cm, 10*cm])
t.setStyle(table_style_default())
story.append(t)
story.append(PageBreak())

# ============ 3. KEY FINDINGS ============
story.append(Paragraph("3. Ключевые находки", h1))

story.append(Paragraph("3.1. Узкий словарь как объяснение понятности", h2))
story.append(Paragraph(
    "Весь его словарь на 762 323 слова — <b>5 749 уникальных слов</b>. Отношение уникальных слов к общему объёму "
    "текста (type-token ratio) крайне низкое — заметно ниже, чем у типичной спонтанной речи носителя языка на "
    "таком же объёме. Иными словами, он не расширяет словарь бесконечно, а сознательно (или интуитивно) работает "
    "в рамках ограниченного, повторяющегося набора конструкций.", finding_style))
story.append(Paragraph(
    "Для человека, который воспринимает английский на слух не как носитель, это ключевой фактор: меньше "
    "незнакомых и редких слов — меньше точек, где распознавание речи срывается.", finding_style))

story.append(Paragraph("3.2. Правило 80/20: 207 слов = 80% речи", h2))
story.append(Paragraph(
    "Из 5 749 уникальных слов всего <b>207 (3,6%)</b> покрывают 80% всего, что он говорит. Похожая картина "
    "внутри каждой части речи: 136 из 2062 глаголов (6,6%) дают 80% всех глагольных употреблений; 303 из 3048 "
    "существительных (9,9%); 107 из 988 прилагательных (10,8%). Грамматический костяк ещё компактнее: 7 местоимений, "
    "4 артикля, 1 сочинительный союз («and») покрывают 80% своих категорий практически полностью.", finding_style))

story.append(Paragraph("3.3. Закон Ципфа и формульность речи", h2))
story.append(Paragraph(
    "Распределение частота-ранг слов в его речи ложится на почти идеальную прямую в лог-лог координатах — "
    "классическое поведение по Ципфу, без аномалий и искусственных выбросов. Это подтверждает: узость и "
    "формульность словаря — не артефакт подсчёта, а системная характеристика его речи.", finding_style))

story.append(Paragraph("3.4. Речевой отпечаток: что общее для всех курсов", h2))
story.append(Paragraph(
    "76 слов входят в топ-150 абсолютно каждого из 8 файлов независимо от темы (SQL, Python, Power BI, Databricks, "
    "архитектура данных) — это подлинное ядро его личного стиля: <i>so, we, going, now, go, like, let's, here, "
    "order, say, see...</i> 53 биграммы и 41 триграмма демонстрируют ту же устойчивость минимум в 6 из 8 файлов. "
    "Конструкции вроде «so let's go», «as you can see», «in order to» — не случайность одного курса, а системная "
    "привычка речи.", finding_style))

story.append(Paragraph("3.5. Скелет построения предложения", h2))
story.append(Paragraph(
    "Построена марковская модель (n=3) на всех 52 583 предложениях. На длинных фразах (7-10 слов) доминирует "
    "практически одна и та же растянутая конструкция — <b>«what we're going to do, we're going to...»</b> — "
    "сотни дословных повторений. С ростом длины фразы число уникальных вариантов резко падает: у него буквально "
    "несколько «рельсов», по которым едет почти вся речь.", finding_style))

story.append(Paragraph("3.6. We vs I: спикер меняет личность в зависимости от формата", h2))
story.append(Paragraph(
    "Самая неожиданная находка. В <b>записанных курсах</b> местоимение «I» встречается редко (7,8–17 на 1000 слов), "
    "а «we» доминирует (37–51) — классическая инклюзивная педагогическая позиция: «мы вместе идём по материалу». "
    "В <b>live-стримах</b> — почти зеркальный разворот: «I» взлетает до 37–44 (в 3–5 раз выше), а «we» падает "
    "до 12–18. В записи он ведёт группу, в live — говорит от своего лица как практик, который думает вслух.", finding_style))

story.append(Paragraph("3.7. Recorded vs live: команды против вопросов", h2))
story.append(Paragraph(
    "В записанных курсах доля предложений-команд («let's create», «go and check») — 2,4–2,8%, а вопросов "
    "мало (3,3–5,1%). В live-стримах картина обратная: вопросов до 10,5% (Databricks Day 2), а команд почти "
    "вдвое меньше (0,76–1,23%). Записанный курс — сценарий «показал → сделай сам»; live — рассуждение вслух "
    "и диалог с самим собой.", finding_style))

story.append(PageBreak())

# ============ 4. VISUAL SUMMARY ============
story.append(Paragraph("4. Визуальная сводка", h1))

story.append(Paragraph("Облако слов (топ-150 значимых слов, весь корпус)", h2))
story.append(Image("wordcloud.png", width=15.5*cm, height=15.5*cm*1380/2430))
story.append(Paragraph("Рис. 1 — облако наиболее частотных содержательных слов across всех 8 курсов", caption_style))

story.append(Paragraph("Тепловая карта: частота слов по курсам", h2))
story.append(Image("heatmap.png", width=14*cm, height=14*cm*1500/1650))
story.append(Paragraph("Рис. 2 — частота топ-25 слов на 1000 слов текста, в разрезе по каждому из 8 курсов. "
                        "Хорошо видно всплеск «i'm» именно в live-форматах (Databricks, Data Architecture)", caption_style))
story.append(PageBreak())

story.append(Paragraph("Сеть словосочетаний", h2))
story.append(Image("ngram_network.png", width=14.5*cm, height=14.5*cm))
story.append(Paragraph("Рис. 3 — топ-40 слов и связи между ними (биграммы). Узлы «going/we/data/order/let's» "
                        "— центральные точки, вокруг которых строится вся речь", caption_style))
story.append(PageBreak())

story.append(Paragraph("Дерево построения предложения (превью, первые уровни)", h2))
story.append(Image("tree_starter_preview.png", width=16*cm, height=16*cm*3200/2334))
story.append(Paragraph("Рис. 4 — марковская цепь первых 4-7 слов предложения, топ-2/3 продолжения на развилке. "
                        "Полная версия в приложении sentence_starter_tree_deep.png", caption_style))
story.append(PageBreak())

# ============ 5. COMMUNICATION KIT ============
story.append(Paragraph("5. Коммуникационный набор (практическое ядро)", h1))
story.append(Paragraph(
    "Синтез всего исследования в формате, пригодном для ежедневной практики: словарь, начала и окончания "
    "предложений, обороты речи, переключатель We/I, шаблоны для заполнения и план отработки. Полная версия — "
    "в приложении communication_kit.md.", body))

story.append(Paragraph("Грамматический каркас (выучить первым)", h2))
kit_grammar = [
    ["Категория", "Слова"],
    ["Местоимения (7)", "we, it, you, i, 's, what, that"],
    ["Вспом. глаголы (7)", "is, have, can, do, are, 's, 're"],
    ["Артикли (4)", "the, this, a, that"],
    ["Предлоги (10)", "in, of, for, to, with, like, from, as, on, about"],
    ["Союз (соч., 1)", "and"],
    ["Союзы (подч., 5)", "if, that, how, because, where"],
]
t = Table(wrap_table_data(kit_grammar), colWidths=[4.5*cm, 12*cm])
t.setStyle(table_style_default())
story.append(t)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("Переключатель We / I", h2))
kit_wei = [
    ["Контекст", "Использовать", "Почему"],
    ["Обучаешь, ведёшь по шагам", "WE", "снижает дистанцию, «мы вместе идём по материалу»"],
    ["Делишься мнением/опытом", "I", "звучит как эксперт, а не ведущий группы"],
    ["Даёшь инструкцию", "WE + повелит.", "мягкая команда без давления («let's go and...»)"],
    ["Рассуждаешь вслух", "I + вопрос", "имитация живого размышления («so what does that mean?»)"],
]
t = Table(wrap_table_data(kit_wei), colWidths=[5*cm, 3.5*cm, 8*cm])
t.setStyle(table_style_default())
story.append(t)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("Шаблоны для заполнения", h2))
templates = [
    "So let's go and [verb] the [noun].",
    "Now what we're going to do is [verb] the [noun].",
    "So this is how you [verb] a [noun].",
    "As you can see, we have [noun] here.",
    "In order to [verb] the [noun], we need to [verb2].",
]
for t_ in templates:
    story.append(Paragraph("• " + t_, body_small))
story.append(PageBreak())

# ============ 6. GENERATOR ============
story.append(Paragraph("6. Генератор речи спикера", h1))
story.append(Paragraph(
    "На основе триграммной марковской модели (93 211 контекстов, топ-6 продолжений на каждый) собран рабочий "
    "генератор — <b>generate_speaker_sentences.py</b> + <b>trigram_model_top6.json</b>. Запускается локально:", body))
story.append(Paragraph("python3 generate_speaker_sentences.py 20",
                        ParagraphStyle('code', parent=body_small, fontName='DejaVuSans',
                                       backColor=colors.HexColor('#F0F0F0'), leftIndent=8,
                                       spaceBefore=4, spaceAfter=10)))
story.append(Paragraph("Примеры реального вывода:", body))
examples = [
    "So that means the output.",
    "So now if you go with the same thing we do the data model.",
    "So let's have a new data model.",
    "And now if you go with the same thing we do the data model.",
]
for ex in examples:
    story.append(Paragraph("« " + ex + " »", quote_style))
story.append(Paragraph(
    "Стресс-тест: 500 генераций подряд — 0 сбоев, 0 пустых результатов. Генератор пригоден для ежедневной "
    "тренировки: читать вслух сгенерированные фразы — упражнение на воспроизведение его синтаксического скелета.", body))
story.append(PageBreak())

# ============ 7. APPENDICES ============
story.append(Paragraph("7. Приложения — полный список материалов", h1))
story.append(Paragraph("Все файлы, созданные в ходе исследования, переданы отдельно вместе с этим отчётом.", body))

appendix_data = [
    ["Файл", "Содержание"],
    ["8 файлов *_report.md", "Полный частотный анализ по каждому из 8 курсов отдельно: слова, словосочетания (n=2-10), обороты, повторяющиеся предложения"],
    ["ngrams_2_10_report.md", "Частотность фраз длиной от 2 до 10 слов по всему объединённому корпусу"],
    ["speaker_fingerprint_report.md", "Речевой отпечаток — слова/фразы, общие для всех 8 курсов независимо от темы"],
    ["pos_frequency_report.md", "Частота слов по каждой части речи отдельно"],
    ["core_vocabulary_pareto.md", "Полные списки слов 80/20 по каждой части речи с накопительным %"],
    ["discourse_markers.md", "32 оборота речи, сгруппированные по функции, с переводом и примерами"],
    ["100_phrases.md, 100_phrases_v2.md", "200 реальных речевых конструкций (без повторов) с переводом и примерами из корпуса"],
    ["deep_speaker_analysis.md", "Сравнение live vs recorded: местоимения, вопросы/команды, модальность, длина предложений"],
    ["communication_kit.md", "Итоговый практический набор: словарь + начала + обороты + окончания + шаблоны + план"],
    ["anki_deck.csv", "141 карточка для интервального повторения (discourse markers + словарь)"],
    ["generate_speaker_sentences.py, trigram_model_top6.json", "Рабочий генератор фраз в его стиле"],
    ["wordcloud.png, heatmap.png, ngram_network.png", "Визуализации: облако слов, тепловая карта, граф словосочетаний"],
    ["sentence_starter_tree*.png, sentence_ending_tree.png", "Деревья построения и завершения предложений (полное разрешение)"],
]
t = Table(wrap_table_data(appendix_data), colWidths=[6.5*cm, 10*cm])
t.setStyle(table_style_default())
story.append(t)

story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="100%", color=colors.HexColor('#CCCCCC')))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Практический итог исследования: понятность речи Baraa Khatib Salkini для не-носителя языка объясняется "
    "не случайностью и не «хорошей дикцией» как таковой, а измеримой структурной особенностью — узким, "
    "дисциплинированным словарём и предсказуемыми синтаксическими конструкциями, которые системно повторяются "
    "вне зависимости от темы. Материалы этого исследования переводят это наблюдение в конкретный тренировочный "
    "план.", body))

doc = SimpleDocTemplate(
    "/home/claude/sql_course/Baraa_Speaker_Research_Report.pdf",
    pagesize=A4,
    topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm,
    title="Речевой профиль спикера — Baraa Khatib Salkini",
    author="Demir"
)
doc.build(story)
print("PDF built successfully")
