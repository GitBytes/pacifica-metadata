#!/usr/bin/python

from metadata.orm import ORM_OBJECTS

for obj_cls in ORM_OBJECTS:
    print "### %s"%(obj_cls.__name__)
    print "| Column | Type | Reference |"
    print "| --- | --- | --- |"
    column_tuples = []
    for obj_cls_attr in dir(obj_cls):
        if type(getattr(obj_cls, obj_cls_attr)).__module__ == 'peewee' and \
           obj_cls_attr != '_meta' and \
           type(getattr(obj_cls, obj_cls_attr)).__name__ != 'ReverseRelationDescriptor' and \
           type(getattr(obj_cls, obj_cls_attr)).__name__ != 'CompositeKey':
            column_name = obj_cls_attr
            column_type = getattr(obj_cls, obj_cls_attr).get_column_type()
            points_to = ""
            if type(getattr(obj_cls, obj_cls_attr)).__name__ == 'ForeignKeyField':
                points_to_class = getattr(obj_cls, obj_cls_attr).to_field.model_class.__name__
                points_to_column = getattr(obj_cls, obj_cls_attr).to_field.name
                points_to = "%s.%s"%(points_to_class, points_to_column)
            column_tuples.append((column_name, column_type, points_to))
    def column_cmp(a, b):
        if a[0] == 'id' and b[0] == 'id':
            return 0
        if a[0] == 'id':
            return -1
        if b[0] == 'id':
            return 1
        common_dates = ['created', 'deleted', 'updated']
        if a[0] == b[0]:
            return 0
        if a[0] in common_dates:
            return 1
        if b[0] in common_dates:
            return -1
        return a[0] < b[0]
    for column in sorted(column_tuples, cmp=column_cmp):
        print "| %s | %s | %s |"%column
    print ""
