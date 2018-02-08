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
    trans = {
        "box":"div",
        "bList":"ul",
        "dList":"dl",
        "i":"li",
        "dt":"dt",
        "dd":"dd",
        "arrows":"svg",
        "arrow":"path",
        "text":"span",
        "figure":"figure",
        "video":"div",
        "table":"table",
        "row":"tr",
        "col":"th",
        "videoOverlay":"div"
    }
           
    def __init__(self,s,top):
        "add a text box"
        self.Coords = top.Coords
        self.node = etree.Element(self.trans[s.tag])
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

        if s.tag=="box":
            if "title" in s.attrib:
                self.title = etree.Element("div")
                self.title.set("class","boxTitle")
                self.title.set("style","width:100%")
                self.title.text = s.get("title")
                self.node.append(self.title)
        elif s.tag=="arrows":
           self.node.set("width","100%")
           self.node.set("height","100%")
        elif s.tag=="arrow":
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
        elif s.tag=="figure":
            [W,H] = top.getDim(s)
            if "cap" in s.attrib:
               fc = etree.Element("figcaption")
               fc.text=s.get("cap")
               self.node.append(fc)
            im = etree.Element("img")
            im.set("src",top.Dirs.cpImage(s.get('src'),W,H))
            im.set("width","100%")
            self.node.append(im)
        elif s.tag=="video":
            newSrc = top.Dirs.cpVideo(s.get("src"))
            v = etree.Element('video')
            v.set("src",newSrc)
            v.set('controls','controls')
            v.set('loop','loop')
            self.node.append(v)
        elif s.tag=="videoOverlay":
            im = etree.Element('img')
            [W,H] = self.getDim(s)
            im.set('src',self.Dirs.cpImage(s.get('src'),W,H))
            if "width" in s.attrib:
                im.set("width",s.get("width"))
                if "height" in s.attrib:
                    im.set("height",s.get("width"))
            self.node.append(im)
            
            

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



        



        
