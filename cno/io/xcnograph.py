# -*- python -*-
#
#  This file is part of the cinapps.tcell package
#
#  Copyright (c) 2012-2013 - EMBL-EBI
#
#  File author(s): Thomas Cokelaer (cokelaer@ebi.ac.uk)
#
#  Distributed under the GLPv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: www.cellnopt.org
#
##############################################################################
from __future__ import print_function
import os
import copy
import tempfile
import itertools
import subprocess
import shutil
import json

import pylab
import networkx as nx
import numpy as np
import easydev
from easydev import Logging

# cellnopt modules
from cno.io.sif import SIF
from cno.io.midas import XMIDAS
from cno.io.reactions import Reaction
from cno.misc import CNOError
from colormap import Colormap
from cno.io.cnograph import CNOGraph

__all__ = ["XCNOGraph"]



class XCNOGraph(CNOGraph):
    """extra plotting and statistical tools"""
    def __init__(self, model=None, midas=None, verbose=True):
        super(XCNOGraph, self).__init__(model, midas, verbose=verbose)

    def hcluster(self):
        """

        .. plot::
            :include-source:
            :width: 50%

            from cno import CNOGraph
            c = CNOGraph(cnodata("PKN-ToyPB.sif"), cnodata("MD-ToyPB.csv"))
            c.hcluster()

        .. warning:: experimental
        """
        from scipy.cluster import hierarchy
        from scipy.spatial import distance
        path_length=nx.all_pairs_shortest_path_length(self.to_undirected())
        n = len(self.nodes())
        distances=np.zeros((n,n))
        nodes = self.nodes()
        for u,p in path_length.iteritems():
            for v,d in p.iteritems():
                distances[nodes.index(u)-1][nodes.index(v)-1] = d
        sd = distance.squareform(distances)
        hier = hierarchy.average(sd)
        pylab.clf();
        hierarchy.dendrogram(hier)

        pylab.xticks(pylab.xticks()[0], nodes)



    def plot_degree_rank(self, loc='upper right', alpha=0.8, markersize=10,
            node_size=25, layout='spring', marker='o', color='b'):
        """Plot degree of all nodes

        .. plot::
            :include-source:
            :width: 50%

            from cno import CNOGraph
            c = CNOGraph(cnodata("PKN-ToyPB.sif"))
            c.plot_degree_rank()

        """
        degree_sequence=sorted(nx.degree(self).values(),reverse=True) # degree sequence

        pylab.clf()
        pylab.loglog(degree_sequence, color+'-', marker=marker,
                markersize=markersize)
        pylab.title("Degree/rank and undirected graph layout")
        pylab.ylabel("Degree")
        pylab.xlabel("Rank")

        # draw graph in inset
        if loc == 'upper right':
            pylab.axes([0.45, 0.45, 0.45, 0.45])
        else:
            pylab.axes([0.1, 0.1, 0.45, 0.45])

        UG = self.to_undirected()
        Gcc = nx.connected_component_subgraphs(UG)[0]
        if layout == 'spring':
            pos = nx.spring_layout(Gcc)
        else:
            pos = nx.circular_layout(Gcc)
        pylab.axis('off')
        nx.draw_networkx_nodes(Gcc, pos, node_size=node_size)
        nx.draw_networkx_edges(Gcc, pos, alpha=alpha)
        pylab.grid()
        #pylab.show()

    def plot_feedback_loops_histogram(self):
        """Plots histogram of the cycle lengths found in the graph

        :return: list of lists containing all found cycles
        """
        data = list(nx.simple_cycles(self))
        pylab.hist([len(x) for x in data])
        pylab.title("Length of the feedback loops")
        return data

    def plot_in_out_degrees(self, show=True,ax=None, kind='kde'):
        """
         .. plot::
            :include-source:
            :width: 50%

            from cno import CNOGraph
            c = CNOGraph(cnodata("PKN-ToyPB.sif"), cnodata("MD-ToyPB.csv"))
            c.plot_in_out_degrees()


        """
        import pandas as pd
        ts1 = pd.TimeSeries(self.in_degree())
        ts2 = pd.TimeSeries(self.out_degree())
        df = pd.DataFrame([ts1, ts2]).transpose()
        df.columns = ["in","out"]
        if show:
            df.plot(kind=kind, ax=ax)  # kernerl density estimation (estimiation of histogram)
        #df = ...
        #df.transpose().hist()
        return df

    def plot_feedback_loops_species(self, cmap="Reds"):
        """Returns and plots species part of feedback loops


        :param str cmap: a color map
        :return: dictionary with key (species) and values (number of feedback loop
            containing the species) pairs.


        """
        cmap = self._get_cmap(cmap)

        data = nx.simple_cycles(self)
        data = list(pylab.flatten(data))
        if len(data) == 0:
            print("no loops found")
            return
        counting = [(x, data.count(x)) for x in self.nodes() if data.count(x)!=0 and "and" not in x and "^" not in x]

        M = float(max([count[1] for count in counting]))
        # set a default
        #for node in self.nodes():
        #    self.node[node]['loops'] = "#FFFFFF"
        for node in self.nodes():
            self.node[node]['loops'] = 0

        for count in counting:
            #ratio_count = sm.to_rgba(count[1]/M)
            ratio_count = count[1]/M
            colorHex = ratio_count
            #self.node[count[0]]['loops'] = colorHex
            self.node[count[0]]['loops'] = ratio_count
            self.node[count[0]]['style'] =  'filled,bold'

        self.plot(node_attribute="loops", cmap=cmap)
        return counting



    def degree_histogram(self, show=True, normed=False):
        """Compute histogram of the node degree (and plots the histogram)

        .. plot::
            :include-source:
            :width: 50%

            from cno import CNOGraph
            c = CNOGraph(cnodata("PKN-ToyPB.sif"), cnodata("MD-ToyPB.csv"))
            c.degree_histogram()


        """
        degree = self.degree().values()
        Mdegree = max(degree)

        if show == True:
            pylab.clf()
            res = pylab.hist(degree, bins=range(0,Mdegree+1), align='left',
                             rwidth=0.8, normed=normed)
            xlims = pylab.xlim()
            ylims = pylab.ylim()
            pylab.axis([0, xlims[1], ylims[0], ylims[1]*1.1])
            pylab.grid()
            pylab.title("Degree distribution")
        return res
    def plot_adjacency_matrix(self, fontsize=12, **kargs):
        """Plots adjacency matrix

        :param kargs : optional arguments accepted by pylab.pcolor

        .. plot::
            :width: 70%

            from cno import CNOGraph
            from pylab import *
            c = CNOGraph(cnodata("PKN-ToyMMB.sif"), cnodata("MD-ToyMMB.csv"))
            c.plot(hold=True)

        .. plot::
            :width: 70%
            :include-source:

            from cno import CNOGraph
            from pylab import *
            c = CNOGraph(cnodata("PKN-ToyMMB.sif"), cnodata("MD-ToyMMB.csv"))
            c.plot_adjacency_matrix()

        """
        nodeNames = sorted(self.nodes())
        nodeNamesY = sorted(self.nodes())

        nodeNamesY.reverse()
        N = len(nodeNames)

        data = self.adjacency_matrix(nodelist=nodeNames)

        pylab.pcolor(pylab.flipud(pylab.array(data)), edgecolors="k", **kargs)
        pylab.axis([0, N, 0, N])
        pylab.xticks([0.5+x for x in pylab.arange(N)], nodeNames, rotation=90,
                      fontsize=fontsize)
        pylab.yticks([0.5+x for x in pylab.arange(N)], nodeNamesY, rotation=0,
                      fontsize=fontsize)
        pylab.tight_layout()