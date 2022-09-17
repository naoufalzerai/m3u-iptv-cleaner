import os
import confuse
from sqlite3 import connect
import re
import wget

from clint.textui import progress


def insert_meta(l,curs):
    result = re.findall(r'(http://.*(\.mkv|\.mp4|\.avi))|(tvg-logo=\"((.|\n)*?)\")|(tvg-name=\"((.|\n)*?)\")|(group-title=\"((.|\n)*?)\")', l)
    if len(result)>3:
        # print(len(result))
        curs.execute("insert into chan values (NULL,?,?,?,0,?)",(result[0][6],result[3][0],result[2][9],result[1][3]))
        
        
def download(curs,out,cat):    
    #in_clause= "('{0}')".format("','".join(cat))
    #res = curs.execute("Select name,url,id from chan where dnwl=1 and cat in {0}".format(in_clause))
    res = curs.execute("Select name,url,id from chan where dnwl=1")
    for meta in res:
        print(meta[0])
        path = '{0}/{1}.mkv'.format(out,meta[0])
        if os.path.isfile(path)==False:
            url=meta[1]
            try:
                # r = requests.get(url, stream=True, headers={'Accept-Encoding': None, 'Content-Encoding':'gzip'}) #requests.get(meta[1], stream=True)
                
                # with open(path, 'wb') as f:
                #     total_length = int(r.headers.get('Content-Length'))
                #     for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                #         if chunk:
                #             f.write(chunk)
                #             f.flush()
                wget.download(url,path)
            except NameError:
                traceback.print_exc()
                pass
            
       
def main():
    config = confuse.Configuration("DownloadVid")
    config.set_file('config.yaml')
    source = config['input'].get()
    db = config['db'].get()
    output = config['output'].get()
    cat = config['cat'].get()
    mode_download= config['mode_download'].get()
    busy = config['busy'].get()
    
    if busy:
        print("busy...")
        return 0
    
    conn = connect(r"{0}".format(db))
    curs = conn.cursor()
    
    if mode_download==0:
        curs.execute("delete from chan where 1=1")
        infile = open(source, 'r')
        lines = infile.readlines()
        
        buffer=[]
        
        for l in lines:
            l = l.rstrip()
            if(l != "#EXTM3U"):
                
                if("#EXTINF" in l):
                    # if buffer not null insert
                    if(len(buffer)!=0):
                        insert_meta( '\n'.join(buffer),curs)
                    # else empty buffer
                    buffer=[]
                    buffer.append(l)
                else:
                    buffer.append(l)
                            
        conn.commit()
    
    else:
        download(curs,output,cat)
    conn.close()

if __name__ == '__main__':
    main()