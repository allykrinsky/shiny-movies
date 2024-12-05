from shiny import App, reactive, render, ui
import pandas as pd
import random

# Define UI
app_ui = ui.page_fluid(
    ui.h1("Movie Picker", class_="text-center mb-4"),
    
    # Input Card
    ui.card(
        ui.card_header("Add New Movie"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_text("text_input", "Enter Movie Title", placeholder="Type something..."),
                ui.input_action_button("add_button", "Add to List", class_="btn-primary btn-lg w-100 mb-2"),
                ui.input_action_button("clear_button", "Clear All Movies", class_="btn-danger btn-lg w-100"),
                width="300px"
            ),
            ui.card(
                ui.card_header("Movie List"),
                ui.output_table("table_output"),
            )
        )
    ),
    
    # Random Picker Card
    ui.card(
        ui.card_header("Random Movie Picker"),
        ui.div(
            ui.input_action_button(
                "random_button", 
                "Pick Random Movie", 
                class_="btn-success btn-lg"
            ),
            ui.div(
                ui.output_text("random_movie"),
                class_="h3 mt-3"
            ),
            class_="d-flex flex-column align-items-center p-3"
        )
    )
)

# Define server logic
def server(input, output, session):
    # Create a reactive value to store the list
    data = reactive.value([])

    @reactive.effect
    @reactive.event(input.add_button)
    def add_to_list():
        if input.text_input().strip():  # Only add non-empty entries
            current_list = data.get()
            new_entry = {
                "Movie Title": input.text_input()
            }
            data.set(current_list + [new_entry])
            ui.update_text("text_input", value="")  # Clear input after adding

    @reactive.effect
    @reactive.event(input.clear_button)
    def clear_list():
        data.set([])

    @output
    @render.table
    def table_output():
        current_list = data.get()
        if not current_list:
            return pd.DataFrame(columns=["Movie Title"])
        return pd.DataFrame(current_list)
    
    @output
    @render.text
    @reactive.event(input.random_button)
    def random_movie():
        current_list = data.get()
        if not current_list:
            return "📽️ No movies in the list yet!"
        random_choice = random.choice(current_list)
        return f"🎬 Selected Movie: {random_choice['Movie Title']}"

# Create the app
app = App(app_ui, server)
