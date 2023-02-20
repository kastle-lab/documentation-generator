from rdflib import Graph, RDF, RDFS, OWL
from rdflib.namespace import Namespace
from rdflib.term import BNode
import os

#Information before running this code:
#- This code must be placed in the earthquake-usgs of the "schemas" directory of the "kwg-seed-graph" reprisatory in order to run.
#- It is just a testing code and then it will be adapted for every ttl fiele in a given directory.
# This code can be adjusted for any directory.
#Still need to remove the "None" prints.


# Convenient
a = RDF.type
sco = RDFS.subClassOf

owl_some = OWL.someValuesFrom
owl_all = OWL.allValuesFrom

def find_axioms(path, filename):
    file_path = os.path.join(path, filename)

    with open(file_path, "r") as f:
        g = Graph()
        g.parse(path + '/' + filename, format="turtle")
        prefixes = {}
        for prefix, namespace in g.namespaces():
            prefixes[prefix] = namespace

        def replace_prefix(uri, prefixes=prefixes,):
            for prefix, namespace in prefixes.items():
                if uri.startswith(namespace):
                    uri = f"{prefix}:{uri.split('#', 1)[-1]}"
                    uri = uri.rpartition('/')[-1]
                    return uri

        def print_axiom(s, p, o):
            
                  
            
            restriction = None
            if p == owl_some:
                restriction = "some"
            elif p == owl_all:
                restriction = "only"
               
            if restriction:
                restriction_axiom = f"{replace_prefix(s)} subClassOf: {replace_prefix(on_property)} {restriction} {replace_prefix(o)}"
                print(restriction_axiom)
            else:
                
                sub_class_axiom = f"{replace_prefix(s)} subClassOf: {replace_prefix(o)}"
                print(sub_class_axiom)
                
        for s1, p1, o1 in g.triples( (None, a, OWL.Class) ):
            axioms = [triple for triple in g.triples( (s1, sco, None) )] + \
            [triple for triple in g.triples( (None, sco, s1) )]
            
            for axiom in axioms:
                
                
                    
                
                    
                
                
                print_axiom(*axiom)
              
                if type(axiom[0]) == BNode:
                    on_property = None
                    some_values_from = None
                    all_values_from = None
                    
                    for triple in g.triples( (axiom[0], None, None) ):
                        if triple[1] == OWL.onProperty:
                            on_property = triple[2]
                        if triple[1] == owl_some:
                            some_values_from = triple[2]
                        if triple[1] == owl_all:
                            all_values_from = triple[2]
                        
                    if on_property and some_values_from:
                        restriction = f"{replace_prefix(on_property)} some {replace_prefix(some_values_from)} "
                        print(restriction)
                    if on_property and all_values_from:
                        restriction = f"{replace_prefix(on_property)} only {replace_prefix(all_values_from)} "
                        print(restriction)
                if type(axiom[2]) == BNode:
                    on_property = None
                    some_values_from = None
                    all_values_from = None
                    
                    for triple in g.triples(( axiom[2],None, None) ):
                        if triple[1] == OWL.onProperty:
                            on_property = triple[2]
                        if triple[1] == owl_some:
                            some_values_from = triple[2]
                        if triple[1] == owl_all:
                            all_values_from = triple[2]
                        
                    if on_property and some_values_from:
                        restriction = f"{replace_prefix(on_property)} some {replace_prefix(some_values_from)}  "
                        print(restriction)
                    if on_property and all_values_from:
                        restriction = f"{replace_prefix(on_property)} only {replace_prefix(all_values_from)} "
                        print(restriction)
                        
            
if __name__ == "__main__":
    path =  "/Users/andreachristou/Documents/kwg-seed-graph-Antrea/schemas/earthquake-usgs"
    filename = "earthquake-usgs-schema.ttl"
    find_axioms(path, filename)
