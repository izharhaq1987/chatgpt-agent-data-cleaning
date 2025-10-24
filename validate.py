import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    ...
except Exception as e:
    logger.exception("Validation failed")
    return JSONResponse(status_code=500, content={"error": str(e)})
