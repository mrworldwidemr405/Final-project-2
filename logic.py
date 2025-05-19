def get_fields(shape, goals):
    if shape in ["circle", "sphere"]:
        return ["Radius"]
    if shape in ["square", "cube"]:
        return ["Side Length"]
    if shape == "triangle":
        return ["Base", "Height"]
    if shape == "pyramid":
        if goals["Volume"] and goals["Surface Area"]:
            return ["Base Length", "Height", "Slant Height"]
        if goals["Volume"]:
            return ["Base Length", "Height"]
        if goals["Surface Area"]:
            return ["Base Length", "Slant Height"]
    return []

def calc(shape, goals, v):
    out = []

    if shape == "circle" and goals["Area"]:
        out.append(f"Area: {3.14 * v['Radius']**2:.2f}")
    elif shape == "square" and goals["Area"]:
        out.append(f"Area: {v['Side Length']**2:.2f}")
    elif shape == "triangle" and goals["Area"]:
        out.append(f"Area: {0.5 * v['Base'] * v['Height']:.2f}")
    elif shape == "sphere":
        r = v["Radius"]
        if goals["Surface Area"]:
            out.append(f"Surface: {4 * 3.14 * r**2:.2f}")
        if goals["Volume"]:
            out.append(f"Volume: {(4/3)*3.14*r**3:.2f}")
    elif shape == "cube":
        s = v["Side Length"]
        if goals["Surface Area"]:
            out.append(f"Surface: {6*s**2:.2f}")
        if goals["Volume"]:
            out.append(f"Volume: {s**3:.2f}")
    elif shape == "pyramid":
        b = v["Base Length"]
        if goals["Volume"]:
            out.append(f"Volume: {(1/3)*b**2*v['Height']:.2f}")
        if goals["Surface Area"]:
            out.append(f"Surface: {b**2 + 2*b*v['Slant Height']:.2f}")
    return "\n".join(out)

def save(shape, result):
    with open("history.txt", "a") as f:
        f.write(f"{shape}:\n{result}\n\n")

def load():
    try:
        with open("history.txt") as f:
            return f.read().split("\n\n")
    except:
        return []