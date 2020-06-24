from typing import List

from PIL import Image, ImageFilter
import os, time
import concurrent.futures

t1 = time.perf_counter()

path = "../images/B351EE3A/"
list_ = os.listdir(path)
# print(list_)
image_names = []
for item in list_:
    image_names.append(path + item)
    # print(image_names)



def process_image(img_name):
    size = (600, 600)
    for image in img_name:
        img = Image.open(image)
        # img = img.filter(ImageFilter.GaussianBlur(15))
        img.thumbnail(size)
        img.save(f'../processed/{image}')

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image,image_names)
t2 = time.perf_counter()
print(f"The start time is {t1} end time is {t2} time elapsed is {t2-t1}")

# item: str
# for item in list_:
#     image_names.append(path + item)
# # print(image_names)
#

# if __name__ == '__main__':
#     size = (600, 600)
#
#
#     def process_image(img_name):
#         img = Image.open(img_name)
#         img = img.filter(ImageFilter.GaussianBlur(15))
#         img.thumbnail(size)
#         img.save(f"processed/{img_name}")
#         print(f"{img_name}  was processed...")
#
#
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.map(process_image, image_names)
#     t2 = time.perf_counter()
#     print(f"Total time taken is {t1 - t2}")
