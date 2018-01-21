import pygame
import sys
from math import pi,sqrt


class cell:
    def __init__(self,x,y,r,state='open'):
        self.center=(x,y)
        self.state=state
        self.r=r
        #self.sellected=False
        list_points=[]
        r2=sqrt(3)*r/2
        self.r2=r2
        list_points.append([x+r,y])
        list_points.append([x+r/2,y+r2])
        list_points.append([x-r/2,y+r2])
        list_points.append([x-r,y])
        list_points.append([x-r/2,y-r2])
        list_points.append([x+r/2,y-r2])
        self.list_points=list_points
        re=pygame.Rect(list_points[4][0],list_points[4][1],abs(list_points[1][0]-list_points[2][0]),abs(list_points[2][1]-list_points[4][1]))
        re2=pygame.Rect(list_points[5][0],list_points[5][1]+r2/2,r/4,r2)
        re3=pygame.Rect(list_points[4][0]-r/4,list_points[4][1]+r2/2,r/4,r2)
        self.rect_list=[re,re2,re3]

def map_generate():
    maps=[]
    adj=[]
    buf_cell=cell(50,50,50)
    for i in range(0,8):
        maps.append(list())
        for j in range(0,4):
            if i%2==0:
                maps[i].append(cell(50+j*buf_cell.r*3,50+i*buf_cell.r2,50))
            else:
                maps[i].append(cell(50+(buf_cell.r+buf_cell.r/2)+j*buf_cell.r*3,50+i*buf_cell.r2,50))
    
    for i in range(0,8):
        adj.append(list())
        for j in range(0,4):
            adj[i].append(list())
            if i+1 in range(0,8):
                adj[i][j].append([i+1,j])
                if i%2==0:
                    if j-1 in range(0,4):
                        adj[i][j].append([i+1,j-1])
                else:
                    if j+1 in range(0,4):
                        adj[i][j].append([i+1,j+1])
            if i-1 in range(0,8):
                adj[i][j].append([i-1,j])
                if i%2==0:
                    if j-1 in range(0,4):
                        adj[i][j].append([i-1,j-1])
                else:
                    if j+1 in range(0,4):
                        adj[i][j].append([i-1,j+1])
            if j+1 in range(0,4):
                adj[i][j].append([i,j+1])
            if j-1 in range(0,4):
                adj[i][j].append([i,j-1])
    return maps,adj


def hexagon(x,y,r):
    list_points=[]
    r2=sqrt(3)*r/2
    list_points.append([x+r,y])
    list_points.append([x+r/2,y+r2])
    list_points.append([x-r/2,y+r2])
    list_points.append([x-r,y])
    list_points.append([x-r/2,y-r2])
    list_points.append([x+r/2,y-r2])
    return list_points



pygame.init()
update_list=[]
screen = pygame.display.set_mode((1024, 748))
#background = pygame.image.load('1.png').convert()
hexg=hexagon(100,100,50)
r=50
r2=sqrt(3)*r/2        
re=pygame.Rect(hexg[4][0],hexg[4][1],abs(hexg[1][0]-hexg[2][0]),abs(hexg[2][1]-hexg[4][1]))
re2=pygame.Rect(hexg[5][0],hexg[5][1]+r2/2,r/4,r2)
re3=pygame.Rect(hexg[4][0],hexg[4][1]+r2/2,-r/4,r2)
selected_cell=[-1,-1]
hower_cell=[-1,-1]
cell_sellected=False
print(hexg)
print(re.topleft, re.bottomleft, re.topright, re.bottomright)
screen.fill(pygame.Color(255,255,255,255))
#screen.blit(background, (0, 0))
maps,adj = map_generate()
for i in maps:
    for j in i:
        pygame.draw.polygon(screen,pygame.Color(0,0,0,255),j.list_points,1)
        #for rec in j.rect_list:
        #    pygame.draw.rect(screen,pygame.Color(255,0,0,255),rec,1)
#pygame.draw.rect(screen,pygame.Color(255,0,0,255),re,2)
#pygame.draw.rect(screen,pygame.Color(255,0,0,255),re2,2)
#pygame.draw.rect(screen,pygame.Color(255,0,0,255),re3,2)

update_list.append(screen.get_rect())
while 1:
    
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()
        if event.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION):
            for i in range(0,len(maps)):
                for j in range(0,len(maps[i])):
                    for rec in maps[i][j].rect_list:
                        if rec.collidepoint(pygame.mouse.get_pos()):
                            if event.type != pygame.MOUSEBUTTONDOWN and pygame.MOUSEMOTION:
                                if hower_cell!=[i,j]:
                                    if [i,j] !=selected_cell:
                                        pygame.draw.polygon(screen,pygame.Color(255,255,255,255),maps[i][j].list_points,0)
                                        pygame.draw.polygon(screen,pygame.Color(0,255,255,255),maps[i][j].list_points,0)
                                    if selected_cell !=hower_cell:
                                        pygame.draw.polygon(screen,pygame.Color(255,255,255,255),maps[hower_cell[0]][hower_cell[1]].list_points,0)
                                        pygame.draw.polygon(screen,pygame.Color(0,0,0,255),maps[hower_cell[0]][hower_cell[1]].list_points,1)
                                    hower_cell=[i,j]
                                    cell_sellected=True
                                    update_list.append(screen.get_rect())
                                    break
                            
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if selected_cell!=[i,j]:
                                    pygame.draw.polygon(screen,pygame.Color(0,0,255,255),maps[i][j].list_points,0)
                                    pygame.draw.polygon(screen,pygame.Color(255,255,255,255),maps[selected_cell[0]][selected_cell[1]].list_points,0)
                                    pygame.draw.polygon(screen,pygame.Color(0,0,0,255),maps[selected_cell[0]][selected_cell[1]].list_points,1)
                                    selected_cell=[i,j]
                                    cell_sellected=True
                                    update_list.append(screen.get_rect())
                                    break
                            
                    if cell_sellected==True:
                        break
                if cell_sellected==True:
                    cell_sellected=False
                    break

    
    if update_list != []:
        for rect in update_list:
            pygame.display.update(rect)
        update_list=[]