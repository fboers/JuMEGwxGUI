#!/usr/bin/env python3

import os
import sys
import wx
import json
import yaml

# https://github.com/amitizle/wxpython-examples/blob/master/config_parser.py

class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(1000,500))
    self.control = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT)
    self.tree_root = self.control.AddRoot("TREE_ROOT")
    self.CreateStatusBar()
    self.build_menu()
    self.Centre()
    self.Show(True)

  def alert_info(self, message, title):
    wx.MessageBox(message, title, wx.OK | wx.ICON_INFORMATION)

  def alert_error(self, message, title):
    wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR)

  def alert_warn(self, message, title):
    wx.MessageBox(message, title, wx.OK | wx.ICON_WARNING)

  def build_menu(self):
    # Setting up the menu.
    filemenu= wx.Menu()

    # file_open
    on_open_item = filemenu.Append(wx.ID_OPEN, "&Open file", " Open a file for reading")
    self.Bind(wx.EVT_MENU, self.on_file_open, on_open_item)
    # seperator
    filemenu.AppendSeparator()
    # exit
    exit_item = filemenu.Append(wx.ID_EXIT,"&Exit"," Exit the application")
    self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
    # about menu
    about_menu = wx.Menu()
    author = about_menu.Append(wx.ID_DEFAULT, "&Author"," Amit Goldberg")
    self.Bind(wx.EVT_MENU, self.on_author, author)
    about_menu.AppendSeparator()
    about_item = about_menu.Append(wx.ID_ABOUT, "&About"," Information about json/yml parser")
    self.Bind(wx.EVT_MENU, self.on_about, about_item)
    # Creating the menubar.
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
    menuBar.Append(about_menu, "&About")
    self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

  def on_author(self, event):
    message = wx.MessageDialog(self, "Amit Goldberg\namit.goldberg@gmail.com", "Amit Goldberg", wx.OK)
    message.ShowModal()
    message.Destroy()

  def on_about(self, event):
    message_string = "YAML/JSON parser was developed in my FREE TIME, on a windy Satruday when outside was cold and while i tried to learn some python ui programming.\nThis application is built using wxPython."
    message = wx.MessageDialog(self, message_string, "YAML/JSON parser",  wx.OK)
    message.ShowModal()
    message.Destroy()

  def on_exit(self, event):
    self.Close(True)

  def on_file_open(self, event):
    self.dirname = "."
    dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.js;*.json;*.yaml;*.yml", style=wx.FD_OPEN| wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      dirname = dlg.GetDirectory()
      f = open(os.path.join(dirname, filename), 'r')
      map_string = f.read()
      f.close()
      self.parse_file(map_string, filename)
      self.control.Expand(self.tree_root)
    dlg.Destroy()

  def parse_file(self, map_string, filename):
    try:
      ext = filename.split(".")[-1]
      if ext == "yaml" or ext == "yml":
        self.parse_yaml_to_tree(map_string, self.tree_root)
      elif ext == "js" or ext == "json":
        self.parse_json_to_tree(map_string, self.tree_root)
    except Exception as e:
      error_str = "Couldn't parse file: %s" % e
      self.alert_error(error_str, "Houston, we have a problem!")

  def parse_yaml_to_tree(self, yaml_string, root):
    ym = yaml.load(yaml_string)
    self.build_tree_recursive(ym, root)

  def parse_json_to_tree(self, json_string, root):
    js = json.loads(json_string)
    self.build_tree_recursive(js, root)

  def build_tree_recursive(self, sub_tree, root):
    if type(sub_tree) is list:
      for item in sub_tree:
        if type(item) is list or type(item) is dict:
          self.build_tree_recursive(item, root)
        else:
          self.control.AppendItem(root, str(item))
    elif type(sub_tree) is dict:
      curr_root = None
      for key,val in sub_tree.items():
        curr_root = self.control.AppendItem(root, key)
        self.build_tree_recursive(val, curr_root)
    else:
      if sub_tree is not None:
        self.control.AppendItem(root, str(sub_tree))
      else:
        self.control.AppendItem(root, "null")

app = wx.App(False)
frame = MainWindow(None, "JSON/YAML parser")
app.MainLoop()
