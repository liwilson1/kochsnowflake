# Liam Wilson
# ID: 8730560
import math
import tkinter as tk


class Koch(tk.Frame):
    # Koch constructor
    def __init__(self, root, x, y):
        tk.Frame.__init__(self, root)
        self.window_width, self.window_height = x, y
        # Line coords array
        self.lines = []
        # Line objs array
        self.objs = []
        self.pack(fill=tk.BOTH, expand=True)
        # Canvas to draw KOCH on
        self.canvas = tk.Canvas(self)
        # Events for mouse drag and window resize
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Configure>", self.resize)
        label = tk.Label(self, text="Enter an order: ")
        generate_btn = tk.Button(self, text="Generate", bg="red",
                           command=self.get_order)
        zoom_lbl = tk.Label(self, text="  Zoom: ")
        zoom_in_btn = tk.Button(self, text="+", command=lambda: self.zoom(1.2))
        zoom_out_btn = tk.Button(self, text="-",
                                 command=lambda: self.zoom(0.8))
        self.input = tk.Entry(self, text="1")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        label.pack(fill=tk.X, side="left")
        self.input.pack(fill=tk.X, side="left")
        zoom_lbl.pack(fill=tk.BOTH, side="left")
        zoom_out_btn.pack(fill=tk.X, side="left")
        zoom_in_btn.pack(fill=tk.X, side="left")
        generate_btn.pack(fill=tk.X, side="top")

        # Last x and y values for the on_drag function, set to false as they
        # haven't been set yet
        self.lastx, self.lasty = False, False

    # Get order from input and then start
    def get_order(self):
        order = self.input.get()
        self.start(order)

    # Sets up initial triangle, and then evolves the triangle depending on the
    # order.
    def start(self, order):
        x0, y0 = 100, 300
        x1, y1 = 400, 300
        xc, yc = rotate60(x0, y0, x1, y1)
        self.lines = [(x0, y0, xc, yc), (xc, yc, x1, y1), (x1, y1, x0,y0)]
        self.drawlines()
        for i in range(int(order) - 1):
            self.evolve(order)

    # Evolve by increasing the order of the triangle.
    #
    # split into three sections to find xa,ya and xb,yb. These are 1/3 and 2/3
    # along the line.
    #
    # xc, yc is the point found after rotating the line ((xb,yb), (xa,ya)) by
    # 60 deg about the origin (xa, ya)
    def evolve(self, order):
        newlines = []
        for x0,y0,x1,y1 in self.lines:
            xa,ya,xb,yb = findsections(x0,y0,x1,y1)
            xc, yc = rotate60(xa,ya,xb,yb)
            newlines.extend([(x0,y0,xa,ya), (xa,ya,xc,yc), (xc,yc,xb,yb),
                             (xb, yb, x1, y1)])
        self.lines = newlines
        self.drawlines()

    # Draws lines
    def drawlines(self):
        self.clearcanvas()
        for x0, y0, x1, y1 in self.lines:
            self.objs.append(self.canvas.create_line(x0, y0, x1, y1))
        self.recenter()

    # Clears the canvas by deleting all lines currently on the canvas
    # Then resets the line objs array
    def clearcanvas(self):
        for obj in self.objs:
            self.canvas.delete(obj)
        self.objs = []

    # Zoom function
    # resets canvas, makes a newlines array, fills array with new line values
    # new line values = each point in the line multiplied by m
    # then creates the lines and sets the main lines array to new lines
    #
    # m = multiplier to apply to each coordinate
    def zoom(self, m):
        self.clearcanvas()
        newlines = []
        for line in self.lines:
            x0 = line[0] * m
            y0 = line[1] * m
            x1 = line[2] * m
            y1 = line[3] * m
            newlines.extend([(x0,y0,x1,y1)])
            self.objs.append(self.canvas.create_line(x0, y0, x1, y1))
        self.lines = newlines
        self.recenter()

    # Recenter function
    # resets the snowflake to try and fit to the left of the screen
    def recenter(self):
        smallestx, smallesty = self.window_width, self.window_height
        biggestx, biggesty = 0,0
        centerx = self.window_width/2
        centery = self.window_height/2
        print(centerx, centery)
        for x0, y0, x1, y1 in self.lines:
            if x0 < smallestx:
                smallestx = x0
            if x1 < smallestx:
                smallestx = x1
            if y0 < smallesty:
                smallesty = y0
            if y1 < smallesty:
                smallesty = y1
            if x0 > biggestx:
                biggestx = x0
            if x1 > biggestx:
                biggestx = x1
            if y0 > biggesty:
                biggesty = y0
            if y1 > biggesty:
                biggesty = y1

        self.move_koch((0.5 * (biggestx+smallestx) - centerx),
                       (0.5 * (biggesty+smallesty)) - centery)

    # Function to move the koch in whatever direction is needed.
    # Used to recenter the koch when zoomed and when window is resized.
    def move_koch(self, movementx, movementy):
        self.clearcanvas()
        newlines = []
        for line in self.lines:
            x0 = line[0] - movementx
            y0 = line[1] - movementy
            x1 = line[2] - movementx
            y1 = line[3] - movementy
            newlines.extend([(x0, y0, x1, y1)])
            self.objs.append(self.canvas.create_line(x0, y0, x1, y1))
        self.lines = newlines

    # On drag the koch should move around
    # This function does this by calling the move_koch function
    #
    # lastx and lasty are variables to set the last known x and y coords of
    # the mouse pointer
    def on_drag(self, event):
        if not self.lastx and not self.lasty:
            self.lastx = event.x
            self.lasty = event.y
        else:
            mx, my = 0, 0
            if event.x < self.lastx:
                mx = -10
            if event.x > self.lastx:
                mx = 10
            if event.y < self.lasty:
                my = -10
            if event.y > self.lasty:
                my = 10
            self.move_koch(mx, my)
            self.lastx, self.lasty = event.x, event.y

    # When the window is resized,
    # set the window_height and window_width variables and recenter koch
    def resize(self, event):
        self.window_width, self.window_height = event.width, event.height
        self.recenter()


# Rotate xb, yb by 60 degrees about the origin of xa, ya
#
# This gives xc, yc which is used to make the equilateral triangle
def rotate60(xa, ya, xb, yb):
    sin, cos = math.sin(math.pi / 3), 0.5
    xc = cos*(xb-xa) + sin*(yb-ya) + xa
    yc = cos*(yb-ya) - sin*(xb-xa) + ya
    return xc, yc


# function to find the two points (xa, ya) and (xb,yb) that are a 1/3 and
# 2/3 along the line (x0,y0),(x1,y1)
def findsections(x0,y0,x1,y1):
    xa,ya = (2*x0+x1)/3.0, (2*y0+y1)/3.0
    xb,yb = (x0+2*x1)/3.0, (y0+2*y1)/3.0
    return xa,ya,xb,yb


# Main function to set the x and y values of the window
# Then create the koch class
def main():
    x,y = 1080, 640
    root = tk.Tk()
    root.title("Koch snowflake")
    root.geometry("{}x{}".format(x,y))
    koch = Koch(root, x, y)
    root.mainloop()


if __name__ == '__main__':
    main()
