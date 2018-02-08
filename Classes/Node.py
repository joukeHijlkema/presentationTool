#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - lun. févr. 11:48 2018
#   - Initial Version 1.0
#  =================================================
from lxml import etree
import uuid
import os

## =========================================================
## The base class
class Node():
    def __init__(self,tag,s,top):
        "add a text box"
        self.Coords = top.Coords
        self.node = etree.Element(tag)
        self.node.set("class",s.tag)
        for a in s.attrib:
            old = ""
            if a in self.node.attrib:
                old = self.node.attrib.get(a)
            
            self.node.set(a,("%s %s"%(s.get(a),old)).strip())
        
        if hasattr(s,'text') and s.text != None: 
            lines          = s.text.split("\\\\")
            self.node.text = self.parse(lines[0])
            for i in range(1,len(lines)):
                br         = etree.SubElement(self.node, "br")
                br.tail    = self.parse(lines[i])

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

## =========================================================
## A box class
class box(Node):
    def __init__(self,s,top):
        "add a box"
        super(box, self).__init__("div",s,top)

        if "title" in s.attrib:
            self.title = etree.Element("div")
            self.title.set("class","boxTitle")
            self.title.set("style","width:100%")
            self.title.text = s.get("title")
            self.node.append(self.title)


## =========================================================
## a button list
class bList(Node):
    def __init__(self,s,top):
        "add a button list"
        super(bList, self).__init__("ul",s,top)

## =========================================================
## a button list
class dList(Node):
    def __init__(self,s,top):
        "add a button list"
        super(dList, self).__init__("dl",s,top)

## =========================================================
## a list item
class i(Node):
    def __init__(self,s,top):
        "add a button list"
        super(i, self).__init__("li",s,top)

## =========================================================
## a list item
class dt(Node):
    def __init__(self,s,top):
        "add a button list"
        super(dt, self).__init__("dt",s,top)

## =========================================================
## a list item
class dd(Node):
    def __init__(self,s,top):
        "add a button list"
        super(dd, self).__init__("dd",s,top)

## =========================================================
## an arrow overlay
class arrows(Node):
    def __init__(self,s,top):
        "an arrow overlay"
        super(arrows, self).__init__("svg",s,top)

        self.node.set("width","100%")
        self.node.set("height","100%")

## =========================================================
## an arrow
class arrow(Node):
    def __init__(self,s,top):
        "docstring"
        super(arrow, self).__init__("path",s,top)

        id = uuid.uuid4()
        self.node.set("id","%s"%id)
        if not "style" in s.attrib:
            self.node.set("stroke","black")
            self.node.set("fill","black")
            self.node.set("stroke-width","10")
        
        link = "%s:%s:%s"%(id,s.get("from"),s.get("to"))
        if top.source.get('data-links'):
            link += ",%s"%top.source.get('data-links')
        top.source.set('data-links',link)

## =========================================================
## text
class text(Node):
    def __init__(self,s,top):
        "docstring"
        super(text, self).__init__("span",s,top)
        
## =========================================================
## A figure
class figure(Node):
    def __init__(self,s,top):
        "docstring"
        super(figure, self).__init__("figure",s,top)
        
        [W,H] = top.getDim(s)
        if "cap" in s.attrib:
            fc = etree.Element("figcaption")
            fc.text=s.get("cap")
            self.node.append(fc)

        im = etree.Element("img")
        im.set("src",top.Dirs.cpImage(s.get('src'),W,H))
        im.set("width","100%")
        
        self.node.append(im)
        
## =========================================================
## A video
class video(Node):
    def __init__(self,s,top):
        "docstring"
        super(video, self).__init__("div",s,top)

        newSrc = top.Dirs.cpVideo(s.get("src"))
        
        v = etree.Element('video')
        v.set("src",newSrc)
        v.set('controls','controls')
        v.set('loop','loop')
        self.node.append(v)
        
## =========================================================
## A table
class table(Node):
    def __init__(self,s,top):
        "docstring"
        super(table, self).__init__("table",s,top)
## =========================================================
## A table row
class row(Node):
    def __init__(self,s,top):
        "docstring"
        super(row, self).__init__("tr",s,top)
## =========================================================
## A table column
class col(Node):
    def __init__(self,s,top):
        "docstring"
        super(col, self).__init__("th",s,top)
        


        
