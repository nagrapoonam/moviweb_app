from abc import ABC, abstractmethod
#abstract base classes and abstract methods.
class DataManagerInterface(ABC):
    """abstract base class,inherits from the ABC class.
        Declaring following abstract methods
    """
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_user(self,user_name, password):
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
    def get_user(self, user_id):
        pass
