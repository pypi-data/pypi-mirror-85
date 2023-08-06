from pik_wrapper.entity.entity import Entity


class Bulk(Entity):
    def __init__(self, id_or_dict, name: str = None, sort: int = None, type_id: int = None):
        super().__init__(id_or_dict)
        if isinstance(id_or_dict, dict):
            name = id_or_dict.get('name')
            sort = id_or_dict.get('sort')
            type_id = id_or_dict.get('type_id')
        if type(name) is not str:
            raise ValueError
        self.name = name
        if type(sort) is not int:
            raise ValueError
        self.sort = sort
        if type(type_id) is not int:
            raise ValueError
        self.type_id = type_id
