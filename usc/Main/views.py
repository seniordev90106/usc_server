from threading import Thread
from typing import Union

from CFR.models import CFRNode, CFRNodeManager
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from USCODE.models import Node, NodeManager
from utils.ai_query import ai_query

QA = "QA"


@cache_page(5)
def index(request):
    """Show collections available"""
    context = {
        "collections": [
            {
                "name": "CFR - Code of Federal Regulations",
                "code": settings.CFR,
            },
            {
                "name": "USCS - United States Code Service",
                "code": settings.USCODE,
            },
        ]
    }

    return render(request, 'Main/index.html', context)


def make_qa(query: str):
    return ai_query(query).lstrip("?")


def get_qa(query, datax: dict):
    qa = make_qa(query)
    datax["qa"] = qa


def get_cfr(query, datax: dict):
    cfr_results = CFRNode.objects.full_text_search(query)
    datax["cfr"] = cfr_results


def get_usc(query, datax: dict):
    usc_results = Node.objects.full_text_search(query)
    datax["usc"] = usc_results


def full_text_search(request):
    """Full text search for collections
    """

    query = request.GET.get("search")
    collection = request.GET.get("collection")

    context = {}

    if query:

        if collection == '':

            datax = {
                "usc": None,
                "cfr": None,
                "qa": None
            }

            # Run all searches in parallel
            threads = (
                Thread(target=get_qa, args=(query, datax)),
                Thread(target=get_cfr, args=(query, datax)),
                Thread(target=get_usc, args=(query, datax)),
            )

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()


            usc_results = datax["usc"]
            cfr_results = datax["cfr"]
            qa = datax["qa"]

            # Combine results of separate model arranged 5 each in a list
            results = []
            for i in range(0, max(len(usc_results), len(cfr_results)), 5):
                results.extend(usc_results[i:i+5])
                results.extend(cfr_results[i:i+5])

            context = {
                "nodes": results,
                "qa": qa
            }

        elif collection == QA:
            context = {
                "qa": make_qa(query)
            }

        else:
            COLLECTION: dict[str, Union[NodeManager, CFRNodeManager]] = {
                settings.USCODE: Node.objects,
                settings.CFR: CFRNode.objects,
            }

            main = COLLECTION.get(collection)
            if main:
                context['nodes'] = main.full_text_search(query)

    return render(
        request,
        "Main/search.html",
        context
    )
