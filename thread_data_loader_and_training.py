# https://www.tutorialspoint.com/python/python_multithreading.htm

import numpy as np
import time
import threading

def holdon(flag,name,intv=1,lapse=10):
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
        self.itr = 0
        self.data = None
        self.train_lapse = 3

    def run(self):
        #print('start training . . ',self.itr)
        self.data = self.data_loader.fetch_data()
        self.do_training()
        #print('end training . .',self.itr)

    def do_training(self):
        for i in range(self.train_lapse):
            print('training ',i,'/',self.train_lapse,\
                  ' on data ',self.data)
            time.sleep(1)
        self.itr += 1
        time.sleep(1)
# ==============================================

class data_loader:

    def __init__(self):
        self.data_ready   = None
        self.data_swap    = None
        self.data_loading = None
        self.ready_flag = [False]
        self.swap_flag = [True]
        self.loader_lapse = 2
        self.itr = 0

    def run(self):

        self.ready_flag[0] = False
        self.load_data() # load into data_loading
        self.ready_flag[0] = True
        self.itr += 1

    # swap data_loading with data_ready
    # so loader can load the next set of data
    # onto data_loading again
    # and then wait for trainer to fetch
    def swap_data(self):

        self.data_swap = self.data_loading
        self.data_loading = self.data_ready
        # do the final swap only after trainer query
        # for the next set of data
        self.data_ready = self.data_swap 
        self.swap_flag[0] = True

    # load data into data_loading 
    # which is a holding place for data
    def load_data(self):
        # load data only if it has been swapped out
        holdon(self.swap_flag,name='swap data lock')
        self.swap_flag[0] = False
        self.data_loading = self.itr*np.ones(4)
        for i in range(self.loader_lapse):
            print('loading ',i,'/',self.loader_lapse,\
                  ' iteration ',self.data_loading)
            time.sleep(1)

    # check that data is ready and then fetch it
    def fetch_data(self):

        holdon(self.ready_flag,name='fetch data lock')
        self.swap_data() # swap the data and return data
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

    for i in range(5):
        data_thread = myThread(d_loader,0)
        ML_thread = myThread(trainer,0)
        ML_thread.start()
        data_thread.start()
        ML_thread.join()
        data_thread.join()
        del(data_thread)  # delete thread object
        del(ML_thread)    # delete thread object

