import numpy as np
import pandas as pd 
import requests

#data
url = 'https://global.espn.com/nba/boxscore?gameId=401160929' 	# Box Score Data Website
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[2]			#select the table data of Lakers' box score data from the website
#df = df_list[1]		#select the table data of Mavs' box score data from the website
print(df)
df.to_csv('box_score_data.csv')