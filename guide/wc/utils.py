def get_features(data):
    return data.get('features', [])


def get_properties(feature):
    return feature.get('properties', {})


def get_type(properties):
    if is_type_iv(properties):
        return 'iv'
    if is_type_pissoir(properties):
        return 'pissoir'
    return 'normal'


def is_type_pissoir(properties):
    is_urinal = has_urinal(properties)
    is_male = supports_male(properties)
    is_female = supports_female(properties)
    return is_urinal and is_male and not is_female


def supports_male(properties):
    return properties.get("male", "no") == "yes"


def supports_female(properties):
    return properties.get("female", "no") == "yes"


def has_urinal(properties):
    return 'urinal' in properties.get('toilets:position', '')


def is_type_iv(properties):
    return properties.get("wheelchair", "no") == "yes"


def has_access(properties):
    access = properties.get("access", "no")
    return access == "yes" or access == "public"


def has_changing_table(properties):
    return properties.get("changing_table", "no") == "yes"


def requires_fee(properties):
    return properties.get("fee", "no") == "yes"


def is_nette_toilette(properties):
    name = str(get_name(properties)).lower()
    description = str(get_description(properties)).lower()
    nette_toilette = 'nette toilette'
    return name == nette_toilette or description == nette_toilette


def get_name(properties):
    return properties.get("name", None)


def get_operator(properties):
    return properties.get("operator", None)


def get_description(properties):
    return properties.get("description", None)


def get_osm_id(feature):
    return feature.get("id", None)


def get_geometry(feature):
    return feature.get("geometry", None)


def get_line_string_center(coordinates):
    lon, lat = 0, 0
    for coordinate in coordinates:
        lon += coordinate[0]
        lat += coordinate[1]
    return [lon / len(coordinates), lat / len(coordinates)]


def get_polygon_center(coordinates):
    polygons = [get_line_string_center(polygon) for polygon in coordinates]
    return get_line_string_center(polygons)


def get_multipolygon_center(coordinates):
    polygons = [get_polygon_center(polygon) for polygon in coordinates]
    return get_line_string_center(polygons)


def geometry_to_point(geometry):
    geometry_type = str(geometry.get("type", None)).lower()
    coordinates = geometry.get("coordinates", None)
    if len(coordinates) == 0:
        return None

    if geometry_type == "point":
        return geometry
    if geometry_type == "linestring":
        return {
            "type": "Point",
            "coordinates": get_line_string_center(coordinates)
        }
    if geometry_type == "polygon":
        return {
            "type": "Point",
            "coordinates": get_polygon_center(coordinates)
        }
    if geometry_type == "multipolygon":
        return {
            "type": "Point",
            "coordinates": get_multipolygon_center(coordinates)
        }
    return None


def transform_feature(feature):
    properties = get_properties(feature)
    geometry = get_geometry(feature=feature)
    return {
        "type": "Feature",
        "geometry": geometry_to_point(geometry),
        "properties": {
            "id": get_osm_id(feature=feature),
            "type": get_type(properties=properties),
            "description": get_description(properties=properties),
            "name": get_name(properties=properties),
            "operator": get_operator(properties=properties),
            "access": has_access(properties=properties),
            "features":
                {
                    "wickeltisch": has_changing_table(properties=properties),
                    "kostenpflichtig": requires_fee(properties=properties),
                    "nettetoilette": is_nette_toilette(properties=properties)
                },
        }
    }


def transform_geojson(data):
    features = get_features(data=data)
    transformed_features = [transform_feature(feature) for feature in features]
    return {
        "count": len(transformed_features),
        "next": None,
        "previous": None,
        "results": {
            "type": "FeatureCollection",
            "features": transformed_features
        }
    }
