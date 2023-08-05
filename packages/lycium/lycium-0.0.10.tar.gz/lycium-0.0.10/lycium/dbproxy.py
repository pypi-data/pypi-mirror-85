#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import re
import six
import sys
import traceback
import sqlalchemy
from sqlalchemy.orm import query, loading, attributes
from sqlalchemy_aio import ASYNCIO_STRATEGY
import sqlalchemy.databases as supported_engines
# from sqlalchemy.orm import sessionmaker
import motor.motor_tornado
import motor
import tornado.gen
from tornado.ioloop import IOLoop

# from tornado.ioloop import IOLoop
# target_module = __import__('tornado.concurrent')
# if not hasattr(target_module.concurrent, 'return_future'):
#     setattr(target_module.concurrent, 'return_future', tornado.gen.coroutine)
# from motorengine import connect as mongo_connect
import mongoengine
import pymongo

try:
    import pymysql
except ImportError:
    pass
try:
    import pymssql
except ImportError:
    pass

try:
    import cx_Oracle
except ImportError:
    cx_Oracle = {}

try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass


from .supports import singleton
from .modelutils import model_columns, format_mongo_value, get_dbinstance_by_model, DEFAULT_SKIP_FIELDS
from .utilities import url_encode
from .exceptionreporter import ExceptionReporter

LOG = logging.getLogger('components.dbproxy')

@singleton
class DbProxy(object):
    """
    database agent component
    """
    def __init__(self):
        self.db_instances = {}
        self.db_engines = {}
        self.default_mongo_db_instance = None
        self.default_rdbms_db_instance = None
        self._motor_count_documents_name = 'count_documents'

        if hasattr(motor.MotorCollection, 'count'):
            self._motor_count_documents_name = 'count'

        self._cur_execution_dbinstances = []

    def setup_rdbms(self, rdbms_configs: dict) -> bool:
        for k, dbconf in rdbms_configs.items():
            self.setup_rdbms_connection(k, dbconf)

    def setup_mongodbs(self, mongodb_configs: dict) -> bool:
        for k, dbconf in mongodb_configs.items():
            self.setup_mongodb_elenment(k, dbconf)

    def setup_rdbms_connection(self, category: str, dbconf: dict) -> bool:
        engine = dbconf.get('connector', '')
        if engine not in supported_engines.__all__:
            return False
        if category.startswith('ignore'):
            return False

        create_engine_params = {
            "encoding": dbconf.get('encoding', 'utf8'),
            "pool_pre_ping": True, 
            "strategy": ASYNCIO_STRATEGY
        }
        if 'connect_args' in dbconf:
            create_engine_params["connect_args"] = dbconf['connect_args']
        conndsn = self.format_connection_string(dbconf)
        db_engine = sqlalchemy.create_engine(conndsn, **create_engine_params)

        db_conn = IOLoop.current().run_sync(db_engine.connect)
        self.db_instances[category] = db_conn
        if not self.default_rdbms_db_instance:
            self.default_rdbms_db_instance = db_conn

        # syncronized connection
        self.db_engines[category] = sqlalchemy.create_engine(conndsn, 
            encoding=dbconf.get('encoding', 'utf8'),
            pool_pre_ping=True)

        return True

    def setup_mongodb_elenment(self, category: str, dbconf: dict) -> bool:
        if category.startswith('ignore'):
            return False
        conndsn = self.format_connection_string(dbconf)
        mongo_cli = motor.motor_tornado.MotorClient(conndsn)
        mongo_db = mongo_cli[dbconf.get('db')]
        if not self.default_mongo_db_instance:
            self.default_mongo_db_instance = mongo_db
        self.db_instances[category] = mongo_db
        return True
    
    def format_connection_string(self, dbconf: dict) -> str:
        engine = dbconf.get('connector', 'mysql')
        user = dbconf.get('user', 'guest')
        pwd = dbconf.get('pwd', '')
        host = dbconf.get('host', 'localhost')
        port = int(dbconf.get('port', 3306))
        dbname = dbconf.get('db', 'guest')
        driverpart = dbconf.get('driver', '')
        if driverpart:
            driverpart = '+' + driverpart

        connection_str = ''
        if engine == 'oracle':
            if sys.platform == 'darwin':
                connection_str = "oracle://%s:%s@%s:%d/%s" % (url_encode(user), url_encode(pwd), host, port, dbname)
            else:
                ora_dsn = cx_Oracle.makedsn(host, port, service_name=dbname)
                connection_str = "oracle://%s:%s@%s" % (user, pwd, ora_dsn)
        else:
            connection_str = '%s%s://%s:%s@%s:%d/%s' % (engine, driverpart, url_encode(user), url_encode(pwd), host, port, dbname)

        return connection_str

    @tornado.gen.coroutine
    def exec_query(self, db_name, sql):
        """
        execute sql for orm dbs
        """
        ret_list = []
        if (not sql) or (db_name not in self.db_instances):
            return ret_list
        try:
            exec_result = yield self.db_instances[db_name].execute(sql)
            ret_list = yield exec_result.fetchall()
        except UnicodeDecodeError as e:
            LOG.error(traceback.format_exc())
            ExceptionReporter().report(key='SQL-'+str('query'), typ='SQL', 
                endpoint='%s|%s' % (str(db_name), str(sql)),
                method='QUERY',
                inputs=str(sql),
                outputs=str(ret_list),
                content=str(e),
                level='ERROR'
            )

        return ret_list

    @tornado.gen.coroutine
    def exec_update(self, db_name, sql):
        """
        execute sql for no back, update or insert
        """
        if (not sql) or (db_name not in self.db_instances):
            return False
        try:
            yield self.db_instances[db_name].execute(sql)
        except Exception as e:
            LOG.error(traceback.format_exc())
            ExceptionReporter().report(key='SQL-'+str('update'), typ='SQL', 
                endpoint='%s|%s' % (str(db_name), str(sql)),
                method='UPDATE',
                inputs=str(sql),
                outputs='',
                content=str(e),
                level='ERROR'
            )
            return False
        return True
    
    def call_procedure_oracle(self, db_name, proc_name, params, out_params=None):
        cur = self.db_engines[db_name].raw_connection().cursor()
        return_params = {}
        if out_params and isinstance(out_params, dict):
            for k, v in out_params.items():
                return_params[k] = cur.var(getattr(cx_Oracle, v))
            params.extend(return_params.values())
        if not isinstance(params, list):
            return False
        # 调用存储过程
        cur.callproc(proc_name, params)
        return {k:int(return_params[k].getvalue()) if out_params.get(k)=='NUMBER' and return_params[k].getvalue() is not None 
            else return_params[k].getvalue() for k in return_params}

    def get_mongo_dbinstance(self, model):
        return self.default_mongo_db_instance

    def get_model_dbinstance(self, model):
        modelName = str(model._sa_class_manager.class_.__name__)
        dbflag = get_dbinstance_by_model(modelName)
        if dbflag is None:
            return self.default_rdbms_db_instance
        if dbflag in self.db_instances:
            return self.db_instances[dbflag]
        else:
            LOG.error('query model:%s while could not determine the database instance', modelName)
        
        # return dbinstance
        return self.default_rdbms_db_instance

    # queries

    # common queries
    @tornado.gen.coroutine
    def query_list(self, model, filters, limit, offset, sort, direction, selections=None, joins=None):
        qry, dbinstance, columns, _ = self._format_rdbms_query(model, filters, sort, direction, joins=joins)
        
        total = yield self._execute_rdbms_query_count(dbinstance, qry)
        if not total:
            return [], total

        qry = qry.limit(limit).offset(offset)
        if selections:
            qry = qry.from_self(*selections)
        rows = yield self._execute_rdbms_result(dbinstance, qry, as_all=True)

        items = []
        if selections:
            for row in rows:
                item = {}
                for k in selections:
                    item[k.key] = row._row[row._keymap['anon_1_'+k.expression._key_label][2]]
                items.append(item)
        else:
            for row in rows:
                item = {}
                for k in columns:
                    if k in DEFAULT_SKIP_FIELDS:
                        continue
                    item[k] = row._row[row._keymap[getattr(model, k).expression._key_label][2]]
                items.append(item)

        return items, total

    def _format_rdbms_query(self, model, filters, sort, direction, joins=None):
        columns,pk = model_columns(model)
        dbinstance = self.get_model_dbinstance(model)
        orderby = None
        if sort:
            if direction == 'desc':
                orderby = sqlalchemy.desc(getattr(model, sort))
            else:
                orderby = sqlalchemy.asc(getattr(model, sort))
        elif (dbinstance.dialect.name == 'mssql' or dbinstance.dialect.name == 'postgresql'):
            if pk:
                orderby = getattr(model, pk)
            else:
                orderby = getattr(model, columns[0])
        
        qry = query.Query(model)
        if joins:
            for join in joins:
                qry = qry.join(*join)
        qry = qry.filter(*filters)
        if isinstance(orderby, list):
            qry = qry.order_by(*orderby)
        elif orderby is not None:
            qry = qry.order_by(orderby)
        return qry, dbinstance, columns, pk

    @tornado.gen.coroutine
    def query_list_mongo(self, model, filters, limit, offset, sort, direction, selections=None, joins=None):
        q = self._format_mongo_query(model, filters)
        if selections:
            selFields = {}
            for k in selections:
                selFields[k] = 1
            if selFields:
                q = q.fields(*selFields)
        if sort:
            if direction.lower() == 'desc':
                q = q.order_by('-'+sort)
            else:
                q = q.order_by(sort)
        if joins:
            # TODO
            pass

        collection = self._prepare_mongo_collection(model)
        total = yield getattr(collection, self._motor_count_documents_name)(q._query)

        q = q.skip(offset)

        cursor = collection.find(q._query)
        rows = yield cursor.to_list(length=limit)

        items = []
        if selections:
            for row in rows:
                item = {model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k: format_mongo_value(v) for k, v in row.items() if k in selections}
                items.append(item)
        else:
            for row in rows:
                item = {model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k: format_mongo_value(v) for k, v in row.items() if k not in DEFAULT_SKIP_FIELDS}
                items.append(item)
        
        return items, total

    @tornado.gen.coroutine
    def query_all_mongo(self, model, filters, limit=100, sort=None, **kwargs):
        direction = kwargs.pop('direction', None)
        selections = kwargs.pop('selections', None)
        joins = kwargs.pop('joins', None)
        as_dict = kwargs.pop('as_dict', True)
        q = self._format_mongo_query(model, filters)
        if selections:
            selFields = {}
            for k in selections:
                selFields[k] = 1
            if selFields:
                q = q.fields(*selFields)
        if sort:
            if direction.lower() == 'desc':
                q = q.order_by('-'+sort)
            else:
                q = q.order_by(sort)
        if joins:
            # TODO
            pass

        collection = self._prepare_mongo_collection(model)

        cursor = collection.find(q._query)
        rows = yield cursor.to_list(length=limit)

        items = []
        if as_dict:
            if selections:
                for row in rows:
                    item = {model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k: v for k, v in row.items() if k in selections}
                    items.append(item)
            else:
                for row in rows:
                    item = {model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k: v for k, v in row.items() if k not in DEFAULT_SKIP_FIELDS}
                    items.append(item)
        else:
            conditions = {}
            prepare_items = {}
            for row in rows:
                item = model()
                for k, v in row.items():
                    attr = model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k
                    if isinstance(model._fields.get(attr), mongoengine.fields.ReferenceField):
                        field = model._fields.get(attr)
                        ref_doc_type = field.document_type
                        pk = ref_doc_type._reverse_db_field_map.get('_id')
                        if pk:
                            if attr not in conditions:
                                conditions[attr] = {'filters': {pk+'__in': []}, 'ref_doc_type': ref_doc_type}
                            if attr not in prepare_items:
                                prepare_items[attr] = {v: []}
                            elif v not in prepare_items[attr]:
                                prepare_items[attr][v] = []
                            conditions[attr]['filters'][pk+'__in'].append(v)
                            prepare_items[attr][v].append(item)
                    
                    setattr(item, attr, v)
                items.append(item)

            if conditions:
                for attr, ref_options in conditions.items():
                    ref_rows = yield self.query_all_mongo(ref_options['ref_doc_type'], ref_options['filters'], limit=limit, as_dict=as_dict)
                    for ref_row in ref_rows:
                        if ref_row.id in prepare_items[attr]:
                            for dst_item in prepare_items[attr][ref_row.id]:
                                setattr(dst_item, attr, ref_row)

        return items

    @tornado.gen.coroutine
    def find_one_mongo(self, model, *args, **kwargs):
        """
        """
        as_dict = kwargs.pop('as_dict', False)
        q = self._format_mongo_query(model, (args, kwargs))
        collection = self._prepare_mongo_collection(model)
        document = yield from collection.find_one(q._query)
        if not document:
            return None

        if as_dict:
            item = {model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k: v for k, v in document.items()}
            # for k1, k2 in model._reverse_db_field_map.items():
            #     item[k2] = format_mongo_value(document.get(k1))
            return item
        else:
            item = model()
            for k, v in document.items():
                attr = model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k
                if isinstance(model._fields.get(attr), mongoengine.fields.ReferenceField):
                    field = model._fields.get(attr)
                    ref_doc_type = field.document_type
                    pk = ref_doc_type._reverse_db_field_map.get('_id')
                    if pk:
                        ref_filters = {pk: v, 'as_dict': as_dict}
                        v = yield self.find_one_mongo(ref_doc_type, **ref_filters)

                setattr(item, attr, v)

        return item

    @tornado.gen.coroutine
    def mongo_aggregate(self, model, pipeline=[], *args, **kwargs):
        """
        query mongo by aggregate.
        """
        as_dict = kwargs.pop('as_dict', True)
        collection = self._prepare_mongo_collection(model)
        cursor = collection.aggregate(pipeline)
        data_list = []
        if as_dict:
            while (yield cursor.fetch_next):
                item = cursor.next_object()
                data_list.append(item)
        else:
            while (yield cursor.fetch_next):
                item = cursor.next_object()
                obj = model()
                for k, v in item.items():
                    attr = model._reverse_db_field_map[k] if k in model._reverse_db_field_map else k
                    if isinstance(model._fields.get(attr), mongoengine.fields.ReferenceField):
                        field = model._fields.get(attr)
                        ref_doc_type = field.document_type
                        pk = ref_doc_type._reverse_db_field_map.get('_id')
                        if pk:
                            ref_filters = {pk: v, 'as_dict': as_dict}
                            v = yield self.find_one_mongo(ref_doc_type, **ref_filters)

                    setattr(obj, attr, v)
                data_list.append(obj)

        return data_list

    @tornado.gen.coroutine
    def save_mongo(self, item, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        """Save the :class:`~mongoengine.Document` to the database. If the
        document already exists, it will be updated, otherwise it will be
        created.

        :param force_insert: only try to create a new document, don't allow
            updates of existing documents.
        :param validate: validates the document; set to ``False`` to skip.
        :param clean: call the document clean method, requires `validate` to be
            True.
        :param write_concern: Extra keyword arguments are passed down to
            :meth:`~pymongo.collection.Collection.save` OR
            :meth:`~pymongo.collection.Collection.insert`
            which will be used as options for the resultant
            ``getLastError`` command.  For example,
            ``save(..., write_concern={w: 2, fsync: True}, ...)`` will
            wait until at least two servers have recorded the write and
            will force an fsync on the primary server.
        :param cascade: Sets the flag for cascading saves.  You can set a
            default by setting "cascade" in the document __meta__
        :param cascade_kwargs: (optional) kwargs dictionary to be passed throw
            to cascading saves.  Implies ``cascade=True``.
        :param _refs: A list of processed references used in cascading saves
        :param save_condition: only perform save if matching record in db
            satisfies condition(s) (e.g. version number).
            Raises :class:`OperationError` if the conditions are not satisfied
        :param signal_kwargs: (optional) kwargs dictionary to be passed to
            the signal calls.

        .. versionchanged:: 0.5
            In existing documents it only saves changed fields using
            set / unset.  Saves are cascaded and any
            :class:`~bson.dbref.DBRef` objects that have changes are
            saved as well.
        .. versionchanged:: 0.6
            Added cascading saves
        .. versionchanged:: 0.8
            Cascade saves are optional and default to False.  If you want
            fine grain control then you can turn off using document
            meta['cascade'] = True.  Also you can pass different kwargs to
            the cascade save using cascade_kwargs which overwrites the
            existing kwargs with custom values.
        .. versionchanged:: 0.8.5
            Optional save_condition that only overwrites existing documents
            if the condition is satisfied in the current db record.
        .. versionchanged:: 0.10
            :class:`OperationError` exception raised if save_condition fails.
        .. versionchanged:: 0.10.1
            :class: save_condition failure now raises a `SaveConditionError`
        .. versionchanged:: 0.10.7
            Add signal_kwargs argument
        """
        if item._meta.get('abstract'):
            raise mongoengine.InvalidDocumentError('Cannot save an abstract document.')

        signal_kwargs = signal_kwargs or {}
        mongoengine.signals.pre_save.send(item.__class__, document=item, **signal_kwargs)

        if validate:
            item.validate(clean=clean)

        if write_concern is None:
            write_concern = {'w': 1}

        doc = item.to_mongo()

        created = ('_id' not in doc or item._created or force_insert)

        mongoengine.signals.pre_save_post_validation.send(item.__class__, document=item,
                                              created=created, **signal_kwargs)
        # it might be refreshed by the pre_save_post_validation hook, e.g., for etag generation
        doc = item.to_mongo()

        if item._meta.get('auto_create_index', True):
            self.mongo_model_ensure_indexes(item)
            pass

        try:
            # Save a new document or update an existing one
            if created:
                object_id = yield self._mongo_save_create(item, doc, force_insert, write_concern)
            else:
                object_id, created = yield self._mongo_save_update(item, doc, save_condition,
                                                       write_concern)

            if cascade is None:
                cascade = (item._meta.get('cascade', False) or
                           cascade_kwargs is not None)

            if cascade:
                kwargs = {
                    'force_insert': force_insert,
                    'validate': validate,
                    'write_concern': write_concern,
                    'cascade': cascade
                }
                if cascade_kwargs:  # Allow granular control over cascades
                    kwargs.update(cascade_kwargs)
                kwargs['_refs'] = _refs
                yield self.mongo_cascade_save(item, **kwargs)

        except pymongo.errors.DuplicateKeyError as err:
            message = 'Tried to save duplicate unique keys (%s)'
            raise mongoengine.NotUniqueError(message % six.text_type(err))
        except pymongo.errors.OperationFailure as err:
            message = 'Could not save document (%s)'
            if re.match('^E1100[01] duplicate key', six.text_type(err)):
                # E11000 - duplicate key error index
                # E11001 - duplicate key on update
                message = 'Tried to save duplicate unique keys (%s)'
                raise mongoengine.NotUniqueError(message % six.text_type(err))
            raise mongoengine.OperationError(message % six.text_type(err))

        # Make sure we store the PK on this document now that it's saved
        id_field = item._meta['id_field']
        if created or id_field not in item._meta.get('shard_key', []):
            item[id_field] = item._fields[id_field].to_python(object_id)

        mongoengine.signals.post_save.send(item.__class__, document=item,
                               created=created, **signal_kwargs)

        item._clear_changed_fields()
        item._created = False

        return item

    @tornado.gen.coroutine
    def insert_mongo(self, model, values):
        """Supports Document, dict, or list(builk insert)

        :param mongoengine.Document|str model: The mongo schema or collection name.
        :param mongoengine.Document|dict|list values: the mongo document or dict or list value to be inserted.
        """
        collection = self._prepare_mongo_collection(model)
        result = False
        if isinstance(values, mongoengine.Document):
            result = yield self.save_mongo(values)
        elif isinstance(values, dict):
            result = yield collection.insert_one(values)
        else:
            inserts = []
            for v in values:
                if isinstance(v, dict):
                    inserts.append(v)
                elif isinstance(v, mongoengine.Document):
                    item = v.to_mongo()
                    inserts.append(item)
                else:
                    raise Exception("insert mongodb values should either be dict or Document type!")
            if inserts:
                result = yield collection.insert_many(inserts)
        return result

    @tornado.gen.coroutine
    def update_mongo(self, model, item, condition):
        """
        update mongo

        :param mongoengine.Document|str model: The mongo schema or collection name.
        :param dict item: update key and value.
        :param dict condition: update by this conditions.
        return int: updated count.
        """
        if not (condition and isinstance(item, dict) and ("id" or "_id") not in item):
            raise mongoengine.OperationError("Invalid input.")
        collection = self._prepare_mongo_collection(model)
        values = {"$set": item}

        updated_ret = yield collection.update_many(condition, values)
        updated_count = updated_ret.modified_count
        if not updated_count:
            raise mongoengine.OperationError("Updated error.")

        return updated_count

    @tornado.gen.coroutine
    def del_item_mongo(self, item, condition=None):
        """
        :param mongoengine.Document|str item: The mongo document or schema or collection name
        :param dict|None condition: the delete condition if condition specified, the field 
            should be provided when item is schame or collection name.
        """
        result = False
        collection = self._prepare_mongo_collection(item)
        if not condition:
            result = yield collection.delete_one({'_id': item.pk()})
        elif isinstance(condition, dict):
            result = yield collection.delete_many(condition)
        return result

    def _prepare_mongo_collection(self, model):
        db = self.get_mongo_dbinstance(model)
        if isinstance(model, str):
            collection_name = model
        else:
            collection_name = model._meta.get('collection')
            if not collection_name:
                collection_name = model._class_name
        collection = db[collection_name]
        return collection

    def _format_mongo_query(self, model, filters):
        q = mongoengine.queryset.QuerySet(model, None)
        qfilters = []
        kwfilters = {}
        if isinstance(filters, tuple):
            for f in filters:
                if isinstance(f, dict):
                    for k,v in f.items():
                        kwfilters[k] = v
                elif isinstance(f, list):
                    for v in f:
                        qfilters.append(v)
        elif isinstance(filters, dict):
            kwfilters = filters
        elif isinstance(filters, list):
            qfilters = filters

        if qfilters or kwfilters:
            q = q.filter(*qfilters, **kwfilters)
        elif filters:
            q = q.filter(filters)
        return q

    @tornado.gen.coroutine
    def mongo_model_ensure_indexes(self, model):
        """Checks the document meta data and ensures all the indexes exist.

        Global defaults can be set in the meta - see :doc:`guide/defining-documents`

        .. note:: You can disable automatic index creation by setting
                  `auto_create_index` to False in the documents meta data
        """
        background = model._meta.get('index_background', False)
        drop_dups = model._meta.get('index_drop_dups', False)
        index_opts = model._meta.get('index_opts') or {}
        index_cls = model._meta.get('index_cls', True)

        collection = self._prepare_mongo_collection(model)
        # 746: when connection is via mongos, the read preference is not necessarily an indication that
        # this code runs on a secondary
        if not collection.is_mongos and collection.read_preference > 1:
            return

        # determine if an index which we are creating includes
        # _cls as its first field; if so, we can avoid creating
        # an extra index on _cls, as mongodb will use the existing
        # index to service queries against _cls
        cls_indexed = False

        # Ensure document-defined indexes are created
        if model._meta['index_specs']:
            index_spec = model._meta['index_specs']
            for spec in index_spec:
                spec = spec.copy()
                fields = spec.pop('fields')
                cls_indexed = cls_indexed or mongoengine.document.includes_cls(fields)
                opts = index_opts.copy()
                opts.update(spec)

                # we shouldn't pass 'cls' to the collection.ensureIndex options
                # because of https://jira.mongodb.org/browse/SERVER-769
                if 'cls' in opts:
                    del opts['cls']

                if mongoengine.pymongo_support.IS_PYMONGO_GTE_37:
                    collection.create_index(fields, background=background, **opts)
                else:
                    collection.ensure_index(fields, background=background,
                                            drop_dups=drop_dups, **opts)

        # If _cls is being used (for polymorphism), it needs an index,
        # only if another index doesn't begin with _cls
        if index_cls and not cls_indexed and model._meta.get('allow_inheritance'):

            # we shouldn't pass 'cls' to the collection.ensureIndex options
            # because of https://jira.mongodb.org/browse/SERVER-769
            if 'cls' in index_opts:
                del index_opts['cls']

            if mongoengine.pymongo_support.IS_PYMONGO_GTE_37:
                collection.create_index('_cls', background=background,
                                        **index_opts)
            else:
                collection.ensure_index('_cls', background=background,
                                        **index_opts)

    @tornado.gen.coroutine
    def _mongo_save_create(self, item, doc, force_insert, write_concern):
        """Save a new document.

        Helper method, should only be used inside save().
        """
        collection = self._prepare_mongo_collection(item)
        if force_insert:
            insert_result = yield collection.insert_one(doc)
            return insert_result.inserted_id
        # insert_one will provoke UniqueError alongside save does not
        # therefore, it need to catch and call replace_one.
        if '_id' in doc:
            raw_object = yield collection.replace_one(
                {'_id': doc['_id']}, doc)
            if raw_object:
                return doc['_id']

        insert_result = yield collection.insert_one(doc)
        object_id = insert_result.inserted_id

        # In PyMongo 3.0, the save() call calls internally the _update() call
        # but they forget to return the _id value passed back, therefore getting it back here
        # Correct behaviour in 2.X and in 3.0.1+ versions
        if not object_id and pymongo.version_tuple == (3, 0):
            pk_as_mongo_obj = item._fields.get(item._meta['id_field']).to_mongo(item.pk)
            rc = yield self.find_one_mongo(item.__class__, pk=pk_as_mongo_obj)
            if rc:
                object_id = rc.pk
            # object_id = (
            #     item._qs.filter(pk=pk_as_mongo_obj).first() and
            #     item._qs.filter(pk=pk_as_mongo_obj).first().pk
            # )  # TODO doesn't this make 2 queries?

        return object_id

    @tornado.gen.coroutine
    def _mongo_save_update(self, item, doc, save_condition, write_concern):
        """Update an existing document.

        Helper method, should only be used inside save().
        """
        collection = self._prepare_mongo_collection(item)
        object_id = doc['_id']
        created = False

        select_dict = {}
        if save_condition is not None:
            select_dict = mongoengine.queryset.query(item.__class__, **save_condition)
            # select_dict = mongoengine.transform.query(item.__class__, **save_condition)

        select_dict['_id'] = object_id

        # Need to add shard key to query, or you get an error
        shard_key = item._meta.get('shard_key', tuple())
        for k in shard_key:
            path = item._lookup_field(k.split('.'))
            actual_key = [p.db_field for p in path]
            val = doc
            for ak in actual_key:
                val = val[ak]
            select_dict['.'.join(actual_key)] = val

        update_doc = item._get_update_doc()
        if update_doc:
            wc = write_concern.pop('w')
            upsert = save_condition is None
            last_error = yield collection.update_one(select_dict, update_doc,
                                                     upsert=upsert, **write_concern)
            if not upsert and last_error._UpdateResult__raw_result['n'] == 0:
                raise mongoengine.SaveConditionError('Race condition preventing'
                                         ' document update detected')
            if last_error is not None:
                updated_existing = last_error.raw_result.get('updatedExisting')
                if updated_existing is False:
                    created = True
                    # !!! This is bad, means we accidentally created a new,
                    # potentially corrupted document. See
                    # https://github.com/MongoEngine/mongoengine/issues/564

        return object_id, created

    @tornado.gen.coroutine
    def mongo_cascade_save(self, item, doc, **kwargs):
        """Recursively save any references and generic references on the
        document.
        """
        _refs = kwargs.get('_refs') or []

        ReferenceField = mongoengine.document._import_class('ReferenceField')
        GenericReferenceField = mongoengine.document._import_class('GenericReferenceField')

        for name, cls in list(item._fields.items()):
            if not isinstance(cls, (ReferenceField,
                                    GenericReferenceField)):
                continue

            ref = item._data.get(name)
            if not ref or isinstance(ref, mongoengine.DBRef):
                continue

            if not getattr(ref, '_changed_fields', True):
                continue

            ref_id = "%s,%s" % (ref.__class__.__name__, str(ref._data))
            if ref and ref_id not in _refs:
                _refs.append(ref_id)
                kwargs["_refs"] = _refs
                yield self.save_mongo(ref, **kwargs)
                ref._changed_fields = []

    @tornado.gen.coroutine
    def query_all(self, model, filters, sort=None, direction='asc', joins=None):
        qry, dbinstance, columns, _ = self._format_rdbms_query(model, filters, sort, direction, joins=joins)
        
        rows = yield self._execute_rdbms_result(dbinstance, qry, as_all=True)
        items = []
        for row in rows:
            item = {}
            for k in columns:
                if k in DEFAULT_SKIP_FIELDS:
                    continue
                item[k] = row._row[row._keymap[getattr(model, k).expression._key_label][2]]
            items.append(item)

        return items

    @tornado.gen.coroutine
    def _execute_rdbms_result(self, dbinstance, qry, as_all=True):
        querycontext = qry._compile_context()
        querycontext.statement.use_labels = True
        result = yield dbinstance.execute(querycontext.statement, qry._params)
        if as_all:
            ret = yield result.fetchall()
        else:
            ret = yield result.fetchone()
        return ret

    @tornado.gen.coroutine
    def _execute_rdbms_query_count(self, dbinstance, qry):
        col = sqlalchemy.sql.func.count(sqlalchemy.sql.literal_column("*"))
        qrycount = qry.from_self(col)
        querycontext = qrycount._compile_context()
        querycontext.statement.use_labels = True
        result = yield dbinstance.execute(querycontext.statement, qrycount._params)
        ret = yield result.fetchone()
        if ret:
            return ret[0]
        return 0

    @tornado.gen.coroutine
    def find_item(self, model, filters):
        dbinstance = self.get_model_dbinstance(model)
        qry = query.Query(model).filter(*filters)
        row = yield self._execute_rdbms_result(dbinstance, qry, as_all=False)
        if not row:
            return None
        columns, _ = model_columns(model)
        item = model()
        for k in columns:
            setattr(item, k, row._row[row._keymap[getattr(model, k).expression._key_label][2]])
        return item

    @tornado.gen.coroutine
    def get_count(self, model, filters):
        dbinstance = self.get_model_dbinstance(model)
        qry = query.Query(model).filter(*filters)
        count = yield self._execute_rdbms_query_count(dbinstance, qry)
        return count

    @tornado.gen.coroutine
    def update_values(self, model, filters, values):
        dbinstance = self.get_model_dbinstance(model)
        stmt = sqlalchemy.update(model).where(*filters).values(**values)
        result = yield dbinstance.execute(stmt)
        if result and result.rowcount:
            return result.rowcount
            
        return 0

    @tornado.gen.coroutine
    def update_item(self, item):
        model = item.__class__
        columns, pk = model_columns(model)
        dbinstance = self.get_model_dbinstance(model)
        values, defaults = self.get_rdbms_instance_update_values(item, model, columns, pk)
        if not values:
            return False
        stmt = sqlalchemy.update(model).where(getattr(model, pk)==getattr(item, pk)).values(**values)
        result = yield dbinstance.execute(stmt)
        if result and result.rowcount:
            for k, v in defaults.items():
                setattr(item, k, v)
            
        return item

    @tornado.gen.coroutine
    def insert_item(self, item, auto_flush=False):
        model = item.__class__
        columns, pk = model_columns(model)
        dbinstance = self.get_model_dbinstance(model)
        values, defaults = self.get_rdbms_instance_insert_values(item, model, columns, pk)
        if not values:
            return False
        stmt = sqlalchemy.insert(model).values(**values)
        result = yield dbinstance.execute(stmt)
        if result and result.rowcount:
            for k, v in defaults.items():
                setattr(item, k, v)
            if result.inserted_primary_key:
                setattr(item, pk, result.inserted_primary_key[0])
            
        return item

    @tornado.gen.coroutine
    def del_item(self, item):
        model = item.__class__
        dbinstance = self.get_model_dbinstance(model)
        _, pk = model_columns(model)
        stmt = sqlalchemy.delete(model).where(getattr(model, pk)==getattr(item, pk))
        result = yield dbinstance.execute(stmt)
        if result and result.rowcount:
            return result.rowcount
            
        return 0

    @tornado.gen.coroutine
    def del_items(self, model, filters):
        dbinstance = self.get_model_dbinstance(model)
        stmt = sqlalchemy.delete(model).where(*filters)
        result = yield dbinstance.execute(stmt)
        if result and result.rowcount:
            return result.rowcount
            
        return 0

    def get_rdbms_instance_insert_values(self, item, model, columns, pk):
        values = {}
        defaults = {}
        for col in columns:
            tbl_col_name = getattr(model, col).expression.name
            if col in item._sa_instance_state.unmodified:
                v = self.get_rdbms_instance_default_value(getattr(model, col).expression, True)
                if v is None and col == pk:
                    continue
                values[tbl_col_name] = v
                defaults[tbl_col_name] = v
            else:
                values[tbl_col_name] = getattr(item, col)
        return values, defaults

    def get_rdbms_instance_update_values(self, item, model, columns, pk):
        values = {}
        defaults = {}
        for col in columns:
            tbl_col_name = getattr(model, col).expression.name
            values[tbl_col_name] = getattr(item, col)
            v = self.get_rdbms_instance_default_value(getattr(model, col).expression, False)
            if v is not None:
                values[tbl_col_name] = v
                defaults[tbl_col_name] = v
            
        return values, defaults

    def get_rdbms_instance_default_value(self, column, is_insert):
        column_default = column.default if is_insert else column.onupdate
        if column_default is None:
            return None
        else:
            return self._exec_rdbms_default(column, column_default, column.type)

    def _exec_rdbms_default(self, column, default, type_):
        if default.is_sequence:
            raise Exception("sequence default column value is not supported")
            return None # self.fire_sequence(default, type_)
        elif default.is_callable:
            return default.arg(None)
        elif default.is_clause_element:
            # TODO: expensive branching here should be
            raise Exception("clause default column value is not supported")
            # # pulled into _exec_scalar()
            # conn = self.connection
            # if not default._arg_is_typed:
            #     default_arg = expression.type_coerce(default.arg, type_)
            # else:
            #     default_arg = default.arg
            # c = expression.select([default_arg]).compile(bind=conn)
            # return conn._execute_compiled(c, (), {}).scalar()
            return None
        else:
            return default.arg
