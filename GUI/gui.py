# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		Stack = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 0, 5, 0, 0 )

		self.loadFile = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		gSizer1.Add( self.loadFile, 0, wx.ALL, 5 )

		self.load = wx.Button( self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.load, 0, wx.ALL, 5 )

		self.delete = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.delete, 0, wx.ALL, 5 )

		self.export = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.export, 0, wx.ALL, 5 )

		self.exit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.exit, 0, wx.ALL, 5 )


		Stack.Add( gSizer1, 1, wx.EXPAND, 5 )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Select" ), wx.VERTICAL )

		sbSizer2.SetMinSize( wx.Size( -1,1000 ) )
		self.treeList = wx.dataview.TreeListCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_MULTIPLE )

		sbSizer2.Add( self.treeList, 1, wx.EXPAND |wx.ALL, 5 )


		Stack.Add( sbSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( Stack )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


