from selenium import webdriver
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Replace with the path to your WebDriver executable (e.g., chromedriver)
WEBDRIVER_PATH = r"C:\Users\mmdip\Downloads\chromedriver_win32 (1)\chromedriver.exe"

# URL of the species list page
SPECIES_URL = 'https://indiabiodiversity.org/species/list?max=16&offset=0&sGroup=841&sort=species.lastUpdated&userGroupList&view=grid'

# Configure Chrome WebDriver
chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = Chrome(executable_path=WEBDRIVER_PATH, options=chrome_options)

# Lists to store species data
data = []

try:
    # Open the URL
    driver.get(SPECIES_URL)

    # Find elements containing species URLs
    species_elements = driver.find_elements(By.CSS_SELECTOR, ".chakra-link.css-spn4bz")
    scientific_name_elements = driver.find_elements(By.CSS_SELECTOR, "h2.chakra-heading.elipsis-2.css-9f6g39")

    # Keep track of seen species URLs
    seen_species = set()

    # Infinite loop to keep scrolling and scraping until the end
    index = 0
    while True:
        # Extract and print the href values and scientific names
        for element, scientific_name_element in zip(species_elements, scientific_name_elements):
            species_url = element.get_attribute("href")
            scientific_name = scientific_name_element.text.strip()

            if species_url not in seen_species:
                seen_species.add(species_url)
                data.append([index + 1, scientific_name, species_url])
                index += 1
                print(f"{index}. {scientific_name} - URL: {species_url}")

        # Scroll to the end of the page using the "End" key
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)

        # Wait for a short duration to allow new species to load
        time.sleep(2)  # Adjust this delay as needed

        # Check if there are new species loaded by comparing the number of previously seen species
        if len(seen_species) == len(species_elements):
            print("No more new species to load.")
            break

        # Update the list of species elements and scientific name elements
        species_elements = driver.find_elements(By.CSS_SELECTOR, ".chakra-link.css-spn4bz")
        scientific_name_elements = driver.find_elements(By.CSS_SELECTOR, "h2.chakra-heading.elipsis-2.css-9f6g39")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the WebDriver
    driver.quit()

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=["Index", "Scientific Name", "URL"])

    # Save the DataFrame to a CSV file
    df.to_csv("species_data_mamals.csv", index=False)

