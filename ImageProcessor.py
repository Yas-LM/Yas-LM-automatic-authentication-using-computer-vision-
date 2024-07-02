import cv2
import numpy as np
import pytesseract

class ImageProcessor:
    def __init__(self, query_image_path, tesseract_cmd):
        self.per = 10
        self.imgQ = cv2.imread(query_image_path)
        h, w, c = self.imgQ.shape
        self.width = w
        self.height = h
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def traitement_img(self, myimg):
        orb = cv2.ORB_create(5000)
        kp1, des1 = orb.detectAndCompute(self.imgQ, None)
        kp2, des2 = orb.detectAndCompute(myimg, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        matches.sort(key=lambda x: x.distance)
        good = matches[:int(len(matches) * (self.per / 100))]
        imgMatch = cv2.drawMatches(myimg, kp2, self.imgQ, kp1, good, None, flags=2)
        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.8)
        imgscan = cv2.warpPerspective(myimg, M, (self.width, self.height))
        imgscan = cv2.resize(imgscan, (self.width, self.height))
        return imgscan

    def grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def detection_image(self, gray):
        class_Cascade = cv2.CascadeClassifier(".//images/haarcascade_frontalface_alt2.xml")
        faces = class_Cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE)
        return faces

    def remove_noise(self, image):
        return cv2.medianBlur(image, 1)

    def thresholding(self, image):
        return cv2.threshold(image, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def tere_chaine(self, image, x, y, w, h):
        region_Nom = image[y:h, x:w]
        region_Nom = self.remove_noise(self.thresholding(self.grayscale(region_Nom)))
        NomCI = pytesseract.image_to_string(region_Nom, lang='aze+eng')
        NomCI = NomCI.replace('\n', '')
        NomCI = NomCI.strip()
        return NomCI