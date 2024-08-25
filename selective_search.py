import cv2
import sys

def ss_config(ss, img, mode):
    ss.setBaseImage(img)

    if mode == 's':
        ss.switchToSingleStrategy()
    elif mode == 'f':
        ss.switchToSelectiveSearchFast()
    elif mode == 'q':
        ss.switchToSelectiveSearchQuality()
    else:
        print("Re-enter the mode. s or f or q")
        sys.exit(1)


def selective_search(img_path, mode='q'):
    # Initiate Selective Search
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    # Read image in color
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # Configure the mode and image
    ss_config(ss, img, mode)

    # Process Selective-Search
    bboxes = ss.process() # bboxes: listof [x, y, w, h]
    bboxes[:, 2] += bboxes[:, 0] # bboxes -> listof [x, y, x + w, h]
    bboxes[:, 3] += bboxes[:, 1] # bboxes -> listof [x, y, x + w, h + y]

    return bboxes