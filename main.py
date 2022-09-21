#!/usr/bin/env python
from select import select
import sys
import PySimpleGUI as sg
import m3u_helper
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

POOL_SIZE = 50

class Tree_Data(sg.TreeData):

    def __init__(self):
        super().__init__()

    def move(self, key1, key2):
        if key1 == '':
            return False
        node = self.tree_dict[key1]
        parent1_node = self.tree_dict[node.parent]
        parent1_node.children.remove(node)
        parent2_node = self.tree_dict[key2]
        parent2_node.children.append(node)
        return True

    def load(self,file):
        LST_M3U_ITEMS = m3u_helper.parse_m3u(file)
        
        def sub(args):
            try:
                gname= args[0]
                category= args[1]                
                
                self.Insert('', gname, gname,values=[len(category)])
                for l in category:
                    self.Insert(gname, l[4], l[4],values=[l[5]])
            except:
                pass

        with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            args = ((k,category)for k,category in LST_M3U_ITEMS.items())            
            args = list(args)
            executor.map(sub,args)

    def delete(self, key):
        if key == '':
            return False
        node = self.tree_dict[key]
                
        self.tree_dict[node.parent].children.remove(node)
        return True

    def export(self,file):   
        selected = ['#EXTM3U']     
        for cat in self.tree_dict[''].children:
            if len(self.tree_dict[cat.key].children)>0:
                for s in self.tree_dict[cat.key].children:
                    val = s.values[0]
                    if not isinstance(val,int):
                        selected.append(val)

        with open(f"{file}.m3u", "w") as outfile:
            outfile.write("\n".join(selected))

treedata = Tree_Data()

starting_path = sg.popup_get_file('File to load')

if not starting_path:
    sys.exit(0)

treedata.load(starting_path)

layout = [[sg.Text('Browse channels')],
          [sg.Tree(data=treedata,
                   headings=['Size', ],
                   auto_size_columns=True,
                   select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                   num_rows=20,
                   col0_width=40,
                   key='-TREE-',
                   show_expanded=False,
                   enable_events=True,
                   expand_x=True,
                   expand_y=True,
                   ),],
          [sg.Button('Delete'),sg.Button('Export'), sg.Button('Cancel')]]

window = sg.Window('M3U Editor', layout, resizable=True, finalize=True)


while True:     # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event in ('Export'):
        save = sg.popup_get_text('Save file')
        treedata.export(save)

    if event in ('Delete'):   
        with ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            executor.map(lambda n:treedata.delete(n),values['-TREE-'])        
        window['-TREE-'].Update(values=treedata)
   
