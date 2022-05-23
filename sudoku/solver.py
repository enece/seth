from grid import Grid
from grid import GRID_RANGE


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
    blank_cells = grid.get_blank_cells()
    for blank_cell in blank_cells:
        subgrids_in_bands = blank_cell.get_subgrids_in_bands()
        for subgrid in subgrids_in_bands:
            distinct_possibilities_in_subgrid = set()
            matched_cells = [c for c in blank_cells if c.subgrid == subgrid]
            matched_cells = [c for c in matched_cells if c.row == blank_cell.row or c.column == blank_cell.column]

            for mbc in matched_cells:
                try:
                    distinct_possibilities_in_subgrid.update(mbc.possibilities)
                except TypeError as e:
                    print(mbc.gid)
                    raise e

            if len(distinct_possibilities_in_subgrid) == len(matched_cells):
                blank_cell.remove_possibility(distinct_possibilities_in_subgrid)


def set_values():
    for blank_cell in grid.get_blank_cells():
        if len(blank_cell.possibilities) == 1:
            blank_cell.set_value(val=blank_cell.possibilities.pop())
            update_possibilities()


def set_values_by_inference():
    for f in [grid.get_cells_in_subgrid, grid.get_cells_in_row, grid.get_cells_in_column]:
        for j in GRID_RANGE:
            cells_by_possibility = {k: list() for k in GRID_RANGE}
            cells_in_grid_structure = f(j)
            values_in_grid_structure = [c.value for c in cells_in_grid_structure]
            for val in values_in_grid_structure:
                cells_by_possibility.pop(val, None)

            for cell in [c for c in cells_in_grid_structure if c.possibilities]:
                for p in cell.possibilities:
                    cells_by_possibility[p].append(cell)

            for k, v in cells_by_possibility.items():
                if len(v) == 1:
                    cell = v[0]
                    cell.set_value(k)
                    try:
                        update_possibilities()
                    except AttributeError as e:
                        print(cell.gid)
                        raise e

            cells_by_possibility.clear()


def run_algo():
    update_possibilities()
    set_values()
    # update_possibilities_by_inference()
    set_values_by_inference()


i = 0
while len(grid.get_blank_cells()) > 0:
    i += 1
    run_algo()
    if i == 10000:
        break

print(grid)
