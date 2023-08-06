
def nocolor():
    return "\033[0m"
def color(r, g, b, bold=False):
    i = 16 + b + g*6 + r*6*6
    if bold:
        return "\033[1m\033[38;5;{}m".format(i)
    return "\033[38;5;{}m".format(i)
