from rdflib import Graph, RDF, RDFS, OWL
from rdflib.namespace import Namespace
from rdflib.term import BNode
import os

path =  "/Users/andreachristou/Documents/kwg-seed-graph/schemas/earthquake-usgs-schema.ttl"

general_axioms = dict()
exceptions = []
ttl_files=dict()

general_axioms = dict()
exceptions = []
ttl_files=dict()

#function to find the axioms
def find_axioms(filename, path="", root="",
             general_axioms=general_axioms):
    with open(os.path.join(root, path, filename)) as f:
        
        g = Graph()
        g.parse(path + '/' + filename, format="turtle")
        # Extract the prefixes from the graph
        
        prefixes = {}
        for prefix, namespace in g.namespaces():
            prefixes[prefix] = namespace
        # Iterate over the triples in the graph
        for s, p, o in g.triples((None,RDF.type,OWL.Class)):
            subject = s
            predicate = p
            obj = o
            for s1,p1,o1 in g.triples((s,RDFS.subClassOf,None)):
                
                # Replace the URI with the corresponding prefix
                for prefix, namespace in prefixes.items():
                    if str(s1).startswith(namespace):
                        subject = f"{prefix}:{s1.split('#', 1)[-1]}"
                        subject_=subject.rpartition('/')[-1]
                        
                    if str(p1).startswith(namespace):
                        predicate = f"{prefix}:{p1.split('#', 1)[-1]}"
                        #predicate_=predicate.replace("rdfs:type","subClassOf")
                        
                    
                    if str(o1).startswith(namespace):
                        obj = f"{prefix}:{o1.split('#', 1)[-1]}"
                        obj_=obj.rpartition('/')[-1]
                                
                    
                if type(s1) == BNode:
                    try:
                        general_axioms[s1] += [(predicate, obj_)]
                    except KeyError as e:
                        general_axioms[s1] = [(predicate, obj_)]
                else:
                    # Print the triple in Manchester syntax
                    print("-----------------------------")
                    print(f"{subject_} {predicate} {obj_} .")
            # Iterate over the general axioms and print them
            """
            for s1, triples in general_axioms.items():
                print("-----------------------------")
                print(f"{s1}  ", end="")
                for p1, o1 in triples:
                    print(f"{p1} {o1};", end=" ")
                print(".")
                """
                    

            
            
                             
                        
                    
                    
        return general_axioms


#finding all axioms from all ttl files in the "schemas" directory and printing out the files that are not properly formatted
for di in os.listdir(path):
    if os.path.isdir(di):
        print(di)
        for file in os.listdir(di):
            if file.endswith(".ttl"):
                print(f"    {file}")
                
                try:
                    general_axioms = find_axioms(
                        filename=file,
                        root=path,
                        path=di
                     )
                
                except:
                    exceptions.append(str(os.path.join(path, di, file)))
print("-----------------")
print(f"Excepions: {exceptions}")
