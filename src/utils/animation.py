"""Utilitaires d'animation."""


class AnimatedValue:
    """Classe pour animer des valeurs numériques en douceur."""

    def __init__(self, value: float, speed: float = 0.15):
        self.target = value
        self.current = value
        self.speed = speed

    def set_target(self, value: float):
        """Définit la valeur cible vers laquelle animer."""
        self.target = value

    def update(self):
        """Met à jour la valeur courante vers la cible."""
        self.current += (self.target - self.current) * self.speed

    def get(self) -> float:
        """Retourne la valeur courante."""
        return self.current
