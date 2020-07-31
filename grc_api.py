import json
import time
import goodreads_api_client as gr

client = gr.Client(developer_key='YOUR DEVELOPER KEY HERE')
book_id = 1
book_list = []
book_titles = set()
starter_keys = [
    'id', 'title', 'publication_date', 'isbn', 'isbn13', 
    'publication_year', 'publication_month', 'publication_day', 
    'publisher', 'language_code', 'average_rating', 'num_pages', 'format'
    ]

def get_books_data(client, book_id, book_titles, books_list):
    while(book_id < 50001):
        try:
            # A big dump of information
            data = client.Book.show(book_id)
            book_dict = {k:v for k, v in data.items() if k in starter_keys}
            
            # Indexing from built-in book.work returns reivew count for ALL editions
            # book.text_reviews_count returns review count for particular edition
            book_dict['rating_dist'] = data['work']['rating_dist']
            book_dict['review_count'] = data['work']['text_reviews_count']['#text']  

            # Get only the 5 most popular "shelves" (genres)
            genre_list = data['popular_shelves']['shelf']
            book_dict['genres'] = [genre['@name'] for genre in genre_list[:5]]
            
            try:
                book_dict['author'] = data['authors']['author']['name']
            except:
                book_dict['author'] = data['authors']['author'][0]['name']
            finally:
                pass
            
            # Prevent duplicates of same book with different goodreads ids
            if book_dict['title'] not in book_titles:
                book_list.append(book_dict)
                book_titles.add(book_dict['title'])
                yield book_dict
                
            # print(f'Book {book_id} read.')          # Used to test
            book_id += 1
            time.sleep(1)

        except:
            # print(f"Can't read book {book_id}")     # Used to test
            book_id += 1
            time.sleep(1)

for book_dict in get_books_data(client, book_id, book_titles, book_list):
    book_data_js = json.dumps(book_dict, indent=4)
    with open('book_data.json', 'a') as file:
        file.write(book_data_js + ',')