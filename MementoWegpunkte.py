import requests
import xml.etree.ElementTree as ET
from MementoToken import MEMENTO_TOKEN

# API-Endpunkte
WAYPOINTS_API_URL = f'https://api.mementodatabase.com/v1/libraries/2jwnhsD0k/search?token={MEMENTO_TOKEN}&fields=0,31,1,15,27,28&q=status:active&pageSize=200'
SYMBOLS_API_URL = f'https://api.mementodatabase.com/v1/libraries/XPiUCnkr2/search?token={MEMENTO_TOKEN}&fields=0&q=status:active&pageSize=200'
MAPPING_WAYPOINTS = {0: 'name', 31: 'comment', 1: 'type', 15: 'icon', 27: 'latitude', 28: 'longitude'}

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
    field_names = ['name', 'comment', 'type', 'symbol', 'latitude', 'longitude']
    
    for entry in data:
        fields = entry['fields']
        transformed_fields = []
        
        for idx, field in enumerate(fields):
            field_name = field_names[idx]
            transformed_fields.append({field_name: field['value']})
        
        entry['fields'] = transformed_fields
    
    return data

def create_gpx(data, filename):
    gpx = ET.Element('gpx')
    for loc in data:
        wpt = ET.SubElement(gpx, 'wpt', lat=str(loc['fields'][4]['latitude']), lon=str(loc['fields'][5]['longitude']))
        name = ET.SubElement(wpt, 'name')
        name.text = loc['fields'][0]['name']
        cmt = ET.SubElement(wpt, 'cmt')
        cmt.text = loc['fields'][1]['comment']
        sym = ET.SubElement(wpt, 'sym')
        sym.text = loc['fields'][3]['symbol']
        typ = ET.SubElement(wpt, 'type')
        typ.text = 'Memento'
        
    tree = ET.ElementTree(gpx)
    with open(filename, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)    
        
    return gpx

def main():
    waypoints = fetch_data(WAYPOINTS_API_URL)
    symbols = fetch_data(SYMBOLS_API_URL)
    
    updated_waypoints = update_waypoints_with_symbols(waypoints, symbols)
    transformed_waypoints = transform_data(updated_waypoints)
    create_gpx(transformed_waypoints, 'D:\\OneDrive\\Dokumente\\GeoCaching\\gpx\\MementoWegpunkte.gpx')
    
    print("Aktualisierte Wegpunkte:")
    print(transformed_waypoints)

if __name__ == "__main__":
    main()
