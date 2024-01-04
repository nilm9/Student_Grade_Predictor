import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for Coursera's course listings
base_url = "https://www.coursera.org/courses"

# Function to scrape course URLs from the first page
def scrape_course_urls(base_url):
    course_urls = []
    url = f"{base_url}?page=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract courses from the page
    courses = soup.find_all('li', class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76')
    new_urls = ['https://www.coursera.org' + course.a['href'] for course in courses if course.a]

    course_urls.extend(new_urls)
    return course_urls

# Function to scrape course details
def scrape_course_details(course_url):
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    course = {
        "name": "",
        "instructor": "",
        "description": "",
        "provider": "",
        "level": "",
        "duration": "",
        "price": "",
        "link": course_url
    }

    # Extracting course name
    course_name = soup.find('h3', class_='cds-CommonCard-title')
    course['name'] = course_name.text.strip() if course_name else 'N/A'

    # Extracting provider
    provider = soup.find('p', class_='cds-ProductCard-partnerNames')
    course['provider'] = provider.text.strip() if provider else 'N/A'

    # Extracting skills
    skills = soup.find('p', class_='cds-Typography-base')
    course['description'] = skills.text.strip() if skills else 'N/A'

    # Extracting rating
    rating = soup.find('p', class_='css-11uuo4b')
    course['rating'] = rating.text.strip() if rating else 'N/A'

    # Extracting reviews count
    reviews = soup.find('p', class_='css-dmxkm1')
    course['reviews'] = reviews.text.strip() if reviews else 'N/A'

    # Extracting level and duration
    metadata = soup.find('p', class_='cds-Typography-base')
    if metadata:
        meta_text = metadata.text.split('·')
        course['level'] = meta_text[0].strip() if len(meta_text) > 0 else 'N/A'
        course['duration'] = meta_text[1].strip() if len(meta_text) > 1 else 'N/A'

        return course

# Main scraping function
def main():
    print("Scraping course URLs...")
    course_urls = scrape_course_urls(base_url)

    all_courses = []
    for url in course_urls:
        print(f"Scraping course details from {url}")
        course_details = scrape_course_details(url)
        all_courses.append(course_details)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_courses)
    df.to_csv('coursera_courses.csv', index=False)
    print("Scraping completed. Data saved to coursera_courses.csv")

if __name__ == '__main__':
    main()
