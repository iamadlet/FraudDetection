"""
Database repositories for CRUD operations
"""

from app.database.connection import db
from app.models.schemas import ValidatedTransaction, Pattern


class ValidatedTransactionRepository:
    """Repository for validated transaction operations"""
    
    @staticmethod
    def create(transaction: ValidatedTransaction):
        """Insert a validated transaction into the database"""
        query = """
            INSERT INTO transactions 
            (cst_dim_id, transdate, transdatetime, amount, docno, direction, target)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            transaction.cst_dim_id,
            transaction.transdate,
            transaction.transdatetime,
            transaction.amount,
            transaction.docno,
            transaction.direction,
            transaction.target
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def get_all():
        """Retrieve all validated transactions"""
        query = "SELECT * FROM validated_transactions ORDER BY id DESC"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_cst_dim_id(cst_dim_id: str):
        """Retrieve transactions by customer ID"""
        query = "SELECT * FROM validated_transactions WHERE cst_dim_id = %s"
        return db.execute_query(query, (cst_dim_id,))


class PatternRepository:
    """Repository for pattern operations"""
    
    @staticmethod
    def create(pattern: Pattern):
        """Insert a pattern into the database"""
        query = """
            INSERT INTO patterns 
            (transdate, cst_dim_id, monthly_os_changes, monthly_phone_model_changes,
             last_phone_model_categorical, last_os_categorical, logins_last_7_days,
             logins_last_30_days, login_frequency_7d, login_frequency_30d,
             freq_change_7d_vs_mean, logins_7d_over_30d_ratio, avg_login_interval_30d,
             std_login_interval_30d, var_login_interval_30d, ewm_login_interval_7d,
             burstiness_login_interval, fano_factor_login_interval, zscore_avg_login_interval_7d)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            pattern.transdate,
            pattern.cst_dim_id,
            pattern.monthly_os_changes,
            pattern.monthly_phone_model_changes,
            pattern.last_phone_model_categorical,
            pattern.last_os_categorical,
            pattern.logins_last_7_days,
            pattern.logins_last_30_days,
            pattern.login_frequency_7d,
            pattern.login_frequency_30d,
            pattern.freq_change_7d_vs_mean,
            pattern.logins_7d_over_30d_ratio,
            pattern.avg_login_interval_30d,
            pattern.std_login_interval_30d,
            pattern.var_login_interval_30d,
            pattern.ewm_login_interval_7d,
            pattern.burstiness_login_interval,
            pattern.fano_factor_login_interval,
            pattern.zscore_avg_login_interval_7d
        )
        return db.execute_insert(query, params)
    
    @staticmethod
    def get_all():
        """Retrieve all patterns"""
        query = "SELECT * FROM patterns ORDER BY id DESC"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_cst_dim_id(cst_dim_id: str):
        """Retrieve patterns by customer ID"""
        query = "SELECT * FROM patterns WHERE cst_dim_id = %s"
        return db.execute_query(query, (cst_dim_id,))
