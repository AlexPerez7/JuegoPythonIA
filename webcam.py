from threading import Thread
import cv2
import platform
    
class Webcam:
    def __init__(self):
         # Variable para indicar si la transmisión de la cámara ha sido detenida
        self.stopped = False
         # Objeto para capturar la transmisión de video desde la cámara
        self.stream = None
        # Último cuadro de video capturado por la cámara
        self.lastFrame = None
        # Variable para almacenar el nombre del sistema operativo
        self.os_name = platform.system()

    def start(self):
        # Crear un nuevo hilo para actualizar los cuadros de video capturados por la cámara
        t = Thread(target=self.update, args=())
        # Hacer que el hilo sea un demonio, lo que significa que se detendrá automáticamente cuando se detenga el programa principal
        t.daemon = True
        # Iniciar el hilo
        t.start()
        return self

    def update(self):
        if self.stream is None:
            # Configurar la transmisión de video para Windows
            if self.os_name == "Windows":
                self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                # Configurar la transmisión de video para macOS
            elif self.os_name == "Darwin":
                self.stream = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else:
                # Configurar la transmisión de video para Linux
                self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)
        while True:
            if self.stopped:
                return
            # Leer un nuevo cuadro de video de la transmisión de la cámara
            (result, image) = self.stream.read()
            if not result:
                self.stop()
                return
            # Actualizar el último cuadro de video capturado
            self.lastFrame = image

    # Devuelve el último cuadro de video capturado por la cámara            
    def read(self):
        return self.lastFrame

    # Detener la transmisión de video de la cámara
    def stop(self):
        self.stopped = True

    # Obtener el ancho de la transmisión de video de la cámara
    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH )

    # Obtener la altura de la transmisión de video de la cámara
    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT )

    # Devuelve True si el último cuadro de video capturado está listo para ser procesado 
    def ready(self):
        return self.lastFrame is not None