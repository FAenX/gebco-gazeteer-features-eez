# %%
# %%
import pandas as pd
import geopandas as gpd
from shapely import wkt

# Load EEZ shapefile /example_data as a GeoDataFrame
# Replace with the actual path to your shapefile
shapefile_path = "/gdp_example/example_data/eez_v12.shp"
eez_gdf = gpd.read_file(shapefile_path)


# %%
# Read the CSV /example_data into a Pandas DataFrame
features = pd.read_csv("/gdp_example/example_data/features.csv")
print(features.columns)
print(features["Coordinates"].head())

# Convert the X and Y columns to a list of shapely Point objects
features['geometry'] = features['Coordinates'].apply(wkt.loads)
features = features.dropna(subset=['geometry'])
# # get lat long from point 

# # Create a GeoDataFrame from the ports DataFrame
features_gdf = gpd.GeoDataFrame(features, geometry='geometry')
within_shape = features_gdf.sjoin(eez_gdf, how='left',predicate='within')

print(within_shape.columns)

# rename Index Right to EEZ and if it has a value replace it to true if it does not then false
within_shape['EEZ'] = within_shape['index_right'].apply(lambda x: True if x >= 0 else False)
within_shape = within_shape.drop(columns=['index_right'])

# new column with all geometry converted to points
within_shape['point'] = within_shape['geometry'].apply(lambda x: x.centroid)

# get lat long from Point
within_shape['Latitude'] = within_shape['point'].apply(lambda x: x.y)
within_shape['Longitude'] = within_shape['point'].apply(lambda x: x.x)


within_shape.to_csv("/gdp_example/example_data/features_eez_6.csv", index=False)



