# Generate tree_structure.json from DB into treeData/
# Example of working tree_structure.json
# {
#     "chart": {
#         "container": "#tree-simple",
#         "hideRootNode": true,
#         "connectors": {"type": "step"},
#         "siblingSeparation": 70,
#         "levelSeparation": 50,
#         "nodeAlign": "TOP"
#     },
#     "nodeStructure": {
#         "text": { "name": "Root node" },
#         "children": [
#             {
#                 "id": 0,
#                 "innerHTML": "generateInnerHTML('Pham Thi Hoa Ly', 'Nguyen Tu', '0')",
#                 "children": [
#                     {   
#                         "innerHTML": "generateInnerHTML('Nguyen Hong Hoa', 'Tran Dac Xuan', '0.0')",
#                         "children": [
#                             {
#                                 "innerHTML": "generateInnerHTML('Tran Hong Duc', 'N/A', '0.0.0')"
#                             },
#                             {
#                                 "innerHTML": "generateInnerHTML('Tran Hong Hai', 'N/A', '0.0.1')"
#                             }
#                         ]
#                     },
#                     {   
#                         "innerHTML": "generateInnerHTML('Nguyen Tung Hoa', 'Ngo Trung Son', '0.1')",
#                         "children": [
#                             {
#                                 "innerHTML": "generateInnerHTML('Ngo Tung', 'Ngoc', '0.1.2')"
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ]
#     }
# }

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from tree.models import Couple
import json

# Following Treant.js format
tree_structure_json = {
    "chart": {
        "container": "#tree-simple",
        "hideRootNode": True,
        "connectors": {"type": "step"},
        "siblingSeparation": 70,
        "levelSeparation": 50,
        "nodeAlign": "TOP"
    },
    
    "nodeStructure": {
        "text": { "name": "Root node" }
    }
}

class Command(BaseCommand):
    help = 'Generate tree_structure.json'

    def add_arguments(self, parser):
        # To use debug, do: "python manage.py genTreeStructure -debug"
        parser.add_argument('-debug', action='store_true')

    def handle(self, *args, **options):
        debug = options['debug']
        # Initialize
        tree_children_list = []
        visited_id = set()
        stack = []

        all_column_names = [field.name for field in Couple._meta.get_fields()]
        all_parent_id = set(filter(None, set(Couple.objects.values_list('parent_id', flat=True))))      # get set of all parent id and remove None value
        all_id = set(Couple.objects.values_list('id', flat=True))
        # print(all_parent_id, all_id)

        # --------------------------------
        # tree_structure.json
        # --------------------------------
        # First loop over all couples
        # Try to fill the tree as much as possible, except those do not see parent in the tree yet
        for curr_couple in Couple.objects.all():
            curr_parentId = curr_couple.parent_id
            # Potential string error here!
            curr_node_out = {
                "id": curr_couple.id,
                "innerHTML": f"generateInnerHTML('{curr_couple.wife_name if curr_couple.wife_name else 'N/A'}', '{curr_couple.husband_name if curr_couple.husband_name else 'N/A'}', '{curr_couple.id}')",
                "children": []
            }
            if curr_parentId not in all_parent_id:
                # Must be root
                tree_children_list.append( curr_node_out )
            elif (curr_parentId in all_parent_id) and (curr_parentId not in visited_id):
                # Parent exists but not yet added to the tree
                # -> push this node to the stack and will revisit after its parent is added
                stack.append( (curr_couple.id, curr_parentId, curr_node_out) )
                continue
            else:
                # Parent exists and is added to the tree
                # -> traverse to add this node under its parent
                if debug: print(f'\nStart... {curr_couple} | {curr_parentId}')
                self.__utilBFS__(curr_node_out, curr_parentId, tree_children_list, set())
                if debug: print(f'End... {tree_children_list}')
                
            visited_id.add(curr_couple.id)
        
        # Second loop to fill the remaining nodes that did not see its parent before
        for node_id, node_parentId, node_out in stack:
            self.__utilBFS__(node_out, node_parentId, tree_children_list, set())
        
        if debug: print(f'\nFinal tree structure:\n{tree_children_list}')

        # Adding final result to tree_structure_json and save to treeData/tree_structure.json
        tree_structure_json["nodeStructure"]["children"] = tree_children_list
        with open("tree/treeData/tree_structure.json", 'w') as outFile:
            json.dump(tree_structure_json, outFile)



        # --------------------------------
        # flat_data.json
        # Adding new field: 
        #   - wife_name_norm and husband_name_norm
        #   - wife_img and husband_img: <name_norm>.jpg
        # --------------------------------
        flat_data_json = {}
        for curr_couple in Couple.objects.all():
            flat_data_json[f"{curr_couple.id}"] = {}
            for col in all_column_names:
                if col != 'id':
                    if col=='wife_name' and curr_couple.wife_name:
                        flat_data_json[f"{curr_couple.id}"]["wife_name_norm"] = ''.join( curr_couple.wife_name.lower().split() )
                        flat_data_json[f"{curr_couple.id}"]["wife_img"] = f"{''.join( curr_couple.wife_name.lower().split() )}.jpg"
                    elif col=='husband_name' and curr_couple.husband_name:
                        flat_data_json[f"{curr_couple.id}"]["husband_name_norm"] = ''.join( curr_couple.husband_name.lower().split() )
                        flat_data_json[f"{curr_couple.id}"]["husband_img"] = f"{''.join( curr_couple.husband_name.lower().split() )}.jpg"

                    flat_data_json[f"{curr_couple.id}"][col] = getattr(curr_couple, col)
        with open("tree/treeData/flat_data.json", 'w') as outFile:
            json.dump(flat_data_json, outFile, cls=DjangoJSONEncoder)



        # --------------------------------
        # flat_member_data.json
        # --------------------------------
        doneFirst = False
        flat_member_data_json = {}
        for key, value in flat_data_json.items():
            if not doneFirst:
                all_cols = value.keys()
                all_cols_short = ['_'.join(c.split('_')[1:]) for c in all_cols if "wife_" in c]
                doneFirst = True

            if "wife_name_norm" in value:
                all_cols_short_v = [value[f"wife_{c}"] for c in all_cols_short]
                flat_member_data_json[f"{value['wife_name_norm']}"] = {k:v for (k,v) in zip(all_cols_short, all_cols_short_v)}
            
            if "husband_name_norm" in value:
                all_cols_short_v = [value[f"husband_{c}"] for c in all_cols_short]
                flat_member_data_json[f"{value['husband_name_norm']}"] = {k:v for (k,v) in zip(all_cols_short, all_cols_short_v)}
        with open("tree/treeData/flat_member_data.json", 'w') as outFile:
            json.dump(flat_member_data_json, outFile, cls=DjangoJSONEncoder)



    def __utilBFS__(self, childNode, parentId, tree, visited_bfs):
        for st in tree:
            if st["id"]==parentId:
                st["children"].append(childNode)
            elif st["id"] not in visited_bfs:
                visited_bfs.add(st["id"])
                self.__utilBFS__(childNode, parentId, st["children"], visited_bfs)