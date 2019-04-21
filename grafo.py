from vertice import *
from aresta import *
import xlrd

class Grafo:

  def __init__(self, nome, direcionado):
    self.nome = nome
    self.direcionado = direcionado
    self.vertices = []
    self.arestas = []

  def criar_aresta(self, id, vertice_1, vertice_2, peso):
    existe_vertice_1 = self.elemento_existe(vertice_1, self.vertices)
    existe_vertice_2 = self.elemento_existe(vertice_2, self.vertices)
    if existe_vertice_1 and existe_vertice_2:
      self.aumenta_grau_vertice(vertice_1)
      self.aumenta_grau_vertice(vertice_2)
      aresta = Aresta(id.upper(), vertice_1, vertice_2, peso)
      self.arestas.append(aresta)
      return True
    else:
      return False

  def aumenta_grau_vertice(self, id_vertice):
    index = self.get_vertice_index(id_vertice)
    self.vertices[index].aumenta_grau()
  
  def diminui_grau_vertice(self, id_vertice):
    index = self.get_vertice_index(id_vertice)
    self.vertices[index].diminui_grau()

  def criar_vertices(self, id):
    lista_vertices = self.get_lista_elementos(id)
    for v in lista_vertices:
      if self.elemento_existe(v, self.vertices):
        print("Vertice {} já existe na lista".format(v))
      else:
        vertice = Vertice(v.upper())
        self.vertices.append(vertice)
    return self.vertices
  
  def get_lista_elementos(self, id):
    return id.split(' ')
    
  def elemento_existe(self, elemento, array):
    for v in array:
      if v.id == elemento.upper():
        return True
    return False

  def deleta_aresta(self, id):
    index = self.get_aresta_index(id)
    aresta = self.arestas.pop(index)
    vertice_1 = aresta.vertice_1
    vertice_2 = aresta.vertice_2
    self.diminui_grau_vertice(vertice_1)
    self.diminui_grau_vertice(vertice_2)
    return index

  def get_aresta_index(self, id_aresta):
    for index, aresta in enumerate(self.arestas):
      if aresta.id == id_aresta:
        return index
    else:
      return False

  def get_vertices_adjacentes(self, id_vertice):
    vertices_adjacentes = []
    for aresta in self.arestas:
      if aresta.vertice_1 == id_vertice:
        vertices_adjacentes.append(aresta.vertice_2)
      elif aresta.vertice_2 == id_vertice:
        vertices_adjacentes.append(aresta.vertice_1)
    return vertices_adjacentes

  def deleta_vertice(self, id):
    index_remocao = self.get_vertice_index(id)
    self.vertices.pop(index_remocao)
    remover_arestas = self.get_arestas_from_vertice(id)
    for aresta in remover_arestas:
      self.deleta_aresta(aresta)

  def get_arestas_from_vertice(self, id_vertice):
    aux_arestas = []
    for a in self.arestas:
      if a.vertice_1 == id_vertice or a.vertice_2 == id_vertice:
        aux_arestas.append(a.id)
    return aux_arestas

  def grau_minimo(self):
    graus_vertices = self.lista_graus()
    return min(graus_vertices)

  def grau_medio(self):
    graus_vertices = self.lista_graus()
    return sum(graus_vertices)/len(graus_vertices)
    
  def grau_maximo(self):
    graus_vertices = self.lista_graus()
    return max(graus_vertices)
  
  def lista_graus(self):
    aux = []
    for vertice in self.vertices:
      aux.append(vertice.grau)
    return aux

  def get_vertice_grau(self, id):
    index = self.get_vertice_index(id.upper())
    vertice = self.vertices[index]
    return vertice.grau

  def get_vertice_index(self, id):
    for index, vertice in enumerate(self.vertices):
      if vertice.id == id:
        return index
    else:
      return False

  def get_vertices(self): 
    return self.vertices
  
  def get_arestas(self):
    aux = []
    for aresta in self.arestas:
      aux.append(aresta.vertice_1.nome)
      aux.append(aresta.vertice_2.nome)
      aux.append(aresta.peso)
    return aux

  def exite_aresta_entre_vertices(self, v1, v2):
    resposta = {"msg": "Não existe aresta entre os vértices {} e {}.".format(v1, v2)}
    v1_existe = self.elemento_existe(v1, self.vertices)
    v2_existe = self.elemento_existe(v2, self.vertices)
    if v1_existe and v2_existe:
      for aresta in self.arestas:
        if (aresta.vertice_1 == v1 and aresta.vertice_2 == v2) or (aresta.vertice_1 == v2 and aresta.vertice_2 == v1):
          resposta = {"msg": "Existe uma aresta entre os vértices {} e {}.".format(v1, v2)}
          return resposta
    else:
      resposta = {"msg": "Ambos os vértices devem existir."}
    return resposta

  def le_arquivo(self):
    arquivo = xlrd.open_workbook("grafo.xlsx")

    planilha_vertices = arquivo.sheet_by_index(0)
    dado_coluna = planilha_vertices.col(0)
    for texto in dado_coluna:
      self.criar_vertices(texto.value)

    planilha_arestas = arquivo.sheet_by_index(1)
    tam = planilha_arestas.nrows
    while tam > 0:
      self.criar_aresta(planilha_arestas.cell_value(tam-1, 0), planilha_arestas.cell_value(tam-1, 1), planilha_arestas.cell_value(tam-1, 2), planilha_arestas.cell_value(tam-1, 3))
      tam -= 1

  def eh_conexo(self):
    self.visitado = []
    vertices_visitados = self.busca_em_profundidade(self.vertices[0].id)
    return len(vertices_visitados) == len(self.vertices)

  def busca_em_profundidade(self, id):
    self.visitado.append(id)
    v_adjacentes = self.get_vertices_adjacentes(id)
    for v in v_adjacentes:
      if not(v in self.visitado):
        self.busca_em_profundidade(v)
    return self.visitado

  def eh_euleriano(self):
    resposta = self.eh_conexo()
    impares = 0
    if (resposta):
      for i in self.vertices:
        if (i.grau % 2 != 0):
          impares += 1
      if (impares == 0) or (impares == 2):
        result = True
      else: 
        result = False
    else:
      result = False
    return result