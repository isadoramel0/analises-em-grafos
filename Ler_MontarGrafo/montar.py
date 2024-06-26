import re

class Grafo:
    def __init__(self, vertices, arestas, direcionado=False):
        self.vertices = vertices
        self.arestas = arestas
        self.direcionado = direcionado
        self.adj_list = {v: [] for v in vertices}
        
        for (v1, v2, peso) in arestas:
            if peso is not None:  # Grafo ponderado
                self.adj_list[v1].append((v2, peso))
                if not self.direcionado:
                    self.adj_list[v2].append((v1, peso))  # aresta bidirecional
            else:  # Grafo não ponderado
                self.adj_list[v1].append(v2)
                if not self.direcionado:
                    self.adj_list[v2].append(v1)  # aresta bidirecional

    def __repr__(self):
        vertices_str = f'Vertices: {self.vertices}\n'
        arestas_str = 'Arestas: ['
        for i, (v1, v2, peso) in enumerate(self.arestas):
            if peso is not None:
                arestas_str += f'({v1}, {v2}, {peso})'
            else:
                arestas_str += f'({v1}, {v2})'
            if i < len(self.arestas) - 1:
                arestas_str += ', '
        arestas_str += ']\n'

        adj_list_str = 'Lista de Adjacencia:\n'
        for v in self.adj_list:
            adj_list_str += f'{v}: {self.adj_list[v]}\n'
        return vertices_str + arestas_str + adj_list_str
    
    def inverter_arestas(self):
        self.adj_list_reverso = {v: [] for v in self.vertices}
        for v in self.vertices:
            for vizinho in self.adj_list[v]:
                if isinstance(vizinho, tuple):  # Aresta ponderada
                    self.adj_list_reverso[vizinho[0]].append((v, vizinho[1]))
                else:  # Aresta não ponderada
                    self.adj_list_reverso[vizinho].append(v)

        self.adj_list, self.adj_list_reverso = self.adj_list_reverso, self.adj_list


def ler_grafo_de_arquivo(filename):
    with open(filename, 'r') as file:
        data = file.read().strip()  # lê o arquivo e remove espaços em branco nas extremidades;

    vertices_padrao = r'V = \{([a-zA-Z,]+)\};'
    arestas_padrao = r'A = \{(.+?)\};'

    # verificação de chaves de vértices e arestas;
    if '{' not in data or '}' not in data:
        raise ValueError("Chaves de vértices ou arestas não encontradas ou incorretamente formatadas.")

    # procurando o padrão dentro de data;
    vertices_match = re.search(vertices_padrao, data)
    arestas_match = re.search(arestas_padrao, data)

    if not vertices_match:
        raise ValueError("O arquivo não segue o formato esperado para vértices.")
    if not arestas_match:
        raise ValueError("O arquivo não segue o formato esperado para arestas.")

    vertices = vertices_match.group(1).split(',')
    arestas_verifica = arestas_match.group(1)

    if not re.match(r'^\(\s*[a-zA-Z]\s*,\s*[a-zA-Z]\s*(?:,\s*-?\d+)?\s*\)(?:,\s*\(\s*[a-zA-Z]\s*,\s*[a-zA-Z]\s*(?:,\s*-?\d+)?\s*\))*$', arestas_verifica):
        raise ValueError("Erro de formatação em uma ou mais arestas.")

    arestas_list = re.findall(r'\(\s*([a-zA-Z]),\s*([a-zA-Z])(?:,\s*(-?\d+))?\s*\)', arestas_verifica)

    if not arestas_list:
        raise ValueError("Nenhuma aresta válida encontrada ou formato de arestas incorreto.")

    arestas = []
    tem_peso = None
    for v1, v2, peso in arestas_list:
        v1 = v1.strip()
        v2 = v2.strip()
        peso = int(peso) if peso else None

        if tem_peso is None:
            tem_peso = peso is not None
        elif (peso is not None) != tem_peso:
            # verifica se todas as arestas têm ou não um peso definido;
            raise ValueError("O arquivo contém arestas com e sem peso misturadas.")

        if v1 not in vertices or v2 not in vertices:
            # verifica se os vértices da aresta pertencem aos do grafo;
            raise ValueError(f"Aresta vai para vértices que não pertencem ao grafo: ({v1},{v2},{peso})")

        arestas.append((v1, v2, peso))

    return vertices, arestas


def criar_grafo_de_arquivo(filename, direcionado):
    vertices, arestas = ler_grafo_de_arquivo(filename)
    grafo = Grafo(vertices, arestas, direcionado)
    return grafo
