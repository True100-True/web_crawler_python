import http.client as hc
import voya_class as vc
import sys
import re


class voya:

    def check_url(url):
        if url:
            bad_urls = vc.voya.nacitat(3)
            if url in bad_urls:
                print("url: {url}. Is in bad_urls")
                return "DOJEBANA"
            else:
                print("url is not in bad_urls fix it yourself if it doesnt work")
                return "DOBRA"
        else:
            return "DOJEBANA"

    @staticmethod
    def nacitat(to_scan):
        if to_scan == 1:
            with open("datas/crawled.txt") as crawled_data:
                crawled_datas = []
                for line in crawled_data:
                    crawled_datas.append(line.strip())  # Append each line to the list
                return crawled_datas  # Return the list

        if to_scan == 2:
            with open("datas/listed.txt") as listed_data:
                listed_urls = []
                for line in listed_data:
                    listed_urls.append(line.strip())  # Append each line to the list
                return listed_urls  # Return the list

        if to_scan == 3:
            with open("datas/bad_data.txt") as bad_data:
                bad_urls_list = []
                for line in bad_data:
                    bad_urls_list.append(line.strip())  # Append each line to the list
                return bad_urls_list  # Return the list
    
    @staticmethod
    def nacitanie_webu(url, thread, path="/"):
        try:
            # Determine the correct connection type (HTTP or HTTPS)
            if url.startswith("https://"):
                connection = hc.HTTPSConnection(url[8:])  # Remove "https://"
            else:
                connection = hc.HTTPConnection(url[7:])  # Remove "http://"

            connection.request("GET", path)
            response = connection.getresponse()

            if response.status == 200:
                print(f"voyager {thread} connected to: {url} successfully")
                return response.read().decode('utf-8')  # Return the HTML content
            else:
                print(f"{thread} cannot connect to: {url} with status code: {response.status}")
                return None
        except Exception as e:
            print(f"{thread} voya message: something went wrong! {e} (no data)")
            return "FAILED_LOAD_CONTENT"  # Return None for any exception

    @staticmethod
    def zapisat_data(urls, code):
        # Mapping the code to corresponding filenames
        files = {
            1: "datas/crawled.txt",
            2: "datas/listed.txt",
            3: "datas/bad_data.txt",
            12: "datas/crawled.txt",
            22: "datas/listed.txt",
            32: "datas/bad_data.txt"
        }

        # Get the file path based on the code
        file_path = files.get(code)
        if not file_path:  # If the code is invalid
            print(f"Error: Code {code} is not mapped to a file.")
            return None

        if code in {12, 22, 23}:
            # Writing all URLs to the file (overwrites content)
            try:
                with open(file_path, "w") as write_file:
                    print(f"Writing URLs to: {file_path}")
                    urls = write_file.read()
                    for word in urls:
                        if not word:  # Check for None or empty strings
                            print("Variable 'word' is invalid. Error code: 0049 ### Something was read badly ###")
                            return 1
                        print(f"Writing URL: {word}")
                        write_file.write(word + "\n")
            except FileNotFoundError:
                print(f"Error: Directory for {file_path} does not exist.")
                return None
        else:
            # Append mode or processing for single URL
            try:
                with open(file_path, "a") as write_file:
                    print(f"Appending to file: {file_path}")
                    for word in urls:
                        if not word:
                            print("Skipping invalid URL.")
                            continue
                        print(f"Appending URL: {word}")
                        write_file.write(word + "\n")
            except FileNotFoundError:
                print(f"Error: Path '{file_path}' is invalid.")
                return None



    @staticmethod
    def odstranit_polozku(url, code):
        if code == 1:
            with open("datas/crawled.txt", "w") as crawled:
                #load the crawled data
                content_lines = []
                with open("datas/crawled.txt", "r") as crawled1:
                    for line in crawled1:
                        line += content_lines
                if url in content_lines:
                    print("url was found in the crawled.txt deleting ... ")
                    crawled -= url
                else:
                    print("the url was not found in crawled.txt")
        elif code == 2:
            with open("datas/listed.txt", "w") as listed:
                #again load the content to the memory aka: content_lines
                content_lines = []
                with open("datas/listed.txt", "r") as listed1:
                    for line in listed1:
                        line += content_lines
                if url in content_lines:
                    listed -= url
        elif code == 3:
            pass
                
    @staticmethod
    def find_all_urls(html_content, deubug_content, archive_output):
        pattern = r'<a\s+href="([^"]+)"'
        urls = re.findall(pattern, html_content, re.IGNORECASE)
        if deubug_content:
            output = f"urls were find [debug_content]: {urls}"
            print(output)
            if archive_output:
                with open("datas/archive_data.txt", "w") as archiv:
                    archiv.write(output + "\n")
        return urls