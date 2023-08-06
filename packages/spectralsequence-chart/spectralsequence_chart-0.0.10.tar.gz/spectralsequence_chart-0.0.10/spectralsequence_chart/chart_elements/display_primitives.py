from typing import Union, List, Tuple, Any

Color = Tuple[float, float, float, float]
UUID_str = str
DashPattern = List[int]
LineWidth = Union[float, str]

class ArrowTip:
    def __init__(self, tip="standard"):
        self._tip = tip

    @property
    def tip(self):
        return self._tip
    
    def to_json(self):
        return dict(
            type=type(self).__name__,
            tip = self.tip,
        )

    @staticmethod
    def from_json(json):
        assert json.pop("type") == ArrowTip.__name__
        return ArrowTip(**json)

    def __repr__(self):
        return f"ArrowTip('{self.tip}')"


class Shape:
    def __init__(self, character=None, font=None):
        if character:
            self.dict = dict(
                ty="character",
                font=font or "stix",
                char=character,
                whole_shape=True
            )
        else:
            self.dict = dict(ty="empty")
    
    def circled(self, padding : float, num_circles : int = 1, circle_gap : float = 0, include_background : bool = True) -> "Shape":
        if "whole_shape" in self.dict:
            self.dict["whole_shape"] = False
        self.dict = dict(
            ty = "composed",
            operation="circled",
            padding=padding,
            num_circles=num_circles,
            circle_gap=circle_gap,
            include_background=include_background,
            innerShape=self.dict
        )
        return self

    def boxed(self, padding : float, include_background : bool = True) -> "Shape":
        if "whole_shape" in self.dict:
            self.dict["whole_shape"] = False
        self.dict = dict(
            ty = "composed",
            operation="boxed",
            padding=padding,
            include_background=include_background,
            innerShape=self.dict
        )
        return self

    def to_json(self):
        result = {"type" : type(self).__name__}
        result.update(self.dict)
        return result
    
    @staticmethod
    def from_json(json):
        assert json.pop("type") == Shape.__name__
        result = Shape()
        result.dict = json
        return result

    def __repr__(self):
        return f"Shape({repr(self.dict)})"