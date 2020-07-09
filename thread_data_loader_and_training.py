# https://www.tutorialspoint.com/python/python_multithreading.htm

import numpy as np
import time
import threading

def holdon(flag,intv,lapse,name):
    cntr = 0
    while 1:
        if flag[0] is True:
            print(name,'-- released ')
            return
        time.sleep(intv) # sleep 10 seconds
        cntr += 1
        print('waiting for ',name,' to release: ',cntr)
        if cntr > lapse:
            print('cannot get data after time lapsed')
            break
# ==============================================

class MLtrainer:

    def __init__(self,data_loader):
        self.data_loader = data_loader
        self.epoch = 0
        self.data = None
        self.train_lapse = 3

    def run(self):
        print('start training . . ',self.epoch)
        self.data = self.data_loader.fetch_data()
        self.do_training()
        print('end training . .',self.epoch)

    def do_training(self):
        for i in range(self.train_lapse):
            print('training ',i,'/',self.train_lapse,\
                  ' on data ',self.data)
            time.sleep(1)
        self.epoch += 1
        time.sleep(1)
# --------------------------------------------

class data_loader:

    def __init__(self):
        self.data_ready   = None
        self.data_swap    = None
        self.data_loading = None
        self.ready_flag = [False]
        self.loader_lapse = 5
        self.epoch = 0

    def run(self):

        print('start loading data . . epoch ',self.epoch) 
        self.ready_flag[0] = False
        self.load_data()
        self.swap_data()
        self.ready_flag[0] = True
        print('end: data waiting to get fetched: epoch ',self.epoch) 
        self.epoch += 1

    def swap_data(self):

        # load data and then swap so that 
        # loader can load the next set of data 
        # and then wait for trainer to fetch
        self.data_swap = self.data_loading
        self.data_loading = self.data_ready
        # do the final swap only after trainer fetch the
        # previous set of data
        query_flag = [not i for i in self.ready_flag]
        holdon(query_flag,intv=2,lapse=4,name='swap data lock')
        self.data_ready = self.data_swap 

    def load_data(self):
        self.data_loading = self.epoch*np.ones(4)
        for i in range(self.loader_lapse):
            print('loading ',i,'/',self.loader_lapse,\
                  ' iteration ',self.data_loading)
            time.sleep(1)

    def fetch_data(self):

        print('start fetch data')
        holdon(self.ready_flag,intv=2,lapse=4,name='fetch data lock')
        print('end fecth data : to load more data for standby ')
        return self.data_ready

# ===================================================

class myThread (threading.Thread):

    def __init__(self,obj,ID):
        super(myThread,self).__init__()

        self.ID = ID
        self.obj = obj

    def run(self):
        print('starting thread for ',self.obj)
        self.obj.run()
        print('exiting thread for ',self.obj)
# ===================================================
if __name__=='__main__':

    d_loader = data_loader()
    trainer  = MLtrainer(d_loader)
    
    d_loader.run() # single thread to load first set of data

    for i in range(10):
        data_thread = myThread(d_loader,0)
        ML_thread = myThread(trainer,0)
        ML_thread.start()
        data_thread.start()
        ML_thread.join()
        data_thread.join()

