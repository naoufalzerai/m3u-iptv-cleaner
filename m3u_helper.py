import os
import re

def meta(l):
    # result = re.findall(r'(http://.*(\.mkv|\.mp4|\.avi))|(tvg-logo=\"((.|\n)*?)\")|(tvg-name=\"((.|\n)*?)\")|(group-title=\"((.|\n)*?)\")', l)

    vidLink= re.findall(r'(http://.*(\.mkv|\.mp4|\.avi))|(http://.*(\.png|\.jpg|\.jpeg))', l)
    streamLink= re.findall(r'(http://.*)', l)
    logo= re.findall(r'(tvg-logo=\"((.|\n)*?)\")', l)
    name= re.findall(r'(tvg-name=\"((.|\n)*?)\")', l)
    group= re.findall(r'(group-title=\"((.|\n)*?)\")', l)

    def ret_best(a):
        if(len(a)==0):
            return ''
        elif (type(a[0]) is tuple):
            return a[0][1]
        else:
            return a[0]
    return (
                ret_best(vidLink),
                ret_best(streamLink),
                ret_best(logo),
                ret_best(name),
                ret_best(group)
            )
        

def parse_m3u(source):

    result = []

    infile = open(source, 'r')
    lines = infile.readlines()
    buffer=[]
    
    for l in lines:
        l = l.rstrip()
        if(l != "#EXTM3U"):
            
            if("#EXTINF" in l):
                # if buffer not null insert
                if(len(buffer)!=0):
                    m = meta( '\n'.join(buffer))
                    result.append(m)
                # else empty buffer
                buffer=[]
                buffer.append(l)
            else:
                buffer.append(l)
    return result
    