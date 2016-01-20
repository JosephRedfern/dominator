import numpy as np
import math
import cv2
import argparse

class SegmentDrawer(object):

    def __init__(self, image_filename=None, output_filename=None):
        # Read in the image and start the drawing
        self.image = cv2.imread(image_filename)
    
        window_width, window_height = self.calc_window_size(500, 500)
        
        self.mask = np.zeros((self.image.shape[0], self.image.shape[1],3), dtype='uint8')
        self.brush_size = 30

        cv2.namedWindow('draw', flags=cv2.WINDOW_NORMAL)
        cv2.imshow('draw', self.image)
        cv2.resizeWindow('draw', window_width, window_height)

        cv2.namedWindow('mask', flags=cv2.WINDOW_NORMAL)
        cv2.imshow('mask', self.mask)
        cv2.resizeWindow('mask', window_width, window_height)

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
                combined_image = cv2.addWeighted(self.image, 0.6, self.mask, 0.4,0)
                cv2.imshow('draw', combined_image)
                cv2.imshow('mask', self.mask)
                self.redraw_required = False

            #Escape functions
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                while self.save and True:
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


    def calc_window_size(self, max_window_width, max_window_height):
        image_width, image_height, _ = self.image.shape
        ratio = min([float(max_window_height)/image_height, float(max_window_width)/image_width])

        window_width = int(ratio*image_width)
        window_height = int(ratio*image_height)

        return window_width, window_height


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
