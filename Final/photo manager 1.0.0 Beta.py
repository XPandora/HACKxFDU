
#-*- coding:utf8 -*- 
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
import os
import time
import shutil
from Tkinter import *
import Tkinter,Tkconstants,tkFileDialog

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='b1b41aa110822a1480943e38565b5e226abf89e9')
usefulTags = ['person','fruit','food','animal','sky','female','tree','nature','rainbow','building','dog']

def Classify(rootdir):
    list = os.listdir(rootdir)
    filename=[]
    returns=[]
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            f = open(path,'rb')
            filename.append(path) # list of each file direction
            tempStr=json.dumps(visual_recognition.classify(images_file=f), indent=2)
            returns.append(tempStr) #list of classify result
        print i+1," pictures identified"
    return returns,filename

def Transfer(rootdir):
    l1,l2=Classify(rootdir)
    ##jsondumpsdict list filenamelist
    d1={}
    ##filenamedict ,list of tags inside
    l3=[]
    ##tagslist
    for i in range(0,len(l1)):
        temp = json.loads(l1[i])
        tempName = l2[i]
        tempPic = temp['images'][0]['classifiers'][0]['classes']
        tagNum = len(tempPic)

        for j in range(0,tagNum):
            if 'type_hierarchy' in tempPic[j]:
                continue
            tempTag = tempPic[j]['class']
            tempScore = tempPic[j]['score']

            if tempTag in usefulTags:
                pass
            else:
                continue
            if tempTag in l3:
                pass
            else:
                l3 += [tempTag]
            if tempName in d1:
                d1[tempName] += [tempTag]
            else:
                d1[tempName] = [tempTag]

        if tempName not in d1:
            otherTag = 'other'
            d1[tempName] = [otherTag]
            if otherTag not in l3:
                l3 += [otherTag]

    return d1,l3

def Transfer2(rootdir):
    l1,l2 = Classify(rootdir)
    #jsondumpsdict list filenamelist
    d1 = {}
    #filenamedict key:filename value:tag of highest score
    l3 = []
    #tagslist
    for i in range(0,len(l1)):
        print (i)
        temp = json.loads(l1[i])
        tempName = l2[i]
        tempClasses = temp['images'][0]['classifiers'][0]['classes']
        tagNum = len(tempClasses)

        maxScoreUseful = 0
        for j in range(0,tagNum):
            if 'type_hierarchy' in tempClasses[j]:
                continue
                
            tempTag = tempClasses[j]['class']
            tempScore = tempClasses[j]['score']
        
            if tempTag in usefulTags:
                pass
            else:
                continue

            if tempScore > maxScoreUseful:
                maxScoreUseful = tempScore
                maxTagUseful = tempTag


        if maxScoreUseful > 0:
            d1[tempName] = [maxTagUseful]
            if maxTagUseful in l3:
                pass
            else:
                l3 += [maxTagUseful]
        else:
            otherTag = 'other'
            d1[tempName] = [otherTag]
            if otherTag in l3:
                pass
            else:
                l3 += [otherTag]

    return d1,l3 

class CanvasDemo:
    def __init__(self,w,h):
        
        self.window = Tk() 
        self.window.title("Photo Manager")
        self.canvas = Canvas(self.window, width = w, height = h, bg = "white")
        self.canvas.pack()

        self.flag = 0
        self.sourcepath = ''
        self.targetpath = ''
        
        self.source_opt = options = {}  
        options['initialdir'] = 'C:\\'  
        options['mustexist'] = True  
        options['parent'] = self.window  
        options['title'] = 'Choose source folder'

        self.target_opt = options = {}  
        options['initialdir'] = 'C:\\'  
        options['mustexist'] = True  
        options['parent'] = self.window  
        options['title'] = 'Choose target folder'

        bm = PhotoImage(file='BG.gif')
        self.frame = PhotoImage(file='frame.gif')
  
        self.canvas.create_image(600,450,image = bm)
        self.canvas.create_image(373,624,image = self.frame,tag='f1')
        
        self.sourcedir = self.canvas.create_text(w*0.90,h*22/45,text = "           \n             \n              \n              ",anchor = E)
        self.targetdir = self.canvas.create_text(w*0.90,h*3/5,text = "           \n             \n              \n              ",anchor = E)
        self.runbt = self.canvas.create_text(w*0.90,h*0.71,text = "      \n             \n              \n        ",anchor = E)
        
        self.canvas.tag_bind(self.sourcedir,'<Button-1>',lambda event,tag = self.canvas.gettags(self.sourcedir):self.sourcedirectory())
        self.canvas.tag_bind(self.targetdir,'<Button-1>',lambda event,tag = self.canvas.gettags(self.targetdir):self.targetdirectory())
        self.canvas.tag_bind(self.runbt,'<Button-1>',lambda event,tag = self.canvas.gettags(self.runbt):self.run())

        self.classifybt = self.canvas.create_text(w*0.186,h*2/3,text = "                                                                             \n                                                                              ",anchor = NW,justify = CENTER)
        self.classifybt2 = self.canvas.create_text(w*0.555,h*2/3,text = "                                                                             \n                                                                              ",anchor = NW,justify = CENTER)
        self.canvas.tag_bind(self.classifybt,'<Button-1>',lambda event,tag = self.canvas.gettags(self.classifybt):self.imageclassify())
        self.canvas.tag_bind(self.classifybt2,'<Button-1>',lambda event,tag = self.canvas.gettags(self.classifybt2):self.imageclassify2())
        
        self.pathlabel = self.canvas.create_text(w*0.196,h*0.48,text="Source File Path",font=("微软雅黑",20,""),anchor = NW,justify = CENTER)
        self.pathlabe2 = self.canvas.create_text(w*0.196,h*0.58,text="Target  File Path",font=("微软雅黑",20,""),anchor = NW,justify = CENTER)

        
        
        self.window.mainloop()


    def sourcedirectory(self):  

        temp = tkFileDialog.askdirectory(**self.source_opt)
        if (temp==""):
            return
        self.sourcepath = temp
        self.canvas.itemconfig(self.pathlabel,text = self.sourcepath)

        self.targetpath = self.sourcepath
        self.canvas.itemconfig(self.pathlabe2,text = self.targetpath)

    def targetdirectory(self):  

        temp = tkFileDialog.askdirectory(**self.target_opt)
        if (temp==""):
            return
        self.targetpath = temp
        self.canvas.itemconfig(self.pathlabe2,text = self.targetpath)

    def imageclassify(self):
        self.flag = 0
        self.canvas.delete('f1')
        self.canvas.create_image(373,624,image = self.frame,tag='f1')
        
        print ("Classification1")        

    def imageclassify2(self):
        self.flag = 1
        self.canvas.delete('f1')
        self.canvas.create_image(820,624,image = self.frame,tag='f1')
        
        print ("Classification2")

    def run(self):
        print ("Completed")
        if(self.flag == 0):
            pic_tag,tag_list=Transfer(self.sourcepath)
            os.chdir(self.targetpath)
            for tag in tag_list:
                os.mkdir(tag)
            for pic in pic_tag:
                for tag in pic_tag[pic]:
                    shutil.copy(pic,tag)
        else:
            pic_tag,tag_list=Transfer2(self.sourcepath)
            os.chdir(self.targetpath)
            for tag in tag_list:
                os.mkdir(tag)
            for pic in pic_tag:
                for tag in pic_tag[pic]:
                    shutil.copy(pic,tag)

def main():
    CanvasDemo(1200,900)
    
    return
  
main()
