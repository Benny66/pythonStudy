#coding:utf-8
import turtle
​

def returnInitialPoint(x: int, y: int):
    turtle.up()
    turtle.hideturtle()
    turtle.goto(x, y)
    turtle.showturtle()
    turtle.down()
​
​
def upperHalfHeart(firstDirection: str, parameter: int, rangeParameter: int, direction: str, dParameter: int,
                   forwardParameter: int):
    turtle.left(parameter) if firstDirection == "left" else turtle.right(parameter)
    for i in range(rangeParameter):
        turtle.left(dParameter) if direction == "left" else turtle.right(dParameter)
        turtle.forward(forwardParameter)
​
​
def arrow():
    turtle.speed(1)
    turtle.color('red', 'red')
    turtle.begin_fill()
    turtle.right(50)
    turtle.forward(30)
    turtle.right(130)
    turtle.forward(80)
    turtle.right(135)
    turtle.forward(80)
    turtle.right(135)
    turtle.forward(30)
    turtle.end_fill()
​
​
if __name__ == '__main__':
    name = input('Please enter yourname: ')
    girlFrient = input('Please enter your girlfriend's name: ')
    turtle.setup(width=1920, height=1080)
​
    turtle.color('red', "pink")
    turtle.pensize(5)
    turtle.speed(7)
    returnInitialPoint(0, 200)
    turtle.begin_fill()
    upperHalfHeart("left", 120, 200, "left", 1, 2)
    returnInitialPoint(0, 200)
    upperHalfHeart("left", 100, 200, "right", 1, 2)
    turtle.left(5)
    turtle.forward(243)
    turtle.right(90)
    turtle.forward(243)
    turtle.end_fill()
​
    returnInitialPoint(130, 90)
    turtle.begin_fill()
    upperHalfHeart("right", 30, 100, "left", 2, 2)
    returnInitialPoint(130, 90)
    upperHalfHeart("left", 130, 100, "right", 2, 2)
    turtle.right(10)
    turtle.forward(145)
    turtle.right(90)
    turtle.forward(145)
    turtle.end_fill()
​
    returnInitialPoint(-400, 200)
    turtle.pensize(10)
    turtle.goto(339, - 50)
    arrow()
    returnInitialPoint(0, 150)
    turtle.color('#CD5C5C', 'pink')
    turtle.write(name, font=('gungsuh', 30,), align="center")
    returnInitialPoint(130, 50)
    turtle.write(girlFrient, font=('gungsuh', 30,), align="center")
    window = turtle.Screen()
    window.exitonclick()


