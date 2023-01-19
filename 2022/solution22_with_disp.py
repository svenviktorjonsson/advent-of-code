from typing import Iterator

from aoclib import show_answers, get_puzzle_input, CArray
import cmath
import numpy as np
import re

def display(data):
    print("  ",*(" " if i<10 else i//10 for i in range(data.shape[1])))
    print("  ",*(i%10 for i in range(data.shape[1])))
    for r,d in enumerate(data):
        print(f"{r: >2}"," ".join(d))

def to_file(data):
    np.savetxt("trace_day_22.txt",data,delimiter=" ",fmt="%s")

def move(z,dz,dist,data,translations):
    for _ in range(dist):
        nz = z + dz
        ndz = dz
        if (nz,dz) in translations:
            nz, ndz = translations[(nz,dz)]
        if data[nz] == "#":
            break
        z,dz = nz,ndz
    return z,dz

def flat_trans(data):
    trans = {}
    top = np.argmax(data!=" ",axis=0)+np.arange(len(data[0]))*1j
    bottom = len(data)-1-np.argmax(data[::-1]!=" ",axis=0)+np.arange(len(data[0]))*1j
    left = np.argmax(data!=" ",axis=1)*1j+np.arange(len(data))
    right = (len(data[0])-1-np.argmax(data[:,::-1]!=" ",axis=1))*1j+np.arange(len(data))
    for t,b in zip(top[1:-1],bottom[1:-1]):
        trans[(t-1,-1+0j)] = b,-1+0j
        trans[(b+1,1+0j)] = t,1+0j
    for l,r in zip(left[1:-1],right[1:-1]):
        trans[(l-1j,-1j)] = r,-1j
        trans[(r+1j,1j)] = l,1j
    return trans

def cube_trans(data):
    atfoup = (-1,-1,-1),(0,1,0),(0,0,1)
    side = int(np.sqrt(np.sum(data!=" ")/6))
    z = np.argmax(data[1]!=" ")*1j
    dz = 1j
    corners = {}
    trans = {}
    for _ in range(14):
        at,forward,up = np.array(atfoup)
        zs = z+np.arange(side)*dz
        key = tuple(at),tuple(at+2*forward)
        if key in corners:
            zs0, dz0 = corners[key]
            for z0,z1 in zip(zs0[::-1],zs):
                trans[(z0,dz0*1j)] = z1-dz*1j,dz/1j
                trans[(z1,dz*1j)] = z0-dz0*1j,dz0/1j
        else:
            corners[key[::-1]] = zs, dz

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
    return trans

def solutions() -> Iterator[int]:
    data, cmds = get_puzzle_input(year=2022, day=22, example=False, as_lines=False).split("\n\n")
    cmds = [(int(d),dict(R=-1j,L=1j).get(r,1)) for d,r in re.findall("(\d+)(R|L)?",cmds)]
    data = data.split("\n")
    width = max(map(len,data))

    data = np.array([list(f"{line:<{width}}") for line in data])
    data = np.pad(data,1,mode="constant",constant_values=" ").view(CArray)

    for trans in flat_trans(data),cube_trans(data):
        z = 1+np.argmax(data[1]!=" ")*1j
        dz = 1j
        for step,rot in cmds:
            z, dz = move(z, dz, step, data, trans)
            dz *= rot
        face = int(1-2*cmath.phase(dz)/cmath.pi)%4
        yield int(1000*z.real+4*z.imag+face)

    



        

show_answers(solutions)
