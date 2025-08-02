import ollama
import inspect 

def fixmes(mes: str) -> str:
    red_mes = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'user', 'content': f'Исправь ошибки, чтобы звучало нормально и больше ничего не пиши: {mes}'}
    ])
    return red_mes['message']['content']

def to_dict_prompt(self):
    smth = self.__dict__
    prompt = 'Это характеристики объекта: \n'+'\n'.join(f'{k}={v}' for k, v in smth.items())
    return prompt
    
