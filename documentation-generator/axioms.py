import rdflib
from rdflib import Graph
g = rdflib.Graph()
import os
import glob
import csv
from rdflib import RDF, RDFS, OWL, Namespace
from rdflib.tools import rdf2dot
from rdflib.plugins.sparql import sparql

#Information before running the code :
# - This specific code should be placed in the directory given below in order to run and produce the csv file.
#- This code can be adjusted for any turtle file that contains axioms by just adjusting the path name.
# - This code has as an output all the turtle files in the given directory for the purpose of double checking and prints out their output, the location of that output can be adjusted.
# -This code also has an output of the names files that are not consistent, possible due to doublications.
# Next step is the translation of said axioms to Manchester Syntax.

data_path = "/Users/andreachristou/Documents/kwg-seed-graph/schemas"
general_axioms = dict()
exceptions = []
ttl_files=dict()

#function to find the axioms
def find_axioms(filename, data_path="", root="",
             general_axioms=general_axioms):
    with open(os.path.join(root, data_path, filename)) as f:
        
        g.parse(f)
        for (s,p,o) in g.triples((None,None,None)):
            if type(s)==rdflib.term.BNode:
                try :
                    general_axioms[s]+=[(p,o)]
                except KeyError as e:
                    general_axioms[s]=[(p,o)]                    
                    
                
                
    return general_axioms

#finding all axioms from all ttl files in the "schemas" directory and printing out the files that are not properly formatted
for di in os.listdir(data_path):
    if os.path.isdir(di):
        print(di)
        for file in os.listdir(di):
            if file.endswith(".ttl"):
                print(f"    {file}")
                
                try:
                    general_axioms = find_axioms(
                        filename=file,
                        root=data_path,
                        data_path=di
                     )
                
                except:
                    exceptions.append(str(os.path.join(data_path, di, file)))
            
                    

def find_ttl_file(filename, data_path="", root="",
             ttl_files=ttl_files):
    with open(os.path.join(root, data_path, filename)) as f:
        g.parse(f)
        print(g.print())
                
                
    return ttl_files


for di in os.listdir(data_path):
    if os.path.isdir(di):
        print(di)
        for file in os.listdir(di):
            if file.endswith(".ttl"):
                
                print(f"    {file}")
                
                
                try:
                    ttl_files = find_ttl_file(
                        filename=file,
                        root=data_path,
                        data_path=di
                     )
                
                except:
                    exceptions.append(str(os.path.join(data_path, di, file)))
print(f"Excepions: {exceptions}")
#losing variables cause of repeated keys

 
             




#printing the axioms to a csv file:
with open('axioms.csv', 'w') as f:
   writer = csv.writer(f)
   writer.writerow(['file','subject','predicate','object'])
    #loop through general_axioms and write to csv
   for subject,pred_obj in general_axioms.items():
        for tup in pred_obj:
            writer.writerow([ file,subject, tup[0], tup[1]])
#-----------------------------------#

