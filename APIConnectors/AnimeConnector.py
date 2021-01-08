import requests

class AnimeConnector:
    @staticmethod
    def Search(title: str ):
        # Here we define our query as a multi-line string
        query = '''
        query ($title: String) {
            Page (perPage: 10){
                media (search: $title, type: ANIME, status: RELEASING) { 
                    id
                    title {
                      romaji
                      english
                    } 
                  }
                }
            }
        '''

        # Define our query variables and values that will be used in the query request
        variables = {
                "title": title
        }

        url = 'https://graphql.anilist.co'

        # Make the HTTP Api request and return
        return requests.post(url, json={'query': query, 'variables': variables}).json()

    @staticmethod
    def getepisodesbyid( id: int):
        # Here we define our query as a multi-line string
        query = '''
        query ($id: Int) {
            Media (id: $id, type: ANIME) { 
                id
                status
                title {
                  romaji
                  english
                } 
                airingSchedule
                {
                    nodes{
                        id
                        episode
                        timeUntilAiring
                        airingAt
                    }
                }
              }
            }
           '''
        # Define our query variables and values that will be used in the query request
        variables = {
            "id": id
        }

        url = 'https://graphql.anilist.co'

        # Make the HTTP Api request and return
        return requests.post(url, json={'query': query, 'variables': variables}).json()

