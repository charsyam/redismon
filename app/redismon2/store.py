def get_store_manager(store_config=None, limit=120):
    if store_config and store_config.get("mode") == "mysql_store":
        from database import db_session, init_db
        db_session = init_db(store_config.get("uri"))

        from mysql_store import MysqlStore
        return MysqlStore(db_session, limit)
    else:
        from memory_store import MemoryStore
        return MemoryStore(limit)
