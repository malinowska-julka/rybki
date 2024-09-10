import cv2
from PIL import Image, ImageDraw
import glob
import numpy as np
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

if __name__ == "__main__":
    image_list = ["/home/julia/Pictures/Screenshots/.png"]
    names = []
    img = cv2.imread("/home/julia/Pictures/Screenshots/GuramiCzekoladowe.png")
    hh, ww = img.shape[:2]

    # threshold on white
    # Define lower and uppper limits
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])

    segmentor = SelfiSegmentation()

    # read image
    imgOffice = cv2.imread("office.jpg")

    # resize office to 640x480
    imgOffice = cv2.resize(imgOffice, (640, 480))

    green = (0, 255, 0)

    imgNoBg = segmentor.removeBG(imgOffice, green, threshold=0.50)

    # show both images
    cv2.imshow("office", imgOffice)
    cv2.imshow("office no bg", imgNoBg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # for filename in glob.glob("/home/julia/Pictures/Screenshots/*.png"):
    #   im = Image.open(filename)
    #  names.append(filename.split("/")[-1])
    # image_list.append(im)

    # for i in range(len(image_list)):
    # bg = Image.open("images/background.png")
    # Removing the background from the given Image
    # image_list[i].thumbnail((750, 750))  # resize
    # bg.paste(image_list[i])
    # bg.save("images/rybki_img/" + names[i])

    # output.save("images/rybki_img/" + names[i])
