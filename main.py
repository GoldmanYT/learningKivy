from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class Container(GridLayout):
    next_move = ObjectProperty()
    label_info = ObjectProperty()
    symbols = {
        0: 'X',
        1: 'O'
    }

    def new_game(self):
        for row in self.field:
            for button in row:
                button.cell = -1
                button.text = ''
        self.next_move = 0
        self.label_info.text = 'Ходит: X'

    def make_move(self, button):
        if button.cell != -1 or self.game_ended():
            return
        button.cell = self.next_move
        button.text = self.symbols.get(button.cell)
        self.next_move = 1 - self.next_move
        symbol = self.symbols.get(self.next_move)
        if self.game_ended():
            winner = self.check_winner()
            if winner is not None:
                self.label_info.text = f'{self.symbols.get(winner)} выиграл!'
            else:
                self.label_info.text = f'Ничья!'
        else:
            self.label_info.text = f'Ходит: {symbol}'

    def check_winner(self):
        for row in range(3):
            if (winner := self.field[row][0].cell) != -1 and \
                    all(winner == self.field[row][col].cell
                        for col in range(3)):
                return winner

        for col in range(3):
            if (winner := self.field[0][col].cell) != -1 and \
                    all(winner == self.field[row][col].cell
                        for row in range(3)):
                return winner

        if (winner := self.field[0][0].cell) != -1 and \
                all(winner == self.field[coord][coord].cell
                    for coord in range(3)):
            return winner

        if (winner := self.field[0][2].cell) != -1 and \
                all(winner == self.field[coord][2 - coord].cell
                    for coord in range(3)):
            return winner

        return None

    def game_ended(self):
        if all(button.cell != -1
               for row in self.field
               for button in row):
            return True

        if self.check_winner() is not None:
            return True

        return False


class MyApp(App):
    def build(self):
        return Container()


if __name__ == '__main__':
    app = MyApp()
    app.run()
