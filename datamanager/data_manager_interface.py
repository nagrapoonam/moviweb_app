from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self,user_name):
        pass

    @abstractmethod
    def add_movie(self,user_name,movie_name,director,year,rating):
        pass

    @abstractmethod
    def update_movie(self,user_name,movie_name,director,year,rating):
        pass

    @abstractmethod
    def delete_movie(self,movie_name):
        pass

    @abstractmethod
    def get_movie(self,user_id, movie_id):
        pass

    @abstractmethod
    def get_movie_name(self, movie_id):
        pass
    @abstractmethod
    def get_user_name(self, user_id):
        pass
