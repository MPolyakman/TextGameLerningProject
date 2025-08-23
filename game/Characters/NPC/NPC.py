from Characters.NPC.creatures import Entity
import ollama
from aistuff.aifunс import context_check, fix_mes
from events import SayEvent

sys_promptNPC = '''
Вы — NPC в текстовой рогалик-игре.
Ваша задача — вести диалог с игроком,
в зависимости от того, что он вам скажет, Вы должны отвечать
в соответствии со своей ролью, без английских слов,
ответ — не более 75 слов. 
Реагируйте на действия игрока, поддерживая живой и естественный диалог, пишите прямой речью. \n
'''

class NPC(Entity):
    def __init__(self, name, position, max_health, biography):
        super().__init__(name, position, max_health)
        self.biography = sys_promptNPC + biography
        self.intelligence_bool = True
        self.history = []
        
    def say(self, speaker):
        messages = []
        messages.append({'role': 'system', 'content': self.biography})
        if (len(self.history) > 0):
            messages.append({'role': 'system', 'content': " ".join(self.history)})
        btw = ollama.chat(model='llama3:instruct', messages=messages)
        ans = btw['message']['content']
        ans = fix_mes(ans)
        self.history.append(f'Вы: {ans}')
        return SayEvent(self, ans, speaker)
    
    def listen_and_decide(self, speaker, mes):
        if (context_check(mes, self.history)):
            self.history.append(f'{speaker.name}: {mes}')
            return self.say(speaker)
        else:
            return SayEvent(self, "Очень жаль, но я не понимаю, что и о чем Вы говорите", speaker)
