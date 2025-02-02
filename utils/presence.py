import re

def get_release_year(release_date):
    return release_date.split()[-1][:4]

def sanitize_console_name(console_name):
    sanitized_name = re.sub('[^0-9a-zA-Z]+', '', console_name)
    return sanitized_name.lower()

def update_presence(RPC, data, game_data, start_time, username):
    year_of_release = get_release_year(game_data['Released'])
    details = f"{game_data['GameTitle']} ({year_of_release})"
    RPC.update(
        state=data["RichPresenceMsg"],
        details=details,
        start=start_time,
        large_image="ra_logo",
        large_text=f"Released {game_data['Released']}, Developed by {game_data['Developer']}, Published by {game_data['Publisher']}",
        small_image=sanitize_console_name(game_data['ConsoleName']),
        small_text=game_data['ConsoleName'],
        buttons=[{"label": "View RA Profile", "url": f"https://retroachievements.org/user/{username}"}]
    )
