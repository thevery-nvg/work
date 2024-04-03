import re

pa1 = r"N(\d{2})(\d{2})(\d{2}\.\d{1,3})"
pa2 = r"E(\d{2})(\d{2})(\d{2}\.\d{1,3})"
pb1 = r"N(\d{2})(\d{1,2}\.\d{1,3})"
pb2 = r"E(\d{2})(\d{1,2}\.\d{1,3})"
pc_d1 = r"N?(\d{2}\.\d+)"
pc_d2 = r"E?(\d{2}\.\d+)"


def clear_data(data):
    data = re.sub(",", ".", data)
    data = re.sub(r"[^NE0-9.]", "", data)
    return data


def convert_coordinates_full(p: str, data: str):
    lat: float = 0
    lon: float = 0
    if p is None:
        return lat, lon
    x = re.fullmatch(p, data).groups()
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


def main():
    with open("geo_data.txt") as f:
        line = clear_data(f.readline())
        out = []
        if re.fullmatch(f"{pc_d1}{pc_d2}", line):
            #Если lat lon
            out.append(convert_coordinates_full(f"{pc_d1}{pc_d2}", clear_data(line)))
            d = f.readlines()
            for line in d:
                line = clear_data(line)
                out.append(convert_coordinates_full(f"{pc_d1}{pc_d2}", line))
            return out
        else:
            d = clear_data(f.read())
            if re.search(pa1, d):
                lats = re.findall(pa1, d)
                lons = re.findall(pa2, d)
                for lat, lon in zip(lats, lons):
                    lat = "N" + "".join(lat)
                    lon = "E" + "".join(lon)
                    out.append(convert_coordinates_full(pa1 + pa2, lat + lon))
            elif re.search(pb1, d):
                lats = re.findall(pb1, d)
                lons = re.findall(pb2, d)
                for lat, lon in zip(lats, lons):
                    lat = "N" + "".join(lat)
                    lon = "E" + "".join(lon)
                    out.append(convert_coordinates_full(pb1 + pb2, lat + lon))
            else:
                print("NO MATCHES")
                return
            return out


if __name__ == '__main__':
    a = main()
    for i in a:
        print(i)
