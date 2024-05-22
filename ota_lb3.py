import tkinter as tk

class NQueens:
    """
    Решение задачи о `k` ферзях на шахматной доске с использованием метода поиска с возвратами.

    Атрибуты:
        n (int): Размер шахматной доски и количество ферзей.
        board (list of int): Список, где индекс представляет строку, а значение - столбец, 
                             в котором размещен ферзь.

    Методы:
        solve() -> list of int:
            Находит решение задачи и возвращает список с размещением ферзей.
        _backtrack(row: int) -> bool:
            Рекурсивный метод для поиска решения путем размещения ферзей строка за строкой.
        _is_safe(row: int, col: int) -> bool:
            Проверяет, безопасно ли размещение ферзя в указанной позиции.
    """

    def __init__(self, n):
        """
        Инициализирует класс NQueens с размером доски `n`.

        Параметры:
            n (int): Размер шахматной доски и количество ферзей.
        """
        self.n = n
        self.board = [-1] * n  # Изначально ни один ферзь не размещен

    def solve(self):
        """
        Запускает процесс решения задачи о `k` ферзях.

        Возвращает:
            list of int: Список с размещением ферзей, где индекс - строка, а значение - столбец.
        """
        self._backtrack(0)
        return self.board

    def _backtrack(self, row):
        """
        Рекурсивный метод для поиска решения путем размещения ферзей строка за строкой.

        Параметры:
            row (int): Текущая строка, в которой пытаемся разместить ферзя.

        Возвращает:
            bool: True, если найдено корректное размещение для всех ферзей, иначе False.
        """
        if row == self.n:
            return True
        for col in range(self.n):
            if self._is_safe(row, col):
                self.board[row] = col
                if self._backtrack(row + 1):
                    return True
                self.board[row] = -1
        return False

    def _is_safe(self, row, col):
        """
        Проверяет, безопасно ли размещение ферзя в указанной позиции.

        Параметры:
            row (int): Строка для проверки.
            col (int): Столбец для проверки.

        Возвращает:
            bool: True, если безопасно разместить ферзя, иначе False.
        """
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                return False
        return True

def draw_board(solution, n):
    """
    Отображает решение задачи о `k` ферзях на графической форме с использованием tkinter.

    Параметры:
        solution (list of int): Список с размещением ферзей,
        где индекс - строка, а значение - столбец.
        n (int): Размер шахматной доски.
    """
    window = tk.Tk()
    window.title(f"{n}-Queens Solution")

    for row in range(n):
        for col in range(n):
            color = "white" if (row + col) % 2 == 0 else "gray"
            cell = tk.Frame(window, width=50, height=50, bg=color)
            cell.grid(row=row, column=col)
            if solution[row] == col:
                label = tk.Label(window, text="Q", bg=color, font=("Arial", 24))
                label.place(x=col*50, y=row*50, width=50, height=50)

    window.mainloop()

def main():
    """
    Основная функция, которая решает задачу о `k` ферзях и отображает результат.
    
    Устанавливает количество ферзей `k` и создает экземпляр класса NQueens.
    Запускает метод solve() и передает найденное решение функции draw_board() для отображения.
    """
    k = 8  # Количество ферзей
    solver = NQueens(k)
    solution = solver.solve()

    if solution:
        draw_board(solution, k)
    else:
        print(f"No solution found for {k} queens.")

if __name__ == "__main__":
    main()
