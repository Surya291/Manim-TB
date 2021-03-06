from manimlib.imports import *

set_custom_quality(800,10)

OUTPUT_DIRECTORY = "TESTS/ANIMATIONS_TESTS"

class AnimationTest(Scene):
	def construct(self):
		t=Text("Hola")
		self.Oldplay(Escribe(t))
		self.wait()

class TypeWriterScene(Scene):
    def construct(self):
        texto=Text("\\tt Ojalá funcione")[0]
        self.wait()
        KeyBoard(self,texto,lag=0.1)
        self.wait()

class TimeTest(Scene):
	def print_time(self):
		print("Time:",round(self.time))

	def construct(self):
		dot=Dot()
		# 0 seconds
		self.print_time()
		self.play(Write(dot,run_time=2))
		# 2 second
		self.print_time()
		self.wait()
		# 3 seconds
		self.print_time()
		self.play(dot.shift,UP,run_time=1)
		# 4 seconds
		self.print_time()
		self.play(FadeToColor(dot,RED,run_time=3))
		# 7 seconds
		self.print_time()
		self.wait()
		# 8 seconds
		self.print_time()

class NewOwnAnimations(Scene):
    def construct(self):
        text1=Formula("x=\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}")[0]
        text2=Text("Alexander")
        obj=Circle(color=RED,fill_opacity=1)

        VGroup(text1,text2,obj).arrange(DOWN)

        text1.move_to(ORIGIN)

        self.wait(0.2)

        #"""
        self.play(
            FadeIn(text1,submobject_mode="lagged_start",rate_func=linear),
            )
        self.play(
            LaggedStart(
            *[FadeInFromPoint(obj,point=[2,0,0])for obj in text1])
        )
        directions=[DL,DOWN,DR,RIGHT,UR,UP,UL,LEFT]
        cycle_directions=it.cycle(directions)
        reverse_directions=it.cycle(list(reversed(directions)))
        self.play(
            LaggedStart(
            *[FadeInFromPoint(obj,point=obj.get_center()+d)for obj,d in zip(text1,reverse_directions)])
        )
        #"""
        

        def get_vector_from(obj,point=ORIGIN,dist=2):
            vect=obj.get_center()-point
            return vect*dist
        
        """
        self.play(
            LaggedStart(
            *[FadeInFromPoint(obj,point=get_vector_from(obj,dist=1.4))for obj in text1]),
            run_time=2
        )
        """
        

        self.wait()

class Indice1(EscenaContenido):
    CONFIG={
    "escala":0.9,
    "mover_contenido":[2,-0.5,0],
    "font_titulo":"\\rm",
    "salida":True,
    "tiempo_espera":3,
    }
    def setup(self):
        self.contenido=[
            "¿Qué es \\tt CONFIG?",
            "sub tema 1",
            "sub tema 2",
            "--",
            "¿Cómo cambiar el color de fondo?",
            "--",
            "\\,"
            ]

class PatternExample(Scene):
    def construct(self):
        pattern_1=RectanglePattern(4,2)
        pattern_2=RectanglePattern(3,add_rectangle=True)
        pattern_3=RectanglePattern(3,6,color=ORANGE)

        pg=VGroup(pattern_1,pattern_2,pattern_3).arrange(RIGHT)
        self.add(pg)

class MeasureObject(Scene):
    def construct(self):
        square=Square()
        measure_line=Line(square.get_corner(DL),square.get_corner(UL))
        measure=MeasureDistance(measure_line).add_tips()
        measure_tex=measure.get_tex("x")
        self.add(square,measure,measure_tex)

class ScreenGridScene(Scene):
    def construct(self):
        screen_grid=ScreenGrid()
        self.add(screen_grid)

class ArrangeScene(Scene):
    def construct(self):
        dots=VGroup(*[Dot() for _ in range(4)])
        dots.arrange_list_to_left()
        self.add(dots)

class ArrangeScene2(Scene):
    def construct(self):
        dots=VGroup(
            FontText("a"),
            FontText("b"),
            FontText("."),
            FontText("X"),
            FontText("y"),
            )
        dots.arrange_in_grid(len(dots),1)
        self.add(dots)

class ArrangeScene3(Scene):
    def construct(self):
        dots=VGroup(
            FontText("a"),
            FontText("b"),
            FontText("."),
            FontText("X"),
            FontText("y"),
            )
        dots.arrange_in_grid(len(dots),1)
        self.add(dots)

class BackgroundScene(Scene):
    def construct(self):
        f1=FontText("Daniel Alexander")
        f2=FontText("Vázquez Zaldivar")
        f3=FontText("Es el mejor")

        fs=VGroup(f1,f2,f3)#.arrange_list_to_left(2)
        max_height=0
        for f in fs:
            f_w=f.get_height()
            max_height=max(f_w,max_height)
        background_rectangle=Rectangle(height=max_height)
        new_fs=VGroup()
        for f in fs:
            br=background_rectangle.copy()
            br.stretch_to_fit_width(f.get_width())
            br.move_to(f)
            f.shift(DOWN*(max_height-f.get_height())/2)
            new_fs.add(VGroup(f,br))
        new_fs.arrange_list_to_left()
        #for f in new_fs:
        #    f.remove(f[1])
        self.add(new_fs)