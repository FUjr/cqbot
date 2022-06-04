def urlparse(str : str):
   return  str.replace('%','%25').replace(' ','%20').replace('"','%22').replace('#','%23').replace('&','%26').replace('(','%28').replace(')','%29').replace('+','%2B').replace(',','%2C').replace('/','%2F').replace(':','%3A').replace(';','%3B').replace('<','%3C').replace('=','%3D').replace('>','%3E').replace('?','%3F').replace('@','%4o').replace('|','%7C').replace('\\','%5C')
   
