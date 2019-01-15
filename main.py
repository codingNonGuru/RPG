import engine
import scene
import server 

def runLoop(callback):
    callback()

from multiprocessing.dummy import Pool as ThreadPool 
pool = ThreadPool(2) 
pool.map(runLoop, [server.Server.Get().Start, engine.Engine.Get().Refresh])
