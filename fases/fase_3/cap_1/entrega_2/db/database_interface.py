from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute_query(self, query, params=None):
        pass

    @abstractmethod
    def fetch_all(self, query, params=None):
        pass

    @abstractmethod
    def fetch_one(self, query, params=None):
        pass

    @abstractmethod
    def insert(self, table, data):
        pass

    @abstractmethod
    def update(self, table, data, condition):
        pass

    @abstractmethod
    def delete(self, table, condition):
        pass