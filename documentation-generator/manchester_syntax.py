from rdflib import Graph, RDF, RDFS, OWL
from rdflib.namespace import Namespace
from rdflib.term import BNode
import os


#Information before running this code:

#- This code must be placed in the "schemas" directory of the "kwg-seed-graph" reprisatory in order to run.
#- For this stage it is suggested to just run this in the command line while being in the directory :
# python3 testing_manchester.py > testing_manchester.txt, just to have a look in what it generates since
# the data is of high volume.
# This code can be adjusted for any directory.
# It takes all axiom triples from the ttl files in the given directory and translates them to Manchester Syntax.
# It is yet to be adjusted for more "human-readable" version.
# The code commented below is a variation of the code on first lines, it is kept for extra help
# if there is a need to adjust the code.
path =  "/Users/andreachristou/Documents/kwg-seed-graph/schemas"

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
        for s, p, o in g.triples((None, None, None)):
            subject = s
            predicate = p
            obj = o
            # Replace the URI with the corresponding prefix
            for prefix, namespace in prefixes.items():
                if str(s).startswith(namespace):
                    subject = f"{prefix}:{s.split('#')[-1]}"
                if str(p).startswith(namespace):
                    predicate = f"{prefix}:{p.split('#')[-1]}"
                if str(o).startswith(namespace):
                    obj = f"{prefix}:{o.split('#')[-1]}"
            if type(s) == BNode:
                try:
                    general_axioms[s] += [(predicate, obj)]
                except KeyError as e:
                    general_axioms[s] = [(predicate, obj)]
            else:
                # Print the triple in Manchester syntax
                print(f"{subject} {predicate} {obj} .")
        # Iterate over the general axioms and print them
        for s, triples in general_axioms.items():
            
            print(f"{s}  ", end="")
            for p, o in triples:
                print(f"{p} {o};", end=" ")
            print(".")
                

        
        
                         
                    
                
                
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
print(f"Excepions: {exceptions}")
            
"""
for filename in os.listdir(path):
    if filename.endswith(".ttl"):
        print(filename)
        # Load the turtle file into a graph
        g = Graph()
        g.parse(path + '/' + filename, format="turtle")
        # Extract the prefixes from the graph
        
        prefixes = {}
        for prefix, namespace in g.namespaces():
            prefixes[prefix] = namespace

        general_axioms = {}

        # Iterate over the triples in the graph
        for s, p, o in g.triples((None, None, None)):
            subject = s
            predicate = p
            obj = o

            # Replace the URI with the corresponding prefix
            for prefix, namespace in prefixes.items():
                if str(s).startswith(namespace):
                    subject = f"{prefix}:{s.split('#')[-1]}"
                if str(p).startswith(namespace):
                    predicate = f"{prefix}:{p.split('#')[-1]}"
                if str(o).startswith(namespace):
                    obj = f"{prefix}:{o.split('#')[-1]}"

            if type(s) == BNode:
                try:
                    general_axioms[s] += [(predicate, obj)]
                except KeyError as e:
                    general_axioms[s] = [(predicate, obj)]

            else:
                # Print the triple in Manchester syntax
                print(f"{subject} {predicate} {obj} .")

        # Iterate over the general axioms and print them
        for s, triples in general_axioms.items():
            
            print(f"{s}  ", end="")
            for p, o in triples:
                print(f"{p} {o};", end=" ")
            print(".")
"""

