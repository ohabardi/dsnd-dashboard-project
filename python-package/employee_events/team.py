from employee_events.query_base import QueryBase
from employee_events.sql_execution import QueryMixin  # already inherited, but fine to include

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
            SELECT positive_events, negative_events FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(query)

def event_counts(self, id):
    query = f"""
        SELECT event_date,
               SUM(CASE WHEN event_type = 'positive' THEN 1 ELSE 0 END) AS positive,
               SUM(CASE WHEN event_type = 'negative' THEN 1 ELSE 0 END) AS negative
        FROM employee_events
        WHERE employee_id = {id}
        GROUP BY event_date
        ORDER BY event_date
    """
    return self.pandas_query(query)
