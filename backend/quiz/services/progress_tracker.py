from abc import ABC, abstractmethod
from typing import List


class ProgressObserver(ABC):
    @abstractmethod
    def update(self, user_id: int, quiz_id: int, progress: float):
        pass


class UserProgressTracker(ProgressObserver):
    def update(self, user_id: int, quiz_id: int, progress: float):
        # Implementation for tracking progress
        pass


class AchievementTracker(ProgressObserver):
    def update(self, user_id: int, quiz_id: int, progress: float):
        # Implementation for tracking achievements
        pass


class ProgressSubject:
    _observers: List[ProgressObserver] = []

    def attach(self, observer: ProgressObserver):
        self._observers.append(observer)

    def detach(self, observer: ProgressObserver):
        self._observers.remove(observer)

    def notify(self, user_id: int, quiz_id: int, progress: float):
        for observer in self._observers:
            observer.update(user_id, quiz_id, progress)
