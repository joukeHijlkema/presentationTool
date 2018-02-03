#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
# Template
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - dimanche 29 janvier 2017
#   - Initial Version 1.0
#  =================================================
from lxml import etree

class Template:
    def __init__(self,Path,Params,Dirs):
        "a template document"
        self.src = etree.parse(Path)
        W        = int(Params.get("slideWidth"))
        H        = int(Params.get("slideHeight"))
        head     = self.src.find("./head")
        body     = self.src.find("./body")
        footer   = self.src.find("./body/div[@id='footer']")
        s        = etree.Element('style')
        s.text   = ".slide {width:%s;height:%s}"%(W,H) 

        head.append(s)

        # extra logos
        if "logos" in Params.attrib:
            logos = eval(Params.get("logos"))
            index=2
            for l in logos:
                logo = etree.Element('div')
                logo.set('id',l)
                img  = etree.Element('img')
                img.set('src',Dirs.cpImage(logos[l],10000,10000))
                logo.append(img)
                body.insert(index,logo)
                index+=1

        # footers*
        if "footerTitle" in Params.attrib:
            f = etree.Element('span')
            f.set('class','footerTitle')
            f.text = Params.get('footerTitle')
            footer.append(f)
        if "footerDate" in Params.attrib:
            f = etree.Element('span')
            f.set('class','footerDate')
            f.text = Params.get('footerDate')
            footer.append(f)

        self.slideRoot = self.src.find("./body/div[@id='impress']")

    ## --------------------------------------------------------------
    ## Description : append a slide
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 29-04-2017 12:04:59
    ## --------------------------------------------------------------
    def append (self,slide):
        self.slideRoot.append(slide.source)

    ## --------------------------------------------------------------
    ## Description :write to file
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 29-08-2017 13:08:56
    ## --------------------------------------------------------------
    def write (self,path):
        self.src.write(path,
                       encoding="UTF-8",
                       xml_declaration=True,
                       method="html",
                       pretty_print=True)

    ## --------------------------------------------------------------
    ## Description :return the doc as a string
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 29-05-2017 17:05:42
    ## --------------------------------------------------------------
    def str (self):
        return etree.tostring(self.src,pretty_print=True).decode()
