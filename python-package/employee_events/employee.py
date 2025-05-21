from employee_events.query_base import QueryBase
from employee_events.sql_execution import QueryMixin  # technically already inherited, but fine to import

class Employee(QueryBase):
    name = "employee"

    def names(self):
        query = """
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM employee
        """
        return self.query(query)

    def username(self, id):
        query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return self.query(query)

    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(query)
def event_counts(self, id):
    query = f"""
        SELECT event_date,
               SUM(positive_events) AS Positive,
               SUM(negative_events) AS Negative
        FROM employee_events
        WHERE employee_id = {id}
        GROUP BY event_date
    """
    return self.pandas_query(query)
