#!/usr/bin/env python3
"""Generate high-quality multi-page PDF from the Utopia MAX Guide HTML infographic."""

from playwright.sync_api import sync_playwright
import os

def main():
    html_path = os.path.abspath("utopia-max-infographic.html")
    output_path = os.path.abspath("Utopia_of_the_Seas_MAX_Guide_Final.pdf")
    
    print(f"Loading: {html_path}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1200, "height": 1600},  # Good for infographic rendering
            device_scale_factor=2,  # Higher quality
        )
        page = context.new_page()
        
        # Load the local HTML file
        page.goto(f"file://{html_path}", wait_until="networkidle", timeout=120000)
        
        # Extra wait for images and Tailwind to fully render
        page.wait_for_timeout(3000)
        
        # Generate PDF - multi-page A4 portrait with good margins
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={
                "top": "0.5in",
                "bottom": "0.5in",
                "left": "0.4in",
                "right": "0.4in",
            },
            display_header_footer=False,
            prefer_css_page_size=True,
        )
        
        browser.close()
    
    print(f"✅ PDF created: {output_path}")
    print(f"   Size: {os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    main()