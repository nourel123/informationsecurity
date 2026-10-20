from PIL import Image
from collections import Counter

width, height = 432, 475

for mode in ["ecb", "cbc"]:
    filename = "classified.enc" if mode == "ecb" else "classified_cbc.enc"

    with open(filename, "rb") as f:
        data = f.read()

    # Skip the lab's 16-byte header and exclude padding.
    ciphertext = data[16:16 + width * height]

    blocks = [
        ciphertext[i:i + 16]
        for i in range(0, len(ciphertext), 16)
    ]

    counts = Counter(blocks)
    repeats = sum(count - 1 for count in counts.values())

    print(mode.upper())
    print("Total blocks:", len(blocks))
    print("Unique blocks:", len(counts))
    print("Repeated occurrences beyond the first:", repeats)

    shades = {}
    pixels = bytearray()

    for block in blocks:
        if block not in shades:
            shades[block] = (len(shades) * 73) % 256

        pixels.extend([shades[block]] * 16)

    image = Image.frombytes("L", (width, height), bytes(pixels))
    image.save(f"pattern_{mode}.png")