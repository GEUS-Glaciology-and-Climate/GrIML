import ee

# Initialize the Earth Engine API
ee.Initialize()

#****************** CLOUD MASK FUNCTION *****************#
def cloudMask(image):
    qa = image.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 3).Or(qa.bitwiseAnd(1 << 4))
    return image.updateMask(mask.Not())

#****************** GET IMAGERY FUNCTION *****************#
def getImages(aoi):
    L9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')\
        .select(['ST_B10', 'QA_PIXEL'], ['ST', 'QA_PIXEL'])\
        .filterBounds(aoi)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))\
        .map(cloudMask)

    L8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')\
        .select(['ST_B10', 'QA_PIXEL'], ['ST', 'QA_PIXEL'])\
        .filterBounds(aoi)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))\
        .map(cloudMask)

    L7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')\
        .select(['ST_B6', 'QA_PIXEL'], ['ST', 'QA_PIXEL'])\
        .filterBounds(aoi)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))\
        .map(cloudMask)

    L5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')\
        .select(['ST_B6', 'QA_PIXEL'], ['ST', 'QA_PIXEL'])\
        .filterBounds(aoi)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))\
        .map(cloudMask)

    L4 = ee.ImageCollection('LANDSAT/LT04/C02/T1_L2')\
        .select(['ST_B6', 'QA_PIXEL'], ['ST', 'QA_PIXEL'])\
        .filterBounds(aoi)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))\
        .map(cloudMask)

    return L9.merge(L8).merge(L7).merge(L5).merge(L4)

#********* DERIVE ST FUNCTION ******************#
def applyWaterCorrection(image):
    waterBands = image.select('ST').multiply(0.00341802).add(149.0)\
                  .multiply(0.806).add(54.37).subtract(273.15)
    return image.addBands(waterBands, None, True)

#************ DERIVE AND ACCUMULATE FUNCTION ******************#
def getST(feature, lake_id):
    aoi = feature.geometry()
    pt = aoi.buffer(-30)

    landsatWT = getImages(aoi).map(applyWaterCorrection)

    def process_image(image):
        return ee.Feature(None, image.reduceRegion(ee.Reducer.mean(), pt, 30))\
                .set('lake_id', lake_id)\
                .set('system:time_start', image.get('system:time_start'))\
                .set('system:index', image.get('system:index'))\
                .set('date', ee.Date(image.get('system:time_start')).format('yyyy-MM-dd'))\
                .set('ST_max', image.reduceRegion(ee.Reducer.max(), pt, 30).get('ST'))\
                .set('ST_min', image.reduceRegion(ee.Reducer.min(), pt, 30).get('ST'))\
                .set('ST_stddev', image.reduceRegion(ee.Reducer.stdDev(), pt, 30).get('ST'))\
                .set('ST_count', image.reduceRegion(ee.Reducer.count(), pt, 30).get('ST'))

    values = landsatWT.map(process_image)
    return values

#************ BATCH PROCESSING FUNCTION ******************#
def process_batch(lake_ids, batch_number):
    all_values = ee.FeatureCollection([])

    for lake_id in lake_ids:
        feature = table.filter(ee.Filter.eq('lake_id', lake_id)).first()
        values = getST(feature, lake_id)
        all_values = all_values.merge(values)

    # Generate a unique filename for each batch
    file_name = f'lake_timeseries_batch_{batch_number}'

    task = ee.batch.Export.table.toDrive(
        collection=all_values,
        description=file_name,
        folder='ST_IIML_poly',
        fileFormat='CSV',
        selectors=['lake_id', 'system:time_start', 'date', 'system:index', 'ST', 'ST_max', 'ST_min', 'ST_stddev', 'ST_count', 'QA_PIXEL']
    )
    task.start()

#************ ITERATE OVER ALL LAKES IN BATCHES AND EXPORT WITH UNIQUE NAMES ******************#
def export_in_batches():
    # Fetch the lake IDs from the table
    lake_ids = table.aggregate_array('lake_id').getInfo()
    batch_size = 50  # Adjust batch size as necessary
    batch_number = 0

    for i in range(0, len(lake_ids), batch_size):
        batch_ids = lake_ids[i:i + batch_size]
        batch_number += 1
        process_batch(batch_ids, batch_number)

# Load your FeatureCollection (replace with the appropriate variable or asset path)
table = ee.FeatureCollection('users/your_username/your_asset')  # Example asset path

# Run the batch export
export_in_batches()

