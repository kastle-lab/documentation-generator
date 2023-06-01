import os
import shutil

import pandas as pd
import rdflib

from manchester_translation import axiom_translation

# =======================
# Generation of common elements in subsections
def generate_label(label):
    label = label.replace(" ", "-").lower()

    return label


def generate_header(section_name, label=None):
    if label is None:
        label = generate_label(section_name)

    header = "%"*35 + "\n"
    header += "\\subsection{" + section_name + "}\n"
    header += "\\label{ssec:" + label + "}\n"
    header += "%"*10 + "\n"

    return header

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
# Generate figure code
def generate_figure_code(filename, caption="Empty Caption", label=None):
    # Create filename path
    # filename = "{resources/" + filename + "}"
    # Generate the label
    if label == None:
        print("No label for figures")
        return 
    if label.startswith("fig:"):
        label = label.replace("fig:", "")
    label = "{fig:" + label + "}"
    # Wrap Caption
    caption = "{" + caption + "}"
    filename = "{" + filename + "}"
    # Construct figure code
    figure_lines = list()
    figure_lines.append("\\begin{figure}[h!]")
    figure_lines.append("  \\begin{center}")
    figure_lines.append(
        "    \\includegraphics[width=\\textwidth]{}".format(filename))
    figure_lines.append("  \\end{center}")
    figure_lines.append("  \\caption{}".format(caption))
    figure_lines.append("  \\label{}".format(label))
    figure_lines.append("\\end{figure}\n")
    # Separate by new lines
    figure = '\n'.join(figure_lines)
    # And return
    return figure


def generate_preamble(contributors, acknowledgement):
    preamble_start = """\\setlrmarginsandblock{1in}{1in}{*}
\\setulmarginsandblock{1in}{1in}{*}
\\checkandfixthelayout

\\usepackage{graphicx}

\\usepackage{enumerate,xcolor,soul,framed}

\\usepackage{mathtools,amssymb}
\\allowdisplaybreaks[1]
\\usepackage{url}
\\usepackage{paralist}
\\usepackage{hyperref}
\\usepackage{parskip}
\\tightlists

\\usepackage{textcomp}
\\usepackage[T1]{fontenc}
\\usepackage{palatino}
\\linespread{1.025}
\\let\\oldtextlangle\\textlangle
\\renewcommand{\\textlangle}{{\\fontfamily{pxr}\\selectfont\\oldtextlangle}}
\\let\\oldtextrangle\\textrangle
\\renewcommand{\\textrangle}{{\\fontfamily{pxr}\\selectfont\\oldtextrangle}}


\\setverbatimfont{\\sffamily}

\\renewcommand{\\theequation}{\\arabic{equation}}

\\newlength{\\drop}% for my convenience
\\newcommand*{\\titleBWF}{\\begingroup
\\drop = 0.1\\textheight
\\parindent=0pt
\\vspace*{\\drop}
{\\Huge\\bfseries KnowWhereGraph Ontology: Fast Forward Through Data Acquisition and Integration}\\\\
[\\baselineskip]

\\vspace*{0.5\\drop}
{\\Large {\itshape Contributors:}}\\\\\n"""
    # Sort the contributors by space delineated last name
    # Hopefully no one has two last names
    contributors = list(contributors)

    def getKey(item):
        return item.split(" ")[-1]
    contributors = sorted(contributors, key=getKey)
    # Write the contributors
    preamble_contributors = ""
    for contributor in contributors:
        preamble_contributors += "{\\large{\\scshape ~}}\\\\\n".replace(
            "~", contributor)
    preamble_contributors = preamble_contributors[:-1] + "[\\baselineskip]\n\n"
    preamble_date = """{\\large {\\itshape Document Date:} \\today}

\\vfill\n\n"""
    preamble_end = """\\endgroup}

\\setsecnumdepth{subsubsection}
\\maxtocdepth{section}
\\chapterstyle{tandh}
\\pagestyle{simple}"""
    
    preamble_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../kwg_documentation/preamble.tex"))
    with open(preamble_path, "w") as output:
        preamble = preamble_start + preamble_contributors + preamble_date
        preamble += "{" + acknowledgement + "}\n\n" + preamble_end
        output.write(preamble)


def generate_overview(g, row):
    # Create Header
    overview = generate_header("Overview")

    # Begin Content Generation
    # =======================
    # Insert Overview Text
    overview += row["description"]
    overview += "\nI am the overview.\n"

    # End Overview Text
    # =======================
    # Insert top level schema Diagram
    # Find if there is a schema diagram
    # get node representing this ontology
    # TODO: this currently assumes there is only 1 schema diagram
    schema_diagram = row["figure_path"]
    if len(schema_diagram) == 0:
        return overview

    filename = str(schema_diagram)
    pattern_name = row["dataset_name"]
    caption = f"The schema diagram for the {pattern_name}."
    figure_code = generate_figure_code(filename, caption, label="ov-diagram")
    overview += "\n" + figure_code

    # End subsection
    overview += "\n"
    return overview


def find_ttl_files(directory, ignore_root=True):
    """
    Returns a list of all files with the .ttl extension found in the
    given directory and its subdirectories.
    """
    ttl_files = []
    for root, dirs, files in os.walk(directory):
        if ignore_root:
            ignore_root = False
            continue
        for file in files:
            if file.endswith('.ttl'):
                ttl_files.append(os.path.join(root, file))
    return ttl_files


def get_info_df(directory, ignore_root=True):
    """
    Returns a Dataframe of all required info for documentation found in the
    given directory and its subdirectories.
    """
    output_df = pd.DataFrame(
        columns=["dataset_name", "ttl_path", "figure_path", "description"])
    for root, dirs, files in os.walk(directory):
        if ignore_root:
            ignore_root = False
            continue

        # Capture Dataset Name
        dataset_name = ' '.join(elem.capitalize()
                                for elem in root.split("/")[-1].split("-"))

        # Capture Dataset description
        dataset_dscription = ""

        for file in files:
            # Capture Dataset ttl file path
            if file.endswith('.ttl'):
                ttl_path = os.path.join(root, file)

            # Capture Dataset figure file path
            if file.endswith('.png'):
                resource_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../kwg_documentation/resources/"))
                figure_path = os.path.join(root, file)
                shutil.copy(figure_path, resource_dir)
                figure_path = os.path.join(
                    "/".join(resource_dir.split("/")[-1:]), file)

        output_dict = {"dataset_name": dataset_name, "ttl_path": ttl_path,
                       "figure_path": figure_path, "description": dataset_dscription}
        output_df = pd.concat(
            [output_df, pd.DataFrame([output_dict])], ignore_index=True)

    return output_df


def generate_pattern_documentation(section_order, output_path, row):
    g = rdflib.Graph()
    g.parse(row["ttl_path"], format="ttl")

    pattern_name = row["dataset_name"]

    documentation = ""
    for section in section_order:
        documentation += section_generator_map[section](g, row) + "\n"

    with open(output_path, "a") as output:
        output.write("%"*35+"\n")
        output.write("\\section{" + pattern_name + "}\n")
        output.write("\\label{sec:" + generate_label(pattern_name) + "}\n")
        output.write(documentation)
        output.write("%"*35+"\n")
        output.write("%"*11 + " End Section " + "%"*11+"\n")
        output.write("%"*35+"\n")
        output.write("\n")


def generate_all_documentation(directory, output_path):
    # Get all the patterns from the provided directory
    patterns = get_info_df(directory, ignore_root=True)

    # Nuke the previous contents of the file
    with open(output_path, "w") as output:
        output.write("\\chapter{Modules}\n")
        output.write("\\label{sec:mods}\n")
        output.write("%"*35+"\n")
        output.write(
            "We list the individual modules of the ontology, together with their axioms and explanations thereof. Each axiom is listed only once (for now), i.e. some axioms pertaining to a module may be found in the axiom set listed for an earlier listed module. Schema diagrams are provided throughout, but the reader should keep in mind that while schema diagrams are very useful for understanding an ontology \\cite{odp-documentation}, they are also inherently ambiguous.")
        output.write("\n\n")
    # Hardcoded info for now
    acknowledgement = "This work was supported by The National Science Foundation through the Award \\#2033521."
    # section_order = ["overview", "cqs", "usecases", "formalization", "submodules", "views", "entanglements", "examples"]
    section_order = ["overview", "formalization"]
    # section_order = ["formalization"]


    # Generate sections for the patterns and get contributors
    contributors = set()
    # for pattern in patterns:
    for i, row in patterns.iterrows():
        try:
            generate_pattern_documentation(section_order, output_path, row)
            print(row["dataset_name"], "Done.")
        except:
            print("ERROR reading file:", i, row["dataset_name"])
        # break
        # contributors.update(pattern_contributors)
    # Regenerate the preamble
    generate_preamble([], acknowledgement)

section_generators = [generate_overview, axiom_translation]
section_names = ["overview", "formalization"]
section_generator_map = {key:value for (key, value) in zip(section_names, section_generators)}

if __name__ == "__main__":

    output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../kwg_documentation/module.tex"))
    schema_root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../kwg-seed-graph/schemas/"))
    # output_path = "../kwg_documentation/module.tex"
    # schema_root_path = "../../kwg-seed-graph/schemas/"
    generate_all_documentation(schema_root_path, output_path)
