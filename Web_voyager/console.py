import voya_class as vc
import general as g

""""
url = "https://www.example.com"  # Just the domain name (host)
thread = 1
path = "/"  # Path you want to scan
option = 0

# Fetch the HTML content from the website
html_content = voya_class.voya.nacitanie_webu(url, thread, path)

if html_content:
    # Extract all URLs from the HTML content
    urls = voya_class.voya.find_all_urls(html_content)

    for found_url in urls:
        if found_url == "#" or found_url == "javascript:" or found_url == "javascript:void();" or found_url == "javascript:;" or found_url == "/?ref=tlogo":
            continue
        else:
            if option == 1:
                print("URL: ", found_url)
            
else:
    print("Failed to retrieve the HTML content.")
"""

#project will be realsted

def skip_url(url, thread, message=None):
    if message == None:
        return 
    elif message == "DOJEBANA":
        pass
    bad_urls = vc.voya.nacitat(3)
    print(f"next_url for voyager {thread}")
    if url in bad_urls:
        print("url is in bad_urls")
        listed = vc.voya.nacitat(2)
        if url in listed:
            vc.voya.odstranit_polozku(url, 2)
    else:
        vc.voya.zapisat_data(url, 3)
        listed = vc.voya.nacitat(2)
        if url in listed:
            vc.voya.odstranit_polozku(url, 2)
        
def pick_a_url(url, thread):
    listed = vc.voya.nacitat(2)
    if url in listed:
        vc.voya.odstranit_polozku(url, 2)
        vc.voya.zapisat_data(url, 1)
    #pick the url
    return listed[0]

def main_loop(thread):
    try:
        while True:
            listed_data = vc.voya.nacitat(2)
            if listed_data == [] or listed_data == None:
                print("error code: 0045 ### error while loading a file ###")
                return 1
            first_url = listed_data[0]
            web = vc.voya.nacitanie_webu(first_url, thread)
            if web == "FAILED_LOAD_CONTENT":
                first_url = skip_url(first_url, thread, "DOJEBANA")

            #debug !
            urls = vc.voya.find_all_urls(web, deubug_content=True, archive_output=True)
            print(urls)
            #debug !

            #funguje modifikovat aby aj precital robots.txt update 1.5
            counter1 = 0
            counter2 = 0
            for url in urls: #filter not good urls
                counter1 += 1
                if url == "#" or url.find("#"):
                    counter2 += 1
                    continue
                else:
                    vc.voya.zapisat_data(urls, 22) #write discovered data to listed.txt doesnt work why ????
            print(f"filtering urls that are specialy ... from {counter1} were filtered {counter2}") 
            #funguje

            #funguje 
            vc.voya.zapisat_data(first_url, 1) # write data to crawled.txt 
            vc.voya.odstranit_polozku(first_url, 2) #delete data from listed.txt
            #funguje

    except KeyboardInterrupt:
        print("ending program ... ")

main_loop(thread=1)

#future update 2.0
def console():
    pass
#future update 2.0

####### TEST FUNCTIONS #######
def debug(url):
    request = vc.voya.nacitanie_webu(url, thread=1, path="/")
    output = vc.voya.find_all_urls(request, deubug_content=True)
    vc.voya.zapisat_data(output, 2)
#debug(url="https://www.sme.sk")