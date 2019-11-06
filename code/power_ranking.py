import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots(figsize =(8,8))	#more concise than fig=plt.figure()	ax=fig.add_subplot(111)
							#fig, ax = plt.subplots(2,2, sharex=True, sharey=True) when want more subplots 
fig.canvas.set_window_title('PowerRanking')
fig.suptitle('NBA Data Visualization', fontsize=12, fontweight='bold')
fig.figsize=(6,6)
df = pd.read_excel('../data/PowerRanking_1106.xlsx')
data = df.to_numpy()	#convert dataframe to array

shortname, ini, longname, conference, division, oeff, deff = data.T

for x, y, z in zip(oeff, deff, shortname):
	plt.text(x+0.15, y-0.25, z, fontsize=8)

plt.plot(oeff, deff, 'o', label='NBA Team')
plt.plot(np.full(30, np.mean(oeff)), np.linspace(deff.min()-1.5, deff.max()+1.5, 30), '--', label='OEFF Average')		#plot avaerage oeff line
plt.plot(np.linspace(oeff.min()-1.5, oeff.max()+1.5, 30), np.full(30, np.mean(deff)), '--', label='DEFF Average')
plt.gca().invert_yaxis() 	#reverse y axis starting from big to small
ax.set_xlabel(r'$\bf{OEFF}$'+' (Offensive Efficiency - Points scored per 100 possessions')		#make OEFF bold
#ax.xaxis.set_label_coords(1.05,-0.025)		#x axis label position
ax.set_xticks(np.arange(80,120,4))			#set axis range
ax.set_xlim(oeff.min()-1.5, oeff.max()+1.5)	#set axis label range

ax.set_ylabel(r'$\bf{DEFF}$'+' (Defensive Efficiency - Points allowed per 100 possessions')		#make OEFF bold
#ax.yaxis.set_label_coords(-0.05,1.02)		#y axis label position
ax.set_yticks(np.arange(80,120,4))
ax.set_ylim(deff.max()+1.5, deff.min()-1.5)
ax.legend(loc='lower left')

ax.set_title('2019-2020 NBA Regular Season Power Ranking --By Nov 6')
plt.show()
