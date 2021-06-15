from glob import glob
import sys
import os
os.environ['NUMEXPR_MAX_THREADS'] = str(1)
import subprocess
import tempfile

import pandas as pd
import numpy as np

from .. import settings
from .. import logging as logg

def vector_field(tdata, 
                      gridRes: int = 30, 
                      smooth: float = 0.5): 
    
    allparents=np.unique(tdata["Parent"])
    allparents=allparents[~np.isnan(allparents)]
    ldata=list(map(lambda x: tdata[["Position X","Position Y","Time"]].loc[tdata.index[tdata["Parent"].isin([x],)]], 
                     [par for par in allparents]))
    
    vfkm = settings.vfkm

    logg.info("Generating grid vector field")
    with tempfile.TemporaryDirectory() as tmp:
        #logg.hint("    Data temporary saved in "+tmp)
        init=[min(tdata["Position X"]),max(tdata["Position X"]),
              min(tdata["Position Y"]),max(tdata["Position Y"]),
              1,max(tdata["Time"])]
        with open(tmp+'/tracks', 'w') as f:
            f.writelines(["%s " % item  for item in init])
        for ld in ldata:
            ld.to_csv(tmp+'/tracks', mode='a', header=False,sep=" ",index=False)
            pd.DataFrame([0,0,0]).transpose().to_csv(tmp+'/tracks',
                                                     header=False,
                                                     sep=" ",
                                                     mode="a",
                                                     index=False)
          

        proc = subprocess.Popen(vfkm+" "+tmp+"/tracks "+str(gridRes)+" 1 "+str(smooth)+" "+tmp, 
                                stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        files_c = [f for f in glob(tmp+"/*curves_r_*", recursive=True)]
        files_v = [f for f in glob(tmp+"/*vf_r_*", recursive=True)]
        curves=pd.read_table(files_c[0],header=None,sep=" ")
        vect=pd.read_table(files_v[0],header=None,sep=" ",skiprows=1)    

    gs=int(np.sqrt(vect.shape[0]))

    a=np.linspace(min(pd.concat(ldata)["Position X"]),max(pd.concat(ldata)["Position X"]),gs)
    b=np.linspace(min(pd.concat(ldata)["Position Y"]),max(pd.concat(ldata)["Position Y"]),gs)
    out = np.stack([each.ravel(order='C') for each in np.meshgrid(a, b)])
    
    u=vect[0].values.reshape(gs,gs)
    v=vect[1].values.reshape(gs,gs)
    X,Y = np.meshgrid(a, b)
    
    return X, Y, u, v
