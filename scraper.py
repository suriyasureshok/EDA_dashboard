import random
from stem import Signal
from stem.control import Controller
from playwright.async_api import async_playwright

def rotate_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def get_random_user_agent():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36",
        # Add more modern user agents
    ])

def get_random_viewport():
    widths = [1280, 1366, 1440, 1920]
    heights = [720, 768, 900, 1080]
    return {
        "width": random.choice(widths),
        "height": random.choice(heights)
    }

async def stealth_context(playwright, proxy, user_agent, viewport):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(
        proxy=proxy,
        user_agent=user_agent,
        viewport=viewport,
        locale="en-US",
        java_script_enabled=True
    )

    page = await context.new_page()

    # Anti-fingerprinting via JS
    await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.navigator.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
    """)
    return browser, page

async def scrape_url(url: str) -> str:
    rotate_ip()
    proxy = {"server": "socks5://127.0.0.1:9050"}
    user_agent = get_random_user_agent()
    viewport = get_random_viewport()

    async with async_playwright() as playwright:
        browser, page = await stealth_context(playwright, proxy, user_agent, viewport)

        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(3000)  # Let page load fully
            content = await page.content()
        except Exception as e:
            content = f"Error: {e}"
        finally:
            await browser.close()

    return content[:2000]  # Return 2000 chars max
