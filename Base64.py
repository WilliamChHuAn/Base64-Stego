# NISRA{base64xstego}
# NISRA{8@5E64x5T3go}

# https://ctf-wiki.org/misc/encode/computer/

# original tool
# https://github.com/cjcslhp/wheels/tree/master/b64stego

# original usage
# py enStego.py source.txt stego.txt NISRA{8@5E64x5T3go}
# py deStego.py stego.txt

# story of source.txt
# https://www.plot-generator.org.uk/story/

# usage
# py Base64.py

import base64
import sys

b64table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
flag = "NISRA{8@5E64x5T3go}"

# encode
with open("source.txt", 'r') as sourceText, open("flag.enc", 'w') as setgoText:
    
    print()
    print("Original flag:", flag)
    print()

    binFlag = ""

    # convert char to binary and zero padding
    for i in flag:
        binFlag += bin(ord(i))[2:].zfill(8)
    
    # 19 char x 8 = 152 bits
    print("After convert:", binFlag)
    print()

    for line in sourceText:
        
        # [-1] refers to the last item
        # [:-1] from [0] to [-2] -> doesn't include [-1]
        # https://www.geeksforgeeks.org/python-list-index/
        # https://www.w3schools.com/python/python_lists_access.asp
        # https://shengyu7697.github.io/python-base64/
        text = base64.b64encode(line[:-1].encode("utf-8")).decode("utf-8")
        
        # number of equals
        l = text.count("=")
        
        # =  -> 2 bits
        # == -> 4 bits
        # https://zh.wikipedia.org/zh-tw/Base64#Base64索引表
        if 0 < 2 * l <= len(binFlag):
            
            # print("stego:", binFlag[:2 * l], "Remaining:", binFlag[2 * l:])
            # print("index:", text[-l-1], "stego:", binFlag[:2 * l], "new base64:", b64table[b64table.index(text[-l-1]) + int(binFlag[:2 * l], 2)], "last:", text[-l:])
            
            # normal base64 + base64[last char + stego message] + ==
            text = text[:-l-1] + b64table[b64table.index(text[-l-1]) + int(binFlag[:2 * l], 2)] + text[-l:]
            
            # remain flag
            binFlag = binFlag[2 * l:]
        
        setgoText.write(text + "\n")
        
        # finish stego
        if not len(binFlag):
            break

    # print()

# decode
with open("flag.enc",'r') as stegoText:

    flag = ""

    # list comprehension
    # https://www.w3schools.com/python/python_lists_comprehension.asp
    for line in stegoText:
        
        try:
            # last char + =
            text = line[line.index("=") - 1 : -1]
            
            for i in text:
                if i != "=":
                    if text.count("=") == 2:
                        # find the first occurrence of i
                        # https://www.w3schools.com/python/ref_string_find.asp
                        flag += bin(b64table.find(i))[2:].zfill(4)[2 : 6]
                    else:
                        flag += bin(b64table.find(i))[2:].zfill(2)[4 : 6]
        
        except:
            pass

decodeFlag = ""
for i in range(0, len(flag), 8):
    decodeFlag += chr(int(flag[i : i + 8], 2))

print("After  decode:", decodeFlag)