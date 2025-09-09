from graphics import Canvas
import random
import time

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
NUM_FISH = 5
NUM_COINS = 10
INITIAL_LIVES = 5
GAME_DURATION = 15  # Game duration in seconds

def main():
    water_img = "waterline.png"
    image_path = "diver2.png" #"scuba-diver-hi.png"
    fish_img = "fish.png"
    boat_img = "boat.png"
    coin_img = "coin.png"
    game_over_img = "GameOver.png"

    # Initialize lives
    lives = INITIAL_LIVES
    lives_display = None
    pts = 0
    # Initially no boat
    boat = None
    
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.focus_set()
    
    diver_width, diver_height = 98, 48  # Preset width and height of your diver
    diver = canvas.create_image_with_size(0, CANVAS_HEIGHT // 2, diver_width, diver_height, image_path)
    waterline_dist = 0

    for i in range(6):
        water = canvas.create_image_with_size(0+waterline_dist,30,100,100,water_img)
        waterline_dist +=75    
    
    print("Diver ID:", diver)

    def display_lives():
        nonlocal lives_display
        if lives_display is not None:
            canvas.delete(lives_display)
        hearts_text = "Lives: " + "♥ " * lives
        lives_display = canvas.create_text(10, 10, text=hearts_text, anchor="nw", font=("Arial", 16))

    display_lives()

    start_time = time.time()
    
    # Create a list to hold each object and their speeds
    objects = []
    obj_spacing = 100  # Adjust this value for more spacing

     # Adding fish
    for i in range(NUM_FISH):
        x = CANVAS_WIDTH + i * obj_spacing # Spread out initial positions
        y = random.randint(160, CANVAS_HEIGHT - 80)  # Random y-position for fish
        fish = canvas.create_image_with_size(x-20,y-20, 50,50, fish_img) 
        speed = random.uniform(0.20, 0.60)
        objects.append((fish, speed, 'fish'))

    # Adding coins
    for i in range(NUM_COINS):
        x = CANVAS_WIDTH + i * obj_spacing
        y = random.randint(200, CANVAS_HEIGHT - 20)  # Random y-position for coin
        coin = canvas.create_image_with_size(x, y,  25,25, coin_img)  
        speed = random.uniform(0.40, 0.60)
        objects.append((coin, speed, 'coin'))
    
    # Main game loop
    while True:
        elapsed_time = time.time() - start_time
        #print(f"Elapsed Time: {elapsed_time:.1f} seconds")
        # Add the boat after >GAME DURATION
        if elapsed_time >= GAME_DURATION:
            print(f"Elapsed Time Reached: {elapsed_time:.1f} seconds - Creating Boat")
        if boat is None:
            boat = canvas.create_image_with_size(CANVAS_WIDTH - 100, 20, 100, 60, boat_img)

        if boat is not None and check_collision(canvas, diver, [(boat, 0, 'boat')]):
            # Recreate diver to bring it to the front
            diver_x = canvas.get_left_x(diver)
            diver_y = canvas.get_top_y(diver)
            canvas.delete(diver)  # Remove the current diver
            # Recreate the diver at the same position
            diver = canvas.create_image_with_size(diver_x, diver_y, diver_width, diver_height, image_path)
            print("Congrats! Game over")
            print(f"points: {pts}") 

            canvas.create_image_with_size(100, 160, 200, 80, game_over_img) 
            canvas.create_text(130, 180, text=f"Congratulations!", anchor="nw", font=("Arial", 16), color='black')
            canvas.create_text(130, 200, text=f"Total Points: {pts}", anchor="nw", font=("Arial", 16), color='black')
        
            # Force the canvas to update and display the congratulations
            canvas.update()
            
            # Keep the window open - wait for a click or key press
            print("Click anywhere or press any key to close...")
            canvas.wait_for_click()  # This will keep the window open until clicked
    
            break  # Exit the loop and freeze the frame

        ########MOVING FISH################
        # Move each object (fish, coin) across the canvas
        for obj, speed, obj_type in objects:
            # Move the object left by its speed
            canvas.move(obj, -speed, 0)

            # Get the current position of the object
            current_x = canvas.get_left_x(obj)

            # Reset object to the right edge if it's off the left side
            if current_x + canvas.get_object_width(obj) < 0:
                # Randomize the new vertical position within canvas boundaries
                y = random.randint(160, CANVAS_HEIGHT - 60)
                canvas.moveto(obj, CANVAS_WIDTH, y)        
        
       
        # Detect collisions
        collision_detected = False
        collision_result = check_collision(canvas, diver, objects)
        
        if collision_result:
            obj, obj_type = collision_result
            print(f"Collision with {obj_type} detected!")
            if obj_type == 'fish':
                # Decrease life only once per detection
                if lives > 0:
                    lives -= 1
                    print(f"Collision with fish detected! Lives remaining: {lives}")
                    display_lives() 
                    flash_and_remove(canvas, objects, obj) 
                    #flash_and_remove_fish(canvas, objects, obj) 
            elif obj_type == 'coin':
                # Handle coin collision, e.g., increase score
                flash_and_remove(canvas, objects, obj) 
                pts +=10
                print("collected coin", pts)

            if lives == 0:
                print("Game Over! No lives left!")
                canvas.create_image_with_size(100,160,200,80, game_over_img) 
                canvas.create_text(160, 185, text=f"Game Over!", font=("Arial", 16), color='black')        
                canvas.create_text(160, 205, text=f"No lives left!", font=("Arial", 16), color='black')
                break
        # else:
        #     print("No collision detected.")

        #KEY PRESS
        # Check for new key presses
        key_presses = canvas.get_new_key_presses()
        
        # Move rectangle based on key press
        #for key in key_presses:
        for key_event in key_presses:
            key = key_event.keysym

            # Get current position of the diver
            diver_x = canvas.get_left_x(diver)
            diver_y = canvas.get_top_y(diver)
            diver_width = canvas.get_object_width(diver)
            diver_height = canvas.get_object_height(diver)
            
            #print("Key pressed:", key)
            if key == 'Left':
                # Check if moving left keeps within the canvas
                if diver_x - 50 >= 0:
                    canvas.move(diver, -50, 0)
            elif key == 'Right':
                 # Check if moving right keeps within the canvas
                if diver_x + diver_width + 50 <= CANVAS_WIDTH:
                    canvas.move(diver, 50, 0)
            elif key == 'Up':
                # Check if moving up keeps within the canvas
                if diver_y - 50 >= 0:
                    canvas.move(diver, 0, -50)
            elif key == 'Down':
                # Check if moving down keeps within the canvas
                if diver_y + diver_height + 50 <= CANVAS_HEIGHT:
                    canvas.move(diver, 0, 50)    
        
        canvas.sleep(0.005)

def check_collision(canvas, diver, objects, padding=5):
    diver_x = canvas.get_left_x(diver)
    diver_y = canvas.get_top_y(diver)
    diver_width = canvas.get_object_width(diver)
    diver_height = canvas.get_object_height(diver)

    if diver_x is None or diver_y is None or diver_width is None or diver_height is None:
        return False

    for obj, speed, obj_type in objects:
        obj_x = canvas.get_left_x(obj)
        obj_y = canvas.get_top_y(obj)
        obj_width = canvas.get_object_width(obj)
        obj_height = canvas.get_object_height(obj)

        if obj_x is None or obj_y is None or obj_width is None or obj_height is None:
            continue

        # Apply collision detection with padding for sensitivity
        if (diver_x < obj_x + obj_width + padding and
            diver_x + diver_width + padding > obj_x and
            diver_y < obj_y + obj_height + padding and
            diver_y + diver_height + padding > obj_y):
            return obj, obj_type  # Return object and type if there's a collision
        
    return None  # Return None if no collision detected

def flash_and_remove(canvas, objects, obj):
    """
    Flashes the specified object and then removes it from the canvas and the objects list.

    Args:
    - canvas: The canvas instance to manipulate objects.
    - objects: List of all objects in the game.
    - obj: The object ID to flash and remove.
    """
    # Flash effect
    # flashes = 1
    # for _ in range(flashes):
    #     canvas.set_hidden(obj, True)
    #     canvas.sleep(0.5)
    #     canvas.set_hidden(obj, False)
    #     canvas.sleep(0.5)
    
    # Remove fish from canvas and list
    canvas.delete(obj)
    # Update the objects list after object removal
    objects[:] = [entry for entry in objects if entry[0] != obj]
   
if __name__ == '__main__':
    main()