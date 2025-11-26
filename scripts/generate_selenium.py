from bs4 import BeautifulSoup

def pick_selector(soup, name_hint):
    el = soup.find(id=name_hint)
    if el:
        return f"#{name_hint}"
    el = soup.find(attrs={"name": name_hint})
    if el and el.get('name'):
        return f"[name='{name_hint}']"
    inputs = soup.find_all('input')
    for i in inputs:
        if i.get('id'):
            return f"#{i.get('id')}"
    if inputs:
        return "input"
    return "body"

def generate_script_from_testcase(test_case, checkout_html_path):
    with open(checkout_html_path, 'r', encoding='utf-8') as fh:
        html = fh.read()

    soup = BeautifulSoup(html, 'lxml')
    script_lines = []

    script_lines.append("from selenium import webdriver")
    script_lines.append("from selenium.webdriver.common.by import By")
    script_lines.append("driver = webdriver.Chrome()")

    clean_path = checkout_html_path.replace('\\', '/')
    script_lines.append(f'driver.get("file:///{clean_path}")')

    if 'discount' in test_case.get('feature','').lower():
        selector = pick_selector(soup, 'discountCode')
        script_lines.append(f'discount = driver.find_element(By.CSS_SELECTOR, "{selector}")')
        script_lines.append('discount.clear()')
        script_lines.append('discount.send_keys("SAVE15")')
        script_lines.append('pay = driver.find_element(By.ID, "payNow")')
        script_lines.append('pay.click()')

    script_lines.append('print("Script finished")')
    return "\n".join(script_lines)
