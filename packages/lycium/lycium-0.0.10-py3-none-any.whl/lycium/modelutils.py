#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bson import ObjectId
import datetime
import mongoengine
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()

def model_columns(model):
    if isinstance(model, mongoengine.Document) or hasattr(model, '_reverse_db_field_map'):
        columns = [k for k in model._fields]
        pk = model._reverse_db_field_map.get('_id')
        return columns, pk
    columns = []
    pk = None
    cls_ = model._sa_class_manager.class_
    ref = model._sa_class_manager.deferred_scalar_loader.args[0]
    colmaps = {}
    for k in model._sa_class_manager._all_key_set:
        c = getattr(cls_, k)
        colmaps[c.expression.key] = c.key
    tbl = None
    if ref.primary_key:
        pk = colmaps[ref.primary_key[0].name]
    for t in ref.tables:
        if t.name == ref.local_table.name:
            tbl = t
            break
    if tbl is not None:
        for k in tbl.columns._all_columns:
            columns.append(colmaps[str(k.key)])
    else:
        for k in model._sa_class_manager._all_key_set:
            columns.append(str(k))
    return columns, pk

def format_mongo_value(v):
    if isinstance(v, ObjectId):
        return str(v)
    elif isinstance(v, mongoengine.Document):
        return {f: format_mongo_value(getattr(v, f)) for f in v}
    elif isinstance(v, datetime.datetime):
        return str(v)
    return v

MODEL_DB_MAPPING = {}
DEFAULT_SKIP_FIELDS = {'obsoleted':True, 'created_at':True, 'updated_at':True, 'created_by':True, 'updated_by':True}

def get_dbinstance_by_model(modelName):
    if modelName in MODEL_DB_MAPPING:
        return MODEL_DB_MAPPING[modelName]
    return ''
