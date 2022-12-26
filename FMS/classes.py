class Directory:
    path = ""
    def __init__(self, name, hashTable, path) -> None:
        self.name = name
        self.hashTable = hashTable
        self.path += path + name + "/"

class File:
    def __init__(self, name, content, path) -> None:
        self.name = name
        self.content = content
        self.path = path + name
        self.read = False
        self.write = False
    
    def writeToFile(self, text, index = 'end') -> None:
        if self.write is True:
            if index == 'end':
                self.content += text
            else:   #does not overwrite TODO index does not exist
                self.content = self.content[:index] + text + self.content[index:]
            print(f"Successfully wrote content in file {self.name}")
        else:
            print(f"Error cannot write to {self.name}: No access")

    def readFromFile(self, index = 0, size  = -1) -> None:
        if self.read is True:
            if size == -1:
                print(self.content[index:])
            else:
                print(self.content[index:index+size])
        else:
            print(f"Error cannot read from {self.name}: No access")
