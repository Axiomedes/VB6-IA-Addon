from abc import ABC, abstractmethod

from typing import Dict, Any, List

from app.core.jobs import Job



class BaseAIProvider(ABC):

    @property

    @abstractmethod

    def name(self) -> str:

        pass



    @abstractmethod

    async def check_health(self) -> Dict[str, Any]:

        pass



    @abstractmethod

    async def get_models(self) -> List[str]:

        pass



    @abstractmethod

    async def generate_stream(self, prompt: str, context: str, model: str, job: Job, language: str = 'es'):

        pass

