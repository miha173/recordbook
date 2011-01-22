import demjson

from django.db import models

class RestModelManager(models.Manager):
    def serialize(self, fields):
        result = [obj.serialize(fields, safe = True) for obj in self.get_query_set()]
        return demjson.encode(result)

class RestModel(models.Model):
    serialize_name = ''
    objects = RestModelManager()
    rest_modified = models.DateTimeField()
    def get_absolute_uri(self):
        return '/api/%s/%d/' % (self.serialize_name, int(self.id))
    def serialize(self, fields, safe = False):
        result = {}
        for field in fields:
            attr = self.__getattribute__(field)
            if type(attr).__name__ == 'ManyRelatedManager':
                attr = [t.id for t in attr.all()]
            elif type(attr).__name__ in ['datetime', 'date', 'time']:
                attr = attr.isoformat()
            result[field] = attr
        if safe:
            return result
        else:
            return demjson.encode(result)
    def save(self, *args, **kwargs):
        from datetime import datetime
        self.rest_modified = datetime.now()
        super(RestModel, self).save(*args, **kwargs)
    class Meta:
        abstract = True

        
        
        