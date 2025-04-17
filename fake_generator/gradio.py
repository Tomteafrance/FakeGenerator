import gradio as gr
import pandas as pd
import json
from fake_generator import FakeGenerator
from dotenv import load_dotenv

load_dotenv()

class GradioInterface:
    def __init__(self):
        self.columns = []
        self.max_columns = 20
        
    def add_column_ui(self):
        """Add control for new column"""
        with gr.Box():
            with gr.Row():
                column_name = gr.Textbox(label="Nom de la colonne")
                category = gr.Textbox(label="Catégorie Faker")
                data_type = gr.Dropdown(
                    ["str", "int", "float", "datetime", "bool"],
                    label="Type de données"
                )
                unique = gr.Checkbox(label="Valeurs uniques")
        
        return [column_name, category, data_type, unique]

    def build_schema(self, *args):
        """ Construct schema from user input """
        schema = []
        for i in range(0, len(args), 4):
            if i+3 >= len(args):
                break
                
            schema.append({
                "column": args[i],
                "category": args[i+1],
                "type": args[i+2] if args[i+2] else None,
                "unique": args[i+3]
            })
        return schema

    def generate_data(self, num_rows, *inputs):
        """Generate Data & Return Dataframe """
        try:
            schema = self.build_schema(*inputs)
            generator = FakeGenerator(schema)
            df = generator.generate_dataframe(num_rows)
            return df, gr.update(visible=True), df.to_csv(index=False)
        except Exception as e:
            raise gr.Error(f"Erreur de génération : {str(e)}")

    def launch(self):
        """ Launch Gradio Interface"""
        with gr.Blocks(title="Générateur de données synthétiques") as demo:
            gr.Markdown("# 🧪 Fake Data Generator")
            
            with gr.Row():
                num_rows = gr.Slider(1, 10000, value=100, label="Nombre de lignes")
                add_btn = gr.Button("➕ Ajouter une colonne")
            
            columns_ui = []
            initial_controls = self.add_column_ui()
            columns_ui.extend(initial_controls)
            
            add_btn.click(
                fn=self.add_column_ui,
                outputs=initial_controls,
                queue=False
            )
            
            generate_btn = gr.Button("🚀 Générer les données", variant="primary")
            
            with gr.Row():
                output_table = gr.Dataframe(label="Données générées")
                download_btn = gr.Button(
                    "💾 Download CSV",
                    visible=False,
                    link=lambda df: (df.to_csv(index=False), "data.csv")
                )
            
            generate_btn.click(
                fn=self.generate_data,
                inputs=[num_rows, *columns_ui],
                outputs=[output_table, download_btn]
            )

        demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    interface = GradioInterface()
    interface.launch()