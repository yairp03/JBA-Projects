from math import floor

MAIN = 0

EXIT = 0
ADD = 1
MUL_BY_CONST = 2
MUL_MATRICES = 3
TRANSPOSE = 4
DETERMINANT = 5
INVERSE = 6

MAIN_DIAGONAL = 1
SIDE_DIAGONAL = 2
VERTICAL_LINE = 3
HORIZONTAL_LINE = 4


class Matrix:

    def __init__(self, rows_count=1, columns_count=1, data=None):
        """
        :type rows_count: int
        :type columns_count: int
        """
        self._rows_count = rows_count
        self._columns_count = columns_count
        if data:
            self._data = data
        else:
            self._data = [[0.0] * self._columns_count for _ in range(self._rows_count)]

    def get_rows_count(self):
        """
        Returns rows count
        :return: rows count
        :rtype: int
        """
        return self._rows_count

    def get_columns_count(self):
        """
        Returns columns count
        :return: columns count
        :rtype: int
        """
        return self._columns_count

    def get_size(self):
        """
        Returns size of matrix
        :return: size of matrix
        :rtype: tuple
        """
        return self._rows_count, self._columns_count

    def update_row(self, row_index, new_row):
        """
        Updates matrix with a new row
        :param row_index: Index of the row to update
        :param new_row: new row to update with
        :type row_index: int
        :type new_row: list
        :raise MatrixSizeException: When row_index is illegal or when new_row length is illegal
        :return: None
        """
        if row_index >= self._rows_count or len(new_row) != self._columns_count:
            raise MatrixException("Invalid size")
        self.get_data()[row_index] = list(new_row)

    @staticmethod
    def input_matrix(size):
        """
        Inputs matrix from keyboard
        :return: inputted matrix
        :rtype: Matrix
        """
        mat = Matrix(*size)
        for r in range(mat.get_rows_count()):
            mat.update_row(r, list(map(float, input().split())))
        return mat

    def get_data(self):
        """
        returns the matrix data
        :return: the matrix data
        :rtype: list
        """
        return self._data

    def __getitem__(self, item):
        """
        Returns a row from the matrix
        :param item: row index
        :type item: int
        :return: row from matrix
        :rtype: list
        """
        return self.get_data()[item]

    def __add__(self, other):
        """
        Adds 2 matrices
        :param other: other matrix
        :type other: Matrix
        :return: Result matrix
        :rtype: Matrix
        """
        if self.get_size() != other.get_size():
            raise MatrixException("Invalid size")
        return Matrix(self.get_rows_count(), self.get_columns_count(),
                      [[self[r][c] + other[r][c] for c in range(self.get_columns_count())] for r in
                       range(self.get_rows_count())])

    def __mul__(self, other):
        if type(other) is Matrix:
            return self.mul_by_matrix(other)
        elif isinstance(other, (int, float)):
            return self.mul_by_const(other)

    def mul_by_const(self, other):
        """
        Multiplies matrix with scalar
        :param other: scalar to multiply with
        :type other: float
        :return: the result matrix
        :rtype: Matrix
        """
        return Matrix(self.get_rows_count(), self.get_columns_count(), [[i * other for i in r] for r in self.get_data()])

    def mul_by_matrix(self, other):
        """
        Multiplies two matrices
        :param other: second matrix to multiply with
        :type other: Matrix
        :return: the result matrix
        :rtype: Matrix
        """
        result = Matrix(self.get_rows_count(), other.get_columns_count())
        mid_length = self.get_columns_count()
        for r in range(self.get_rows_count()):
            for c in range(other.get_columns_count()):
                temp = 0
                for m in range(mid_length):
                    temp += self[r][m] * other[m][c]
                result[r][c] = temp
        return result

    def __str__(self):
        return '\n'.join([' '.join([str(int(n)) if n.is_integer() else str(round(n, 3)) for n in r]) for r in self.get_data()])

    def transpose_main(self):
        """
        Transposes along the main diagonal
        :return: transposed matrix
        :rtype: Matrix
        """
        res = Matrix(*(self.get_size()[::-1]))
        for i, r in enumerate(self.get_data()):
            for j, e in enumerate(r):
                res[j][i] = e
        self._rows_count, self._columns_count = res.get_size()
        self._data = res.get_data()
        return self

    def transpose_side(self):
        """
        Transposes along the side diagonal
        :return: transposed matrix
        :rtype: Matrix
        """
        self.transpose_vertical()
        self.transpose_main()
        self.transpose_vertical()
        return self

    def transpose_vertical(self):
        """
        Transposes along the vertical line
        :return: transposed matrix
        :rtype: Matrix
        """
        for i, r in enumerate(self.get_data()):
            self.update_row(i, r[::-1])
        return self

    def transpose_horizontal(self):
        """
        Transposes along the horizontal line
        :return: transposed matrix
        :rtype: Matrix
        """
        self.transpose_main()
        self.transpose_vertical()
        self.transpose_main()
        return self

    def calc_determinant(self):
        if self.get_columns_count() == 1:
            return self[0][0]
        if self.get_columns_count() == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        d = 0
        for j in range(self.get_columns_count()):
            d += self[0][j] * self.find_cofactor(0, j)
        return d

    def find_cofactor(self, r, c):
        return (-1) ** (r + c) * self.find_minor(r, c).calc_determinant()

    def find_minor(self, r, c):
        new_mat = Matrix(self.get_rows_count() - 1, self.get_columns_count() - 1)
        index = 0
        for i, row in enumerate(self):
            if i == r:
                continue
            new_row = list(row)
            del new_row[c]
            new_mat.update_row(index, new_row)
            index += 1
        return new_mat

    def calc_inverse(self):
        d = self.calc_determinant()
        if d == 0:
            raise MatrixException("This matrix doesn't have an inverse.")
        data = [[self.find_cofactor(r, c) for c in range(self.get_columns_count())] for r in range(self.get_rows_count())]
        new_mat = Matrix(self.get_rows_count(), self.get_columns_count(), data)
        new_mat.transpose_main()
        return new_mat * (1 / self.calc_determinant())


class MatrixException(Exception):

    def __init__(self, s):
        self.what = s

    def __str__(self):
        return self.what


def show_menu(menu=MAIN):
    """
    Prints the menu
    :param menu: menu to print
    :type menu: int
    :return: None
    """
    if menu == MAIN:
        print("""\
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")
    elif menu == TRANSPOSE:
        print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")


def take_option():
    """
    Takes an option from the user
    :return: the option
    :rtype: int
    """
    return int(input("Your choice: "))


def handle_option(option):
    """
    Handles the user input
    :param option: user input
    :type option: int
    :return: None
    """
    if option == ADD:
        add_matrices()
    elif option == MUL_BY_CONST:
        multiply_by_const()
    elif option == MUL_MATRICES:
        multiply_matrices()
    elif option == TRANSPOSE:
        handle_transpose()
    elif option == DETERMINANT:
        calculate_determinant()
    elif option == INVERSE:
        calculate_inverse()


def take_matrix(number=''):
    """
    Template for inputting matrix
    :param number: extra text for the inputted matrix
    :type number: str
    :return: the inputted matrix
    :rtype: Matrix
    """
    size = list(map(int, input(f"Enter size of{number} matrix: ").split()))
    print(f"Enter{number} matrix:")
    return Matrix.input_matrix(size)


def truncate(f, n):
    return floor(f * 10 ** n) / 10 ** n


def add_matrices():
    """
    Adds two matrices and prints the result
    :return: None
    """
    mat1 = take_matrix(' first')
    mat2 = take_matrix(' second')
    print(f'The result is:\n{mat1 + mat2}')


def multiply_by_const():
    """
    Multiplies matrix by const and prints it
    :return: None
    """
    mat = take_matrix()
    const = float(input("Enter constant: "))
    print(f'The result is:\n{mat * const}')


def multiply_matrices():
    """
    Multiplies two matrices and prints the result
    :return: None
    """
    mat1 = take_matrix(' first')
    mat2 = take_matrix(' second')
    if mat1.get_columns_count() != mat2.get_rows_count():
        print('The operation cannot be performed.')
        return
    print(f'The result is:\n{mat1 * mat2}')


def handle_transpose():
    """
    Transpose a matrix
    :return: None
    """
    show_menu(TRANSPOSE)
    option = take_option()
    matrix = take_matrix()
    if option == MAIN_DIAGONAL:
        print(matrix.transpose_main())
    elif option == SIDE_DIAGONAL:
        print(matrix.transpose_side())
    elif option == VERTICAL_LINE:
        print(matrix.transpose_vertical())
    elif option == HORIZONTAL_LINE:
        print(matrix.transpose_horizontal())


def calculate_determinant():
    m = take_matrix()
    print(f'The result is:\n{m.calc_determinant()}')


def calculate_inverse():
    m = take_matrix()
    try:
        print(f'The result is:\n{m.calc_inverse()}')
    except MatrixException as e:
        print(e.what)


def main():
    show_menu()
    while (option := take_option()) != EXIT:
        handle_option(option)
        print()
        show_menu()


if __name__ == '__main__':
    main()
