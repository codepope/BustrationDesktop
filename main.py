import time
import json
import requests
from requests import Response
import tkinter as tk
from tkinter import ttk
import SECRETS

class BusArrivalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Arrivals")
        
        # Create frames for north and south bus stops
        self.north_frame = ttk.LabelFrame(root, text="Northbound", padding="10")
        self.north_frame.pack(fill="x", padx=5, pady=5)
        
        self.south_frame = ttk.LabelFrame(root, text="Southbound", padding="10")
        self.south_frame.pack(fill="x", padx=5, pady=5)
        
        # Labels for north direction
        self.north_bus = ttk.Label(self.north_frame, text="")
        self.north_bus.pack()
        self.north_time = ttk.Label(self.north_frame, text="")
        self.north_time.pack()
        
        # Labels for south direction
        self.south_bus = ttk.Label(self.south_frame, text="")
        self.south_bus.pack()
        self.south_time = ttk.Label(self.south_frame, text="")
        self.south_time.pack()
        
        # Time label
        self.time_label = ttk.Label(root, text="")
        self.time_label.pack(pady=5)
        
        # Start updating
        self.update_time_display()
        self.update_display()
        # Bring window to front
        self.root.attributes('-topmost', True)


    def update_time_display(self):
        current_time = time.localtime()
        self.time_label.config(text=f"{current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}")
        self.root.after(1000, self.update_time_display)

    def update_display(self):
        # Update time
        current_time = time.localtime()
        self.time_label.config(text=f"{current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}")
        
        # Update northbound
        arrival_n = get_next_arrival(SECRETS.APPKEY, SECRETS.BUSSTOPN)
        if len(arrival_n) != 0:
            self.north_bus.config(text=f"{arrival_n[0]}: {arrival_n[1]}")
            self.north_time.config(text=f"{arrival_n[2]}")
        else:
            self.north_bus.config(text="No arrivals")
            self.north_time.config(text="")
        
        # Update southbound
        arrival_s = get_next_arrival(SECRETS.APPKEY, SECRETS.BUSSTOPS)
        if len(arrival_s) != 0:
            self.south_bus.config(text=f"{arrival_s[0]}: {arrival_s[1]}")
            self.south_time.config(text=f"{arrival_s[2]}")
        else:
            self.south_bus.config(text="No arrivals")
            self.south_time.config(text="")
        
        # Schedule next update
        self.root.after(1000, self.update_time_display)
        self.root.after(15000, self.update_display)

def get_next_arrival(appkey, busstop):
    # Your existing get_next_arrival function remains unchanged
    endpoint=f"https://api.tfl.gov.uk/StopPoint/{busstop}/Arrivals?app_key={appkey}"

    request: Response = requests.get(endpoint)
    if request.status_code == 200:
        data = json.loads(request.text)
        if len(data) > 0:
            arrival = data[0]
            if len(data) > 1:
                for i in range(1, len(data)):
                    if data[i]['timeToStation'] < arrival['timeToStation']:
                        arrival = data[i]
            bus_line = arrival['lineName']
            destination = arrival['destinationName']
            expected_mins= arrival['timeToStation'] // 60
            if expected_mins < 1:
                expected_arrival = "Arriving"
            elif expected_mins == 1:
                expected_arrival = "1 min"
            else:
                expected_arrival = f"{expected_mins} mins"
            return (bus_line,destination,expected_arrival)
        else:
            return ()
    else:
        print("Error:", request.status_code)
    return ()

if __name__ == '__main__':
    root = tk.Tk()
    app = BusArrivalGUI(root)
    root.mainloop()