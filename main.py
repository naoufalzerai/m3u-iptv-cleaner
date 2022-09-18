from GUI import gui
import m3u_helper
import wx
from threading import Thread



# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()


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
    """Test Worker Thread Class."""
        
    #----------------------------------------------------------------------
    def __init__(self, window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.window = window
        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        lst = m3u_helper.parse_m3u(window.loadFile.GetPath())
        root = window.treeList.GetRootItem()

        def sub(window,l,grp_node,gname):
            for l in category:
                child_node = window.treeList.AppendItem(grp_node, "")
                window.treeList.SetItemText(child_node, 0, "")
                window.treeList.SetItemText(child_node, 1, l[4])
                window.treeList.SetItemText(child_node, 2, l[2])
                window.treeList.SetItemText(child_node, 3, l[1])
                window.treeList.SetItemText(child_node, 4, l[3])  

            wx.PostEvent(self.window, ResultEvent(f"Loading {gname}"))
                                                 
        for k,category in lst.items():
            grp_node = window.treeList.AppendItem(root, k)
            window.treeList.SetItemText(grp_node, 0, k)                    
            Thread(target=sub,args=(window,category,grp_node,k)).start()


        wx.PostEvent(self.window, ResultEvent("Thread finished!"))

def config_btn_load(window):
    def load_m3u(_):
        thread = asyncLoad(window)

    window.load.Bind(wx.EVT_BUTTON, load_m3u) 

def config_list(window):
    
    window.treeList.AppendColumn("Category")
    window.treeList.AppendColumn("Name")    
    window.treeList.AppendColumn("Stream link")    
    window.treeList.AppendColumn("Video link")    
    window.treeList.AppendColumn("Logo")    

def updateDisplay( msg):
    """
    Receives data from thread and updates the display
    """
    t = msg.data
    print(t)

if __name__ == '__main__':
    app = wx.App()
    # Set up event handler for any worker thread results
    	
    window = gui.MainFrame(None)
    EVT_RESULT(window, updateDisplay)

    config_btn_load(window)
    config_list(window)

    
    window.Show()
    app.MainLoop()