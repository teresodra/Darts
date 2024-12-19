

class Cell:
    """Contain the value of the cell, the locations that take you to this cell and whether one can finish by hitting this cell or not."""
    def __init__(self,
                 value:int,
                 locations:list,
                 finish:bool):
        self.value = value
        self.locations = locations
        self.finish = finish


class Location:
    """Contains the locations of the cell"""
    def __init__(self,
                 min_r:float,
                 max_r:float,
                 min_phi:float,
                 max_phi:float
                 ):
        self.min_phi = min_phi