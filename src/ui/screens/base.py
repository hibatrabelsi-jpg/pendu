"""Classe de base pour les écrans."""
from abc import ABC, abstractmethod
import pygame


class BaseScreen(ABC):
    """Classe abstraite de base pour tous les écrans."""

    def __init__(self, game_state: dict):
        """
        Initialise l'écran.

        Args:
            game_state: Dictionnaire partagé contenant l'état du jeu
        """
        self.game_state = game_state
        self.next_screen: str | None = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Gère un événement.

        Returns:
            Le nom du prochain écran ou None pour rester sur cet écran
        """
        pass

    @abstractmethod
    def update(self, dt: float, mouse_pos: tuple):
        """
        Met à jour l'état de l'écran.

        Args:
            dt: Delta time en secondes
            mouse_pos: Position de la souris
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface, fonts: dict):
        """
        Dessine l'écran.

        Args:
            surface: Surface pygame sur laquelle dessiner
            fonts: Dictionnaire des polices
        """
        pass
