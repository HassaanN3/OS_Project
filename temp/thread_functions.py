import functions
import classes
import sys

def exec_testcases(thread_num, home_directory, current_directory, current_file):
    file = open(f"./testCases/input/input_thread{thread_num}.txt","r")
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].lower()
    stdout = sys.stdout
    with open(f'./testCases/output/output_thread{thread_num}.txt', 'w') as sys.stdout:  #all print statements directed to file
        for i in range(len(lines)):
            print(f"Command: {lines[i]}Output: ", end="")
            if "mkdir" in lines[i]:  
                words = lines[i].split()    #1 = dir_name
                functions.mkDir(current_directory, words[1])
            elif "chdir" in lines[i]:
                words = lines[i].split()    #1 = dir_name, 2 = mode
                words[1] = words[1].replace(',',"")    #removing comma
                if words[2] == "p":
                    current_directory = functions.chDir(home_directory, current_directory, mode="parent")
                elif words[2] == "c":   #child
                    current_directory = functions.chDir(current_directory,words[1], mode="child")
                elif words[2] == "f":   #full path
                    current_directory = functions.chDir(home_directory, new_directory=words[1], mode = "path")
            elif "open" in lines[i]:
                words = lines[i].split()    #1 = file_name, 2 = mode
                words[1] = words[1].replace(',',"")    #removing comma
                if words[2] == 'w':
                    words[2] = "write"
                elif words[2] == 'r':
                    words[2] = "read"
                current_file = functions.Open(current_directory, words[1], words[2])
            elif "close" in lines[i]:
                words = lines[i].split()    #1 = file_name
                current_file = functions.Close(current_file)
            elif "create" in lines[i]:
                words = lines[i].split()    #1 = file_name
                functions.create(current_directory, words[1])
            elif "delete" in lines[i]:
                words = lines[i].split()    #1 = file_name
                functions.delete(current_directory, words[1])
            elif "write" in lines[i]:
                words = lines[i].split()    #1 = file_name, 2 = text
                words[1] = words[1].replace(',',"")    #removing comma
                if isinstance(current_file, classes.File):
                    current_file.writeToFile(text=words[2])
            elif "read" in lines[i]:
                words = lines[i].split()    #1 = file_name
                print("\nContent: ")
                if isinstance(current_file, classes.File):
                    current_file.writeToFile(text=words[2])
            elif "memory" in lines[i]:
                functions.printMemoryMap(home_directory)
            else:
                print("Invalid command")
            print("")   #new line
    file.close()    #closing file
    sys.stdout = stdout     #redirecting output