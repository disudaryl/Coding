import turtle
import math

screen = turtle.Screen()
screen.bgcolor("black")

i = turtle.Turtle()

i.speed(1)
i.hideturtle()
i.penup()
i.color("#ffb6c1")

for scale in range(11, 17):
    for t in range(120):
        angle = t * (math.pi * 2) / 120

        x = 16 * (math.sin(angle) ** 3) * scale

        y = (13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * 
        angle) - math.cos(4 * angle)) * scale

        i.goto(x, y)
        i.write("I love you",
                align="center", font=("Arial", 8,
                "bold"))

turtle.done