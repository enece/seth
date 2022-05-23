import math
import itertools

from sudoku.sample.grid_data import data as sample_data


GRID_RANGE_OBJECT = range(1, 10)
GRID_RANGE_LIST = list(GRID_RANGE_OBJECT)


class Grid:
    class _InputRow:
        def __init__(self, row_number: int, test_mode: bool):
            self._test_mode = test_mode
            self.row_number = row_number
            self.data = self._make_input_row_data()

        @staticmethod
        def _validation(input_text: str):
            input_cells = list(input_text)

            number_of_cells = len(input_cells)
            if number_of_cells != 9:
                raise ValueError(f'Expected 9 cells, got {number_of_cells}.')

            invalid_input = [i for i in input_cells if not (i.isnumeric() or i.isspace())]
            if invalid_input:
                raise ValueError(f'Invalid input detected.')

            return None

        def _make_input_row_data(self):
            if not self._test_mode:
                input_text = input(f'Enter row for row number {self.row_number}: ')
                self._validation(input_text=input_text)
                raw_input = {k: v for k, v in enumerate(input_text, start=1)}
                input_ = {k: None if v.isspace() else int(v) for k, v in raw_input.items()}
            else:
                input_ = sample_data[self.row_number]

            return input_

    class Cell(object):
        def __init__(self, gid: tuple):
            self.gid = gid
            self.column = gid[0]
            self.row = gid[1]
            self.subgrid = self._get_subgrid()
            self.value = None
            self.possibilities = {i for i in GRID_RANGE_OBJECT}

        def _get_subgrid(self):
            column_band = math.ceil(self.column / 3)
            row_band = math.ceil(self.row / 3)
            return (row_band - 1) * 3 + column_band

        def set_value(self, val: int):
            self.value = val
            if val is not None:
                self.possibilities = None

        def remove_possibility(self, vals: set):
            if self.value:
                raise AttributeError('Cell already set with value; No possibilities to remove')
            self.possibilities = self.possibilities - vals

    class GridMarkup(str):
        def append_first_row(self):
            data = self
            data += '\n\t  '
            for i in GRID_RANGE_OBJECT:
                data += f'   {str(i)}  '
            data += '\n'
            return data

        def append_row_divider(self):
            data = self
            data += '\t  '
            data += '+-----' * 9
            data += '+\n'
            return data

        def append_row_by_row_number(self, row_number: int, cells: list):
            data = self
            data += f'\t{str(row_number)} |'
            for cell in cells:
                data += f"  {str(cell.value or ' ')}  |"
            data += '\n'
            return data

    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        if not self.test_mode:
            self._print_initial_grid_rows_instructions()
        self.initial_grid_rows = dict()
        self.cells = dict()
        self._initialize_cells()
        self._intake_initial_grid_rows()
        self._load_input_to_cells()

    @staticmethod
    def _print_initial_grid_rows_instructions():
        initial_grid_instructions = """
            Enter initial grid one row at a time, with no delimiter between cells. Use a whitespace for blank cells.

            For example, if one grid has the following row:
                +---+---+--+---+---+---+---+--+---+
                | 9 | 1 |  | 7 | 8 | 6 | 2 |  | 4 |
                +---+---+--+---+---+---+---+--+---+
            You would enter "91 7862 4"

            You must make an entry for each row in order, even blank rows, for which you should enter nine whitespaces.
        """
        print(initial_grid_instructions)

    def _intake_initial_grid_rows(self):
        for i in GRID_RANGE_OBJECT:
            while True:
                try:
                    self.initial_grid_rows[i] = self._InputRow(row_number=i, test_mode=self.test_mode)
                    break
                except ValueError as e:
                    print(e)
                    pass

    def _initialize_cells(self):
        grid_structure_range = [i for i in GRID_RANGE_OBJECT]
        cell_range = itertools.product(*[grid_structure_range for i in range(2)])
        for cell in cell_range:
            self.cells[cell] = self.Cell(gid=cell)

    def _load_input_to_cells(self):
        for row_number, input_row in self.initial_grid_rows.items():
            for column_number, input_value in input_row.data.items():
                self.cells[(column_number, row_number)].set_value(val=input_value)

    def get_cells_in_row(self, row_number: int):
        cells_in_row = list()
        for cell in self.cells.values():
            if cell.row == row_number:
                cells_in_row.append(cell)

        return sorted(cells_in_row, key=lambda c: c.column)

    def get_values_in_row(self, row_number: int):
        cells_in_row = self.get_cells_in_row(row_number=row_number)
        all_values_in_row = [cell.value for cell in cells_in_row]

        return [val for val in all_values_in_row if val is not None]

    def get_cells_in_column(self, column_number: int):
        cells_in_column = list()
        for cell in self.cells.values():
            if cell.column == column_number:
                cells_in_column.append(cell)

        return sorted(cells_in_column, key=lambda c: c.row)

    def get_values_in_column(self, column_number: int):
        cells_in_column = self.get_cells_in_column(column_number=column_number)
        all_values_in_column = [cell.value for cell in cells_in_column]

        return [val for val in all_values_in_column if val is not None]

    def get_cells_in_subgrid(self, subgrid_number: int):
        cells_in_subgrid = list()
        for cell in self.cells.values():
            if cell.subgrid == subgrid_number:
                cells_in_subgrid.append(cell)

        return sorted(cells_in_subgrid, key=lambda c: c.row)

    def get_values_in_subgrid(self, subgrid_number: int):
        cells_in_subgrid = self.get_cells_in_subgrid(subgrid_number=subgrid_number)
        all_values_in_subgrid = [cell.value for cell in cells_in_subgrid]

        return [val for val in all_values_in_subgrid if val is not None]

    def get_blank_cells(self):
        return [cell for cell in self.cells.values() if cell.value is None]

    def __repr__(self):
        grid_markup = self.GridMarkup()
        grid_markup = self.GridMarkup(grid_markup.append_first_row())
        grid_markup = self.GridMarkup(grid_markup.append_row_divider())
        for i in GRID_RANGE_OBJECT:
            cells_in_row = self.get_cells_in_row(row_number=i)
            grid_markup = self.GridMarkup(grid_markup.append_row_by_row_number(row_number=i, cells=cells_in_row))
            grid_markup = self.GridMarkup(grid_markup.append_row_divider())
        return grid_markup
