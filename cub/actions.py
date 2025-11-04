from threading import Thread
from queue import Queue
import time
import random
import math

class AdvancedBacterialController:
    def __init__(self):
        self.queue = Queue()
        self.worker = None
        self.running = False
        self.params = {
            'dx': 0,
            'dy': 0,
            'dr': 0
        }
    
    def start(self):
        if not self.running:
            self.running = True
            self.worker = Thread(target=self._main_loop, daemon=True)
            self.worker.start()
    
    def stop(self):
        if self.running:
            self.running = False
            self.queue.put(('STOP', None))
    
    def update_param(self, param_name, value):
        self.queue.put(('UPDATE_PARAM', (param_name, value)))
    
    def get_status(self):
        self.queue.put(('GET_STATUS', None))
    
    def _main_loop(self):
        while self.running:
            # Обрабатываем все команды в очереди
            while not self.queue.empty():
                try:
                    command, data = self.queue.get_nowait()
                    if command == 'UPDATE_PARAM':
                        param_name, value = data
                        self.params[param_name] = value
                        print(f"Updated {param_name} to {value}")
                    
                    elif command == 'GET_STATUS':
                        print(f"Current params: {self.params}")
                    
                    elif command == 'STOP':
                        return
                        
                except:
                    break
            
            # Основная логика
            self._gen_d_xyr()
            time.sleep(0.1)
    
    def _gen_d_xyr(self):
        # Используем текущие параметры для симуляции
        r = 0 # нужно получать из очереди
        rand = 0
        if rand == 0:
            # dr = random.randint(-20, 20)
            dr = random.randint(-20, 20)
            dx = 0
            dy = 0
            rand = 1
        elif rand == 1:
            dr = 0
            dx = 10 * math.cos(math.radians(r))
            dy = 10 * math.sin(math.radians(r))
            rand = 0
        randdd = random.randint(1, 4)
        if randdd == 4:
            dr = 0
            dx = -math.cos(math.radians(r))
            dy = -math.sin(math.radians(r))
        
        # # Уменьшаем nutrients со временем
        # self.params['nutrients'] -= 0.1

# # Использование
# controller = AdvancedBacterialController()

# def some_view_function(request):
#     controller.start()
    
#     # Передаем разные параметры
#     controller.update_param('growth_rate', 25)
#     controller.update_param('temperature', 30)
#     controller.get_status()