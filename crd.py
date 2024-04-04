import re
from functools import reduce


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
        data = re.sub(",", ".", data)
        data = re.sub(r"[^NE0-9.]", "", data)
        return data

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


if __name__ == '__main__':
    crd = Coordinates()
    crd.read_data()
    print(crd.parse_file())
