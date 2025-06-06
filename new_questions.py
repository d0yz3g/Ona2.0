from typing import Dict, List, Union, Tuple, Any, Optional
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Демо-вопросы для первоначального знакомства
DEMO_QUESTIONS = [
    {
        "id": "name",
        "text": "Как тебя зовут?",
        "type": "text"
    },
    {
        "id": "age",
        "text": "Сколько тебе лет?",
        "type": "text"
    },
    {
        "id": "birthdate",
        "text": "Какая у тебя дата рождения? (формат: ДД.ММ.ГГГГ)",
        "type": "text"
    },
    {
        "id": "birthplace",
        "text": "Где ты родился/родилась? (город, страна)",
        "type": "text"
    },
    {
        "id": "timezone",
        "text": "В каком часовом поясе ты находишься? (например, UTC+3 для Москвы)",
        "type": "text"
    }
]

# Тест 2.0 - 34 вопроса из файла test2.0 с вариантами ответов и интерпретациями
VASINI_QUESTIONS = [
    {
        "id": "vasini_1",
        "text": "Что ты чувствуешь, когда смотришь в своё будущее?",
        "type": "choice",
        "options": {
            "A": "Воодушевление. Будущее манит как архитектура нового мира",
            "B": "Напряжение. Я не хочу думать о том, чего ещё нет",
            "C": "Конкретику. Я мыслю шагами, а не образами",
            "D": "Привязанность к настоящему. Я живу здесь и сейчас"
        },
        "interpretations": {
            "A": "Ты действуешь из будущего, а не из настоящего. Ты не фантазируешь — ты проектируешь. Ты не ждёшь вдохновения — ты уже живёшь в мире, который другие только начинают воображать. Это встроенная функция прогностики, а не идеализм. Твоё «завтра» — это топливо «сегодня».",
            "B": "У тебя защитный фильтр от неопределённости. Будущее кажется слишком зыбким — и ты предпочитаешь реальные точки опоры. Это не слабость, а адаптивный механизм к хаосу. Но он отключает дальнее зрение, если не перезагрузить внутреннюю безопасную среду.",
            "C": "У тебя мышление системного исполнителя. Не образы, а действия. Не фантазии, а модели. Ты способна строить мосты — но только если знаешь, куда они ведут. Это фокус на процессе, а не на горизонте. Это инженер внутри архитектора.",
            "D": "У тебя дом в настоящем. Ты живёшь моментом и не ускользаешь в симуляции будущего. В этом сила, если ты создаёшь глубину здесь. Но это может стать якорем, если избежать будущего — это способ спрятаться от необходимости роста."
        }
    },
    {
        "id": "vasini_2",
        "text": "Как в тебе рождаются идеи?",
        "type": "choice",
        "options": {
            "A": "Я скачиваю их как поток — будто через меня кто-то говорит",
            "B": "Они приходят через образы, метафоры, цветовые связи",
            "C": "Я вижу структуры, которые соединяют несвязанное",
            "D": "Я беру идею из воздуха и превращаю в систему"
        },
        "interpretations": {
            "A": "Ты — приёмник, не автор. У тебя нет «я придумала» — у тебя «я услышала». Ты входишь в канал, а идеи протекают сквозь. Ты — транслятор. Если перекрыть поток — система падает. Сила в доверии без контроля.",
            "B": "Ты синестетик смыслов. Идеи в тебе не из логики — они из образов, цвета, ощущения. Ты видишь мысль в форме. Это не мышление — это внутренний дизайнер смыслов. Ты переводишь абстрактное в чувственное.",
            "C": "Ты архитектор связей. Твоя сила — объединять то, что не соединяется. Ты находишь мост между полюсами. Ты не придумываешь — ты распознаёшь. Это идеация высокого уровня: не "создаю", а "вижу, как всё работает вместе".",
            "D": "Ты визионер-реализатор. Ты не любишь просто идею — тебе нужно её закрепить. Построить. Проверить. Ты не романтик, а синтезатор систем: видишь импульс — превращаешь в механизм. Это редкое сочетание мечты и процесса."
        }
    },
    # Добавьте остальные вопросы из test2.0 здесь
]

# Функции для получения вопросов
def get_demo_questions() -> List[Dict[str, Union[str, List[str]]]]:
    """
    Получение списка демо-вопросов.
    
    Returns:
        List[Dict]: Список демо-вопросов.
    """
    return DEMO_QUESTIONS

def get_all_vasini_questions() -> List[Dict[str, Union[str, Dict[str, str]]]]:
    """
    Получение полного списка вопросов Vasini.
    
    Returns:
        List[Dict]: Полный список вопросов Vasini.
    """
    return VASINI_QUESTIONS

def get_question_by_id(question_id: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Получение вопроса по его ID.
    
    Args:
        question_id: ID вопроса.
        
    Returns:
        Dict: Данные вопроса или пустой словарь, если вопрос не найден.
    """
    # Объединяем демо-вопросы и все вопросы Vasini
    all_questions = DEMO_QUESTIONS + get_all_vasini_questions()
    
    # Ищем вопрос по ID
    for question in all_questions:
        if question["id"] == question_id:
            return question
    
    # Если вопрос не найден, возвращаем пустой словарь
    return {}

def get_personality_type_from_answers(answers: Dict[str, Any]) -> Tuple[Dict[str, int], str, Optional[str]]:
    """
    Определяет тип личности по ответам на вопросы Vasini.
    
    Args:
        answers: Словарь с ответами пользователя
    
    Returns:
        Tuple[Dict[str, int], str, Optional[str]]: Кортеж с количеством ответов каждого типа, 
                                              основным типом личности и дополнительным типом (если есть)
    """
    # Счетчики для типов ответов
    type_counts = {
        "A": 0,  # Аналитический тип
        "B": 0,  # Эмпатический тип
        "C": 0,  # Практический тип
        "D": 0   # Творческий тип
    }
    
    # Подсчитываем количество ответов каждого типа
    vasini_count = 0
    for question_id, answer in answers.items():
        # Проверяем, что это вопрос Vasini (начинается с 'vasini_')
        if question_id.startswith('vasini_') and answer in ["A", "B", "C", "D"]:
            type_counts[answer] += 1
            vasini_count += 1
    
    # Логируем информацию о подсчете
    logger.info(f"Подсчитано {vasini_count} ответов на вопросы Vasini")
    logger.info(f"Распределение ответов: A ({type_counts['A']}), B ({type_counts['B']}), C ({type_counts['C']}), D ({type_counts['D']})")
    
    # Если ответов на вопросы Vasini нет, возможно структура ответов другая
    # Проверяем наличие ответов в другом формате
    if sum(type_counts.values()) == 0:
        logger.warning("Не найдены ответы в стандартном формате, пробуем альтернативный формат")
        for key, value in answers.items():
            if isinstance(value, str) and value.upper() in ["A", "B", "C", "D"]:
                type_counts[value.upper()] += 1
    
    # Находим тип с наибольшим количеством ответов
    primary_type = max(type_counts, key=type_counts.get)
    max_count = type_counts[primary_type]
    
    # Если все счетчики равны 0, устанавливаем тип по умолчанию
    if max_count == 0:
        logger.warning("Не удалось определить тип личности, используется тип по умолчанию")
        return type_counts, "Аналитический тип", None
        
    # Название типа личности
    personality_types = {
        "A": "Аналитический тип",
        "B": "Эмпатический тип",
        "C": "Практический тип",
        "D": "Творческий тип"
    }
    
    # Находим второй по частоте тип
    type_counts_copy = type_counts.copy()
    type_counts_copy.pop(primary_type)
    secondary_type = max(type_counts_copy, key=type_counts_copy.get)
    second_max_count = type_counts_copy[secondary_type]
    
    # Если второй тип сильно отстает от первого, не учитываем его
    if second_max_count < max_count * 0.7:
        secondary_result = None
    else:
        secondary_result = personality_types[secondary_type]
    
    logger.info(f"Определен тип личности: {personality_types[primary_type]}" + 
               (f" с элементами {secondary_result}" if secondary_result else ""))
    
    return type_counts, personality_types[primary_type], secondary_result

def generate_profile_prompt(answers: Dict[str, str]) -> str:
    """
    Генерирует промт для создания психологического профиля по структуре 2.0.
    
    Args:
        answers: Словарь с ответами пользователя на вопросы
    
    Returns:
        str: Промт для генерации профиля
    """
    # Получаем информацию о типе личности
    type_counts, primary_type, secondary_type = get_personality_type_from_answers(answers)
    
    # Получаем базовую информацию о пользователе
    name = answers.get("name", "пользователь")
    age = answers.get("age", "")
    birthdate = answers.get("birthdate", "")
    birthplace = answers.get("birthplace", "")
    timezone = answers.get("timezone", "")
    
    # Формируем строку с личными данными пользователя
    personal_data = f"Личные данные пользователя:\n"
    personal_data += f"- Имя: {name}\n"
    
    if age:
        personal_data += f"- Возраст: {age}\n"
    if birthdate:
        personal_data += f"- Дата рождения: {birthdate}\n"
    if birthplace:
        personal_data += f"- Место рождения: {birthplace}\n"
    if timezone:
        personal_data += f"- Часовой пояс: {timezone}\n"
    
    # Формируем промт на основе структуры профайлинга 2.0
    prompt = f"""Создай персональный профиль пользователя согласно структуре профайлинга 2.0.

{personal_data}

Информация о типе личности:
- Основной тип: {primary_type}
- Дополнительный тип: {secondary_type if secondary_type else "не выявлен"}
- Распределение ответов: A ({type_counts['A']}), B ({type_counts['B']}), C ({type_counts['C']}), D ({type_counts['D']})

Структура персонального профиля должна СТРОГО соответствовать следующим требованиям:

1. **Ядро личности (5 основных модулей)** - выбери 5 главных модулей силы на основе выборов A-D
   Для каждого из 5 модулей:
   - **Название модуля** (8-24 символа)
   - **Описание модуля** (180-230 символов)
   - **Как проявляется** (260-320 символов)
   - **Раскрытие** (260-320 символов)
   - **Ключ-фраза** (35-80 символов)
   Разделяй модули строкой из трёх тире `---`

2. **Вспомогательные модули (5 модулей)** - выбери 5 дополнительных модулей
   Для каждого из 5 модулей:
   - **Название модуля** (8-24 символа)
   - **Описание модуля** (140-180 символов)
   - **Как проявляется** (220-280 символов)
   - **Раскрытие** (220-280 символов)
   - **Ключ-фраза** (35-80 символов)

3. **Общий код личности** - один непрерывный абзац (420-540 символов)

4. **P.S.** - один абзац мотивации (300-400 символов)

Стиль и тон текста:
- Обращайся к пользователю исключительно на «ты», во втором лице единственного числа, женский род
- Используй поэтичный и образный язык с метафорами и ритмом
- Сохраняй ясность и конкретику, избегай "воды" и эзотерики
- Используй короткие энергичные предложения для ключевых мыслей
- Тон должен быть поддерживающим, вдохновляющим и честным
- Названия модулей выделяй жирным шрифтом с нумерацией
- Формулируй ключ-фразы в настоящем времени, от первого лица

ВАЖНО: Избегай тавтологии и однотипных фраз. Разнообразь стиль следующим образом:
1. Для блока "Как проявляется" используй разные начала фраз: "В твоей жизни этот дар раскрывается...", "Твоя сила заметна в ситуациях...", "Окружающие видят этот талант..."
2. Для блока "Раскрытие" разнообразь конструкции: "Путь к углублению этой способности...", "Усилить этот дар можно...", "Для активации потенциала..."
3. Разнообразь описания способностей вместо частого "Ты умеешь": "В тебе живет дар...", "Тебе присуща способность...", "У тебя есть талант..."

Ограничения по метафорам:
- Используй метафоры умеренно — не более 1-2 образных сравнений на смысловой блок
- Делай акцент на конкретных действиях и проявлениях в реальной жизни
- Не допускай повторов одних и тех же образов (например: "маяк", "зеркало", "компас") в разных частях текста
- Если образ уже использовался — замени его или полностью переформулируй мысль

Естественность тона:
- Избегай искусственно "приподнятого" тона и поэтических штампов
- Сохраняй профессиональный подход в описании качеств
- Стремись к тёплому, вдохновляющему, но естественному звучанию текста

Дополнительные стилистические ограничения:
- Избегай повторяющихся конструкций: «этот дар раскрывается», «ты — как…», «твоя способность проявляется…»
- Ограничь количество метафор: не более 1–2 на весь раздел, чтобы не перегружать образность
- Варьируй синтаксис и лексику — используй разные способы начала абзацев и фраз, избегай шаблонов
- Делай упор на действия и проявления, а не только на образы и абстракции
- Чередуй простые и сложные предложения, прямую и инверсионную структуру для ритмичности текста
- Сопровождай образные сравнения конкретными примерами из жизни для баланса

Окончательные стилистические указания:
- Избегай повторяющихся фраз и шаблонов (например, "этот дар проявляется", "ты умеешь", "усилить этот дар можно...")
- Используй метафоры и образы ограниченно — не более 1–2 на весь текст, избегай штампов типа "маяк", "компас"
- Отдавай приоритет действиям, конкретным ситуациям и живым формулировкам вместо общих абстракций
- Тон должен быть тёплым, профессиональным и легко читаемым, без канцелярита и чрезмерной поэтичности
- Текст должен звучать естественно, избегая искусственного "вдохновляющего" тона

Итоговые стилистические требования:
- Избегай повторяющихся фраз и шаблонов, таких как: «Этот дар проявляется…», «Ты обладаешь…», «Путь к раскрытию…», «Этот аспект твоей натуры…»
- Не дублируй смысловые блоки (например, "Обучаемость" ≈ "Умение учиться"). Каждый модуль должен раскрывать отдельный аспект личности
- Метафоры и образные выражения используй умеренно — не более 1–2 на весь текст, избегай штампов
- Разнообрази структуру абзацев и синтаксис. Не начинай каждый абзац одинаково (например, "Ты обладаешь...")
- Итоговый тон — вдохновляющий, но не клишированный, без излишне абстрактных фраз вроде «Ты — создательница своей реальности»

Расширенные стилистические требования:
- Избегай повторяющихся конструкций: «ты обладаешь…», «этот дар проявляется…», «раскрыть этот аспект можно, если…»
- Ограничь использование слов «уникальный», «дар», «талант» — заменяй на синонимы, чтобы текст не звучал механически
- Исключи повторяющиеся метафоры и шаблоны в заключении: «ты — сильная женщина», «ты — мастер», «ты — уникальная личность»
- Разнообрази подачу модулей — не начинай каждый с одинаковой формулы
- Избегай смыслового дублирования между основными и вспомогательными модулями. Если черты повторяются — объедини и конкретизируй их различие
- Поддерживай тёплый, вдохновляющий, но профессионально выверенный тон без излишней поэтичности

ВАЖНО: Соблюдай точное количество символов в каждом блоке согласно указанным диапазонам. Символы считаются вместе с пробелами и знаками пунктуации.

Ответы пользователя на вопросы:
"""
    
    return prompt 