# Read Text Files with Pandas using read_csv() 

# importing pandas 
import pandas as pd 

# read text file into pandas DataFrame 
df = pd.read_csv("330TF.txt", sep=",") 

# display DataFrame 
print(df) 
