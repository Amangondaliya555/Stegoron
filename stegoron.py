from PIL import Image
import pyfiglet
import terminal_banner


print("\033[1;34;48m* LINUX BASED TOOL V1.0 \033[1;32;48mDeveloped By @Aman Gondaliya\033[1;32;48m & @Ujjwal Kumar\033[1;31;48m")
the_banner = pyfiglet.figlet_format("<Stegoron>")
print(the_banner)
print("\033[1;32;48m")
banner_text = "-->It is a linux based tool.\n-->It uses LSB method to hide data in PNG files.\n-->Please Enter the extension png with the file name while encoding or decoding"
my_banner = terminal_banner.Banner(banner_text)
print(my_banner)



msg = ''

def data_conversion(data):
    new_data = []

    for x in data:
        new_data.append(format(ord(x), '08b'))
    return new_data


def modify_pixels(new_pic, data):
    datarow = data_conversion(data)
    len_data = len(datarow)
    pic_data = iter(new_pic)
    pixels = []
    for i in range(len_data):
        temp_pixels = [value for value in pic_data.__next__()[:3] + pic_data.__next__()[:3] + pic_data.__next__()[:3]]
        # print(temp_pixels)
        for j in range(0, 8):
            if (datarow[i][j] == '0') and (temp_pixels[j] % 2 != 0):
                if(temp_pixels[j] == 256):
                    temp_pixels[j] = 254

                else:
                    temp_pixels[j] += 1


            elif (datarow[i][j] == '1') and (temp_pixels[j] % 2 == 0):
                if (temp_pixels[j] == 256):
                    temp_pixels[j] = 254

                else:
                    temp_pixels[j] += 1



            #if temp_pixels[j] == 0:
             #   temp_pixels[j] = 1

        if i == len_data - 1:
            if temp_pixels[-1] % 2 == 0:
                temp_pixels[-1] += 1
        else:
            if temp_pixels[-1] % 2 != 0:
                temp_pixels[-1] += 1


        pixels = pixels + temp_pixels

    # print("after for loop")

    pixels = tuple(pixels)
    

    len_data = len_data*9
    for i in range(0, len_data, 3):
        yield pixels[i:i+3]


def put_pixel(new_pic, data):
    s = new_pic.size[0]
    (x, y) = (0, 0)
    for pixels in modify_pixels(new_pic.getdata(), data):
        # print(pixels)
        # print('\n')
        new_pic.putpixel((x, y), pixels)

        if x == s - 1:
            y += 1
            x = 0
        else:
            x += 1


def encode():
    org_pic = input("Enter image name:")
    pic = Image.open(org_pic,'r')

    data = input("Enter data to be encoded:")
    global msg
    msg = data
    if (len(data) == 0):
        raise ValueError('Data is empty')
    
    new_pic = pic.copy()
    put_pixel(new_pic, data)

    new_pic_name = input("Enter the name of new image:")
    new_pic.save(new_pic_name)
    


def decode():
    img = input("Enter image name:")
    image = Image.open(img,'r')

    data = ''
    imgdata = iter(image.getdata())
    
    pixels = []
    while True:
        temp_pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]

        binstr = ''

        for i in temp_pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        pixels = pixels + temp_pixels
        
        data += chr(int(binstr, 2))
        
        if (temp_pixels[-1] % 2 != 0):
            return data



def main():
    options = int(input("!--Welcome to stegoron--!\n"
                        "1.Encode\n2.Decode\n-->"))
    if (options == 1):
        encode()
    elif (options == 2):
        print("Your Hidden data is:" + decode())
    else:
        raise Exception("Wrong Input,Please Enter Either 1 or 2")


main()

