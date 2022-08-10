from enum import unique
import scipy.sparse as sparse

def normalize(city):
    return '_'.join(city.lower().split())

def denormalize(city):
    return ' '.join(map(lambda x: x.capitalize(), city.split('_')))

def add_city(city):
    normalized = normalize(city)
    if normalized not in dict:
        dict[normalized] = True

def build_array():
    unique_cities = len(dict)
    matrix = [[9999 for i in range(unique_cities)] for j in range(unique_cities)]
    i = 0
    for key in dict.keys():
        dict[key] = i
        name_lookup[i] = key
        i = i + 1
    for x in range(len(matrix)):
        cur = matrix[x][x]
        matrix[x][x] = 0
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

starting = True

dict = {}
name_lookup = {}
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

populate_array(matrix, tuples)

result = sparse.csgraph.floyd_warshall(matrix)

result_grid = [['City']]

for x in range(len(result)):
    denorm_name = denormalize(name_lookup[x])
    result_grid[0].append(denorm_name)

for x in range(len(result)):
    current_house = [denormalize(name_lookup[x])]
    for y in range(len(result)):
        current_house.append(int(result[x][y]))
    result_grid.append(current_house)


with open('output.csv',"w") as f:
    for row in result_grid:
        csv = ','.join(map(lambda x: str(x),row))
        f.write(csv)
        f.write('\n')
        