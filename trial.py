from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Placeholder for the file URL. The caller will replace this.
# Example: FILE_URL = "file:///C:/path/to/checkout.html"
FILE_URL = "C:/Users/tasha/Downloads/autonomous-qa-agent/autonomous-qa-agent/assets/checkout.html"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get(FILE_URL)

    # Add one Wireless Mouse to the cart to get a base price
    add_mouse_button = driver.find_element(By.ID, "addMouse")
    add_mouse_button.click()

    # Wait for the total price to update to the initial price (20.00 for one mouse)
    # The updateTotal function is called on button click, so it should be updated.
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "totalPrice"), "20.00")
    )
    
    # Get the initial total price before discount
    initial_total_price_text = driver.find_element(By.ID, "totalPrice").text
    initial_total_price = float(initial_total_price_text)

    # Define the discount code and expected discounted value
    discount_code = "SAVE15"
    expected_discounted_price = initial_total_price * 0.85

    # Enter the discount code
    discount_code_input = driver.find_element(By.ID, "discountCode")
    discount_code_input.send_keys(discount_code)

    # Manually trigger the updateTotal function since typing into the discount code
    # field doesn't automatically trigger it based on the current JS event listeners.
    driver.execute_script("updateTotal();")

    # Wait for the total price to update with the discount
    # We expect the total to be 20.00 * 0.85 = 17.00
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "totalPrice"), f"{expected_discounted_price:.2f}")
    )

    # Get the final total price after applying the discount
    final_total_price_text = driver.find_element(By.ID, "totalPrice").text
    final_total_price = float(final_total_price_text)

    # Assert that the final price is reduced by 15 percent
    assert abs(final_total_price - expected_discounted_price) < 0.01, \
        f"Assertion Failed: Expected discounted price {expected_discounted_price:.2f}, but got {final_total_price:.2f}"
    
    print(f"Test TC-001 PASSED: Discount code '{discount_code}' successfully reduced the price.")
    print(f"Initial Price: ${initial_total_price:.2f}, Final Price: ${final_total_price:.2f}")

except Exception as e:
    print(f"Test TC-001 FAILED: {e}")

finally:
    # Close the browser
    driver.quit()