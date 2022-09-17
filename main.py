from GUI import gui
import m3u_helper
import wx


def config_btn_load(window):
    def load_m3u(_):
        lst = m3u_helper.parse_m3u(window.loadFile.GetPath())
        root = window.treeList.GetRootItem()
                        
        for l in lst:
            grp_node = window.treeList.AppendItem(root, "A GROUP")
            window.treeList.SetItemText(grp_node, 0, "A GROUP")
            window.treeList.SetItemText(grp_node, 1, "A")
            window.treeList.SetItemText(grp_node, 2, "B")

            for child_str in lst:
                child_node = window.treeList.AppendItem(grp_node, "A CHILD")
                window.treeList.SetItemText(child_node, 0, "A CHILD")
                window.treeList.SetItemText(child_node, 1, "a")
                window.treeList.SetItemText(child_node, 2, "b")



    window.load.Bind(wx.EVT_BUTTON, load_m3u) 

def config_list(window):
    
    window.treeList.AppendColumn("Category")
    window.treeList.AppendColumn("Name")    
    window.treeList.AppendColumn("URL")    



if __name__ == '__main__':
    app = wx.App()
    window = gui.MainFrame(None)

    config_btn_load(window)
    config_list(window)

    window.Show()
    app.MainLoop()