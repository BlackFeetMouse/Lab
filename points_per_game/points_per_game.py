from bokeh.plotting import figure, output_file, show, reset_output, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20b		# color palette
from bokeh.palettes import Greys			# color palette
import pandas as pd
import requests
import numpy as np
import re

#data
url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html#per_game_stats::pts_per_g' # Player Status Points Per Game
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]		#select the first table data from the website

to_drop = ['PTS']
df=df[~df['PTS'].isin(to_drop)]		#delet header rows
df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')	#change datatype to number 
df_PTS = df.nlargest(20,'PTS')		#extract top twenty twos in terms of Colume TPS's value
df_PTS = df_PTS.iloc[::-1]
print(df_PTS)

#insert column for profile picture website
#df_PTS.insert(30, 'Profile', 'https://d2cwpp38twqe55.cloudfront.net/req/201910291/images/players/adamsst01.jpg')
Player_add = []
translationTable = str.maketrans("čćöášý", "ccoasy")
# edit profile website string
for x in range(len(df_PTS)):
	player_name_ori = re.sub("[^a-z ]", "", df_PTS.iloc[x]['Player'].lower().translate(translationTable))	#make letters lowercase and translare letters from other language to english and delet all non-alphabet letters
	player_name_list=player_name_ori.split(" ")
	if(player_name_ori=='anthony davis' or player_name_ori=='kemba walker' or player_name_ori=='lou williams'):		# exception on anthony davis since his profile picture is ..davisan02.html
		player_name_finial = "https://d2cwpp38twqe55.cloudfront.net/req/201910291/images/players/" + player_name_list[1][:5]+player_name_list[0][:2] +"02.jpg"
		Player_add.insert(x,player_name_finial)
	else:
		player_name_finial = "https://d2cwpp38twqe55.cloudfront.net/req/201910291/images/players/" + player_name_list[1][:5]+player_name_list[0][:2] +"01.jpg"
		Player_add.insert(x,player_name_finial)

	#print(df_PTS['Profile'][0])
#################################################### need change dataframe data 11/15 6pm
#df_PTS.insert(30, 'Profile', Player_add)

df_PTS['Profile']=Player_add		# insert new column for Profile picture address
print(df_PTS['Profile'])

df_PTS['Color'] = Category20b[len(df_PTS)][::-1]		# insert one colum for bar color 
#df_PTS['Color'] = bokeh.palettes.grey(len(df_PTS))		# insert one colum for bar color 
print(df_PTS['Color'])
#Create ColumDataSource from dataframe. instead of using pts = df_PTS['PTS']
source_pts = ColumnDataSource(df_PTS)


output_file('PointsPerGame2019-2020.html')
playerlist = source_pts.data['Player'].tolist()
# Add a plot
p = figure(
	y_range = playerlist,  # pass player list to y_range 
	plot_width = 1000,
	plot_height = 800,
	title = 'NBA Data Visualization',
	x_axis_label = 'Points Per Game',
	y_axis_label = 'Top 20 Players in PTS',
	tools = 'pan, box_select, zoom_in, zoom_out, save, reset',
	match_aspect=True,
	min_border_top = 120,		# leave padding to the figure
	min_border_bottom = 0,
	min_border_left = 100,
	min_border_right = 60
	)

p.hbar (
	y = 'Player',
	right = 'PTS',
	left = 0,
	height = 0.6,
	source = source_pts,
	fill_color = 'Color',
    fill_alpha=0.5
)

# Add interaction
hover = HoverTool()
hover.tooltips = """
	<div>
		<h3>@Player</h3>
		<div><strong>Points Per Game: </strong>@PTS{0.2f}</div>	
		<div><strong>Team: </strong>@Tm</div>
		<div><strong>Position: </strong>@Pos</div>
		<div><strong>Age: </strong>@Age</div>
		<div><img src="@Profile" alt="" width="80" /></div>
	</div>
"""
p.add_tools(hover)

# Show plot
show(p)
	
#df_data = pd.DataFrame(df_PTS.to_numpy())		#change numpy array to dataframe
#df_data.to_excel('pandas_playerdat.xlsx', index=False)		#save dataframe data to excel
