import random
import os
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]



def main():
    while 0 == 0:
        generate_ran()
        print_results()
        direction_input = input() 
        direction(direction_input)
        print_results()



# Add random numbers to grid if it is empty
# number to choose from
def generate_ran():
    count = random.randint(1,2)
    while count != 0:
        num_list = [2, 4]
        x = random.randint(0,3)
        y = random.randint(0,3)
        v = random.choice(num_list)
        # Get the current value of the X- Y 
        value_point = grid[x][y]
        if value_point == 0:
            grid[x][y] = v
            count -= 1
    print(grid)

def print_results():
    os.system('cls')
    for row in grid:
        print(row)


# If flip is true it will slide left.
def slide_left(flip):
    for index, row in enumerate(grid):
        # if flip is true it will reverse the whole grid
        if flip:
            grid[index] == row.reverse()
        # Creates temp row to set values added to
        temp_row = []
        # Removes the 0's
        grid[index] = [x for x in row if x != 0]
        # test to see if its only one value in a row
        # if so just add that to the test list and dont
        # attempt to add later
        more_than_one = True
        if len(grid[index]) == 1:
            more_than_one = False
            temp_row.append(grid[index][0])
        # get the length minus on for indexing
        for i in range(len(grid[index])-1):
            #if values match add them and append to row and set the last value to 0 so it doesnt get added twice
            if grid[index][i] == grid[index][i+1] and more_than_one:
                # append the added valeus
                temp_row.append(grid[index][i] + grid[index][i+1])
                # set that second value to 0 so it wont add on its iteration
                grid[index][i+1] = 0
            # if a value does not equal then append
            elif grid[index][i] != 0:
                temp_row.append(grid[index][i])
            # on the last one if the value 3 is equal to last then append added
            # else append last value
            if i == (len(grid[index])-2):
                if grid[index][i] == grid[index][i+1] and more_than_one:
                    temp_row.append(grid[index][i] + grid[index][i+1])
                else:
                    temp_row.append(grid[index][i+1])
        # add back the zeros 
        while len(temp_row) != 4:
            temp_row.append(0)
        # Reverse temp row back
        # if the list is flipped when attempting to add to another list it will
        # Cause a memory issue
        if flip:
            temp_row.reverse()
        grid[index] = temp_row


def rotate(time):
    global grid
    for x in range(time):
        temp_grid = [[],[],[],[]]
        for colum in range(0,4):
            for row in range(0,4):
                temp_grid[colum].append(grid[row][colum])
        temp_grid.reverse()
        grid = temp_grid

def rotate_back(time):
    global grid
    for x in range(time):
        temp_grid = [[],[],[],[]]
        for colum in range(3,-1,-1):
            for row in range(3,-1,-1):
                temp_grid[colum].append(grid[row][colum])
        temp_grid
        grid = temp_grid



def direction(input_value):
    if input_value == "a":
        slide_left(False)
    elif input_value == "d":
        slide_left(True)
    elif input_value == "w":
        rotate(1)
        slide_left(False)
        rotate(3)
    elif input_value == "s":
        rotate(3)
        slide_left(False)
        rotate(1)
main()
