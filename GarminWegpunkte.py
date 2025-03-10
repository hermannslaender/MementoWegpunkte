import gpxpy
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import webbrowser


def send_to_Memento():
    pass


def check_table(*args):
    print(f'Einträge: {len(table.get_children())}')
    match len(table.get_children()):
        case 0:
            btn_delete.config(state=tk.DISABLED)
            return lbl_hint.config(text='keine Daten geladen')
        case 1:
            btn_delete.config(state=tk.NORMAL)
            return lbl_hint.config(text=f'{len(table.get_children())} Wegpunkt, Doppelklick für Karte')
        case _:
            btn_delete.config(state=tk.NORMAL)
            return lbl_hint.config(text=f'{len(table.get_children())} Wegpunkte, Doppelklick für Karte')


def open_map(event):
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
            comment = waypoints[i].comment if waypoints[i].comment else ''
            data = (name, symbol, latitude, longitude, comment)
            table.insert(parent="", index=tk.END, values=data, tags=('font',))
            print()

        check_table()


def delete_selected():
    selected_items = table.selection()
    print(f'{selected_items = }')
    for item in selected_items:
        table.delete(item)


window = tk.Tk()
window.geometry('1100x600')

window.title('GarminWegpunkte')
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 8, 'bold'),)

table = ttk.Treeview(window, columns = ('name', 'symbol', 'latitude', 'longitude', 'comment', 'dummy'), show = 'headings')
table.tag_configure('font', font=('Helvetica', 12))
table.heading('name', text = " Name", anchor=tk.W)
table.heading('symbol', text = " Symbol", anchor=tk.W)
table.heading('latitude', text = "Latitude", anchor=tk.S)
table.heading('longitude', text = "Longitude", anchor=tk.S)
table.heading('comment', text = " Bemerkung", anchor=tk.W)

table.column('name', anchor=tk.W, width=250)
table.column('symbol', anchor=tk.W, width=200)
table.column('latitude', anchor=tk.S, width=120)
table.column('longitude',anchor=tk.S, width=120)
table.column('comment',anchor=tk.W, width=400)
table.column('dummy',anchor=tk.E, width=5)

scrollbar = ttk.Scrollbar(table, orient='vertical', command=table.yview)
scrollbar.pack(side='right', fill='y')
table.configure(yscrollcommand=scrollbar.set)

btn_load = ttk.Button(window, text='Datei laden', command=load_gpx)
btn_delete = ttk.Button(window, text='markierte Zeilen löschen', command=delete_selected)
btn_Memento = ttk.Button(window, text='Liste an Memento senden', command=send_to_Memento)

lbl_hint = ttk.Label(window, text='keine Daten geladen')

table.pack(expand=True, fill="both")
lbl_hint.pack()
btn_load.pack(side='left', padx=10, pady=10)
btn_delete.pack(side='left', padx=10, pady=10)
btn_delete.config(state=tk.DISABLED)
btn_Memento.pack(side='left', padx=10, pady=10)
btn_Memento.config(state=tk.DISABLED)


table.bind('<Double-1>', open_map)
table.bind('<<TreeviewSelect>>', check_table)

window.mainloop()
