import numpy as np
import matplotlib.colors as cols
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg 
from numba import njit
import math


@njit
def sinuosity_max(x,y,dx,dy,win):
    dist=np.sqrt((x-dx)**2 + (y-dy)**2)
    sinuosities=np.empty(len(x))
    sinuosities.fill(np.nan)
    for w in range(0,(x.shape[0]-win)):
        ppd=np.sqrt((x[w+win]-x[w])**2 + (y[w+win]-y[w])**2)
        sinuosity=np.sum(dist[(w+1):(w+win+1)])/ppd
        for i in range(w,w+win+1):
            sinuosities[i]=np.nanmax([sinuosities[i],sinuosity])
            
    return sinuosities
            
def sinuosities_max(ldata,win=20):
    x = ldata["Position X"].values
    y = ldata["Position Y"].values
    dx = ldata["Position X"].shift().values
    dy = ldata["Position Y"].shift().values
    ldata["sinuosity"]=sinuosity_max(x,y,dx,dy,win)
    return(ldata)            

def sinuosity_max_old(ldata,win=20):
    dx = ldata["Position X"].shift()
    dy = ldata["Position Y"].shift()
    ldata['dist'] = np.sqrt((ldata["Position X"]-dx)**2 + (ldata["Position Y"]-dy)**2)
    ldata["sinuosity"] = np.nan

    for w in range(0,(ldata.shape[0]-win)):
        ppd=np.sqrt((ldata["Position X"].values[w+win]-ldata["Position X"].values[w])**2 + 
                    (ldata["Position Y"].values[w+win]-ldata["Position Y"].values[w])**2)

        sinuosity=sum(ldata["dist"].values[(w+1):(w+win+1)])/ppd
        for i in range(w,w+win+1):
            ldata["sinuosity"].values[i]=np.nanmax([ldata["sinuosity"].values[i],sinuosity])
    
    return(ldata)


def sinuosities_track(ldata):
    dx = ldata["Position X"].shift()
    dy = ldata["Position Y"].shift()
    ldata['dist'] = np.sqrt((ldata["Position X"]-dx)**2 + (ldata["Position Y"]-dy)**2)
    
    ppd=np.sqrt((ldata["Position X"].values[len(dx)-1]-ldata["Position X"].values[0])**2 + 
                (ldata["Position Y"].values[len(dx)-1]-ldata["Position Y"].values[0])**2)
    
    return(sum(ldata["dist"].values[1:])/ppd)








def alpha_cmap(cmap):
        my_cmap = cmap(np.arange(cmap.N))
        # Set a square root alpha.
        x = np.linspace(0, 1, cmap.N)
        my_cmap[:,-1] = x ** (0.5)
        my_cmap = cols.ListedColormap(my_cmap)

        return my_cmap
    

def tracksplot(files_c,files_v,ldata_e,sc,map_img,palette=None):
    if (len(files_c)>1):
        rown=round((np.sqrt(len(files_c)))/2.)*2
        coln=len(files_c)/rown
    else:
        rown=coln=1
    plt.figure(figsize=(coln*4,rown*4))
    for i in range(0,len(files_c)):
        plt.subplot(rown,coln,i+1)
        curves=pd.read_table(files_c[i],header=None,sep=" ")
        vect=pd.read_table(files_v[i],header=None,sep=" ",skiprows=1)/sc/355

        gs=int(np.sqrt(vect.shape[0]))

        a=np.linspace(min(pd.concat(ldata_e)["Position X"]),max(pd.concat(ldata_e)["Position X"]),gs)/sc/355
        b=np.linspace(min(pd.concat(ldata_e)["Position Y"]),max(pd.concat(ldata_e)["Position Y"]),gs)/sc/355
        out = np.stack([each.ravel(order='C') for each in np.meshgrid(a, b)])

        if (len(files_c)>1):
            for cu in curves[0]:
                plt.plot(ldata_e[cu]["Position X"]/sc/355,ldata_e[cu][["Position Y"]]/sc/355,c=palette[i],linewidth=0.5)
            plt.gca().invert_yaxis()
            plt.quiver(out[0],out[1],vect[0],-vect[1],alpha=.7)
        else:
            U_grid=vect[0].values.reshape(gs,gs)
            V_grid=vect[1].values.reshape(gs,gs)
            speed = np.sqrt(U_grid**2 + V_grid**2)
            X,Y = np.meshgrid(a, b)
            plt.streamplot(X,Y,U_grid,V_grid,color=speed,cmap="autumn")
            plt.imshow(map_img, zorder=0)

    return(plt.gca())



@njit()
def cdist_numba(coords,out):
    for i in range(0,coords.shape[0]-1):
        out[i] = math.sqrt((coords[i,0] - coords[i+1,0])**2+(coords[i,1] - coords[i+1,1])**2)

def distances_accelerations(ldat):
    dst= np.zeros(ldat.values.shape[0]-1)
    cdist_numba(ldat.iloc[:,:2].values,dst)
    ldat["dst"]=np.append(np.nan,dst)
    ldat["acc"]=np.append(np.nan,np.diff(ldat["dst"]))
    return(ldat)
        
def distances_accelerations_old(ldat):
    dst=list(map(lambda x: np.sqrt((ldat.values[x,0]-ldat.values[x+1,0])**2+(ldat.values[x,1]-ldat.values[x+1,1])**2),
                        range(0,ldat.values.shape[0]-1)))
    ldat["dst"]=[np.nan]+dst
    ldat["acc"]=np.append(np.nan,np.diff(ldat["dst"]))
    return(ldat)
