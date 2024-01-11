from PIL import Image
import subprocess

def take_screenshot(device_id=None, output_file="screenshot.png"):
    adb_command = "adb exec-out screencap -p > screenshot.png"
    
    subprocess.run(adb_command, shell=True)


def crop_image(input_image_path, output_image_path, x, y, width, height):
    # Open the image
    img = Image.open(input_image_path)

    # Crop the image using the specified coordinates
    cropped_img = img.crop((x, y, x + width, y + height))

    # Save the cropped image
    cropped_img.save(output_image_path)

# Example usage
input_image_path = "screenshot.png"  # Replace with the path to your input image
output_image_path = "cropped_image.png"  # Replace with the desired output path
x = 141 + 2  # X-coordinate of the top-left corner
y = 697  # Y-coordinate of the top-left corner
width = 939 - 141 - 4  # Width of the cropped region
height = 1195 - 697 - 2  # Height of the cropped region
# [141,697][939,1195]

take_screenshot()
crop_image(input_image_path, output_image_path, x, y, width, height)
