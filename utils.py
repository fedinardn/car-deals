import requests

SLACK_WEBHOOK_URL = ""

def construct_links_message(make, site, links):
    if len(links) == 0:
        return f"Found 0 {make} deals\n\n\n"
    final_string = (
        f"Found {len(links)} {make} deal(s) for the team to consider:\n")
    for i in range(len(links)):
        final_string += f"{i+1}. {links[i]}\n"
    final_string += f"\n\nSource: {site}\n\n\n"
    return final_string


def send_message(message):
    data = {"message": message}
    requests.post(SLACK_WEBHOOK_URL, json=data)
