#!/usr/bin/env python
# coding: utf-8

# In[232]:


import pandas as pd
import numpy as np

class sys:
    argv = ["topsis.py", "data.csv", "1,1,1,1", "+,+,-,+", "result.csv"]
def main():
    
    if len(sys.argv) < 5:
        print("System arguments error")
        return
    
    w = sys.argv[2]
    imp = sys.argv[3]
    try:
        w = w.split(",")
        imp = imp.split(",")
    except:
        print("Weight or Impact not comma seperated!")
        return
    w = [float(i) for i in w]
    for i in imp:
        if not (i == "-" or i == "+"):
            print("Wrong Impact values")
            return 
    
#     file not found error
    try:
        tp = pd.read_csv("D:\\College\\Data Science\\Input files for Assignment06\\" + sys.argv[1])
    except:
        print("file not found")
        return
    tp = tp.set_index("Model")
    
#     checking for string values
    for i in range(len(tp)):
        for j in range(len(tp.columns)):
            if isinstance(tp.iloc[i, j], str):
                print("Data contains string value")
                return
            
#     checking length of columns
    if len(tp.columns) < 3:
        print("Less than 3 columns inputted")
        return
    
    if len(w) != len(imp) or len(imp) != len(tp.columns):
        print("Lengths of columns, weights and impact do not match")
        return 
    
    # squaring the values
    df = tp**2
    # summing the squares
    df = df.sum(axis = 0)
    # taking root of sum squares
    df = np.sqrt(df)
    # dividing each value by root
    tp = tp/df
    # multiplying with weight
    tp = tp*w
    vp = [0] * 4
    vn = [0] * 4
    for i in range(len(imp)):
        if imp[i] == "+":
            vp[i] = tp.iloc[:,i].max()
            vn[i] = tp.iloc[:,i].min()
        else:
            vp[i] = tp.iloc[:,i].min()
            vn[i] = tp.iloc[:,i].max()

    tp["sp"] = 0
    tp["sn"] = 0
    for i in range(5):
        for j in range(4):
            tp.iloc[i, 4] += (tp.iloc[i, j] - vp[j]) ** 2
            tp.iloc[i, 5] += (tp.iloc[i, j] - vn[j]) ** 2
        tp.iloc[i, 4] = np.sqrt(tp.iloc[i, 4])
        tp.iloc[i, 5] = np.sqrt(tp.iloc[i, 5])


    tp["Topsis score"] = 0
    for i in range(5):
        tp.iloc[i, 6] = tp.iloc[i, 5]/(tp.iloc[i, 4] + tp.iloc[i, 5])
    tp = tp.sort_values(["Topsis score"], ascending = False)
    tp["rank"] = 0
    for i in range(1, 6):
        tp.iloc[i - 1, 7] = i
    tp = tp.reset_index()
    tp = tp.sort_values(["Model"])
    tp = tp.drop(["sp", "sn"], axis = 1)
    tp.to_csv("D:\\College\\Data Science\\Result_assignment-6\\" + sys.argv[4])
if __name__ == "__main__":
    main()





