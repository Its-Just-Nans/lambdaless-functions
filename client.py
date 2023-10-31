""" lambda less call example """

from time import sleep, time
from json import loads, dumps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

DATA_LAMBDA = '"DATA_LAMBDA"'
ERROR_LAMBDA = '"ERROR_LAMBDA"'


def do_lambda_less_call(driver, target_url, max_time=10):
    """ do the trick """
    driver.get(target_url)
    start_time = time()
    final_data = {}
    try:
        while (time() - start_time) < max_time:
            sleep(0.5)
            for entry in driver.get_log('browser'):
                message = entry.get('message')
                real_message = ' '.join(message.split()[2:])
                if real_message.startswith(DATA_LAMBDA):
                    message_data = real_message.replace(
                        f"{DATA_LAMBDA} ", "", 1)
                    decoded = loads(message_data.replace("\\", "")[1:-1])
                    return decoded
                elif real_message.startswith(ERROR_LAMBDA):
                    return {}
    except KeyboardInterrupt:
        return final_data


if __name__ == '__main__':
    options = Options()
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    ChromeDriverManager().install()
    web_driver = webdriver.Chrome(options=options)
    URL = 'http://localhost:8000/'
    data = do_lambda_less_call(web_driver, URL)
    print(dumps(data, indent=2))
