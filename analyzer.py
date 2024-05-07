from sys import platform
import sys
import subprocess
from subprocess import PIPE
import errno
import shutil
import os
from colorama import Fore

class Inform:

    def __init__(self, step):
        self.step = step
    
    def message(self, msg):
        print(Fore.BLUE, "[" + str(self.step) + "] " + msg, end="")
        print(Fore.RESET)
        self.step += 1

# run cmake commands
def cmake_build(src, build, options):

    # generate an array to pass to subprocess
    command = ["cmake"]

    if platform == "win32":
        command.append("-DCMAKE_CXX_COMPILER=g++")
        command.append("-DCMAKE_C_COMPILER=gcc")
        command.append("-G")
        command.append("MinGW Makefiles")

    command.append("-S")
    command.append(src)
    command.append("-B")
    
    if platform == "linux" or platform == "linux2" or "darwin":
        command.append("./" + build)
    elif platform == "win32":
        command.append(".\\" + build)


    for option in options:
        command.append(option)

    # build with cmake
    try:
        subprocess.call(command)
    
    # error out
    except OSError as e:
        if e.errno == errno.ENOENT:
            # program was not found
            print(Fore.RED, f"[ERROR] : failed to run CMake! with command \"{command}\"")
            quit()
        else:
            # program output
            raise

#compile c code
def compile_code(project_name):
    try:
        if platform == "win32":
            subprocess.call(["mingw32-make","-C",".\\build", project_name])
        else:
            subprocess.call(["make","-C","./build", project_name])

    except OSError as e:
        if e.errno == errno.ENOENT:
            # program was not found
            print(Fore.RED, "[ERROR] : failed to compile C code!")
            quit()
        else:
            # program output
            raise


def write_mp3_file_extension_paths(directory, filename):
    with open(filename, "wb") as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp3"):
                    f.write(os.path.join(root, file).encode() + b"\n")


if __name__ == "__main__":

    inform = Inform(1)

    inform.message("Starting CMake build process")
    
    foldername = "build"
    inform.message(f"Checking for {foldername} directory")
    if not os.path.exists(foldername):
        inform.message(f"Creating {foldername} directory")
        os.mkdir(foldername)
    else:
        inform.message(f"Removing and recreating {foldername} directory")
        shutil.rmtree(foldername)
        os.mkdir(foldername)


    cmake_build(".", "build", ["-DBUILD_SHARED_LIBS=ON"])
    inform.message("Built C code with CMake")

    inform.message("Compiling C code")
    compile_code("toCSV")

    inform.message("Creating a CSV file")

    inform.message("Creating paths.txt file")
    write_mp3_file_extension_paths(sys.argv[1], "build/paths.txt")

    try:
        if platform == "win32":
            os.chdir("build")
            subprocess.call(["toCSV.exe", "paths.txt"])
            os.chdir("..")
        else:
            subprocess.call(["valgrind","./build/toCSV", "build/paths.txt"])
    except OSError as e:
        if e.errno == errno.ENOENT:
            # program was not found
            print(Fore.RED, "[ERROR] : failed to run toCSV!")
            quit()
        else:
            # program output
            raise
    inform.message("Generated CSV")

    # inform.message("Creating plots")
    # try:
    #     subprocess.call(["Rscript", "mktables.r"])
    # except OSError as e:
    #     if e.errno == errno.ENOENT:
    #         # program was not found
    #         print(Fore.RED, "[ERROR] : failed to generate plots!")
    #         quit()
    #     else:
    #         # program output
    #         raise

    