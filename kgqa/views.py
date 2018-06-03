import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from py2neo import Graph, authenticate
from kgqa.KB_query import query_main

# Create your views here.
def index_post(request):
    return render(request, "index.html")
def search_post(request):
    return render(request, "post_from_base.html")
def content_post(request):
    ctx = {}
    if request.POST:
        question = request.POST['q']
        ctx['rlt'] = query_main.query_function(question)
        print(ctx['rlt'])
        ctx['q']=question
        print(ctx['q'])
    return render(request, "con_from_base.html", ctx)
def temp_post(request):
    return render(request, "temp_from_base.html")

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "XXXX")
# connect to authenticated graph database
graph = Graph("http://localhost:7474/db/data/")

def cyNeo4j_post(request):
    return render(request, "cytoscape_neo4j.html")


def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)
    return {"data": data}


def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id),
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}
    return {"data": data}


def ghJson_post(request):
    nodes = list(map(buildNodes, graph.cypher.execute('MATCH (n) RETURN n')))
    edges = list(map(buildEdges, graph.cypher.execute('MATCH ()-[r]->() RETURN r')))
    elements = {"nodes": nodes, "edges": edges}
    return HttpResponse(json.dumps(elements, ensure_ascii=False), content_type="application/json")
    #return JsonResponse(elements,safe=False)