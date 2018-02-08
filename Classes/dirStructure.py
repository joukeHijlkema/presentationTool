#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
# dirStructure
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Jan 19 12:39:33 2017
#   - Initial Version 1.0
#  =================================================
import os
import shutil
import subprocess
import sys
from colorama import Fore, Back, Style

class dirStructure:
    def __init__(self,Params,Coords,progBase,root=""):
        "create the directory structure of the presentation at the root"
        self.parseParams(Params)
        self.nbImages = 0
        if root=="":
            self.root = Params.get("root")
        else:
            self.root=root
        self.mkdir(self.root)
        for d in ["CSS","JS","IMAGES","VIDEO"]:
            self.mkdir("%s/%s"%(self.root,d))
            
        # copy the javascript
        shutil.copyfile("%s/javaScript/impress.js/js/impress.js"%progBase,"%s/JS/impress.js"%self.root)
        shutil.copyfile("%s/javaScript/myImpress.js"%progBase,"%s/JS/myImpress.js"%self.root)
        shutil.copyfile("%s/javaScript/vector.js"%progBase,"%s/JS/vector.js"%self.root)
        shutil.copyfile("%s/javaScript/pdf.js"%progBase,"%s/JS/pdf.js"%self.root)
        for f in ["jqmath-0.4.3.css","jqmath-etc-0.4.5.min.js","jquery-1.4.3.min.js"]:
            shutil.copyfile("%s/javaScript/mathscribe/%s"%(progBase,f),"%s/JS/%s"%(self.root,f))

        # copy the css
        shutil.copyfile("%s/CSS/Global.css"%progBase,"%s/CSS/Global.css"%self.root)
        shutil.copyfile("%s/CSS/Init.css"%progBase,"%s/CSS/Init.css"%self.root)
        shutil.copyfile("%s/CSS/Onera.css"%progBase,"%s/CSS/Presentation.css"%self.root)
        shutil.copyfile("%s/CSS/Positioning.css"%progBase,"%s/CSS/Positioning.css"%self.root)
        shutil.copyfile("%s/CSS/Pdf.css"%progBase,"%s/CSS/Pdf.css"%self.root)
        shutil.rmtree("%s/CSS/CONTENT"%self.root,True)
        shutil.copytree("%s/CSS/Content"%progBase,"%s/CSS/CONTENT"%self.root)

        self.convertImages = Params.get("convertImages")=="True" if "convertImages" in Params.attrib else False
        
        if "css" in Params.attrib:
            shutil.copy(Params.get("css"),"%s/CSS/Presentation.css"%self.root)
        if "backgrounds" in Params.attrib:
            Items = eval(Params.get("backgrounds"))
            for i in Items:
                print(i)
                self.cpImage(Items[i],Coords.W,Coords.H,fileName=i)
        
    def mkdir(self,path):
        if (os.path.isdir(path)):
            return
        else:
            os.makedirs(path)

    ## --------------------------------------------------------------
    ## Description : Parse parameters
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 05-56-2017 13:56:30
    ## --------------------------------------------------------------
    def parseParams (self,Params):
        self.templates=Params.get('templates')
        self.imageRoot=Params.get('imageRoot')
        self.videoRoot=Params.get('videoRoot')
        for i in Params.attrib:
            new = Params.get(i)
            for r in ["templates","imageRoot","videoRoot"]:
                new = new.replace("#%s#"%r,Params.get(r))
            Params.set(i,new)
            
    ## --------------------------------------------------------------
    ## Description :kill a file
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 29-02-2017 19:02:55
    ## --------------------------------------------------------------
    def rm (self,path):
        os.system("rm %s"%path)

    ## --------------------------------------------------------------
    ## Description :copy a video
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-21-2017 14:21:57
    ## --------------------------------------------------------------
    def cpVideo (self,path):
        if os.path.dirname(path)=='':
            path=os.path.join(self.videoRoot,path)

        try:
            shutil.copy(path,"%s/VIDEO/%s"%(self.root,os.path.basename(path)))
        except:
            print(Fore.WHITE+Back.RED+"!!!! ERROR !!!!"+Style.RESET_ALL)
            print(sys.exc_info()[0])
            
        return "VIDEO/%s"%os.path.basename(path)

    ## --------------------------------------------------------------
    ## Description :copy an image
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-28-2017 14:28:36
    ## --------------------------------------------------------------
    def cpImage (self,path,W,H,target="IMAGES",fileName=""):

        if os.path.dirname(path)=='':
            path=os.path.join(self.imageRoot,path)
        
        bn  = os.path.basename(path)
        if fileName=="":
            fn  = os.path.splitext(bn)[0].lower()
        else:
            fn = fileName

        ext = os.path.splitext(bn)[1].lower()
        if ext in [".svg"]:
            newExt="svg"
        else:
            newExt="png"
        
        outFileShort = "%s/%s.%s"%(target,fn,newExt)
        outFileLong  = "%s/%s/%s.%s"%(self.root,target,fn,newExt)

        if  os.path.isfile(outFileLong):
            print("%s exists, doing nothing"%outFileLong)
        elif self.convertImages==True:
            if ext in [".jpg",".jpeg",".png",".tiff",".bmp"]:
                cmd= ['convert','-resize','%sx%s>'%(W,H),path,"%s"%outFileLong]
            elif ext in [".svg"]:
                # cmd = ['inkscape','-z','-e',outFileLong,path]
                cmd = ['cp',path,outFileLong]
            else:
                print("don't know what to do with %s, skipping"%path)

            print("converting %s to %s (%sx%s) using : %s"%(path,outFileShort,W,H," ".join(cmd)))
            try:
                subprocess.check_output(cmd,stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print(Fore.WHITE+Back.RED+"!!!! ERROR !!!!"+Style.RESET_ALL)
                print(e)
                print(e.output)
        else:
            print("not converting %s to %s"%(path,outFileShort))
            shutil.copy(path,outFileLong)

        return outFileShort

