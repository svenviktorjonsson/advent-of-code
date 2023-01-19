from typing import Iterator

from aoclib import show_answers, get_puzzle_input, CArray
import cmath
import numpy as np
from itertools import product,combinations
from typing import Iterable
import sys

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
    data,commands = get_puzzle_input(year=2022, day=22, example=False, as_lines=False).split("\n\n")
    data = data.split("\n")
    width = max(map(len,data))
    cmds = commands.strip()+"E"
    data = np.array([list(w:=line)+[" "]*(width-len(w)) for line in data]).view(CArray)
    z = next(i for i,c in enumerate(data[0]) if c==".")*1j
    dz = 1j
    while cmds:
        z, dz, cmds, zs,dzs,rot = follow_commands(z, dz, cmds, data)

    face = int(1-2*cmath.phase(dz)/cmath.pi)%4
    yield int(1000*(z.real+1)+4*(z.imag+1)+face)

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
            
        # chrs = [chr(i) for i in inds]
        # disp_data[zs]=chrs
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

    cmds = commands.strip()+"E"
    z = 1+next(i for i,c in enumerate(data[1]) if c==".")*1j
    dz = 1j
    # display(disp_data)
    # for k,v in wormholes.items():
    #     print(k, *v)
    disp_data[z] = "S"
    while cmds:
        face = int(1-2*cmath.phase(dz)/cmath.pi)%4
        z, dz, cmds, zs,dzs,rot = follow_commands(z, dz, cmds, data, wormholes)
        for zi,dzi in zip(zs[1:],dzs[1:]):
            disp_data[zi] = ">v<^"[int(1-2*cmath.phase(np.array(dzi))/cmath.pi)%4]
        disp_data[z] = rot
    to_file(disp_data)
    yield int(1000*z.real+4*z.imag+face)


        

show_answers(solutions)
