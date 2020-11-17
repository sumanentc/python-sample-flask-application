from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        load_only = ("store",)
        include_fk= True