from typing import List

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.strand.StrandTag import StrandTag


class StrandStrand(Model):
    def __init__(self, id, title=None, tags=None):
        self.id = id
        self.title = title
        self.tags: List[StrandTag] = tags


class StrandStrandSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_strand_strand(self, data):
        return StrandStrand(**data)

    class Meta:
        strict = True
