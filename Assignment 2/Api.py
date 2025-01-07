import tkinter as tk # importing tkinter
from tkinter import ttk # importing tkinter widgets
from PIL import Image, ImageTk #Importing pillow for images
import requests #Importing requests to access external APIs
import io #IMporting IO to read the binary streams of data provided by the API


class MealAPI:
    BASE_URL = "https://www.themealdb.com/api/json/v1/1" #Entering the url to access the API

    @staticmethod
    #Fetching the meal data from the API based on what the user has searched
    def search_meal_by_name(name):
        response = requests.get(f"{MealAPI.BASE_URL}/search.php?s={name}")
        return response.json() if response.status_code == 200 else None


    @staticmethod
    #Fetching the meal data randomly
    def get_random_meal():
        response = requests.get(f"{MealAPI.BASE_URL}/random.php")
        return response.json() if response.status_code == 200 else None

    @staticmethod
    #Fetching the meal data based on the category the user has selected
    def get_meal_categories():
        response = requests.get(f"{MealAPI.BASE_URL}/list.php?c=list")
        return response.json() if response.status_code == 200 else None


class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Recipe App") #Setting the app title
        self.root.geometry("800x600")  #Setting APP size
        self.root.configure(bg="#FAF3E0")  #Setting the color to a light yellow

        #Creating the GUI
        self.create_main_gui()

    def create_main_gui(self):
        #Creating the app title
        self.title_label = ttk.Label(
            self.root,
            text="Meal Recipe",
            font=("Comic Sans MS", 30, "bold"),
            background="#FAF3E0"
        )
        self.title_label.pack(pady=10)

        #Creating a search window inside the root window
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        #Creating a text entry window inside the search window
        self.search_entry = ttk.Entry(search_frame, font=("Comic Sans MS", 14), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        #Creating a search button inside the search window
        self.search_button = ttk.Button(search_frame, text="Search Meal", command=self.search_meal)
        self.search_button.pack(side=tk.LEFT, padx=5)

        #Creating a random meal button inside the main window
        self.random_button = ttk.Button(self.root, text="Get Random Meal", command=self.get_random_meal)
        self.random_button.pack(pady=10)

        #Creating a category button and drop down inside the main window
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            self.root,
            textvariable=self.category_var,
            state="readonly",
            font=("Comic Sans MS", 12)
        )
        self.category_combobox.pack(pady=10)
        self.load_categories()

        self.category_combobox.bind("<<ComboboxSelected>>", self.search_by_category)

        #Creating a image display for the meals
        self.image_label = tk.Label(self.root, bg="#FAF3E0")
        self.image_label.pack(pady=10)

        #Creating a window for the result in the main window
        result_frame = ttk.Frame(self.root)  # Create a frame to hold text and scrollbar
        result_frame.pack(pady=10)

        #Customizing the text inside the result window
        self.result_text = tk.Text(
            result_frame,
            wrap=tk.WORD,
            font=("Comic Sans MS", 12),
            height=15,
            width=70,
            bg="#FFF7E6",
            relief=tk.FLAT
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #Adding a vertical scroll bar in the result window for easier navigation
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #Connecting the scrollbar with the result window
        self.result_text.config(yscrollcommand=result_scrollbar.set)


    def load_categories(self):
        #Getting all the categories from the API
        categories = MealAPI.get_meal_categories()
        #Writing an if statement to check if the response is correct
        if categories and categories['meals']:
            #Extracting all the categories from meals
            category_names = [meal['strCategory'] for meal in categories['meals']]
            #Appending the values in combobox to category_names
            self.category_combobox['values'] = category_names
        else:
            #if there are no values setting the list as empty
            self.category_combobox['values'] = []

    #Adding functionality to the search window
    def search_meal(self):
        #Getting the meal name from the search window
        meal_name = self.search_entry.get()
        #Writing an if statement that searches the API for the meal searched by user and the displays it
        if meal_name:
            data = MealAPI.search_meal_by_name(meal_name)
            self.display_meal(data)

    #Setting the random meal button
    def get_random_meal(self):
        #Getting a random meal from the API
        data = MealAPI.get_random_meal()
        #Displaying the random meal
        self.display_meal(data)

    def search_by_category(self, event=None):
        #getting the selected category from the list
        selected_category = self.category_var.get()
        #writing an if statement to search the api for the selected category and the displaying it
        if selected_category:
            data = MealAPI.search_meal_by_name(selected_category)
            self.display_meal(data)

    def display_meal(self, data):
        #Checking if the data contains the meal information
        if data and data['meals']:
            #getting the first meal from meals
            meal = data['meals'][0]
            #getting information about the meal
            meal_name = meal['strMeal']
            meal_category = meal['strCategory']
            meal_area = meal['strArea']
            meal_instructions = meal['strInstructions']

            #Displaying the image of the meal
            image_url = meal['strMealThumb'] #getting image URL
            image_data = requests.get(image_url).content #Getting the image from the URL
            image = Image.open(io.BytesIO(image_data)) #Opening the image in binary data form
            image = image.resize((300, 200), Image.Resampling.LANCZOS) #Resizing the image
            meal_image = ImageTk.PhotoImage(image) #Converting the image back to a useable format

            #Updating the label to display image
            self.image_label.config(image=meal_image)
            self.image_label.image = meal_image

            #Displaying all the meal details in the result window 
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Meal Name: {meal_name}\n")
            self.result_text.insert(tk.END, f"Category: {meal_category}\n")
            self.result_text.insert(tk.END, f"Area: {meal_area}\n")
            self.result_text.insert(tk.END, f"Instructions: {meal_instructions}\n")

            #Adding a section called ingredients in the result window
            self.result_text.insert(tk.END, "\nIngredients:\n")
            for i in range(1, 21): #Going through the whole ingredient and measure pair
                ingredient = meal.get(f"strIngredient{i}") #Getting the name of the ingredients
                measure = meal.get(f"strMeasure{i}") #Getting the measure of the ingredients
                if ingredient and ingredient.strip(): #Checking if ingredient is empty or not
                    self.result_text.insert(tk.END, f"- {ingredient}: {measure}\n") #Adding the ingredient and measures to the result window
        else:
            self.result_text.delete(1.0, tk.END) #Clearing the result window if nothing is found
            self.result_text.insert(tk.END, "No meal found.") #Displaying the error message

#Creating the splash screen to run before the actual app
class SplashScreen:
    def __init__(self, root, callback):
        self.root = root #Calling the main root function
        self.callback = callback #using the callback function to launch the app

        # Create a Toplevel window for the splash screen
        self.splash = tk.Toplevel(root) #Creating an individual window for the splash screen
        self.splash.overrideredirect(True)  #Removing the title bar
        self.splash.geometry("800x600+300+100")  #Setting the size for the splash screen

        # Load the splash image
        image = Image.open("meal_app.png")  #SPecifying the path for my image used in the splash screen
        image = image.resize((800, 600), Image.Resampling.LANCZOS)  #Resizing the image to fit in the app
        self.meal_app = ImageTk.PhotoImage(image) #Coverting the image to tkinter compatible format

        #Ceating a label to display the image
        splash_label = tk.Label(self.splash, image=self.meal_app)
        splash_label.pack() #Packing the label to fill the entire window

        #Setting up the splash screen to close after 5 seconds
        self.splash.after(5000, self.close_splash)

    def close_splash(self):
        self.splash.destroy()  #Closing the splash screen window
        self.callback()  #Calling the callback function to launch the main app

# Main function
def main():
    root = tk.Tk()
    root.withdraw()

    # Show splash screen
    def show_main_app():
        root.deiconify()
        MealApp(root)

    SplashScreen(root, show_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()
