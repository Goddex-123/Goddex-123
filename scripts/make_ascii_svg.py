import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@" 

def make_ascii_svg(input_path, output_path, width=70, char_aspect_ratio=0.5):
    # Read the prepped grayscale image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error loading {input_path}")
        return

    # Calculate new height to preserve aspect ratio, adjusting for character dimensions
    original_height, original_width = img.shape
    aspect_ratio = original_height / float(original_width)
    height = int(width * aspect_ratio * char_aspect_ratio)
    
    # Resize image
    resized_img = cv2.resize(img, (width, height))
    
    # Map pixels to ASCII
    # Image is grayscale (0-255). We want 255 (white) to map to RAMP[0] (' ')
    # and 0 (black) to map to RAMP[-1] ('@').
    # So we can just invert it or map directly.
    # 0 -> len-1, 255 -> 0
    ascii_grid = []
    ramp_len = len(RAMP)
    
    for row in resized_img:
        ascii_row = ""
        for pixel in row:
            # Map 0-255 to 0-(ramp_len-1)
            # 255 -> 0, 0 -> ramp_len-1
            index = int((255 - pixel) / 255.0 * (ramp_len - 1))
            ascii_row += RAMP[index]
        ascii_grid.append(ascii_row)

    # SVG parameters
    font_size = 12
    line_height = 14
    svg_width = width * 7.2  # Approximate width of a monospace char
    svg_height = height * line_height + 20
    
    type_dur = 0.04 # seconds per line
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .ascii { font-family: monospace; font-size: ' + str(font_size) + 'px; fill: #a8b2bd; white-space: pre; }')
    svg_lines.append('    .cursor { fill: #a8b2bd; }')
    svg_lines.append('  </style>')
    svg_lines.append('  <defs>')
    
    # Generate clip paths for each row
    for i in range(height):
        begin_time = i * type_dur
        svg_lines.append(f'    <clipPath id="wipe-{i}">')
        svg_lines.append(f'      <rect x="0" y="{i*line_height}" width="0" height="{line_height}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{begin_time}s" dur="{type_dur}s" fill="freeze" />')
        svg_lines.append(f'      </rect>')
        svg_lines.append(f'    </clipPath>')
    svg_lines.append('  </defs>')
    
    # Add text rows
    svg_lines.append('  <g class="ascii">')
    for i, row in enumerate(ascii_grid):
        # Escape special XML chars if any (though RAMP chars are mostly safe, '&' and '<' are not in our RAMP)
        row_safe = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y_pos = (i + 1) * line_height
        svg_lines.append(f'    <text x="0" y="{y_pos}" clip-path="url(#wipe-{i})">{row_safe}</text>')
    svg_lines.append('  </g>')
    
    # Add cursor block
    for i in range(height):
        begin_time = i * type_dur
        y_pos = i * line_height + 2
        # Cursor appears at start of line, moves across, then disappears
        svg_lines.append(f'  <rect x="0" y="{y_pos}" width="7" height="{font_size}" class="cursor" opacity="0">')
        svg_lines.append(f'    <set attributeName="opacity" to="1" begin="{begin_time}s" />')
        svg_lines.append(f'    <animate attributeName="x" from="0" to="{svg_width}" begin="{begin_time}s" dur="{type_dur}s" />')
        svg_lines.append(f'    <set attributeName="opacity" to="0" begin="{begin_time + type_dur}s" />')
        svg_lines.append(f'  </rect>')
        
    svg_lines.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated {output_path}")

if __name__ == "__main__":
    make_ascii_svg("source-prepped.png", "avi-ascii.svg")
