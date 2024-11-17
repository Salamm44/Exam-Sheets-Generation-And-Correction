from pdf2image import convert_from_path
import os


def convert_pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{i + 1}.jpg')  # No prefix
        image.save(output_path, 'JPEG')
        image_paths.append(output_path)

    return image_paths

                       
    
