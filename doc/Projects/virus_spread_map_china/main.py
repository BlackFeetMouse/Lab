# -*- coding: utf-8 -*-
from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Range1d, HoverTool, CustomJS, LinearColorMapper,LogColorMapper,ColorBar, Label
from bokeh.layouts import widgetbox,column,row, gridplot, layout
from bokeh.palettes import brewer
from bokeh.models.widgets import TextInput, Button, RadioButtonGroup, Select, Slider, DataTable, DateFormatter, TableColumn, Paragraph
import json
import pandas as pd
import numpy as np
from china_province import China_Province
from chinamap import ChinaMap
from datetime import date
from random import randint
import requests


legends = []
colors = []

for x in range(0,35):
    colors.append("lightblue")

china_province = China_Province()
provinceArray = china_province.provinceArray
provinceArray2Hebei = china_province.provinceArray2Hebei
chinamap = ChinaMap()
xs, ys = chinamap.allProvinces()

'''
Get Virus Status Data from online API
'''
re_all = requests.get('https://lab.isaaclin.cn/nCoV/api/area?latest=1')
re_all_dict = re_all.json()     
df_all = pd.DataFrame(data=re_all_dict['results'])  # change virus data to dataframe
df_china = df_all[df_all['country']=='中国'][['provinceShortName','confirmedCount', 'suspectedCount', 'curedCount', 'deadCount']]  #virus data of China only (33 parts)
#df_china.reindex(china_province.provinceArray)     #reorder the dataframe to be same as geojson data's order

#df_china['index'] = pd.Series(np.arange(len(df_china.index)), index=df_china.index)
print(df_china)
'''
        mapdata_dict = dict(
            x = xs,
            y = ys,
            provinces = china_province.provinceArray2Hebei,
            colors = colors,
            #number = [1,2]
        )
        '''
df_map = pd.DataFrame(list(zip(xs,ys,china_province.provinceArray2Hebei,colors)), columns=['x','y','provinces','colors'])
df_map = df_map.merge(df_china, left_on='provinces', right_on = 'provinceShortName')
print(df_map)
source = ColumnDataSource(df_map)
#print(type(source.data))
#print(df_china)
#print(source.data)
'''
hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">@provinces</span>
                <span style="font-size: 17px; font-weight: bold;">@confirmedCount</span>
            </div>
        </div>
        """
    )
'''
# Define color palettes
palette = brewer['Reds'][8]     # Used Bokeh palettes through brewer dictionary ['Reds'] palette
palette = palette[::-1] # reverse order of colors so higher values have darker colors
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LogColorMapper(palette = palette, low = 0, high = 2500)
# Define custom tick labels for color bar.
tick_labels = {'0':'0', '10':'10','200':'200', '1000':'1000', '2000':'2000+'}
# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal',
                     major_label_overrides = tick_labels)


p = figure(toolbar_location="below",
           toolbar_sticky=False,tools = ["pan","wheel_zoom","box_zoom","reset","save"])
p.toolbar.logo = None
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.y_range = Range1d(10, 65)
p.x_range = Range1d(70, 140)
p.patches('x', 'y',color = "colors", source=source, fill_alpha=1, line_width=2,line_color = "gray", fill_color = {'field' :'confirmedCount','transform' : color_mapper},)
# Create hover tool
p.add_tools(HoverTool(tooltips = [('Province','@provinces'),
                               ('Confirmed', '@confirmedCount')]))

p.add_layout(color_bar, 'below')

label1 = Label(x=74, y=23, text="China", text_font_size='15pt', text_color='red')
label2 = Label(x=74, y=20, text="Confirmed:"+str(df_china.sum()['confirmedCount']), text_font_size='15pt', text_color='red')
label3 = Label(x=74, y=17, text="Cured:"+str(df_china.sum()['curedCount']), text_font_size='15pt', text_color='red')
label4 = Label(x=74, y=14, text="Dead:"+str(df_china.sum()['deadCount']), text_font_size='15pt', text_color='red')
p.add_layout(label1)
p.add_layout(label2)
p.add_layout(label3)
p.add_layout(label4)


output_file("chinamap.html", title = "China Map")
show(p)











