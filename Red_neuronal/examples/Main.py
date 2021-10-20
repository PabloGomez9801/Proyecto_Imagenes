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
for i in range(58,62):
    # Always 13 frames
    #print("Display image which has index %d:" %i) #opcion de seleccionar frame para detectar por medio de index
    #auairdataset.display_bboxes(i)
    #ret_name = "frame_20190905091750_x_00048" + str(i) + ".jpg" #Video 2
    #ret_name = "frame_20190905103112_x_00022"+str(i)+".jpg" #Video 3
    ret_name = "frame_20190905111947_x_00003" + str(i) + ".jpg"  # Video 4
    #auairdataset.display_bboxes(ret_name)
    #ret_name = "frame_20190905112522_x_000219"+str(i)+".jpg" #Video 5.1
    #ret_name = "frame_20190905112522_x_000220"+str(i)+".jpg" # Video 5.2
    #ret_name = "frame_20190905112522_x_000220"+str(i)+".jpg" # Video 5.3-5.4

    auairdataset.display_bboxes(ret_name)

print("Done")
##############################################################