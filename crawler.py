from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv


def select_noc_2171(driver):
    checkbox_group = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[13]/fieldset/div/details[3]")
    driver.execute_script("arguments[0].setAttribute('open', 'open')", checkbox_group)

    checkbox = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[13]/fieldset/div/details[3]/div[26]/span/input")
    checkbox.click()


def select_atlantic_provincies(driver):
    nova_scotia = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[14]/fieldset/div/details[7]/summary/span/input")
    nova_scotia.click()

    pei = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[14]/fieldset/div/details[10]/summary/span/input")
    pei.click()

    new_brunswick = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[14]/fieldset/div/details[4]/summary/span/input")
    new_brunswick.click()

    nfl_labrador = driver.find_element_by_xpath(
        "/html/body/main/div[2]/form/div[14]/fieldset/div/details[5]/summary/span/input")
    nfl_labrador.click()


def get_result_count(driver):
    """
    :param driver: selenium webdriver instance
    :return: number of job found given company name
    """
    found_div = driver.find_element_by_class_name('found')
    found_div_text = found_div.text
    found = found_div_text.replace(',', '')
    return int(found)


def get_job_link_list_from_single_company(driver):
    """
    :param driver: selenium webdriver instance
    :return: list of job links from a single company
    """
    job_link_list = []
    if get_result_count(driver) > 0:

        result_block = driver.find_element_by_class_name('results-jobs')
        result_list = result_block.find_elements_by_tag_name('article')

        for result in result_list:
            result_element = result.find_element_by_tag_name('a')
            job_link = result_element.get_attribute('href')
            job_link_list.append(job_link)

    return job_link_list


def import_company_data_to_list(input_file_name):
    """
    Import csv file with company name to list
    :return: list of companies
    """
    input_file_path = 'resources/in/' + input_file_name + '.csv'
    company_name_list = []
    with open(input_file_path, newline='') as file:
        reader = csv.reader(file)
        res = list(reader)

    for r in res:
        company_name_list.append(r[0])

    return company_name_list


def export_list_to_pdf(output_file_name, job_list):
    csv_out_file = 'resources/out/' + output_file_name + '.csv'

    with open(csv_out_file, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for job in job_list:
            writer.writerow([job])


def get_complete_job_list(input_file_name, output_file_name, only_noc=None, only_aipp=None):
    """
    :return: list of all job link found
    """
    options = Options()
    options.headless = True

    companies = import_company_data_to_list(input_file_name=input_file_name)
    job_list = []
    for company in companies:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.jobbank.gc.ca/jobsearch/advancedsearch")

        elem = driver.find_element_by_name("empl")  # empl
        elem.clear()
        elem.send_keys(company)

        if only_noc:
            select_noc_2171(driver)

        if only_aipp:
            select_atlantic_provincies(driver)

        elem.send_keys(Keys.RETURN)

        result = get_job_link_list_from_single_company(driver)

        if result:
            for r in result:
                job_list.append(r)

        driver.close()
    print('Jobs Found: {} Only 2171: {} Only aipp: {}'.format(str(len(job_list)), True if only_noc else False,
                                                              True if only_aipp else False))
    export_list_to_pdf(output_file_name=output_file_name, job_list=job_list)


if __name__ == '__main__':
    get_complete_job_list(input_file_name='pei-companies', output_file_name='pei_2171_aipp', only_noc=True,
                          only_aipp=True)
    get_complete_job_list(input_file_name='pei-companies', output_file_name='pei_aipp', only_aipp=True)
    get_complete_job_list(input_file_name='pei-companies', output_file_name='pei')

