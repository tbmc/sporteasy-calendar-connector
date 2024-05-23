from calendar_connector.calendar_converter import CalendarConverter, load_env_data
from calendar_connector.sporteasy_connector import SporteasyConnector

username, password, _ = load_env_data()
connector = SporteasyConnector()
connector.login(username, password)

teams = connector.list_teams()

str_template = "{:^8} | {:15} | {}"
print(str_template.format("TEAM ID", "TEAM NAME", "URL"))
for team_id, team_name, team_url in teams:
    print(str_template.format(team_id, team_name, team_url))
