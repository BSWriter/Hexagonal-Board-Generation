import pygame
import sys
import math
from GenClasses import Board
import json

BOARD_NAME = input("Enter name of board: ")
num_rows = int(input("Enter the number of rows: "))
num_cols = int(input("Enter the number of columns: "))
panel_size = int(input("Enter the size of panels (avg. size is 25): "))
enableWalls = int(input("Have the board surrounded by walls (No->0, Yes->1): "))

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(str(BOARD_NAME))

# Set up colors
# General colors
GRID_COLOR = (50, 50, 50)
LABEL_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Panel colors
VOID = BLACK
DIRT = (204, 102, 0)
STONE = (50, 50, 50)
GRASS = (0, 100, 0) 
WALL = (102, 61, 0)

panelColors = [VOID, DIRT, STONE, GRASS, WALL]
panelOffsetX = panel_size * 2
panelOffsetY = panel_size * 2
surroundingTiles = []
chosenLabel = 0
numberFont = pygame.font.Font(None, 20)

# Define the button properties
sButton_width, sButton_height = 200, 50
sButton_x, sButton_y = (screen_width - sButton_width) // 2, (screen_height - sButton_height) - 50
sButton_color = WHITE
sButton_text = "Save Board"

# Set up the grid (Board)
board = Board(int(num_rows), int(num_cols), 2, enableWalls)
hashBoard = {}
for panel in board.getPanels():
    hashBoard[panel.gridPos] = panel

# Set up the font
font_size = 20
font = pygame.font.Font(None, font_size)

# Set up the game loop
running = True


def saveBoard():
    # Convert modified hashBoard data into the original board data
    conversionPanels = []
    for pos, panel in hashBoard.items():    
        conversionPanels.append(panel)
    board.setPanels(conversionPanels)

    board_data = board.getDict()

    # Specify the file path for save data
    file_path = str(BOARD_NAME) + ".json"

    # Write the dictionary to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(board_data, json_file)
    mouse_pos = (-1, -1)


while running:
    
    mouse_pos = (-1, -1)
    numKeyDown = None
    upArrowKey = False
    downArrowKey = False
    
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Upward scroll (Zoom in on board)
                panel_size += 5 if panel_size < 50 else 0
            elif event.button == 5:  # Downward scroll (Zoom out)
                panel_size -= 5 if panel_size > 5 else 0
            else:
                # Get the position of the mouse click
                mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            # Pressing the arrow keys change the elevation of the tile
            if event.key == pygame.K_UP:
                upArrowKey = True
                # Get the position of the mouse hover
                mouse_pos = pygame.mouse.get_pos()
            elif event.key == pygame.K_DOWN:
                downArrowKey = True
                # Get the position of the mouse hover
                mouse_pos = pygame.mouse.get_pos()
            # Check if the key pressed is a number
            elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                # Get the number from the key code
                numKeyDown = event.key - pygame.K_0
                mouse_pos = pygame.mouse.get_pos()
            # WASD presses allow user to look around board
            elif event.key == pygame.K_w:
                panelOffsetY += 10
            elif event.key == pygame.K_s:
                panelOffsetY -= 10
            elif event.key == pygame.K_a:
                panelOffsetX += 10
            elif event.key == pygame.K_d:
                panelOffsetX -= 10
            

            


    # Fill the background with black
    screen.fill(BLACK)

        
    # Draw Hexagon Grid
    for pos, panel in hashBoard.items():
        panelCoord = [(x * panel_size + panelOffsetX, y * panel_size + panelOffsetY) for x, y in panel.getCoordinates()]
        if pos in surroundingTiles:
            currPanel = pygame.draw.polygon(screen, panelColors[-1], panelCoord)
            panel.setLabel(chosenLabel, len(panelColors)-1)  
            # Remove pos from surroundingTIles
            surroundingTiles.remove(pos)
        else:
            currPanel = pygame.draw.polygon(screen, panelColors[panel.label], panelCoord)

        # If the mouse click is inside the hexagon, update the label
        if currPanel.collidepoint(mouse_pos):
            # If the user presses an arrow key, increment or decrement the elevation
            if upArrowKey:
                panel.incrementElevation()
            elif downArrowKey:
                panel.decrementElevation()
            # If the user pressed a number key, change tile and surrounding tiles to corresponding type
            elif numKeyDown and len(surroundingTiles) == 0:
                surroundingTiles = [pos] + panel.getSurroundingPanels()
                chosenLabel = numKeyDown - 1
            else:
                panel.setLabel(panel.label + 1, len(panelColors)-1)


        # Draw elevation labels for each tile
        # Render the number as text
        number = panel.getElevation()
        position = (panel.getCenter()[0] * panel_size + panelOffsetX - (panel_size/4), panel.getCenter()[1] * panel_size + panelOffsetY - (panel_size/4))

        number_text = numberFont.render(str(number), True, WHITE)

        # Blit the number onto the screen surface at the specified position
        screen.blit(number_text, position)

    # ----------------------- Board Save Button -------------------------------- 
    # Draw the save button
    saveButton = pygame.draw.rect(screen, sButton_color, (sButton_x, sButton_y, 
                                                sButton_width, sButton_height))

    # Draw the save button text
    saveButtonFont = pygame.font.Font(None, 36)
    saveButtonText = font.render(sButton_text, True, BLACK)
    buttonTextRect = saveButtonText.get_rect(center=(sButton_x + sButton_width // 2, sButton_y + sButton_height // 2))
    screen.blit(saveButtonText, buttonTextRect)

    if saveButton.collidepoint(mouse_pos):
        saveBoard()
        print("Saved Board!")
            

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
