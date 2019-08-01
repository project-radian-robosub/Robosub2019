import os
from pathlib import Path

# path = input('What is the desired path? \n')
path = Path('/home/stewe951/Documents/Robosub2019/TrainingData/')
image_path = Path(os.path.join(path, 'Images'))
annotation_path = Path(os.path.join(path, 'Annotations'))

for image in image_path.iterdir():
    image = image.name.strip('.jpg')

    found = False

    for anno in annotation_path.iterdir():
        anno = anno.name.strip('.xml')

        if anno == image:
            found = True

    if not found:
        try:
            os.remove(os.path.join(image_path, '%s.jpg' % image))
        except FileNotFoundError:
            print('you hit a block')

'''
i = 1
images = os.scandir(image_path)

for img in images:
    os.rename(os.path.join(image_path, img.name), os.path.join(image_path, str(i) + '.jpg'))

    i += 1
'''