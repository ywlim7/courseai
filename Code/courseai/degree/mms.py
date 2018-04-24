import json

from django.http import JsonResponse

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


def get_mms_data(code):
    if len(code) <= 5:
        return JsonResponse({"error": "Input length insufficient"})

    if code[-4:] == "-MAJ":
        return get_major_data(code[:-4])

    if code[-4:] == "-MIN":
        return get_minor_data(code[:-4])

    if code[-5:] == "-SPEC":
        return get_spec_data(code[:-5])

    return JsonResponse({"error": "code must end with -MAJ, -MIN or -SPEC"})


def get_major_data(code):
    client = Elasticsearch()
    response = Search(using=client, index='majors').query("match",
                                                          code=code).execute().to_dict()  # the to_dict() works like magic

    responses = response['hits']['hits']
    if not responses:
        return JsonResponse({})

    res = responses[0]['_source']

    return JsonResponse(res)


def get_minor_data(code):
    client = Elasticsearch()
    response = Search(using=client, index='minors').query("match",
                                                          code=code).execute().to_dict()  # the to_dict() works like magic

    responses = response['hits']['hits']
    if not responses:
        return JsonResponse({})

    res = responses[0]['_source']

    return JsonResponse(res)


def get_spec_data(code):
    client = Elasticsearch()
    response = Search(using=client, index='specialisations').query("match",
                                                                   code=code).execute().to_dict()  # the to_dict() works like magic

    responses = response['hits']['hits']
    if not responses:
        return JsonResponse({})

    res = responses[0]['_source']

    return JsonResponse(res)
