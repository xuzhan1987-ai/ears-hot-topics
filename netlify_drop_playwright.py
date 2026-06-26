#!/usr/bin/env python3
"""
Netlify Drop file upload using Playwright
"""
from playwright.sync_api import sync_playwright
import time
import os

HTML_PATH = "/app/data/所有对话/主对话/hot_web/index.html"

def main():
    with sync_playwright() as p:
        # Launch browser with more args
        browser = p.chromium.launch(headless=True, args=['--disable-fonts', '--disable-web-security'])
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900}
        )
        page = context.new_page()
        
        print("Opening Netlify Drop...")
        try:
            page.goto("https://app.netlify.com/drop", wait_until="load", timeout=60000)
        except Exception as e:
            print(f"Navigation error: {e}")
            # Try anyway
            page.goto("https://app.netlify.com/drop", timeout=30000)
        
        time.sleep(3)
        
        print("Page loaded. Looking for file input...")
        
        # Check for file input elements
        file_inputs = page.query_selector_all("input[type='file']")
        print(f"Found {len(file_inputs)} file input elements")
        
        # Try to find any hidden file inputs
        hidden_inputs = page.evaluate("""
            () => {
                const inputs = Array.from(document.querySelectorAll('input'));
                const hiddenInputs = inputs.filter(inp => {
                    const style = window.getComputedStyle(inp);
                    return style.display === 'none' || style.visibility === 'hidden' || inp.type === 'file';
                });
                return hiddenInputs.map(inp => ({
                    type: inp.type,
                    display: window.getComputedStyle(inp).display,
                    visibility: window.getComputedStyle(inp).visibility,
                    id: inp.id,
                    className: inp.className
                }));
            }
        """)
        print(f"Hidden inputs: {hidden_inputs}")
        
        # Try using set_input_files directly
        if file_inputs:
            print("Found file input, trying to upload...")
            try:
                file_inputs[0].set_input_files(HTML_PATH, timeout=10000)
                print("File set!")
                time.sleep(5)
            except Exception as e:
                print(f"Error setting file: {e}")
        else:
            print("No file input found.")
            
            # Try to find and dispatch drag/drop events manually
            try:
                # Find the drop zone
                drop_zone = page.query_selector(".page-drop__content, [class*=drop-hero__media], .drop-hero__content")
                if drop_zone:
                    print(f"Found drop zone: {drop_zone.tag_name}")
                    
                    # Create file-like data transfer
                    with open(HTML_PATH, 'rb') as f:
                        file_content = f.read()
                    
                    # Try to dispatch drag events
                    page.evaluate("""
                        (fileContent) => {
                            const dropZone = document.querySelector('.page-drop__content, [class*=drop-hero__media], .drop-hero__content');
                            if (dropZone) {
                                // Create a DataTransfer with file
                                const dataTransfer = new DataTransfer();
                                const file = new File([fileContent], 'index.html', {type: 'text/html'});
                                dataTransfer.items.add(file);
                                
                                // Create drag event
                                const dragEvent = new DragEvent('drop', {
                                    bubbles: true,
                                    cancelable: true,
                                    dataTransfer: dataTransfer
                                });
                                
                                // Dispatch the event
                                dropZone.dispatchEvent(dragEvent);
                                console.log('Drag event dispatched');
                            }
                        }
                    """, fileContent=file_content)
                    print("Dispatched drop event")
                    time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
        
        # Wait and check page state
        print("Waiting for upload...")
        time.sleep(5)
        
        # Check for URL on page
        try:
            page_content = page.content()
            if ".netlify.app" in page_content:
                import re
                urls = re.findall(r'https?://[^\s<>"\'/]+\.netlify\.app[^\s<>"\'/]*', page_content)
                print(f"Found Netlify URLs: {urls}")
            else:
                print("No Netlify URL found on page")
        except Exception as e:
            print(f"Error checking page: {e}")
        
        browser.close()
        print("Done!")

if __name__ == "__main__":
    main()
