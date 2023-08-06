__version__ = "2.0.0"

__all__ = [
    "DashboardsClient",
    "TabbedDashboardModel",
    "TabModel",
    "TileModel",
    "TileConfigurationModel",
    "TileType",
    "DashboardStatus",
]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .dashboard_service_client import DashboardsClient
    from .models import (
        TabbedDashboardModel,
        TabModel,
        TileModel,
        TileConfigurationModel,
        TileType,
        DashboardStatus
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
