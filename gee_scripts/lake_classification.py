import ee

# Initialize the Earth Engine API
ee.Initialize()

print('Commencing script run')

#--------------------------------------------------------------------------
# DEFINE VARIABLES

date1 = '2016-07-01'
date2 = '2016-08-31'

# Define the Area of Interest (AOI)
aoi = ee.FeatureCollection('users/pennyruthhow/greenland_coastline')
featcol = ee.FeatureCollection('users/pennyruthhow/greenland_rectangle_mask')

print(f'Searching for images... Date range: {date1} - {date2}, Cloud percentage: 20')

#--------------------------------------------------------------------------
# Sentinel-2 classification

# Function to mask clouds from Sentinel-2 imagery
def maskS2clouds(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    # Both cloud and cirrus flags should be 0 for clear conditions
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

# Search for Sentinel-2 images
dataset_s2 = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
                .filterDate(date1, date2) \
                .filterBounds(aoi) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(maskS2clouds)

# Select bands
blue = 'B2'
green = 'B3'
red = 'B4'
vnir = 'B8'
swir1 = 'B11'
swir2 = 'B12'

# Mean reducer
image = dataset_s2.select([blue, green, red, vnir, swir1, swir2]).reduce(ee.Reducer.mean())

# Resample SWIR bands
sw = image.select([swir1 + '_mean', swir2 + '_mean']).resample('bilinear')\
          .reproject(crs='EPSG:4326', scale=10).rename(['B11_mean_1', 'B12_mean_1'])

# Add bands and print band names
image = image.addBands(sw)
print(image.bandNames().getInfo())

# Create water indices
ndwi = image.normalizedDifference([green + '_mean', vnir + '_mean'])
mndwi = image.normalizedDifference([green + '_mean', swir1 + '_mean_1'])

AWEIsh = image.expression(
    'BLUE + 2.5 * GREEN - 1.5 * (VNIR + SWIR1) - 0.25 * SWIR2', {
        'BLUE': image.select(blue + '_mean'),
        'GREEN': image.select(green + '_mean'),
        'SWIR1': image.select(swir1 + '_mean_1'),
        'VNIR': image.select(vnir + '_mean'),
        'SWIR2': image.select(swir2 + '_mean_1')
    })

AWEInsh = image.expression(
    '4.0 * (GREEN - SWIR1) - (0.25 * VNIR + 2.75 * SWIR2)', {
        'GREEN': image.select(green + '_mean'),
        'SWIR1': image.select(swir1 + '_mean_1'),
        'VNIR': image.select(vnir + '_mean'),
        'SWIR2': image.select(swir2 + '_mean_1')
    })

bright = image.expression(
    '(RED + GREEN + BLUE) / 3', {
        'BLUE': image.select(blue + '_mean'),
        'GREEN': image.select(green + '_mean'),
        'RED': image.select(red + '_mean')
    })

# Classify Sentinel-2 lakes
s2_lakes = image.expression(
    "(BRIGHT > 5000) ? 0 : (NDWI > 0.3) ? 1 : (MNDWI < 0.1) ? 0 : "
    "(AWEISH < 2000) ? 0 : (AWEISH > 5000) ? 0 : "
    "(AWEINSH < 4000) ? 0 : (AWEINSH > 6000) ? 0 : 1", {
        'NDWI': ndwi,
        'MNDWI': mndwi,
        'AWEISH': AWEIsh,
        'AWEINSH': AWEInsh,
        'BRIGHT': bright
    }).rename('s2_lakes').toByte()

s2_lakes = s2_lakes.updateMask(s2_lakes)

print('S2 scenes classified')

#--------------------------------------------------------------------------
# Sentinel-1 lakes classification

# Search for Sentinel-1 images
dataset_s1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
                .filterDate(date1, date2) \
                .filterBounds(aoi) \
                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'HH')) \
                .filter(ee.Filter.eq('instrumentMode', 'IW'))

# Create smooth mosaic
aver = dataset_s1.select('HH').mosaic()
smooth = aver.focal_median(50, 'circle', 'meters')

# Classify lakes based on Sentinel-1
s1_lakes = smooth.lt(-20).rename('s1_lakes').toByte()
s1_lakes = s1_lakes.updateMask(s1_lakes)

print('S1 scenes classified')

#--------------------------------------------------------------------------
# DEM lakes classification

# Load DEM data and process
dem = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic').clip(aoi)
elev = dem.select('elevation').focal_median(110, 'circle', 'meters').toInt64()

fill = ee.Terrain.fillMinima(elev, 10, 50)
diff = fill.subtract(elev)
dem_lakes = diff.gt(0).rename('dem_lakes').toByte()

dem_lakes = dem_lakes.focal_median(50, 'circle', 'meters').updateMask(dem_lakes)

print('DEM scenes classified')

#--------------------------------------------------------------------------
# Combine all lakes and export

# Combine layers
all_lakes = s2_lakes.addBands([s1_lakes.select('s1_lakes'), dem_lakes.select('dem_lakes')])
print('All lakes combined')

# Clip and reproject the combined image
clip_lakes = all_lakes.clip(featcol.first()).reproject(crs='EPSG:3413', scale=10)

# Get projection info
projection = clip_lakes.select('s2_lakes').projection().getInfo()
print('All lakes clipped and reprojected')
print(projection)

# Export the image to Google Drive
task = ee.batch.Export.image.toDrive(
    image=clip_lakes,
    description='lakes',
    folder='out',
    region=featcol.first().geometry(),
    scale=10,
    crs=projection['crs'],
    crsTransform=projection['transform'],
    maxPixels=1e13
)
task.start()

#--------------------------------------------------------------------------
print('Run finished')

