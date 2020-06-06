""" Day 8 

    split input into list of lists (list of layers)
    layer 'L' contains the fewest 0s
    let one = num 1s in L, two = num 2s in L; return one*two

"""

def make_layers(pixels, width, height):

    layers = []

    layer_area = width * height

    i = 0
    while i < len(pixels):
        layers.append(pixels[i:i+layer_area])
        i += layer_area
    
    return layers


def find_layer_fewest_digit(layers, digit):

    fewest = None
    cnt = float('infinity')

    for layer in layers:
        layer_cnt = layer.count(digit)
        if layer_cnt < cnt:
            cnt = layer_cnt
            fewest = layer
    
    return fewest


def decode_image(layers):

    decoded = list(layers[0])

    for i, pixel in enumerate(decoded):
        if pixel == '2':
            decoded[i] = get_opaqe(layers[1:], i)

    return ''.join(decoded)


def get_opaqe(layers, i):

    for layer in layers:
        if layer[i] != '2':
            return layer[i]


##########
if __name__ == "__main__":
    import common

    pixels = common.listify_input_string('08-input.txt')[0]
    layers = make_layers(pixels, 25, 6)
    fewest_0 = find_layer_fewest_digit(layers, '0')

    # Part 1
    print("Part 1:", fewest_0.count('1') * fewest_0.count('2'))  # 1224

    # Part 2
    decoded = decode_image(layers)
    rows = make_layers(decoded, 25, 1)
    for row in rows:
        print(row)
