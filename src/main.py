#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : Thu Mar 25 2021
# @Author  : Shanming Liu
# @File    : wxpython_demo3.py
# @Version : 1.0.0

import os
import wx
import wx.lib.imagebrowser as ib

from image_converter import convert_image

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


########################################################################
class InchChoicePanel(wx.Panel):
    def __init__(self,
                 parent,
                 label="Image size",
                 choices=None,
                 callback=None):
        wx.Panel.__init__(self, parent)
        self.label = label
        self.choices = choices if choices else []
        self.callback = callback if callable(
            callback) else lambda evt: print(f'Trigger evt: {evt}')
        # Init the default value
        self.value = self.choices[0] if self.choices else None

        self.initUI()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label=self.label)
        choice = wx.Choice(self, choices=self.choices)
        choice.SetSelection(0) if self.choices else None

        choice.Bind(wx.EVT_CHOICE, self.onChange)

        sizer.Add(text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(choice, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def onChange(self, event):
        if event.GetString() != self.value:
            self.value = event.GetString()
            self.callback(event.GetString())


class ConditionPanel(wx.Panel):
    def __init__(self, parent, callback=None):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.callback = callback if callable(
            callback) else lambda *args: print(args)
        self.selectedImage = None
        self.convertedImage = None

        self.initUI()

    def initUI(self):
        self.SetBackgroundColour('yellow')
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.idInchChoice = InchChoicePanel(self,
                                            "证件尺寸", ['1', '2', '1&2'],
                                            callback=self.onIDInchChange)
        self.photoInchChoice = InchChoicePanel(self,
                                               "照片尺寸", ['5', '6'],
                                               callback=self.onPhotoInchChange)
        importBtn = wx.Button(self, label='导入图片')
        exportBtn = wx.Button(self, label='导出图片')

        importBtn.Bind(wx.EVT_BUTTON, self.loadImageFile)
        exportBtn.Bind(wx.EVT_BUTTON, self.saveImageFile)

        sizer.Add(self.idInchChoice, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.photoInchChoice, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(importBtn, 2, wx.ALL | wx.EXPAND, 20)
        sizer.Add(exportBtn, 2, wx.ALL | wx.EXPAND, 20)
        self.SetSizer(sizer)

    def onIDInchChange(self, _):
        if self.selectedImage:
            self.convertImage(self.selectedImage, self.idInchChoice.value,
                              self.photoInchChoice.value)

    def onPhotoInchChange(self, _):
        if self.selectedImage:
            self.convertImage(self.selectedImage, self.idInchChoice.value,
                              self.photoInchChoice.value)

    def loadImageFile(self, _):
        with ib.ImageDialog(self, set_dir=os.getcwd()) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.selectedImage = dialog.GetFile()
                self.convertImage(self.selectedImage, self.idInchChoice.value,
                                  self.photoInchChoice.value)

    def saveImageFile(self, _):
        with ib.ImageDialog(self, set_dir=os.getcwd()) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.callback(dialog.GetFile())

    def convertImage(self, selectedImage, idInch, photoInch):
        self.convertedImage = convert_image(selectedImage, idInch,
                                            photoInch)
        self.callback(self.convertedImage)


########################################################################
class MainPanel(wx.Panel):
    """"""
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.initUI()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        condition_panel = ConditionPanel(self, callback=self.generatedImage)
        self.image_panel = image_panel = ib.ImagePanel(self)
        sizer.Add(condition_panel, 0, wx.EXPAND)
        sizer.Add(image_panel, 3, wx.EXPAND)

        self.SetSizer(sizer)

    def generatedImage(self, tmpImage):
        print(f"Converted image: {tmpImage}")
        self.image_panel.SetValue(tmpImage)


########################################################################
class MainFrame(wx.Frame):
    """"""
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Image converter", size=(600, 400))
        MainPanel(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
