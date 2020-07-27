import subprocess

def open_program(programPath):
    subprocess.Popen(programPath)
    #subprocess.Popen("C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe")

def write_to_file(filename, textToAdd):
    file = open(filename, 'w')
    file.write(textToAdd)


if __name__ == "_main__":
    open_program("")
