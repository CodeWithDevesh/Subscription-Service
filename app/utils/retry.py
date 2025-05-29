from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from sqlalchemy.exc import OperationalError
from app.utils.logger import get_logger
logger = get_logger(__name__)

retry_on_db_error = retry(
    stop=stop_after_attempt(3), 
    wait=wait_fixed(2),
    retry=retry_if_exception_type(OperationalError),  # Retry only on database errors
    retry_error_callback=lambda retry_state: logger.warning(
    f"Retrying due to {retry_state.outcome.exception()}"
)

)