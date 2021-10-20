import cv2
from PIL import Image, ImageOps
from auairtools.auair import AUAIR

# Paths to annotation file and source data.
annotFile = 'C:/Users/Pablo Gomez/Desktop/Red Neuronal/examples/auair_subset/annotations.json'
#Direccion de la carpeta donde se encuentran las anotaciones en un archivo .json
dataDir = 'C:/Users/Pablo Gomez/Desktop/Red Neuronal/examples/auair_subset/images2'
#Direccion de la carpeta donde se encuentra el dataset Raw, tal cual lo entrega AuairDataset

# Create a AUAIR object.
auairdataset = AUAIR(annotation_file=annotFile, data_folder = dataDir)

##############################################################
      #MOSTRAR LAS IMAGENES YA CON LA CLASIFICACION#
##############################################################
for i in range(10,23):
    # Always 13 frames
    #print("Display image which has index %d:" %i) #opcion de seleccionar frame para detectar por medio de index
    #auairdataset.display_bboxes(i)
    # ret_name = "frame_20190905091750_x_00002"+str(i)+".jpg"
    #ret_name = "frame_20190905103112_x_00015"+str(i)+".jpg"
    ret_name = "frame_20190905142119_x_00013" + str(i) + ".jpg"
    #ret_name = "frame_20190905103112_x_00015"+str(i)+".jpg"
    auairdataset.display_bboxes(ret_name)

print("Done")
##############################################################