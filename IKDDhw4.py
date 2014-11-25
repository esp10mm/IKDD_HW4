#!/usr/bin/python
#coding:utf-8

import sys
import copy
from os import listdir
from os.path import isfile, join

class Node:
    def __init__(self,url):
        self.url = url
        self.dst = []
        self.prob = 0
        self.match = False

def makeNode(url):
    node = Node(url)
    return node

class pageRank:
    def __init__(self,nodes):
        self.nodes = copy.deepcopy(nodes)
        self.backNodes = copy.deepcopy(nodes)
        self.matrix = []

    def listNodes(self):
        for n in self.nodes:
            print n.url
            print n.dst
            print n.prob
            print

    def listBackNodes(self):
        for n in self.backNodes:
            print n.url
            print n.dst
            print n.prob
            print

    def dropEnd(self):
        for n in self.backNodes:
            if len(n.dst) == 0:
                self.backNodes.remove(n)
                for j in self.backNodes:
                    if n.url in j.dst:
                        j.dst.remove(n.url)
                self.dropEnd()
                break

    def nodeIndex(self,url):
        for n in self.backNodes:
            if n.url == url:
                return self.backNodes.index(n)

    def matrixCreate(self):
        for n in self.backNodes:
            p = [0 for y in range(len(self.backNodes))]
            n.prob = float(1)/len(self.backNodes)
            for d in n.dst:
                p[self.nodeIndex(d)] = float(1)/len(n.dst)
            self.matrix.append(p)

    def matrixRun(self,count):
        for c in range(count):
            p = [0 for y in range(len(self.backNodes))]
            for j in range(len(self.matrix)):
                for i in range(len(self.matrix[j])):
                    p[i] += self.backNodes[j].prob * self.matrix[j][i]
                    # print self.matrix[j][i]
            for i in range(len(self.backNodes)):
                self.backNodes[i].prob = p[i]

    def matrixPrint(self):
        for m in self.matrix:
            print m

    def dropRestore(self):
        dirty = False
        for n in self.nodes:
            if(self.nodeIndex(n.url) == None):
                for n2 in self.nodes:
                    if n.url in n2.dst:
                        if self.nodeIndex(n2.url) is not None:
                            dirty = True
                            self.backNodes[self.nodeIndex(n2.url)].dst.append(n.url)
                            if self.nodeIndex(n.url) is None:
                                self.backNodes.append(makeNode(n.url))
                            added = self.backNodes[self.nodeIndex(n.url)]
                            exist = self.backNodes[self.nodeIndex(n2.url)]
                            added.match = n.match
                            added.prob += exist.prob/len(exist.dst)
        if dirty:
            self.dropRestore()

    def sortNodes(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.nodes[i].prob > self.nodes[j].prob:
                    tmp = self.nodes[i]
                    self.nodes[i] = self.nodes[j]
                    self.nodes[j] = tmp

    def run(self):
        self.dropEnd()
        self.matrixCreate()
        self.matrixRun(1000)
        self.dropRestore()
        self.nodes = self.backNodes
        self.sortNodes()


dataPath = './data/'
onlyfiles = [ f for f in listdir(dataPath) if isfile(join(dataPath,f)) ]

nodes = [Node(f) for f in onlyfiles]

for fileName in onlyfiles:
    file = open(dataPath+fileName,'r')
    while True:
        line = file.readline()
        if not line: break
        if 'http://' in line:
            words = line.split()
            for word in words:
                if 'http://' in word:
                    for node in nodes:
                        if node.url == fileName:
                            node.dst.append(word[7:])
                            break

        if sys.argv[1] in line:
            # print fileName
            for node in nodes:
                if node.url == fileName:
                    node.match = True

    file.close()

pageRank = pageRank(nodes)
pageRank.run()
print 'Rank\t\tFilename'
count = 0
for n in pageRank.nodes:
    # print n.url
    if n.match:
        count += 1
        print('%d\t\t%s'%(count,n.url))
