
def CeasarCipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def CeasarDecipher(text, shift):
    return CeasarCipher(text, -shift)


def CeasarbruteForce(text):
    for shift in range(26):
        print(f"Shift {shift}: {CeasarCipher(text, shift)}")


string="CRYPTO IS FUN UNTIL THE PROFESSOR SAYS QUIZ"
print("Original:", string)
print("Ciphertext:", CeasarCipher(string, 4))

cipher="GWCL JMBBMZ VWB JM CAQVO BWWTA BW AWTDM BPQA"
print("Ciphertext:", cipher)
print("Decrypted:", CeasarDecipher(cipher, 8))

cipher2="ESP VPJ TD FYVYZHY ECJ MCFEP QZCNP"
print("Ciphertext:", cipher2)
print("Brute Force:")
CeasarbruteForce(cipher2)


def count_occurrences(text):
    occurrences = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            occurrences[char] = occurrences.get(char, 0) + 1
    return occurrences

print("Letter frequencies in ciphertext:")
text="EKT YTJRTE BTYYQFT PY KPZZTO PO EKPY NQRQFRQNK. STEETR GRTCVTOJD ZXTY OXE RTHTQS EKT IKXST LTD, MVE PE FPHTY Q FXXZ YEQRE. SXXL GXR JXBBXO IXRZY, RTNTQETZ NQEETROY, QOZ YKXRE IXRZY. IKTO DXV RTJXHTR EKT BTYYQFT, EKT HPFTOTRT LTD KQY GXVR STEETRY."
print(sorted(count_occurrences(text).items(), key=lambda x: x[1], reverse=True))

def recover_text(text):
    text = text.lower()
    recovered_text = ""
    for char in text:
        if char=='e':
            recovered_text += 't'
        elif char=='k':
            recovered_text += 'h'
        elif char=='t':
            recovered_text += 'e'
        
        elif char=='p':
            recovered_text += 'i'
        elif char=='y':
            recovered_text += 's'
        elif char=='x':
            recovered_text += 'o'
        elif char=='j':
            recovered_text += 'c'
        elif char=='q':
            recovered_text += 'a'
        elif char=='o':
            recovered_text += 'n'
        elif char=='z':
            recovered_text += 'd'
        elif char=='n':
            recovered_text += 'p'
        elif char=='f':
            recovered_text += 'g'
        elif char=='b':
            recovered_text += 'm'
        elif char=="i":
            recovered_text += 'w'
        elif char=="h":
            recovered_text += 'v'
        elif char=="s":
            recovered_text += 'l'
        elif char=="m":
            recovered_text += 'b'
        elif char=="v":
            recovered_text += 'u'
        elif char=="d":
            recovered_text += 'y'
        elif char=="l":
            recovered_text += 'k'
        elif char=="g":
            recovered_text += 'f'
        else:
            recovered_text += char
    return recovered_text

    

print("Recovered text:", recover_text(text))



Ciphertext = "VVHWGQUIVYHIRSUPGTWXJSVIPCWIUPHGCIVIVVHPGHWITSDTRSDVUSYITMZLGFHIXSUCVSDQOSPFGFVLQIOHEVHGMSDGJQRPWAQWGSNXJSPSUHIVGEXIPHVCOPRPCBGYUSLXVCUIECYITHKIMSBAJSQXJSPIUGDKGPHGQAHWEZHETSQXGFWL GOFGGGVAQFGIEZLTUS"

def vigenere_find_key(ciphertext, key_length):
    key = ""
    for i in range(key_length):
       
        nth_chars = ciphertext[i::key_length]
        
        frequencies = count_occurrences(nth_chars)
        
        most_common_letter = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[0][0]
       
        shift = (ord(most_common_letter) - ord('e')) % 26
        key += chr(shift + ord('a')) 
    return key

def vigenere_decrypt(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    count=0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[count % key_length])-ord('a')
            decrypted_text += CeasarDecipher(char, shift)
            count += 1
        else:
            decrypted_text += char
    return decrypted_text

print("Vigenere Key:", vigenere_find_key(Ciphertext, 4))
print("Decrypted Text:", vigenere_decrypt(Ciphertext, "code"))