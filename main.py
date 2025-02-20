from easyocr import Reader
import argparse
import cv2

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image",default="images/2.jpg",
        help="path to input image to be OCR'd")
    ap.add_argument("-l", "--langs", type=str, default="en",
        help="comma separated list of languages to OCR")
    ap.add_argument("-g", "--gpu", type=int, default=-1,
        help="whether or not GPU should be used")
    args = vars(ap.parse_args())

    langs = args["langs"].split(",")
    # print("[INFO] OCR'ing with the following languages: {}".format(langs))
    # load the input image from disk
    image = cv2.imread(args["image"])
    # OCR the input image using EasyOCR
    # print("[INFO] OCR'ing input image...")
    reader = Reader(langs, gpu=args["gpu"] > 0)
    results = reader.readtext(image)

    # loop over the results
    for (bbox, text, prob) in results:
        # display the OCR'd text and associated probability
        print("[INFO] {:.4f}: {}".format(prob, text))
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        # cleanup the text and draw the box surrounding the text along
        # with the OCR'd text itself
        text = cleanup_text(text)
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
