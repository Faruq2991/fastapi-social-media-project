from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# Create a Pydantic model for the request body
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='yourpassword', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as error:
    print("Database connection failed")
    print("Error:", error)



my_posts=[{"title": "My dreams.", "content": "My dreams to live a life in fear and obedience to Allah, take care of my family, set up a farm house and retire.", "id": 1}, {"title": "favorite books", "content": "['The Hobbits', 'Lord of the Rings']", "id": 2}]

def find_post(id):
    for postt in my_posts:
        if postt["id"] == id:
            return postt
            
def find_index(id):
    for i, pst in enumerate(my_posts):
        if pst["id"] == id:
            return i


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"date": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() #save to database
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not Found")
    return{"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found.")
    return {"data": updated_post}
    