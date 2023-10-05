from utils.calendar_converter import CalendarConverter, load_env_data


username, password, _ = load_env_data()
calendar_converter = CalendarConverter()
calendar_converter.login(username, password)

teams = calendar_converter.list_teams()

team_list = [
    ("TEAM NAME", "TEAM ID"),
] + teams

str_template = "{:^8} | {}"
print(str_template.format("TEAM ID", "TEAM NAME"))
for team_id, team_name in teams:
    print(str_template.format(team_id, team_name))
