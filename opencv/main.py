import os
from bounding_box import make_bbox
from augmentation import augmentation
import cv2
import math

cwd = os.getcwd()


folders_1 = ['test', 'train', 'valid']
folders_2 = ['images', 'labels']

data_path = f'{cwd}/opencv/pliers/'
augmented_data_path = f'{cwd}/opencv/pliers_buffor/'
dataset_path = f'{cwd}/opencv/dataset_pliers/'

ratio = [0.85, 0.1, 0.05]
images_amount = 400

train_ratio = math.floor(images_amount * ratio[0])
test_ratio = math.floor(images_amount * ratio[1])
valid_ratio = math.floor(images_amount * ratio[2])

augmentation(data_path, augmented_data_path, images_amount)

print(
    f'train_ratio: {train_ratio} test_rato: {test_ratio} valid_ratio {valid_ratio}')

file_names = os.listdir(augmented_data_path)

i = 0

for file_name in file_names:

    if file_name.endswith(".jpg") or file_name.endswith(".png") and i <= train_ratio:
        image_path = os.path.join(augmented_data_path, file_name)
        img_bbox = make_bbox(image_path)
        img = cv2.imread(image_path)
        cv2.imwrite(f'{dataset_path}train/images/pliers{i}.jpg', img)
        with open(f'{dataset_path}train/labels/pliers{i}.txt', "w") as file:
            file.write(
                f'0 {img_bbox[0]} {img_bbox[1]} {img_bbox[2]} {img_bbox[3]}')
        i += 1
        print(i)
    elif file_name.endswith(".jpg") or file_name.endswith(".png") and i <= test_ratio and i > train_ratio:
        image_path = os.path.join(augmented_data_path, file_name)
        img_bbox = make_bbox(file_name)
        img = cv2.imread(image_path)
        cv2.imwrite(f'{dataset_path}test/images/pliers{i}.jpg', img)
        with open(f'{dataset_path}test/labels/pliers{i}.txt', "w") as file:
            file.write(
                f'0 {img_bbox[0]} {img_bbox[1]} {img_bbox[2]} {img_bbox[3]}')
        i += 1
        print('asdas', i)
    elif file_name.endswith(".jpg") or file_name.endswith(".png") and i <= valid_ratio and i > test_ratio:
        image_path = os.path.join(augmented_data_path, file_name)
        img_bbox = make_bbox(file_name)
        img = cv2.imread(image_path)
        cv2.imwrite(f'{dataset_path}valid/images/pliers{i}.jpg', img)
        with open(f'{dataset_path}valid/labels/pliers{i}.txt', "w") as file:
            file.write(
                f'0 {img_bbox[0]} {img_bbox[1]} {img_bbox[2]} {img_bbox[3]}')
        i += 1
    else:
        print('generowanie datasetu skonczone')
