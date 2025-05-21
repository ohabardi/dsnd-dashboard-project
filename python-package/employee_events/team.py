# Import the QueryBase class
# YOUR CODE HERE

# Import dependencies for sql execution
#### YOUR CODE HERE

# Create a subclass of QueryBasefrom employee_events.query_base import QueryBase
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

# called  `Team`
#### YOUR CODE HERE

    # Set the class attribute `name`
    # to the string "team"
    #### YOUR CODE HERE


    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE
        
        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        #### YOUR CODE HERE
    

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        #### YOUR CODE HERE


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):

        return f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
