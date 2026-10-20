from PIL import Image

width, height = 432, 475

# Skip the 16-byte
with open("classified.enc", "rb") as f:
    ciphertext = f.read()[16:16 + width * height]

shades = {}
pixels = bytearray()

for i in range(0, len(ciphertext), 16):
    block=ciphertext[i:i + 16]

    
    if block not in shades:

        
        shades[block] = (len(shades) * 73) % 256

    
    pixels.extend([shades[block]] * 16)

image = Image.frombytes("L", (width, height), bytes(pixels))

image.save("pattern_ecb.png")
image.show()
