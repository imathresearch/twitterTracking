import datetime
from Queue import Empty
import json

class PartialDataWriter(object):
    
    def __init__(self, input_queu, fileName_writeOut, write_frecuency):
        self.file = fileName_writeOut;
        self.queue = input_queu;
        self.write_frecuency = write_frecuency 
   
    def run(self):
        more = True
        last_write = datetime.datetime.now()
        dic = {}

        while more is True:
            ts = self.write_frecuency - int((datetime.datetime.now() - last_write).total_seconds())
            try:
                val = self.queue.get(block=True, timeout=ts)
                for key in val.keys():
                    if key == "END" and val[key] == -1:
                        more = False
                    else:
                        if key not in dic.keys():
                            dic[key] = []
                        dic[key].append(val[key])
            except Empty:
                pass
            
            if more is False or (datetime.datetime.now() - last_write).total_seconds() > self.write_frecuency:
                now = datetime.datetime.now()
                f1=open(self.file, 'w')
                print >>f1, json.dumps(dic)
                f1.close();
                last_write = now

