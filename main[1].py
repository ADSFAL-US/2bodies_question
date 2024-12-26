import pygame_widgets
import pygame as pg
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import random as r
import math
import numpy as np
pg.init()
fps = 120
fpsClock = pg.time.Clock()
moon_rad = 150
erth_rad = 800
omass = 0.1
gmass = 100000
mmass = 25000
Ocolors = [[0,0,200],[0,200,0],[200,0,0]]
select = []
quality = 0
count = quality
opt = 50
time = 1
cords = [500,500]
times = [1,2,3,50,100,500,10000,100000]
speed = [0.185,-0.0]


width, height = 1900, 1080
display = pg.display.set_mode((width, height), pg.FULLSCREEN)
stars = []

slider = Slider(display, 100, 100, 800, 40, min=-0.001, max=0.001, step=0.000001, inital = 0)
slider1 = Slider(display, 100, 250, 800, 40, min=-0.001, max=0.001, step=0.000001, inital = 0)
time_s = Slider(display, 100, 400, 800, 40, min = 0, max = 5, step = 1, inital = 0)
time_s.setValue(0)
spbox = TextBox(display, 2250, 50, 300, 100, fontSize = 35)


def m(n):
	if n<0:
		n=-n
	return n

def gforce(p1,p2,p3):
	global Ocolors
	global select
	# Calculate the gravitational force exerted on p1 by p2.
	G = 0.001 # Change to 6.67e-11 to use real-world values.
	# Calculate distance vector between p1 and p2.
	r_vec = p1-p3
	r1_vec = p2-p3
	# Calculate magnitude of distance vector.
	r_mag = np.linalg.norm(r_vec)
	r1_mag = np.linalg.norm(r1_vec)
    
	if r_mag/4<r1_mag:
		r_hat = r_vec/r_mag
		select.append(Ocolors[0])
	else:
		r_hat = r1_vec/r1_mag
		r_mag = r1_mag
		select.append(Ocolors[1])
    # Calcualte unit vector of distance vector.
    
	# Calculate force magnitude.
	force_mag = G*omass*gmass/r_mag**2
    
	# Calculate force vector.
	force_vec = -force_mag*r_hat
    
    
	return force_vec
   

def collide_circle(point, pos, radius):
	
	dist = np.linalg.norm(point-pos)
	if dist < radius:
		return True
	else:
		return False
	
for c in range(0,int(width/10)):
	stars.append([r.randint(0,width), r.randint(0,height), r.randint(2,8), r.randint(240,255),r.randint(240,255)])
cordsM1 = cords
while True:
	widg_ev = pg.event.get()
	for event in pg.event.get():
		
		if event.type == pg.QUIT:
			exit(0)
			
	display.fill((10,10,10))
	
	for star in stars:
		pg.draw.circle(display, (star[3], 250, star[4]),[star[0], star[1]], star[2], 0)
	
	earth = pg.draw.circle(display, (0, 80, 255),[500,800],250, 0)
	moon = pg.draw.circle(display, (180, 180, 180),[1500,800],60, 0)
	
	pg.draw.circle(display, (220, 180, 180),cords,20, 0)
	
	
	reentry = 0
	
	x = slider.getValue()
	y = slider1.getValue()
	time = time_s.getValue()
	
	slider.setValue(0)
	slider1.setValue(0)

	count += 1
	if time <= 4:
		opt = 50
	if time > 3:
		quality = 60
		opt = 50
	else:
		quality = 0
		
	time = times[time]
	
	spbox.setText(str(round(speed[0], 2))+" | "+str(round(speed[1], 2))+"|"+str(time)+"x")
	
	if count > quality:
		count = 0
		speed1=speed
		cords1=cords
		orbit = []
		select = []
		disto = []
		for orb in range(1500):
			opt1 = opt
			gvec1 = gforce(np.array([500,800], dtype = float), np.array([1500,800], dtype = float), np.array(cords1, dtype = float))
			speed1 = [speed1[0]-gvec1[0]*opt1,speed1[1]-gvec1[1]*opt1]
			cords1 = [cords1[0] + speed1[0]*opt1,cords1[1] + speed1[1]*opt1]
			orbit.append(cords1)
			
		
	
	for obt in range(len(orbit)):
		#pg.draw.circle(display, select[obt],max(orbit),15, 3)
		#pg.draw.circle(display, select[obt],min(orbit),15, 3)
		try:
				pg.draw.line(display, select[obt], orbit[obt], orbit[obt+1])
		except:
			if orbit[obt] not in orbit:
				pg.draw.circle(display, select[obt],orbit[obt],5, 0)
		
		if collide_circle(np.array(orbit[obt]),np.array([1500,800]),60) == True:
			break
		if collide_circle(np.array(orbit[obt]),np.array(cords),20) == True and obt > 25+opt:
			break
		if collide_circle(np.array(orbit[obt]),np.array([500,800]),250) == True:
			break
		if (orbit[obt][0] > width+500 or orbit[obt][1] > height+500) or (orbit[obt][0] < 0-500 or orbit[obt][1] < 0-500):
			break
		if reentry > 10:
			break
		
		try:
			
			if select[obt] != select[obt+1]:
				pg.draw.circle(display, select[obt],orbit[obt],25, 2)
				reentry += 1
		except:
			pass
		
	
	gvec = gforce(np.array([500,800], dtype = float), np.array([1500,800], dtype = float), np.array(cords, dtype = float))
	#mgvec = gforce(np.array([1500,800], dtype = float), np.array(cords, dtype = float))
	if time <= 3:
		speed = [speed[0]-(gvec[0]+x)*time,speed[1]-(gvec[1]+y)*time]
	else:
		speed = [speed[0]-(gvec[0])*time,speed[1]-(gvec[1])*time]
	cords = [cords[0] + speed[0]*time,cords[1] + speed[1]*time]
	
	pygame_widgets.update(widg_ev)
	pg.display.flip()
	fpsClock.tick(fps)