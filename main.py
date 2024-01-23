from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
from kivy.clock import Clock

class VRApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='horizonta')
        self.image_left = Image()
        self.image_right = Image()
        self.layout.add_widget(self.image_left)
        self.layout.add_widget(self.image_right)

        # Inicializa a captura de vídeo
        self.capture = cv2.VideoCapture(0)

        # Define a função de atualização do vídeo a ser chamada periodicamente
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        return self.layout

    def update(self, dt):
        # Lê um quadro da câmera
        ret, frame = self.capture.read()

        # Divide o quadro em duas imagens (lente esquerda e lente direita)
        height, width, _ = frame.shape
        half_width = width // 2

        frame_left = frame[:, :half_width, :]
        frame_right = frame[:, half_width:, :]

        # Converte as imagens OpenCV para texturas Kivy
        texture_left = self.convert_frame_to_texture(frame_left)
        texture_right = self.convert_frame_to_texture(frame_right)

        # Atualiza as texturas nas imagens
        self.image_left.texture = texture_left
        self.image_right.texture = texture_right

    def convert_frame_to_texture(self, frame):
        # Converte o quadro OpenCV para uma textura Kivy
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture

    def on_stop(self):
        # Libera os recursos da câmera ao fechar o aplicativo
        self.capture.release()

if __name__ == '__main__':
    VRApp().run()
