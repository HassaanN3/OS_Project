import classes
import functions
import sys
import threading
import thread_functions

def getIntInput(min, max):
    while(1):
        user_input = int(input(": "))
        if user_input >= min and user_input <= max:
            return user_input
        else:
            print("Enter Valid Option")

if __name__ == '__main__':
    home_directory = classes.Directory(name='home', hashTable=functions.loadFromDat(), path="/")
    current_directory = home_directory
    current_file = ""

    print("\tFile Management System\n")
    print(f"Current Directory: {current_directory.path}")

    print("Enter number of threads to launch (min 1, max 6)")
    user_input = getIntInput(min=1,max=6)
    threads = []

    for i in range(user_input):     #creating threads
        threads.append(threading.Thread(target=thread_functions.exec_testcases, args=(i+1,home_directory, current_directory, current_file)))
    
    print(f"\nSuccessfully created {user_input} threads.\n")
    
    for i in range(user_input):     #executing threads -> can be done in a single loop but same complexity
        threads[i].start()

    for i in range(user_input):     #thread rejoining after executing its functions
        threads[i].join()
    
    #try error
    sys.stdout = sys.__stdout__     #redirect Output -> Failsafe incase threading fails before redirecting
    print("Successfully executed all test cases\n")
    #print all changes
    #exit