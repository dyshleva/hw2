# HW2
## TOKEN-BASED AUTH
Client service use token-based authentication. To communicate with you need to provide authorization header with specidic token. Then, client sevice checks whether provided token matches with some code-defined token. If tokens are the same, you will have access, if they are different, you will not have access.

## START APP
To start app, you need firstly install ```docker``` and ```docker compose```, then you can run ```start.bash``` script and it will create you three containers where three services will be located.

You can interact with app on address **http://127.0.0.1:8000**.

## USAGE (using CLI ```curl```)
1. Run app
![run app](./img/run.png)
2. Get all movies
![movies](./img/read.png)
3. Add new movie and check it existence
![new mpovie](./img/write.png)
4. Get description for film with id = 3
![mpvie desc](./img/desc.png)

## REQUEST FLOW
1. **/movies/read**: user -> client -> db -> cliebt -> user
2. **/movies/write**: user -> client -> db -> cliebt -> user
3. **/description?id=value**: user -> client -> business -> db -> business -> client -> user

## ADDITIONAL
- Auth token: krutyitoken (you will also need to create .env file inside project dir)
- Token for LLM must be created here https://openrouter.ai/