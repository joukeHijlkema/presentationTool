#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
# Slide
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Thu Jan 19 13:05:20 2017
#   - Initial Version 1.0
# Todo
# - scale boxes to content
#  =================================================
from lxml import etree
import re
import os
from Classes.Node import Node

class Slide:
    def __init__(self,s,Coords,Dirs,number,lastSlide):
        "create a new slide"

        self.parseSlide(s)
        self.Dirs   = Dirs
        self.Coords = Coords
        self.Name   = "slide_%s"%number
        
        self.source = etree.Element('div')
        
        self.source.set("data-x","%s"%Coords.X)
        self.source.set("data-y","%s"%Coords.Y)

        self.source.set("data-scale",s.get("scale") if "scale" in s.attrib else "1.0")
        self.source.set("data-rotate-z",s.get("rotateZ") if "rotateZ" in s.attrib else "0.0")
        self.source.set("data-rotate-y",s.get("rotateY") if "rotateY" in s.attrib else "0.0")
        self.source.set("data-rotate-x",s.get("rotateX") if "rotateX" in s.attrib else "0.0")
        
        self.source.set('data-title',s.get("title") if "title" in s.attrib else "")
        self.source.set('data-subtitle',s.get("subtitle") if "subtitle" in s.attrib else "")
        self.source.set('data-number',"%s/%s"%(number,lastSlide))
        self.source.set('data-name',"%s"%self.Name)

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

        for a in s.attrib:
            old = ""
            if a in self.source.attrib:
                old = self.source.attrib.get(a)
            
            self.source.set(a,("%s %s"%(s.get(a),old)).strip())

        if "id" in s.attrib:
            self.source.set('id',s.get('id'))
        else:
            self.source.set('id',"slide_%d"%number)

        for n in s.iterchildren():
            self.source.append(self.walk(n))

    ## --------------------------------------------------------------
    ## Description : Walk the tree
    ## NOTE : 
    ## -
    ## Author : jouke hylkema
    ## date   : 05-32-2018 13:32:06
    ## --------------------------------------------------------------
    def walk (self,s):
        print(s)
        out = Node(s,self)
        for n in s.iterchildren():
            out.node.append(self.walk(n))
        return out.node
        
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
        

