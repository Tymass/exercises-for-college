from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import os


def augmentation(image_dir, output_dir, images_count):
    datagen = ImageDataGenerator(
        rotation_range=45,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode="nearest"
    )

    image_files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
    for file in image_files:
        img_path = os.path.join(image_dir, file)
        img = tf.keras.preprocessing.image.load_img(img_path)
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = tf.expand_dims(x, axis=0)

        i = 0
        for batch in datagen.flow(x, batch_size=32, save_to_dir=output_dir, save_prefix="pliers", save_format="jpg"):
            i += 1
            if i == images_count:
                break
        break
