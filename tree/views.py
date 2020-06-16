from django.shortcuts import render
# from django.http import HttpResponse
import json
import os

# Create your views here.
def index(request):
    # reference from root, i.e. Family_tree/django_family_tree
    with open('tree/treeData/flat_ngoai_data.json', 'r') as inJson:
        flat_json = json.load(inJson)

    context = {
        'flat_json': flat_json
    }
    return render(request, 'tree/index.html', context)