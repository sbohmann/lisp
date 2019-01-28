from io import open

def run():
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        processed = fully_process(line)
        print(len(processed), '[' + processed + ']')

        chars = set()
        for c in line:
            chars.add(c.lower())
        for c in chars:
            processed = fully_process(line.replace(c, '').replace(c.upper(), ''))
            print(c, len(processed), '[' + processed + ']')



def fully_process(line):
    while True:
        line, changed = process(line)
        if not changed:
            break
    return line


def process(line):
    last = None
    changed = False
    buffer = []
    for c in line:
        if remove(last, c):
            last = None
            changed = True
        else:
            if last is not None:
                buffer.append(last)
            last = c
    if changed:
        if last is not None:
            buffer.append(last)
        return ''.join(buffer), changed
    else:
        return line, changed


def remove(last, c):
    if last is None:
        return False
    same_lowercase = last.lower() == c.lower()
    different_case = last.islower() != c.islower()
    return same_lowercase and different_case


run()
