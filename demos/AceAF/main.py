import threading
import time
from agentforge.utils.storage_interface import StorageInterface

class ACE:
    def __init__(self):
        self.storage = StorageInterface()
        self.selectsouthbus = self.storage.select_collection("SouthBus")
        self.loadsouthbus = self.storage.load_collection("SouthBus")
        self.selectnorthbus = self.storage.select_collection("NorthBus")
        self.loadnorthbus = self.storage.load_collection("NorthBus")
def loop_1():
    while True:
        print("Loop 1")
        time.sleep(1)

def loop_2():
    while True:
        print("Loop 2")
        time.sleep(1.5)

# Create two threads
t1 = threading.Thread(target=loop_1)
t2 = threading.Thread(target=loop_2)

# Start both threads
t1.start()
t2.start()

# If you don't want the main program to exit immediately,
# you can either use a join (but in this case with infinite loops, it doesn't make much sense)
# or you can have another infinite loop in the main thread.
# However, do note that in this specific example, the main program will keep running indefinitely.
while True:
    pass


class LayersInit():

    def __init__(self):
        pass

    def l1start(self):
        l1 = L1AspirationalClass()
        l1.start_sub_threads()

    def l2start(self):
        l2 = L2StrategyClass()
        l2.start_sub_threads()

    def threadlayers(self):
        thread1 = threading.Thread(target=self.l1start)
        thread2 = threading.Thread(target=self.l2start)
        thread1.start()
        thread2.start()