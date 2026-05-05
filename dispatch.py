import requests
from notion_client import Client

def send_to_slack(webhook_url, summary):
    payload = {"text": f"🚀 *New Meeting Summary:*\n{summary}"}
    requests.post(webhook_url, json=payload)

def send_to_notion(token, database_id, summary, tasks):
    notion = Client(auth=token)
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": "Meeting Summary"}}]},
            "Status": {"select": {"name": "Done"}}
        },
        children=[
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": summary}}]}}
        ]
    )