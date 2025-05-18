# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
from .sql_execution import execute_sql, execute_sql_df

# Define a subclass of QueryBase called Employee
class Employee(QueryBase):

    # Set the class attribute `name` to the string "employee"
    name = "employee"

    # Define a method called `names` that returns (full_name, id) for all employees
    def names(self):
        query = """
            SELECT full_name, employee_id
            FROM employee
        """
        return execute_sql(query)

    # Define a method called `username` that returns the full name for a given employee id
    def username(self, id):
        query = f"""
            SELECT full_name
            FROM employee
            WHERE employee_id = {id}
        """
        return execute_sql(query)

    # Define a method called model_data that returns a pandas DataFrame
    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return execute_sql_df(query)
