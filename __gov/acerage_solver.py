import re


ACRE_SQFT = 43560
HALF_ACRE = 0.5

def acres1(text):
    match = re.search(r"(\d+\.?\d*)\s*AC", text, re.I)
    if match:
        return float(match.group(1))
    return None

def acres2(text):
    match = re.search(r"(\d+\.?\d*)[' ]?X[' ]?(\d+\.?\d*)", text.upper())
    if match:
        w = float(match.group(1))
        h = float(match.group(2))
        sqft = w * h
        return sqft / ACRE_SQFT
    return None

def acres3(text):
    if "PART" in text:
        return None  # avoid false positives

    acres = 640
    fractions = re.findall(r"(1\/2|1\/4)", text)

    if not fractions:
        return None

    for f in fractions:
        if f == "1/2":
            acres *= 0.5
        elif f == "1/4":
            acres *= 0.25

    return acres

def acres4(text):
    directions = re.findall(r"([NSEW]{1,2})\s*(\d+\.?\d*)", text)
    ns = []
    ew = []

    if len(directions) < 4:
        return None

    

    for d, val in directions:
        val = float(val)
        if "N" in d or "S" in d:
            ns.append(val)
        if "E" in d or "W" in d:
            ew.append(val)

    if not ns or not ew:
        return None

    height = sum(ns) / 2  # average opposing sides
    width = sum(ew) / 2

    sqft = width * height
    return sqft / ACRE_SQFT

def acres5(text):
    south = sum(float(x) for x in re.findall(r"S\s*(\d+\.?\d*)", text))
    north = sum(float(x) for x in re.findall(r"N\s*(\d+\.?\d*)", text))
    east  = sum(float(x) for x in re.findall(r"E\s*(\d+\.?\d*)", text))
    west  = sum(float(x) for x in re.findall(r"W\s*(\d+\.?\d*)", text))

    vertical = south + north
    horizontal = east + west

    if vertical > 0 and horizontal > 0:
        # crude bounding box estimate
        sqft = (horizontal / 2) * (vertical / 2)
        return sqft / ACRE_SQFT

    return None

def acres6(text):
    # remove section/township/range references
    cleaned = re.sub(r"S\d+|T\d+[NS]?|R\d+[EW]?", "", text)

    nums = [float(x) for x in re.findall(r"\b\d+\.?\d*\b", cleaned)]

    if len(nums) < 2:
        return None

    dims = [n for n in nums if 10 <= n <= 500]  # tighter filter

    if len(dims) >= 2:
        dims.sort()
        w, h = dims[0], dims[1]
        sqft = w * h
        return sqft / ACRE_SQFT

    return None




def half_acre_check(legal):
    legal = legal.upper()

    funcs = [
        acres1,
        acres2,
        acres3,
        acres4,
        acres5,
        acres6
    ]

    for func in funcs:
        acres = func(legal)
        if acres is not None:
            return "YES" if acres >= HALF_ACRE else "NO"

    return "UNKNOWN"


def acerage(data):
    try:
        legal = data.get("Legal Text", "")
    except:
        legal = data
    answer = half_acre_check(legal)
    YES_VALUES = ["YES", "Y", "TRUE"]
    return answer and answer.strip().upper() in YES_VALUES
        
    



























