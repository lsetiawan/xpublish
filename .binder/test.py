import xarray as xr
from dask.distributed import Client

import xpublish  # noqa: F401
from xpublish.routers import APIRouterWrapper
from fastapi import Depends

if __name__ == "__main__":

    client = Client(n_workers=4, dashboard_address=8787)
    print(client.cluster)
    print(client.cluster.dashboard_link)

    ds = xr.tutorial.open_dataset("air_temperature", chunks=dict(lat=5, lon=5), decode_cf=False)
    print(ds)

    ds.rest.serve()

    # === Multiple datasets =================
    # class DatasetRouters(APIRouterWrapper):
    #     """A simple example."""

    #     def init_router(self):
    #         super().init_router()

    #         @self._router.get("/dims")
    #         def get_dims(dataset: xr.Dataset = Depends(self.dataset)):
    #             return dataset.dims

    # routers = DatasetRouters(
    #     {
    #         'air_temp': xr.tutorial.open_dataset(
    #             "air_temperature", chunks=dict(lat=5, lon=5), decode_cf=False
    #         ),
    #         'rasm': xr.tutorial.open_dataset("rasm", decode_cf=False),
    #     }
    # )

    # xr.Dataset.rest(routers=routers).serve()
    # ========================================
