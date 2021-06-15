import matplotlib.pyplot as plt
import numpy as np
import SimplePPT


def fit_ppt(img,ppts,tdata,times=None,**kwargs):  
    times=tdata.Time.unique() if times is None else times
    fig,ax = plt.subplots()
    ax.set_aspect('equal')
    i=0
    for t in times:
        toproject = tdata.loc[tdata.Time==t,["Position X","Position Y"]]
        SimplePPT.project_ppt(ppts[i],toproject,ax=ax,plot_datapoints=False,alpha_nodes=0,alpha_seg=.05,show=False)
        i=i+1
    ax.imshow(img,origin='lower')
    #ax.scatter(mouthpos["Position X"],mouthpos["Position Y"],zorder=2000,s=100,c="red")
    ax.axis("off")
    plt.tight_layout()