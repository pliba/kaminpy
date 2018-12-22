
def parse_exp(line):
    try:
        return int(line)
    except ValueError:
        return line
