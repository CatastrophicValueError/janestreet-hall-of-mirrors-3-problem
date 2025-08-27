'''
This is an interactive recreation of the Jane Street puzzle 'Hall of Mirrors 3' (March 2025).

A description of the puzzle can be found on their website:
    https://www.janestreet.com/puzzles/hall-of-mirrors-3-index/

The interface is farily straightforward to use:
    1) Click any box in the grid to place a mirror.
    2) Click the same box again to change the direction of the mirror.
    3) Click any dot to fire a laser into the grid.
    4) Press 'c' to clear the grid.

Note: Mirrors cannot be placed in orthogonally adjacent cells.

Have fun!
'''

import tkinter as tk

FRAME_WIDTH = 800
BLOCK_SIZE = FRAME_WIDTH/14
DOT_WIDTH = 7

# Clue numbers — taken from the Jane Street Puzzle:
TOP_CLUE_NUMS = [None,None,112,None,48,3087,9,None,None,1]
LEFT_CLUE_NUMS = [None,None,None,27,None,None,None,12,225,None]
RIGHT_CLUE_NUMS = [None,4,27,None,None,None,16,None,None,None]
BOTTOM_CLUE_NUMS = [2025,None,None,12,64,5,None,405,None,None]

def initialise_mirror_index():
    return [['  ' for _ in range(12)] for _ in range(12)]

def initialise_number_dict():
    top_num_dict = dict(zip([(0,j) for j in range(1,11)],[None for _ in range(10)]))
    left_num_dict = dict(zip([(i,0) for i in range(1,11)],[None for _ in range(10)]))
    right_num_dict = dict(zip([(i,11) for i in range(1,11)],[None for _ in range(10)]))
    bottom_num_dict = dict(zip([(11,j) for j in range(1,11)],[None for _ in range(10)]))
    return top_num_dict | left_num_dict | right_num_dict | bottom_num_dict

def initialise_laser_dict():
    dot_indexes = [(i,j) for i in range(12) for j in range(12) if ((i in [0,11]) != (j in [0,11]))]
    return dict(zip(dot_indexes,[None for _ in range(len(dot_indexes))]))

mirror_index = initialise_mirror_index()
number_dict = initialise_number_dict()
laser_dict = initialise_laser_dict()

# These are the nodes on the gridlines that the lasers pass through (horizontal and vertical, respectively)
x_node_map = [[(2*BLOCK_SIZE + BLOCK_SIZE*i, 5*BLOCK_SIZE/2 + BLOCK_SIZE*j) for i in range(11)] for j in range(10)]
y_node_map = [[(5*BLOCK_SIZE/2 + BLOCK_SIZE*i, 2*BLOCK_SIZE + BLOCK_SIZE*j) for i in range(10)] for j in range(11)]


class GridGUI:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=FRAME_WIDTH, height=FRAME_WIDTH)
        self.canvas.pack()
        self.draw_puzzle()


    def draw_puzzle(self):
        self.draw_gridlines()
        self.draw_dots()
        self.draw_clue_nums()


    def draw_gridlines(self):
        for i in range(1,12):
            if i==1 or i==11:
                line_wid = 4
            else:
                line_wid = 1
            self.canvas.create_line(BLOCK_SIZE*(i+1), 2*BLOCK_SIZE, 
                                    BLOCK_SIZE*(i+1), FRAME_WIDTH - 2*BLOCK_SIZE,
                                    width=line_wid)  # vertical
            self.canvas.create_line(2*BLOCK_SIZE - line_wid/2, BLOCK_SIZE*(i+1), 
                                    FRAME_WIDTH - 2*BLOCK_SIZE + line_wid/2, BLOCK_SIZE*(i+1),
                                    width=line_wid)  # horizontal

    def draw_dots(self):
        for i in range(1,11):
            self.canvas.create_oval(5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) - DOT_WIDTH/2, 
                                    3*BLOCK_SIZE/2 - DOT_WIDTH/2, 
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) + DOT_WIDTH/2, 
                                    3*BLOCK_SIZE/2 + DOT_WIDTH/2, 
                                    fill='black')  # top
            self.canvas.create_oval(5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) - DOT_WIDTH/2, 
                                    FRAME_WIDTH - 3*BLOCK_SIZE/2 - DOT_WIDTH/2, 
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) + DOT_WIDTH/2, 
                                    FRAME_WIDTH - 3*BLOCK_SIZE/2 + DOT_WIDTH/2,
                                    fill='black')  # bottom
            self.canvas.create_oval(3*BLOCK_SIZE/2 - DOT_WIDTH/2,
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) - DOT_WIDTH/2,
                                    3*BLOCK_SIZE/2 + DOT_WIDTH/2,
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) + DOT_WIDTH/2,
                                    fill='black')  # left
            self.canvas.create_oval(FRAME_WIDTH - 3*BLOCK_SIZE/2 - DOT_WIDTH/2,
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) - DOT_WIDTH/2, 
                                    FRAME_WIDTH - 3*BLOCK_SIZE/2 + DOT_WIDTH/2,
                                    5*BLOCK_SIZE/2 + BLOCK_SIZE*(i-1) + DOT_WIDTH/2,
                                    fill='black')  # right


    def draw_nums(self):
        """
        Displays the values stored in number_dict next to the dots.
        """
        for n in range(1,11):
            self.canvas.create_text(3*BLOCK_SIZE/2 + BLOCK_SIZE*n, BLOCK_SIZE, 
                                    text=number_dict[(0,n)], anchor='center', tags='dot_number')  # top
            self.canvas.create_text(3*BLOCK_SIZE/2 + BLOCK_SIZE*n, FRAME_WIDTH-BLOCK_SIZE, 
                                    text=number_dict[(11,n)], anchor='center', tags='dot_number')  # bottom
            self.canvas.create_text(BLOCK_SIZE, 3*BLOCK_SIZE/2 + BLOCK_SIZE*n, 
                                    text=number_dict[(n,0)], anchor='e', tags='dot_number')  # left
            self.canvas.create_text(FRAME_WIDTH-BLOCK_SIZE, 3*BLOCK_SIZE/2 + BLOCK_SIZE*n, 
                                    text=number_dict[(n,11)], anchor='w', tags='dot_number')  # right


    def add_upright_mirror(self,i,j):
        self.canvas.create_line(3*BLOCK_SIZE/2 + j*BLOCK_SIZE - BLOCK_SIZE/3, 3*BLOCK_SIZE/2 + i*BLOCK_SIZE - BLOCK_SIZE/3, 
                                3*BLOCK_SIZE/2 + j*BLOCK_SIZE + BLOCK_SIZE/3, 3*BLOCK_SIZE/2 + i*BLOCK_SIZE + BLOCK_SIZE/3, 
                                width=4,tags=f"{i},{j}")
        mirror_index[i][j] = '\\'


    def add_upleft_mirror(self,i,j):
        self.canvas.create_line(3*BLOCK_SIZE/2 + j*BLOCK_SIZE + BLOCK_SIZE/3, 3*BLOCK_SIZE/2 + i*BLOCK_SIZE - BLOCK_SIZE/3, 
                                3*BLOCK_SIZE/2 + j*BLOCK_SIZE - BLOCK_SIZE/3, 3*BLOCK_SIZE/2 + i*BLOCK_SIZE + BLOCK_SIZE/3,
                                width=4, tags=f"{i},{j}")
        mirror_index[i][j] = '/ '


    def clear_screen(self):
        """
        Protocol for clearing screen and indexes.
        """
        global number_dict, mirror_index
        self.canvas.delete("all")
        number_dict = initialise_number_dict()
        mirror_index = initialise_mirror_index()
        self.draw_puzzle()


    def reconfigure_lasers(self):
        global laser_dict
        self.canvas.delete("laser")
        laser_dict = initialise_laser_dict()


    def clear_nums(self):
        global number_dict
        self.canvas.delete('dot_number')
        number_dict = initialise_number_dict()


    def draw_clue_nums(self):
        for n in range(1,11):
                self.canvas.create_text(3*BLOCK_SIZE/2 + BLOCK_SIZE*(n), BLOCK_SIZE/2, 
                                        text=TOP_CLUE_NUMS[n-1], anchor='center', 
                                        fill='red')  # top
                self.canvas.create_text(3*BLOCK_SIZE/2 + BLOCK_SIZE*(n), FRAME_WIDTH - BLOCK_SIZE/2, 
                                        text=BOTTOM_CLUE_NUMS[n-1], anchor='center',
                                        fill='red')  # bottom
                self.canvas.create_text(5 + BLOCK_SIZE/2, 3*BLOCK_SIZE/2 + BLOCK_SIZE*n, 
                                        text=LEFT_CLUE_NUMS[n-1], anchor='e', 
                                        fill='red')  # left
                self.canvas.create_text(FRAME_WIDTH - BLOCK_SIZE/2, 3*BLOCK_SIZE/2 + BLOCK_SIZE*n, 
                                        text=RIGHT_CLUE_NUMS[n-1], anchor='w', 
                                        fill='red')  # right


    def mark_nodes(self):
        """
        Optional function that illustrates all the nodes that a laser step can pass through.
        """
        for i in range(len(x_node_map)):
            for j in range(len(x_node_map[i])):
                self.canvas.create_rectangle(x_node_map[i][j][0] - 2, x_node_map[i][j][1] - 2,
                                             x_node_map[i][j][0] + 2, x_node_map[i][j][1] + 2,
                                             fill='red')
        for i in range(len(y_node_map)):
            for j in range(len(y_node_map[i])):
                self.canvas.create_rectangle(y_node_map[i][j][0] - 2, y_node_map[i][j][1] - 2,
                                             y_node_map[i][j][0] + 2, y_node_map[i][j][1] + 2,
                                             fill='red')
    

class Laser:

    global laser_dict, number_dict

    def __init__(self, i_id, j_id, canvas):
        self.i_id = i_id
        self.j_id = j_id
        self.segments = []
        self.current_segment_length = 0
        self.last_direction = None
        self.current_direction = None
        self.canvas = my_gui.canvas


    def draw_laser(self, i_gmat, j_gmat, direction):
        """
        Draws a single laser unit step on a given node.
        Here 'gmat' means 'greater matrix' — a representation of the grid (dots inclusive) as a 12*12 matrix.
        """
        if direction == 'up':
            node_i = i_gmat-1
            node_j = j_gmat-1
            self.canvas.create_line(y_node_map[node_i][node_j][0], y_node_map[node_i][node_j][1] - BLOCK_SIZE/2,
                                    y_node_map[node_i][node_j][0], y_node_map[node_i][node_j][1] + BLOCK_SIZE/2,
                                    width=2, tags="laser")
        elif direction == 'down':
            node_i = i_gmat
            node_j = j_gmat-1
            self.canvas.create_line(y_node_map[node_i][node_j][0], y_node_map[node_i][node_j][1] - BLOCK_SIZE/2,
                                    y_node_map[node_i][node_j][0], y_node_map[node_i][node_j][1] + BLOCK_SIZE/2,
                                    width=2, tags="laser")
        elif direction == 'left':
            node_i = i_gmat-1
            node_j = j_gmat-1
            self.canvas.create_line(x_node_map[node_i][node_j][0] - BLOCK_SIZE/2, x_node_map[node_i][node_j][1],
                                    x_node_map[node_i][node_j][0] + BLOCK_SIZE/2, x_node_map[node_i][node_j][1],
                                    width=2, tags="laser")
        elif direction == 'right':
            node_i = i_gmat-1
            node_j = j_gmat
            self.canvas.create_line(x_node_map[node_i][node_j][0] - BLOCK_SIZE/2, x_node_map[node_i][node_j][1],
                                    x_node_map[node_i][node_j][0] + BLOCK_SIZE/2, x_node_map[node_i][node_j][1],
                                    width=2, tags="laser")


    def run_laser(self, pos_i, pos_j, direction=None):
        """
        A laser starts at some position (i,j) continuing until it reaches a dot
            returns the final position of the laser
        """
        if not direction:
            if pos_j in range(1,11):
                if pos_i == 0:
                    direction = 'down'
                elif pos_i == 11:
                    direction = 'up'
            elif pos_i in range(1,11):
                if pos_j == 0:
                    direction = 'right'
                elif pos_j == 11:
                    direction = 'left'
        while True:
            self.draw_laser(pos_i,pos_j,direction)

            if self.last_direction!= direction and self.last_direction:
                self.segments.append(self.current_segment_length)
                self.current_segment_length = 0

            if direction == 'right':
                self.last_direction = 'right'
                pos_j += 1
            elif direction == 'left':
                self.last_direction = 'left'
                pos_j -= 1
            elif direction == 'up':
                self.last_direction = 'up'
                pos_i -= 1
            elif direction == 'down':
                self.last_direction = 'down'
                pos_i += 1

            self.current_segment_length += 1

            if (pos_i,pos_j) in number_dict:
                self.segments.append(self.current_segment_length)
                return pos_i, pos_j

            if mirror_index[pos_i][pos_j] == '/ ':
                direction_map = {'right': 'up',
                                 'down': 'left',
                                 'up': 'right',
                                 'left': 'down'}
                self.last_direction = direction
                return self.run_laser(pos_i, pos_j, direction_map[direction])
            
            if mirror_index[pos_i][pos_j] == '\\':
                direction_map = {'right': 'down',
                                 'down': 'right',
                                 'up': 'left',
                                 'left': 'up'}
                self.last_direction = direction
                return self.run_laser(pos_i, pos_j, direction_map[direction])

            self.last_direction = direction        


    def transmit_number(self):
        '''
        This function carries out all the functionality of the laser:
            - Traces the laser's path
            - Calculates the product of the segment lengths for the Laser object
            - Stores the result in the number_dict for both ends of the laser
        '''
        exit_pos = None
        if self.j_id == 0:
            exit_pos = self.run_laser(self.i_id, self.j_id, 'right')
        elif self.j_id == 11:
            exit_pos = self.run_laser(self.i_id, self.j_id, 'left')
        elif self.i_id == 0:
            exit_pos = self.run_laser(self.i_id, self.j_id, 'down')
        elif self.i_id == 11:
            exit_pos = self.run_laser(self.i_id, self.j_id, 'up')

        if exit_pos:
            i, j = exit_pos
            result = 1
            for segment in self.segments:
                result *= segment

            number_dict[(i, j)] = result
            number_dict[(self.i_id,self.j_id)] = result
            #print(f"Laser traveled with segment lengths {self.segments}. Number {result} assigned to dot at ({i}, {j})")
              

root = tk.Tk()
root.title("Hall of mirrors 3 (press c to clear)")
my_gui = GridGUI(root)
my_gui.draw_clue_nums()


# Solution for Jane Street problem:
'''
mirror_index = [['xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx'],
                ['xx', '  ', '  ', '\\', '  ', '  ', '  ', '\\', '  ', '  ', '\\', 'xx'], 
                ['xx', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '\\', '  ', 'xx'], 
                ['xx', '/ ', '  ', '  ', '  ', '/ ', '  ', '  ', '/ ', '  ', '  ', 'xx'], 
                ['xx', '  ', '  ', '/ ', '  ', '  ', '  ', '  ', '  ', '  ', '\\', 'xx'], 
                ['xx', '  ', '  ', '  ', '  ', '  ', '  ', '/ ', '  ', '  ', '  ', 'xx'], 
                ['xx', '  ', '/ ', '  ', '  ', '\\', '  ', '  ', '\\', '  ', '  ', 'xx'], 
                ['xx', '/ ', '  ', '\\', '  ', '  ', '/ ', '  ', '  ', '/ ', '  ', 'xx'], 
                ['xx', '  ', '  ', '  ', '\\', '  ', '  ', '  ', '  ', '  ', '  ', 'xx'], 
                ['xx', '  ', '  ', '  ', '  ', '/ ', '  ', '/ ', '  ', '/ ', '  ', 'xx'], 
                ['xx', '/ ', '  ', '  ', '  ', '  ', '/ ', '  ', '  ', '  ', '  ', 'xx'], 
                ['xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx', 'xx']]
'''

def has_no_neighbours(i,j):
    allowed = {'  ', 'xx'}
    neighbours = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    return all(mirror_index[x][y] in allowed for x, y in neighbours)


def on_click(event):
    for i in range(len(mirror_index)):
        for j in range(len(mirror_index[0])):
            if mirror_index[i][j] == '\\':
                my_gui.add_upright_mirror(i,j)
            elif mirror_index[i][j] == '/ ':
                my_gui.add_upleft_mirror(i,j)

    x,y = event.x//BLOCK_SIZE, event.y//BLOCK_SIZE
    i = int(y)-1
    j = int(x)-1

    if (i,j) in laser_dict.keys():
        if laser_dict[(i,j)] is None:
            laser_dict[(i,j)] = Laser(i,j,my_gui.canvas)
            laser_dict[(i,j)].transmit_number()
            my_gui.draw_nums()
        else:
            my_gui.reconfigure_lasers()
            my_gui.clear_nums()
        
    if (2<=x<12) and (2<=y<12):
        my_gui.reconfigure_lasers()
        my_gui.clear_nums()

        if has_no_neighbours(i,j):
            if mirror_index[i][j] == '  ':
                my_gui.add_upright_mirror(i,j)
                mirror_index[i][j] = '\\'
            elif mirror_index[i][j] == '\\':
                my_gui.canvas.delete(f'{i},{j}')
                my_gui.add_upleft_mirror(i,j)
                mirror_index[i][j] = "/ "
            elif mirror_index[i][j] == '/ ':
                my_gui.canvas.delete(f'{i},{j}')
                mirror_index[i][j] = "  "
                my_gui.reconfigure_lasers()

# Key bindings
my_gui.canvas.bind("<Button-1>",on_click)
root.bind("<c>", lambda event : my_gui.clear_screen())

# Fills the screen with the initial mirrors
for i in range(len(mirror_index)):
    for j in range(len(mirror_index[0])):
        if mirror_index[i][j] == '\\':
            my_gui.add_upright_mirror(i,j)
        elif mirror_index[i][j] == '/ ':
            my_gui.add_upleft_mirror(i,j)

root.mainloop()
