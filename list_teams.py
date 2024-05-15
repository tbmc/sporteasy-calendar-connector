from calendar_connector.calendar_converter import CalendarConverter, load_env_data
from calendar_connector.sporteasy_connector import SporteasyConnector

username, password, _ = load_env_data()
connector = SporteasyConnector()
connector.login(username, password)

teams = connector.list_teams()

team_list = [
    ("TEAM NAME", "TEAM ID"),
] + teams

str_template = "{:^8} | {}"
print(str_template.format("TEAM ID", "TEAM NAME"))
for team_id, team_name in teams:
    print(str_template.format(team_id, team_name))
