# This is the code for https://www.youtube.com/watch?v=xwWNCDau0u4&t=14s
# demo of Page-Object model (POM). Стек: Python, Selenium, Pytest
# https://github.com/senior-tester/simple-auto
# https://qa-practice.com

# pip install -r requirements.txt
# pip install selenium



# To run the tests:
cd pom
python -m pytest tests --alluredir results
pytest -v -s --alluredir results
allure serve results
