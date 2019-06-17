# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
input_dir  = Path("data")
output_dir = Path("solution")
# 1. Go to http://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
#    and download the 0.25 deg. file for daily mean temperature.
#    Save the file into the data directory but don't commit it to github!!! [2P]
# 2. Read the file using xarray. Get to know your data. What's in the file?
#    Calculate monthly means for the reference periode 1981-2010 for Europe (Extent: Lon_min:-13, Lon_max: 25, Lat_min: 30, Lat_max: 72). [2P]
data = input_dir / "tg_ens_mean_0.25deg_reg_v19.0e.nc"
new_ds = xr.open_dataset(data)
croped_ds = new_ds.sel(latitude = slice(30,72), longitude = slice(-13,25), time = slice("1981-01-01","2010-12-31"))
croped_mean = croped_ds.groupby("time.month").mean("time")
# 3. Calculate monthly anomalies from the reference period for the year 2018 (use the same extent as in #2).
#    Make a quick plot of the anomalies for the region. [2P]
ds_2018 = new_ds.sel(latitude = slice(30,72), longitude = slice(-13,25), time = slice("2018","2018"))
mean_2018 = ds_2018.groupby("time.month").mean("time")
anomalies_2018 = mean_2018 - croped_mean 
anomalies_2018["tg"].plot()
# 4. Calculate the mean anomaly for the year 2018 for Europe (over all pixels of the extent from #2) 
#    Compare this overall mean anomaly to the anomaly of the pixel which contains Marburg. 
#    Is the anomaly of Marburg lower or higher than the one for Europe? [2P] 
croppe_mean_ts =  new_ds.sel(latitude = slice(30,72), longitude = slice(-13,25), time = slice("1981-01-01","2010-12-31")).mean("time")
cropped_mean_2018 =  new_ds.sel(latitude = slice(30,72), longitude = slice(-13,25), time = slice("2018","2018")).mean("time")
anomalies_all_2018 = cropped_mean_2018 - croppe_mean_ts
# Marburg, Geography, Deutschhausstraße 10, lat = 50.81, lon = 8.77
marburg_anomalies = anomalies_all_2018.sel(latitude = 50.81, longitude = 8.77, method = "nearest")
if marburg_anomalies > anomalies_all_2018:
    print("The anomaly of Marburg is higher than the one for Europe.")
else:
    print("The anomaly of Marburg is lower than the one for Europe.")
# 5. Write the monthly anomalies from task 3 to a netcdf file with name "europe_anom_2018.nc" to the solution directory.
#    Write the monthly anomalies for Marburg to a csv file with name "marburg_anom_2018.csv" to the solution directory. [2P]
anomalies_2018.to_netcdf(output_dir / "europe_anom_2018.nc")
marburg_anomalies_monthly = anomalies_2018.sel(latitude = 50.81, longitude = 8.77, method = "nearest")
mr_df = marburg_anomalies_monthly.to_dataframe()
mr_df.to_csv(output_dir / "marburg_anom_2018.csv")