from cub.models import Edge
from cub.models import Food_db
class Food:
  
    def __init__(self, top, left, div_id, height, width):
        self.top = top
        self.left = left
        self.div_id = div_id
        self.height = height
        self.width = width
        self.db_id = None
        self.obj_db, created = Food_db.objects.get_or_create(
            top = top,
            left = left,
            div_id = div_id,
            height = height,
            width = width
        )
        self.st_top_db, created = Food_db.objects.get_or_create(
            top = top,
            left = left,
            div_id = div_id,
            height = height,
            width = width
        )
        if not created:
            self.obj_db.save()
            data_dict = {}
            data_dict['pref_parent_id'] = f"'food_'{str(self.top)}'_'{str(self.left)}'"
            data_dict['x1'] = left
            data_dict['y1'] = top
            data_dict['x2'] = left + width
            data_dict['y2'] = top
            Edge.objects.create(**data_dict)
            data_dict['x1'] = left + width
            data_dict['y1'] = top
            data_dict['x2'] = left + width
            data_dict['y2'] = top + height
            Edge.objects.create(**data_dict)
            data_dict['x1'] = left + width
            data_dict['y1'] = top + height
            data_dict['x2'] = left
            data_dict['y2'] = top + height
            Edge.objects.create(**data_dict)
            data_dict['x1'] = left
            data_dict['y1'] = top + height
            data_dict['x2'] = left
            data_dict['y2'] = top
            Edge.objects.create(**data_dict)
     
    def __del__(self):
        self.obj_db.delete()