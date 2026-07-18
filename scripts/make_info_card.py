import os

def make_info_card(output_path):
    # Colors matching the neofetch theme
    color_title = "#a855f7" # purple from the typing SVG
    color_key = "#3b82f6"   # blue
    color_text = "#a8b2bd"  # light gray
    
    # User data
    username = "soham@github"
    hostname = "AI-ML-Engineer"
    
    info_lines = [
        ("Now", "Bridging research models to production"),
        ("Focus", "MLOps, NLP, Computer Vision"),
        ("Stack", "Python, TensorFlow, PyTorch, Docker, FastAPI"),
        ("Highlight", "SIH Winner & 12+ Production-Grade Projects"),
        ("Contact", "sohambarate16@gmail.com")
    ]
    
    # SVG configuration
    width = 490
    height = 300
    font_family = "monospace"
    font_size = 14
    line_height = 24
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('  <style>')
    svg_lines.append(f'    text {{ font-family: {font_family}; font-size: {font_size}px; fill: {color_text}; }}')
    svg_lines.append(f'    .title {{ fill: {color_title}; font-weight: bold; }}')
    svg_lines.append(f'    .key {{ fill: {color_key}; font-weight: bold; }}')
    svg_lines.append(f'    .separator {{ fill: {color_text}; }}')
    
    # Animation styles
    stagger_dur = 0.2
    
    if os.environ.get("STATIC") != "1":
        for i in range(len(info_lines) + 2): # +2 for title and dashes
            delay = i * stagger_dur
            svg_lines.append(f'    .line-{i} {{ opacity: 0; animation: fadeInSlide 0.4s ease-out {delay}s forwards; }}')
        
        svg_lines.append('    @keyframes fadeInSlide {')
        svg_lines.append('      from { opacity: 0; transform: translateX(-10px); }')
        svg_lines.append('      to { opacity: 1; transform: translateX(0); }')
        svg_lines.append('    }')
    else:
        for i in range(len(info_lines) + 2):
            svg_lines.append(f'    .line-{i} {{ opacity: 1; }}')
            
    svg_lines.append('  </style>')
    
    # Content
    svg_lines.append('  <g transform="translate(20, 40)">')
    
    # Title
    y_pos = 0
    svg_lines.append(f'    <text x="0" y="{y_pos}" class="title line-0">{username}<tspan class="separator">@</tspan>{hostname}</text>')
    
    # Dashes
    y_pos += line_height
    dashes = "-" * (len(username) + 1 + len(hostname))
    svg_lines.append(f'    <text x="0" y="{y_pos}" class="line-1">{dashes}</text>')
    
    # Info lines
    for i, (key, value) in enumerate(info_lines):
        y_pos += line_height
        class_name = f"line-{i+2}"
        svg_lines.append(f'    <text x="0" y="{y_pos}" class="{class_name}">')
        svg_lines.append(f'      <tspan class="key">{key.ljust(10)}</tspan>')
        svg_lines.append(f'      <tspan class="separator">:</tspan> {value}')
        svg_lines.append(f'    </text>')
        
    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_info_card("info-card.svg")
