from PIL import Image
import pytesseract

title_coords = (385, 995, 895, 1027)
artist_coords = ()

img = Image.open('sv6c_BryONPDgWT.jpg')
img = img.transpose(Image.ROTATE_270)
cropped_img = img.crop(title_coords)
extracted_title = pytesseract.image_to_string(cropped_img,lang='jpn')
#img = pytesseract.image_to_string(img,lang='eng+jpn')
print(extracted_title)
#print(img)

cropped_img.save('new.jpg')