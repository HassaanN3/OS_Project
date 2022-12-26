import classes
import functions
import os

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

    while(1):
        print("\tFile Management System\n")
        print(f"Current Directory: {current_directory.path}")
        print("\n1. Create File\t\t2. Delete File")
        print("3. Open File\t\t4. List all files")
        print("5. Make Directory\t6. Delete Directory")
        print("7. Change Directory\t8. Print Memory Map")
        print("9. Clear Screen\t\t10. Save")
        print("11. Exit")
        user_input = getIntInput(min=1,max=11)
        
        if user_input == 1: #Create File
            file_name = input("\nEnter File Name\n: ")
            functions.create(current_directory, file_name)

        elif user_input == 2: #Delete File
            file_name = input("\nEnter File Name\n: ")    #TODO file does not exist
            functions.delete(current_directory, file_name)

        elif user_input == 3: #Open File
            file_name = input("\nEnter File Name\n: ")    #TODO file does not exist
            mode = input("\nEnter Mode\n: ")
            current_file = functions.Open(current_directory, file_name, mode)

            while(current_file != False):    #Valid Parameters
                print(f"\nCurrent File: {current_directory.path}{file_name}")
                print("\n1. Write in File\t2. Read from File\n3. Close File")
                user_input = getIntInput(min=1,max=3)

                if user_input == 1: #Write in File
                    if current_file.write == True:
                        print("\n1. Append Mode\t2. Write at Index")
                        user_input = getIntInput(min=1,max=2)

                        content = input("Enter text to write: ")

                        if user_input == 1: #Write in Append Mode
                            current_file.writeToFile(text=content)

                        elif user_input == 2: #Write at Index
                            write_at = int(input("Enter index: "))
                            current_file.writeToFile(text=content, index=write_at)
                    else:
                        print(f"Error cannot read from {current_file.name}: No access")

                elif user_input == 2:   #Read from File
                    if current_file.read == True:
                        print("\n1. Sequential Read\t2. Read from Index")
                        user_input = getIntInput(min=1,max=2)

                        if user_input == 1: #Read in Sequential 
                            print("\nContent: ")
                            current_file.readFromFile()
                        elif user_input == 2:   #Read from Index
                            read_from = int(input("Enter index: "))
                                
                            print("\n1. Read All\t2. Read x characters")
                            user_input = getIntInput(min=1,max=2)
                            
                            if user_input == 1: #Read all
                                print("\nContent: ")
                                current_file.readFromFile(index = read_from)

                            elif user_input == 2:   #Read x characters
                                print("\nContent: ")
                                read_size = int(input("Enter Number of Characters to Read: "))
                                current_file.readFromFile(index = read_from, size = read_size) 
                    else:
                        print(f"Error cannot write in {current_file.name}: No access")

                elif user_input == 3:   #Close
                    current_file = functions.Close(current_file)

        elif user_input == 4:   #List all files in directory
            functions.printElements(current_directory)

        elif user_input == 5:   #make dir
            directory_name = input("\nEnter Directory Name\n: ")
            functions.mkDir(current_directory, directory_name)
            
        elif user_input == 6:   #del dir
            directory_name = input("\nEnter Directory Name\n: ")    #TODO file does not exist
            functions.delete(current_directory, directory_name)

        elif user_input == 7:   #change dir
            print("\nChange Directory: ")
            print("1. Parent Directory\t2. Child Directory\n3. Use Full Path")
            user_input = getIntInput(min=1,max=3)

            if user_input == 1:
                current_directory = functions.chDir(home_directory, current_directory, mode="parent")

            elif user_input == 2:
                user_input = input("\nEnter Child Directory Name: ")
                current_directory = functions.chDir(current_directory,user_input, mode="child")
                
            elif user_input == 3:
                user_input = input("\nEnter Full Path to Directory: ")
                current_directory = functions.chDir(home_directory, new_directory=user_input, mode = "path")

        elif user_input == 8:   #Print Memory Map
            functions.printMemoryMap(home_directory)

        elif user_input == 9:   #Clear Screen
            os.system('clear')

        elif user_input == 10:   #Save in .Dat File
            functions.saveInDat(home_directory)

        elif user_input == 11:  #Exit
            break
               
        print("\n")