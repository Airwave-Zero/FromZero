import subprocess
import time
#import sheets

global current_commands


current_commands = ["Open" , "Write"]

def generic_UI():

    print("Welcome! The currently existing commands are:")
    for command in current_commands:
        print(command)

    option = input("\nWhat would you like to do? ('Quit' to exit)\n")

    while(option.lower() != "quit"):
        if(option.lower().startswith("open")):
            print("Opening program: " + itemDesired[1])
        elif(option.lower().startswith("write")):
            handle_writing()
        else:
            print("You entered: " + option + ".")
            print("Invalid command!")
        option = input("What else would you like to do?\n")
       
def open_program(programPath):
    subprocess.Popen(programPath)
    #subprocess.Popen("C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe")


#Handles logistical writing and calls write to file
def handle_writing():
    fileName = "F:\\MiscText\\" + input("Please enter a .txt file\n")
    print("Opening text file: " + fileName)
    newText = input("What text do you want to add to the file?\n")
    write_to_file(fileName, newText)


#Writes inputted text into the file with a time stamp on it
def write_to_file(filename, textToAdd):
    file = open(filename, "a")
    file.write("\nNote added on - " + time.ctime() + " : ")
    file.write(textToAdd + "\n")
    file.close()


if __name__ == "__main__":
    generic_UI()
