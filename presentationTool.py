#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  =================================================
# presentationsTool
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Jan 19 12:38:12 2017
#   - Initial Version 1.0
#  =================================================
## ========= TODO =============
## - APearences on one slide
## ============================

import sys
from lxml import etree, objectify
from collections import OrderedDict

import Classes.dirStructure as dirStructure
from Classes.Slide import Slide
from Classes.Coords import Coords
from Classes.Template import Template

import math

import pdfkit
import os

from colorama import Fore, Back, Style

print(Fore.WHITE+Back.BLUE+"!!!! Starts parsing !!!!"+Style.RESET_ALL)

# read the script
parser = etree.XMLParser(remove_comments=True)
script   = objectify.parse(sys.argv[1],parser=parser).getroot()
progBase = os.path.dirname(os.path.realpath(sys.argv[0]))
params   = script.find("./parameters")
myCoords = Coords(params)

myDirStruct = dirStructure.dirStructure(params,myCoords,progBase)

#construct the slides
Slides    = []
counter   = 0
if "lastSlide" in params.attrib:
    lastSlide = params.get("lastSlide")
else:
    lastSlide = len(script.findall("./slide"))-1

print("lastSlide = %s"%lastSlide)

for s in script.findall("./slide"):
    title = "%s"%s.get("title")
    print ("found slide with title '%s'"%title.encode("utf-8"))
    myCoords.update(s)
    newSlide = Slide(s,myCoords,myDirStruct,counter,lastSlide)
    Slides.append(newSlide)
    counter+=1

#fill the outlines
planElements=OrderedDict()
for s in Slides:
    if s.inPlan:
        print("in plan : %r"%s.inPlan.encode('utf-8'))
        items = s.inPlan.split("/")
        chap  = items[0]
        if len(items)>1:
            sect = items[1]
        else:
            sect =""
        if chap in planElements:
            planElements[chap].append([sect,s.source.get('id')])
        else:
            if sect!="":
                planElements[chap]=[[sect,s.source.get('id')]]
            else:
                planElements[chap]=''
for s in Slides:
    if s.type == "plan":
        counter=0
        for chap in planElements:
            print("adding %s"%chap.encode('utf-8'))
            i1 =etree.Element('li')
            i1.text=chap
            if len(planElements[chap])>0:
                u  = etree.Element('ul')
                i1.append(u)
                for sect in planElements[chap]:
                    print("-- adding %s"%sect)
                    i2 = etree.Element('li')
                    i2.text = sect[0]
                    i2.set("data-target","#%s"%sect[1])
                    
                    if counter in s.Done:
                        i2.set("class","raise done")
                    else:
                        i2.set("class","raise")
                    u.append(i2)
                    counter+=1
            s.entreePlan.append(i1)
                

# read the template
template = Template("%s/Templates/presentation.html"%progBase,params,myDirStruct)
for s in Slides:
    template.append(s)
    
# write the presentation file
template.write("%s/presentation.html"%myDirStruct.root)

# make a pdf aswell
if "makePdf" in params.attrib and params.get("makePdf") == "True":
    options = {
        'encoding': "UTF-8",
        'viewport-size':'%sx%s'%(myCoords.W,myCoords.H),
        'page-height':'%d'%(math.floor(0.6*myCoords.H)),
        'page-width':'%d'%(math.floor(0.6*myCoords.W)),
        'javascript-delay':1000,
        'disable-smart-shrinking':None
    }

    files=[]
    counter=0
    for s in Slides:
        pdf = Template("Templates/pdf.html",params,myDirStruct)
        pdf.append(s)
        fn = "%s/pdf_%d.html"%(myDirStruct.root,counter)
        pdf.write(fn)
        files.append(fn)
        print("added slide %d"%counter)
        counter+=1
    
    pdfkit.from_file(files,'%s/presentation.pdf'%myDirStruct.root,options=options)

    counter=0
    for s in Slides:
        myDirStruct.rm("%s/pdf_%d.html"%(myDirStruct.root,counter))
        counter+=1
    
