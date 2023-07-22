import pygame
import numpy as np
from pygame.locals import * 
from math import sqrt, cos, sin, pi, e

def length(q):
	return sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)

def normalize(q):
	l = length(q)
	return [q[0]/l, q[1]/l, q[2]/l, q[3]/l]

def qMul(q1,q2):
	a,b,c,d = q1[0], q1[1], q1[2], q1[3]
	w,x,y,z = q2[0], q2[1], q2[2], q2[3]

	return [a*w - b*x - c*y - d*z,
		a*x + b*w + c*z - d*y,
		a*y - b*z + c*w + d*x,
		a*z + b*y - c*x + d*w]

def project2d(p):
	distance = 2
	z = 1 / (distance - p[3])
	projectionMat = [[z, 0, 0],
					 [0, z, 0]]

	return [p[1]*z, p[2]*z]

class QCube:
	def __init__(self):
		self.trans = [0,0,0]
		self.scale = 100
		self.dir = True
		self.verts = [[0,-1,-1, 1],[0,1,-1, 1],[0,1,1, 1],[0,-1,1, 1],
					  [0,-1,-1,-1],[0,1,-1,-1],[0,1,1,-1],[0,-1,1,-1]]
		self.edges = [[0,1],[1,2],[2,3],[3,0],
					  [4,5],[5,6],[6,7],[7,4],
					  [0,4],[1,5],[2,6],[3,7]]

	def prep_for_show(self,e):
		a = project2d(self.verts[e[0]])
		b = project2d(self.verts[e[1]])
		a = [a[0]*self.scale + W//2, a[1]*self.scale + H//2]
		b = [b[0]*self.scale + W//2, b[1]*self.scale + H//2]
		return a, b

	def _scale(self,v):
		self.scale = self.scale * v[0] 
		self.scale = self.scale * v[1] 
		self.scale = self.scale * v[2] 

	def _translate(self,v):
		self.trans[0] = self.trans[0] + v[0] 
		self.trans[1] = self.trans[1] + v[1] 
		self.trans[2] = self.trans[2] + v[2] 

	def _show(self,screen):
		color = (255,255,255)
		for e in self.edges:
			pA, pB = self.prep_for_show(e)
			pygame.draw.aaline(screen, color, pA, pB)

	def _rotate(self,theta,axis=4):
		#{0:x, 1:y, 2:z, 3:xy, 4:xz, 5:yz, 6:xyz}
		angle = pi * theta/360
		axes = {0: [cos(angle),-sin(angle),0,0],
			1: [cos(angle),0,-sin(angle),0],
			2: [cos(angle),0,0,-sin(angle)],
			3: [cos(angle),-sin(angle),-sin(angle),0],
			4: [cos(angle),-sin(angle),0,-sin(angle)],
			5: [cos(angle),0,-sin(angle),-sin(angle)],
			6: [cos(angle),-sin(angle),-sin(angle),-sin(angle)]}

		try:
			q = axes[axis]

		except KeyError:
			print("invalid selection for axis. Value must be in 0 to 6.")
			exit()

		for i in range(len(self.verts)):
			qConj = [q[0], -q[1], -q[2], -q[3]]
			self.verts[i] = normalize(
				qMul(normalize(qMul(q, normalize(self.verts[i]))), qConj))

#MAIN

W,H = 300,300
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
running = True

cube = QCube()
axis = None

while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	screen.fill((0,0,0))
	cube._rotate(1, axis=0)
	cube._show(screen)
	pygame.display.flip()
	clock.tick(60)

pygame.quit()
exit()
