#!/usr/bin/env python
from select import select
import sys
import PySimpleGUI as sg
import m3u_helper
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

POOL_SIZE = 50
# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'


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
                
                self.Insert('', gname, gname,values=[len(category)], icon=folder_icon)
                for l in category:
                    self.Insert(gname, l[4], l[4],values=[l[5]], icon=file_icon)
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
        
        parent_node = self.tree_dict[node.parent]
        parent_node.children.remove(node)
        return True

    def export(self,file):   
        selected = ['#EXTM3U']     
        for cat in self.tree_dict:
            if len(self.tree_dict[cat].values)>0:
                val = self.tree_dict[cat].values[0]
                if not isinstance(val,int):
                    selected.append(val)

        with open(f"{file}.m3u", "w") as outfile:
            outfile.write("\n".join(selected))

treedata = Tree_Data()

starting_path = sg.popup_get_file('File to load')

if not starting_path:
    sys.exit(0)

treedata.load(starting_path)

layout = [[sg.Text('Browse chanels')],
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
   
