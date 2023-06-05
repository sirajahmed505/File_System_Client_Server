import os
import threading
import sys
import json
import pickle

filesInUse = []
#get current working directory of process
root = os.getcwd()
global datdict
datdict = {}
#to avoid concurrent modifies
lock = threading.Lock()
global clientInfo
clientInfo = {
    'message': ''
}


def thread_function(user_response):
    user_response = user_response.strip()
    user_response = user_response.split(' ')
    if user_response[0] == 'create':
        createFile(user_response[1])
    elif user_response[0] == 'delete':
        deleteFile(user_response[1])
    elif user_response[0] == 'makeDir':
        makeDirectory(user_response[1])
    elif user_response[0] == 'changeDir':
        changeDirectory(user_response[1])
    if user_response[0] == 'open':
        user_response[1] = user_response[1].replace("<", "")
        user_response[1] = user_response[1].replace(">", "")
        user_response[1] = user_response[1].replace("\n", "")
        args = user_response[1].split(',')
        openFile(args[0], args[1])
    elif user_response[0] == 'read_from_file':
        user_response[1] = user_response[1].replace("<", "")
        user_response[1] = user_response[1].replace(">", "")
        user_response[1] = user_response[1].replace(",", "")
        user_response[1] = user_response[1].replace("\n", "")
        user_response[2] = user_response[2].replace(",", "")
        user_response[3] = user_response[3].replace("\n", "")
        openFile(user_response[1], 'x', '', user_response[2], user_response[3])
    elif user_response[0] == 'close':
        user_response[1] = user_response[1].replace("<", "")
        user_response[1] = user_response[1].replace(">", "")
        user_response[1] = user_response[1].replace("\n", "")
        args = user_response[1].split(',')
        closeFile(args[0])
    elif user_response[0] == 'write_to_file':
        user_response[2] = ' '.join(user_response[2:])
        user_response[1] = user_response[1].replace("<", "")
        user_response[1] = user_response[1].replace(">", "")
        user_response[1] = user_response[1].replace("\n", "")
        user_response[1] = user_response[1].replace(",", "")
        user_response[2] = user_response[2].replace(",", "")
        user_response[2] = user_response[2].replace("\n", "")
        openFile(user_response[1], 'w', user_response[2])
    elif user_response[0] == 'write_at':
        user_response[1] = user_response[1].replace("<", "")
        user_response[1] = user_response[1].replace(">", "")
        user_response[1] = user_response[1].replace("\n", "")
        user_response[1] = user_response[1].replace(",", "")
        more_text = a[2:-1]
        user_response[3] = user_response[3].replace("\n", "")
        user_response[3] = user_response[3].replace(",", "")
        user_response[4] = user_response[4].replace("\n", "")
        more_text = ' '.join(more_text)
        openFile(user_response[1], 'w', more_text, user_response[-1])
    elif user_response[0] == 'truncate_file':
        truncateFile(user_response[1], user_response[2])
    elif user_response[0] == 'mov':
        moveFile(user_response[1], user_response[2])
    elif user_response[0] == 'show_mmap':
        showDat()
    elif user_response[0] == 'exit':
        sys.exit(0)
    else:
        clientInfo


def showDat():
    readDat()
    clientInfo["message"] = ""
    for key in datdict:
        clientInfo["message"] += key + " " + datdict[key] + "\n"


def saveDat():
    file = open(root+"/" + "dat.dat", "w")
    for key in datdict:
        file.write(key + "#" + datdict[key] + "\n")
    file.close()


def writeDat(filename):
    readDat()
    file = open(filename, "r")
    content = file.read()
    datdict[filename] = content
    saveDat()


def readDat():

    if os.path.isfile(root+"/"+"dat.dat"):
        file = open(root+"/"+"dat.dat", "r")
        for line in file:
            if '#' in line:
                (key, val) = line.split('#', 1)
                datdict[key] = val

        file.close()

    else:
        file = open(root+"/"+"dat.dat", "w")
        file.close()


def createFile(filename):
    file = open(filename, "w")
    file.close()
    writeDat(filename)
    clientInfo["message"] = 'File ' + filename + ' created successfully!'


def deleteFile(filename):
    print(filesInUse)
    if filename not in filesInUse:
        datdict.pop(filename)
        print(filename)
        os.remove(filename)
        clientInfo["message"] = 'File ' + filename + ' deleted successfully!'
    else:
        clientInfo["message"] = 'File ' + filename + ' is in use!'


def makeDirectory(directory):
    if os.path.isdir(directory):
        print("Directory already exists!!!")
        clientInfo["message"] = "Directory already exists!!!"
    else:
        directoryName = root + "/" + directory
        print(directoryName)
        clientInfo["message"] = "Directory created successfully --> " + directoryName
        os.mkdir(directoryName)


def changeDirectory(directory):

    if directory == "..":
        directoryName = root
    else:
        directoryName = root + "/" + directory
        directoryName = directoryName.replace("\n", "")
    print(directoryName)
    clientInfo["message"] = "Directory changed successfully!"
    if os.path.isdir(directoryName):
        os.chdir(directoryName)
        clientInfo["message"] = "Directory changed successfully to " + directoryName
    else:
        print("Directory does not exist!")
        clientInfo["message"] = "Directory does not exist!"


def moveFile(filename, destination):
    lock.acquire()

    if os.path.exists(filename):
        if filename in filesInUse:
            print("File is in use, cannot be moved!")
            clientInfo["message"] = "File is in use, cannot be moved!"
        else:
            directoryName = root + "/" + destination
            if os.path.isdir(directoryName):
                os.rename(filename, directoryName + "/" + filename)
                clientInfo["message"] = "File moved successfully to " + \
                    directoryName
            else:
                print("Directory does not exist!")
                clientInfo["message"] = "Directory does not exist!"

    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"

    lock.release()


def openFile(filename, mode, content='', startingIndex=0, size=0):
    fileName = filename
    if os.path.exists(filename):
        match mode:

            case 'w':
                #<< this if else condition implements synchronization >>
                #<< can not write to file if the file is fileInUse array >>
                if filename not in filesInUse:
                    file = open(filename, "r")
                    filesInUse.append(file)
                    contents = file.read()
                    filesInUse.remove(file)
                    file.close()
                    contents = str(contents)
                    if int(startingIndex) > len(contents):
                        startingIndex = len(contents)

                    contents = contents[:int(startingIndex)] + \
                        content + contents[int(startingIndex):]
                    file = open(filename, "w")
                    filesInUse.append(file)
                    if (startingIndex == 0):
                        file.write(content)
                    else:
                        file.write(contents)
                    if filename in filesInUse:
                        filesInUse.remove(filename)
                    file.close()
                    clientInfo["message"] = "File written to successfully!"
                else:
                    print("File is in use, cannot be written to!")
                    clientInfo["message"] = "File is in use, cannot be written to!"
            #<< no need to implement synchronization in case of read only >>
            case 'r':
                filename = open(filename, "r")
                filesInUse.append(fileName)
                print("Contents of " + fileName +
                      ": " + filename.read())
                clientInfo["message"] = "Contents of " + \
                    fileName + ":\t" + filename.read()
                filename.close()
            case 'x':
                file = open(filename, "r")
                filesInUse.append(file)
                index = startingIndex
                length = size
                contents = file.read()
                print(contents[int(index):int(index) + int(length)])
                clientInfo["message"] = contents[int(
                    index):int(index) + int(length)]
                file.close()

            case _:
                print("Invalid mode!")
                clientInfo["message"] = "Invalid mode!"

        writeDat(fileName)
    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"

def truncateFile(filename, size):
    if os.path.exists(filename):
        fileSize = os.path.getsize(filename)
        if int(size) < fileSize:
            file = open(filename, "r+")
            filesInUse.append(file)
            file.truncate(int(size))
            filesInUse.remove(file)
            file.close()
            writeDat(filename)
        else:
            print("The position you entered exceeds file length!")
            clientInfo["message"] = "The position you entered exceeds file length!"
    else:
        print("File does not exist!")
        clientInfo["message"] = "File does not exist!"


def closeFile(filename):
    if filename in filesInUse:
        filesInUse.remove(filename)
    else:
        print("File is not open!")
        clientInfo["message"] = "File is not opened!"


def memoryMap():
    arr = {}
    #os.walk() creates tree structure of the directory
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            file = open(os.path.join(root, name), "r")
            arr[os.path.join(root, name)] = hex(id(file))

        for name in dirs:
            if os.path.isdir(os.path.join(root, name)) == False:
                file = open(os.path.join(root, name), "r")
                arr[os.path.join(root, name)] = hex(id(file))

        clientInfo["message"] = ''
        for key, value in arr.items():
            print(key + ':\t' + value+'\n')
            clientInfo["message"] += key + ':\t' + value+'\n'


if __name__ == "__main__":
    filenames = ['fileOfText.txt','siraj.txt','file1.txt']

    nThreads = int(sys.argv[1])
    print("Threads: " + str(nThreads))

    for i in range(nThreads):
        f = open(filenames[i], "r")
        lines = f.readlines()

        t = threading.Thread(target=thread_function, args=[i, lines])
        t.start()

