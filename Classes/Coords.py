#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  =================================================
# Coords
#   - Author jouke hijlkema <jouke.hijlkema@onera.fr>
#   - Fri Jan 20 11:23:30 2017
#   - Initial Version 1.0
#  =================================================

class Coords:
    def __init__(self,Params):
       "defines the coordinate system"
       self.W     = int(Params.get("slideWidth"))
       self.H     = int(Params.get("slideHeight"))
       self.M     = int(Params.get("margin"))
       self.X     = 0
       self.Y     = 0
       self.scale = 1.0
       self.remeber = {}

    ## --------------------------------------------------------------
    ## Description : update the coordinates
    ## NOTE :
    ## -
    ## Author : jouke hylkema
    ## date   : 20-33-2017 11:33:19
    ## --------------------------------------------------------------
    def update (self,s):
        sc = 0.5*(self.scale)
        self.scale = float(s.get("scale") if "scale" in s.attrib else "1.0")
        sc += 0.5*(self.scale)

        if "useCoords" in s.attrib:
            self.X=self.remeber[s.get("useCoords")][0]
            self.Y=self.remeber[s.get("useCoords")][1]
        else:
            if "x" in s.attrib:
                self.X = float(s.get("x"))
            elif "moveX" in s.attrib:
                if s.get("moveX") == "left":
                    self.X-=sc*(self.W+self.M)
                elif s.get("moveX") == "right":
                    self.X+=sc*(self.W+self.M)
            elif "useX" in s.attrib:
                self.X = self.remeber[s.get("useX")][0]
            
            if "y" in s.attrib:
                self.Y = float(s.get("y"))
            elif "moveY" in s.attrib:
                if s.get("moveY") == "up":
                    self.Y-=sc*(self.H+self.M)
                elif s.get("moveY") == "down":
                    self.Y+=sc*(self.W+self.M)
            elif "useY" in s.attrib:
                self.Y = self.remeber[s.get("useY")][1]

        if "rememberCoords" in s.attrib:
            self.remeber[s.get("rememberCoords")]=[self.X,self.Y]
