import weakref

class _Base:
    def set_plot(self, plot):
        self.plot = weakref.proxy(plot)
        return self

    def reset(self):
        pass

class Point(_Base):
    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        self.plot.point(x, y, r, g, b, a)

class Plus(_Base):
    def __init__(self, size=5):
        self.size = size

    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        def vertexor(view, w, h):
            size_x = self.size / w * view.w
            size_y = self.size / h * view.h
            self.plot.line(x-size_x, y, x+size_x, y, r, g, b, a)
            self.plot.line(x, y-size_y, x, y+size_y, r, g, b, a)
        self.plot.late_vertexor(vertexor)

class Cross(_Base):
    def __init__(self, size=5):
        self.size = size

    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        def vertexor(view, w, h):
            size_x = self.size / w * view.w
            size_y = self.size / h * view.h
            self.plot.line(x-size_x, y-size_y, x+size_x, y+size_y, r, g, b, a)
            self.plot.line(x-size_x, y+size_y, x+size_x, y-size_y, r, g, b, a)
        self.plot.late_vertexor(vertexor)

class Line(_Base):
    def __init__(self):
        self.reset()

    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        if self.x:
            self.plot.line(self.x, self.y, x, y, r, g, b, a)
        else:
            self.plot.point(x, y, r, g, b, a)
        self.x = x
        self.y = y

    def reset(self):
        self.x = None
        self.y = None

class Compound(_Base):
    def __init__(self, *primitives):
        self.primitives = primitives

    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        for i in self.primitives:
            i(x, y, r, g, b, a)

    def set_plot(self, plot):
        for i in self.primitives:
            i.set_plot(plot)
        return self

    def reset(self):
        for i in self.primitives:
            i.reset()
