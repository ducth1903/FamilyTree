from django.shortcuts import render
# from django.http import HttpResponse
import json
import os
import pathlib

# reference from root, i.e. Family_tree/django_family_tree
with open('tree/treeData/flat_data.json', 'r') as inJson:
    flat_tree_json = json.load(inJson)

with open('tree/treeData/flat_member_data.json', 'r') as inMemberJson:
    flat_member_json = json.load(inMemberJson)

with open('tree/treeData/tree_structure.json', 'r') as inTreeStructure:
    tree_structure_json = json.load(inTreeStructure)

# Create your views here.
def index(request):
    global flat_tree_json
    flat_tree_json = __process_blank_img(flat_tree_json)

    context = {
        'flat_tree_json': flat_tree_json,
        'tree_structure_json': tree_structure_json,
    }
    return render(request, 'tree/index.html', context)

def displayMember(request, memberName):
    global flat_member_json
    flat_member_json = __process_blank_img(flat_member_json)

    context = {
        'memberName': memberName,
        'member_detail_json': flat_member_json[memberName]
    }
    return render(request, 'tree/member.html', context)

def __process_blank_img(json_obj):
    # Process flat_tree_json: replace image path to blank.jpg 
    # if image does not exist
    for k,v in json_obj.items():
        if 'wife_img' in v and not os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{v['wife_img']}")):
            v['wife_img'] = 'blank.png'
        if 'husband_img' in v and not os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{v['husband_img']}")):
            v['husband_img'] = 'blank.png'

        # flat_member_json
        if 'img' in v and not os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{v['img']}")):
            v['img'] = 'blank.png'
    return json_obj