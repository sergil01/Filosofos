from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
import time
import random

class Table():
    def __init__(self,nphil,manager):
        self.phil = None
        self.mutex = Lock()
        self.used_forks = Array('i',[-1 for _ in range(nphil)]) #array de tenedores
                                                                #-1 si están libres
        self.free_forks = Condition(self.mutex)
        self.manager = manager
    
    def set_current_phil(self,num):
        self.phil = num
    
    def available_forks(self):
        #mira si su tenedor y el siguiente están libres (su valor es -1)
        return self.used_forks[self.phil] == -1 and self.used_forks[(self.phil+1)%len(self.used_forks)] == -1
    
    def wants_eat(self,phil):
        self.mutex.acquire()
        fork1 = phil
        fork2 = (phil + 1) % len(self.used_forks)
        self.free_forks.wait_for(lambda: self.available_forks()) #mira si están libres
        self.used_forks[fork1] = phil
        self.used_forks[fork2] = phil
        #cambia los valores de cada tenedor al filósofo que lo usa
        self.mutex.release()
        
    def wants_think(self,phil):
        self.mutex.acquire()
        fork1 = phil
        fork2 = (phil + 1) % len(self.used_forks)
        self.used_forks[fork1] = -1
        self.used_forks[fork2] = -1
        #libera los tenedores
        self.free_forks.notify()
        self.mutex.release()