from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):

    title: str
    content: str
    published: bool = True
    Rating: Optional[int]



my_posts = [{"title": "",
        "content": "They are just sereen",
        "id": 2}, 
        {"title": "ejhejfj",
        "content": "They not just sereen",
        "id": 3},
        {
            "title": "jenfjdhbfjf",
            "content": "plain english letters",
            "id": 4


        }
        
        
        ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p







@app.get("/")
async def root():
    return {"message": "Mad"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}




@app.get("posts/latest")
async def get_latest_post():
   post =  my_posts[len(my_posts) - 1]
   return {"detail": post}
   



@app.get("/posts/{id}")
async def find_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")


        




    return {"post_detail": post}






@app.post("/posts")
async def create_post(post: Post):

    post_dict = post.dict()

    my_posts.append(post.dict)

    return {"data": post_dict}



@app.delete("/posts/{id}")
async def delete_post(id: int):

    for p in my_posts:
        if p["id"] == id:
            temp_index = my_posts.index(p)

            if temp_index == None:
                raise HTTPException(status_code=status.HTT_NOT_FOUND, detail=f"Post with id: {id} not found")




            my_posts.pop(temp_index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post:Post):

    for p in my_posts:
        if p["id"] == id:
            index = my_posts.index(p)

            posts_dict = post.dict()
            posts_dict["id"] = id
            my_posts[index] = posts_dict

            return {"data": posts_dict}
            






    







