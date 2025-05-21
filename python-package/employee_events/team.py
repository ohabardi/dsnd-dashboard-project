from employee_events.query_base import QueryBase
from employee_events.sql_execution import QueryMixin


class Team(QueryBase):
    name = "team"

    def names(self):
        query = """
            SELECT team_name, team_id
            FROM team
        """
        return self.query(query)

    def username(self, id):
        query = f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """
        return self.query(query)

    def model_data(self, id):
        query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee
            JOIN employee_events USING(employee_id)
            WHERE team_id = {id}
        """
        return self.pandas_query(query)

    def event_counts(self, id):
        query = f"""
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee
            JOIN employee_events USING(employee_id)
            WHERE team_id = {id}
            GROUP BY event_date
        """
        return self.pandas_query(query)
