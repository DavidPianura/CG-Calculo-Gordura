from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import pyvista as pv
import threading

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', 0)

from kivy.core.window import Window
Window.clearcolor = (0.1, 0.4, 1)

class CG(Widget):    
    lbl_volume = ObjectProperty(None)
    lbl_densidade = ObjectProperty(None)
    lbl_gordura = ObjectProperty(None)
    txt_altura = ObjectProperty(None)
    txt_peso = ObjectProperty(None)
    
    def render_ply(self):
        def show_ply():
            mesh = pv.read("thales_processado.ply")
            plotter = pv.Plotter()
            plotter.add_mesh(mesh)
            plotter.show()

        threading.Thread(target=show_ply, daemon=True).start()

    def calcula_vol_pulmao(self, altura, peso):
        return (((0.0472*(altura))+(0.000009*peso))-5.92)*1000
    
    def calcula_densidade(self, peso, vol_pulmao):
        volume = 104857896/1000
        return peso/(volume - vol_pulmao) 
    
    def calcula_percentual_gordura(self, densidade):
        return (437/densidade)-393
        
    
    def calcular(self):
        try:
            altura = float(self.txt_altura.text)
            peso = float(self.txt_peso.text)
            vol_pulmao = self.calcula_vol_pulmao(altura, peso)
            densidade = self.calcula_densidade(peso, vol_pulmao)
            percentual_gordura = self.calcula_percentual_gordura(densidade)
            
            self.lbl_gordura.text = f"% de gordura: {percentual_gordura:.2f}"
            self.lbl_volume.text = f"Volume Pulmão: {vol_pulmao:.2f}"
            self.lbl_densidade.text = f"Densidade: {densidade}"

        except ValueError:
            self.lbl_gordura.text = f"% de gordura: Erro! Defina os campos primeiro!"
            self.lbl_volume.text = "Volume Pulmão: Erro!"
            self.lbl_densidade.text = "Densidade: Erro!"

class FormularioApp(App):
    def build(self):
        return CG()

if __name__ == "__main__":
    FormularioApp().run()
