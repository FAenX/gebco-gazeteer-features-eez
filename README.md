# Project Title: Underwater Data EEZ Assignment

## Description
This project processes underwater data to determine whether each point lies within an Exclusive Economic Zone (EEZ). The data is processed using Pandas and GeoPandas libraries to achieve spatial joins between underwater data points and EEZ boundaries.

## File Structure
```
project-root/
│
├── example_data/
│   ├── eez_v12.shp
│   ├── underwater.csv
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
2. **Read Underwater CSV Data**: Loads underwater data from a CSV file into a Pandas DataFrame.
3. **Convert Coordinates to Geometries**: Converts the longitude and latitude columns into Shapely Point objects and creates a new GeoDataFrame.
4. **Spatial Join**: Performs a spatial join to determine whether each underwater data point is within an EEZ boundary.
5. **Flag EEZ Points**: Adds a new column to flag points within an EEZ.
6. **Save Output**: Writes the resulting DataFrame to a new CSV file.

```python
# main.py

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, shape

# Load EEZ shapefile as a GeoDataFrame
shapefile_path = "/workspace/example_data/eez_v12.shp"
eez_gdf = gpd.read_file(shapefile_path)

# Read the CSV data into a Pandas DataFrame
underwater = pd.read_csv("/workspace/example_data/underwater.csv")

# Convert the longitude and latitude columns to Shapely Point objects
underwater['geometry'] = underwater.apply(lambda x: Point((float(x.longitude), float(x.latitude))), axis=1)
underwater = underwater.dropna(subset=['geometry'])

# Create a GeoDataFrame from the underwater DataFrame
underwater_gdf = gpd.GeoDataFrame(underwater, geometry='geometry')
within_shape = underwater_gdf.sjoin(eez_gdf, how='left', predicate='within')

# Rename 'index_right' to 'EEZ' and set it to True if it has a value, otherwise False
within_shape['EEZ'] = within_shape['index_right'].apply(lambda x: True if x >= 0 else False)
within_shape = within_shape.drop(columns=['index_right'])

# Save the resulting DataFrame to a new CSV file
within_shape.to_csv("/workspace/example_data/underwater_eez_6.csv", index=False)
```

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