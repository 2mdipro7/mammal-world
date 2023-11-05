from selenium import webdriver
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Replace with the path to your WebDriver executable (e.g., chromedriver)
WEBDRIVER_PATH = r"C:\Users\mmdip\Downloads\chromedriver_win32 (1)\chromedriver.exe"

# Load the CSV file containing collected URLs
urls_df = pd.read_csv("species_data_mamals.csv")
urls = urls_df["URL"]

# Configure Chrome WebDriver
chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = Chrome(executable_path=WEBDRIVER_PATH, options=chrome_options)

# Lists to store scraped data
scraped_data = []

try:
    # Loop through the collected URLs
    for index, url in enumerate(urls, start=1):
        driver.get(url)
        
        try:
            # Find the element containing the species name
            species_name_element = driver.find_element(By.CLASS_NAME, "chakra-heading")
            species_name = species_name_element.text
            
             # Find the div with class 'css-p3oxm2'
            target_div = driver.find_element(By.CLASS_NAME, "css-tuh9u2")
            
            # Find the Taxonomy table inside the div
            taxonomy_table = target_div.find_element(By.XPATH, ".//table[@class='chakra-table css-5605sr']")

            rows = taxonomy_table.find_elements(By.TAG_NAME, "tr")
            
            taxonomy_data = {}  # To store the taxonomy data

            # Extract overview text
            overview_link = driver.find_element(By.ID, "summary")
            overview_div = overview_link.find_element(By.XPATH, "./following::div[@class='css-1ph2s56']/article/div")
            overview_text = overview_div.text

            # Extract the text from the article for different sections
            # Extract size text
            size_link = driver.find_element(By.ID, "size")
            size_div = size_link.find_element(By.XPATH, "./following::div[@class='css-1ph2s56']/article/div")
            size_text = size_div.text

            # Extract morphology text
            morphology_link = driver.find_element(By.ID, "morphology")
            morphology_div = morphology_link.find_element(By.XPATH, "./following::div[@class='css-1ph2s56']/article/div")
            morphology_text = morphology_div.text

            # Extract behavior text
            behavior_link = driver.find_element(By.ID, "behaviour")
            behavior_div = behavior_link.find_element(By.XPATH, "./following::div[@class='css-1ph2s56']/article/div")
            behavior_text = behavior_div.text

            # Extract distribution text
            distribution_link = driver.find_element(By.ID, "distribution")
            distribution_div = distribution_link.find_element(By.XPATH, "./following::div[@class='css-1ph2s56']/article/div")
            distribution_text = distribution_div.text
            
            # Iterate through rows to extract taxonomy levels and values
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 2:
                    taxonomy_level = columns[0].text
                    taxonomy_value = columns[1].text
                    taxonomy_data[taxonomy_level] = taxonomy_value

            scraped_data.append({
                "URL": url,
                "SpeciesName": species_name,
                "Overview": overview_text,
                "Size": size_text,
                "Morphology": morphology_text,
                "Behavior": behavior_text,
                "Distribution": distribution_text,
                **taxonomy_data
            })
            
            print(f"Scraped {index}/{len(urls)} URLs")
            print(scraped_data)

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
        
        except NoSuchElementException:
            print(f"No data found for {overview_text}")

        # Introduce a delay between requests to avoid overloading the server
        time.sleep(2)  # Adjust this delay as needed

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the WebDriver
    driver.quit()

    # Create a DataFrame from the scraped data
    scraped_df = pd.DataFrame(scraped_data)

    # Save the DataFrame to a CSV file
    scraped_df.to_csv("scraped_species_info_mamals.csv", index=False)
