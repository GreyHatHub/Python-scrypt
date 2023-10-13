import undetected_chromedriver as uc

PATHDRIVER = "/home/otk/Desktop/Python-script/WEB-Parser/Selenium Parse/chromedriver"
def main():
    # Set the path to the chromedriver executable
    chromedriver_path = "path/to/chromedriver"

    # Create options object
    options = uc.ChromeOptions()

    # Add options if needed
    # options.add_argument("--headless")  # Run in headless mode
    # options.add_argument("--disable-gpu")  # Disable GPU acceleration

    # Create an instance of Undetected ChromeDriver with options
    driver = uc.Chrome(executable_path=PATHDRIVER, options=options)

    try:
        # Open Google
        driver.get("https://www.google.com")

        # Rest of your code for interacting with the Google page

    except Exception as ex:
        print(ex)

    finally:
        # Close the ChromeDriver
        driver.quit()

if __name__ == "__main__":
    main()