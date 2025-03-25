import os
import requests
from datetime import datetime, timedelta

HCP_API_TOKEN = os.environ['HCP_API_TOKEN']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def main():
    since_time = (datetime.utcnow() - timedelta(minutes=10)).isoformat()

    headers = {
        'Authorization': f'Bearer {HCP_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get('https://api.housecallpro.com/v1/estimates', headers=headers)
    estimates = response.json()

    for estimate in estimates:
        created_by = estimate.get('created_by', {}).get('name', '')
        updated_at = estimate.get('updated_at', '')

        if (
            estimate.get('status') == 'sent' and
            'John Doe' in created_by and
            updated_at > since_time
        ):
            slack_data = {
                "text": f"📤 *New Estimate Sent by {created_by}*\n"
                        f"🏠 Customer: {estimate.get('customer', {}).get('name', 'Unknown')}\n"
                        f"💰 Amount: ${estimate.get('amount', 0)}\n"
                        f"📅 Sent At: {updated_at}"
            }

            requests.post(SLACK_WEBHOOK_URL, json=slack_data)

if __name__ == "__main__":
    main()
