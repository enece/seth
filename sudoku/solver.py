from grid import Grid


grid = Grid()
print(grid)


def update_possibilities():
    for blank_cell in grid.get_blank_cells():
        values_to_remove = set()
        values_to_remove.update(grid.get_values_in_row(row_number=blank_cell.row))
        values_to_remove.update(grid.get_values_in_column(column_number=blank_cell.column))
        values_to_remove.update(grid.get_values_in_subgrid(subgrid_number=blank_cell.subgrid))

        blank_cell.remove_possibility(vals=values_to_remove)


def update_possibilities_by_inference():
    pass


def set_values():
    for blank_cell in grid.get_blank_cells():
        if len(blank_cell.possibilities) == 1:
            blank_cell.set_value(val=blank_cell.possibilities.pop())


def run_algo():
    update_possibilities()
    set_values()


i = 0
while len(grid.get_blank_cells()) > 0:
    i += 1
    run_algo()
    if i == 100:
        break

print(grid)
