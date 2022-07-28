from enum import unique
import scipy.sparse as sparse
import sys

def normalize(city):
    return '_'.join(city.lower().split())

def add_city(city):
    normalized = normalize(city)
    if normalized not in dict:
        dict[normalized] = True

def build_array():
    unique_cities = len(dict)
    matrix = [[9999]*unique_cities]*unique_cities
    i = 0
    for key in dict.keys():
        dict[key] = i
        i = i + 1
    return matrix

def add_weight(matrix, source, sink, weight):
    source_index = dict[source]
    sink_index = dict[sink]
    matrix[source_index][sink_index] = weight
    matrix[sink_index][source_index] = weight

def populate_array(matrix, edges):
    for edge in edges:
        (source, sink, weight) = edge
        add_weight(matrix, source, sink, weight)



# graph = [[0,1,2],[1,0,5],[2,5,0]]
# result = sparse.csgraph.floyd_warshall(graph)
# print(result)

starting = True

dict = {}
tuples = []



with open('graph.tsv', 'r') as f:
    for line in f:
        try: 
            if starting:
                starting = False
                continue        
            source, sink, weight = tuple(line.split('\t'))
            source, sink = (normalize(source), normalize(sink))
            weight = int(weight)
            add_city(source)
            add_city(sink)
            tuples.append((source, sink, weight))
        except Exception:
            print("Error parsing line ", line, " : please validate that the format is correct.")

matrix = build_array()
print(dict)
print(tuples)

populate_array(matrix, tuples)

result = sparse.csgraph.floyd_warshall(matrix)
for distance in result:
    print(distance)
        