import pandas as pd

# crear un dataframe usando el archivo final.csv 
df = pd.read_csv('final.csv')

# clasificar dataframe : wrt a weighted rating col en orden ascendente
df = df.sort_values('weighted_rating' , ascending = False)

# dataframe final
output = df[['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating' ]].head(20)
