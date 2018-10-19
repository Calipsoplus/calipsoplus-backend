class CalipsoPlusDBRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'external_db_auth':
            return 'auth_db'
        return 'default'

    def db_for_write(self, model, **hints):
        # Auth_db is read_only (external database)
        if model._meta.app_label == 'external_db_auth':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # No migrations in auth_db
        if app_label == 'external_db_auth':
            return False
        return True
