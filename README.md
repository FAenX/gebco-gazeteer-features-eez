# Project Title: Features Data EEZ Assignment

## Description
This project processes features data to determine whether each point lies within an Exclusive Economic Zone (EEZ). The data is processed using Pandas and GeoPandas libraries to achieve spatial joins between features data points and EEZ boundaries.

## File Structure
```
project-root/
│
├── example_data/
│   ├── eez_v12.shp
|   |-- eez_v12.shx
│   ├── features.csv
│
├── gdp_example/
│   ├── main.py
│
├── README.md
```

## Script Details

### main.py
The script `main.py` performs the following tasks:
1. **Load EEZ Shapefile**: Reads the EEZ shapefile into a GeoDataFrame using GeoPandas.
2. **Read Features CSV Data**: Loads features data from a CSV file into a Pandas DataFrame.
3. **Convert Coordinates to Geometries**: Converts the longitude and latitude columns into Shapely Point objects and creates a new GeoDataFrame.
4. **Spatial Join**: Performs a spatial join to determine whether each features data point is within an EEZ boundary.
5. **Flag EEZ Points**: Adds a new column to flag points within an EEZ.
6. **Save Output**: Writes the resulting DataFrame to a new CSV file.

```python
# main.py

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
```

## Data Sources
- **Features Data**: The features data is stored in a CSV file with columns for `longitude` and `latitude`.
- **EEZ Shapefile**: The Exclusive Economic Zone (EEZ) boundaries are stored in a shapefile format. The shapefile contains polygons representing the EEZ boundaries of different countries.

- **Features Data Source**: [NOAA National Centers for Environmental Information](https://www.ngdc.noaa.gov/gazetteer/)






## How to Run
1. Ensure you have the required data files in the `example_data` directory.
2. Install the necessary Python packages:
    ```bash
    pip install pandas geopandas shapely
    ```
3. Run the script:
    ```bash
    python scripts/main.py
    ```

## Future Development
- **Testing**: Implement unit tests for each function.
- **Data Validation**: Add data validation to ensure correct data types and non-null values.
- **Error Handling**: Enhance error handling for file reading and data processing steps.
- **Performance Optimization**: Investigate and apply optimizations for handling large datasets.
- **Visualization**: Add functionality to visualize the points and EEZ boundaries on a map.