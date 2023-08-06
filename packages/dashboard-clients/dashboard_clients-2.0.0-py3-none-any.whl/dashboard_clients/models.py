"""
Dashboard Enums and Models are from:
https://e360-dashboard-service-dev.internal.imsglobal.com/wrapper/documents
"""


import enum
from datetime import datetime
from typing import List, ClassVar, Type, Optional
from dataclasses import field
from marshmallow import Schema as Schema_
from marshmallow_dataclass import dataclass as ma_dataclass


class DashboardStatus(enum.Enum):
    unlocked = 1  # The default value of dashboard when created
    locked = 2  # The value of locked status


class TileType(enum.Enum):
    staticText = 1  # A tile which shows the static text
    image = 2  # A tile which shows the image
    codelistSummary = 3  # A tile which shows the codelist info
    document = 4  # A tile which shows the document info
    cohortDetails = 5  # A tile which shows information about a cohort including it's size and name
    link = 6  # A tile which shows the link's name as well as the thumbnail image if available
    cohortGenderBreakdown = 7  # A tile which shows the gender breakdown for a cohort
    cohortAgeBreakdown = 8  # A tile which shows the age breakdown for a cohort
    cohortGenderAgeBreakdown = 9  # A tile which shows the age range and gender combination breakdown for a cohort
    stackEventDistribution = 10  # A tile which shows the stack event distribution for a cohort
    cohortGeographicBreakdown = 11  # A tile which shows the geographic breakdown for a cohort
    analytic = 12  # A tile which displays an analytic asset
    visualisationPreview = 13  # A tile which displays a visualisation preview


@ma_dataclass
class TileConfigurationModel:
    title: Optional[str] = field(default=None)
    show_title: bool = field(default=True, metadata=dict(data_key='showTitle'))
    colour_theme: Optional[str] = field(default=None, metadata=dict(data_key='colourTheme'))
    show_border: bool = field(default=True, metadata=dict(data_key='showBorder'))


@ma_dataclass
class TileModel:
    width: int = field(default=0)  # The tile's width value to render
    height: int = field(default=0)  # The tile's height value to render
    x: int = field(default=0)  # The tile's X position to render
    y: int = field(default=0)  # The tile's Y position to render
    tile_index: int = field(default=0, metadata=dict(data_key='tileIndex'))  # The sequence index of tile in current dashboard
    internal_id: int = field(default=0, metadata=dict(data_key='internalId'))  # The internal id of tile
    tile_type: TileType = field(default=TileType.staticText, metadata=dict(data_key='tileType'))
    asset_id: Optional[str] = field(default=None, metadata=dict(data_key='assetId'))  # The asset's guid to navigate
    tile_config: TileConfigurationModel = field(default_factory=TileConfigurationModel, metadata=dict(data_key='tileConfiguration'))  # The TileConfiguration object included tile's general info
    breakdown_config: dict = field(default_factory=dict, metadata=dict(data_key='breakdownConfiguration'))  # The BreakdownConfiguration object included tile's breakdown configuration info
    created: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    updated: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking


@ma_dataclass
class TabModel:
    internal_id: Optional[int] = field(default=None, metadata=dict(data_key='internalId'))  # The internal id of tab
    tab_index: int = field(default=0, metadata=dict(data_key='tabIndex'))  # The sequence index of tab in current dashboard
    title: str = field(default='Tab 1')  # The title of tab
    tiles: List[TileModel] = field(default_factory=list)  # The list of TileModel in tab
    created: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    updated: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking


@ma_dataclass
class TabbedDashboardModel:
    """Dashboard with tabs for v2 endpoint"""
    id: Optional[int] = field(default=None)
    dashboard_status: DashboardStatus = field(default=DashboardStatus.unlocked, metadata=dict(data_key='dashboardStatus'))
    tabs: List[TabModel] = field(default_factory=list)  # The list of TabModel in dashboard
    created: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    updated: Optional[datetime] = field(default=None, metadata=dict(load_only=True))
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking
