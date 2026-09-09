import uuid

import time

from typing import Dict, Optional, List

from pydantic import BaseModel



class Job(BaseModel):

    id: str

    status: str  # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED

    provider: str

    model: str

    text_chunks: List[str] = []

    error: Optional[str] = None

    created_at: float = 0.0

    updated_at: float = 0.0

    is_cancelled: bool = False



    @property

    def full_text(self) -> str:

        return "".join(self.text_chunks)



class JobManager:

    def __init__(self):

        self._jobs: Dict[str, Job] = {}



    def create_job(self, provider: str, model: str) -> Job:

        job_id = f"job_{uuid.uuid4().hex[:10]}"

        now = time.time()

        job = Job(

            id=job_id,

            status="PENDING",

            provider=provider,

            model=model,

            created_at=now,

            updated_at=now

        )

        self._jobs[job_id] = job

        return job



    def get_job(self, job_id: str) -> Optional[Job]:

        return self._jobs.get(job_id)



    def append_chunk(self, job_id: str, chunk: str):

        job = self._jobs.get(job_id)

        if job and not job.is_cancelled:

            job.text_chunks.append(chunk)

            job.status = "RUNNING"

            job.updated_at = time.time()



    def complete_job(self, job_id: str):

        job = self._jobs.get(job_id)

        if job and not job.is_cancelled:

            job.status = "COMPLETED"

            job.updated_at = time.time()



    def fail_job(self, job_id: str, error_msg: str):

        job = self._jobs.get(job_id)

        if job:

            job.status = "FAILED"

            job.error = error_msg

            job.updated_at = time.time()



    def cancel_job(self, job_id: str):

        job = self._jobs.get(job_id)

        if job:

            job.is_cancelled = True

            job.status = "CANCELLED"

            job.updated_at = time.time()



job_manager = JobManager()

