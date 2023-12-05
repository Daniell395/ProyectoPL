from fractions import Fraction

class Printer:
    def __init__(self):
        pass

    def print_columns(self, column_array, file):
        header = "\t" + "\t".join(column_array) + "\t"
        file.write(header + "\n")
        print(header)

    def print_u_row(self, table, row_labels, file):
        row_u = row_labels[0] + "\t"
        for x in range(len(table[0])):
            result = round(table[0][x].NUM, 2)
            convert = Fraction(result).limit_denominator()
            row_u += str(convert) + "\t"
        file.write(row_u + "\n")
        print(row_u)

    def print_matrix(self, table, row_labels, column_labels, file):
        if len(table) != 0:
            self.print_columns(column_labels, file)
            self.print_u_row(table, row_labels, file)
            for i in range(1, len(table)):
                row = row_labels[i] + "\t"
                for j in range(len(table[i])):
                    result = round(table[i][j], 2)
                    convert = Fraction(result).limit_denominator()
                    row += str(convert) + "\t"
                file.write(row + "\n")
                print(row)

class Solution:
    def __init__(self):
        self.variable_list = []
        self.value_list = []

    def show_solution(self, table, row_labels, column_labels, file, is_minimization):
        self.variable_list.append("U")
        self.value_list.append(str(round(table[0][len(table[0]) - 2].NUM, 2)))
        for i in range(1, len(row_labels)):
            self.value_list.append(table[i][len(table[i]) - 2])
            self.variable_list.append(row_labels[i])

        self.place_variables(column_labels)
        self.print_variables(file)

    def place_variables(self, column_labels):
        for i in range(0, len(column_labels) - 2):
            if column_labels[i] in self.variable_list:
                continue
            else:
                self.variable_list.append(column_labels[i])
                self.value_list.append(0)

    def print_variables(self, file):
        result_str = "OPTIMAL VALUE: [Z] = " + str(self.value_list[0]) + "\t Resulting variable values: (" + \
                     str(self.variable_list[1]) + ": " + str(round(self.value_list[1], 2))
        for i in range(2, len(self.variable_list)):
            result_str += "," + str(self.variable_list[i]) + ": " + str(round(self.value_list[i], 2))
        print(result_str + " )")
        file.write(result_str + " )\n")

class MultipleSolutions:
    def __init__(self):
        self.position_list = []

    def locate_basic_variables(self, table, row_labels, column_labels):
        for i in range(1, len(row_labels)):
            if row_labels[i] in column_labels:
                self.position_list.append(column_labels.index(row_labels[i]))

        return self.check_multiple_solutions(table)

    def check_multiple_solutions(self, table):
        for i in range(len(table[0]) - 2):
            if i not in self.position_list:
                if table[0][i].NUM == 0:
                    return i
        return -1

class OutputFile:
    def __init__(self, name):
        self.file = open(name, "w+")
        print(name)

    def get_file(self):
        return self.file
