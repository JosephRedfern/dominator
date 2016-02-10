import cv2
import numpy as np

class Dominator(object):

    def __init__(self, domino_filename):
        self.domino_image = cv2.imread(domino_filename)


    def detect_blobs(self, image=None):
        if image is None:
            image = self.domino_image

        params = cv2.SimpleBlobDetector_Params()
        params.filterByCircularity = True
        params.minCircularity = 0.85

        detector = cv2.SimpleBlobDetector_create(params)

        keypoints = detector.detect(image)
        print "Keypoint Count: {0}".format(len(keypoints))

        overlayed_blobs = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

        return overlayed_blobs

    def get_mask(self, image=None):
        if image is None:
            image = self.domino_image
        self.show_image(image=image)
        gray_scene = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray_scene, 200, 255, cv2.THRESH_BINARY)
        self.show_image(image=thresh)
        kernel = np.ones((25,25),np.uint8)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(closed, connectivity=4)

        for i in range(2, ret):
            im = labels[labels==i]
            print im.shape
#            self.show_image(image = labels[labels==i])

        print ret
        print labels
        print stats
        print centroids


        return closed

    def show_image(self, title="Image Preview", image=None):
        if image is None:
            image = self.domino_image

        cv2.imshow(title, image)#title, cv2.resize(image, (0,0), fx=0.2, fy=0.2))
        while cv2.waitKey(100) != 1048603:
            pass


if __name__ == "__main__":
    dm = Dominator("data/IMG_4332.JPG")
    mask = dm.get_mask()
    dm.show_image(image=mask)
    masked = cv2.bitwise_and(dm.domino_image, dm.domino_image, mask=mask)
    dm.show_image(image=masked)
    blobby = dm.detect_blobs(image=masked)

    dm.show_image(image=blobby)
