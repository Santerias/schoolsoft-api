import schoolsoft
from dotenv import load_dotenv
from os import getenv

if __name__ == "__main__":
    load_dotenv()

    USER = getenv("USER")
    PASS = getenv("PASS")
    SCHOOL = getenv("SCHOOL")

    api = schoolsoft.Api(USER, PASS, SCHOOL)
    print(api.get_current_lesson())
