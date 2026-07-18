import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(json_path, output_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    days = data.get('days', [])
    total_text = data.get('total_text', '')
    
    # SVG Dimensions
    box_size = 11
    box_spacing = 3
    
    # 53 weeks, 7 days
    cols = 53
    rows = 7
    
    graph_width = cols * (box_size + box_spacing)
    graph_height = rows * (box_size + box_spacing)
    
    width = 860
    height = 200
    
    # Calculate offset to center the graph
    offset_x = (width - graph_width) / 2
    offset_y = 50
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .day { rx: 2; ry: 2; opacity: 0; animation: slideDown 0.5s ease-out forwards; }')
    svg_lines.append('    .text-muted { fill: #8b949e; font-family: monospace; font-size: 12px; }')
    svg_lines.append('    @keyframes slideDown {')
    svg_lines.append('      from { opacity: 0; transform: translateY(-10px); }')
    svg_lines.append('      to { opacity: 1; transform: translateY(0); }')
    svg_lines.append('    }')
    svg_lines.append('  </style>')
    
    svg_lines.append(f'  <g transform="translate({offset_x}, {offset_y})">')
    
    # Group days by weeks
    weeks = [[] for _ in range(cols)]
    
    # GitHub data starts on Sunday
    # The first week might not be full, we need to map date to day of week
    
    if days:
        first_date = datetime.strptime(days[0]['date'], "%Y-%m-%d")
        # 0=Monday, 6=Sunday. GitHub week starts on Sunday (day 6 maps to row 0)
        start_day_idx = (first_date.weekday() + 1) % 7 
        
        current_week = 0
        current_day = start_day_idx
        
        for day in days:
            weeks[current_week].append({
                "level": day["level"],
                "row": current_day
            })
            current_day += 1
            if current_day > 6:
                current_day = 0
                current_week += 1
                if current_week >= cols:
                    break
    
    # Draw boxes
    for w, week in enumerate(weeks):
        for day in week:
            r = day["row"]
            level = min(day["level"], len(PALETTE) - 1)
            color = PALETTE[level]
            
            x = w * (box_size + box_spacing)
            y = r * (box_size + box_spacing)
            
            # Diagonal stagger: delay based on x + y
            delay = (w + r) * 0.015
            
            svg_lines.append(f'    <rect class="day" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay}s" />')
            
    svg_lines.append('  </g>')
    
    # Draw footer
    footer_y = offset_y + graph_height + 25
    svg_lines.append(f'  <text class="text-muted" x="{offset_x}" y="{footer_y}">{total_text}</text>')
    
    # Legend
    legend_x = offset_x + graph_width - (len(PALETTE) * (box_size + box_spacing) + 50)
    svg_lines.append(f'  <text class="text-muted" x="{legend_x - 35}" y="{footer_y}">Less</text>')
    for i, color in enumerate(PALETTE):
        lx = legend_x + i * (box_size + box_spacing)
        ly = footer_y - 10
        delay = (cols + rows + i) * 0.015
        svg_lines.append(f'  <rect class="day" x="{lx}" y="{ly}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay}s" />')
    
    svg_lines.append(f'  <text class="text-muted" x="{legend_x + len(PALETTE) * (box_size + box_spacing) + 5}" y="{footer_y}">More</text>')
    
    svg_lines.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    render_heatmap("data/contributions.json", "contrib-heatmap.svg")
