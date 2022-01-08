from tools.encoders.dhash import dhash_encoder
from tools.encoders.histogram import histogram_encoder


ENCODING_FUNCTIONS = {
    "histogram": histogram_encoder,
    "dhash": dhash_encoder
}

ENCODING_ALGORITHMS = {
    "abs_norm": ("histogram", histogram_encoder),
    "eucl_norm": ("histogram", histogram_encoder),
    "dhash_xor_norm": ("dhash", dhash_encoder)
}

