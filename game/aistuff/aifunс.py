import ollama
import inspect 
import numpy as np

def fix_mes(mes: str) -> str:
    red_mes = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'user', 'content': f'Ты знаешь русский язык на уровне носителя, исправь ошибки, чтобы оно звучало красиво и не теряло смысл: {mes}'}
    ])
    return red_mes['message']['content']

def to_dict_prompt(self):
    smth = self.__dict__
    prompt = 'Это характеристики объекта: \n'+'\n'.join(f'{k}={v}' for k, v in smth.items())
    return prompt

def reduce_mes(mes: str) -> str:
    red_mes = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'user', 'content': f'''Ты профессиональный русскоязычный копирайтер,
        переформулируй всё сообщение так, чтобы основной посыл не потерялся,
         но общий объём значительно уменьшился: {mes}'''}
    ])
    return red_mes['message']['content']

def str_to_prompt(mes: str):
    return {'role': 'user', 'content': mes}

def print_var_name(var):
    frame = inspect.currentframe()
    if frame is not None and frame.f_back is not None:
        for name, val in frame.f_back.f_locals.items():
            if val is var:
                print(name)

def condition_str_to_dict (self, prompt: str):
    lines = prompt.strip().split('\n')
    if not lines[0].startswith('Это характеристики объекта:'):
        raise ValueError('Неверный формат строки')
    for line in lines[1:]:
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if value.isdigit():
                value = int(value)
            elif value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass 
            setattr(self, key, value)    

def context_check(prompt: str, messages: list[str]) -> bool:
    if not messages:
        return True  
    try:
        prompt_embedding = ollama.embeddings(model='nomic-embed-text', prompt=prompt)['embedding']
        context = " ".join(messages)
        context_embedding = ollama.embeddings(model='nomic-embed-text', prompt=context)['embedding']
        similarity = np.dot(prompt_embedding, context_embedding) / (
            np.linalg.norm(prompt_embedding) * np.linalg.norm(context_embedding)
        )
        threshold = 0.350
        print(f"Сходство: {similarity:.3f}")
        return similarity >= threshold
    except Exception as e:
        print(f"Ошибка при проверке контекста: {e}")
        return False
