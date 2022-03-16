from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
import time
import random

from monitor import Table

NPHIL = 5
K = 5

def delay(n):
    time.sleep(random.random()/n)
    
def philosopher_task(num: int, table: Table):
    table.set_current_phil(num)
    cont = 0
    while cont<K:
        print(f"Philosopher {num} thinking")
        delay(3)
        print(f"Philosopher {num} wants to eat")
        table.wants_eat(num)
        print(f"Philosopher {num} eating")
        delay(3)
        print(f"Philosopher {num} stops eating")
        table.wants_think(num)
        cont += 1
        
def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    philosophers = [Process(target=philosopher_task, args=(i,table)) \
                    for i in range(NPHIL)]
    for i in range(NPHIL):
        philosophers[i].start()
    for i in range(NPHIL):
        philosophers[i].join()
        
if __name__ == '__main__':
    main()