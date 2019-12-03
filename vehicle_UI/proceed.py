# # show images inline
# % matplotlib
# inline
#
# # automatically reload modules when they have changed
# % load_ext
# autoreload
# % autoreload
# 2

# import keras
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf


def start_proceed(img_path):
    def get_session():
        # for tf2.0
        # config = tf.compat.v1.ConfigProto()
        # for tf 1.x
        config = tf.ConfigProto()

        config.gpu_options.allow_growth = True

        # tf2.0
        # return tf.compat.v1.Session(config=config)
        # tf 1.x
        return tf.Session(config=config)


    # use this environment flag to change which GPU to use
    # os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    # set the modified tf session as backend in keras
    keras.backend.tensorflow_backend.set_session(get_session())

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    filename = 'keras-retinanet/path/classes.csv'

    # df = pd.read_csv(filename, header=None)

    model_path2 = ('keras-retinanet/snapshots/converted_restnet50_model.h5')

    # load retinanet model
    model = models.load_model(model_path2, backbone_name='resnet50')

    # if the model is not converted to an inference model, use the line below
    # see: https://github.com/fizyr/keras-retinanet#converting-a-training-model-to-inference-model
    # model = models.convert_model(model)


    # load label to names mapping for visualization purposes
    # labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
    #                    7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter',
    #                    13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant',
    #                    21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie',
    #                    28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite',
    #                    34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
    #                    39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
    #                    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog',
    #                    53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
    #                    60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
    #                    67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
    #                    73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
    #                    79: 'toothbrush'}
    labels_to_names = {0: 'AM General Hummer SUV 2000', 1: 'Acura RL Sedan 2012', 2: 'Acura TL Sedan 2012',
                       3: 'Acura TL Type-S 2008', 4: 'Acura TSX Sedan 2012', 5: 'Acura Integra Type R 2001',
                       6: 'Acura ZDX Hatchback 2012', 7: 'Aston Martin V8 Vantage Convertible 2012',
                       8: 'Aston Martin V8 Vantage Coupe 2012', 9: 'Aston Martin Virage Convertible 2012',
                       10: 'Aston Martin Virage Coupe 2012', 11: 'Audi RS 4 Convertible 2008', 12: 'Audi A5 Coupe 2012',
                       13: 'Audi TTS Coupe 2012', 14: 'Audi R8 Coupe 2012', 15: 'Audi V8 Sedan 1994',
                       16: 'Audi 100 Sedan 1994', 17: 'Audi 100 Wagon 1994', 18: 'Audi TT Hatchback 2011',
                       19: 'Audi S6 Sedan 2011', 20: 'Audi S5 Convertible 2012', 21: 'Audi S5 Coupe 2012',
                       22: 'Audi S4 Sedan 2012', 23: 'Audi S4 Sedan 2007', 24: 'Audi TT RS Coupe 2012',
                       25: 'BMW ActiveHybrid 5 Sedan 2012', 26: 'BMW 1 Series Convertible 2012',
                       27: 'BMW 1 Series Coupe 2012', 28: 'BMW 3 Series Sedan 2012', 29: 'BMW 3 Series Wagon 2012',
                       30: 'BMW 6 Series Convertible 2007', 31: 'BMW X5 SUV 2007', 32: 'BMW X6 SUV 2012',
                       33: 'BMW M3 Coupe 2012', 34: 'BMW M5 Sedan 2010', 35: 'BMW M6 Convertible 2010',
                       36: 'BMW X3 SUV 2012', 37: 'BMW Z4 Convertible 2012',
                       38: 'Bentley Continental Supersports Conv. Convertible 2012', 39: 'Bentley Arnage Sedan 2009',
                       40: 'Bentley Mulsanne Sedan 2011', 41: 'Bentley Continental GT Coupe 2012',
                       42: 'Bentley Continental GT Coupe 2007', 43: 'Bentley Continental Flying Spur Sedan 2007',
                       44: 'Bugatti Veyron 16.4 Convertible 2009', 45: 'Bugatti Veyron 16.4 Coupe 2009',
                       46: 'Buick Regal GS 2012', 47: 'Buick Rainier SUV 2007', 48: 'Buick Verano Sedan 2012',
                       49: 'Buick Enclave SUV 2012', 50: 'Cadillac CTS-V Sedan 2012', 51: 'Cadillac SRX SUV 2012',
                       52: 'Cadillac Escalade EXT Crew Cab 2007', 53: 'Chevrolet Silverado 1500 Hybrid Crew Cab 2012',
                       54: 'Chevrolet Corvette Convertible 2012', 55: 'Chevrolet Corvette ZR1 2012',
                       56: 'Chevrolet Corvette Ron Fellows Edition Z06 2007', 57: 'Chevrolet Traverse SUV 2012',
                       58: 'Chevrolet Camaro Convertible 2012', 59: 'Chevrolet HHR SS 2010',
                       60: 'Chevrolet Impala Sedan 2007', 61: 'Chevrolet Tahoe Hybrid SUV 2012',
                       62: 'Chevrolet Sonic Sedan 2012', 63: 'Chevrolet Express Cargo Van 2007',
                       64: 'Chevrolet Avalanche Crew Cab 2012', 65: 'Chevrolet Cobalt SS 2010',
                       66: 'Chevrolet Malibu Hybrid Sedan 2010', 67: 'Chevrolet TrailBlazer SS 2009',
                       68: 'Chevrolet Silverado 2500HD Regular Cab 2012',
                       69: 'Chevrolet Silverado 1500 Classic Extended Cab 2007', 70: 'Chevrolet Express Van 2007',
                       71: 'Chevrolet Monte Carlo Coupe 2007', 72: 'Chevrolet Malibu Sedan 2007',
                       73: 'Chevrolet Silverado 1500 Extended Cab 2012', 74: 'Chevrolet Silverado 1500 Regular Cab 2012',
                       75: 'Chrysler Aspen SUV 2009', 76: 'Chrysler Sebring Convertible 2010',
                       77: 'Chrysler Town and Country Minivan 2012', 78: 'Chrysler 300 SRT-8 2010',
                       79: 'Chrysler Crossfire Convertible 2008', 80: 'Chrysler PT Cruiser Convertible 2008',
                       81: 'Daewoo Nubira Wagon 2002', 82: 'Dodge Caliber Wagon 2012', 83: 'Dodge Caliber Wagon 2007',
                       84: 'Dodge Caravan Minivan 1997', 85: 'Dodge Ram Pickup 3500 Crew Cab 2010',
                       86: 'Dodge Ram Pickup 3500 Quad Cab 2009', 87: 'Dodge Sprinter Cargo Van 2009',
                       88: 'Dodge Journey SUV 2012', 89: 'Dodge Dakota Crew Cab 2010', 90: 'Dodge Dakota Club Cab 2007',
                       91: 'Dodge Magnum Wagon 2008', 92: 'Dodge Challenger SRT8 2011', 93: 'Dodge Durango SUV 2012',
                       94: 'Dodge Durango SUV 2007', 95: 'Dodge Charger Sedan 2012', 96: 'Dodge Charger SRT-8 2009',
                       97: 'Eagle Talon Hatchback 1998', 98: 'FIAT 500 Abarth 2012', 99: 'FIAT 500 Convertible 2012',
                       100: 'Ferrari FF Coupe 2012', 101: 'Ferrari California Convertible 2012',
                       102: 'Ferrari 458 Italia Convertible 2012', 103: 'Ferrari 458 Italia Coupe 2012',
                       104: 'Fisker Karma Sedan 2012', 105: 'Ford F-450 Super Duty Crew Cab 2012',
                       106: 'Ford Mustang Convertible 2007', 107: 'Ford Freestar Minivan 2007',
                       108: 'Ford Expedition EL SUV 2009', 109: 'Ford Edge SUV 2012', 110: 'Ford Ranger SuperCab 2011',
                       111: 'Ford GT Coupe 2006', 112: 'Ford F-150 Regular Cab 2012', 113: 'Ford F-150 Regular Cab 2007',
                       114: 'Ford Focus Sedan 2007', 115: 'Ford E-Series Wagon Van 2012', 116: 'Ford Fiesta Sedan 2012',
                       117: 'GMC Terrain SUV 2012', 118: 'GMC Savana Van 2012', 119: 'GMC Yukon Hybrid SUV 2012',
                       120: 'GMC Acadia SUV 2012', 121: 'GMC Canyon Extended Cab 2012', 122: 'Geo Metro Convertible 1993',
                       123: 'HUMMER H3T Crew Cab 2010', 124: 'HUMMER H2 SUT Crew Cab 2009',
                       125: 'Honda Odyssey Minivan 2012', 126: 'Honda Odyssey Minivan 2007', 127: 'Honda Accord Coupe 2012',
                       128: 'Honda Accord Sedan 2012', 129: 'Hyundai Veloster Hatchback 2012',
                       130: 'Hyundai Santa Fe SUV 2012', 131: 'Hyundai Tucson SUV 2012', 132: 'Hyundai Veracruz SUV 2012',
                       133: 'Hyundai Sonata Hybrid Sedan 2012', 134: 'Hyundai Elantra Sedan 2007',
                       135: 'Hyundai Accent Sedan 2012', 136: 'Hyundai Genesis Sedan 2012',
                       137: 'Hyundai Sonata Sedan 2012', 138: 'Hyundai Elantra Touring Hatchback 2012',
                       139: 'Hyundai Azera Sedan 2012', 140: 'Infiniti G Coupe IPL 2012', 141: 'Infiniti QX56 SUV 2011',
                       142: 'Isuzu Ascender SUV 2008', 143: 'Jaguar XK XKR 2012', 144: 'Jeep Patriot SUV 2012',
                       145: 'Jeep Wrangler SUV 2012', 146: 'Jeep Liberty SUV 2012', 147: 'Jeep Grand Cherokee SUV 2012',
                       148: 'Jeep Compass SUV 2012', 149: 'Lamborghini Reventon Coupe 2008',
                       150: 'Lamborghini Aventador Coupe 2012', 151: 'Lamborghini Gallardo LP 570-4 Superleggera 2012',
                       152: 'Lamborghini Diablo Coupe 2001', 153: 'Land Rover Range Rover SUV 2012',
                       154: 'Land Rover LR2 SUV 2012', 155: 'Lincoln Town Car Sedan 2011',
                       156: 'MINI Cooper Roadster Convertible 2012', 157: 'Maybach Landaulet Convertible 2012',
                       158: 'Mazda Tribute SUV 2011', 159: 'McLaren MP4-12C Coupe 2012',
                       160: 'Mercedes-Benz 300-Class Convertible 1993', 161: 'Mercedes-Benz C-Class Sedan 2012',
                       162: 'Mercedes-Benz SL-Class Coupe 2009', 163: 'Mercedes-Benz E-Class Sedan 2012',
                       164: 'Mercedes-Benz S-Class Sedan 2012', 165: 'Mercedes-Benz Sprinter Van 2012',
                       166: 'Mitsubishi Lancer Sedan 2012', 167: 'Nissan Leaf Hatchback 2012',
                       168: 'Nissan NV Passenger Van 2012', 169: 'Nissan Juke Hatchback 2012',
                       170: 'Nissan 240SX Coupe 1998', 171: 'Plymouth Neon Coupe 1999', 172: 'Porsche Panamera Sedan 2012',
                       173: 'Ram C/V Cargo Van Minivan 2012', 174: 'Rolls-Royce Phantom Drophead Coupe Convertible 2012',
                       175: 'Rolls-Royce Ghost Sedan 2012', 176: 'Rolls-Royce Phantom Sedan 2012',
                       177: 'Scion xD Hatchback 2012', 178: 'Spyker C8 Convertible 2009', 179: 'Spyker C8 Coupe 2009',
                       180: 'Suzuki Aerio Sedan 2007', 181: 'Suzuki Kizashi Sedan 2012', 182: 'Suzuki SX4 Hatchback 2012',
                       183: 'Suzuki SX4 Sedan 2012', 184: 'Tesla Model S Sedan 2012', 185: 'Toyota Sequoia SUV 2012',
                       186: 'Toyota Camry Sedan 2012', 187: 'Toyota Corolla Sedan 2012', 188: 'Toyota 4Runner SUV 2012',
                       189: 'Volkswagen Golf Hatchback 2012', 190: 'Volkswagen Golf Hatchback 1991',
                       191: 'Volkswagen Beetle Hatchback 2012', 192: 'Volvo C30 Hatchback 2012',
                       193: 'Volvo 240 Sedan 1993', 194: 'Volvo XC90 SUV 2007', 195: 'smart fortwo Convertible 2012'}


    # model.summary()

    # df_test = pd.read_csv("keras-retinanet/path/annotations_test.csv", header=None)

    # load image
    # image = read_image_bgr('/Users/joey/Nutstore Files/我的坚果云/vehicle/00003.jpg')
    image = read_image_bgr(img_path)

    # copy to draw on
    draw = image.copy()
    draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

    # preprocess image for network
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    process_time=time.time()-start
    # print("processing time: ", time.time() - start)

    # print(labels)
    # correct for image scale
    boxes /= scale

    # visualize detections
    for box, score, label in zip(boxes[0], scores[0], labels[0]):
        # scores are sorted so we can break
        if score < 0.5:
            break

        color = label_color(label)

        b = box.astype(int)
        draw_box(draw, b, color=color)

        # print(labels_to_names[label])
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)

    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(draw)
    plt.savefig('output.jpg')
    # plt.show()
    # print(caption)
    return caption,process_time


if __name__=='__main__':
    pass
    # start_proceed('/Users/joey/Nutstore Files/我的坚果云/vehicle/00003.jpg')
# def trans_data():
#         return caption


