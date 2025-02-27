import requests
import json
import xml.etree.ElementTree as ET
from MementoToken import MEMENTO_TOKEN

# API-Endpunkte
WAYPOINTS_API_URL = f'https://api.mementodatabase.com/v1/libraries/2jwnhsD0k/search?token={MEMENTO_TOKEN}&fields=0,31,1,15,14,27,28&q=status:active&pageSize=200'
SYMBOLS_API_URL = f'https://api.mementodatabase.com/v1/libraries/XPiUCnkr2/search?token={MEMENTO_TOKEN}&fields=0&q=status:active&pageSize=200'
MAPPING_WAYPOINTS = {0: 'name', 31: 'comment', 1: 'type', 15: 'icon', 14: 'color', 27: 'latitude', 28: 'longitude'}

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['entries']

def update_waypoints_with_symbols(waypoints, symbols):
    symbol_dict = {symbol['id']: symbol['fields'][0]['value'] for symbol in symbols}
    
    for waypoint in waypoints:
        for field in waypoint['fields']:
            if field['id'] == 15:  # Feld "symbol"
                field['value'] = [symbol_dict.get(ref, ref) for ref in field['value']][0]
            
    return waypoints


def transform_data(data):
    field_names = ['name', 'comment', 'type', 'symbol', 'color', 'latitude', 'longitude']
    
    for entry in data:
        fields = entry['fields']
        transformed_fields = {}
        
        for idx, field in enumerate(fields):
            field_name = field_names[idx]
            transformed_fields |= {field_name: field['value']}
        
        entry['fields'] = transformed_fields
    
    return data


def create_gpx(data, filename):
    gpx = ET.Element('gpx')
    for loc in data:
        wpt = ET.SubElement(gpx, 'wpt', lat=str(loc['fields']['latitude']), lon=str(loc['fields']['longitude']))
        name = ET.SubElement(wpt, 'name')
        name.text = loc['fields']['name']
        cmt = ET.SubElement(wpt, 'cmt')
        cmt.text = loc['fields']['comment']
        sym = ET.SubElement(wpt, 'sym')
        sym.text = loc['fields']['symbol']
        typ = ET.SubElement(wpt, 'type')
        typ.text = 'Memento'
        
    tree = ET.ElementTree(gpx)
    with open(filename, 'wb') as gpx_file:
        tree.write(gpx_file, encoding='utf-8', xml_declaration=True)    
        
    return gpx


def create_json(data, filename):
    output = {
        "id": 1,
        "points": [],
        "polylines": []
    }
    
    for idx, item in enumerate(data):
        point = {
            "uid": str(idx + 1),
            "name": item['fields']['name'],
            "lat": item['fields']['latitude'],
            "lon": item['fields']['longitude'],
            "format": "coords_dmm",
            "color": item['fields']['color'],
            "edit": True
        }
        output["points"].append(point)
        
    with open(filename, 'w') as json_file:
        json.dump(output, json_file, indent=4)

    return output


def main():
    waypoints = fetch_data(WAYPOINTS_API_URL)
    symbols = fetch_data(SYMBOLS_API_URL)
    
    updated_waypoints = update_waypoints_with_symbols(waypoints, symbols)
    transformed_waypoints = transform_data(updated_waypoints)
    
    create_gpx(transformed_waypoints, 'D:\\OneDrive\\Dokumente\\GeoCaching\\gpx\\MementoWegpunkte.gpx')
    create_json(transformed_waypoints, 'D:\\OneDrive\\Dokumente\\GeoCaching\\gpx\\MementoWegpunkte.json')
    
    print("Aktualisierte Wegpunkte:")
    print(transformed_waypoints)

if __name__ == "__main__":
    main()
