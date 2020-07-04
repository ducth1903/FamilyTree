from django.shortcuts import render
# from django.http import HttpResponse
import json
import os
import pathlib

# reference from root, i.e. Family_tree/django_family_tree
with open('tree/treeData/flat_data_noi.json', 'r') as inJson:
    flat_tree_json = json.load(inJson)

with open('tree/treeData/flat_member_data_noi.json', 'r') as inMemberJson:
    flat_member_json = json.load(inMemberJson)

with open('tree/treeData/tree_structure_noi.json', 'r') as inTreeStructure:
    tree_structure_json = json.load(inTreeStructure)

# Ngoai data
with open('tree/treeData/flat_data_ngoai.json', 'r') as inJson:
    flat_tree_ngoai_json = json.load(inJson)

with open('tree/treeData/flat_member_data_ngoai.json', 'r') as inMemberJson:
    flat_member_ngoai_json = json.load(inMemberJson)

with open('tree/treeData/tree_structure_ngoai.json', 'r') as inTreeStructure:
    tree_structure_ngoai_json = json.load(inTreeStructure)

# Create your views here.
def index(request):
    global flat_tree_json
    flat_tree_json = __process_blank_img(flat_tree_json)

    context = {
        'flat_tree_json': flat_tree_json,
        'tree_structure_json': tree_structure_json,
        'isNoi': 'yes',
    }
    return render(request, 'tree/index.html', context)

def ngoai(request):
    global flat_tree_ngoai_json
    flat_tree_ngoai_json = __process_blank_img(flat_tree_ngoai_json)

    context = {
        'flat_tree_json': flat_tree_ngoai_json,
        'tree_structure_json': tree_structure_ngoai_json,
        'isNoi': None,
    }
    return render(request, 'tree/index.html', context)

def displayMember(request, memberName):
    global flat_member_json, flat_tree_ngoai_json
    # Check if origin of request sent from noi/ or ngoai/ url
    # Append this to "Back to Tree" button so can go back to the corresponding tree
    origin = request.META['HTTP_REFERER']
    origin = origin.replace("//", "")
    origin = origin.split('/')[1].strip()
    origin = origin if origin else None

    if memberName in flat_member_json:
        member_json = flat_member_json
    if memberName in flat_member_ngoai_json:
        member_json = flat_member_ngoai_json
    member_json = __process_blank_img(member_json)
    
    context = {
        'memberName': memberName,
        'member_detail_json': member_json[memberName],
        'origin': origin
    }
    return render(request, 'tree/member.html', context)

def __process_blank_img(json_obj):
    # Process flat_tree_json: replace image path to blank.jpg 
    # if image does not exist
    # NOTE: while deploying to Heroku, there is a glitch that capitalize .jpg to .JPG for some images only 
    for k,v in json_obj.items():
        if 'wife_img' in v:
            img_jpg = v['wife_img']
            img_jpg_split = img_jpg.split('.')
            img_JPG = '.'.join( [img_jpg_split[0], img_jpg_split[1].upper()] )
            if os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_jpg}")):
                pass
            elif os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_JPG}")):
                v['wife_img'] = img_JPG
            else:
                v['wife_img'] = 'blank.png'

        if 'husband_img' in v:
            img_jpg = v['husband_img']
            img_jpg_split = img_jpg.split('.')
            img_JPG = '.'.join( [img_jpg_split[0], img_jpg_split[1].upper()] )
            if os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_jpg}")):
                pass
            elif os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_JPG}")):
                v['husband_img'] = img_JPG
            else:
                v['husband_img'] = 'blank.png'

        # flat_member_json
        if 'img' in v:
            img_jpg = v['img']
            img_jpg_split = img_jpg.split('.')
            img_JPG = '.'.join( [img_jpg_split[0], img_jpg_split[1].upper()] )
            if os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_jpg}")):
                pass
            elif os.path.exists(os.path.join(os.getcwd(), f"tree/static/tree/img/members/{img_JPG}")):
                v['img'] = img_JPG
            else:
                v['img'] = 'blank.png'
    return json_obj