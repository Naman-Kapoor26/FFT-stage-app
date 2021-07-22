from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')

class MainApp(App):
    def build(self):
        self.operators = [",", "j", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=True, readonly=True, halign="left", font_size=30,
            size_hint_y = None, 
            height=250
            )
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", ","],
            ["4", "5", "6", "j"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5 , "center_y": 0.5},
                    
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            '''if current and (
                self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return'''
            if current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(self.solution.text)
            li=solution.split(',')
            ki=[]
            for i in li:
                ki.append(complex(i))
            import math
            from cmath import exp,pi
            def W(A,B,n=0):
                a=A+B*exp(-1j*pi*n/4)
                a=complex(round(a.real,3),round(a.imag,3))
                b=A-B*exp(-1j*pi*n/4)
                b=complex(round(b.real,3),round(b.imag,3))
                return([a,b])
            def stage1(x):
                a=W(x[0],x[4])
                b=W(x[2],x[6])
                c=W(x[1],x[5])
                d=W(x[3],x[7])
                return([a[0],a[1],b[0],b[1],c[0],c[1],d[0],d[1]])
            def stage2(x):
                a=W(stage1(x)[0],stage1(x)[2])
                b=W(stage1(x)[1],stage1(x)[3],2)
                c=W(stage1(x)[4],stage1(x)[6])
                d=W(stage1(x)[5],stage1(x)[7],2)
                return([a[0],b[0],a[1],b[1],c[0],d[0],c[1],d[1]])
            def stage3(x):
                a=W(stage2(x)[0],stage2(x)[4])
                b=W(stage2(x)[1],stage2(x)[5],1)
                c=W(stage2(x)[2],stage2(x)[6],2)
                d=W(stage2(x)[3],stage2(x)[7],3)
                return([a[0],b[0],c[0],d[0],a[1],b[1],c[1],d[1]])
            def DIT_FFT(x):
                #RESULT={}
                #RESULT['Stage1']=stage1(x)
                #RESULT['Stage2']=stage2(x)
                #RESULT['Stage3']=stage3(x)
                #print('Stage1',stage1(x))
                #print('Stage2',stage2(x))
                #print('Stage3',stage3(x))
                return """STAGE1:{0}\nSTAGE2:{1}\nSTAGE3:{2}""".format(stage1(x),stage2(x),stage3(x))
            
            self.solution.text = str(DIT_FFT(ki))


if __name__ == "__main__":
    app = MainApp()
    app.run()
