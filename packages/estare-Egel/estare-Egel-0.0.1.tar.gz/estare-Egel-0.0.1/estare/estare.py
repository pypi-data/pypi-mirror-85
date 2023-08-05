import numpy as np
from src.init import examine
from src.feature import extract
from src.align import *

from matplotlib import pyplot as plt
import argparse
import os
from skimage.io import imsave



parser = argparse.ArgumentParser(prog='estare', description='''Program for aligning and stacking astro photos.''',
                                 epilog='''estare is a Persian word for star.''')

sub_parsers = parser.add_subparsers()

# create the parser for the feature detection command
parse_feature = sub_parsers.add_parser('scan', help='''Scan an input image to find suitable features such as (a) bright 
                                        star(s) that can be used for aligning multiple frames.''')

parse_feature.add_argument('image', action='store', type=str, help='The input image to be scanned.')
parse_feature.add_argument('kapa', action='store', type=float, help='''Threshold for picking pixels of a certain  
                            brightness. It takes a floating point values from the range [0, 1]. Pick a larger value to
                            limit the detected features to those of a higher brightness.''')
parse_feature.set_defaults(Mode='scan')

parse_stack = sub_parsers.add_parser('stack', help='''This mode should normally be used after the alignment features
                                        have been detected in the scan mode. The stack mode uses the coordinates of the 
                                        features to align two images. It then stacks them up. Two input images along 
                                        with one identical feature for each image are required.''')

parse_stack.add_argument('layer_1', help='Path and name of the reference image (base layer)')
parse_stack.add_argument('layer_2', help='Path and name of the second image (top layer)')
parse_stack.add_argument('feature_1', help='''Path and name of a .npy file containing the coordinates of the feature in 
                            the reference layer''')
parse_stack.add_argument('feature_2', help='''Path and name of a .npy file containing the coordinates of the feature in
                            the second layer which will be lined up with the identical feature in the reference 
                            layer.''')
parse_stack.set_defaults(Mode='stack')

args = parser.parse_args()

if args.Mode == 'scan':
    # prepare the data directory structure for the program
    try:
        os.mkdir('./data')
        os.mkdir('./data/features')
        os.mkdir('./data/refuse')
        
        os.mkdir('./data/features/coordinates')
        os.mkdir('./data/features/pixels')

        os.mkdir('./data/refuse/coordinates')        
        os.mkdir('./data/refuse/pixels')                
    except OSError:
        print('Failed to create data directories. This may be due to the lack of write permission.')

    # handle input arguments
    imagePath = args.image
    threshold = args.kapa

    img_as_array, x_range, y_range = examine(imagePath, save=True, verbose=False, graphics=False)
    # Replace with:
    # img_as_array = FloatImage(imagePath)
    # img_as_array.print_info()
    # img_as_array.save()
    # x_range, y_range = img_as_array.size()
    
    print(f'Image has x-range = {x_range}, and y-range = {y_range}')

    imgGray = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale
    # Replace with (makes FloatImage redundant):
    # imgGray = GrayImage(imagePath)
    # imgGray.print_info()
    # imgGray.save()
    # x_range, y_range = imgGray.size()

    fig2, frame = plt.subplots(1, 1)
    image_features = frame.imshow(imgGray, cmap='gray')
    frame.set_title('Marked features', fontsize=14)

    numFeatures, indices, markers = extract(imgGray, xRng=[0, x_range], yRng=[0, y_range],
                                            kapa=threshold)
    # Replace with:
    # numFeatures, indices, markers = imgGray.extract(xRng=[0, x_range], yRng=[0, y_range], kapa=threshold)

    print(f'''
        Total number of features detected: {numFeatures}. If this is too many, consider increasing  
        the threshold input.
    ''')

    # Loop over features and ask the user if a feature is of interest to be saved
    keepFeature = False

    xy_FeatureCount = 0   # number of already-saved feature coordinates initialized to zero
    binFeatureCount = 0   # number of already-saves feature images in binary format initialized to zero
    imgFeatureCount = 0   # number of already-saves feature images in .png format initialized to zero

    xy_RefusedCount = 0   # number of already-saved refused coordinates initialized to zero
    binRefusedCount = 0   # number of already-saves refused images in binary format initialized to zero
    imgRefusedCount = 0   # number of already-saves refused images in .png format initialized to zero  

    for files in os.listdir('./data/features'):
        if files.endswith('.png'):
            imgFeatureCount += 1

    for files in os.listdir('./data/features/pixels'):
        if files.endswith('.npy'):
            binFeatureCount += 1

    for files in os.listdir('./data/features/coordinates'):
        if files.endswith('.npy'):
            xy_FeatureCount += 1


    for files in os.listdir('./data/refuse'):
        if files.endswith('.png'):
            imgRefusedCount += 1

    for files in os.listdir('./data/refuse/pixels'):
        if files.endswith('.npy'):
            binRefusedCount += 1

    for files in os.listdir('./data/refuse/coordinates'):
        if files.endswith('.npy'):
            xy_RefusedCount += 1    
            
    selectedFeatures = 0  # counter
    refusedFeatures = 0  # counter
    
    
    # TODO: add a feature to use matplotlib.ginput
    if numFeatures > 0:
        print('''A detected feature is displayed by a black square. Press any key to save the current feature, or click 
                the mouse to discard it...''')
        for pair_0, pair_1 in zip(indices[0], indices[1]):
            if pair_0 > 3 and pair_1 > 3:
                arrow = frame.annotate('O', xy=(pair_1, pair_0), arrowprops=dict(arrowstyle='->'))
                plt.draw()  # , plt.pause(0.01)
                btnpress = plt.waitforbuttonpress(-1)
                if btnpress:
                    selectedFeatures += 1
                    np.save('./data/features/coordinates/feature_{}'.format(xy_FeatureCount), [pair_0, pair_1])
                    xy_FeatureCount += 1
                    np.save('./data/features/pixels/feature_{}_pixels'.format(binFeatureCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    binFeatureCount += 1
                    imsave('./data/features/feature_{}_pixels.png'.format(imgFeatureCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    imgFeatureCount += 1
                    # TODO: Find install path and cd to data
                    plt.waitforbuttonpress(0.1)
                else:
                    refusedFeatures += 1
                    np.save('./data/refuse/coordinates/refused_{}'.format(xy_RefusedCount), [pair_0, pair_1])
                    xy_RefusedCount += 1
                    np.save('./data/refuse/pixels/refused_{}_pixels'.format(binRefusedCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    binRefusedCount += 1
                    imsave('./data/refuse/refused_{}_pixels.png'.format(imgRefusedCount), imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                    imgRefusedCount += 1
                arrow.remove()   # removing the arrow must be the last thing to do at the end of the if-block

    print('Feature detection completed.')
    plt.show()

elif args.Mode == 'stack':
    img_1 = args.layer_1
    img_2 = args.layer_2
    pivot_1 = args.feature_1
    pivot_2 = args.feature_2

    align(img_1, img_2, pivot_1, pivot_2)
