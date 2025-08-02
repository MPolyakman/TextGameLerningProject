import ollama
 
def fixmes(mes: str) -> str:
    red_mes = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'user', 'content': f'Исправь это сообщение в соответсвии со всеми нормами русского языка: {mes}'}
    ])
    return red_mes['messages']['content']