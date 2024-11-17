import cv2
import os

def display_image(image_path):
	if not os.path.exists(image_path):
		print(f"File does not exist: {image_path}")
		return

	image = cv2.imread(image_path)
	if image is not None:
		cv2.imshow("Image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	else:
		print("Failed to load the image. Check file path/integrity")