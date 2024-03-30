import requests
from pexelsapi.pexels import Pexels
from PIL import Image, ImageDraw, ImageFont
import uuid

pexels_key = "nuh uh"

def genQuote() -> tuple:
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()

    content = quote["content"]
    author = quote["author"]
    tag = quote["tags"][0]

    return content, author, tag

def genImg(tag):
    pexel = Pexels(pexels_key)
    search_photos = pexel.search_photos(query=tag, orientation='', size='', color='', locale='', page=1, per_page=1)
    id = search_photos['photos'][0]['id']
    get_photo = pexel.get_photo(id)
    response = requests.get(get_photo['src']['original'])
    filename = str(uuid.uuid4()) + ".jpg"

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print("Image saved successfully. ->", filename)
    else:
        print("Failed to fetch image:", response.status_code)
    return filename
    

def draw(filename: str, quote_content, quote_author):
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)

    quote_author = "- " + quote_author
    font_size_content = 150
    font_size_author = 75
    font_content = ImageFont.truetype("arial.ttf", font_size_content)
    font_author = ImageFont.truetype("arial.ttf", font_size_author)

    text_width_content, text_height_content = draw.textsize(quote_content, font=font_content)
    text_width_author, text_height_author = draw.textsize(quote_author, font=font_author)

    # Calculate position to center the text
    x_content = (image.width - text_width_content) / 2
    y_content = (image.height - text_height_content - text_height_author) / 2
    x_author = (image.width - text_width_author) / 2
    y_author = y_content + text_height_content

    # Draw the text on the image
    draw.text((x_content, y_content), quote_content, fill="white", font=font_content)
    draw.text((x_author, y_author), quote_author, fill="white", font=font_author)

    image.save(filename)

    print("Image with text saved successfully:", filename)
    


if __name__ == '__main__':
    new_quote = genQuote()
    file_name = genImg(new_quote[2])
    draw(filename=file_name, quote_content=new_quote[0], quote_author=new_quote[1])
    
