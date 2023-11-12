from database.models import Base
from database.connection import engine, get_db
from sqlalchemy import text
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    Base.metadata.create_all(engine)
    
    trigger_creation_sql = text(
    """
    CREATE OR REPLACE TRIGGER after_insert_trigger
        AFTER INSERT
        ON public.rabbitmq_logs
        FOR EACH ROW
        EXECUTE FUNCTION public.notify_insert();
    """
    )
    function_creation_sql = text(
    """
        CREATE OR REPLACE FUNCTION public.notify_insert()
            RETURNS trigger
            LANGUAGE 'plpgsql'
            COST 100
            VOLATILE NOT LEAKPROOF
        AS $BODY$
        DECLARE 
            row_json text;
        BEGIN
            row_json := row_to_json(NEW)::text;
            PERFORM pg_notify('new_record', row_json);
            RETURN NEW;
        END;
        $BODY$;
    """
    )

    with get_db() as session:
        try:
            session.execute(function_creation_sql)
        except Exception as e:
            logger.warning('failed to create function')
        
        try:
            session.execute(trigger_creation_sql)
        except Exception as e:
            logger.warning('failed to create trigger')

    logger.info("init complete")
