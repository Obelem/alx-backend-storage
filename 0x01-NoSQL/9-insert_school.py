#!/usr/bin/env python3
''' insert a document in python '''


def insert_school(mongo_collection, **kwargs):
    '''insert school'''
    document_id = mongo_collection.insert(kwargs)
    return document_id
