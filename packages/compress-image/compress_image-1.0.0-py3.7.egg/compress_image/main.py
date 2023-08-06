import argparse
import functools
import os
import time
from typing import List

from PIL import Image

BASE_DIM = 2000
FILE_SIZE_THRESHOLD = 500000


def timeit(f):
    @functools.wraps(f)
    def run(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        print("Time exec '{}': {:.3}s".format(f.__name__, end_time - start_time))
        return result

    return run

@timeit
def compress_image(input_path: str, output_path) -> str:
    img = Image.open(input_path)

    w, h = img.size
    max_dim = max(w, h)
    if max_dim > BASE_DIM:
        scale = BASE_DIM / max_dim
        new_w, new_h = int(scale * w), int(scale * h)
        img = img.resize((new_w, new_h), Image.ANTIALIAS)
    img = img.convert('RGB')
    img.save(output_path, "jpeg", optimize=True, quality=95)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Compress Image Tool")
    parser.add_argument("--input", "-i", required=True, help="Đường dẫn đến ảnh đầu vào.")
    parser.add_argument("--output", "-o", help="Đường dẫn lưu ảnh đầu ra.")
    args = parser.parse_args()

    file_path = args.input
    input_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    file_id, ext = os.path.splitext(filename)

    output_path = args.output
    if output_path is None:
        output_path = os.path.join(input_dir, file_id + "_compressed.jpg")

    return compress_image(file_path, output_path)
