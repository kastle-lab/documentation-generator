import os

from rdflib import OWL, RDF, RDFS, Graph
from rdflib.namespace import Namespace
from rdflib.term import BNode

# Information before running this code:
# - This code must be placed in the earthquake-usgs of the "schemas" directory of the "kwg-seed-graph" reprisatory in order to run.
# - It is just a testing code and then it will be adapted for every ttl fiele in a given directory.
# This code can be adjusted for any directory.
# Still need to remove the "None" prints.


# Convenient
a = RDF.type
sco = RDFS.subClassOf

owl_some = OWL.someValuesFrom
owl_all = OWL.allValuesFrom


def replace_prefix(uri, prefixes=[]):
    for prefix, namespace in prefixes.items():
        if uri.startswith(namespace):
            uri = f"{prefix}:{uri.split('#', 1)[-1]}"
            uri = uri.rpartition('/')[-1]
            return uri


def get_axiom(s, p, o, prefixes):
    restriction = None
    if p == owl_some:
        restriction = "some"
    elif p == owl_all:
        restriction = "only"
    if restriction:
        s = replace_prefix(s, prefixes=prefixes) if s else None
        o = replace_prefix(o, prefixes=prefixes) if o else None
        if s and o:
            restriction_axiom = f"{s} subClassOf: {replace_prefix(s, prefixes=prefixes)} {restriction} {o}"
            return restriction_axiom
    else:
        s = replace_prefix(s, prefixes=prefixes) if s else None
        o = replace_prefix(o, prefixes=prefixes) if o else None
        if s and o:
            sub_class_axiom = f"{s} subClassOf: {o}"
            return sub_class_axiom


def get_restrictions(g, axiom, prefixes):
    on_property = None
    some_values_from = None
    all_values_from = None

    for triple in g.triples((axiom, None, None)):
        if triple[1] == OWL.onProperty:
            on_property = triple[2]
        if triple[1] == owl_some:
            some_values_from = triple[2]
        if triple[1] == owl_all:
            all_values_from = triple[2]

    if on_property and some_values_from:
        restriction = f"{replace_prefix(on_property, prefixes=prefixes)} some {replace_prefix(some_values_from, prefixes=prefixes)} "
        return restriction
    if on_property and all_values_from:
        restriction = f"{replace_prefix(on_property, prefixes=prefixes)} only {replace_prefix(all_values_from, prefixes=prefixes)} "
        return restriction


def axiom_translation(g, row):
    axiomatization = ""
    axioms_list = list()
    restrictions = list()
    explanations = list()

    g = Graph()
    g.parse(row["ttl_path"], format="turtle")
    prefixes = {}
    for prefix, namespace in g.namespaces():
        prefixes[prefix] = namespace

    for s1, p1, o1 in g.triples((None, a, OWL.Class)):
        axioms = [triple for triple in g.triples((s1, sco, None))] + \
            [triple for triple in g.triples((None, sco, s1))]

        for axiom in axioms:
            
            s, p, o = axiom
            axioms_list.append(get_axiom(s, p, o, prefixes))

            if type(axiom[0]) == BNode:
                restrictions.append(get_restrictions(g, axiom[0], prefixes))

            if type(axiom[2]) == BNode:
                restrictions.append(get_restrictions(g, axiom[2], prefixes))

    axiomatization += "\\subsection{Axioms}\n"
    axiomatization += "\\begin{align}\n"
    sum_list = axioms_list + restrictions
    # print(sum_list)
    for axiom in sum_list:
        if axiom:
            formated_axiom = "".join(["~\\textsf{" + s + "}" for s in axiom.split()])[1:]
            formated_axiom = formated_axiom.replace("_","\_")
            axiomatization += "  " + formated_axiom
            if axiom != sum_list[-1]:
                axiomatization += "\\\\\n"
    axiomatization += "\\end{align}\n\n"
    return axiomatization

if __name__ == "__main__":
    path = "/Users/saeid/Documents/GitHub/kwg-seed-graph/schemas/earthquake-usgs"
    filename = "earthquake-usgs-schema.ttl"
    ttl_path = os.path.join(path, filename)
    row = {}
    row["ttl_path"] = ttl_path
    print(axiom_translation(g=None, row=row))
