'''
Created on Jun 16, 2021

@author: Bill Nicholson
nicholdw@ucmail.uc.edu

'''
# Producer/Consumer multithreading
# Is a Python list thread-safe? 
#  This SO page says lists are thread-safe but that's not authoritative: https://stackoverflow.com/questions/6319207/are-lists-thread-safe

import threading
import time
import random
from _random import Random

  
def producer(threadID, itemsToAdd):
    """
    populate our shared data structure
    """
    if itemsToAdd > 1:
        for i in range(0,itemsToAdd):
            myData.append(threadID + ": " + str(i))
            myData.pop(-1)           # Just pop the oldest one. We don't care what it is.
    else:
        counter = 999;
        while True:
            myData.append(threadID + ": " + str(counter))
            time.sleep(random.random()*5)           # 5 seconds or less
            counter = counter + 1
            r = random.random()*5
            if (r < 2):
                myData.append(threadID + ": " + "Apple")

  
def consumer(threadID):
    """
    Process elements in the shared data structure
    """
    while True:
        time.sleep(1)
        if (len(myData) > 1):
            tmp = myData.pop(-1)
            print(threadID + ": " + str(tmp))
        
def agent():
    """
    Just check to see how we're doing
    """
    while True:
        time.sleep(5)
        if (len(myData) > 0) :
            print("Agent: " + str(len(myData)) + " elements remaining. Oldest element is " + str(myData[0]))
        else:
            print("Agent: " + str(len(myData)) + " elements remaining.")
            

  
def isPrime(num):
    if (num == 2): 
        return True
    for i in range(3,num/2,2):
        if (num % i == 0):
            return False
    return True


'''
This function will throw an exception when multiple threads try to run .remove() (or .pop() ) on a list BECAUSE it has a logic error.
It's worth studying because the logic error is a good lesson in bad multithreaded programming.
Code in this function was adapted from https://stackoverflow.com/questions/6319207/are-lists-thread-safe
'''
def demoOfNonThreadSafe():
    # Change this number as you please, bigger numbers will get the error quickly
    count = 1000
    l = []
    
    def add():
        for i in range(count):
            l.append(i)
            time.sleep(0.0001)
    
    def remove():
        for i in range(count):
            l.remove(i)
            time.sleep(0.0001)
    
    
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=remove)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print(l)

      
if __name__ == "__main__":
    
    
    #demoOfNonThreadSafe()
    #exit
    
    
    myData = []
    items = 1000000
    tAgent   = threading.Thread(target=agent, kwargs={})
    
    # creating threads
    tConsumer   = threading.Thread(target=consumer, kwargs={"threadID":"C01"})
    tProducer01 = threading.Thread(target=producer, kwargs={"threadID":"P01", "itemsToAdd":items})
    tProducer02 = threading.Thread(target=producer, kwargs={"threadID":"P02", "itemsToAdd":items})
    tProducer03 = threading.Thread(target=producer, kwargs={"threadID":"P03", "itemsToAdd":items})
  
    tAgent.start()

    #tConsumer.start()
    tProducer01.start()
    tProducer02.start()
    tProducer03.start()
  
    # wait until threads are done.
    #tConsumer.join()
    tProducer01.join()
    tProducer02.join()
    tProducer03.join()
    tAgent.join()
    
    print(str(len(myData) + " items in our data structure."))
    
    print("Done!")