import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

def create_us_map():
    """Create an interactive map of US facilities and save as HTML"""
    
    try:
        # Load the CSV file
        df = pd.read_csv('facilities.csv')
        print(f"Loaded {len(df)} total facilities")
        
        # Display column names to help with debugging
        print("CSV columns:", df.columns.tolist())
        
        # Common column name variations - adjust these based on your CSV structure
        lat_columns = ['latitude', 'lat', 'Latitude', 'LAT', 'y', 'Y']
        lon_columns = ['longitude', 'lon', 'lng', 'Longitude', 'LON', 'LONGITUDE', 'x', 'X']
        name_columns = ['site_name', 'name', 'facility_name', 'site', 'Site', 'Name', 'facility']
        address_columns = ['address', 'Address', 'full_address', 'location', 'street_address']
        
        # Find the correct column names
        lat_col = next((col for col in lat_columns if col in df.columns), None)
        lon_col = next((col for col in lon_columns if col in df.columns), None)
        name_col = next((col for col in name_columns if col in df.columns), None)
        address_col = next((col for col in address_columns if col in df.columns), None)
        
        if not lat_col or not lon_col:
            print("Error: Could not find latitude/longitude columns")
            print("Available columns:", df.columns.tolist())
            return False
            
        print(f"Using columns - Lat: {lat_col}, Lon: {lon_col}, Name: {name_col}, Address: {address_col}")
        
        # Clean and convert coordinates
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
        
        # Remove rows with invalid coordinates
        df = df.dropna(subset=[lat_col, lon_col])
        print(f"After cleaning coordinates: {len(df)} facilities")
        
        # Filter for United States coordinates
        # Continental US + Alaska + Hawaii bounds
        us_df = df[
            (df[lat_col] >= 18.0) & (df[lat_col] <= 72.0) &  # Includes Alaska and Hawaii
            (df[lon_col] >= -180.0) & (df[lon_col] <= -65.0)
        ].copy()
        
        print(f"US facilities found: {len(us_df)}")
        
        # Optional: Filter by status (uncomment the lines below if you want only specific statuses)
        # FILTER OPTIONS - Uncomment ONE of these if desired:
        
        # Option 1: Only idle sites
        # us_df = us_df[us_df['status'].str.lower() == 'idle']
        # print(f"Idle facilities: {len(us_df)}")
        
        # Option 2: Only active sites  
        # us_df = us_df[us_df['status'].str.lower() == 'active']
        # print(f"Active facilities: {len(us_df)}")
        
        # Option 3: Exclude certain statuses
        # us_df = us_df[~us_df['status'].str.lower().isin(['closed', 'inactive'])]
        # print(f"Open facilities: {len(us_df)}")
        
        # Show status breakdown
        if 'status' in us_df.columns:
            print("\nStatus breakdown:")
            status_counts = us_df['status'].value_counts()
            for status, count in status_counts.items():
                print(f"  {status}: {count}")
            print()
        
        if len(us_df) == 0:
            print("No facilities found in US coordinate range")
            return False
        
        # Prepare hover text
        hover_data = {}
        hover_name = None
        
        if name_col and name_col in us_df.columns:
            hover_name = name_col
            hover_data[name_col] = False  # Don't show in hover data since it's the hover_name
        
        if address_col and address_col in us_df.columns:
            hover_data[address_col] = True
            
        # Always hide coordinates from hover
        hover_data[lat_col] = False
        hover_data[lon_col] = False
        
        # Create the interactive map using the new scatter_map function
        fig = px.scatter_map(
            us_df,
            lat=lat_col,
            lon=lon_col,
            hover_name=hover_name,
            hover_data=hover_data,
            zoom=3,
            height=700,
            title="US Facility Locations"
        )
        
        # Update map style and layout
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            title={
                'text': "Interactive Map of US Facilities",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            }
        )
        
        # Update marker appearance (removed invalid 'line' property)
        fig.update_traces(
            marker=dict(
                size=10,
                color='red',
                opacity=0.7
            )
        )
        
        # Save the map as HTML
        fig.write_html("location_map.html")
        print("Map saved as location_map.html")
        
        # Also show the map if running interactively
        # fig.show()
        
        return True
        
    except FileNotFoundError:
        print("Error: facilities.csv file not found")
        return False
    except Exception as e:
        print(f"Error creating map: {str(e)}")
        return False

if __name__ == "__main__":
    print("Creating California facilities map...")
    success = create_us_map()
    
    if success:
        print("\nCalifornia map creation completed successfully!")
        print("Files created:")
        print("- location_map.html (interactive California map)")
    else:
        print("\nMap creation failed. Please check your CSV file and try again.")