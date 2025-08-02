import ollama
 
def fixmes(mes: str) -> str:
    red_mes = ollama.chat(
    model='llama3:instruct',
    messages=[
        {'role': 'user', 'content': f'Исправь ошибки, чтобы звучало нормально и больше ничего не пиши: {mes}'}
    ])
    return red_mes['message']['content']