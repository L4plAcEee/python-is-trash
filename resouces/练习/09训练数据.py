import os
import cv2
import sys
import numpy as np


def getImagesAndLabels(path):
    faceSamples = []
    ids = []
    imagePaths = []
    for f in os.listdir(path):
        imagePaths.append(os.path.join(path, f))

    face_detector = cv2.CascadeClassifier("../../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

    for imagePath in imagePaths:
        img = cv2.imread(imagePath)
        PIL_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        img_numpy = np.array(PIL_img)
        faces = face_detector.detectMultiScale(img_numpy)
        id = int(os.path.split(imagePath)[1].split(".")[0])
        for x, y, w, h in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
            print(ids)
    return faceSamples, ids


if __name__ == "__main__":
    path = "../data"
    faces, ids = getImagesAndLabels(path)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.write("trainer/trainer.yml")
