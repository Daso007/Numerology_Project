# --- UPGRADED NUMEROLOGY CALCULATOR ---

def reduce_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(digit) for digit in str(n))
    return n

def get_birth_chart_digits(birth_date_str):
    day_str, month_str, year_str = birth_date_str.split('/')
    all_digits_str = day_str + month_str + year_str
    birth_chart_digits = [int(digit) for digit in all_digits_str if digit != '0']
    return birth_chart_digits

def calculate_life_path(birth_date_str):
    digits_for_sum = [int(d) for d in birth_date_str if d.isdigit()]
    total_sum = sum(digits_for_sum)
    life_path_number = reduce_number(total_sum)
    return life_path_number

def identify_arrows(birth_date_str):
    digits_in_chart = set(get_birth_chart_digits(birth_date_str))
    ARROWS_OF_STRENGTH = {
        'Arrow of Determination': {1, 5, 9},
        'Arrow of Spirituality': {3, 5, 7},
        'Arrow of the Intellect': {3, 6, 9},
        'Arrow of Emotional Balance': {2, 5, 8},
        'Arrow of Practicality': {1, 4, 7},
        'Arrow of the Planner': {1, 2, 3},
        'Arrow of the Will': {4, 5, 6},
        'Arrow of Activity': {7, 8, 9},
    }
    ARROWS_OF_WEAKNESS = {
        'Arrow of Frustration': {4, 5, 6},
        'Arrow of Hypersensitivity': {2, 5, 8},
        'Arrow of Poor Memory': {3, 6, 9},
        'Arrow of Disorder': {1, 4, 7},
    }
    found_arrows = []
    for name, required_numbers in ARROWS_OF_STRENGTH.items():
        if required_numbers.issubset(digits_in_chart):
            found_arrows.append(name)
    for name, missing_numbers in ARROWS_OF_WEAKNESS.items():
        if not missing_numbers.intersection(digits_in_chart):
            found_arrows.append(name)
    return found_arrows

# --- NEW FUNCTION TO DRAW THE GRID ---
def generate_lo_shu_grid(birth_date_str):
    digits = get_birth_chart_digits(birth_date_str)
    
    # This dictionary maps each number to its fixed position in the Pythagorean grid.
    grid_positions = {
        3: (0, 0), 6: (0, 1), 9: (0, 2),
        2: (1, 0), 5: (1, 1), 8: (1, 2),
        1: (2, 0), 4: (2, 1), 7: (2, 2)
    }
    
    # Create an empty 3x3 grid represented by lists of strings.
    grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    # Place the digits from the birth date into the grid.
    for digit in digits:
        if digit in grid_positions:
            row, col = grid_positions[digit]
            # Append the digit to the string in that cell.
            grid[row][col] += str(digit)
            
    # Format the grid for display.
    grid_str = ""
    grid_str += f" --- --- ---\n"
    grid_str += f"| {grid[0][0]:<2}| {grid[0][1]:<2}| {grid[0][2]:<2}|\n"
    grid_str += f" --- --- ---\n"
    grid_str += f"| {grid[1][0]:<2}| {grid[1][1]:<2}| {grid[1][2]:<2}|\n"
    grid_str += f" --- --- ---\n"
    grid_str += f"| {grid[2][0]:<2}| {grid[2][1]:<2}| {grid[2][2]:<2}|\n"
    grid_str += f" --- --- ---\n"
    
    return grid_str