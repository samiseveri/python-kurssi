from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, List

class BaseItem(ABC):
    """Abstract base class for all item types"""
    def __init__(self, title: str, year: int):
        self._title = title
        self._year = self._validate_year(year)
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def year(self) -> int:
        return self._year
    
    @staticmethod
    def _validate_year(year) -> int:
        """Validate and convert year input"""
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if not (0 <= year_int <= current_year + 2):  # Allow some future items
                raise ValueError(f"Year must be between 0 and {current_year + 2}")
            return year_int
        except ValueError:
            raise ValueError("Year must be a valid integer")
    
    @abstractmethod
    def print_description(self) -> str:
        """Returns a formatted description of the item"""
        pass

class Book(BaseItem):
    """Class representing a book item"""
    def __init__(self, title: str, author: str, year: int):
        super().__init__(title, year)
        self._author = author
    
    @property
    def author(self) -> str:
        return self._author
    
    def print_description(self) -> str:
        return f"Book: {self.title} by {self.author} ({self.year})"

class Music(BaseItem):
    """Class representing a music item"""
    def __init__(self, title: str, artist: str, year: int):
        super().__init__(title, year)
        self._artist = artist
    
    @property
    def artist(self) -> str:
        return self._artist
    
    def print_description(self) -> str:
        return f"Music: {self.title} by {self.artist} ({self.year})"

class Movie(BaseItem):
    """Class representing a movie item"""
    def __init__(self, title: str, director: str, year: int):
        super().__init__(title, year)
        self._director = director
    
    @property
    def director(self) -> str:
        return self._director
    
    def print_description(self) -> str:
        return f"Movie: {self.title} directed by {self.director} ({self.year})"

class Game(BaseItem):
    """Class representing a computer game item"""
    def __init__(self, title: str, developer: str, year: int):
        super().__init__(title, year)
        self._developer = developer
    
    @property
    def developer(self) -> str:
        return self._developer
    
    def print_description(self) -> str:
        return f"Game: {self.title} developed by {self.developer} ({self.year})"

class ItemBox:
    """Container class for managing collections of items"""
    def __init__(self):
        self._items: Dict[str, BaseItem] = {}
    
    def add_item(self, key: str, item: BaseItem) -> None:
        """Add an item to the box with the given key"""
        if key in self._items:
            raise ValueError(f"Item with key '{key}' already exists")
        self._items[key] = item
    
    def remove_item(self, key: str) -> None:
        """Remove an item from the box"""
        if key not in self._items:
            raise ValueError(f"No item found with key '{key}'")
        del self._items[key]
    
    def replace_item(self, old_key: str, new_key: str, new_item: BaseItem) -> None:
        """Replace an existing item with a new one"""
        if old_key not in self._items:
            raise ValueError(f"No item found with key '{old_key}'")
        del self._items[old_key]
        self._items[new_key] = new_item
    
    def get_descriptions(self) -> List[str]:
        """Get descriptions for all items in the box"""
        return [item.print_description() for item in self._items.values()]
    
    def update_item(self, key: str, **kwargs) -> None:
        """Update properties of an existing item"""
        if key not in self._items:
            raise ValueError(f"No item found with key '{key}'")
        
        item = self._items[key]
        
        if 'title' in kwargs:
            item._title = kwargs['title']
        if 'year' in kwargs:
            item._year = BaseItem._validate_year(kwargs['year'])
        
        # Type-specific updates
        if isinstance(item, Book) and 'author' in kwargs:
            item._author = kwargs['author']
        elif isinstance(item, Music) and 'artist' in kwargs:
            item._artist = kwargs['artist']
        elif isinstance(item, Movie) and 'director' in kwargs:
            item._director = kwargs['director']
        elif isinstance(item, Game) and 'developer' in kwargs:
            item._developer = kwargs['developer']

class ItemManager:
    """Main application class for managing items through a user interface"""
    def __init__(self):
        self._box = ItemBox()
        self._log: List[str] = []
    
    def _log_action(self, action: str) -> None:
        """Log an action to the internal log"""
        self._log.append(action)
    
    def _save_log(self) -> None:
        """Save the action log to a file"""
        with open("item_log.txt", "w") as file:
            for entry in self._log:
                file.write(entry + "\n")
    
    def _create_item(self) -> Optional[BaseItem]:
        """Create a new item based on user input"""
        print("\nSelect item type:")
        print("1. Book")
        print("2. Music")
        print("3. Movie")
        print("4. Game")
        
        item_type = input("Enter item type (1-4): ")
        title = input("Enter title: ")
        year = input("Enter year: ")
        
        try:
            year_int = BaseItem._validate_year(year)
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
        if item_type == "1":
            author = input("Enter author: ")
            if not author:
                print("Error: Author is required for books")
                return None
            return Book(title, author, year_int)
        elif item_type == "2":
            artist = input("Enter artist: ")
            if not artist:
                print("Error: Artist is required for music")
                return None
            return Music(title, artist, year_int)
        elif item_type == "3":
            director = input("Enter director: ")
            if not director:
                print("Error: Director is required for movies")
                return None
            return Movie(title, director, year_int)
        elif item_type == "4":
            developer = input("Enter developer: ")
            if not developer:
                print("Error: Developer is required for games")
                return None
            return Game(title, developer, year_int)
        else:
            print("Invalid item type selected")
            return None
    
    def run(self) -> None:
        """Run the main application loop"""
        while True:
            print("\nItem Management System")
            print("1. Add item")
            print("2. Remove item")
            print("3. Replace item")
            print("4. View all items")
            print("5. Update item")
            print("6. Exit")
            
            choice = input("Select an option (1-6): ")
            
            if choice == "1":
                item = self._create_item()
                if item:
                    key = input("Enter a unique key for this item: ")
                    try:
                        self._box.add_item(key, item)
                        self._log_action(f"Added item: {key} - {item.print_description()}")
                        print("Item added successfully")
                    except ValueError as e:
                        print(f"Error: {e}")
            
            elif choice == "2":
                key = input("Enter key of item to remove: ")
                try:
                    self._box.remove_item(key)
                    self._log_action(f"Removed item: {key}")
                    print("Item removed successfully")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == "3":
                old_key = input("Enter key of item to replace: ")
                print("Create the new replacement item:")
                new_item = self._create_item()
                if new_item:
                    new_key = input("Enter new key for the item: ")
                    try:
                        self._box.replace_item(old_key, new_key, new_item)
                        self._log_action(f"Replaced item: {old_key} with {new_key} - {new_item.print_description()}")
                        print("Item replaced successfully")
                    except ValueError as e:
                        print(f"Error: {e}")
            
            elif choice == "4":
                print("\nCurrent Items:")
                for desc in self._box.get_descriptions():
                    print(f"- {desc}")
            
            elif choice == "5":
                key = input("Enter key of item to update: ")
                print("Enter new values (leave blank to keep current):")
                
                try:
                    item = self._box._items[key]  # Access protected member for update
                    print(f"Current title: {item.title}")
                    new_title = input("New title: ") or None
                    
                    print(f"Current year: {item.year}")
                    new_year = input("New year: ") or None
                    
                    update_kwargs = {}
                    if new_title:
                        update_kwargs['title'] = new_title
                    if new_year:
                        update_kwargs['year'] = new_year
                    
                    if isinstance(item, Book):
                        print(f"Current author: {item.author}")
                        new_author = input("New author: ") or None
                        if new_author:
                            update_kwargs['author'] = new_author
                    elif isinstance(item, Music):
                        print(f"Current artist: {item.artist}")
                        new_artist = input("New artist: ") or None
                        if new_artist:
                            update_kwargs['artist'] = new_artist
                    elif isinstance(item, Movie):
                        print(f"Current director: {item.director}")
                        new_director = input("New director: ") or None
                        if new_director:
                            update_kwargs['director'] = new_director
                    elif isinstance(item, Game):
                        print(f"Current developer: {item.developer}")
                        new_developer = input("New developer: ") or None
                        if new_developer:
                            update_kwargs['developer'] = new_developer
                    
                    self._box.update_item(key, **update_kwargs)
                    self._log_action(f"Updated item: {key} - {item.print_description()}")
                    print("Item updated successfully")
                
                except KeyError:
                    print("Error: No item found with that key")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == "6":
                self._save_log()
                print("Log saved. Exiting...")
                break
            
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    manager = ItemManager()
    manager.run()