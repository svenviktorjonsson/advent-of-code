from typing import Iterator

from aoclib import show_answers, get_puzzle_input, CArray
import cmath
import numpy as np
from itertools import product,combinations
from typing import Iterable
import sys
from collections import deque

def display(data):
    print("  "," ".join(map(str,list(range(10))*2)))
    for r,d in enumerate(data):
        print(f"{r: >2}"," ".join(d))

def to_file(data):
    np.savetxt("log.txt",data[1:-1,1:-1],delimiter=" ",fmt="%s")

def follow_commands(z,dz,commands,data,wormholes = {}):
    height,width = data.shape
    index = next((i for i,c in enumerate(commands) if c in "RLE"),len(commands))
    dist = int("".join(commands[:index]))
    rot = commands[index]
    commands = commands[index+1:]
    step = 0
    last_valid_z = z
    zs = []
    dzs = []
    while step<dist:
        zs.append(z)
        dzs.append(dz)
        nz = z+dz
        if nz in wormholes:
            nz,f,_ = wormholes[nz]
            dz*=f
        else:
            nz = int(nz.real)%height+(int(nz.imag)%width)*1j
        next_value = data[nz]
        if next_value == "#":
            break
        z = nz
        if next_value.strip():
            step += 1
            last_valid_z = nz
    if rot!="E":
        dz *= -1j if rot=="R" else 1j
    return last_valid_z,dz,commands,zs,dzs,rot


def solutions() -> Iterator[int]:
    with open("2022/input_day_22_all_nets.txt",'r') as file:
        data = file.read().strip().split("\n\n")
    for d in data:
        solve(d)


def solve(data):
    data = data.split("\n")
    width = max(map(len,data))
    data = np.array([list(w:=line)+[" "]*(width-len(w)) for line in data])
    
    atfoup = (-1,-1,-1),(0,1,0),(0,0,1)
    side = int(np.sqrt(np.sum(data!=" ")/6))
    data = np.pad(data,1,mode = "constant", constant_values = " ").view(CArray)
    disp_data=data.copy()
    z = next(i for i,c in enumerate(data[1]) if c==".")*1j
    dz = 1j
    corners = {}
    wormholes = {}
    indices = []
    imax = ord("A")
    for _ in range(14):
        at,forward,up = np.array(atfoup)
        zs = z+np.arange(side)*dz
        next_ = tuple(at+2*forward)
        if (key:=(tuple(at),next_)) in corners:
            zs0, dz0, inds0 = corners[key]
            inds = indices[-side:][::-1]
            indices = indices[:-side]
            wormholes.update({z0:(z1-dz*1j,-dz/dz0,f"{chr(i0)}->{chr(i1)}") for z0,z1,i0,i1 in zip(zs0[::-1],zs,inds0[::-1],inds)})
            wormholes.update({z1:(z0-dz0*1j,-dz0/dz,f"{chr(i0)}->{chr(i1)}") for z0,z1,i0,i1 in zip(zs0[::-1],zs,inds0[::-1],inds)})
            
        else:
            indices.extend(inds:=imax+np.arange(side))
            imax+=side
            corners[key[::-1]] = zs, dz, inds
            
        chrs = [chr(i) for i in inds]
        disp_data[zs]=chrs
        turn_right = data[z+(side-1j)*dz] == " "
        go_forward = data[z+side*dz] == " "
        at += 2*forward
        if turn_right:
            forward = np.cross(forward, up)
            z += (side-1j)*dz
            dz *= -1j
        elif go_forward:
            s = at@up
            forward,up = -s*up,s*forward
            z += side*dz
        else:
            up = np.cross(forward,up)
            forward = -forward
            z += (side-1)*dz
            dz *= 1j
        atfoup = at,forward,up

    # cmds = commands.strip()+"E"
    # z = 1+next(i for i,c in enumerate(data[1]) if c==".")*1j
    # dz = 1j
    # # display(disp_data)
    # # for k,v in wormholes.items():
    # #     print(k, *v)
    # disp_data[z] = "S"
    # while cmds:
    #     face = int(1-2*cmath.phase(dz)/cmath.pi)%4
    #     z, dz, cmds, zs,dzs,rot = follow_commands(z, dz, cmds, data, wormholes)
    #     for zi,dzi in zip(zs[1:],dzs[1:]):
    #         disp_data[zi] = ">v<^"[int(1-2*cmath.phase(np.array(dzi))/cmath.pi)%4]
    #     disp_data[z] = rot
    # to_file(disp_data)
    # yield int(1000*z.real+4*z.imag+face)
    
    # side = np.min(np.r_[np.sum(data!=" ",axis=1),np.sum(data!=" ",axis=0)])
    # data = np.pad(data,1,mode = "constant",constant_values = " ").view(CArray)
    # disp_data = data.copy().view(CArray)
    # z = np.argmax(data[1]!=" ")*1j
    # dz = 1j
    # connections = {}
    # trans = {}
    # # sides = [[]]
    # add = True
    # pop_more = False
    # index = 0
    # indices = []
    # for pos in range(14*side):
    #     if add:
    #         index = len(connections)
    #         indices.append((index,pop_more))
    #         connections[index] = (z,dz)
    #     else:
    #         index,pop_more = indices.pop(-1)
    #         z0, dz0 = connections[index]
    #         trans[z0] = z+1j*dz, dz/dz0
    #         trans[z] = z0+1j*dz0, dz0/dz
    #     disp_data[z] = chr(index+ord("A"))
    #     turn_right = data[z+(1-1j)*dz]==" "
    #     walk = data[z+dz]==" "
    #     if turn_right:
    #         z += (1-1j)*dz
    #         dz *= -1j
    #         if add:
    #             pop_more = False
    #         add = not pop_more
    #     elif walk:
    #         z += dz
    #         pop_more = True
    #     else:
    #         dz *= 1j
    #         add = False
    #     if not indices:
    #         add = True
    #     if len(trans)+(14*side-1-pos)*2<14*side:
    #         add = False
    display(disp_data)

solutions()
    
#     inputs = 
#     data,commands = get_puzzle_input(year=2022, day=22, example=True, as_lines=False).split("\n\n")
#     data = data.split("\n")
#     height = len(data)
#     width = max(map(len,data))
#     commands = commands.strip()+"E"
#     data = np.array([list(w:=line)+[" "]*(width-len(w)) for line in data])
#     z = next(i for i,c in enumerate(data[0]) if c==".")
#     dz = 1+0j
#     while commands:
#         z,dz,commands = follow_commands(z,dz,commands,data)
#     face = int(2*cmath.phase(dz)/cmath.pi)%4
#     yield int(1000*(z.imag+1)+4*(z.real+1)+face)

#     side = np.min(np.sum(data[1:-1]!=" ",axis=1))
#     data = np.pad(data,1,mode = "constant",constant_values = " ").view(ZArray)
#     show_data = data.copy().view(ZArray)

#     z = np.argmax(data[1]!=" ")
#     parity = 1
#     dz = parity+0j
#     trans = {0:[(z,dz)]}
#     zs = []
#     tf = 1+parity*1j
#     key = 0
#     inds = [key]
#     touse = 0
#     use = False
#     while not zs or z!=zs[0]:
#         ch = chr(key+ord("A"))
#         show_data[z] = ch
#         turn = data[z+tf*dz]==" "
#         walk = data[z+dz]==" "
#         zs.append(z)
#         if turn:
#             z += (1+parity*1j)*dz
#             dz *= parity*1j
#             if not use and touse<=side:
#                 touse = 0
#             touse += -1 if use else 1
#             print(chr(key+65),chr(65+inds[-1]) if inds else "none")
#             if touse<=0 or (not inds or key-inds[-1]<side * 3):
#                 use = False
#         elif walk:
#             z += dz
#             touse += -1 if use else 1
#         else: #at corner
#             dz *= -parity*1j
#             use = True
#         if use:
#             key = inds.pop(-1)
#         else:
#             key = max(trans.keys())+1
#             inds.append(key)
#         trans.setdefault(key,[]).append((z,dz))
#     display(show_data)
#     return

    
#     side = np.min(np.sum(data[1:-1]!=" ",axis=1))
#     z = np.argmax(data[1]!=" ")
#     dz = 1+0j
#     inds = list(range(side))
#     coords = list(z+np.arange(side)*dz)
#     trans = {i:[(z,dz)] for i,z in zip(inds,coords)}
#     i=0
#     use = 0
#     corner_passed = False
#     unique_corners = 1
#     while inds:
#         print(chr(ord("A")+list(trans.keys())[-1]),"use:",use,corner_passed)
#         i+=1
#         z = coords[-1]
#         turn_right = data[int((z+(1+1j)*dz).imag),int((z+(1+1j)*dz).real)]==" "
#         can_continue = data[int((z+dz).imag),int((z+dz).real)]==" "
#         if turn_right:
#             z = z+(1+1j)*dz
#             dz *= 1j
#             coords.extend(z+np.arange(side)*dz)
#             if use and corner_passed:
#                 for coord in coords[-side:]:
#                     trans.setdefault(inds.pop(-1),[]).append((coord,dz))
#                 use-=1
#             else:
#                 inds.extend(max(trans.keys())+1+np.arange(side))
#                 for coord,ind in zip(coords[-side:],inds[-side:]):
#                     trans.setdefault(ind,[]).append((coord,dz))
#         elif can_continue:
#             z = z+dz
#             coords.extend(z+np.arange(side)*dz)
#             if use and corner_passed:
#                 for coord in coords[-side:]:
#                     trans.setdefault(inds.pop(-1),[]).append((coord,dz))
#                 use-=1
#             else:
#                 inds.extend(max(trans.keys())+1+np.arange(side))
#                 for coord,ind in zip(coords[-side:],inds[-side:]):
#                     trans.setdefault(ind,[]).append((coord,dz))
#                 use+=1
#         else: #turn left
#             dz *= -1j
#             coords.extend(z+np.arange(side)*dz)
#             for coord in coords[-side:]:
#                 trans.setdefault(inds.pop(-1),[]).append((coord,dz))
#             corner_passed = True
#         if use==0 and corner_passed:
#             corner_passed = False
#         if i==8:
#             break
#     for ind, zdzs in trans.items():
#         for z,dz in zdzs:
#             data[int(z.imag),int(z.real)] = chr(ord("A")+ind)
#     # print(len(coords),len(inds))    
#     display(data)
#     yield 0
#     # padded_data = np.pad(data,1,mode = "constant",constant_values = " ")

#     # xvals = np.tile(np.arange(1,width+1),2)
#     # yvals = np.tile(np.arange(1,height+1),2)
    
#     # xbs = np.r_[np.argmax(data!=" ",axis=1),width-np.argmax(data[:,::-1]!=" ",axis=1)+1]
#     # xcoords = set(zip(yvals,xbs))

#     # ybs = np.r_[np.argmax(data!=" ",axis=0),height-np.argmax(data[::-1]!=" ",axis=0)+1]
#     # ycoords = set(zip(ybs,xvals))

#     # corners = set.intersection(xcoords,ycoords)
#     # init_border = set.union(xcoords,ycoords)
#     # border = init_border.copy()
#     # index = 0
#     # rem_sides_nbs = {}
#     # connections = {}
#     # for c in corners:
#     #     coords = [(c,(0,0))]
#     #     index = find_connections(index,coords,padded_data,connections,border,rem_sides_nbs)
    
#     # display(padded_data)

#     # rem_sides_nbs = {chr(ord("A")+k):v for k,v in rem_sides_nbs.items() if k in connections}
#     # for k,v in rem_sides_nbs.items():
#     #     print(k,v)
#     # yield 0
#     # print([str(chr(-index)) for index in rem_sides_nbs])
#     # new_rem = [rs for index,rs in rem_sides_nbs.items() if rs[0] in border]
#     # print(new_rem)
#     # for index,nbs in rem_sides_nbs.items():
#     #     padded_data[nbs[0]] = "?"
#     # coords = next(cs for index,cs in rem_sides_nbs.items() if all(c in border for c,_ in cs))
#     # print(coords)
#     # index = find_connections(index,coords,padded_data,connections,border,rem_sides_nbs)
#     # transformations = {}
#     # for index,cds in connections.items():
#     #     pass
#     # rem_coords,dydx = zip(*rem_sides_nbs)
#     # rem_nbs = border.intersection(set(rem_coords))
#     # c1 = rem_nbs.pop()

#     # c2 = next(c for c in rem_nbs if any(x==y for x,y in zip(c1,c)))
#     # print(c1,c2)


#     # ybs = np.array([np.argmax(d!=" ",axis=0) for d in (data,data[::-1])]).flat
    
#     # bleft,bup,bright,bdown = [np.argmax(d!=" ",axis=ax) for d,ax in zip((data,data,data[::-1],data[::-1]),(0,1,0,1))]
#     # display(padded_data)
#     # yield 0
#     # # 
#     # display(data)
#     # edge = set()
#     # z = next(i for i,c in enumerate(data[0]) if c==".")-1j
#     # dz = 1
#     # side = width//3
#     # while z not in edge:
#     #     edge.update([z+dz*n for n in range(side)])
#     #     nzin = z + dz*1j
#     #     if (nx:=int(nzin.real))==width or data[ny][nx]==" ":

#     #         dz*=1j
#     #     if (ny:=int(nzr.imag)) > height data[int(nzr.imag)][int(nzr.real)]==" "
#     #     nzl = z + dz*(1-1j)
        


        

# show_answers(solutions)
