import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_contributions(username, output_path):
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching contributions from {url}...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # GitHub's contribution graph uses rects or tds depending on the A/B test or exact layout
    # Often it's <td class="ContributionCalendar-day" data-date="2023-01-01" data-level="1">
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    contributions = []
    
    for day in days:
        date_str = day.get('data-date')
        level_str = day.get('data-level')
        
        if not date_str or level_str is None:
            continue
            
        contributions.append({
            "date": date_str,
            "level": int(level_str)
        })
    
    if not contributions:
        # Fallback for SVG based rendering
        rects = soup.find_all('rect', class_='ContributionCalendar-day')
        for rect in rects:
            date_str = rect.get('data-date')
            level_str = rect.get('data-level')
            if date_str and level_str is not None:
                contributions.append({
                    "date": date_str,
                    "level": int(level_str)
                })

    # Sort by date
    contributions.sort(key=lambda x: x['date'])
    
    # Calculate stats
    total_contributions = 0
    # To get exact numbers, we'd need to parse the tooltips which have exact counts, 
    # but level 0-4 is sufficient for rendering the heatmap visually.
    # The stats footer ("9,376 contributions") is often in a text element nearby.
    h2 = soup.find('h2', class_='f4 text-normal mb-2')
    total_text = h2.text.strip() if h2 else ""
    
    data = {
        "days": contributions,
        "total_text": total_text
    }
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(contributions)} days of contributions to {output_path}")

if __name__ == "__main__":
    fetch_contributions("Goddex-123", "data/contributions.json")
