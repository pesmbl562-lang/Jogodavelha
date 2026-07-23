"""Jogo da Velha Offline para Android, feito com Python e Kivy."""

from __future__ import annotations

import math
import os
import random
from typing import List, Optional, Sequence, Tuple

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


WINNING_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class GameCell(Button):
    """Uma casa clicável do tabuleiro."""

    index = NumericProperty(0)


class TicTacToeGame(BoxLayout):
    """Controla a interface, as partidas e o adversário automático."""

    mode = StringProperty("cpu")
    difficulty = StringProperty("hard")
    current_player = StringProperty("X")
    status_text = StringProperty("Sua vez: X")
    score_x = NumericProperty(0)
    score_o = NumericProperty(0)
    score_draw = NumericProperty(0)
    game_over = BooleanProperty(False)
    cpu_thinking = BooleanProperty(False)
    board = ListProperty([""] * 9)
    cells: List[GameCell]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cells = []

    def on_kv_post(self, _base_widget) -> None:
        """Cria as nove casas depois de o arquivo KV ser carregado."""
        if self.cells:
            return

        for index in range(9):
            cell = GameCell(index=index)
            cell.bind(on_release=self._on_cell_pressed)
            self.ids.board_grid.add_widget(cell)
            self.cells.append(cell)

        self._refresh_board()

    def load_scores(self) -> None:
        """Carrega o placar salvo no armazenamento interno do aplicativo."""
        store = App.get_running_app().score_store
        if store.exists("score"):
            data = store.get("score")
            self.score_x = int(data.get("x", 0))
            self.score_o = int(data.get("o", 0))
            self.score_draw = int(data.get("draw", 0))

    def save_scores(self) -> None:
        """Salva o placar localmente, sem internet."""
        App.get_running_app().score_store.put(
            "score",
            x=int(self.score_x),
            o=int(self.score_o),
            draw=int(self.score_draw),
        )

    def set_mode(self, mode: str) -> None:
        """Seleciona dois jogadores ou partida contra o computador."""
        if mode not in {"two", "cpu"}:
            return
        self.mode = mode
        self.new_game()

    def set_difficulty(self, difficulty: str) -> None:
        """Seleciona a dificuldade do computador."""
        if difficulty not in {"easy", "hard"}:
            return
        self.difficulty = difficulty
        if self.mode == "cpu":
            self.new_game()

    def _on_cell_pressed(self, cell: GameCell) -> None:
        self.play_move(int(cell.index))

    def play_move(self, index: int) -> None:
        """Executa uma jogada humana."""
        if (
            self.game_over
            or self.cpu_thinking
            or index < 0
            or index > 8
            or self.board[index]
        ):
            return

        # No modo contra o computador, o usuário sempre joga com X.
        if self.mode == "cpu" and self.current_player != "X":
            return

        self._place_symbol(index, self.current_player)

        if self._finish_if_needed():
            return

        if self.mode == "two":
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_text = f"Vez de {self.current_player}"
        else:
            self.current_player = "O"
            self.cpu_thinking = True
            self.status_text = "Computador pensando..."
            Clock.schedule_once(self._computer_move, 0.35)

    def _computer_move(self, _dt: float) -> None:
        """Escolhe e executa a jogada do computador."""
        if self.game_over:
            self.cpu_thinking = False
            return

        empty = [i for i, value in enumerate(self.board) if not value]
        if not empty:
            self.cpu_thinking = False
            self._finish_if_needed()
            return

        if self.difficulty == "easy":
            choice = random.choice(empty)
        else:
            choice = self._best_move()

        self._place_symbol(choice, "O")
        self.cpu_thinking = False

        if self._finish_if_needed():
            return

        self.current_player = "X"
        self.status_text = "Sua vez: X"

    def _place_symbol(self, index: int, symbol: str) -> None:
        new_board = list(self.board)
        new_board[index] = symbol
        self.board = new_board
        self._refresh_board()

    def _refresh_board(self) -> None:
        """Atualiza textos e cores das casas."""
        app = App.get_running_app()
        if app is None:
            return

        for index, cell in enumerate(self.cells):
            cell.text = self.board[index]
            cell.disabled = bool(self.board[index]) or self.game_over or self.cpu_thinking
            cell.background_color = app.cell_bg
            cell.color = app.x_color if self.board[index] == "X" else app.o_color

    def _winner(self, board: Optional[Sequence[str]] = None) -> Tuple[Optional[str], Tuple[int, ...]]:
        current = board if board is not None else self.board
        for line in WINNING_LINES:
            a, b, c = line
            if current[a] and current[a] == current[b] == current[c]:
                return current[a], line
        return None, ()

    def _finish_if_needed(self) -> bool:
        """Encerra a rodada quando há vitória ou empate."""
        winner, line = self._winner()

        if winner:
            self.game_over = True
            if winner == "X":
                self.score_x += 1
            else:
                self.score_o += 1

            if self.mode == "cpu":
                self.status_text = "Você venceu!" if winner == "X" else "Computador venceu!"
            else:
                self.status_text = f"{winner} venceu!"

            self._highlight_winner(line)
            self.save_scores()
            self._disable_all_cells()
            return True

        if all(self.board):
            self.game_over = True
            self.score_draw += 1
            self.status_text = "Empate!"
            self.save_scores()
            self._disable_all_cells()
            return True

        return False

    def _highlight_winner(self, line: Sequence[int]) -> None:
        app = App.get_running_app()
        for index in line:
            self.cells[index].background_color = app.win_color

    def _disable_all_cells(self) -> None:
        for cell in self.cells:
            cell.disabled = True

    def new_game(self) -> None:
        """Limpa o tabuleiro, preservando o placar."""
        Clock.unschedule(self._computer_move)
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.cpu_thinking = False
        self.status_text = "Sua vez: X" if self.mode == "cpu" else "Vez de X"
        self._refresh_board()

    def reset_scores(self) -> None:
        """Zera vitórias e empates."""
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0
        self.save_scores()
        self.new_game()

    def _best_move(self) -> int:
        """Usa Minimax para encontrar uma jogada impossível de derrotar."""
        best_score = -math.inf
        best_moves: List[int] = []

        for index, value in enumerate(self.board):
            if value:
                continue

            trial = list(self.board)
            trial[index] = "O"
            score = self._minimax(trial, maximizing=False)

            if score > best_score:
                best_score = score
                best_moves = [index]
            elif score == best_score:
                best_moves.append(index)

        # Escolha aleatória entre jogadas equivalentes deixa as partidas menos repetitivas.
        return random.choice(best_moves)

    def _minimax(self, board: List[str], maximizing: bool) -> int:
        winner, _ = self._winner(board)
        if winner == "O":
            return 10
        if winner == "X":
            return -10
        if all(board):
            return 0

        if maximizing:
            best = -math.inf
            for index, value in enumerate(board):
                if not value:
                    board[index] = "O"
                    best = max(best, self._minimax(board, maximizing=False))
                    board[index] = ""
            return int(best)

        best = math.inf
        for index, value in enumerate(board):
            if not value:
                board[index] = "X"
                best = min(best, self._minimax(board, maximizing=True))
                board[index] = ""
        return int(best)


class JogoDaVelhaApp(App):
    """Aplicativo principal."""

    title = "Jogo da Velha Offline"

    background = ListProperty([0.035, 0.055, 0.10, 1])
    surface = ListProperty([0.075, 0.105, 0.17, 1])
    surface_light = ListProperty([0.12, 0.16, 0.24, 1])
    cell_bg = ListProperty([0.10, 0.14, 0.22, 1])
    accent = ListProperty([0.18, 0.74, 0.63, 1])
    x_color = ListProperty([0.31, 0.78, 1.0, 1])
    o_color = ListProperty([1.0, 0.62, 0.31, 1])
    win_color = ListProperty([0.15, 0.55, 0.34, 1])
    text_primary = ListProperty([0.96, 0.97, 1.0, 1])
    text_secondary = ListProperty([0.67, 0.72, 0.82, 1])

    def build(self) -> TicTacToeGame:
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.score_store = JsonStore(os.path.join(self.user_data_dir, "placar.json"))
        root = TicTacToeGame()
        root.load_scores()
        return root


if __name__ == "__main__":
    JogoDaVelhaApp().run()
