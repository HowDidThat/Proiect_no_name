from abc import ABC, abstractmethod
from typing import List, Dict


class QuizRendererBase(ABC):
    @abstractmethod
    def render_question(self, question: Dict):
        pass

    @abstractmethod
    def render_options(self, options: List):
        pass


class QuizRepresentation(ABC):
    def __init__(self, renderer: QuizRendererBase):
        self.renderer = renderer

    @abstractmethod
    def show_question(self, question: Dict):
        pass

    @abstractmethod
    def show_options(self, options: List):
        pass


class BasicQuizRenderer(QuizRendererBase):
    def render_question(self, question: Dict):
        # Implementation for basic question rendering
        pass

    def render_options(self, options: List):
        # Implementation for basic options rendering
        pass


class InteractiveQuizRenderer(QuizRendererBase):
    def render_question(self, question: Dict):
        # Implementation for interactive question rendering
        pass

    def render_options(self, options: List):
        # Implementation for interactive options rendering
        pass
