

def encode_image(img_tuple, encoder_func):
    encoded_json = encoder_func(img_tuple[1])
    encoded_json["id"] = img_tuple[0]
    return encoded_json
