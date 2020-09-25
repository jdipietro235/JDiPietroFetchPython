
# Justin DiPietro
# jdipietro235@gmail.com
# 2020-9-25

# Importing http for hosting
from http.server import BaseHTTPRequestHandler, HTTPServer
# Importing CGI to handle form data
import cgi
# Imporing re for regex search function used in checking if the emails are valid
import re 


class web_server(BaseHTTPRequestHandler):
    # Defines what to do when client requests the main page
    def do_GET(self):
        # if the url the user entered it just localhost:8080, send them the index page
        if self.path == '/':
            self.path = '/index.html'
        try:
            #Reading the file
            fileToOpen = open(self.path[1:]).read()
            self.send_response(200)
        except:
            # if the index page can't be found, just send them an error
            file_to_open = "File not found"
            self.send_response(404)
        #self.send_header('Content-Type', 'text/html')
        self.end_headers()
        # Send over either the index page or the error message
        self.wfile.write(bytes(fileToOpen, 'utf-8'))
    def do_POST(self):
        # Get the form data from the index page
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],
                     })
        formString = form.getvalue('addresses')
        # Replace any spaces with commas, that way the user can separate inputs with either 
        formString = formString.replace(' ', ',')
        # Split the form data into a list of strings
        addressList = formString.split(',')
        # Turn the int returned by countAddresses into a string
        addrCount = str(countAddresses(addressList))
        stringToDisplay = 'You entered ' + addrCount + ' distinct email addresses'
        # Send the response to the user
        self.wfile.write(bytes(stringToDisplay, 'utf-8'))

def countAddresses(addressList):
    # List for saving each distinct email address
    outputList = []
    print(addressList)
    for email in addressList:
        # The regex function checks to see if the string is a legitimate email
        if (re.search('^[a-z0-9]+[\._]?[a-z0-9\+]+[@]\w+[.]\w{2,3}$', email)):
            #then get rid of any '.' before the host name
            email = email[0:email.find('@')].replace('.', '') + email[email.find('@'):len(email)]
            if '+' in email:
                #remove everything between the '+' and the start of the host (@) including the '+'
                email = email[0:email.find('+')] + email[email.find('@'):len(email)]
            # if the 'true' email address we've just arrived at has not already been added to the list
            if email not in outputList:
                # Then add it to the list
                outputList.append(email)
    #return the number of true email addresses to the list
    return len(outputList)
            


# Start up the server and keep running it until it stops
httpd = HTTPServer(('localhost', 8080), web_server)
print('JDiPietro Fetch Python Server Starting')
httpd.serve_forever()
