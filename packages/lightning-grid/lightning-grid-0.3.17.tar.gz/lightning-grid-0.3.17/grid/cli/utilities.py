import click

from typing import Dict, Any
from grid.tracking import tracker, TrackingEvents

DISK_SIZE_ERROR_MSG = "Invalid disk size, should be greater than 100Gb"


def validate_config(cfg: Dict[str, Any]) -> None:
    """
    Validates Grid config.

    Parameters
    ----------
    cfg: Dict[str, Any]
        Dictionary representing a Grid config
    """
    disk_size = cfg['compute']['train']['disk_size']
    if disk_size is not None and disk_size < 100:
        raise click.ClickException(DISK_SIZE_ERROR_MSG)

    tracker.send_event(TrackingEvents.CONFIG_PARSED,
                       properties={'config': cfg})


def validate_disk_size_callback(ctx, param, value: int) -> int:
    """
    Validates the disk size upon user input.

    Parameters
    ----------
    ctx
        Click context
    param
        Click parameter
    value: int

    Returns
    --------
    value: int
        Unmodified value if valid
    """
    if value < 100:
        raise click.BadParameter(DISK_SIZE_ERROR_MSG)

    return value
