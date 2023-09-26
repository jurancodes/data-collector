import requests, os
import mysql.connector

# MySQL database configuration
db_config = {
    "host": os.environ['MYSQL_HOST'],
    "port": int(os.environ['MYSQL_PORT']),  # Convert port to an integer
    "user": os.environ['MYSQL_USER'],
    "password": os.environ['MYSQL_PASSWORD'],
    "database": os.environ['MYSQL_DATABASE'],
}

def fetch_and_insert_players(page, per_page):
    # API endpoint URL with pagination parameters
    api_url = f"https://www.balldontlie.io/api/v1/players?page={page}&per_page={per_page}"

    try:
        # Fetch data from the API
        response = requests.get(api_url)
        data = response.json().get("data", [])

        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create a table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS nba_players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            position VARCHAR(255),
            height_feet INT,
            height_inches INT,
            weight_pounds INT,
            team_id INT,
            team_abbreviation VARCHAR(255),
            team_city VARCHAR(255),
            team_conference VARCHAR(255),
            team_division VARCHAR(255),
            team_full_name VARCHAR(255),
            team_name VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)

        # Insert data into the MySQL database
        insert_query = """
        INSERT INTO nba_players (first_name, last_name, position, height_feet, height_inches, weight_pounds, 
                                team_id, team_abbreviation, team_city, team_conference, team_division, team_full_name, team_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for player in data:
            cursor.execute(insert_query, (
                player.get("first_name"),
                player.get("last_name"),
                player.get("position"),
                player.get("height_feet"),
                player.get("height_inches"),
                player.get("weight_pounds"),
                player["team"]["id"],
                player["team"]["abbreviation"],
                player["team"]["city"],
                player["team"]["conference"],
                player["team"]["division"],
                player["team"]["full_name"],
                player["team"]["name"]
            ))
        
        # Commit the changes and close the database connection
        connection.commit()
        cursor.close()
        connection.close()

        print(f"Page {page}: Data successfully fetched and saved to MySQL database.")

    except Exception as e:
        print(f"An error occurred on page {page}: {str(e)}")

# Set the desired pagination parameters
per_page = int(os.environ['PER_PAGE'])  # Convert per_page to an integer
total_pages = int(os.environ['TOTAL_PAGES'])  # Convert total_pages to an integer

# Fetch data for each page
for page in range(1, total_pages + 1):
    fetch_and_insert_players(page, per_page)

print("All data fetched and saved to MySQL database.")
