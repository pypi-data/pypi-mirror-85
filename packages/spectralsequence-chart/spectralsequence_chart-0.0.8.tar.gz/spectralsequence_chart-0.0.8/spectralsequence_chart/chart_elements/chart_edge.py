from abc import ABC, abstractmethod
from ..helper_classes import (
    PageProperty, PagePropertyOrValue, ensure_page_property,
    SignalDict
)
from uuid import uuid4

from typing import Optional, TYPE_CHECKING, Any, Dict, cast, Union, Optional, Tuple
if TYPE_CHECKING:
    from ..chart import SseqChart
    from .chart_class import ChartClass, ChartClassStyle
    from .display_primitives import Shape

from .display_primitives import UUID_str, Color, DashPattern, LineWidth, ArrowTip

class ChartEdgeStyle:
    def __init__(self, 
        color : Color = (0, 0, 0, 1),
        dash_pattern : DashPattern = [],
        line_width : float = 2,
        bend : float = 0,
        start_tip : Optional[ArrowTip] = None,
        end_tip : Optional[ArrowTip] = None,
    ):
        self._color : Color = color
        self._dash_pattern : DashPattern = dash_pattern
        self._line_width : float = line_width
        self._bend : float = bend
        self._start_tip : Optional[ArrowTip] = start_tip
        self._end_tip : Optional[ArrowTip] = end_tip

    @property
    def color(self) -> Color:
        """ The color of the edge. """
        return self._color

    @color.setter
    def color(self, v : Color):
        self._color = v

    @property
    def dash_pattern(self) -> DashPattern:
        """The dash pattern of the edge. A dash pattern is represented as a list of positive integers."""
        return self._dash_pattern

    @dash_pattern.setter
    def dash_pattern(self, v : DashPattern):
        self._dash_pattern = v

    @property
    def line_width(self) -> LineWidth:
        """The width of the edge."""
        return self._line_width


    @line_width.setter
    def line_width(self, v : LineWidth):
        self._line_width = v

    @property
    def bend(self) -> float:
        """The bend angle of the edge. If bend is nonzero, the edge is drawn as a circular arc through the start and end points,
           where the angle between the edge from the start to the end and the tangent vector at the start point is specified by "bend".
        """
        return self._bend

    @bend.setter
    def bend(self, v : float):
        self._bend = v

    @property
    def start_tip(self) -> Optional[ArrowTip]:
        """ The start arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._start_tip

    @start_tip.setter
    def start_tip(self, v : Optional[ArrowTip]):
        self._start_tip = v

    @property
    def end_tip(self) -> Optional[ArrowTip]:
        """ The end arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._end_tip

    @end_tip.setter
    def end_tip(self, v : Optional[ArrowTip]):
        self._end_tip = v

class ChartEdge(ABC):
    """ ChartEdge is the base class of ChartStructline, ChartDifferential, and ChartExtension. """
    def __init__(self, source_uuid : UUID_str, target_uuid : UUID_str):
        """ Do not call SseqEdge constructor directly, use instead SseqChart.add_structline(),
            SseqChart.add_differential(), SseqChart.add_extension(), or JSON.parse()."""
        self._sseq : SseqChart
        self._source_uuid = source_uuid
        self._target_uuid = target_uuid
        self._source : ChartClass
        self._target : ChartClass        
        self._uuid = str(uuid4())
        self._user_data : SignalDict[Any] = SignalDict({}, parent=self) # type: ignore

    def __repr__(self):
        fields = [repr(x) for x in [self.source, self.target]]
        return f"{type(self).__name__}({', '.join(fields)})"


    def _needs_update(self):
        if hasattr(self, "_sseq"):
            self._sseq._add_edge_to_update(self)

    def replace_source(self, 
        style : "ChartClassStyle" = None,
        shape : "Shape" = None,
        background_color : Color = None,
        border_color : Color = None,
        border_width : float = None,
        foreground_color : Color = None,
    ) -> "ChartEdge":
        """ Calls "replace" on the source of the edge. Returns self to be chainable. """
        self.source.replace(
            style=style, shape=shape,  border_width=border_width,
            background_color=background_color, border_color=border_color, foreground_color=foreground_color
        )
        return self
    
    def replace_target(self, 
        style : "ChartClassStyle" = None,
        shape : "Shape" = None,
        background_color : Color = None,
        border_color : Color = None,
        border_width : float = None,
        foreground_color : Color = None,
    ) -> "ChartEdge":
        """ Calls "replace" on the target of the edge. Returns self to be chainable. """
        self.target.replace(
            style=style, shape=shape,  border_width=border_width,
            background_color=background_color, border_color=border_color, foreground_color=foreground_color
        )
        return self

    def delete(self):
        """ Deletes the edge. """
        self._sseq._add_edge_to_delete(self)
        del self._sseq._edges[self.uuid]
        del self.source.edges[self.source.edges.index(self)]
        del self.target.edges[self.target.edges.index(self)]

    _EDGE_TYPE_DICT : Dict[str, type]
    @staticmethod
    def from_json(json : Dict[str, Any]) -> "ChartEdge":
        if not hasattr(ChartEdge, "EDGE_TYPE_DICT"):
            ChartEdge._EDGE_TYPE_DICT = {edge_type.__name__ : edge_type for edge_type in [ChartStructline, ChartDifferential, ChartExtension]}
        edge_type = json["type"]
        if edge_type in ChartEdge._EDGE_TYPE_DICT:
            init_args = {}
            for key in ["source_uuid", "target_uuid", "page"]:
                if key in json:
                    init_args[key] = json.pop(key)
            edge = ChartEdge._EDGE_TYPE_DICT[edge_type](**init_args)
            edge._from_json_helper(**json)
            return edge
        else:
            type_names = list(ChartEdge._EDGE_TYPE_DICT.keys())
            types_list = ",".join(f'"{type}"' for type in type_names[:-1])
            types_list += f', or "${type_names[-1]}"'
            raise ValueError(f'"edge_type" should be one of {types_list}, not "{edge_type}"')

    @property
    def uuid(self) -> str:
        """ A unique id for the edge. For internal use. """
        return self._uuid

    @property
    def source(self) -> "ChartEdge":
        """ The start class of the edge. (All edges are directed.) """
        return self._source

    @property
    def target(self) -> "ChartEdge":
        """ The end class of the edge. (All edges are directed.) """
        return self._target

    def _from_json_helper(self,
        type : Optional[str], 
        uuid : UUID_str,
        user_data : Dict[str, Any],
    ):
        assert type == self.__class__.__name__
        self._uuid = uuid
        self._user_data = SignalDict(user_data, parent=self)
        

    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        return dict(
            type=self.__class__.__name__,
            uuid=self.uuid,
            source_uuid=self._source_uuid,
            target_uuid=self._target_uuid,
            # color=self.color,
            # dash_pattern=self.dash_pattern,
            # line_width=self.line_width,
            # bend=self.bend,
            # visible=self.visible,
            user_data=self._user_data
        )

class ChartStructline(ChartEdge):
    """ A ChartStructline is an edge used to represent some sort of algebraic data on the spectral sequence. 
        Structlines are typically used to represent multiplication by a few standard elements.
        A structline will appear on page_range (<page>, <max_differential_length>) if structline.visible[<page>] 
        is true and both the source and the target class of the structure line are visible.
    """
    def __init__(self, source_uuid : UUID_str, target_uuid : UUID_str):
        super().__init__(source_uuid, target_uuid)
        self.color = (0, 0, 0, 1)
        self.dash_pattern = []
        self.line_width = 2
        self.bend = 0
        self.start_tip = None
        self.end_tip = None
        self.visible = True

    def set_style(self, page : slice, style : ChartEdgeStyle) -> "ChartStructline":
        self.color[page] = style.color
        self.dash_pattern[page] = style.dash_pattern
        self.line_width[page] = style.line_width
        self.bend[page] = style.bend
        self.start_tip[page] = style.start_tip
        self.end_tip[page] = style.end_tip
        return self
    
    def to_json(self) -> Dict[str, Any]:
        return dict(
            super().to_json(),
            type=self.__class__.__name__,
            uuid=self.uuid,
            source_uuid=self._source_uuid,
            target_uuid=self._target_uuid,
            color=self.color,
            dash_pattern=self.dash_pattern,
            line_width=self.line_width,
            bend=self.bend,
            start_tip=self.start_tip,
            end_tip=self.end_tip,
            visible=self.visible,
            user_data=self._user_data
        )

    def _from_json_helper(self,
        color : PagePropertyOrValue[Color],
        dash_pattern : PagePropertyOrValue[DashPattern],
        line_width : PagePropertyOrValue[float],
        bend : PagePropertyOrValue[float],
        start_tip : PagePropertyOrValue[Optional[ArrowTip]],
        end_tip : PagePropertyOrValue[Optional[ArrowTip]],
        visible : PagePropertyOrValue[bool],
        **kwargs,
    ) -> "ChartEdge":
        super()._from_json_helper(**kwargs)
        self._color = cast(PageProperty[Color], ensure_page_property(color, parent=self))
        self._dash_pattern = cast(PageProperty[DashPattern], ensure_page_property(dash_pattern, parent=self))
        self._line_width = cast(PageProperty[Union[float, str]], ensure_page_property(line_width, parent=self))
        self._bend = cast(PageProperty[float], ensure_page_property(bend, parent=self)) 
        self._start_tip = cast(PageProperty[Optional[ArrowTip]], ensure_page_property(start_tip, parent=self)) 
        self._end_tip = cast(PageProperty[Optional[ArrowTip]], ensure_page_property(end_tip, parent=self)) 
        self._visible = cast(PageProperty[bool], ensure_page_property(visible, parent=self))

    @property
    def color(self) -> PageProperty[Color]:
        """ The color of the edge. """
        return self._color

    @color.setter
    def color(self, v : PagePropertyOrValue[Color]): # type: ignore
        self._color = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def dash_pattern(self) -> PageProperty[DashPattern]:
        """The dash pattern of the edge. A dash pattern is represented as a list of positive integers."""
        return self._dash_pattern

    @dash_pattern.setter
    def dash_pattern(self, v : PagePropertyOrValue[DashPattern]): # type: ignore
        self._dash_pattern = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def line_width(self) -> PageProperty[LineWidth]:
        """The width of the edge."""
        return self._line_width


    @line_width.setter
    def line_width(self, v : PagePropertyOrValue[LineWidth]): # type: ignore
        self._line_width = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def bend(self) -> PageProperty[float]:
        """The bend angle of the edge. If bend is nonzero, the edge is drawn as a circular arc through the start and end points,
           where the angle between the edge from the start to the end and the tangent vector at the start point is specified by "bend".
        """
        return self._bend

    @bend.setter
    def bend(self, v : PagePropertyOrValue[float]): # type: ignore
        self._bend = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def visible(self) -> PageProperty[bool]:
        """Is the structline visible on the given page?"""
        return self._visible

    @visible.setter
    def visible(self, v : PagePropertyOrValue[bool]): # type: ignore
        self._visible = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def start_tip(self) -> PageProperty[Optional[ArrowTip]]:
        """ The start arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._start_tip


    @start_tip.setter
    def start_tip(self, v : PagePropertyOrValue[Optional[ArrowTip]]):
        self._start_tip = ensure_page_property(v, parent=self)
        self._needs_update()

    @property
    def end_tip(self) -> PageProperty[Optional[ArrowTip]]:
        """ The end arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._end_tip

    @end_tip.setter
    def end_tip(self, v : PagePropertyOrValue[Optional[ArrowTip]]):
        self._end_tip = ensure_page_property(v, parent=self)
        self._needs_update()

class SinglePageChartEdge(ChartEdge):
    """ SinglePageChartEdge is handles most of the common code between ChartDifferential and ChartExtension. """
    def __init__(self, source_uuid : UUID_str, target_uuid : UUID_str):
        super().__init__(source_uuid, target_uuid)
        self._color : Color = (0, 0, 0, 1)
        self._dash_pattern = []
        self._line_width = 3
        self._bend = 0
        self._start_tip = None
        self._end_tip = None
        self._visible = True

    def set_style(self, style : ChartEdgeStyle) -> "SinglePageChartEdge":
        self.color = style.color
        self.dash_pattern = style.dash_pattern
        self.line_width = style.line_width
        self.bend = style.bend
        self.start_tip = style.start_tip
        self.end_tip = style.end_tip
        return self
    

    def _from_json_helper(self,
        color : Color,
        dash_pattern : DashPattern,
        line_width : float,
        bend : float,
        start_tip : Optional[ArrowTip],
        end_tip : Optional[ArrowTip],
        visible : bool,
        **kwargs,
    ) -> "ChartEdge":
        super()._from_json_helper(**kwargs)
        self._color = color
        self._dash_pattern = dash_pattern
        self._line_width = line_width
        self._bend = bend
        self._start_tip = start_tip
        self._end_tip = end_tip
        self._visible = visible

    @property
    def color(self) -> Color:
        """ The color of the edge. """
        return self._color

    @color.setter
    def color(self, v : Color):
        self._color = v
        self._needs_update()

    @property
    def dash_pattern(self) -> DashPattern:
        """The dash pattern of the edge. A dash pattern is represented as a list of positive integers."""
        return self._dash_pattern

    @dash_pattern.setter
    def dash_pattern(self, v : DashPattern):
        self._dash_pattern = v
        self._needs_update()

    @property
    def line_width(self) -> LineWidth:
        """The width of the edge."""
        return self._line_width


    @line_width.setter
    def line_width(self, v : LineWidth):
        self._line_width = v
        self._needs_update()

    @property
    def bend(self) -> float:
        """The bend angle of the edge. If bend is nonzero, the edge is drawn as a circular arc through the start and end points,
           where the angle between the edge from the start to the end and the tangent vector at the start point is specified by "bend".
        """
        return self._bend

    @bend.setter
    def bend(self, v : float):
        self._bend = v
        self._needs_update()

    @property
    def visible(self) -> bool:
        """Is the structline visible on the given page?"""
        return self._visible

    @visible.setter
    def visible(self, v : bool):
        self._visible = v
        self._needs_update()


    @property
    def start_tip(self) -> Optional[ArrowTip]:
        """ The start arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._start_tip


    @start_tip.setter
    def start_tip(self, v : Optional[ArrowTip]):
        self._start_tip = v
        self._needs_update()

    @property
    def end_tip(self) -> Optional[ArrowTip]:
        """ The end arrow tip. TODO: Explain how we represent arrow tips and make ArrowTip not be any? """
        return self._end_tip

    @end_tip.setter
    def end_tip(self, v : Optional[ArrowTip]):
        self._end_tip = v
        self._needs_update()


    def to_json(self) -> Dict[str, Any]:
        return dict(
            super().to_json(),
            type=self.__class__.__name__,
            uuid=self.uuid,
            source_uuid=self._source_uuid,
            target_uuid=self._target_uuid,
            color=self.color,
            start_tip=self.start_tip,
            end_tip=self.end_tip,
            dash_pattern=self.dash_pattern,
            line_width=self.line_width,
            bend=self.bend,
            visible=self.visible,
            user_data=self._user_data
        )


class ChartDifferential(SinglePageChartEdge):
    """ A ChartDifferential is an edge used to represent the behavior of the differential on the spectral sequence. 
        A chart differential will appear on page_range (<page>, <max_differential_length>) if <page> <= differential.page <= <max_differential_length>
        and if both the source and target of the differential appear on page <page>.
    """
    def __init__(self, source_uuid : UUID_str, target_uuid : UUID_str, page : int):
        super().__init__(source_uuid, target_uuid)
        self.page : int = page

    def to_json(self) -> Dict[str, Any]:
        return dict(
            super().to_json(),
            page=self.page
        )

class ChartExtension(SinglePageChartEdge):
    """ A ChartExtension is an edge used to represent extensions in the spectral sequence. 
        Generally extensions represent the same sort of algebraic structure as the structlines.
        A chart extension will appear on page_range (<page>, <max_differential_length>) if <page> == infinity
        and both the source and the target of the extension appear on page infinity.
    """
    pass