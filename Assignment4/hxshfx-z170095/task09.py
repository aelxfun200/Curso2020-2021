# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aA_7cDJnS46kKnLS5uuCGN5_s3QANqk-

**Task 09: Data linking**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"resources/data03.rdf", format="xml")
g2.parse(github_storage+"resources/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

print("TASK 9")

from rdflib.namespace import RDF, RDFS, OWL

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")

people_g1 = []
people_g2 = []

# Incluye en la lista del grafo correspondiente las personas encontradas,
# asi como su apodo y nombre de familia
def recopilate(graph):
    if graph is g1:
        people = people_g1
        ns = ns1
    else:
        people = people_g2
        ns = ns2
    for s,p,o in graph.triples((None, RDF.type, ns.Person)):
        given = graph.value(subject=s, predicate=VCARD.Given, object=None)
        family = graph.value(subject=s, predicate=VCARD.Family, object=None)
        if given is not None and family is not None:
            people.append([s, given, family])

# Compara si la persona descrita en el segundo argumento se encuentra en la lista
# de personas pasada como primer argumento. La comparacion se realiza mirando
# los valores de los literales, almacenados en la primera y segunda posicion
def contains(list, person):
    result = None
    for elem in list:
        if result is not None:
            break
        if elem[1].value == person[1].value and elem[2].value == person[2].value:
            result = elem[0]
    return result

recopilate(g1)
recopilate(g2)

for p1 in people_g1:
    p2 = contains(people_g2, p1)
    if p2 is not None:
        g3.add((p1[0], OWL.sameAs, p2))

print("\nGraph 3:")
print(g3.serialize(format="ttl").decode("UTF-8"))