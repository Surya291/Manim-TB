from mobject import Mobject
from image_mobject import ImageMobject
from helpers import *

#TODO, Cleanup and refactor this file.

class TexMobject(Mobject):
    DEFAULT_CONFIG = {
        "template_tex_file" : TEMPLATE_TEX_FILE,
        "color"             : WHITE,
        "point_thickness"   : 1,
        "should_center"     : False,
    }
    def __init__(self, expression, **kwargs):
        if "size" not in kwargs:
            #Todo, make this more sophisticated.
            if len("".join(expression)) < MAX_LEN_FOR_HUGE_TEX_FONT:
                size = "\\Huge"
            else:
                size = "\\large"
        digest_locals(self)
        Mobject.__init__(self, **kwargs)

    def generate_points(self):
        image_files = tex_to_image_files(
            self.expression, 
            self.size, 
            self.template_tex_file
        )
        for image_file in image_files:
            self.add(ImageMobject(image_file))
        if self.should_center:
            self.center()
        self.highlight(self.color)



class TextMobject(TexMobject):
    DEFAULT_CONFIG = {
        "template_tex_file" : TEMPLATE_TEXT_FILE,
        "size" : "\\Large", #TODO, auto-adjust?
    }


class Underbrace(TexMobject):
    DEFAULT_CONFIG = {
        "buff" : 0.2,
    }
    def __init__(self, left, right, **kwargs):
        expression = "\\underbrace{%s}"%(14*"\\quad")
        TexMobject.__init__(self, expression, **kwargs)
        result.stretch_to_fit_width(right[0]-left[0])
        result.shift(left - result.points[0] + buff*DOWN)

    

def tex_hash(expression, size):
    return str(hash(expression + size))

def tex_to_image_files(expression, size, template_tex_file):
    """
    Returns list of images for correpsonding with a list of expressions
    """
    image_dir = os.path.join(TEX_IMAGE_DIR, tex_hash(expression, size))
    if os.path.exists(image_dir):
        return get_sorted_image_list(image_dir)
    tex_file = generate_tex_file(expression, size, template_tex_file)
    dvi_file = tex_to_dvi(tex_file)
    return dvi_to_png(dvi_file)


def generate_tex_file(expression, size, template_tex_file):
    if isinstance(expression, list):
        expression = tex_expression_list_as_string(expression)
    result = os.path.join(TEX_DIR, tex_hash(expression, size))+".tex"
    if not os.path.exists(result):
        print "Writing %s at size %s to %s"%(
            "".join(expression), size, result
        )
        with open(template_tex_file, "r") as infile:
            body = infile.read()
            body = body.replace(SIZE_TO_REPLACE, size)
            body = body.replace(TEX_TEXT_TO_REPLACE, expression)
        with open(result, "w") as outfile:
            outfile.write(body)
    return result

def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi")
    if not os.path.exists(result):
        commands = [
            "latex", 
            "-interaction=batchmode", 
            "-output-directory=" + TEX_DIR,
            tex_file,
            "> /dev/null"
        ]
        #TODO, Error check
        os.system(" ".join(commands))
    return result

def tex_expression_list_as_string(expression):
    return "\n".join([
        "\onslide<%d>{"%count + exp + "}"
        for count, exp in zip(it.count(1), expression)
    ])

def dvi_to_png(dvi_file, regen_if_exists = False):
    """
    Converts a dvi, which potentially has multiple slides, into a 
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    directory, filename = os.path.split(dvi_file)
    name = filename.replace(".dvi", "")
    images_dir = os.path.join(TEX_IMAGE_DIR, name)
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
    if os.listdir(images_dir) == [] or regen_if_exists:
        commands = [
            "convert",
            "-density",
            str(PDF_DENSITY),
            dvi_file,
            "-size",
            str(DEFAULT_WIDTH) + "x" + str(DEFAULT_HEIGHT),
            os.path.join(images_dir, name + ".png")
        ]
        os.system(" ".join(commands))
    return get_sorted_image_list(images_dir)
    

def get_sorted_image_list(images_dir):
    return sorted([
        os.path.join(images_dir, name)
        for name in os.listdir(images_dir)
        if name.endswith(".png")
    ], cmp_enumerated_files)

def cmp_enumerated_files(name1, name2):
    num1, num2 = [
        int(name.split(".")[0].split("-")[-1]) 
        for name in (name1, name2)
    ]
    return num1 - num2














