from datetime import datetime
from uuid import UUID
from typing import Union, Optional, List

from dateutil.parser import parse

from datalogue.dtl_utils import SerializableStringEnum
from datalogue.dtl_utils import _parse_list, _parse_uuid
from datalogue.errors import _enum_parse_error, DtlError


class JobStatus(SerializableStringEnum):
    Scheduled = "Scheduled"
    Defined = "Defined"
    Running = "Running"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Unknown = "Unknown"
    Cancelled = "Cancelled"

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error("job status", s))

    @staticmethod
    def job_status_from_str(string: str) -> Union[DtlError, 'JobStatus']:
        return SerializableStringEnum.from_str(JobStatus)(string)


class Job:
    def __init__(
        self,
        id: UUID,
        pipeline_id: Optional[UUID],
        run_at: datetime,
        status: JobStatus,
        remaining_time_millis: Optional[int],
        percentage_progress: Optional[float],
        created_by: UUID,
        errors: Optional[str],
        started_at: Optional[datetime],
        ended_at: Optional[datetime],
        average_records_speed: float,
        current_records_speed: float,
        estimated_processed_records_count: int,
        average_bytes_speed: Optional[float],
        current_bytes_speed: Optional[float],
        estimated_processed_bytes_count: Optional[int],
        total_source_records: Optional[int],
        total_source_bytes: Optional[int],
        wait_on: List[UUID] = [],
        abort_if_overlong: bool = True,
        frequency: Optional[str] = None,
        parent_job_id: Optional[UUID] = None
    ):
        self.pipeline_id = pipeline_id
        self.status = status
        self.run_at = run_at
        self.id = id
        self.remaining_time_millis = remaining_time_millis
        self.percentage_progress = percentage_progress
        self.created_by = created_by
        self.errors = errors
        self.ended_at = ended_at
        self.started_at = started_at
        self.wait_on = wait_on
        self.abort_if_overlong = abort_if_overlong
        self.frequency = frequency
        self.parent_job_id = parent_job_id

        self.average_records_speed = average_records_speed
        self.current_records_speed = current_records_speed
        self.estimated_processed_records_count = estimated_processed_records_count
        self.average_bytes_speed = average_bytes_speed
        self.current_bytes_speed = current_bytes_speed
        self.estimated_processed_bytes_count = estimated_processed_bytes_count
        self.total_source_records = total_source_records
        self.total_source_bytes = total_source_bytes

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'id: {self.id!r}, '
                f'pipeline_id: {self.pipeline_id!r}, '
                f'status: {self.status!r}, '
                f'run_at: {self.run_at!r}, '
                f'wait_on: {self.wait_on!r}, '
                f'created_by: {self.created_by!r}, '
                f'remaining_time_millis: {self.remaining_time_millis!r}, '
                f'percent_progress: {self.percentage_progress!r}, '
                f'errors: {self.errors!r}, '
                f'average_records_speed: {self.average_records_speed!r}, '
                f'current_records_speed: {self.current_records_speed!r}, '
                f'estimated_processed_records_count: {self.estimated_processed_records_count!r}, '
                f'average_bytes_speed: {self.average_bytes_speed!r}, '
                f'current_bytes_speed: {self.current_bytes_speed!r}, '
                f'estimated_processed_bytes_count: {self.estimated_processed_bytes_count!r}, '
                f'total_source_records: {self.total_source_records!r}, '
                f'total_source_bytes: {self.total_source_bytes!r}, '
                f'ended_at: {self.ended_at!r}, '
                f'started_at: {self.started_at!r}, '
                f'abort_if_overlong: {self.abort_if_overlong}, '
                f'frequency: {self.frequency}, '
                f'parent_job_id: {self.parent_job_id})')


def _job_from_payload(json: dict) -> Union[DtlError, Job]:
    job_id = json.get('jobId')
    if job_id is None:
        return DtlError("Job object should have a 'jobId' property")
    else:
        try:
            job_id = UUID(job_id)
        except ValueError:
            return DtlError("'jobId' field was not a proper uuid")

    pipeline_id = json.get('streamId')
    if pipeline_id is not None:
        try:
            pipeline_id = UUID(pipeline_id)
        except ValueError:
            return DtlError("'streamId' field was not a proper uuid")

    run_at = json.get("runDate")
    if run_at is None:
        return DtlError("Job object should have a 'runDate' property")
    else:
        try:
            run_at = parse(run_at)
        except ValueError:
            return DtlError("The 'runDate' could not be parsed as a valid date")

    status = json.get("status")
    if status is None:
        return DtlError("Job object should have a 'status' property")
    else:
        status = JobStatus.job_status_from_str(status)
        if isinstance(status, DtlError):
            return status

    remaining_time_millis = json.get('remainingTimeInMillis')
    if remaining_time_millis is not None:
        try:
            remaining_time_millis = int(remaining_time_millis)
        except ValueError:
            return DtlError("'remainingTimeInMillis' was not a proper int")

    percentage_progress = json.get('percentage')
    if percentage_progress is None:
        percentage_progress = None
    else:
        try:
            percentage_progress = float(percentage_progress)
        except ValueError:
            return DtlError("'percentage' was not a proper number")

    created_by = json.get('createdBy')
    if created_by is None:
        return DtlError("Job object should have a 'createdBy' property")
    else:
        try:
            created_by = UUID(created_by)
        except ValueError:
            return DtlError("'createdBy' was not a proper uuid")

    # details is optional
    errors = json.get('details')

    # ended_at is optional
    ended_at = json.get("endDate")
    if ended_at is not None:
        try:
            ended_at = parse(ended_at)
        except ValueError:
            return DtlError("The 'endDate' could not be parsed as a valid date")

    # started_at is optional
    started_at = json.get("startDate")
    if started_at is not None:
        try:
            started_at = parse(started_at)
        except ValueError:
            return DtlError("The 'startDate' could not be parsed as a valid date")

    wait_on = json.get('waitOn')
    if wait_on is not None:
        wait_on = _parse_list(_parse_uuid)(wait_on)
        if isinstance(wait_on, DtlError):
            return wait_on
    else:
        return DtlError("Job object should have a 'waitOn' property")

    frequency = None
    if json.get("intervalInSec") is not None:
        # TODO rename in scout so we have the same naming in both
        frequency = str(json.get("intervalInSec"))

    parent_job_id = None
    if json.get("parentJobId") is not None:
        parent_job_id = json.get("parentJobId")

    abort_if_overlong = json.get("abortIfOverlong")

    average_records_speed = json.get("averageRecordsSpeed")
    if average_records_speed is None:
        return DtlError("Job object should have a 'averageRecordsSpeed' property")
    else:
        try:
            average_records_speed = float(average_records_speed)
        except ValueError:
            return DtlError("'averageRecordsSpeed' was not a proper number")

    current_records_speed = json.get("currentRecordsSpeed")
    if current_records_speed is None:
        return DtlError("Job object should have a 'currentRecordsSpeed' property")
    else:
        try:
            current_records_speed = float(current_records_speed)
        except ValueError:
            return DtlError("'currentRecordsSpeed' was not a proper number")

    estimated_processed_records_count = json.get("estimatedProcessedRecordsCount")
    if estimated_processed_records_count is None:
        return DtlError("Job object should have a 'estimatedProcessedRecordsCount' property")
    else:
        try:
            estimated_processed_records_count = int(estimated_processed_records_count)
        except ValueError:
            return DtlError("'estimatedProcessedRecordsCount' was not a proper int")

    average_bytes_speed = json.get("averageBytesSpeed")
    if average_bytes_speed is not None:
        try:
            average_bytes_speed = float(average_bytes_speed)
        except ValueError:
            return DtlError("'averageBytesSpeed' was not a proper number")

    current_bytes_speed = json.get("currentBytesSpeed")
    if current_bytes_speed is not None:
        try:
            current_bytes_speed = float(current_bytes_speed)
        except ValueError:
            return DtlError("'currentBytesSpeed' was not a proper number")

    estimated_processed_bytes_count = json.get("estimatedProcessedBytesCount")
    if estimated_processed_bytes_count is not None:
        try:
            estimated_processed_bytes_count = int(estimated_processed_bytes_count)
        except ValueError:
            return DtlError("'estimatedProcessedBytesCount' was not a proper int")

    total_source_records = json.get("totalSourceRecords")
    if total_source_records is not None:
        try:
            total_source_records = int(total_source_records)
        except ValueError:
            return DtlError("'totalSourceRecords' was not a proper int")

    total_source_bytes = json.get("totalSourceBytes")
    if total_source_bytes is not None:
        try:
            total_source_bytes = int(total_source_bytes)
        except ValueError:
            return DtlError("'totalSourceBytes' was not a proper int")

    job = Job(
        id=job_id,
        pipeline_id=pipeline_id,
        run_at=run_at,
        status=status,
        remaining_time_millis=remaining_time_millis,
        percentage_progress=percentage_progress,
        created_by=created_by,
        errors=errors,
        started_at=started_at,
        ended_at=ended_at,
        average_records_speed=average_records_speed,
        current_records_speed=current_records_speed,
        estimated_processed_records_count=estimated_processed_records_count,
        average_bytes_speed=average_bytes_speed,
        current_bytes_speed=current_bytes_speed,
        estimated_processed_bytes_count=estimated_processed_bytes_count,
        total_source_records=total_source_records,
        total_source_bytes=total_source_bytes,
        wait_on=wait_on,
        abort_if_overlong=abort_if_overlong,
        frequency=frequency,
        parent_job_id=parent_job_id)

    return job
