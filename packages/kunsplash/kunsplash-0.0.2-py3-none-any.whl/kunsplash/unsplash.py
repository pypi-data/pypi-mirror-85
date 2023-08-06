# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Optional
from urllib.parse import quote

# Pip
from kcu import request

# Local
from .models.unsplash_image import UnsplashImage

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: Unsplash ------------------------------------------------------------ #

class Unsplash:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def search(cls, term: str, max: int = 30, user_agent: Optional[str] = None, debug: bool = False) -> List[UnsplashImage]:
        return cls.__get_images('https://unsplash.com/napi/search/photos?query={}&xp='.format(quote(term)), max, 'results', user_agent, debug)

    @classmethod
    def explore(cls, category: str, max: int = 30, user_agent: Optional[str] = None, debug: bool = False) -> List[UnsplashImage]:
        return cls.__get_images('https://unsplash.com/napi/landing_pages/{}'.format(category.strip('/')), max, 'photos', user_agent, debug)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __get_images(base_url: str, max: int, json_key: str, user_agent: Optional[str], debug: bool) -> List[UnsplashImage]:
        images = []

        base_url += ('?' if '?' not in base_url else '&') + 'per_page=30&page='
        page = 0

        while len(images) < max:
            page += 1

            try:
                url = base_url + str(page)
                elements = request.get(url, user_agent=user_agent, debug=debug).json()[json_key]

                if len(elements) == 0:
                    return images

                for e in elements:
                    try:
                        images.append(UnsplashImage(e))
                    except Exception as e:
                        if debug:
                            print(e)
                    
                    if len(images) >= max:
                        return images
            except Exception as e:
                if debug:
                    print(e)

                return images

        return images


# ---------------------------------------------------------------------------------------------------------------------------------------- #