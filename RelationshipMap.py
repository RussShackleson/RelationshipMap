from graphviz import Source
from pyexcel_ods import get_data
import ast
import json
import sys


#https://www.graphviz.org/doc/info/shapes.html
entity_shapes = {
	"Place":"house",
	"Business":"diamond",
	"Non-Profit":"box",
	"Government Org":"pentagon",
	"Government Official":"triangle",
	"Civilian":"egg",
	"School":"box"
}

def create_entity_type_template(rel_list):
	template = ""
	entities = []
	for line in rel_list:
		entities.append(line[0].strip())
		entities.append(line[2].strip())
	uniq_entities = set(entities)
	for e in uniq_entities:
		ret, entity = get_entity_type(e, entity_lookup)
		if ret:
			shape = entity_shapes.get(entity)
			template = template + "\"{0}\" [shape={1}, fontsize=8]; \n".format(e, shape)
		else:
			print("Failed to process: {0}".format(e))
	return template

def create_diagraph(relationship_list):
	diagraph_header = """digraph {
	"""
	diagraph_footer = "}"
	output = diagraph_header
	e_template = create_entity_type_template(rel_list)
	output = output + e_template
	for entity in relationship_list:
			src_entity = entity[0]
			rel = entity[1]
			tgt_entity = entity[2]
			entry = "\"{0}\" -> \"{1}\"[label=\"{2}\",fontsize=6];\n".format(src_entity.strip(), tgt_entity.strip(), rel.strip())
			output = output + entry
	output = output + diagraph_footer
	print(output)
	s = Source(output, format="png")
	s.view()

def create_entity_dict(ods_rel):
	dump = load_ods_file(ods_rel)
	entity_type_dict = string_to_dict(dump)
	print(entity_type_dict)
	cells = entity_type_dict['EntityTypes']
	entity_type_lookup = {}
	itercells = iter(cells)
	next(itercells)
	for cell in itercells:
		entity_type_lookup[cell[0].strip()] = cell[1].strip()
	return entity_type_lookup

def create_rel_list(ods_rel):
	out = load_ods_file(ods_rel)
	rel_dict = string_to_dict(out)
	rel_list = rel_dict["EntityRelationships"]
	iterrel = iter(rel_list)
	next(iterrel)
	return list(iterrel)

def load_ods_file(ods_file):	
	data = get_data(ods_file)
	dump = json.dumps(data)
	return dump

def string_to_dict(dict_str):
	return ast.literal_eval(dict_str)

def get_entity_type(entity, entity_lookup):
	entity = entity_lookup.get(entity)
	if entity:
		return True, entity
	else:
		return False, "get_entity_type(): Entity Lookup Error"

if __name__== "__main__":
	ods_rel = sys.argv[1]
	entity_lookup = create_entity_dict(ods_rel)
	rel_list = create_rel_list(ods_rel)
	create_diagraph(rel_list)