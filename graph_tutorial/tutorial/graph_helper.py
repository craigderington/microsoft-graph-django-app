from requests_oauthlib import OAuth2Session

graph_url = "https://graph.microsoft.com/v1.0"

def get_user(token):
    """
    Get the logged in users detail
    """
    graph_client = OAuth2Session(token=token)
    user = graph_client.get("{0}/me".format(graph_url))
    return user.json()


def get_calendar_events(token):
    """
    Get the logged in users event calendar
    """
    graph_client = OAuth2Session(token=token)
    query_params = {
        "$select": "subject,organizer,start,end",
        "$orderby": "createdDateTime DESC"
    }

    events = graph_client.get("{0}/me/events".format(graph_url), params=query_params)
    
    return events.json()
