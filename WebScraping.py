import bs4
import requests
import os
import time
from selenium import webdriver


PATH = ""  # SET YOUR PATH TO CHROME DRIVER/WEB DRIVER
GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'


def download_image(url, folder_name, filename, num):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(os.path.join(folder_name, filename + str(num) + ".jpg"), 'wb') as file:
            file.write(reponse.content)


def get_and_download(wd, max_images, search_URL, folder_name, filename, max_waittime):
    try:
        wd.get(search_URL)
    except:
        print('------------------------')
        print('couldn"t get to site')
        print('------------------------')
        return

    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    wd.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    page_html = wd.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})

    print(len(containers))

    len_containers = len(containers)

    for i in range(1, len_containers + 1):
        if i == max_images+1:
            break
        if i % 25 == 0:
            continue
        try:
            xPath = """//*[@id="islrg"]/div[1]/div[%s]""" % (i)
            previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img""" % (i)
            previewImageElement = wd.find_element_by_xpath(previewImageXPath)
            previewImageURL = previewImageElement.get_attribute("src")
        except:
            max_images += 1
            len_containers += 1
            continue
        try:
            wd.find_element_by_xpath(xPath).click()
        except:
            print("FAILED")
            continue

        timeStarted = time.time()
        while True:
            try:
                imageElement = wd.find_element_by_xpath(
                    """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
                imageURL = imageElement.get_attribute('src')
            except:
                max_images += 1
                len_containers += 1
                print("failed")
                continue

            if imageURL != previewImageURL:
                break

            else:
                currentTime = time.time()

                if currentTime - timeStarted > max_waittime:
                    print("Timeout! Will download a lower resolution image and move onto the next one")
                    break
        try:
            download_image(imageURL, folder_name, filename, i)
            print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
        except:
            len_containers += 1
            max_images += 1
            print("Couldn't download an image %s, continuing downloading the next one" % i)


if __name__ == '__main__':
    wd = webdriver.Chrome(PATH)
    search_name = "cat"
    filename = ""
    folder_name = "cat_and_dog"
    n_of_images = 2
    waittime = 2
    search_url = GOOGLE_IMAGE + 'q=' + search_name.replace(' ', '+')

    get_and_download(wd, n_of_images, search_url, folder_name, filename,waittime)
    wd.quit()
