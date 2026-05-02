import turtle


def koch_line(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        new_length = length / 3
        koch_line(t, new_length, depth - 1)
        t.left(60)
        koch_line(t, new_length, depth - 1)
        t.right(120)
        koch_line(t, new_length, depth - 1)
        t.left(60)
        koch_line(t, new_length, depth - 1)


def draw_snowflake():
    screen = turtle.Screen()
    screen.bgcolor("white")

    # Використовуємо графічне вікно для введення числа
    level = screen.numinput("Рівень рекурсії", "Введіть рівень (наприклад, 0-5):", default=3, minval=0, maxval=7)

    # Перевірка, чи користувач не натиснув "Cancel"
    if level is None:
        return

    level = int(level)
    t = turtle.Turtle()
    t.speed(0)

    # Центрування сніжинки
    size = 400
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    t.color("royalblue")
    t.begin_fill()  # Додамо заливку для краси

    for _ in range(3):
        koch_line(t, size, level)
        t.right(120)

    t.end_fill()
    t.hideturtle()
    screen.mainloop()


if __name__ == "__main__":
    draw_snowflake()