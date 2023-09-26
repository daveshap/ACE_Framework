import threading
import time

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
