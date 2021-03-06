# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:33:39 2022

@author: Elena
"""

from multiprocessing import Lock, Condition, Value



class Table():
    
    def __init__(self, nphil: int, manager):
        self.mutex = Lock()
        self.nphil = nphil
        self.eating = Value('i',0)
        self.manager = manager
        self.phil = self.manager.list([False]* nphil)
        self.current_phil = None
        self.free_fork = Condition(self.mutex)
        
    def set_current_phil(self, num):
        self.current_phil = num
    
    def no_comen_lados(self):
        n = self.current_phil
        return ((not self.phil[(n-1)%(self.nphil)]) and (not self.phil[(n+1)%(self.nphil)]))
    
    def wants_eat(self, num):
        self.mutex.acquire()
        self.current_phil = num
        self.free_fork.wait_for(self.no_comen_lados)
        self.phil[num] = True
        self.eating.value += 1
        self.mutex.release()
        
    
    def wants_think(self,num):
        self.mutex.acquire()
        self.phil[num] = False
        self.eating.value -= 1
        self.free_fork.notify()
        self.mutex.release()
        