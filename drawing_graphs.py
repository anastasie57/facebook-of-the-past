#!/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
from matplotlib import rc
import networkx as nx
import codecs

font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)


def build_base_for_graphs(database):
    opened = codecs.open(database, u'r', u'utf-8')

    nodes = {}

    for i in opened:
        if i[0] == 'i':
            i = ''
        break
    
    for i in opened:
        case = [fact for fact in i.split(';')]
        ## case[1] - author, case[2] - addressee
        if case[1] not in nodes:
            nodes[case[1]] = {}
        if case[2] not in nodes:
            nodes[case[2]] = {}
            nodes[case[2]][case[1]] = 0
        if case[2] not in nodes[case[1]]:
            nodes[case[1]][case[2]] = 1        
        else:
            nodes[case[1]][case[2]] = nodes[case[1]][case[2]] + 1
            
    return nodes

def make_analyze(nodes, graph):
    html = u'<p><b>Всего участников сообщества:</b>' + str(graph.number_of_nodes()) + '</p>'
    html += u'<p><b>Самые популярные участники переписки:</b></p><ul>'
    popularity = nx.degree(graph)
    most_popular = max([popularity[node] for node in popularity])
    for node in popularity:
        if popularity[node] > 0.1 * most_popular:
            html += '<li>' + node + '</li>'
    html += '</ul'
##    html += u'<p><b>Самые активные участники переписки:</b></p><ul>'
##    for edge in graph.edges():
##        print edge
##        if edge[0]['weight'] > 0.3 * most_popular:
##            html += '<li>' + ' - '.join(edge)+ '</li>'
##    html += '</ul>'
    return html

def make_legend(legend):
    html = u'<table border="1"><colgroup width="110"/>'
    strings = legend.split('\r\n')
    html += u'<tr><td colspan="6" align = "center">Легенда</td></tr>'
    n = 0
    while n!= len(strings):
        for i in xrange(10):
            html += '<tr>\r\n'
            while i < len(strings):
                html += u'<td style="font-size: 10">' + strings[i] + u'</td>'
                i += 10
                n += 1
            html += u'\r\n</tr>\r\n'
    html += u'</table>'
    f = codecs.open('legend.html', 'w', 'utf-8')
    f.write(html)
    f.close()
    return html
            

def build_graph_for_socium(database):
    nodes = build_base_for_graphs(database)

    G = nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    nodesizes = [1/0.01 for node in nodes]
    for node in nodes:
        nodesizes[G.nodes().index(node)] = len(nodes[node])/0.01
    pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = nodesizes, node_color = 'yellow')

    for author in nodes:
        for person in nodes[author]:
            if nodes[author][person] == 0:
                G.add_weighted_edges_from([(person, author, nodes[person][author])])
            else:
                G.add_weighted_edges_from([(author, person, nodes[author][person])])
                if nodes[person][author] != 0:
                    G.add_weighted_edges_from([(person, author, nodes[person][author])])
                    
    colors=xrange(len(G.edges()))
    nx.draw_networkx_edges(G, pos, edge_color = colors, width = 0.5, edge_cmap = plt.cm.Greys)

    for p in pos: # raise text positions
        pos[p][1]+=0.06

    activeness = [len(nodes[node]) for node in nodes]
    most_active = max(activeness)
    
    nodelabels = {}
    in_legend = []
    n = 1
    for node in nodes:
        if len(nodes[node]) > 0.3 * most_active:
            nodelabels[G.nodes()[G.nodes().index(node)]] = node
        else:
            nodelabels[G.nodes()[G.nodes().index(node)]] = str(n)
            in_legend.append(node)
            n += 1
        
    nx.draw_networkx_labels(G,pos,labels = nodelabels, font_family = 'Verdana')

    legend = u''
    for node in in_legend:
        legend += nodelabels[node] + u' - '+ node + u'\r\n'
    make_legend(legend[:-4])
    
    result = plt.gcf()
    result.set_size_inches(10.5, 10.5)
    result.savefig('static/graph_socium.png', dpi=300)
    return make_legend(legend[:-4]), make_analyze(nodes, G)

def build_graph_for_person(database, info):
    nodes = build_base_for_graphs(database)
    
    G = nx.MultiDiGraph()
    G.add_node(info)
    for person in nodes[info]:
        G.add_node(person)
    nodesizes = []
    for i in xrange(len(G.nodes())):
        nodesizes.append(1/0.01)
    nodesizes[G.nodes().index(info)] = len(nodes[info])/0.01
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size = nodesizes, node_color = 'yellow')

    for person in nodes[info]:
        print person, info
        G.add_weighted_edges_from([(info, person, nodes[info][person])])
        if info in nodes[person]:
            if nodes[person][info] != 0:
                G.add_weighted_edges_from([(person, info, nodes[person][info])])

    colors=xrange(len(G.edges()))
    nx.draw_networkx_edges(G, pos, edge_color = colors, width = 0.7, edge_cmap = plt.cm.Greys)

    for p in pos: # raise text positions
        pos[p][1]-=0.06

    nodelabels = {}
    nodelabels[info] = info
    for node in nodes[info]:
        nodelabels[G.nodes()[G.nodes().index(node)]] = node
        
    nx.draw_networkx_labels(G,pos,labels = nodelabels, font_family = 'Verdana')
    
    result = plt.gcf()
    result.set_size_inches(10.5, 10.5)
    result.savefig('static/graph_person.png', dpi=300)


    return make_analyze(nodes, G)

#build_graph_for_person('tutchev.csv', u'Ф.И.Тютчев')

#build_graph_for_socium('tutchev.csv')
