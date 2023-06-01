# Jobs_aggregator

Jobs_aggregator is an educational project that demonstrates web scraping using Selenium and BeautifulSoup modules to extract job data from the job portal Jobs.cz. The project also includes a web application built with the Django framework, with dynamic frontend elements implemented using JavaScript.

## Project Goals

The primary goals of this project are:

- Learn Django framework by building the first web application
- Gain knowledge and experience in web scraping techniques
- Create a project that can be demonstrated during interviews

## Functionality

The current features of Jobs_aggregator include:

- User authentication: Users must log in to access the scraping functionality.
- Customized authentication: Authentication function in Django is adjusted, and BruteBuster module is implemented to protect against brute force attacks.
- Job scraping: Users can select a job title and city to scrape data from Jobs.cz.
- Data storage: Scraped job data is stored in a SQLite3 database using Django models.
- Data rendering: The scraped data is rendered in an HTML table.
  - Table filtering: Users can filter the table by text, salary (indicated/not indicated), and junior (junior included in the title).
  - Table sorting: Users can sort the table by all headings, except URL, by clicking on the headers (switching between ascending and descending order).

## Observations

Throughout the project, there were instances where the direction and scope of the project evolved. The initial idea was to build a web app in Django that could scrape jobs automatically and provide users with rendered data. However, the project took a different path, allowing users to perform the scraping themselves, which required additional adjustments.

For future projects, it is essential to clearly define the project goals, functionalities, and prioritize them accordingly to avoid ambiguity and ensure a smoother development process.

## Installation and Usage

To use Jobs_aggregator locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/Jobs_aggregator.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Edit the `decorators.py` file in the BruteBuster module:
   - Locate the file at `brutebuster/decorators.py`
   - In line 45, modify the code snippet as follows:
   ```python
   if fa.recent_failure():
       if fa.too_many_failures():
           fa.failures += 1
           fa.save()
           return False # MODIFY HERE
4. Set up the database: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the web application in your browser at `http://localhost:8000/dashboard`

## Contributing

Contributions to Jobs_aggregator are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your modifications.
4. Commit and push your changes to your forked repository.
5. Submit a pull request describing your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or need further assistance, please feel free to contact the project owner.

Enjoy using Jobs_aggregator!
