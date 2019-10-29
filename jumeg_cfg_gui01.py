#!/usr/bin/env python3
# -+-coding: utf-8 -+-

"""
"""

#--------------------------------------------
# Authors: Frank Boers <f.boers@fz-juelich.de> 
#
#-------------------------------------------- 
# Date: 29.10.19
#-------------------------------------------- 
# License: BSD (3-clause)
#--------------------------------------------
# Updates
#--------------------------------------------

import os,sys,argparse

import wx
from jumeg_base_config import JuMEG_CONFIG_YAML_BASE


import logging
from jumeg.base import jumeg_logger
logger = logging.getLogger('jumeg')


__version__="2019-10-29-001"

class CtrlPanel(wx.Panel):
    def __init__(self,parent,**kwargs):
        super().__init__(parent)
        self._wx_init(**kwargs)
        self._ApplyLayout()
    @property
    def cfg(self): return self._CFG
    
    def _wx_init(self,**kwargs):
        self.SetBackgroundColour(wx.GREEN)
       #--- load cfg
        self._CFG =  JuMEG_CONFIG_YAML_BASE(**kwargs)
        self._CFG.update(**kwargs)
       #--- init panel
        self._pnl1 = wx.Panel(self)
        self._pnl1.SetBackgroundColour(wx.BLUE)
       #--- init show button
        self._bt = wx.Button(self,label="Show Config",name="BT_INFO")
        self.Bind(wx.EVT_BUTTON,self.ClickOnButton)
        
    def _ApplyLayout(self):
        LEA = wx.LEFT|wx.EXPAND|wx.ALL
      
        vbox = wx.BoxSizer(wx.VERTICAL)
       #---
        st1 = wx.StaticLine(self)
        st1.SetBackgroundColour("GREY85")
        st2 = wx.StaticLine(self)
        st2.SetBackgroundColour("GREY80")
        
        vbox.Add(st1,0,LEA,1)
        vbox.Add(self._pnl1,1,LEA,1)
        vbox.Add(st2,0,LEA,1)
        vbox.Add(self._bt,0,LEA,2)
    
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        self.Fit()
        self.Layout()

    def ClickOnButton(self,evt):
        obj = evt.GetEventObject()
        if obj.GetName() == "BT_INFO":
           self.cfg.info()

class MainWindow(wx.Frame):
  def __init__(self, parent, title, **kwargs):
    wx.Frame.__init__(self, parent, -1,title=title)
    self._wx_init(**kwargs)
   
  def _update_from_kwargs(self,**kwargs):
      pass
  
  def _wx_init(self,**kwargs):
        w,h = wx.GetDisplaySize()
        self.SetSize(w/4.0,h/3.0)
        self.Center()
        
        self._update_from_kwargs(**kwargs)
      #--- init STB in a new CLS
        self._STB = self.CreateStatusBar()
        
        self._PNL = CtrlPanel(self,**kwargs)
      
      #--- ToDo init OnClose
       #self.Bind(wx.EVT_CLOSE,   self.ClickOnClose)
      
#---
def run(opt):
    if opt.debug:
        opt.verbose = True
        opt.debug   = True
        opt.path    = "./config/"
        opt.config  = "test_config.yaml"
    
    app = wx.App()
    
    if opt.path:
       cfg = os.path.join((opt).path,opt.config)
    else:
       cfg = opt.config
       
    frame = MainWindow(None,'JuMEG Config',config=cfg,verbose=opt.verbose,debug=opt.debug)
    frame.Show()
    
    app.MainLoop()

    
#----
def get_args(argv):
    info_global = """
     JuMEG Config GUI Start Parameter

     ---> view time series data FIF file
      jumeg_cfg_gui01.py --config=test_config.yaml --path=./config -v

    """
   
    parser = argparse.ArgumentParser(info_global)
    
    parser.add_argument("-p","--path",help="config file path")
    parser.add_argument("-cfg","--config",help="config file name")
    
    parser.add_argument("-v","--verbose",action="store_true",help="verbose mode")
    parser.add_argument("-d","--debug",action="store_true",help="debug mode")
    
    #--- init flags
    # ck if flag is set in argv as True
    # problem can not switch on/off flag via cmd call
    opt = parser.parse_args()
    for g in parser._action_groups:
        for obj in g._group_actions:
            if str(type(obj)).endswith('_StoreTrueAction\'>'):
                if vars(opt).get(obj.dest):
                    opt.__dict__[obj.dest] = False
                    for flg in argv:
                        if flg in obj.option_strings:
                           opt.__dict__[obj.dest] = True
                           break
    
    return opt,parser


#=========================================================================================
#==== MAIN
#=========================================================================================
if __name__ == "__main__":
    opt,parser = get_args(sys.argv)
    
    if len(sys.argv) < 2:
       parser.print_help()
       sys.exit(-1)
       
    jumeg_logger.setup_script_logging(name=sys.argv[0],opt=opt,logger=logger)
    
    run(opt)