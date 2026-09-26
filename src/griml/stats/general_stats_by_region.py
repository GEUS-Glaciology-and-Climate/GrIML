import geopandas as gpd
import numpy as np

gdf = gpd.read_file("misc/iml_2016-2025/final_v4/ALL-ESA-GRIML-IML-fv4.gpkg")


regions = ["CE", "CW", "NE", "NO", "NW", "SE", "SW"]

for r in regions:
    gdf_r = gdf[gdf["region"]==r]
    gdf_r_is = gdf_r[gdf_r["margin"]=="ICE_SHEET"]
    gdf_r_pgic = gdf_r[gdf_r["margin"]=="ICE_CAP"]
    print(f"\n\n{r} lake abundance")
    print("IS: " + str(len(gdf_r_is)))
    print("PGIC: " + str(len(gdf_r_pgic)))
    print("All: " + str(len(gdf_r)))
    print(f"\n{r} total lake area")
    print("IS: " + str(sum(list(gdf_r_is["area_all"]))))
    print("PGIC: " + str(sum(list(gdf_r_pgic["area_all"]))))
    print("All: " + str(sum(list(gdf_r["area_all"]))))
    print(f"\n{r} median lake area")
    print("IS: " + str(np.nanmedian(list(gdf_r_is["area_all"]))))
    print("PGIC: " + str(np.nanmedian(list(gdf_r_pgic["area_all"]))))
    print("All: " + str(np.nanmedian(list(gdf_r["area_all"]))))
    print(f"\n{r} number of GLOF lakes")
    print("IS: " + str(len(gdf_r_is[gdf_r_is["glof_lake"]=="Yes"])))
    print("PGIC: " + str(len(gdf_r_pgic[gdf_r_pgic["glof_lake"]=="Yes"])))
    print("All: " + str(len(gdf_r[gdf_r["glof_lake"]=="Yes"])))
    print(f"\n{r} average surface temperature")
    print("IS: " + str(np.nanmean(list(gdf_r_is["t_aver_all"]))))
    print("PGIC: " + str(np.nanmean(list(gdf_r_pgic["t_aver_all"]))))
    print("All: " + str(np.nanmean(list(gdf_r["t_aver_all"]))))
