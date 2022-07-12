# -*- coding: utf-8 -*-

import json
from ast import Param
from email import contentmanager
from queue import Empty
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



# option = Options()
# option.headless = True
# driver = webdriver.Chrome(options=option)

# driver = webdriver.Chrome()

# driver.implicitly_wait(13)
# driver.get("https://pt.wikipedia.org/")

# driver.close()


driver = webdriver.Chrome()

acceptable_alphabetical_characters = [
        'a', 'á', 'à', 'ã', 'â', 'b', 'c', 'd', 'e', 'ê', 'é', 'f', 'g',
        'h', 'i', 'í', 'j', 'k', 'l', 'm', 'n', 'o', 'ó', 'ô', 'õ', 'p', 'q', 'r', 's', 't', 'u', 'ú', 'v',
        'w', 'x', 'y', 'z', ' ', 'ç'
    ]

acceptable_numerical_characters = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

# check if a page has already been visited
def page_is_visited(page_url):
    with open('JSON files/visited_wikipedia_pages.js','r+') as json_file:
        file_data = json.load(json_file)

        if(page_url in file_data):
            return True

        else:
            return False

# add the weights if the word was already in file_data
# or add the word and the weight if not
def add_to_file_data(file_data, new_data):
    for item_to_add in new_data:
        if(item_to_add in file_data):
            file_data[item_to_add] = new_data[item_to_add] + file_data[item_to_add]

        else:
            file_data[item_to_add] = new_data[item_to_add]

# save visited links on JSON file
# most of this function is from:
# https://www.geeksforgeeks.org/append-to-json-file-using-python/
def save_file_visited_wikipedia_pages(new_data):
    with open('JSON files/visited_wikipedia_pages.js','r+') as json_file:
        # First we load existing data into a dict.
        file_data = json.load(json_file)

        # Join new_data with file_data
        file_data.update(new_data)

        # Sets file's current position at offset.
        json_file.seek(0)

        # convert back to json.
        json.dump(file_data, json_file, indent = 4)

# save words and their weights on JSON file
def save_file_old_words_and_weights(new_data):
    with open('JSON files/old_words_and_weights.js','r+') as json_file:
        # First we load existing data into a dict.
        file_data = json.load(json_file)

        # Add new_data to file_data
        add_to_file_data(file_data, new_data)

        # Sets file's current position at offset.
        json_file.seek(0)

        # convert back to json.
        json.dump(file_data, json_file, indent = 4)

def process_page_content(content_to_process):

    textual_content = []

    # remove undesireble characters
    # and save the words and the numbers in two separate lists
    for paragraph_index, paragraph in enumerate(content_to_process):
        textual_content.append("")
        for character_index, current_character in enumerate(paragraph):
            if(current_character in acceptable_alphabetical_characters):
                textual_content[paragraph_index] += current_character
                
                # remove textual characters, letting only numbers and blank spaces
                paragraph = list(paragraph)
                paragraph[character_index] = " "
                paragraph = "".join(paragraph)

            elif(not (current_character in acceptable_numerical_characters)):
                paragraph = list(paragraph)
                paragraph[character_index] = " "
                paragraph = "".join(paragraph)

        content_to_process[paragraph_index] = paragraph

    # at this point
    # content_to_process is a list of strings
    # only with blank spaces and numbers
    numerical_content = " ".join(content_to_process)
    numerical_content = numerical_content.split(" ")
    numerical_content = list(dict.fromkeys(numerical_content))
    if("" in numerical_content):
        numerical_content.remove("")

    del content_to_process

    textual_content = " ".join(textual_content)
    textual_content = textual_content.split(" ")
    textual_content = list(dict.fromkeys(textual_content))
    if("" in textual_content):
        textual_content.remove("")

    # create two lists with no duplicate elements
    no_textual_duplicates = list(dict.fromkeys(textual_content))
    no_numerical_duplicates = list(dict.fromkeys(numerical_content))

    # count the words and the numbers
    # and save the information on a dictionary
    old_words_and_weights = {}

    for word in no_textual_duplicates:
        old_words_and_weights[word] = textual_content.count(word)

    for numerical_element in no_numerical_duplicates:
        old_words_and_weights[numerical_element] = numerical_content.count(numerical_element)

    return old_words_and_weights

# check if the link is acceptable to be accessed later
def check_link(link):
    if(page_is_visited(link)):
        return False

    # "https://pt.wikipedia.org/wiki/Sistema_fechado"
    # every valid link has only 4 '/' and no '#'
    elif(link.count('/') > 4 or link.count('#') > 0):
        return False

    else:
        return True


# main function to get the content from the wikipedia pages
def get_content(page_url, level):

    if(page_url == "" and level == 0):
        driver.get("https://pt.wikipedia.org/")

    driver.find_element(by=By.XPATH, value='//*[@id="n-randompage"]/a').click()

    # get the url of the first page visited
    visited_page_url = driver.current_url

    print("level: " + str(level))
    print(visited_page_url)

    # check if the page was visited
    # if it is, begin the process again
    if(page_is_visited(visited_page_url)):
        get_content(page_url="", level=0)

    # and if not save the url
    # to avoid future visits to it
    else:
        save_file_visited_wikipedia_pages(
            new_data={
                visited_page_url: visited_page_url
            }
        )

    # get the text data from the page
    # process it and save it in a JSON file
    raw_content = driver.find_elements(by=By.XPATH, value='//*[@id="bodyContent"]//p')
    content_to_process = []
    
    for paragraph in raw_content:
        content_to_process.append(paragraph.text.lower())

    del raw_content

    old_words_and_weights = process_page_content(
        content_to_process=content_to_process
    )

    # print(old_words_and_weights)

    save_file_old_words_and_weights(new_data=old_words_and_weights)

    # if level != x
    # get the links from the page to start another scraping
    if(level != 3):
        raw_links = driver.find_elements(by=By.XPATH, value='//*[@id="bodyContent"]//p//a')
        links = []

        for link in raw_links:
            link_as_string = link.get_attribute('href')

            if(link_as_string):
                if(check_link(link_as_string)):
                    links.append(link_as_string)

        # print(links)
        
        for link in links:
            get_content(page_url=link, level=(level + 1))

    else:
        return 1



# number_of_executions = int(input("Number of times the main loop should be run: "))

for currente_execution_number in range(1):
    get_content(page_url="", level=0)

# get_content(page_url="", level=0)
