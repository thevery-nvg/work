import re

a = 'N60 54 45.1 E70 52 53.7'
b = 'N60 54.751 E70 52.896'
c = 'N60.91252 E70.88160'
d = '60.912521 70.881596'

pa = r"N(\d{2})(\d{2})(\d{2}\.\d{1})E(\d{2})(\d{2})(\d{2}\.\d{1})"
pb = r"N(\d{2})(\d{2}\.\d{3})E(\d{2})(\d{2}\.\d{3})"
pc_d = r"N?(\d+\.\d+)E?(\d{2}\.\d+)"


def clear_data(data):
    replace_data = {" ": "", ",": "."}
    for i in replace_data:
        data = data.replace(i, replace_data[i])
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


for rand_coord in [clear_data(a), clear_data(b), clear_data(c), clear_data(d)]:
    print("found ", convert_coordinates_full({re.fullmatch(pa, rand_coord) is not None: pa,
                                              re.fullmatch(pb, rand_coord) is not None: pb,
                                              re.fullmatch(pc_d, rand_coord) is not None: pc_d,
                                              re.fullmatch(pc_d, rand_coord) is not None: pc_d}.get(True),
                                             rand_coord))
