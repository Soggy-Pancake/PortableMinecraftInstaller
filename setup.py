import sys
import os
import shutil
import subprocess
import time
import socket
import zipfile
import webbrowser

print("test!")

'''
Check for java folder
    if doesn't exist grab java zip and extract to ./java

double check for java/bin/javaw.exe

check for minecraft launcher

create shortcut if it doesn't exist

set minecraft launcher to use ./minecraft as mc directory and
./java for the java installation

save user data in the same folder as well
'''

def moveFolder(source_Path : str, dest_Path : str):
    for root, dirs, files in os.walk(source_Path):
        for file in files:
            file_path = os.path.join(root, file)
            shutil.move(file_path, dest_Path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.move(dir_path, dest_Path)
    
def stringInArray(inp : str, theList : list):
    for item in theList:
        print(inp, item)
        if item == inp:
            return True
    return False

def downloadJava():

    if(not os.path.exists("java")):

        print("Setting up Java!")
        
        #check for java zip file and hash
        if(not os.path.exists("java19.zip") and not os.path.exists("java19.sha256")):
            print("Downloading Java!\n\n\n")
            time.sleep(1)
            os.system("powershell wget https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip -outfile java19.zip")
            os.system("powershell wget https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip.sha256 -outfile java19.sha256")

        #verify downloaded zip
        with open("java19.sha256", 'r') as hashfile:
            javaHash = subprocess.check_output(["certutil", "-hashfile", "java19.zip", "SHA256"]).decode('utf-8').splitlines()[1]
            verifyHash = hashfile.read()
            #print(javaHash)

            if(not verifyHash == javaHash):
                print("Something went wrong! Redownloading...\n\n\n")
                hashfile.close()
                os.remove("java19.zip")
                os.remove("java19.sha256")
                downloadJava()
                return

        with zipfile.ZipFile("java19.zip", 'r') as javaZip:
            javaZip.extractall("java")

    java_numbered_dir = "./java/" + os.listdir("java")[0]

    #put everything in ./java instead of java-19. whatever 
    moveFolder("./java/" + os.listdir("java")[0], "./java")
    os.rmdir(java_numbered_dir) #get rid of useless java version folder
    os.remove("java19.zip")
    os.remove("java19.sha256")

    print("Downloading Java!\n\n\n")
    os.system("powershell wget https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip -outfile java19.zip")
    os.system("powershell wget https://download.oracle.com/java/19/latest/jdk-19_windows-x64_bin.zip.sha256 -outfile java19.sha256")


def installCracked():
    if not os.path.exists("launcher.jar"):
        os.system("powershell wget https://tlaun.ch/dl/mcl/jar -outfile launcher.jar")

        if not os.path.exists("launcher.jar"):
            browserdown = input("Download failed??? Would you like to try downloading from browser?(y/N): ").casefold() == 'y'
            if(browserdown):
                webbrowser.open("https://tlaun.ch/dl/mcl/jar")
                print("If it downloaded through your browser you can move it to the same folder as this script called 'launcher.jar' and try again")
                input("Press enter to close...")
                sys.exit()

        


def installMultiMC():
    if not os.path.exists("UltimMC.zip"):
        os.system("powershell wget https://nightly.link/UltimMC/Launcher/workflows/main/develop/mmc-cracked-win32.zip -outfile UltimMC.zip")
        if not os.path.exists("UltimMC.zip"):
            browserdown = input("Download failed??? Would you like to try downloading from browser?(y/N): ").casefold() == 'y'
            if(browserdown):
                webbrowser.open("https://nightly.link/UltimMC/Launcher/workflows/main/develop/mmc-cracked-win32.zip")
                print("If it downloaded through your browser you can move it to the same folder as this script called 'UltimMC' and try again")
                input("Press enter to close...")
                sys.exit()
            

    if not os.path.exists("UltimMC"):
        with zipfile.ZipFile("UltimMC.zip", 'r') as mcZip:
            mcZip.extractall()


    #Automatically edit the cfg file to use the local java install
    with open('UltimMC/ultimmc.cfg', 'w') as file:
        
        config = ["Analytics=false\n", "AnalyticsClientID=\n", "AnalyticsSeen=2\n", "JavaPath=../java/bin/javaw.exe\n", "Language=en_US\n", f"LastHostname={socket.gethostname()}\n", "MainWindowGeometry=AdnQywACAAAAAAIoAAAAvQAABVcAAAM7AAACMAAAANwAAAVPAAADMwAAAAAAAAAAB4A=\n", "MainWindowState=AAAA/wAAAAD9AAAAAAAAAqsAAAIIAAAABAAAAAQAAAAIAAAACPwAAAADAAAAAQAAAAEAAAAeAGkAbgBzAHQAYQBuAGMAZQBUAG8AbwBsAEIAYQByAwAAAAD/////AAAAAAAAAAAAAAACAAAAAQAAABYAbQBhAGkAbgBUAG8AbwBsAEIAYQByAQAAAAD/////AAAAAAAAAAAAAAADAAAAAQAAABYAbgBlAHcAcwBUAG8AbwBsAEIAYQByAQAAAAD/////AAAAAAAAAAA=\n", "MaxMemAlloc=4096\n", "MinMemAlloc=512\n", "ShownNotifications=\n"]

        file.writelines(config)

    with open("runMinecraft.bat", "w") as file:
        file.writelines(["@echo off\n","python setup.py MultiMC\n","cd UltimMC\n", "UltimMC.exe"])

    
#allow bat file to update hostname in multimc config as well as make sure everything is installed properly
if len(sys.argv) > 1:
    if(sys.argv[1] == "MultiMC"):
        installMultiMC()
        sys.exit()
    
    if(sys.argv[1] == "TL"):
        installCracked()
        sys.exit()



#get java and unpack to ./java
if(not os.path.exists("java")):

    print("Setting up Java!")
     
    #check for java zip file and hash
    if(not os.path.exists("java19.zip") and not os.path.exists("java19.sha256")):
        downloadJava()

    #verify downloaded zip
    with open("java19.sha256", 'r') as hashfile:
        javaHash = subprocess.check_output(["certutil", "-hashfile", "java19.zip", "SHA256"]).decode('utf-8').splitlines()[1]
        verifyHash = hashfile.read()
        #print(javaHash)

        if(not verifyHash == javaHash):
            print("Something went wrong! Redownloading...\n\n\n")
            hashfile.close()
            downloadJava()

    with zipfile.ZipFile("java19.zip", 'r') as javaZip:
        javaZip.extractall("java")

    java_numbered_dir = "./java/" + os.listdir("java")[0]

    #put everything in ./java instead of java-19. whatever 
    moveFolder("./java/" + os.listdir("java")[0], "./java")
    os.rmdir(java_numbered_dir) #get rid of useless java version folder


#Get input for multiMC or cracked version of minecraft to use

launcher = input("Download MultiMC or TL Legacy? (M/t)").casefold()
print(launcher)

if stringInArray(launcher, ["multi", 'm', "multimc"]):
    print("MULTIMC")
    installMultiMC()
    os.system("runMinecraft.bat")

if stringInArray(launcher, ['tl', 't', 'cracked', 'crack']):
    print("TLAUNCHER")
    installCracked()
    os.system("runMinecraft.bat")