#! /usr/bin/python

import json

class Node:
    def __init__(self, id, left, right, coeff, j0, j1, j2, j3):
        self.id=id
        self.left=left
        self.right=right
        self.coeff=coeff
        self.j0=j0
        self.j1=j1
        self.j2=j2
        self.j3=j3
        
length=0

def newnode(left, right, coeff, j0, j1, j2, j3):
    global length
    length=length+1
    node=Node(length, left, right, coeff, j0, j1, j2, j3)
    return(node)

def newnodefromarray(node):
    result=newnode(None, None, node[3], node[4], node[5], node[6], node[7])
    return(result)
    
def reconstruct(nodes):
    global length
    length=0
    nodearray=[]
    for i in range(len(nodes)):
        nodearray.append(newnodefromarray(nodes[i]))
    for i in range(len(nodes)):
        nodearray[i].left=nodearray[nodes[i][1]-1] if nodes[i][1] else None
        nodearray[i].right=nodearray[nodes[i][2]-1] if nodes[i][2] else None
    return(nodearray[len(nodes)-1])

def readjson(filename):
    with open(filename, "r") as input:
        return(json.load(input))

