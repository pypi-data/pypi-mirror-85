# -*-encoding:utf-8-*-
import os
import json
import configparser
import sys
from onebrain.utils.requeststool import  RequestsTool
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib3 import encode_multipart_formdata
from onebrain.utils.process import ShowProcess
from onebrain.utils.config import BASE_DIR
chunkSize = 5096000
ONEBRAIN = "ONEBRAIN"
ONEBRAIN_MERGE = "ONEBRAIN_MERGE"
FILE_TAG="file:"
CHUNK_TAG="chunk:"


def getChunkSize():
    return chunkSize

def setChunkSize(size):
    chunkSize = size

def getFileSize(file):
    file.seek(0, os.SEEK_END)
    fileLength = file.tell()
    file.seek(0, 0)
    return fileLength

def getAllFiles(path):
    result = []  # 所有的文件
    pathLen = len(path)
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            apath = apath[pathLen:]
            apath = apath.replace('\\', "/")
            if apath.startswith("/"):
                apath = apath[1:]
            result.append(apath)
        # for filename in subdir:
        #
        #     apath = os.path.join(maindir, filename)  # 合并成一个完整路径
        #     print("filename=" + apath)
        #     r = getAllFiles(apath)
        #     result.extend(r)
    return result

#保存进展
def saveFileProgress(id,fileName):
    file =BASE_DIR+"/"+id
    if os.path.exists(file) == False:
        with open(file, 'w') as f:
            f.writelines(FILE_TAG+fileName+"\n")
    else:
        with open(file, 'a') as f:
            f.writelines(FILE_TAG+fileName+"\n")

#保存chunk进展
def saveChunkProgress(id,chunkName):
    file =BASE_DIR+"/"+id
    if os.path.exists(file) == False:
        with open(file, 'w') as f:
            f.writelines(CHUNK_TAG+chunkName+"\n")
    else:
        with open(file, 'a') as f:
            f.writelines(CHUNK_TAG+chunkName+"\n")

def readProgress(id):
    file =BASE_DIR+"/"+id
    fileDict = {}
    chunkDict = {}
    if os.path.exists(file) == False:
        return fileDict,chunkDict
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            if line.startswith(FILE_TAG):
                fileDict[line[len(FILE_TAG):]]=True
            if line.startswith(CHUNK_TAG):
                chunkDict[line[len(CHUNK_TAG):]] = True
            line = f.readline()
    return fileDict, chunkDict

def getFileName(fileFullPath):
    index = fileFullPath.rindex('\\')
    if index == -1:
        return fileFullPath
    else:
        return fileFullPath[index + 1:]

def mergeFile(fileName,type,path):
    data = {
        "fileName": fileName,
        "path": path,
        "type": type
    }
    rq = RequestsTool()
    url = "/api/1/file/merge"
    re = rq.post(url, data)
    if  'status' in re and re['status'] == 200:
        print(fileName + " merge success")
        return True
    else:
        print(fileName+" error")
        print(re)
        return False

def getTotalSize(path, finishFiles):
    if path.endswith("/")==False:
        path = path + "/"
    targetFiles = getAllFiles(path)
    totalSize = 0
    for item in targetFiles:
        with open(path+item, 'a') as f:
            fileSize = getFileSize(f)
            totalChunks = int(fileSize / chunkSize)
            lastSize = fileSize % chunkSize
            if lastSize != 0:
                totalChunks = totalChunks + 1
            if totalChunks == 0:
               totalChunks =1
            totalSize = totalSize + totalChunks
    return totalSize

def fileChunckUpLoad(path,apiUrl,fileName, chunkNumber, totalChunks, fileLength):
    file = open(path+fileName, "rb")
    file.seek(chunkSize*(chunkNumber-1))
    fileData = file.read(chunkSize)

    m = MultipartEncoder(
        fields={
            'chunkNumber': str(chunkNumber),
            'chunkSize': str(chunkSize),
            'currentChunkSize': str(len(fileData)),
            'totalSize': str(fileLength),
            'filename': fileName,
            'relativePath': fileName,
            'totalChunks': str(totalChunks),
            'file': ('test01.xlsx', fileData,
                                    'application/octet-stream')
        })
    rq = RequestsTool()
    re = rq.upload(apiUrl, data=m)
    if  'status'in re and re['status'] == 200:
        print(fileName+str(chunkNumber)+" success")
        return True
    print(fileName+str(chunkNumber)+" error")
    print(re)
    return False

def uploadPathFiles(id,type,uuid, path,resume=True):
    if path.endswith("/")==False:
        path = path + "/"
    targetFiles = getAllFiles(path)
    finishFiles = {}
    finishChunk = {}
    apiUrl = "/api/1/file/upload?type="+type+"&uuid="+uuid
    if resume:
        if os.path.exists(BASE_DIR +"/"+ id):
            finishFiles ,finishChunk = readProgress(id)
    finish = False
    finishSize = 0
    totalSize = getTotalSize(path,finishFiles)
    if totalSize == 0:
        print("没有文件需要上传")
        return
    max_steps = totalSize
    process_bar = ShowProcess(max_steps, 'OK')
    while finish == False:
        error = False
        for item in targetFiles:
            with open(path+item, 'a') as f:
                fileSize = getFileSize(f)
                totalChunks = int(fileSize / chunkSize)
                lastSize = fileSize % chunkSize
                if lastSize != 0:
                   totalChunks = totalChunks + 1
                if totalChunks == 0:
                    totalChunks = totalChunks + 1
                if item in finishFiles.keys():
                    finishSize = finishSize + totalChunks
                    process_bar.show_process(finishSize)
                    continue
                if totalChunks == 1 or totalChunks == 0 :
                    result = fileChunckUpLoad(path, apiUrl, item, 1, 1, fileSize)
                    if result == True:
                        finishFiles[item] = True
                        saveFileProgress(id,item)
                        finishSize = finishSize +1
                        process_bar.show_process(finishSize)
                    else:
                        error = True
                else:
                   chunkError = False
                   for i in range(totalChunks):
                       key = item + "/" + str(i+1)
                       if key in finishChunk.keys():
                           finishSize = finishSize + 1
                           continue
                       result = fileChunckUpLoad(path,apiUrl,item,i+1,totalChunks,fileSize)
                       if result == True:
                            finishChunk[key] = True
                            saveChunkProgress(id, key)
                            finishSize = finishSize + 1
                            process_bar.show_process(finishSize)
                       else:
                           error = True
                           chunkError = True
                   if chunkError == False:
                           result = mergeFile(item,type, uuid)
                           if result == True:
                               finishFiles[item] = True
                               saveFileProgress(id, item)
                           else:
                               error = True

        if error == False:
            finish = True

if __name__ == "__main__":
    filePath ="c:/Users/like/Downloads"
    fileName = "bs.png"
    file = open(filePath+"/"+fileName,"rb")
    fileSize = getFileSize(file)
    totalChunks = int(fileSize/chunkSize)
    if fileSize % chunkSize != 0:
        totalChunks = totalChunks+1
    apiUrl="/api/1/file/upload?type=dataset&uuid=bfe9b8f8b3ab62ce876069fa71b1eead"
    fileChunckUpLoad(apiUrl, fileName, 1, totalChunks, fileSize)
