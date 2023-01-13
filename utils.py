import igraph
from numpy.random import gumbel


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in set(graph.neighbors(start, mode="OUT")) - set(path):
        paths.extend(find_all_paths(graph, node, end, path))
    return paths

def calculate_new_cost(graph_matrix):
    graph_matrix.loc[:, 'cost'] = graph_matrix.loc[:, 'free_flow_time'] + graph_matrix.loc[:, 'b'] * (graph_matrix.loc[:, 'flow'] / graph_matrix.loc[:, 'capacity'])
    return graph_matrix

# need to calculate softmax logit
def get_path_cost(path_list, graph_matrix):
    path_cost = 0.
    for i, _ in enumerate(path_list, 0):
        if i + 1 == len(path_list):
            break
        path_cost += list(graph_matrix[(graph_matrix.init_node == path_list[i]) & (graph_matrix.term_node == path_list[i + 1])]['cost'])[0]
    return path_cost

# def calculate_new_cost(graph_matrix):
#     graph_matrix.loc[:, 'cost'] = graph_matrix.loc[:, 'free_flow_time'] * (1 + graph_matrix.loc[:, 'b'] * (graph_matrix.loc[:, 'flow'] / graph_matrix.loc[:, 'capacity'])**(graph_matrix.loc[:, 'power']))
#     return graph_matrix

def get_gumbel_values(path_quantity, gamma, euler_value = 0.5772, mean_value = 0.):
    return gumbel(loc=mean_value, scale=gamma, size = path_quantity)