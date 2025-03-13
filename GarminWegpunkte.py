import gpxpy
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import requests
from MementoToken import MEMENTO_TOKEN
WAYPOINTS_API_URL = f'https://api.mementryodatabase.com/v1/libraries/2jwnhsD0k/entryries?token={MEMENTO_TOKEN}'


def save_waypoint_change(entry_name, entry_comment, entry_lat, entry_lon):
    name = entry_name.get()
    comment = entry_comment.get()
    lat = entry_lat.get()
    lon = entry_lon.get()
    print(f'speichern: {name = }   {comment = }   {lat = }    {lon = }')


def edit_selected():
    selected_item = table.selection()[0]
    values = table.item(selected_item, 'values')
    print(f'{values = }')
    name, comment, lat, lon = values[0], values[4], values[2], values[3]


    edit_window = tk.Tk()
    edit_window.geometry('600x220')

    edit_window.title('GarminWegpunkt bearbeiten')

    # Label und entry für Name
    label_name = ttk.Label(edit_window, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    entry_name = ttk.Entry(edit_window, width=30)
    entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="W")
    entry_name.insert(0, name)

    # Label und entry für Bemerkung
    label_comment = ttk.Label(edit_window, text="Bemerkung:")
    label_comment.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    entry_comment = ttk.Entry(edit_window, width=80)
    entry_comment.grid(row=1, column=1, padx=10, pady=10, sticky="W")
    entry_comment.insert(0, comment)
    
    # Label und entry für Latitude
    label_lat = ttk.Label(edit_window, text="Latitude:")
    label_lat.grid(row=2, column=0, padx=10, pady=10, sticky="W")
    entry_lat = ttk.Entry(edit_window, width=30)
    entry_lat.grid(row=2, column=1, padx=10, pady=10, sticky="W")
    entry_lat.insert(0, lat)

    # Label und entry für Longitude
    label_lon = ttk.Label(edit_window, text="Longitude:")
    label_lon.grid(row=3, column=0, padx=10, pady=10, sticky="W")
    entry_lon = ttk.Entry(edit_window, width=30)
    entry_lon.grid(row=3, column=1, padx=10, pady=10, sticky="W")
    entry_lon.insert(0, lon)

    btn_save = ttk.Button(edit_window, text='speichern', command=lambda: save_waypoint_change(entry_name, entry_comment, entry_lat, entry_lon))
    btn_save.grid(row=4, column =1, padx=10, pady=10, sticky="W")


def send_to_Mementryo(name = 'Test 1', commentry = 'Kommentryar 1', lat = 51.000000, lon = 8.000000):
    headers = {
        "Authorization": f"Bearer {MEMENTO_TOKEN}",
        "Contentry-Type": "application/json"
    }

    values = "{'fields':[{'id': 0,'value': '" + name + "'},{'id': 31,'value': '" + commentry + "'},{'id': 1,'value': 'neu'},{'id': 14,'value': '#ffffff'},{'id': 2,'value': 'Dezimal'},{'id': 10,'value': " + str(lat) + "},{'id': 11,'value': " + str(lon) + "}]}"
    #print(values)

    response = requests.post(WAYPOINTS_API_URL, headers=headers, data=values)

    if response.status_code == 201:
        print("Eintrag erfolgreich erstellt!")
        print("Antwort:", response.json())
        print()
    else:
        print("Fehler beim Erstellen des Eintrags.")
        print("Statuscode:", response.status_code)
        print("Antwort:", response.text)
        print()


def send_all_rows_from_table():
    while len(table.get_children()):
        first_id = table.get_children()[0]
        name = table.item(first_id, 'values')[0]
        commentry = table.item(first_id, 'values')[4]
        lat = table.item(first_id, 'values')[2]
        lon = table.item(first_id, 'values')[3]

        send_to_Mementryo(name, commentry, lat, lon)
        table.delete(first_id)

        check_table()


def check_table(*args):
    print(f'Einträge: {len(table.get_children())}', end="    ")
    print(f'Markiert: {len(table.selection())}')
    match len(table.get_children()):
        case 0:
            label_hint.config(text='keine Daten geladen')
        case 1:
            label_hint.config(text=f'{len(table.get_children())} Wegpunkt, Doppelklick für Karte')
        case _:
            label_hint.config(text=f'{len(table.get_children())} Wegpunkte, Doppelklick für Karte')

    match len(table.selection()):
        case 0:
            btn_delete.config(state=tk.DISABLED)
            btn_edit.config(state=tk.DISABLED)
        case 1:
            btn_delete.config(state=tk.NORMAL)
            btn_edit.config(state=tk.NORMAL)
        case _:
            btn_delete.config(state=tk.NORMAL)
            btn_edit.config(state=tk.DISABLED)


def open_map(eventry):
    selected_item = table.selection()[0]
    values = table.item(selected_item, 'values')
    lat, lon = values[2], values[3]
    print(f'{lat=}   ' + f'{lon=}')
    url = f'https://www.google.com/maps?q={lat},{lon}'
    webbrowser.open_new(url)


def load_gpx():
    gpx_file = filedialog.askopenfilename(title='Wähle eine Datei', filetypes=(('GPX-Datei', '*.gpx'), ('Alle Dateien', '*.*')))
    print(f'{gpx_file = }')

    if gpx_file:
        with open(gpx_file, 'r', encoding='utf-8') as gpx_file:
            waypoints = gpxpy.parse(gpx_file).waypoints
            print(f"{waypoints = }" + '\n')

        for i in range(len(waypoints)):
            print(f"{waypoints[i].name = }")
            print(f"{waypoints[i].symbol = }")
            print(f"{waypoints[i].latitude = }")
            print(f"{waypoints[i].longitude = }")
            print(f"{waypoints[i].comment = }")

            name = waypoints[i].name
            symbol = waypoints[i].symbol
            latitude = round(waypoints[i].latitude,6)
            longitude = round(waypoints[i].longitude,6)
            commentry = waypoints[i].comment if waypoints[i].comment else ''
            data = (name, symbol, latitude, longitude, commentry)
            table.insert(parent="", index=tk.END, values=data, tags=('font',))
            print()

        check_table()


def delete_selected():
    selected_items = table.selection()
    print(f'{selected_items = }')
    for item in selected_items:
        table.delete(item)

    check_table()



window = tk.Tk()
window.geometry('1100x600')

window.title('GarminWegpunkte')
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 8, 'bold'),)

table = ttk.Treeview(window, columns = ('name', 'symbol', 'latitude', 'longitude', 'commentry', 'dummy'), show = 'headings')
table.tag_configure('font', font=('Helvetica', 12))
table.heading('name', text = " Name", anchor=tk.W)
table.heading('symbol', text = " Symbol", anchor=tk.W)
table.heading('latitude', text = "Latitude", anchor=tk.S)
table.heading('longitude', text = "Longitude", anchor=tk.S)
table.heading('commentry', text = " Bemerkung", anchor=tk.W)

table.column('name', anchor=tk.W, width=250)
table.column('symbol', anchor=tk.W, width=200)
table.column('latitude', anchor=tk.S, width=120)
table.column('longitude',anchor=tk.S, width=120)
table.column('commentry',anchor=tk.W, width=400)
table.column('dummy',anchor=tk.E, width=5)

scrollbar = ttk.Scrollbar(table, orient='vertical', command=table.yview)
scrollbar.pack(side='right', fill='y')
table.configure(yscrollcommand=scrollbar.set)

btn_load = ttk.Button(window, text='Datei laden', command=load_gpx)
btn_delete = ttk.Button(window, text='markierte Zeilen löschen', command=delete_selected)
btn_edit = ttk.Button(window, text='markierten bearbeiten', command=edit_selected)
btn_Mementryo = ttk.Button(window, text='Liste an Mementryo senden', command=send_all_rows_from_table)

label_hint = ttk.Label(window, text='keine Daten geladen')

table.pack(expand=True, fill="both")
label_hint.pack()
btn_load.pack(side='left', padx=10, pady=10)
btn_delete.pack(side='left', padx=10, pady=10)
btn_delete.config(state=tk.DISABLED)
btn_edit.pack(side='left', padx=10, pady=10)
btn_edit.config(state=tk.DISABLED)
btn_Mementryo.pack(side='left', padx=10, pady=10)
btn_Mementryo.config(state=tk.DISABLED)

table.bind('<Double-1>', open_map)
table.bind('<<TreeviewSelect>>', check_table)

window.mainloop()
