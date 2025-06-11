import turtle
def createLSystems(iterations, axiom):
    startString = axiom
    endString = ""
    for i in range(iterations):
        endString = processString(startString)
        startString = endString
    return endString
def processString(oldStr):

    newstr = ""
    for ch in oldStr:
        newstr = newstr + applyrules(ch)
    return newstr

def applyrules(ch):

    newstr = ""
    if ch == "F":
        newstr = 'FF[+F-F]FF[-F+F]FF'
    else:
        newstr = ch 

    return newstr

def drawLSystems(turtle,instructions,angle,size):
    stack=[]
    for cmd in instructions:
        if cmd == 'F':
            turtle.forward(size)
        if cmd == '+':
            turtle.left(angle)
        if cmd == '-':
            turtle.right(angle)
        if cmd == '[':
            stack.append((turtle.position(), turtle.heading()))
        if cmd == ']':
            position, heading = stack.pop()
            turtle.penup()
            turtle.goto(position)
            turtle.setheading(heading)
            turtle.pendown()
            
def main():
 gen=int(input("Number between 1 and 3: ")) #gen is the number of the generation
 nrF=10**gen
 nrF_str=str(nrF)
 nrS=2*((10**gen-1)/9)
 nrS_str=str(nrS)
 print("Number of F's: "+nrF_str)
 print("Number of +, -, ] and [: "+nrS_str)
 turtle.setworldcoordinates(-400, 0, 400, 600) #this line sets the point P(0,0) to the bottom of the turtle screen
 t = turtle.Turtle('turtle')
 screen = turtle.Screen()
 canvas = screen.getcanvas()
 root = canvas.winfo_toplevel()
 root.attributes('-topmost', True)
 screen.bgcolor('white')
 t.speed(0)
 t.width(2)
 t.color('green')
 inst = createLSystems(gen,"F")
 t.penup()
 t.setposition(x=0, y=0)
 t.pendown()
 t.left(90)
 unit=23
 drawLSystems(t, inst, 90, unit)
 print("Height of the cactus: "+str(t.ycor()/unit))
 t.hideturtle()
 turtle.done()
 print(inst)
main()