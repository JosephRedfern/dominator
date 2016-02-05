import numpy as np
import cv2
import argparse

class SegmentDrawer(object):

    def __init__(self, image_filename=None, output_filename=None):
        # Read in the image and start the drawing
        image = cv2.imread(image_filename)
        self.mask = np.zeros((image.shape[0],image.shape[1],3), dtype='uint8')
        self.brush_size = 30

        cv2.namedWindow('draw', flags=cv2.WINDOW_NORMAL)
        cv2.imshow('draw',image)
        cv2.resizeWindow('draw', 500, 500)

        cv2.namedWindow('mask', flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow('mask', 500, 500)

        # Flag for up or down mouse position
        self.drawing = False
        cv2.setMouseCallback('draw', self.select_pixel)

        # Output setting
        self.save = False
        self.output_filename = output_filename
        if output_filename is not None:
            self.save = True

        #avoid needlessly caling imshow by setting redraw_required to true when we've modified image or mask
        self.redraw_required = True

        while True:
            #Generate the image to draw based on image + mask
            if self.redraw_required:
                combined_image = cv2.addWeighted(image, 0.6, self.mask, 0.4,0)
                cv2.imshow('draw', combined_image)
                cv2.imshow('mask', self.mask)
                self.redraw_required = False

            #Escape functions
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                if self.save:
                    while True:
                        input_var = input('You have specified a save file, would you like to save before quiting? [y/n]')
                        if input_var.strip() == 'y':
                            self.save_mask()
                            break
                        elif input_var.strip() == 'n':
                            break
                break

            elif k == ord('s'):
                self.save_mask()

        # Final clear up
        cv2.destroyAllWindows()


    def select_pixel(self, event, x, y, flag, param):
        ## Cannot find good description of required callback spec
        if event == cv2.EVENT_LBUTTONDOWN:
            #Start
            self.drawing = True
            self.mask[y-self.brush_size:y+self.brush_size, x-self.brush_size \
                    :x+self.brush_size,0:3] = 255
            self.redraw_required = True

            print('Down')
        elif event == cv2.EVENT_LBUTTONUP:
            #End
            self.drawing = False
            print('UP')
        elif event == cv2.EVENT_MOUSEMOVE:
            #Middle
            print('hold')
            if self.drawing == True:
                self.mask[y-self.brush_size:y+self.brush_size, x-self.brush_size \
                        :x+self.brush_size,0:3] = 255
                self.redraw_required = True

    def save_mask(self):
        np.save(self.output_filename, self.mask)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='Image file to annotate')
    parser.add_argument('--output_file', help='File to save annotation too')

    args = parser.parse_args()

    SegmentDrawer(image_filename=args.image_file, output_filename=args.output_file)
