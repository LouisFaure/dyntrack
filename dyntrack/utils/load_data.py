import matplotlib.image as mpimg 
import pandas as pd

def load_data(csv_path,img_path,x_col,y_col,parent_col,time_col):
    tdata = pd.read_csv(csv_path)
    tdata = tdata[[x_col,y_col,parent_col,time_col]]
    tdata.columns = ["Position X", "Position Y", "Parent","Time"]
    img = mpimg.imread(img_path)
    
    return tdata, img