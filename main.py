from GUI import gui
import m3u_helper
import wx
from threading import Thread

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
app = wx.App() 

def EVT_RESULT(win, func):
	"""Define Result Event."""
	win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

########################################################################
class asyncLoad(Thread):
       
    #----------------------------------------------------------------------
    def __init__(self, window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.window = window
        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):

        """Run Worker Thread."""
        wx.PostEvent(self.window, ResultEvent("Start Loading..."))
        LST_M3U_ITEMS = m3u_helper.parse_m3u(window.loadFile.GetPath())
        root = window.treeList.GetRootItem()

        def sub(window,l,grp_node,gname):
            for l in category:
                child_node = window.treeList.AppendItem(grp_node, "")
                window.treeList.SetItemText(child_node, 0, "")
                window.treeList.SetItemText(child_node, 1, l[4])
                window.treeList.SetItemText(child_node, 2, l[2])
                window.treeList.SetItemText(child_node, 3, l[1])
                window.treeList.SetItemText(child_node, 4, l[3])  
                window.treeList.SetItemText(child_node, 5, l[5])  

            wx.PostEvent(self.window, ResultEvent(f"Loading {gname}..."))
                                                 
        for k,category in LST_M3U_ITEMS.items():
            grp_node = window.treeList.AppendItem(root, k)
            window.treeList.SetItemText(grp_node, 0, k)                    
            Thread(target=sub,args=(window,category,grp_node,k)).start()


        wx.PostEvent(self.window, ResultEvent("Loading finished!"))

def config_btns(window):    
    # Loading
    def load_m3u(_):
        window.treeList.DeleteAllItems()
        thread = asyncLoad(window)

    window.load.Bind(wx.EVT_BUTTON, load_m3u) 
    
    # Delete
    def delete(_):
        sels = window.treeList.GetSelections()
        for s in sels:
            window.treeList.DeleteItem(s)
        pass
    window.delete.Bind(wx.EVT_BUTTON, delete)

    # Export
    def export(_):
        checkedItems = []              
        item = window.treeList.GetFirstItem()
        while item.IsOk():
            checkedItems.append(window.treeList.GetItemText(item,5))
            item = window.treeList.GetNextItem(item)
                        
        with open("outfile.m3u", "w") as outfile:
            outfile.write("\n".join(checkedItems))
        
    window.export.Bind(wx.EVT_BUTTON, export)
    
    # Exit
    def exit(_):
        app.ExitMainLoop()
    window.exit.Bind(wx.EVT_BUTTON, exit)

def config_list(window):    
    window.treeList.AppendColumn("Category")
    window.treeList.AppendColumn("Name")    
    window.treeList.AppendColumn("Stream link")    
    window.treeList.AppendColumn("Is Video link")    
    window.treeList.AppendColumn("Logo")    
    window.treeList.AppendColumn("Raw")    


def config_update_display(window):
    def updateDisplay( msg):        
        t = msg.data
        window.statusBar.SetStatusText(t,1)
        
    EVT_RESULT(window, updateDisplay)

if __name__ == '__main__':
       
    window = gui.MainFrame(None)
        
    config_update_display(window)
    config_btns(window)
    config_list(window)
    
    window.Show()
    app.MainLoop()