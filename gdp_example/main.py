# %%
# %%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, shape

# Load EEZ shapefile /example_data as a GeoDataFrame
# Replace with the actual path to your shapefile
shapefile_path = "/workspace/example_data/eez_v12.shp"
eez_gdf = gpd.read_file(shapefile_path)


# %%
# Read the CSV /example_data into a Pandas DataFrame
underwater = pd.read_csv("/workspace//example_data/underwater.csv")

# Convert the X and Y columns to a list of shapely Point objects
underwater['geometry'] = underwater.apply(lambda x: Point((float(x.longitude), float(x.latitude))), axis=1)
underwater = underwater.dropna(subset=['geometry'])
# get lat long from point 

# Create a GeoDataFrame from the ports DataFrame
underwater_gdf = gpd.GeoDataFrame(underwater, geometry='geometry')
within_shape = underwater_gdf.sjoin(eez_gdf, how='left',predicate='within')

print(within_shape.columns)

# rename Index Right to EEZ and if it has a value replace it to true if it does not then false
within_shape['EEZ'] = within_shape['index_right'].apply(lambda x: True if x >= 0 else False)
within_shape = within_shape.drop(columns=['index_right'])


within_shape.to_csv("/workspace//example_data/underwater_eez_6.csv", index=False)



