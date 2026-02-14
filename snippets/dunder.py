# dunder is double underscore

class Rect:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Rectangle {self.x} by {self.y}"
    
    def __repr__(self) -> str:
        return f"Rect(x='{self.x}', y='{self.y}')"
    
    def __expand__(self, incr: int):
        if isinstance(incr, int):
            return Rect(self.x + incr, self.y + incr)
        else:
            raise TypeError(f"Cannot expand Rect by {type(incr)}")


r1 = Rect(2, 4)
#print(type(r1))
print(str(r1))
print(repr(r1))

r2 = r1.__expand__(2)
#print(type(r2))
print(r2)


# __add__, __sub__, __mult__, __len__, __del__, __lt__, __gt__