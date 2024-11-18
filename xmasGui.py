import random
import pygame
import tkinter as tk

number_of_snowflakes = 50
number_of_presents = 3
tree_color = "green"
list_colors = ["green", "pink", "lightgreen", "darkgreen"]
present_coords = [(0,0) for _ in range(number_of_presents)]
present_colors = ["" for _ in range(number_of_presents)]

def create_snowflakes(canvas, num_snowflakes):
    """Creates initial positions for snowflakes."""
    snowflakes = []
    for _ in range(num_snowflakes):
        x = random.randint(0, 400)
        y = random.randint(0, 400)
        snowflakes.append(canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="white", outline="white"))
    return snowflakes

def animate_snow(canvas, snowflakes):
    """Animates the falling snowflakes."""
    for snowflake in snowflakes:
        # Move each snowflake downward
        canvas.move(snowflake, 0, random.uniform(1, 3))  # Falling speed

        # Get the current coordinates of the snowflake
        coords = canvas.coords(snowflake)
        if len(coords) == 4:  # Ensure we have valid coordinates
            x1, y1, x2, y2 = coords
            # If the snowflake has moved beyond the bottom of the canvas
            if y1 > 400:
                # Reset the snowflake to the top with a random x position and proper size
                new_x = random.randint(0, 400)
                new_y = 0
                canvas.coords(snowflake, new_x - 3, new_y - 3, new_x + 3, new_y + 3)  # Set as a small circle
    # Schedule the next frame of animation
    canvas.after(50, animate_snow, canvas, snowflakes)


def blink_star(canvas, star_id):
    """Makes the star blink by toggling its visibility."""
    current_fill = canvas.itemcget(star_id[0], "fill")
    new_fill = "yellow" if current_fill == "black" else "black"
    canvas.itemconfig(star_id[0], fill=new_fill)

    # Schedule the next blink
    canvas.after(500, blink_star, canvas, star_id)

def on_tree_click(event, canvas, x, y, star_id):
    global tree_color
    """Changes the tree color when clicked."""
    tree_color = random.choice(list_colors)

def draw_christmas_tree(canvas, x, y, star_id):
    global tree_color
    canvas.delete("tree")
    # Draw the tree layers (triangles)
    canvas.create_polygon(x, y+100, x-100, y+200, x+100, y+200, fill=tree_color, outline="black", tags="tree")  # Bottom layer
    canvas.create_polygon(x, y+50, x-80, y+150, x+80, y+150, fill=tree_color, outline="black", tags="tree")  # Middle layer
    canvas.create_polygon(x, y, x-60, y+100, x+60, y+100, fill=tree_color, outline="black", tags="tree")  # Top layer

    # Add a trunk
    canvas.create_rectangle(x-15, y+200, x+15, y+250, fill="brown", outline="black", tags="tree")

    # Draw colorful "lights" (circles) at random positions within the tree triangles
    colors = ["red", "blue", "yellow", "white", "pink", "purple"]
    for _ in range(20):  # Add 20 lights
        rn = random.randint(1,3)
        if rn == 1:
            if random.randint(1,2) == 1:
                light_y = random.randint(y + 20, y + 40)
                light_x = random.randint(x - 10, x + 10)
            else:
                light_y = random.randint(y + 30, y + 60)
                light_x = random.randint(x - 20, x + 10)
        elif rn == 2:
            light_x = random.randint(x - 40, x + 40)
            light_y = random.randint(y+100, y + 150)
        else:
            light_x = random.randint(x - 60, x + 60)
            light_y = random.randint(y+130, y + 200)

        # decorations
        canvas.create_oval(light_x - 5, light_y - 5, light_x + 5, light_y + 5, fill=random.choice(colors), outline="black", tags="tree")

    for p in range(number_of_presents):
        if present_coords[p] == (0,0):
            present_x = x - random.randint(-50, 100)
            present_y = y + random.randint(200, 225)
            present_coords[p] = (present_x, present_y)
        else:
            present_x, present_y = present_coords[p]

        if present_colors[p] == "":
            colors = ["red", "pink", "blue"]
            present_colors[p] = random.choice(colors)

        canvas.create_rectangle(present_x, present_y, present_x + 60, present_y + 40, fill=present_colors[p],
                                outline="black")  # Present box
        canvas.create_line(present_x + 30, present_y, present_x + 30, present_y + 40, fill="gold",
                           width=2)  # Vertical ribbon
        canvas.create_line(present_x, present_y + 20, present_x + 60, present_y + 20, fill="gold",
                           width=2)  # Horizontal ribbon

    # Draw a star at the top of the tree
    # Coordinates for a 5-pointed star
    star_x = x
    star_y = y - 12  # Just above the top of the tree
    star_coords = [
        (star_x, star_y - 15),  # Top point
        (star_x + 5, star_y - 5),  # Upper right
        (star_x + 15, star_y - 5),  # Right point
        (star_x + 7, star_y + 5),  # Lower right
        (star_x + 10, star_y + 15),  # Bottom right
        (star_x, star_y + 10),  # Bottom point
        (star_x - 10, star_y + 15),  # Bottom left
        (star_x - 7, star_y + 5),  # Lower left
        (star_x - 15, star_y - 5),  # Left point
        (star_x - 5, star_y - 5)  # Upper left
    ]
    star_id[0] = canvas.create_polygon(star_coords, fill="yellow", outline="black", tags="tree")

    # Schedule the next redraw after 2 seconds (2000 milliseconds)
    canvas.after(800, draw_christmas_tree, canvas, x, y, star_id)
def main():

    #DJ part
    pygame.mixer.init()
    pygame.mixer.music.load("SantaClausIsComingToTownKaraoke.mp3")  # Load your background music file
    pygame.mixer.music.play(-1, 0.0)  # Play music looped indefinitely

    # Create the main window
    root = tk.Tk()
    root.title("X-MAS Tree")

    # Create a Canvas widget
    canvas = tk.Canvas(root, width=400, height=400, bg="black")
    canvas.pack()

    # Create snowflakes
    snowflakes = create_snowflakes(canvas, number_of_snowflakes)  # Create 50 snowflakes

    # Start animating snowflakes
    animate_snow(canvas, snowflakes)

    star_id = [None]  # This will store the star's ID

    # Draw the initial Christmas tree and start the redraw loop
    draw_christmas_tree(canvas, 200, 50, star_id)

    # Start blinking the star
    blink_star(canvas, star_id)

    canvas.bind("<Button-1>", lambda event: on_tree_click(event, canvas, 200, 50, star_id))

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
