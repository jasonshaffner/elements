def generate_camel_case(words):
    assert isinstance(words, str)
    if not " " in words:
        return words
    return generate_camel_case("".join((words[0].lower(), "".join((words.split()[0][1:])), words.split()[1][0].upper(), "".join((words.split(maxsplit=1)[1][1:])))))

def generate_underscore(words):
    assert isinstance(words, str)
    if not " " in words:
        return words
    return re.sub(' ', '_', words.strip()).lower()

def underline(input, linechar="-"):
    return input.strip() + '\n' + makeline(len(input.strip()), linechar)

def makeline(count, linechar="-"):
    return linechar * int(count)

def pad(input, count, padchar=" "):
    return padleft(padright(input.strip(), count, padchar), count, padchar)

def padleft(input, count, padchar=" "):
    return makeline(count, padchar) + " " + input.strip()

def padright(input, count, padchar=" "):
    return input.strip() + " " + makeline(count, padchar)

def columnize(input, bars=0, width=0):
    maxlen = []
    for line in input:
        n = 0
        for entry in line:
            if entry:
                if len(maxlen) < len(line):
                    maxlen.append(len(entry.strip()))
                else:
                    maxlen[n] = max(maxlen[n], len(entry.strip()))
            n += 1
    output = '\n'
    for line in input:
        n = 0
        if bars: tmp = padright('|', width/2)
        else: tmp = ""
        for entry in line:
            padding = maxlen[n] - len(str(entry))
            if bars:
                tmp += padright(padright(str(entry).strip(), padding + width/2) + '|', width/2)
            else:
                tmp += padright(str(entry).strip(), padding + width)
            n += 1
        if bars and (line == input[0] or line == input[-1]):
            tmp = underline(tmp)
        output += tmp + '\n'
    return output

def pluralize(word):
    if word.lower() in same_singular_plural:
        return word
    elif not word.endswith('s'):
        return word + 's'
    return word

same_singular_plural = [
        'chassis',
        'hardware',
        'software',
        'firmware',
        ]
