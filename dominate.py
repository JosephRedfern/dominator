import cv2
import numpy as np

class Dominator(object):

    def __init__(self, domino_filename):
        self.domino_image = cv2.imread(domino_filename)


    def detect_blobs(self, image=None):
        if image is None:
            image = self.domino_image

        detector = cv2.SimpleBlobDetector_create()

        keypoints = detector.detect(image)
        print "Keypoints: {0}".format(len(keypoints))

        overlayed_blobs = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

    def get_mask(self, image=None):
        if image is None:
            image = self.domino_image

        gray_scene = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray_scene, 200, 255, cv2.THRESH_BINARY)

        kernel = np.ones((25,25),np.uint8)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return closed

    def show_image(self, title="Image Preview", image=None):
        if image is None:
            image = self.domino_image

        cv2.imshow(title, cv2.resize(image, (0,0), fx=0.2, fy=0.2))
        while cv2.waitKey(100) != 1048603:
            pass


if __name__ == "__main__":
    dm = Dominator("data/IMG_4332.JPG")
    mask = dm.get_mask()
    dm.show_image(image=cv2.bitwise_and(dm.domino_image, dm.domino_image, mask=mask))
