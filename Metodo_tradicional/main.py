import numpy as np
import imutils
import cv2
from imutils.object_detection import non_max_suppression

# Función para alinear frames
def align_images(image, template, maxFeatures=2000, keepPercent=0.2, debug=False):
    # Se convierten las dos entradas a escala de grises
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # Se usa el ORB para detectar los keypoints
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    # Se emparejan las características
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)
    # Se ordenan los emparejamientos por su distancia
    matches = sorted(matches, key=lambda x: x.distance)
    # Se toman solo los mas altos emparejamientos
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]
    # Revisar si es posible observar los keypoints
    if debug:
        matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)
    # Se guardan en la memoria los keypoints
    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")
    for (i, m) in enumerate(matches):
        # Indica que dos keypoints de la imagen encajan
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt
    # SE computa la homografía
    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
    # Se alinean la imagen de entrada según el template
    (h, w) = template.shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    return aligned
# Función para extraer los frames del drive
def extract_frames(i):
    # Direccion donde se encuentra el dataset pre procesado.
    frame = cv2.imread('C:\\Users\\Pablo Gomez\\Desktop\\images\\Video 5\\frame (' + str(i) + ').jpg')
    return frame
# Función para preparar los frames para la sustracción de fondo
def set_images(aligned, template):
    # Se cambia el tamaño de los frames para su visualización
    aligned = imutils.resize(aligned, width=700)
    template = imutils.resize(template, width=700)
    # Se obtiene el una imágen sobrepuesta de el template y el frame alineado a este
    overlay = template.copy()
    output = aligned.copy()
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    cv2.imshow("Imagen sobrepuesta", output)
    # Se convierten a escala de grises las entradas
    alignedGray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    height, width = alignedGray.shape
    # Se crea una mascara con el fin de eliminar las zonas vacías originadas por la alineación
    mask = np.zeros(alignedGray.shape[:2], dtype="uint8")
    mask[np.abs(alignedGray) > 0] = 255
    templateGray = cv2.bitwise_and(templateGray, templateGray, mask=mask)
    return alignedGray, templateGray, output

frameCnt = 2025
M = -1
pickf = []
while (frameCnt < 5000):

    frameCnt += 1
    template = extract_frames(frameCnt)
    frame = extract_frames(frameCnt+1)
    aligned = align_images(frame, template, debug=True)
    frame = imutils.resize(frame, width=700)
    alignedGray, templateGray, output = set_images(aligned, template)
    #Background subtraction
    dframe = cv2.absdiff(alignedGray, templateGray)
    #Se desenfoca la imágen resultante
    blurred = cv2.GaussianBlur(dframe, (11, 11), 0)
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(blurred, dilate_kernel, iterations=4)
    dilate[np.abs(dilate) < 50] = 0
    # Thresholding to binarise
    ret, tframe = cv2.threshold(dilate, 0, 255,
                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    (cnts, _) = cv2.findContours(tframe.copy(),
                                 cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects=[]
    MN = np.average(dilate)
    if(M==-1):
        M = MN
    frame_detect = frame.copy()
    # Se crean los contornos
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        rects.append([x, y, x + w, y + h])
    rects = np.array(rects)
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.95)
    if (MN < M + 2.5 ):
        pickf = pick
        M=MN
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(frame_detect, (xA, yA), (xB, yB), (0, 255, 0), 2)
    else:
        for (xA, yA, xB, yB) in pickf:
            cv2.rectangle(frame_detect, (xA, yA), (xB, yB), (0, 255, 0), 2)

    dilate = cv2.merge([dilate,dilate, dilate])
    final_frame1 = np.hstack([frame,output])
    final_frame2 = np.hstack([dilate, frame_detect])
    final_frame = np.vstack([final_frame1, final_frame2])
    cv2.imshow("Deteccion de objetos en movimiento", final_frame)
    # Presionar cualquier tecla para continuar al siguiente frame
    cv2.waitKey(0)