from datetime import datetime
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'GPSInfo':
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    result = {
        'camera': get_camera(exif_data),
        'lens': get_lens(exif_data),
        'location': get_location(exif_data),
        'datetime': get_datetime(exif_data),
        'raw_data': exif_data
    }
    return result


def get_datetime(exif_data):
    return datetime.strptime(
        str(exif_data.get('DateTimeOriginal')), '%Y:%m:%d %H:%M:%S'
    )


def get_camera(exif_data):
    result = None
    make = exif_data.get('Make')
    model = exif_data.get('Model')

    if make or model:
        if make and model:
            result = '%s %s' % (make, model)
        elif make:
            result = make
        else:
            result = model

    return result.replace('\x00', '') \
        if result is not None else None


def get_lens(exif_data):
    result = None
    make = exif_data.get('LensMake')
    model = exif_data.get('LensModel')

    if make or model:
        if make and model:
            result = '%s %s' % (make, model)
        elif make:
            result = make
        else:
            result = model

    return result.replace('\x00', '') \
        if result is not None else None


def get_location(exif_data):
    lat = None
    lng = None

    gps_info = exif_data.get('GPSInfo')
    if gps_info is not None:
        gps_latitude = gps_info.get('GPSLatitude')
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and \
                gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            if gps_latitude_ref != 'N':
                lat = 0 - lat

            lng = convert_to_degrees(gps_longitude)
            if gps_longitude_ref != 'E':
                lng = 0 - lng

    return '%s, %s' % (lat, lng) \
        if lat is not None and lng is not None else None


def convert_to_degrees(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)
