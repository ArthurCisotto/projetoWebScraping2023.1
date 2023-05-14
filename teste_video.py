
import cv2
import os,sys, os.path
import numpy as np
import easyocr

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

data_dir = os.getcwd() + "/data/img/"
print("Diretório de dados: ", data_dir)

# Carrega a imagem
#img = cv2.imread(data_dir + "IMG_4124.jpg")
#scale image to fit 'window'
#img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)
# Convert to grayscale
def digit_recognition(img):
    # Carrega a imagem
    # img = cv2.imread(data_dir + "IMG_4124.jpg")
    # scale image to fit 'window'
    img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    # Convert to grayscale

    WIDTH = img.shape[1]
    HEIGHT = img.shape[0]

    img_cropped = img[int(HEIGHT / 2 - 200):int(HEIGHT / 2 + 200), int(WIDTH / 2 - 200):int(WIDTH / 2 + 200)]
    img_gray_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, img_thresh = cv2.threshold(img_gray_cropped, 250, 255, cv2.THRESH_BINARY)

    # Crop center square

    mask = img_thresh.copy()
    mask = cv2.blur(mask, (5, 5))

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))

    # INVERT COLOR
    mask = cv2.bitwise_not(mask)

    reader = easyocr.Reader(lang_list=['pt'], gpu=False)
    texto = reader.readtext(mask, detail=0)

    texto = texto[0].replace(" ", "")

    img_rgb = img_cropped.copy()
    cropped_height = img_rgb.shape[0]
    cropped_width = img_rgb.shape[1]

    cv2.putText(img_rgb, texto, (int(cropped_width / 2), int(cropped_height / 2 + 50)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 0, 0), 2)

    return img_rgb
# Mostra a imagem segmentada


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture("data/video/video.mov")

    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        print("Capturando frame")
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if frame is None:
            print("Frame vazio")
            break
        # Our operations on the frame come here
        img = frame.copy()

        try:
            img = digit_recognition(img)
        except:
            print("Erro ao processar imagem")
            pass
        
        

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('Input', frame)
        cv2.imshow('Output', img)

        # Pressione 'q' para interromper o video
        if cv2.waitKey(1000//30) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
