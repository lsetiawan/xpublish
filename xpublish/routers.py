from typing import Callable, Dict, Union

import xarray as xr
from fastapi import APIRouter, HTTPException

DatasetOrCollection = Union[xr.Dataset, Dict[str, xr.Dataset]]


def _get_dataset_dependency(obj: DatasetOrCollection) -> Callable:
    """Returns a xarray Dataset getter to be used as fastAPI dependency."""

    def get_obj():
        return obj

    def get_from_mapping(dataset_id: str):
        if dataset_id not in obj:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return obj[dataset_id]

    if isinstance(obj, xr.Dataset):
        return get_obj
    else:
        return get_from_mapping


class APIRouterWrapper:
    """Wraps :class:`fastapi.APIRouter` so that it can be included
    in an application serving either a single xarray Dataset or a
    collection of Datasets.

    """

    def __init__(self, obj: DatasetOrCollection):

        self._obj = obj
        self._router = None
        self._dataset = None

    def __len__(self):
        if isinstance(self._obj, dict):
            return len(self._obj.keys())

    @property
    def dataset(self) -> Callable:
        if self._dataset is None:
            self._dataset = _get_dataset_dependency(self._obj)
        return self._dataset

    def init_router(self):
        self._router = APIRouter()

    @property
    def router(self) -> APIRouter:
        if self._router is None:
            self.init_router()
        return self._router
