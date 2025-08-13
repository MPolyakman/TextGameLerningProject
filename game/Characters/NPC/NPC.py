from creatures import Entity
import ollama
from aistuff.aifunс import fix_mes

sys_promptNPC = '''
Вы — NPC в текстовой рогалик-игре.
Ваша задача — вести диалог с игроком,
в зависимости от того, что он вам скажет, Вы должны отвечать
в соответствии со своей ролью, без английских слов,
ответ — не более 75 слов. 
Реагируйте на действия игрока, поддерживая живой и естественный диалог.
'''

class NPC(Entity):
    def __init__(self, name, position, max_health, biography):
        super().__init__(name, position, max_health)
        self.biography = biography
        self.history = sys_promptNPC

    def say(self, messages):
        messages.append({'role': 'system', 'content': self.biography})
        messages.append({'role': 'system', 'content': self.history})
        btw = ollama.chat(model='llama3:instruct', messages=messages)
        ans = btw['message']['content']
        ans = fix_mes(ans)
        messages.append({'role': 'system', 'content': ans})
        messages.append({'role': 'user', 'content': "Вкратце перескажи всё то что, говорил этот NPC и всё что с ним происходило за исключением исходного описания"})
        self.history = ollama.chat(model='llama3:instruct', messages=messages)['message']['content']
        return ans
