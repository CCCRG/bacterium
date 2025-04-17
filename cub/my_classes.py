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
        self.is_new = created
        self.pref_id_str = f"food_{str(self.top)}_{str(self.left)}"
        self.st_top_db, created = Edge.objects.get_or_create(
            pref_parent_id = self.pref_id_str,
            x1 = left,
            y1 = top,
            x2 = left + width,
            y2 = top
        )
        self.st_right_db, created = Edge.objects.get_or_create(
            pref_parent_id = self.pref_id_str,
            x1 = left + width,
            y1 = top,
            x2 = left + width,
            y2 = top + height,
        )
        self.st_bottom_db, created = Edge.objects.get_or_create(
            pref_parent_id = self.pref_id_str,
            x1 = left + width,
            y1 = top + height,
            x2 = left,
            y2 = top + height,
        )
        self.st_left_db, created = Edge.objects.get_or_create(
            pref_parent_id = self.pref_id_str,
            x1 = left,
            y1 = top + height,
            x2 = left,
            y2 = top,
        )
    def get_div(self):
        data = {}
        data['left'] = self.left
        data['top'] = self.top
        data['div_id'] = self.pref_id_str
        data['height'] = self.height
        data['width'] = self.width
        return data
    
    def delete(self):
        self.obj_db.delete()
        self.st_bottom_db.delete()
        self.st_left_db.delete()
        self.st_right_db.delete()
        self.st_top_db.delete()