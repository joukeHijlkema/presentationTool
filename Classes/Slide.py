#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
# Slide
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Jan 19 13:05:20 2017
#   - Initial Version 1.0
#  =================================================
from lxml import etree
import re

class Slide:
    def __init__(self,s,Coords,Dirs,number):
        "create a new slide"

        self.parseSlide(s)
        self.Dirs   = Dirs
        self.Coords = Coords
        
        self.source = etree.Element('div')
        
        self.source.set("data-x","%s"%Coords.X)
        self.source.set("data-y","%s"%Coords.Y)

        self.source.set("data-scale",s.get("scale") if "scale" in s.attrib else "1.0")
        self.source.set("data-rotate-z",s.get("rotateZ") if "rotateZ" in s.attrib else "0.0")
        self.source.set("data-rotate-y",s.get("rotateY") if "rotateY" in s.attrib else "0.0")
        self.source.set("data-rotate-x",s.get("rotateX") if "rotateX" in s.attrib else "0.0")
        
        self.source.set('data-title',s.get("title") if "title" in s.attrib else "")
        self.source.set('data-subtitle',s.get("subtitle") if "subtitle" in s.attrib else "")
        self.source.set('data-number',"%s"%number)
        self.inPlan = s.get('inPlan') if 'inPlan' in s.attrib else None
        self.Done   = eval(s.get("done")) if "done" in s.attrib else [] 
        self.type   = s.get('type')

        if self.type == "firstSlide":
            self.source.set('class','step slide first_slide')
        elif self.type == "titleSlide":
            self.source.set('class','step slide title')
            h1      = etree.Element('h1')
            h1.set("class","hcenter")
            h1.text = s.get('presTitle')
            h2      = etree.Element('h2')
            h2.text = s.get("subTitle")
            h3      = etree.Element('h3')
            h3.text = s.get('author')
            self.source.append(h1)
            self.source.append(h2)
            self.source.append(h3)
        elif self.type=="plan":
            self.source.set('class','step slide plan')
            self.entreePlan = etree.Element('ul')
            self.source.append(self.entreePlan)
        else:
            self.source.set('class','step slide')

        if "class" in s.attrib:
            self.source.set('class',"%s %s"%(self.source.get("class"),s.get("class")))

        if "id" in s.attrib:
            self.source.set('id',s.get('id'))
        else:
            self.source.set('id',"slide_%d"%number)

        for i in s:
            self.source.append(self.chose(i))

    ## --------------------------------------------------------------
    ## Description : Parse slide
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 05-56-2017 13:56:30
    ## --------------------------------------------------------------
    def parseSlide (self,Slide):
        for i in Slide.attrib:
            new = Slide.get(i)
            for r in ["templates","imageRoot","videoRoot"]:
                if "#%s#"%r in new:
                    new = new.replace("#%s#"%r,Slide.get(r))
            Slide.set(i,new)

    ## --------------------------------------------------------------
    ## Description :chose what item this is
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 20-26-2017 15:26:56
    ## --------------------------------------------------------------
    def chose (self,i) -> etree._Element:

        out=None
        if i.tag=="textBox":
            out = self.generic(i,'div')
        elif i.tag=="bList":
            out = self.generic(i,'ul')
        elif i.tag=="i":
            out = self.generic(i,'li')
        elif i.tag=="video":
            out = self.video(i)
        elif i.tag=="video-overlay":
            out = self.videoOverlay(i)
        elif i.tag=="figure":
            out = self.figure(i)
        elif i.tag=="plan":
            out = self.plan(i)
        elif i.tag == "table":
            out=self.generic(i,'table')
        elif i.tag=="row":
            out=self.generic(i,'tr')
        elif i.tag=="tableHead":
            out=self.generic(i,'th')
        elif i.tag=="cell":
            out=self.generic(i,'td')
        else:
            out=self.generic(i,i.tag)
            # print("!! used generic %s"%i.tag) 

        if "class" in i.attrib:
            out.set("class","%s %s"%(i.tag,i.get("class")))
        else:
            out.set("class","%s"%i.tag)
        if "style" in i.attrib:
            out.set("style",i.get("style"))
        if "id" in i.attrib:
            out.set("id",i.get("id"))
        if "width" in i.attrib:
            out.set("width",i.get("width"))

        return out

    ## --------------------------------------------------------------
    ## Description :table row
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 26-14-2017 16:14:47
    ## --------------------------------------------------------------
    def generic (self,s,tag):
        out          = etree.Element(tag)
        lines        = s.text.split("\\\\")
        out.text     = self.parse(lines[0])
        for i in range(1,len(lines)):
            br       = etree.SubElement(out, "br")
            br.tail  = self.parse(lines[i])
        for i in s:
            out.append(self.chose(i))
        return out

    ## --------------------------------------------------------------
    ## Description :get dimensions
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 24-44-2017 15:44:41
    ## --------------------------------------------------------------
    def getDim (self,s):
        W = self.Coords.W
        H = self.Coords.H
        
        if "style" in s.attrib:
            styles = s.get("style")
            for rule in styles.split(";"):
                key=rule.split(":")[0]
                val=rule.split(":")[1][:-1]
                if key == "width":
                    W *= 0.01*float(val)
                elif key == "height":
                    H *= 0.01*float(val)
        return [W,H]


    ## --------------------------------------------------------------
    ## Description :make a figure
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-32-2017 15:32:45
    ## --------------------------------------------------------------
    def figure (self,s):
        [W,H] = self.getDim(s)
        if "cap" in s.attrib:
            out = etree.Element('figure')
            fc = etree.Element("figcaption")
            fc.text=s.get("cap")
            out.append(fc)
        else:
            out = etree.Element('div')

        im = etree.Element("img")
        im.set("src",self.Dirs.cpImage(s.get('src'),W,H))
        im.set("width","100%")
        
        out.append(im)
            
        return out
    
    ## --------------------------------------------------------------
    ## Description :make a video overlay
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-17-2017 15:17:00
    ## --------------------------------------------------------------
    def videoOverlay (self,s):
        out = etree.Element('div')
        im = etree.Element('img')
        [W,H] = self.getDim(s)
        im.set('src',self.Dirs.cpImage(s.get('src'),W,H))
        if "width" in s.attrib:
            im.set("width",s.get("width"))
        if "height" in s.attrib:
            im.set("height",s.get("width"))
        out.append(im)
        return out
        
    ## --------------------------------------------------------------
    ## Description :make a video box
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 22-02-2017 14:02:49
    ## --------------------------------------------------------------
    def video (self,s) -> etree._Element:
        out = etree.Element('div')
        v = etree.Element('video')
        v.set("src",self.Dirs.cpVideo(s.get("src")))
        v.set('controls','controls')
        v.set('loop','loop')
        out.append(v)
        return out

    ## --------------------------------------------------------------
    ## Description :parse text for special characters
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 24-38-2017 14:38:25
    ## --------------------------------------------------------------
    def parse (self,txt):
        subs = {
            "#Rarrow#":u"\u2192",
            "#RDarrow#":u"\u21D2"
        }
        for s in subs:
            txt=txt.replace(s,subs[s])
        return txt
