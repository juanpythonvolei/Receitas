from marshmallow import Schema, fields
from db.db import *

class ReceitaSchema(Schema):
    nome = fields.Str()  
    id = fields.Int()
    usuario = fields.Str()
    data = fields.Str()
    infos = fields.Str()
    tipo = fields.Str()