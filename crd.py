import re
from functools import reduce
import random


class Coordinates:
    def __init__(self):
        self.pa1 = r"N(\d{2})(\d{2})(\d{2}\.\d{1,3})"
        self.pa2 = r"E(\d{2})(\d{2})(\d{2}\.\d{1,3})"
        self.pb1 = r"N(\d{2})(\d{1,2}\.\d{1,3})"
        self.pb2 = r"E(\d{2})(\d{1,2}\.\d{1,3})"
        self.pc_d1 = r"N?(\d{2}\.\d+)"
        self.pc_d2 = r"E?(\d{2}\.\d+)"
        self.data = None
        self.out = []

    @staticmethod
    def clear_data(data):
        return re.sub(r"[^NE0-9.]", "", data.replace(",", "."))

    def read_data(self):
        with open("geo_data.txt") as f:
            data = f.readlines()
        self.data = data

    def convert_coordinates_full(self, p: str, data: str):
        lat: float = 0
        lon: float = 0
        if p is None:
            return lat, lon
        x = re.fullmatch(p, self.clear_data(data)).groups()
        if len(x) == 2:
            lat = float(x[0])
            lon = float(x[1])
        elif len(x) == 4:
            lat = float(x[0]) + float(x[1]) / 60
            lon = float(x[2]) + float(x[3]) / 60
        elif len(x) == 6:
            lat = float(x[0]) + float(x[1]) / 60 + float(x[2]) / 3600
            lon = float(x[3]) + float(x[4]) / 60 + float(x[5]) / 3600
        return round(lat, 5), round(lon, 5)

    def parse_file(self):
        line = self.clear_data(self.data[0])
        if re.fullmatch(f"{self.pc_d1}{self.pc_d2}", line):
            for line in self.data:
                self.out.append(self.convert_coordinates_full(f"{self.pc_d1}{self.pc_d2}", line))
            return self.out
        else:
            d = self.clear_data(reduce(lambda x, y: x + y, self.data))
            if re.search(self.pa1, d):
                lats = re.findall(self.pa1, d)
                lons = re.findall(self.pa2, d)
                for lat, lon in zip(lats, lons):
                    lat = "N" + "".join(lat)
                    lon = "E" + "".join(lon)
                    self.out.append(self.convert_coordinates_full(self.pa1 + self.pa2, lat + lon))
            elif re.search(self.pb1, d):
                lats = re.findall(self.pb1, d)
                lons = re.findall(self.pb2, d)
                for lat, lon in zip(lats, lons):
                    lat = "N" + "".join(lat)
                    lon = "E" + "".join(lon)
                    self.out.append(self.convert_coordinates_full(self.pb1 + self.pb2, lat + lon))
            else:
                print("NO MATCHES")
                return
            return self.out


class CreateGPX:
    def __init__(self):
        self.height = None
        self.head = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <gpx xmlns="http://www.topografix.com/GPX/1/1" creator="MapSource 6.16.3" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">

          <metadata>
            <link href="http://www.garmin.com">
              <text>Garmin International</text>
            </link>
            <time>2024-01-23T12:24:21Z</time>
            <bounds maxlat="56.092479145154357" maxlon="55.898553002625704" minlat="53.633718425408006" minlon="51.073859967291355"/>
          </metadata>'''
        self.tail = '\n</gpx>'
        self.output = ""

    def input_height(self):
        self.height = int(input("Введите высоту: "))
        if not self.height:
            self.height = random.randint(35, 88)

    def create_data(self, data: list[tuple]):
        self.output += self.head
        for i, coordinates in enumerate(data):
            lat, lon = coordinates[0], coordinates[1]
            temp = f'''  <wpt lat="{lat}" lon="{lon}">
            <ele>{self.height}</ele>
            <time>2024-01-16T12:56:09Z</time>
            <name>{i + 1:03}</name>
            <cmt>30-APR-04 0:57:35</cmt>
            <desc>30-APR-04 0:57:35</desc>
            <sym>Flag, Green</sym>
            <extensions>
            <gpxx:WaypointExtension xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
            <gpxx:DisplayMode>SymbolAndName</gpxx:DisplayMode>
            </gpxx:WaypointExtension>
            </extensions>
            </wpt>\n'''
            self.output += temp
        self.output += self.tail

    def write_gpx(self):
        with open("coord_fixed.gpx", "w") as f:
            f.write(self.output)

    def __call__(self, data):
        self.input_height()
        self.create_data(data)
        self.write_gpx()


if __name__ == '__main__':
    crd = Coordinates()
    wrt = CreateGPX()
    crd.read_data()
    wrt(crd.parse_file())
