
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup

AUTH = 'brd-customer-hl_415c5534-zone-ai_scraper:ktn14m0xtvxb'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print("Launching Chrome browser...")
    
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        
        # Capthcha handeling
        print("Waiting captcha to solve ...")
        solve_res = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10000},
            })
        print('Captchs solve status:', solve_res['value']['status'])
        
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        
        return html
    
        """    # specifying where chrome driver(an application to control chrome) is
        chrome_driver_path = "./chromedriver.exe"
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        
        try:
            driver.get(website)
            print("Website launched successfully!")
            html = driver.page_source
            time.sleep(10)
            
            return html
        finally:
            driver.quit()"""


def extract_body_content(html_content):
    soup= BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content): 
    # Re parse again
    soup = BeautifulSoup(body_content, 'html.parser')
    
    # Remove all script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    # effectively remove any backslash N characters that are unecessary
    cleaned_content ="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content


# LLM Has an 8,000 token limit
# We need to separate into chunks of 8,000 tokens or less (batches)

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]