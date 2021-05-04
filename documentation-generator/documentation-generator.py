import rdflib
from rdflib import RDF, RDFS, OWL

# =======================
# rdflib helper functions
def get_namespace(prefix, graph):
	'''Iterate through the namespaces and return the match'''
	for p, ns in graph.namespaces():
		if p == prefix:
			return ns
	return None

def get_predicate(prefix, predicate, graph):
	'''Construct a URI for a predicate given the pred_name, prefix, and graph'''
	ns = get_namespace(prefix, graph)
	return ns + predicate

# =======================
# LaTeX rendering
def tsf(x):
	'''Render in sans serif font'''
	return "\\textsf{" + x + "} "

# Shortcuts for math notations
sc     = "&\\sqsubseteq "
forall = "\\forall "
exists = "\\exists "
minz   = "\\lte 0"
func   = "\\lte 1"

# =======================
# Generate figure code
def generate_figure_code(filename, caption="Empty Caption", label=None):
	# Create filename path
	filename = "{resources/" + filename + "}"
	# Generate the label
	if label == None:
		label = get_label(filename)
	label = "{fig:" + label + "}"
	# Wrap Caption
	caption = "{" + caption + "}"
	# Construct figure code
	figure_lines = list()
	figure_lines.append("\\begin{figure}[h!]")
	figure_lines.append("  \\begin{center}")
	figure_lines.append("    \\includegraphics[width=\\textwidth]{}".format(filename))
	figure_lines.append("  \\end{center}")
	figure_lines.append("  \\caption{}".format(caption))
	figure_lines.append("  \\label{}".format(label))
	figure_lines.append("\\end{figure}")
	# Separate by new lines
	figure = '\n'.join(figure_lines)
	# And return
	return figure

# =======================
# Generation of common elements in subsections
def generate_label(label):
	label = label.replace(" ", "-").lower()

	return label

def generate_header(section_name, label=None):
	if label is None:
		label = generate_label(section_name)

	header =  "%"*35 + "\n"
	header += "\\subsection{" + section_name + "}\n"
	header += "\\label{ssec:" + label + "}\n"
	header += "%"*10 + "\n"

	return header

# =======================
# Subsection generators
def generate_overview(g):
	# Create Header
	overview = generate_header("Overview")
	# Begin Content Generation
	# =======================
	# Insert Overview Text
	overview += "I am the overview.\n"
	
	overview += "\n"
	# End Overview Text
	# =======================
	# Insert top level schema Diagram
	# Find if there is a schema diagram
	# get node representing this ontology
	# get predicate for schema diagram file name
	hSDF = get_predicate("opla-sd", "hasSchemaDiagramFileName", g)
	for s, p, o in g.triples((None, hSDF, None)):
		filename = str(o)
		figure_code = generate_figure_code(filename,label="ov")
		overview += figure_code

	# End subsection
	overview += "\n"
	return overview

def generate_cqs(g):
	# Create Header
	cqs = generate_header("Competency Questions", label="cqs")
	# Begin Content Generation
	cqs += "\\begin{enumerate}[\\phantom{CQ }CQ 1.]\n"
	# Create the predicate URI for the opla-cp:hasCompetencyQuestion
	hCQ = get_predicate("opla-cp", "hasCompetencyQuestion", g)
	# Now for each triple in the pattern, get the competency question
	# Note: g.triples() does not guarantee order
	for s, p, o in g.triples((None, hCQ, None)):
		cqs += "\t\\item "
		cqs += str(o)
		cqs += "\n"
	cqs += "\\end{enumerate}"
	# End subsection
	cqs += "\n"
	return cqs

def generate_usecases(g):
	# Create Header
	usecases = generate_header("Use Cases")
	# Begin Content Generation
	# Create the predicate URI for the opla-cp:addressesScenario
	aS = get_predicate("opla-cp", "addressesScenario", g)
	# Now for each triple in the pattern, get the scenarios (usecases)
	scenarios = g.triples((None, aS, None))
	# Note: g.triples() is a generator, so there is no easy way to 
	#   generate len hence this weird conditional workaround to 
	#   leave a token message if no competency questions are found.
	# Note: g.triples() does not guarantee order
	scenarios_is_empty = True
	first = True
	for s, p, o in scenarios:
		if first:
			scenarios_is_empty = False
			first = False
			usecases += "These are the usecases!\n"
			usecases += "\n"

		usecase = str(o)
		title, text = usecase.split("\n")

		usecases += "\\subsubsection{" + title + "}\n"
		usecases += text + "\n"
		usecases += "\n"

	if scenarios_is_empty:
		usecases += "There are no usecases listed."

	# End subsection
	usecases += "\n"
	return usecases

def generate_formalization(g):
	# Create Header
	formalization = generate_header("Formalization")
	# Begin Content Generation
	hC = get_predicate("opla-sd", "hasConnections", g)
	connections = None

	# There should only ever be one of these
	for s, p, o in g.triples((None, hC, None)):
		connections = str(o)

	axioms = list()
	lines = o.split("\n")
	for line in lines:
		s, p, o = line.strip().split(" ")

		# Write Scoped Range
		lhs = tsf(s)
		rhs = forall + tsf(p + "." + o)
		scoped_range = lhs + sc + rhs
		axioms.append(scoped_range)

		# Write Scoped Domain
		lhs = exists + tsf(p + "." + s)
		rhs = tsf(o)
		scoped_domain = lhs + sc + rhs
		axioms.append(scoped_domain)

	formalization += "\\subsubsection{Axioms}\n"
	formalization += "\\begin{align}\n"
	for axiom in axioms:
		formalization += "  " + axiom + "\\\\\n"
	formalization += "\\end{align}\n"

	formalization += "\\subsubsection{Explanations}\n"
	formalization += "\\begin{align}\n"
	
	formalization += "\\end{align}"

	# End subsection
	formalization += "\n"
	return formalization

def generate_submodules(g):
	# Create Header
	submodules = generate_header("Submodules")
	# Begin Content Generation
	pass
	# End subsection
	submodules += "\n"
	return submodules

def generate_views(g):
	# Create Header
	views = generate_header("Views")
	# Begin Content Generation
	pass
	# End subsection
	views += "\n"
	return views

def generate_entanglements(g):
	# Create Header
	entanglements = generate_header("Entanglements")
	# Begin Content Generation
	pass
	# End subsection
	entanglements += "\n"
	return entanglements

def generate_examples(g):
	# Create Header
	examples = generate_header("Examples")
	# Begin Content Generation
	examples += "\\begin{verbatim}\n"
	examples += "Example Triples\n"
	examples += "\\end{verbatim}"
	# End subsection
	examples += "\n"
	return examples

# ======================
# Set up
section_generators = [generate_overview, generate_cqs, generate_usecases, generate_formalization, generate_submodules, generate_views, generate_entanglements, generate_examples]
section_names = ["overview", "cqs", "usecases", "formalization", "submodules", "views", "entanglements", "examples"]
section_generator_map = {key:value for (key, value) in zip(section_names, section_generators)}
# ======================

def generate_documentation(section_order, filename):
	g = rdflib.Graph()
	g.parse(filename, format="ttl")

	documentation = ""
	for section in section_order:
		documentation += section_generator_map[section](g) + "\n"

	with open("../documentation/documentation.tex", "w") as output:
		output.write(documentation)
		output.write("%"*35+"\n")
		output.write("%"*11 + " End Section "+ "%"*11+"\n")
		output.write("%"*35+"\n")
		
section_order = ["overview", "cqs", "usecases", "formalization", "submodules", "views", "entanglements", "examples"]

generate_documentation(section_order, "../patterns/causal_event_pattern.ttl")