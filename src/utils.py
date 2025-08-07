import matplotlib.colors as mcolors

def is_light(color):
    if isinstance(color, str):
        rgb = mcolors.to_rgb(color)
    else:
        if len(color) == 4:
            rgb = color[:3]
        else:
            rgb = color
    
    r, g, b = rgb
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    return luminance > 0.5