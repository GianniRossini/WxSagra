#!/usr/bin/env python
# -*- coding: utf-8 -*-
# "constants" for use with printer setup calls


import wx
import wx.html

#import abstractmodel - now moved inside wxsagra 
#     astractmodule not present in portable python installation
import sys
import os
import locale
import re
# giorni della settimana
import calendar

import datetime
from collections import OrderedDict

# from MSWinPrint I used class document 
#  here is license from original MSwinPrint

"""
MSWinPrint.py
Copyright 2006-2012 Chris Gonnerman.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer. Redistributions in binary
form must reproduce the above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or other materials
provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
"""

import win32gui, win32ui, win32print, win32con
import Image
#import pprint

try:
    from PIL import ImageWin
except:
    ImageWin = None

# reqiered by class Document
scale_factor = 20
prdict = None

# Window printer constant

HORZRES = 8
VERTRES = 10
LOGPIXELSX = 88
LOGPIXELSY = 90
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111

paper_sizes = {
    "letter":       1,
    "lettersmall":  2,
    "tabloid":      3,
    "ledger":       4,
    "legal":        5,
    "statement":    6,
    "executive":    7,
    "a3":           8,
    "a4":           9,
}

orientations = {
    "portrait":     1,
    "landscape":    2,
}




# Item menu constants
ID_ABOUT=101
ID_HELP=102
ID_OPEN=1113
ID_SAVE=1114
ID_SAVE_AS=1115
ID_NEW=1116
ID_PRINT=1117
ID_PRINT_PREVIEW=1118
ID_EDIT=1200
ID_EXIT=110


"""
wxID_WXSAGRA,
wxID_WXSAGRAANNULLA, 
wxID_WXSAGRAB1DISP, 
wxID_WXSAGRABUTTONB1, 
wxID_WXSAGRABUTTONC1, 
wxID_WXSAGRABUTTONP1, 
wxID_WXSAGRABUTTONP2,
wxID_WXSAGRABUTTONS1, 
wxID_WXSAGRAC1DISP, 
wxID_WXSAGRADATATIME_MENUPROGR,
wxID_WXSAGRAESCI, 
wxID_WXSAGRAINFOPORTATE, 


wxID_WXSAGRABUTTONP0, 
wxID_WXSAGRABUTTONP1,
wxID_WXSAGRABUTTONP2, 
wxID_WXSAGRABUTTONP3,
wxID_WXSAGRABUTTONP4, 
wxID_WXSAGRABUTTONP5,
wxID_WXSAGRABUTTONP6, 
wxID_WXSAGRABUTTONP7,
wxID_WXSAGRABUTTONP8, 
wxID_WXSAGRABUTTONP9,

wxID_WXSAGRAOMAGGI, 
wxID_WXSAGRAP0DISP, 
wxID_WXSAGRAP1DISP,
wxID_WXSAGRAP2DISP, 
wxID_WXSAGRAP3DISP,
wxID_WXSAGRAP4DISP,
wxID_WXSAGRAP5DISP,
wxID_WXSAGRAP6DISP,
wxID_WXSAGRAP7DISP,
wxID_WXSAGRAP8DISP,
wxID_WXSAGRAP9DISP,

wxID_WXSAGRAPANEL1, 
wxID_WXSAGRAQTB1, 
wxID_WXSAGRAQTC1, 
wxID_WXSAGRAQTP1, 
wxID_WXSAGRAQTP2, 
wxID_WXSAGRAQTS1, 
wxID_WXSAGRAREGISTRA, 
wxID_WXSAGRAS1DISP, 
wxID_WXSAGRASTAMPA, 

wxID_WXSAGRASTATICTEXT1, 
wxID_WXSAGRASTATICTEXT2, 
wxID_WXSAGRASTATICTEXT3, 
wxID_WXSAGRASTATICTEXT4, 
wxID_WXSAGRASTORNA, 
wxID_WXSAGRATEXTCTRL1, 
wxID_WXSAGRATEXTCTRL2, 
wxID_WXSAGRATEXTCTRL3, 
"""

wxID_WXSAGRASTATICBOX1 = wx.NewId()
wxID_WXSAGRASTATICBOX2 = wx.NewId()
wxID_WXSAGRASTATICBOX3 = wx.NewId()
wxID_WXSAGRASTATICBOX4 = wx.NewId() 

wxID_WXSAGRAINFOPRINTER = wx.NewId()
wxID_WXSAGRADATATIME_MENUPROGR = wx.NewId()
wxID_WXSAGRALBL_TOTPREC = wx.NewId() 
wxID_WXSAGRALBL_CASSA = wx.NewId() 
wxID_WXSAGRAVAL_CASSA = wx.NewId()
wxID_WXSAGRALBL_RESTO = wx.NewId() 
wxID_WXSAGRAVAL_RESTO = wx.NewId()

wxID_WXSAGRASTATICTEXTTOTALE = wx.NewId()
wxID_WXSAGRATOTALE = wx.NewId() 
wxID_WXSAGRAVAL_TOTPREC = wx.NewId() 


def substr (s, start, length = None):
    """Returns the portion of string specified by the start and length 
    parameters.
    """
    if len(s) >= start:
        return False
    if not length:
        return s[start:]
    elif length > 0:
        return s[start:start + length]
    else:
        return s[start:length]
#
# used to display autoclose message info

class AbstractModel(object):

    def __init__(self):
        self.listeners = []

    def addListener(self, listenerFunc):
        self.listeners.append(listenerFunc)

    def removeListener(self, listenerFunc):
        self.listeners.remove(listenerFunc)

    def update(self):
        for eachFunc in self.listeners:
            eachFunc(self)

class MessageDialog(wx.Dialog):
    def __init__(self, message, title, ttl):
        wx.Dialog.__init__(self, None, -1, title,size=(400, 150))
        self.CenterOnScreen(wx.BOTH)
        self.timeToLive = ttl

        stdBtnSizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL) 
        stMsg = wx.StaticText(self, -1, message)
        self.stTTLmsg = wx.StaticText(self, -1, 'visualizza per %d s...'%self.timeToLive)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(stMsg, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox.Add(self.stTTLmsg,1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox.Add(stdBtnSizer,1, wx.ALIGN_CENTER|wx.TOP, 10)
        self.SetSizer(vbox)

        self.timer = wx.Timer(self)
        self.timer.Start(1000)        #Generate a timer event every second
        self.timeToLive = ttl 
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)

    def onTimer(self, evt):
        self.timeToLive -= 1
        self.stTTLmsg.SetLabel('visualizza per %d s...'%self.timeToLive)

        if self.timeToLive == 0:
            self.timer.Stop()
            self.Destroy()

class InfoPortate(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "InfoPortate Frame", pos=(10,10), size=(-1,600))
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self)

        self.timeToLive = 10 
        #stMsg = wx.StaticText(self, -1, message)
        msg = str('Situazione piatti venduti - visualizza per %d s...'%self.timeToLive)

        self.instructions = wx.StaticText(panel, label=msg)

        self.timer = wx.Timer(self)
        self.timer.Start(1000)        #Generate a timer event every second

        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer) 

        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(self.instructions, 0, flags, 5)

        now = datetime.datetime.now()
        filename =  "piatti"+ str(now.strftime("%Y-%m-%d")) + ".csv"
        piatti_log = []
        # print filename
        self.menunumero = 0        
        if os.path.exists(filename):
            piatti_log = load_tabbed_file(filename)
            self.index = 0
            self.list_ctrl = wx.ListCtrl(panel, size=(-1,550),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         )
            self.list_ctrl.InsertColumn(0, 'Portata', width=155)
            self.list_ctrl.InsertColumn(1, 'Costo unit.', width=70)
            self.list_ctrl.InsertColumn(2, 'menu/q.ta', width=70)
            self.list_ctrl.InsertColumn(3, 'totale', width=80 )
            i= 0            
            for y in range(i,len(piatti_log)) :
                line = "Line %s" % self.index
                self.list_ctrl.InsertStringItem(self.index, piatti_log[y][0])
                # Put date in first line
                if y > 0 :
                    self.list_ctrl.SetStringItem(self.index, 1, piatti_log[y][1])
                else:
                    self.list_ctrl.SetStringItem(self.index, 1, str(now.strftime("%Y-%m-%d"))) 
                self.list_ctrl.SetStringItem(self.index, 2, piatti_log[y][2])
                self.list_ctrl.SetStringItem(self.index, 3, piatti_log[y][3])
                self.index += 1
                # add empty line 
                if self.index == 1 :
                    #add empty line 
                    self.list_ctrl.InsertStringItem(self.index, "----------------")
                    self.list_ctrl.SetStringItem(self.index, 1, "-----------")
                    self.list_ctrl.SetStringItem(self.index, 2, "-----------")
                    self.list_ctrl.SetStringItem(self.index, 3, "-----------")
                    self.index += 1


            sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
            # sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
        closeBtn = wx.Button(panel, label="Send and Close")
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        sizer.Add(closeBtn, 0, flags, 5)
        panel.SetSizer(sizer)

    def onTimer(self, evt):
        self.timeToLive -= 1
        self.instructions.SetLabel('Situazione piatti venduti - visualizza per %d s...' % self.timeToLive)

        if self.timeToLive == 0:
            self.timer.Stop()
            self.Destroy()


    #----------------------------------------------------------------------
    def add_line(self, event,piatti_log_item):
        line = "Line %s" % self.index
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetStringItem(self.index, 2, "USA")
        self.index += 1
 
    #----------------------------------------------------------------------
    def onClose(self, event):
        """
        close frame
        """
        self.Close()
 

class HelpDialog(wx.Dialog) :
    """Display the help file"""
    def __init__(self, parent) :
        wx.Dialog.__init__(self,parent, wx.ID_ANY, "Menu Sagre Help", size = (600, 500))
        self.html = wx.html.HtmlWindow(self)
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainsizer.Add(self.html, 1, wx.EXPAND | wx.ALIGN_TOP)
        self.html.LoadFile(sys.path[0] + os.sep + "appunti.txt")
        # self.html.SetPage("<htm><body><p>This is a test.</p></body></html>")
        self.SetSizer(self.mainsizer)


def load_ini(file):
#    if (isEmpty(@file)exists(file)):
#        return array();
    cfg =OrderedDict()
    #cfg =namedtuple()
    #serviti = {}
    #serviti = OrderedDict()
    c = open(file).readlines()
    piatti = 0
    chiave = ""
    x = 0
    line =""
    pattern = re.compile("\[(.*?)\]")
    r={}
    while (x < len(c) ):
        line = c[x].strip()
        # print line 
        x += 1
        if (line != ""):
            if (re.findall(pattern, line)):
                if (len(cfg) > 0 ) : 
                    #print chiave
                    #print cfg 
                    r[chiave] = cfg
                    #print r
                    #print "\n"

                chiavelist = re.findall(pattern, line);
                chiave = chiavelist[0]
                #print "\nchiave is: [" + chiave +"]"
                ordine = 0
                cfg = OrderedDict()
                if (chiave == "Primi") : 
                    piatti = 1
                    #serviti = {}
                    serviti = OrderedDict()
                    #print "piatti is: " + str(piatti)

            else :
                # print line;
                k, v = line.split ('=')
                k = k.strip()
                #k = str(ordine)+ "-"+ k
                ordine += 1
                # print "chiave is: " + chiave + " k is: " + k + " v is: " + v
                # is better not remove trailing blank so we can position and center by adding space 
                if (substr(k,0,4) != "riga") : v = v.strip()
                #addedd qta iniziale
                if (piatti == 0) :
                    # print "--chiave is: " + chiave + " k is: " + k + " v is: " + v
                    cfg[k] = v
                    #r[chiave] = cfg

                if (piatti == 1) :
                    #cfg[k] = k
                    # print v.find('?')
                    if (v.find('?', 0) >  0 ) :
                        # print "found ? v is: " + v
                        p, q = v.split('?')
                        # print "--chiave is: " + chiave + " k is: " + k +" p is: " + p +" q is: " + q
                        cfg[k] = float (p)
                        serviti[k] = int(q)
                    else :
                        # print "--chiave is: " + chiave + " k is: " + k +" v is: " + v 
                        cfg[k] = float(v)
                        serviti[k] = -1
# at end of file 
    # print "\n at end chiave is " + chiave
    # print cfg 
    r[chiave] = cfg
    r['QINZ'] = serviti
    r['QRES'] = serviti

    return r

# load_tabbed_file(string filepath)
# loads a file with content saparated by comma (csv 
#
def load_tabbed_file(filename):
    # print filename
    f = open(filename, 'r')
    output = []
    for line in f:
      line = line.strip()
      res = line.split(",")
      output.append(res)
    return output 

def save_tabbed_file(filename,portate):
    # print "save tabbed file on " , filename
    # print portate
    fp = open(filename, 'w+')
#    for x in range(len(portate)):
#       #rec = []
#       rec = str(portate[x][0],",", portate[x][1],",",portate[x][2],",",portate[x][3],",",portate[x][4],"\r\n")
#       # rec = rec + "\r\n"
#       fp.write(rec)
    for item in portate:
        i = 0
        while i < len(item)-1 :
            fp.write("%s," % item[i])
            i= i + 1
        fp.write("%s\n" % item[i])
        # fp.write ("\n")
    fp.close 
    return

# from original work MSWinPrint.py
# Copyright 2006-2012 Chris Gonnerman.
# see license in first line (20 ... ) of this module 
class document:

    def __init__(self, printer = None, papersize = None, orientation = None):
        self.dc = None
        self.font = None
        self.printer = printer
        self.papersize = papersize
        self.orientation = orientation
        self.page = 0

    # scalepos  is used only in drawing  line and rectangle
    def scalepos(self, pos):
        rc = []
        for i in range(len(pos)):
            p = pos[i]
            if i % 2:
                p *= -1
            rc.append(int(p * scale_factor))
        return tuple(rc)

    def begin_document(self, desc = "WxSagra.py print job"):

        # open the printer
        if self.printer is None:
            self.printer = win32print.GetDefaultPrinter()
            # added to test
            # print self.printer
        self.hprinter = win32print.OpenPrinter(self.printer)

        # load default settings
        devmode = win32print.GetPrinter(self.hprinter, 8)["pDevMode"]
        # added to test
        
        
        # change paper size and orientation
        if self.papersize is not None:
            devmode.PaperSize = paper_sizes[self.papersize]
        if self.orientation is not None:
            devmode.Orientation = orientations[self.orientation]

        # create dc using new settings
        self.hdc = win32gui.CreateDC("WINSPOOL", self.printer, devmode)
        self.dc = win32ui.CreateDCFromHandle(self.hdc)

        # self.dc = win32ui.CreateDC()
        # if self.printer is not None:
        #     self.dc.CreatePrinterDC(self.printer)
        # else:
        #     self.dc.CreatePrinterDC()

        self.dc.SetMapMode(win32con.MM_TWIPS) # hundredths of inches
        self.dc.StartDoc(desc)
        self.pen = win32ui.CreatePen(0, int(scale_factor), 0L)
        self.dc.SelectObject(self.pen)
        self.page = 1

    def end_document(self):
        if self.page == 0:
            return # document was never started
        self.dc.EndDoc()
        del self.dc
        win32print.ClosePrinter(self.hprinter)
    def end_page(self):
        if self.page == 0:
            return # nothing on the page
        self.dc.EndPage()
        self.page += 1

    def getsize(self):
        if self.page == 0:
            self.begin_document()
        # returns printable (width, height) in points
        width = float(self.dc.GetDeviceCaps(HORZRES)) * (72.0 / self.dc.GetDeviceCaps(LOGPIXELSX))
        height = float(self.dc.GetDeviceCaps(VERTRES)) * (72.0 / self.dc.GetDeviceCaps(LOGPIXELSY))
        # print "printable page in points width: %d ,height: %d" %(width ,height)
        return width, height

    def line(self, from_, to):
        if self.page == 0:
            self.begin_document()
        self.dc.MoveTo(self.scalepos(from_))
        self.dc.LineTo(self.scalepos(to))

    def rectangle(self, box):
        if self.page == 0:
            self.begin_document()
        self.dc.MoveTo(self.scalepos((box[0], box[1])))
        self.dc.LineTo(self.scalepos((box[2], box[1])))
        self.dc.LineTo(self.scalepos((box[2], box[3])))
        self.dc.LineTo(self.scalepos((box[0], box[3])))
        self.dc.LineTo(self.scalepos((box[0], box[1])))

    def text(self, position, text):
        if self.page == 0:
            self.begin_document()
        # print
        # print "text: %s at xpos is scale factor %d * pos[0] %d  = %d "  % (text, scale_factor, position[0], (scale_factor * position[0]))
        # print "text: %s at ypos is scale factor %d * pos[1] %d  = %d "  % (text, scale_factor, position[1], (scale_factor * position[1]))
        self.dc.TextOut(scale_factor * position[0],
            -1 * scale_factor * position[1], text)

    # Gianni Rossini 2013 added family 0 = nornal 1 = italic
    def setfont(self, name, size, bold = None,family = 0):
        if self.page == 0:
            self.begin_document()
        wt = 400
        if bold:
            wt = 700
        self.font = getfont(name, size, wt, family)
        self.dc.SelectObject(self.font)

    def image(self, position, name, size):
        # "print PIL image at position with given size"
        if ImageWin is None:
            raise NotImplementedError, "PIL required for image method"
        if self.page == 0:
            self.begin_document()

        bmp = Image.open (name)
        dib = ImageWin.Dib(bmp)
        endpos = (position[0] + size[0], position[1] + size[1])
        dest = (position[0] * scale_factor, 
               -1 * position[1] * scale_factor,
               endpos[0] * scale_factor, 
               -1 * endpos[1] * scale_factor)
        dib.draw(self.hdc, dest)

    def setink(self, ink):
        pass

    def setfill(self, onoff):
        pass

def build_dict():
    global prdict
    lst = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_CONNECTIONS
        + win32print.PRINTER_ENUM_LOCAL)
    prdict = {}
    for flags, description, name, comment in lst:
        prdict[name] = {}
        prdict[name]["flags"] = flags
        prdict[name]["description"] = description
        prdict[name]["comment"] = comment

def listprinters():
    dft = win32print.GetDefaultPrinter()
    if prdict is None:
        build_dict()
    keys = prdict.keys()
    keys.sort()
    rc = [ dft ]
    for k in keys:
        if k != dft:
            rc.append(k)
    return rc

def desc(name):
    if prdict == None:
        listprinters()
    return prdict[name]


# Gianni Rossini 2013 added style family for italic  0 = nornal 1 = italic
def getfont(name, size, weight = 400,family = 0):
    return win32ui.CreateFont({
        "name": name,
        "height": scale_factor * size,
        "weight": weight,
        "italic": family,
    })


class SimpleName(AbstractModel):
    
    def __init__(self, first="", last=""):
        AbstractModel.__init__(self)
        self.set(first, last)
        
    def set(self, first, last):
        self.first = first
        self.last = last
        self.update()                                     


##class HelpDialog(wx.Dialog) :
##    """Display the help file"""
##    def __init__(self, parent) :
##        wx.Dialog.__init__(self,parent, wx.ID_ANY, "AddMachine Help", size = (600, 500))
##        self.html = wx.html.HtmlWindow(self)
##        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
##        self.mainsizer.Add(self.html, 1, wx.EXPAND | wx.ALIGN_TOP)
##        self.html.LoadFile(sys.path[0] + os.sep + "AddMachineHelp.html")
##        # self.html.SetPage("<htm><body><p>This is a test.</p></body></html>")
##        self.SetSizer(self.mainsizer)

class WxSagra(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'WXSAGRA', 
                size=(784, 640))

        self.CreateStatusBar()
        self.LastState = 0
        self.InfoPortatePanel = ""
        if sys.platform[:3].lower() == "win" :
            self.icon = wx.Icon(sys.path[0] + os.sep + "cogornese_ma_ico.ico", wx.BITMAP_TYPE_ICO)
        else :
            self.icon = wx.Icon(sys.path[0] + os.sep + "cogornese_ma_ico.ico", wx.BITMAP_TYPE_XPM)
        self.SetIcon(self.icon)

        # Set up the menu.
        filemenu = wx.Menu()
        #filemenu.Append(ID_NEW, "&New\tCtrl+N", " Create a New xxxxx")
        #wx.EVT_MENU(self, ID_NEW, self.OnNew)
        filemenu.Append(ID_OPEN, "&Open\tCtrl+O", " Open an xxxxxxx")
        #wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        self.menu_save = filemenu.Append(ID_SAVE, "&Save\tCtrl+S", " Save an Add xx")
        #wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        self.menu_save_as = filemenu.Append(ID_SAVE_AS, "Save &As\tCtrl+A", " Save an Add as xxx")
        #wx.EVT_MENU(self, ID_SAVE_AS, self.OnSaveAs)
        filemenu.AppendSeparator()
        self.menu_print = filemenu.Append(ID_PRINT, "&Print\tCtrl+P", " Print an xxxxx")
        #wx.EVT_MENU(self, ID_PRINT, self.OnPrint)
        self.menu_print_preview = filemenu.Append(ID_PRINT_PREVIEW, "Print Pre&view", " Preview the Printout for an xxxx")
        #wx.EVT_MENU(self, ID_PRINT_PREVIEW, self.OnPrintPreview)
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        
        helpmenu = wx.Menu()       
        helpmenu.Append(ID_HELP, "&Manual"," see appunti.txt")
        wx.EVT_MENU(self, ID_HELP, self.OnHelp)
        helpmenu.Append(ID_ABOUT, "A&bout"," Information about this program")
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)

        # Create the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        #menuBar.Append(editmenu,"&Edit")
        menuBar.Append(helpmenu, "&Help")


        panel = wx.Panel(self)   

        # we need this info to return focus to this frame after InfoPortate frame is shown
        self.main_win_frame = panel


        panel.SetBackgroundColour("White")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) 
        self.textFields = {}
        self.labelFields = {}
        # self.createTextFields(panel)     
        self.model = SimpleName()                         
        self.model.addListener(self.OnUpdate)             
        
        # array (liste in python ) utilized:
        #      to dynamic menu total calculation (TotalCalc) 
        #      to print menu (OnStampa) 
        #      to update log of the day (piattiaaaa-mm-gg (OnRegistra) 

        self.Voce = [""] * 100       # item (portata)
        self.Portata = [""] * 100    #group of item (primi .secondi etc) 
        self.TotaliRiga = [0]*100    # single item total
        self.QtaRiga = [0]*100       # single item qty
        self.PortataPrice = [0]*100  # single item qty
        self.totmenu = 0

        #
        # load configuration - menu and setting 
        #
        self.debug = 0
        self.menu_data_ora = 0
        self.menu_progr = 0

        self.r = load_ini('portate.ini')
        # print self.r
        # test and set setting present in stampa box.(convert in integer please) 
        box = "stampa" 
        print "\n",box
        for item in self.r[box]:
            print item, self.r[box][item]
            if item == "debug" :
                self.debug = int(self.r[box][item])
            if item == "menu_data_ora" :
                self.menu_data_ora = int(self.r[box][item])
            if item == "menu_progr" :
                self.menu_progr = int(self.r[box][item])

        if self.debug == 1 :
            box = "stampa" 
            print "\n",box
            for item in self.r[box]:
                print item, self.r[box][item]

            box = "intestazione" 
            print "\n",box
            for item in self.r[box]:
                print item, self.r[box][item]
            
            box = "Primi"
            # print "\n",box
            for item in self.r[box]:
                print item, self.r[box][item]
            box = "Secondi"
            print "\n",box
            for item in self.r[box]:
                print item, self.r[box][item]
            box = "Contorni"
            print "\n",box
            for item in self.r[box]:
               print item, self.r[box][item]
            box = "Bevande"
            print "\n",box
            for item in self.r[box]:
                print item, self.r[box][item]
            

        # get info saved from log of the day (backup for restart )
        #     create or update file of this day activity  - name format is  piattiyyyy-mm-dd.csv

        #   we can handle limited portate using self.r['QRES'] and self.r['QINZ']
        #     see configuration file to load self.r['QINZ] il limit value > 0
        #     example for limiting portata to 20 : Mesciua = 5.00 ? 20
        #   If restart in same day we can load residual from log file piattiyyyy-mm-dd.csv

        #   see  infoportate
        now = datetime.datetime.now()
        filename =  "piatti"+ str(now.strftime("%Y-%m-%d")) + ".csv"
        piatti_log = []
        # print filename
        self.menunumero = 0        
        if os.path.exists(filename):
            piatti_log = load_tabbed_file(filename)
            if self.debug == 1 : 
                print "ultimo menu" , piatti_log[0][2]
            self.menunumero = piatti_log[0][2]

            count = 1
            for y in range(count,len(piatti_log)) :
                riga = piatti_log[y][0]
                #  magia 2010 k non da' errore sui piatti rimossi - da portate.ini
                if (self.r['QINZ'][riga] < 0):
                    piatti_log[y][4] = ""
                else :
                    # per questa portata imposto 
                    #   quantita residua = quantita limite iniziale - quntita gia' venduta 
                    self.r['QRES'][riga] = self.r['QINZ'][riga] - float(piatti_log[y][2])
                    #    update log due change in QINZ after reloading)
                    if (piatti_log[y][4] != ""):
                        piatti_log[y][4] = self.r['QRES'][riga]
                        refresh_log = 1 
            if (refresh_log == 1) :
                save_tabbed_file(filename,piatti_log)
# code from winbinder version to manage piatti residui  - to do -  
#           $count=0;
#           #//print_r( $cfg['INZ']);
#           #//print_r( $cfg['QRES']);
#           foreach($piatti_log as $param) {
#               #//  echo "\n0 ". $param[0]. " -1- ".$param[1]. " -2- ".$param[2]. " -3- ".$param[3]." -3- ". $param[4] ;
#                 if ($count == 0 ) {
#               #//
#                   $count++;
#                 }
#                 else
#                 {
#                    #// magia 2010 k non da' errore sui piatti rimossi - da portate.ini
#                    if (isset($cfg['QINZ'][$param[0]]) and ($cfg['QINZ'][$param[0]] < 0 ) )
#                         $param[4] = "";
#                    #//   echo " \n-debug  RES" . $cfg['QRES'][$param[0]] ." -INZ- ". $cfg['QINZ'][$param[0]]." -p[2]- ".$param[2]." -p[4]- ".$param[4];
#                    if (isset($cfg['QINZ'][$param[0]]))
#                    {
#                      $cfg['QRES'][$param[0]] = $cfg['QINZ'][$param[0]] - $param[2];
#                      #// update log due change in QINZ after reloading)
#                      if( $param[4] != "")
#                      {
#                        $param[4] = $cfg['QRES'][$param[0]];
#                        $piatti_log[$count][4] = $cfg['QRES'][$param[0]];
#                        $refesh_log = 1;
#                      }
#                      $count++;
#                    }
#                 }
#              }
#            if ($refresh_log == 1) save_tabbed_file($filename,$piatti_log);
#                                                                              


        #
        # draw four staticbox - group of item (primi, seondi, contorni, bevande)
        #
        f_weekday = [calendar.day_name[i].lower() for i in range(7)]
        #print f_weekday
        self.staticBox4 = wx.StaticBox(id=wxID_WXSAGRASTATICBOX4,
                label="Bevande", name="staticBox4", parent=panel,
                pos = wx.Point(352, 280), size=wx.Size(336, 232), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_WXSAGRASTATICBOX2,
              label=u'Secondi', name='staticBox2', parent=panel,
              pos=wx.Point(352, 32), size=wx.Size(336, 232), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_WXSAGRASTATICBOX3,
              label=u'Contorni', name='staticBox3', parent=panel,
              pos=wx.Point(8, 280), size=wx.Size(336, 232), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_WXSAGRASTATICBOX1,
              label=u'Primi', name=u'staticBox1', parent=panel,
              pos=wx.Point(8, 32), size=wx.Size(336, 232), style=0)
        

        #
        # draw single item button and related textfield for quantity 
        #     use createButtonCommand - build OneButton
        #     use createButtonText

        #
        self.createButtonBar1(panel)
        self.createButtonBar2(panel)
        self.createButtonBar3(panel)
        self.createButtonBar4(panel)
        self.createButtonCommand(panel)

        #
        # draw menu dinamic Total (big to read better)
        #
        self.staticTextTotale = wx.StaticText(id=wxID_WXSAGRASTATICTEXTTOTALE,
              label=u'Totale', name='staticText5', parent=panel,
              pos=wx.Point(528, 524), size=wx.Size(47, 18), style=0)
        self.staticTextTotale.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'Tahoma'))
                
        self.GrandTotal = wx.TextCtrl(id=wxID_WXSAGRATOTALE, name=u'Totale',
              parent=panel, pos=wx.Point(582, 520), size=wx.Size(100, 27),
              style=wx.TE_READONLY | wx.TE_RIGHT, value=u'0.00')
        self.GrandTotal.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'Tahoma'))
        self.GrandTotal.SetThemeEnabled(False)

        #totale ticket cntorni con @ in prima posizione
        self.staticLabelTotalTicket = wx.StaticText(id = -1, label="", parent = panel,
              pos=wx.Point(700, 510), size=wx.Size(90, 13), style=0)
        self.staticTotalTicket = wx.StaticText(id = -1, label="", parent = panel,
              pos=wx.Point(700, 530), size=wx.Size(90, 13), style=0)

        #
        # get and draw default printer info
        #
        if self.debug == 1 :
            print 
            print "GetPrinterName:" , win32print.GetDefaultPrinter()

        defaultprt = "Stampa su: %s " % win32print.GetDefaultPrinter()
        printer = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer)
        devmode = win32print.GetPrinter(hprinter, 8)["pDevMode"]
        #print devmode.PaperSize
        for key in paper_sizes.keys():
          if paper_sizes[key] == devmode.PaperSize :
            # print key 
            defaultprt += ' '
            defaultprt += str(key)
            break
        for key in orientations.keys():
        #print devmode.Orientation
          if orientations[key] == devmode.Orientation :
            # print key 
            defaultprt += ' '
            defaultprt += str(key)
            break
        # print devmode.YResolution
        defaultprt += ' Y_scale_dot/inch:'
        defaultprt += str(devmode.YResolution)
        # close printer 
        win32print.ClosePrinter(hprinter)
        # print "Close printer handle"
        #end get default printer info 

        self.infoprinter = wx.StaticText(id=wxID_WXSAGRAINFOPRINTER,
              label= defaultprt, name=u'infoprinter',
              parent=panel, pos=wx.Point(8, 8), size=wx.Size(354, 13),
              style=0)

        self.datatime_menuprogr = wx.StaticText(id=wxID_WXSAGRADATATIME_MENUPROGR,
              label=u'30/12/2012 15:00  -- menu fstti = 0',
              name=u'datatime_menuprogr', parent=panel, pos=wx.Point(570, 8),
              size=wx.Size(180, 13), style=0)

        #
        # get and draw date time info and his update logic 
        #
        #dt = str(wx.DateTimeFromDMY(now.day, now.now.month, now.year))
        now = datetime.datetime.now()
        dt = str(now.strftime("%d-%m-%Y %H:%M:%S"))
        self.datatime_menuprogr.SetLabel(dt)
 
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimerUpdate, self.timer)
        self.timer.Start(1000)

        #
        # get and draw previous menu total and logic to handle cash change
        #
        self.lbl_TotPrec = wx.StaticText(id=wxID_WXSAGRALBL_TOTPREC,
              label=u'Totale Precedente', name=u'lbl_TotPrec', parent=panel,
              pos=wx.Point(22, 530), size=wx.Size(90, 13), style=0)

        self.val_TotPrec = wx.TextCtrl(id=wxID_WXSAGRAVAL_TOTPREC, name=u'val_TotPrec', 
              parent=panel, pos= (115, 526),
              size=wx.Size(50, 21), style= wx.TE_READONLY |wx.ALIGN_RIGHT, value = '0.00')


        self.lbl_cassa = wx.StaticText(id=wxID_WXSAGRALBL_CASSA,
              label='Cassa', name='lblCassa', parent=panel,
              pos=wx.Point(170, 530), size=wx.Size(40, 13), style=0)

        self.val_cassa = wx.TextCtrl(id=wxID_WXSAGRAVAL_CASSA, name='val_cassa',
              parent=panel, pos=wx.Point(210, 526), size=wx.Size(64, 21),
              style=0, value='0')
        self.Bind(wx.EVT_TEXT, self.RestoCalc, self.val_cassa)

        self.lbl_resto = wx.StaticText(id=wxID_WXSAGRALBL_RESTO,
              label='Resto', name='lblresto', parent=panel,
              pos=wx.Point(280, 530), size=wx.Size(40, 13), style=0)
        self.val_resto = wx.TextCtrl(id=wxID_WXSAGRAVAL_RESTO, name='val_resto',
              parent=panel, pos=wx.Point(320, 526), size=wx.Size(64, 21),
              style=0, value='0')

        self.val_TotalTicketPrec =wx.StaticText(id= -1,
              label='ticket menu prec.', name='', parent=panel,
              pos=wx.Point(400, 530), size=wx.Size(110, 13), style=0)

        # Hook frame event so we can warn on unsaved exit        
        self.Bind(wx.EVT_CLOSE, self.OnClose)        

        #                           
        #                           
        #                           
        #                           
        #  end menu creation        
        #                           
        #                           
        #                           
        #                           


        """
        self.OpenFile()
    def OpenFile(self, newfilename = "portate.ini") :
        # Opens a file, parses each line 
       
        
        f = open(newfilename, "r")
        for s in f.readlines() :
           print s
        f.close()
        
##        iLen = len(newportate)
##        if iLen > 0 :
##            self.SetTape(newportate, newfilename)
##        else :
##            self.ShowWarningBox("No values were found to open in this file", "Unable to Open " + newfilename)

    """

    def buttonData_primi(self):
        return (("Primi_1", self.OnPrimi_1),
                ("Primi_2", self.OnPrimi_2),
                ("Primi_3", self.OnPrimi_3),
                ("Primi_4", self.OnPrimi_4),
                ("Primi_5", self.OnPrimi_5),
                ("Primi_6", self.OnPrimi_6),
                ("Primi_7", self.OnPrimi_7),
                ("Primi_8", self.OnPrimi_8),
                ("Primi_9", self.OnPrimi_9),
                ("Primi_10", self.OnPrimi_10))

    def buttonData_secondi(self):
        return (("Secondi_1", self.OnSecondi_1),
                ("Secondi_2", self.OnSecondi_2),
                ("Secondi_3", self.OnSecondi_3),
                ("Secondi_4", self.OnSecondi_4),
                ("Secondi_5", self.OnSecondi_5),
                ("Secondi_6", self.OnSecondi_6),
                ("Secondi_7", self.OnSecondi_7),
                ("Secondi_8", self.OnSecondi_8),
                ("Secondi_9", self.OnSecondi_9),
                ("Secondi_10", self.OnSecondi_10))

    def buttonData_contorni(self):
        return (("Contorni_1", self.OnContorni_1),
                ("Contorni_2", self.OnContorni_2),
                ("Contorni_3", self.OnContorni_3),
                ("Contorni_4", self.OnContorni_4),
                ("Contorni_5", self.OnContorni_5),
                ("Contorni_6", self.OnContorni_6),
                ("Contorni_7", self.OnContorni_7),
                ("Contorni_8", self.OnContorni_8),
                ("Contorni_9", self.OnContorni_9),
                ("Contorni_10", self.OnContorni_10))

    def buttonData_bevande(self):
        return (("Bevande_1", self.OnBevande_1),
                ("Bevande_2", self.OnBevande_2),
                ("Bevande_3", self.OnBevande_3),
                ("Bevande_4", self.OnBevande_4),
                ("Bevande_5", self.OnBevande_5),
                ("Bevande_6", self.OnBevande_6),
                ("Bevande_7", self.OnBevande_7),
                ("Bevande_8", self.OnBevande_8),
                ("Bevande_9", self.OnBevande_9),
                ("Bevande_10", self.OnBevande_10))

    def buttonData_Comandi(self):
        return (("Annulla", self.OnAnnulla),
                ("Registra", self.OnRegistra),
                ("Storna", self.OnStorna),
                ("Stampa", self.OnStampa),
                ("Omaggi", self.OnOmaggi),
                ("Esci", self.OnExit))
                #("test menu", self.OnTestMenu))



    def createButtonBar1(self, panel, xPos = 48):
        yPos = 47
        dimens = (256,21)
        handler = ( self.OnPrimi_1, self.OnPrimi_2,self.OnPrimi_3,
                    self.OnPrimi_4, self.OnPrimi_5,self.OnPrimi_6,
                    self.OnPrimi_7, self.OnPrimi_8,self.OnPrimi_9,
                    self.OnPrimi_10)
        x = 0
        #for eachLabel,eachpippo in self.buttonData_primi():
        for eachLabel in self.r['Primi']:
            #eachHandler = self.OnPrimi_1
            pos = (xPos, yPos)
            eachHandler = handler[x]
            #print eachHandler
            x += 1
            button = self.buildOneButton(panel, eachLabel ,eachHandler , pos, dimens)
            self.createButtonText(panel,eachLabel, ( xPos+258,yPos+2))
            # label residui
            self.createButtonLabel(panel,eachLabel, ( xPos+258,yPos+2))
            yPos += button.GetSize().height


    def createButtonBar2(self, panel, xPos = 384):
        yPos = 47
        dimens = (256,21)
        handler = ( self.OnSecondi_1, self.OnSecondi_2,self.OnSecondi_3,
                    self.OnSecondi_4, self.OnSecondi_5,self.OnSecondi_6,
                    self.OnSecondi_7, self.OnSecondi_8,self.OnSecondi_9,
                    self.OnSecondi_10)
        #for eachLabel, eachHandler in self.buttonData_secondi():
        x = 0
        for eachLabel in self.r['Secondi']:
            pos = (xPos, yPos)
            eachHandler = handler[x]
            x += 1
            button = self.buildOneButton(panel, eachLabel, eachHandler, pos, dimens)
            self.createButtonText(panel,eachLabel, ( xPos+258,yPos+2))
            self.createButtonLabel(panel,eachLabel, ( xPos+258,yPos+2))
            yPos += button.GetSize().height
    
    def createButtonBar3(self, panel, xPos = 48):
        yPos = 295
        dimens = (256,21)
        #for eachLabel, eachHandler in self.buttonData_contorni():
        handler = ( self.OnContorni_1, self.OnContorni_2,self.OnContorni_3,
                    self.OnContorni_4, self.OnContorni_5,self.OnContorni_6,
                    self.OnContorni_7, self.OnContorni_8,self.OnContorni_9,
                    self.OnContorni_10)
        #for eachLabel, eachHandler in self.buttonData_secondi():
        x = 0
        for eachLabel in self.r['Contorni']:
            eachHandler = handler[x]
            x += 1
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel, eachHandler, pos, dimens)
            self.createButtonText(panel,eachLabel, ( xPos+258,yPos+2))
            self.createButtonLabel(panel,eachLabel, ( xPos+258,yPos+2))
            yPos += button.GetSize().height

    def createButtonBar4(self, panel, xPos = 384):
        yPos = 295        
        dimens = (256,21)
        #for eachLabel, eachHandler in self.buttonData_bevande():
        handler = ( self.OnBevande_1, self.OnBevande_2,self.OnBevande_3,
                    self.OnBevande_4, self.OnBevande_5,self.OnBevande_6,
                    self.OnBevande_7, self.OnBevande_8,self.OnBevande_9,
                    self.OnBevande_10)
        x = 0
        for eachLabel in self.r['Bevande']:
            eachHandler = handler[x]
            x += 1
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel, eachHandler, pos, dimens)
            self.createButtonText(panel,eachLabel, ( xPos+258,yPos+2))
            self.createButtonLabel(panel,eachLabel, ( xPos+258,yPos+2))
            yPos += button.GetSize().height

    def createButtonCommand(self, panel, xPos = 700):
        yPos = 100 
        dimens = (50,50)
        for eachLabel, eachHandler in self.buttonData_Comandi():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel, eachHandler, pos, dimens)
            yPos += button.GetSize().height + 20

        # add ButtonCommand testmenu
        dimens = (70,20)
        yPos = 30
        pos = (xPos, yPos)
        button = self.buildOneButton(panel, "InfoPortate", self.OnInfoPortate, pos, dimens)


        # add ButtonCommand testmenu
        dimens = (70,20)
        yPos = 60
        pos = (xPos, yPos)
        button = self.buildOneButton(panel, "test menu", self.OnTestMenu, pos, dimens)
    
    def createButtonText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), "", pos)
        static.SetBackgroundColour("White")
        textPos = (pos[0] + 1, pos[1])
        temp = wx.NewId()
        self.textFields[label] = wx.TextCtrl(panel, temp, 
                "0", size=(20, 15), pos=textPos,
                style=wx.TE_RIGHT)
        # self.textFields[label] e' un array dei campi di immissiome creati
        # essi sono identificati da label (Primi_1 ..Primi_2 etc )
        # per gestirli si usa self.textFields["Primi_1"].SetValue("1")  
        self.Bind(wx.EVT_TEXT, self.TotalCalc, self.textFields[label])
        # print"x:" + str(temp) + " " + label

    def createButtonLabel(self, panel, label, pos):
        #static = wx.StaticText(panel, wx.NewId(), "", pos)
        #static.SetBackgroundColour("White")
        textPos = (pos[0] -285 , pos[1])
        temp = wx.NewId()
        self.labelFields[label] = wx.StaticText(panel,temp,
              "---", pos=textPos, size=wx.Size(10, 15), style=0)


    def buildOneButton(self, parent, label, handler, pos=(0,0), dimens=(0,0)):
        # printlabel
        button = wx.Button(parent, -1, label, pos, dimens)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button
    """   
    def textFieldData(self):
        return (("First Name", (10, 520)),
                ("Last Name", (200, 520)))
     
    def createTextFields(self, panel):
        for eachLabel, eachPos in self.textFieldData():
            self.createCaptionedText(panel, eachLabel, eachPos)
    """            

    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
        textPos = (pos[0] + 75, pos[1])
        self.textFields[label] = wx.TextCtrl(panel, wx.NewId(), 
                "", size=(100, -1), pos=textPos,
                style=wx.TE_READONLY)
        

    def OnUpdate(self, model):
        self.textFields["First Name"].SetValue(model.first)    
        self.textFields["Last Name"].SetValue(model.last) 
        
        
    def OnPrimi_1(self, event):                                   
        # self.model.set("Fred", "Flintstone")                   
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item   in self.r["Primi"]:
            x += 1
            if (x == 1): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)
        
    def OnPrimi_2(self, event):                                 
        # self.model.set("Barney", "Rubble")                     
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 2): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)
                                                               
    def OnPrimi_3(self, event):                                  
        # self.model.set("Wilma", "Flintstone")                  
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 3): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_4(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 4): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_5(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 5): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_6(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 6): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

        
    def OnPrimi_7(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 7): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_8(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 8): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_9(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 9): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnPrimi_10(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0        
        for item  in self.r["Primi"]:
            x += 1
            if (x == 10): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    # evento secondi
    def OnSecondi_1(self, event):                                   
        # self.model.set("Fred", "Flintstone")                   
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 1): break 
        tempqta = int(self.textFields [item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_2(self, event):                                 
        # self.model.set("Barney", "Rubble")                     
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 2): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_3(self, event):                                  
        # self.model.set("Wilma", "Flintstone")                  
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 3): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)
                                                               
    def OnSecondi_4(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 4): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_5(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 5): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_6(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 6): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_7(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 7): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_8(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 8): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_9(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 9): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnSecondi_10(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0 
        for item  in self.r["Secondi"]:
            x += 1
            if (x == 10): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

# evento contorni
    def OnContorni_1(self, event):                                   
        # self.model.set("Fred", "Flintstone")                   
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 1): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_2(self, event):                                 
        # self.model.set("Barney", "Rubble")                     
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 2): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_3(self, event):                                  
        # self.model.set("Wilma", "Flintstone")                  
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 3): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_4(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 4): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_5(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 5): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_6(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 6): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_7(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x=0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 7): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_8(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 8): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_9(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 9): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnContorni_10(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Contorni"]:
            x += 1
            if (x == 10): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta)  
        # textFields - bottontext is binded on change to self.TotalCalc(0)

# evento bevande
    def OnBevande_1(self, event):                                   
        # self.model.set("Fred", "Flintstone")                   
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 1): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_2(self, event):                                 
        # self.model.set("Barney", "Rubble")                     
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 2): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_3(self, event):                                  
        # self.model.set("Wilma", "Flintstone")                  
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 3): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_4(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 4): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_5(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 5): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_6(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 6): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_7(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 7): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_8(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 8): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_9(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 9): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def OnBevande_10(self, event):                                  
        # self.model.set("Betty", "Rubble")                      
        # get value return string - 
        # to use in calculation we must convert it to numeric
        x = 0
        for item  in self.r["Bevande"]:
            x += 1
            if (x == 10): break 
        tempqta = int(self.textFields[item].GetValue())
        tempqta = tempqta + 1
        self.textFields[item].SetValue("%d" % tempqta) 
        # textFields - bottontext is binded on change to self.TotalCalc(0)

    def Piatti_Log_init(self, piatti_log, pp,ss,cc,bb):
        i= 1
        #line=[0,"",0,0,""]
        for item in self.r[pp]:
            #piatti_log[i][0] = item              #piatto
            #piatti_log[i][1] = self.r[a][item]   #costo
            #piatti_log[i][2] = 0                 #quantita'
            #piatti_log[i][3] = 0                 #valore 
            #piatti_log[i][4] = self.r['QINZ'][item]
            line=[0,"",0,0,""]
            line[0] = item
            line[1] = self.r[pp][item]
            line[2] = 0
            line[3] = 0
            line[4] = self.r['QINZ'][item]
            piatti_log.append(line)
            i += 1

        for item in self.r[ss]:
            #piatti_log[i][0] = item              #piatto
            #piatti_log[i][1] = self.r[a][item]   #costo
            #piatti_log[i][2] = 0                 #quantita'
            #piatti_log[i][3] = 0                 #valore 
            #piatti_log[i][4] = self.r['QINZ'][item]
            line=[0,"",0,0,""]
            line[0] = item
            line[1] = self.r[ss][item]
            line[2] = 0
            line[3] = 0
            line[4] = self.r['QINZ'][item]
            piatti_log.append(line)
            i += 1
        for item in self.r[cc]:
            #piatti_log[i][0] = item              #piatto
            #piatti_log[i][1] = self.r[a][item]   #costo
            #piatti_log[i][2] = 0                 #quantita'
            #piatti_log[i][3] = 0                 #valore 
            #piatti_log[i][4] = self.r['QINZ'][item]
            line=[0,"",0,0,""]
            line[0] = item
            line[1] = self.r[cc][item]
            line[2] = 0
            line[3] = 0
            line[4] = self.r['QINZ'][item]
            piatti_log.append(line)
            i += 1
        for item in self.r[bb]:
            #piatti_log[i][0] = item              #piatto
            #piatti_log[i][1] = self.r[a][item]   #costo
            #piatti_log[i][2] = 0                 #quantita'
            #piatti_log[i][3] = 0                 #valore 
            #piatti_log[i][4] = self.r['QINZ'][item]
            line=[0,"",0,0,""]
            line[0] = item
            line[1] = self.r[bb][item]
            line[2] = 0
            line[3] = 0
            line[4] = self.r['QINZ'][item]
            piatti_log.append(line)
            i += 1
        return piatti_log

    def Piatti_Log_update(self, piatti_log, pp,ss,cc,bb):
        x = 0
            #search in piatti_log 
            #for item in self.r[pp]:
            #piatti_log[i][0] = item              #piatto]
            #piatti_log[i][1] = self.r[a][item]   #costo
            #piatti_log[i][2] = 0                 #quantita'
            #piatti_log[i][3] = 0                 #valore 
            #piatti_log[i][4] = self.r['QINZ'][item]
            

        # used to test if we must write updated piatti_log 
        tmp_totmenu = 0

        # leggi tutte le portate di questo menu dalle tuples 
        i= 1
        for x in range(40) :
          if self.Voce[x] != "" and self.QtaRiga[x] > 0:
            # print "get info from Voce[x] ", x, self.Voce[x] 
            # test per piatto da aggiornare  non trovato piatti_log
            piatto_found = 0 
            for y in range(i,x+2) :
                riga =  piatti_log[y][0]
                # print "update test for " , riga
                if (self.Voce[x] == riga):
                    # print "found, now update piatti_log for ", x , self.Voce[x] ,\
                    #       self.Portata[x], self.QtaRiga[x]
                    # print "previous ", piatti_log[y] , "QRES: ", self.r['QRES'][riga]
                    piatti_log[y][2] = float(piatti_log[y][2]) + self.QtaRiga[x]
                    piatti_log[y][3] = float(piatti_log[y][3]) + self.TotaliRiga[x]
                    piatti_log[y][4] = self.r['QINZ'][riga] - self.QtaRiga[x]
                    self.r['QRES'][riga] = self.r['QINZ'][riga] - self.QtaRiga[x]
                    if self.debug == 1 :
                        print "updated  ", piatti_log[y], "QRES: ", self.r['QRES'][riga]
                    tmp_totmenu = tmp_totmenu + self.TotaliRiga[x]
                    piatto_found = 1
                    break

            # piatto non presente in piatti_log (aggiunto durante la sessione) 
            # aggiungo la relativa riga
            if piatto_found == 0:
                #add voce 
                #piatti_log[][0] = item              #piatto
                #piatti_log[][1] = self.r[a][item]   #costo
                #piatti_log[][2] = 0                 #quantita'
                #piatti_log[][3] = 0                 #valore 
                #piatti_log[][4] = self.r['QINZ'][item]
                if self.debug == 1 :
                    print " aggiungo portata non presente in piatti_log " , riga
                line=[0,"",0,0,""]
                line[0] = riga
                # print self.TotaliRiga[x]/self.QtaRiga[x] 
                line[1] = self.TotaliRiga[x]/self.QtaRiga[x]
                # print self.PortataPrice[x]
                line[1] = self.PortataPrice[x]
                line[2] = self.QtaRiga[x]
                line[3] = self.TotaliRiga[x]
                line[4] = self.r['QINZ'][riga]
                piatti_log.append(line)
                tmp_totmenu = tmp_totmenu + self.TotaliRiga[x]
        if self.debug == 1 :
            print piatti_log

        if tmp_totmenu > 0 :
           #update first record info
           self.menunumero = int(self.menunumero) + 1
           now = datetime.datetime.now()
           piatti_log[0][1] = str(now.strftime("%Y-%m-%d"))        # aaaa-mm-gg
           piatti_log[0][2] = self.menunumero                     # progr  menu fatti nella sessione
           piatti_log[0][3] = float(piatti_log[0][3]) + tmp_totmenu
           if self.debug == 1 :
                print "check menu ", self.menunumero, " total printed: ", self.totmenu , " logged: ",tmp_totmenu
        return 

    def TotalCalc(self, event):
        # arrivo qui sia per quantita immessa manualmente 
        #            sia per click sul pulsante (+ 1 ad ogni click)
        # ricalcolo i totali riga (quantita * prezzo) 
        
        # print"function totalcalc"
        # print
        self.total_ticket=0

        x = 0 
        for item in self.r["Primi"]:
            # printitem, 
            tempqta = int(self.textFields [item].GetValue())
            # printtempqta , tempqta* self.r['Primi'][item]
            self.Voce[x] = item
            self.Portata[x] = 'Primi'
            self.QtaRiga[x] = tempqta
            self.TotaliRiga[x] = tempqta* self.r['Primi'][item]
            self.PortataPrice[x] = self.r['Primi'][item]
            x += 1
        x = 10 
        for item in self.r["Secondi"]:
            # printitem, 
            tempqta = int(self.textFields [item].GetValue())
            # printtempqta , tempqta* self.r['Secondi'][item]
            self.Voce[x] = item
            self.Portata[x] = 'Secondi'
            self.QtaRiga[x] = tempqta
            self.TotaliRiga[x] = tempqta* self.r['Secondi'][item]
            self.PortataPrice[x] = self.r['Secondi'][item]
            x += 1
        x = 20 
        for item in self.r["Contorni"]:
            # printitem, 
            tempqta = int(self.textFields [item].GetValue())
            # printtempqta , tempqta* self.r['Contorni'][item]
            self.Voce[x] = item
            self.Portata[x] = 'Contorni'
            self.QtaRiga[x] = tempqta
            self.TotaliRiga[x] = tempqta* self.r['Contorni'][item]
            self.PortataPrice[x] = self.r['Contorni'][item]

            # handle ticket 
            if (item.find ("@") != -1): 
                self.total_ticket= self.total_ticket + self.TotaliRiga[x]
            #
            x += 1
        x = 30
        for item in self.r["Bevande"]:
            # printitem, 
            tempqta = int(self.textFields [item].GetValue())
            # printtempqta , tempqta* self.r['Bevande'][item]
            self.Voce[x] = item
            self.Portata[x] = 'Bevande'
            self.QtaRiga[x] = tempqta
            self.TotaliRiga[x] = tempqta* self.r['Bevande'][item]
            self.PortataPrice[x] = self.r['Bevande'][item]
            x += 1
        #
        # aggiorno il totale del memnu
        #
        self.totmenu = 0
        for i in range(40):
            self.totmenu = self.totmenu + self.TotaliRiga[i]
        self.GrandTotal.SetValue("%.2f" % self.totmenu)

        # handle ticket 
        if self.total_ticket > 0 :
            self.staticLabelTotalTicket.SetLabel("di cui ticket") 
            self.staticTotalTicket.SetLabel("%.2f" % self.total_ticket)

    def RestoCalc(self, event):
        temptotprec = float(self.val_TotPrec.GetValue())
        tempcassa = float(self.val_cassa.GetValue())         
        resto = temptotprec - tempcassa
        self.val_resto.SetValue("%.2f" % resto)

    def OnTimerUpdate(self, event):
        now = datetime.datetime.now()
        dt = str(now.strftime("%d-%m-%Y %H:%M:%S")) + " menu fatti = "+ str(self.menunumero)
        self.datatime_menuprogr.SetLabel(dt)

        # this operation occurs every 3 seconds
        ss = 0
        if (now.second % 3 == 0 ):
            if (ss != now.second) :
                ss= now.second
                #  conteggio e visualizzazione dei piatti a numero limitato
                #i = 0;
                #print ss
                for item in self.r["Primi"]:
                    #print item, 
                    # we change only if qta > 0 to avoid not needed bind on change
                    #self.textFields[item].SetValue("%d" % 0)
                    tqta = int(self.textFields[item].GetValue())
                    temp_res = self.r['QRES'][item] - tqta
                    if (self.r['QINZ'][item] >= 0) :
                        self.labelFields[item].SetLabel("%d" % temp_res)
                    else:
                        self.labelFields[item].SetLabel("")

                for item in self.r["Secondi"]:
                    #print item, 
                    # we change only if qta > 0 to avoid not needed bind on change
                    #self.textFields[item].SetValue("%d" % 0)
                    tqta = int(self.textFields[item].GetValue())
                    temp_res = self.r['QRES'][item] - tqta
                    if (self.r['QINZ'][item] >= 0) :
                        self.labelFields[item].SetLabel("%d" % temp_res)
                    else:
                        self.labelFields[item].SetLabel("")

                for item in self.r["Contorni"]:
                    #print item, 
                    # we change only if qta > 0 to avoid not needed bind on change
                    #self.textFields[item].SetValue("%d" % 0)
                    tqta = int(self.textFields[item].GetValue())
                    temp_res = self.r['QRES'][item] - tqta
                    if (self.r['QINZ'][item] >= 0) :
                        self.labelFields[item].SetLabel("%d" % temp_res)
                    else:
                        self.labelFields[item].SetLabel("")

                for item in self.r["Bevande"]:
                    #print item, 
                    # we change only if qta > 0 to avoid not needed bind on change
                    #self.textFields[item].SetValue("%d" % 0)
                    tqta = int(self.textFields[item].GetValue())
                    temp_res = self.r['QRES'][item] - tqta
                    if (self.r['QINZ'][item] >= 0) :
                        self.labelFields[item].SetLabel("%d" % temp_res)
                    else:
                        self.labelFields[item].SetLabel("")

# not used - moved in OnStampa to abort print if total menu value is 0 is empty
#    def ShowMessage(self):
#        wx.MessageBox('Nulla da stampare', 'Info', 
#            wx.OK | wx.ICON_INFORMATION)

    def OnAnnulla(self, event) :
        # print "Annulla"
        # we change only if qta > 0 to avoid not needed bind on change
        for item in self.r["Primi"]:
            #print item, 
            # we change only if qta > 0 to avoid not needed bind on change
            #self.textFields[item].SetValue("%d" % 0)
            tempqta = int(self.textFields[item].GetValue())
            if tempqta > 0 : self.textFields[item].SetValue("%d" % 0)
            
        for item in self.r["Secondi"]:
            #print item, 
            tempqta = int(self.textFields[item].GetValue())
            if tempqta > 0 : self.textFields[item].SetValue("%d" % 0)
            
        for item in self.r["Contorni"]:
            #print item, 
            tempqta = int(self.textFields[item].GetValue())
            if tempqta > 0 : self.textFields[item].SetValue("%d" % 0)
        
        for item in self.r["Bevande"]:
            #print item, 
            tempqta = int(self.textFields[item].GetValue())
            if tempqta > 0 : self.textFields[item].SetValue("%d" % 0)

        self.staticLabelTotalTicket.SetLabel("") 
        self.staticTotalTicket.SetLabel("")


        # textFields - bottontext is binded on change to self.TotalCalc(0)
        
        #
        # aggiorno il totale del memnu
        #
        #t = 0
        #for i in range(40):
        #    t = t + self.TotaliRiga[i]
        #self.GrandTotal.SetValue("%.2f" % t)

    def OnInfoPortate(self, event) :
        # show a new windows (and give focus to it)
        new_frame = InfoPortate()
        new_frame.Show()
        #return focus to main windows of sagra menu(thanks)
        self.main_win_frame.SetFocus()
        self.InfoPortatePanel = new_frame
    def OnTestMenu(self, event) :
        # print "test menu"
        # print "Annulla"
        # we change only if qta > 0 to avoid not needed bind on change
        for item in self.r["Primi"]:
            #print item, 
            # we change only if qta > 0 to avoid not needed bind on change
            #self.textFields[item].SetValue("%d" % 0)
            tempqta = int(self.textFields[item].GetValue())
            self.textFields[item].SetValue("%d" % 1)

            # experiment how we can change residuo value
            self.labelFields[item].SetLabel("%d" % 0)
            #

        for item in self.r["Secondi"]:
            # print item, 
            tempqta = int(self.textFields[item].GetValue())
            self.textFields[item].SetValue("%d" % 1)
            
        for item in self.r["Contorni"]:
            # print item, 
            tempqta = int(self.textFields[item].GetValue())
            self.textFields[item].SetValue("%d" % 1)
        
        for item in self.r["Bevande"]:
            # print item, 
            tempqta = int(self.textFields[item].GetValue())
            self.textFields[item].SetValue("%d" % 1)

    def OnStorna(self, event) :
        print "Storna"

    def OnRegistra(self, event) :
        # print "Registra" 
        now = datetime.datetime.now()
        filename =  "piatti"+ str(now.strftime("%Y-%m-%d")) + ".csv"
        piatti_log = []
        # print filename
        # print "self.menunumero: ", self.menunumero 
        if os.path.exists(filename):
           piatti_log = load_tabbed_file(filename)

        # file not exixst - create first line of piatti_log list
        if (len(piatti_log) == 0 ) :
           # create array in memory
           # descr, totale, numero menu, valore
           line ="Totali,0,0,0,0" ;
           res = line.split(",")
           piatti_log.append(res); 
           i=1;
           # initialize piatti_log
           self.Piatti_Log_init( piatti_log, "Primi", "Secondi", "Contorni", "Bevande")
           # print piatti_log
        
        # print  "\n  Update array -piatt_log - cvs" ;
        self.Piatti_Log_update(piatti_log, "Primi", "Secondi", "Contorni", "Bevande")
        self.menunumero = piatti_log[0][2]
        save_tabbed_file(filename, piatti_log)

        # clear for next menu
        self.val_TotPrec.SetValue("%.2f" % self.totmenu)
        self.val_TotalTicketPrec.SetLabel("ticket menu prec %.2f" % self.total_ticket) 
        self.OnAnnulla(True)


    def OnStampa(self, event) :
        if self.totmenu == 0:
            dlg = MessageDialog('Nulla da stampare - Menu vuoto', 'Info', 1)
            dlg.ShowModal()
            return
        # print "Stampa"

        # ini setting for print info about menu and data_ora moved after load ini setting

        doc = document(orientation = "portrait")
        doc.begin_document()
        doc.getsize()

        riga = 0
        colonna = 0
        vert = 0

        # todo in bevande we can change descrition only in printed output 
        #      to set this feature portata for bevande must contain *
        #      to handle this feature we use note[] 

        # intestazione  prima   riga Tahoma y (pos 72 ) nuovariga +30 (add to vert) 
        #               seconda riga Arial  y (pos 112) nuovariga +24 (add to vert) 
        #               terza   riga Arial  y (pos 136) nuovariga +24 (add to vert) 
        #               quarta  riga Arial  y (pos 160) nuovariga +24 (add to vert) 

        doc.setfont("Tahoma", 24 )
        #doc.text((72, 72), "Testing...")
        #doc.text((72, 72+48), "Testing #2")
        box = "intestazione" 
        label_override = [""] * 4
        # print "\n",box
        for item in self.r[box]:
            # print
            # print item, self.r[box][item]
            # print riga
            lunghezza_riga = len(self.r[box][item])
            # print lunghezza_riga
            if riga == 0: 
                doc.text((30, 80 ), self.r[box][item])
                nuovariga= 24
                vert += nuovariga
            if (riga > 0 and riga < 4): 
               doc.setfont("Arial",20)
               doc.text((30 + (45-lunghezza_riga/2)*2, 80 + vert), self.r[box][item])
               nuovariga = 20
               vert += nuovariga
            # posizionati sulla riga seguente 
            if riga >= 4 : 
                label_override[ riga -4] = self.r[box][item]
                #break
            riga += 1

        #                   
        #riga data ora menu 
        #                   
        now = datetime.datetime.now()
        filename =  "piatti"+ str(now.strftime("%Y-%m-%d")) + ".csv"
        piatti_log = []
        # print filename
        if os.path.exists(filename):
           piatti_log = load_tabbed_file(filename)
           #self.menunumero = piatti_log[0][2]
           # print "ultimo menu" , piatti_log[0][2]
        doc.setfont("Arial",10, None,1) 
        if self.menu_data_ora == 1:
            riga_data_ora = str(now.strftime("%A-%d-%m-%Y %H:%M:%S")) 
        else:
            riga_data_ora = str(now.strftime("%A-%d-%m-%Y"))
        if self.menu_progr == 1:
            riga_data_ora = riga_data_ora + "    menu = "+ str(int(self.menunumero) + 1)
        doc.text((30, 85 + vert), riga_data_ora)

        #                   
        # stampa piede.bmp  
        #                   
        doc.image((1,580),"piede.bmp",( 500,200))


        # test se gruppo contiene portata da stampare
        x = 0 
        flag = 0
        vert += 14
        for item in self.r["Primi"]:
            if self.QtaRiga[x] > 0 : flag = 1
            x += 1
        if flag == 1:
            # print label_override[0]
            doc.setfont("Arial",16)
            doc.text((30, 80 + vert), label_override[0])
            vert += 16
            doc.setfont("Arial",12)
            x = 0 
            for item in self.r["Primi"]:
                if self.QtaRiga[x] > 0 :
                    # printitem, 
                    # print x, self.Voce[x] , self.Portata[x] , self.QtaRiga[x] , self.TotaliRiga[x] 
                    doc.text((30, 80 + vert), str(self.QtaRiga[x]))
                    doc.text((55, 80 + vert), self.Voce[x])
                    doc.text((360, 80 + vert), u"€")
                    doc.text((400, 80 + vert), str(self.TotaliRiga[x]))
                    vert += 11
                x += 1
   
        x = 10 
        flag = 0
        for item in self.r["Secondi"]:
            if self.QtaRiga[x] > 0 : flag = 1
            x += 1
        if flag == 1:
            # print label_override[1]
            doc.setfont("Arial",16)
            doc.text((30, 80 + vert), label_override[1])
            vert += 16
            doc.setfont("Arial",12)
            x = 10 
            for item in self.r["Secondi"]:
                if self.QtaRiga[x] > 0 : 
                    # printitem, 
                    # print x, self.Voce[x] , self.Portata[x] , self.QtaRiga[x] , self.TotaliRiga[x] 
                    doc.text((30, 80 + vert), str(self.QtaRiga[x]))
                    doc.text((55, 80 + vert), self.Voce[x])
                    doc.text((360, 80 + vert), u"€")
                    doc.text((400, 80 + vert), str(self.TotaliRiga[x]))
                    vert += 11
                x += 1

        # to do 
        # added feature 2011 to handle self service item (only in contorni)
        # the items with @ at first position are not printed on waiter list 
        #  but added in total cash 
        #  on screen there is additional info for the ticket to be delivered 

        x = 20 
        flag = 0

        for item in self.r["Contorni"]:
            # test ticket
            if (item.find ("@") != -1) : ticket = 1
            else : ticket = 0
            if (self.QtaRiga[x] > 0  and ticket == 0 ): flag = 1
            x += 1
        if flag == 1:
            # print label_override[2]
            doc.setfont("Arial",16)
            doc.text((30, 80 + vert), label_override[2])
            vert += 16
            doc.setfont("Arial",12)
            x = 20 
            for item in self.r["Contorni"]:
                # test ticket
                if (item.find ("@") != -1): ticket = 1
                else : ticket = 0
                if (self.QtaRiga[x] > 0  and ticket == 0 ): 
                    # printitem, 
                    # print x, self.Voce[x] , self.Portata[x] , self.QtaRiga[x] , self.TotaliRiga[x] 
                    doc.text((30, 80 + vert), str(self.QtaRiga[x]))
                    doc.text((55, 80 + vert), self.Voce[x])
                    doc.text((360, 80 + vert), u"€")
                    doc.text((400, 80 + vert), str(self.TotaliRiga[x]))
                    vert += 11
                x += 1

        x = 30 
        flag = 0
        for item in self.r["Bevande"]:
            if self.QtaRiga[x] > 0 : flag = 1
            x += 1
        if flag == 1:
            # print label_override[3]
            doc.setfont("Arial",16)
            doc.text((30, 80 + vert), label_override[3])
            vert += 16
            doc.setfont("Arial",12)
            x = 30
            for item in self.r["Bevande"]:
              # printitem, 
              # print x, self.Voce[x] , self.Portata[x] , self.QtaRiga[x] , self.TotaliRiga[x] 
                if self.QtaRiga[x] > 0 : 
                    doc.text((30, 80 + vert), str(self.QtaRiga[x]))
                    doc.text((55, 80 + vert), self.Voce[x])
                    doc.text((360, 80 + vert), u"€")
                    doc.text((400, 80 + vert), str(self.TotaliRiga[x]))
                    vert += 11
                x += 1

        doc.setfont("Arial",18)
        doc.text( (290 , 80+ vert) , "Totale")
        doc.text((360, 80 + vert), u"€")
        doc.text((400, 80 + vert), str(self.totmenu))

        #doc.rectangle((72, 72, 72*6, 72*3))
        #doc.line((72, 72), (72*6, 72*3))

        # added to complete example with print 
        doc.end_page()
        doc.end_document()
        # registra 
        self.OnRegistra(True)

    def OnOmaggi(self, event) :
        # print "Omaggi"
        temp = ""
    def OnClose(self, event) :
        """Prompt to save modified tapes when closing"""

        if event.CanVeto() :
            # Note:  putting this here causes a segmentation fault after the window
            # is destroyed under Linux - I have no idea why; but - it doesn't appear
            # to break anything so I'm leaving it
            # bKill = self.OkToContinue("Close AddMachine")
            bKill = True  
        else :
            bKill = True
                        
        if bKill == True :
            # Keep track of if we are iconized/maximized, and then restore to get accurate size
            if self.IsIconized() :
                self.LastState = -1
                self.Iconize(False)
                self.SendSizeEvent()
            elif self.IsMaximized() :
                self.LastState = 1
                self.Maximize(False)
                self.SendSizeEvent()
            #self.SaveConfiguration()
            self.Destroy()
        else :
            event.Veto(True)

    def OnCloseWindow(self, event):
        self.Destroy
        self.InfoPortatePanel.Close(True)

    def OnExit(self,e):
        """Closes the application"""
        # print "close application"
        if self.InfoPortatePanel :
           self.InfoPortatePanel.Close(True)
        self.Close(True)

    def OnAbout(self,e):
        """Displays about dialog box"""
        dlg = wx.MessageDialog(self, 
            "Menu sagre by Gianni Rossini - magiainformatica@alice.it \n\n" + 
            "Please see additional information in accompanying help file.",
            "Menu Sagre ", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def OnHelp(self, e) :
        """Displays help dialog box"""
        try :
            dlg = HelpDialog(self)
            dlg.ShowModal()
            dlg.Destroy()
        except e :
            self.ShowErrorBox(e, "Unable to Display Help")

if __name__ == '__main__':
    #set italian language (for day week) 
    #locale.setlocale(locale.LC_ALL, "italian")

    #  avoid deprecated message on wx.PySimpleApp()
    #     app = wx.PySimpleApp()
    app = wx.App(None) 
    frame = WxSagra(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
    
