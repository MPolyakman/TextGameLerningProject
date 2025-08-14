import ollama
from aifunс import fix_mes, to_dict_prompt, str_to_prompt

rules = '''
Привет, ты являешься игровым мастером в текстовой игре жанра rogulike -
твоя задача текстово описывать происходящее в ней при последовательных действиях игрока. 
При описании ты должна опираться на ранеее произошедшие действия, 
а также соответствующие характеристики окружения, игрока, предметов.
Сначала описываешь ментальное и физическое состояние игрока, обращайся к нему на Вы, 
после этого описываешь ближайший объект к самому игроку.
Описание должно занимать не более 75 слов, пиши на хорошем литературном русском языке,
не используя английский язык
'''

def descr(obj):
    prompt = f'''Исходя из следующего описания, которое дано, опиши этот объект, по шаблону: "Название предмета - имя объекта
    Описание самого предмета
    Описание его состояния", используй русский язык, не более 75 слов: {obj}'''
    description = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'system', 'content': rules},
        str_to_prompt(prompt)
    ])
    return fix_mes(description['message']['content'])

def condition(mes: str, obj):
    prompt = f'''Исходя из этого: "{mes}" - предскажи как поменяется состояние объекта,
      учитывая его нынешние характеристики. "{to_dict_prompt(obj)}" -
        ответ пиши в точности также, как и написано в кавычках,
     не меняй характеристики которые задают объект сам по себе'''
    cond = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'system', 'content': rules},
        str_to_prompt(prompt)
    ])
    return cond


response = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'system', 'content': rules},
        {'role': 'user', 'content': "Игрок запустил игру и вошел в первую комнату"}
    ]
)
ans = response['message']['content']
ans_fix=fix_mes(ans)
print(ans)
print(ans_fix)