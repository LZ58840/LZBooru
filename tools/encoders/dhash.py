import imagehash


def dhash_encoder(img):
    red, green, blue = img.split()
    
    return {
        "red": bin(int(str(imagehash.dhash(red)), 16)).lstrip('0b').zfill(64),
        "green": bin(int(str(imagehash.dhash(green)), 16)).lstrip('0b').zfill(64),
        "blue": bin(int(str(imagehash.dhash(blue)), 16)).lstrip('0b').zfill(64),
    }
