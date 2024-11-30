import panel as pn
from src.config import Settings
from src.app import MultiModalChatApp

def main():
    # Load settings
    settings = Settings.load_from_env()
    
    # Create application
    app = MultiModalChatApp(settings)
    if not app.initialize():
        raise RuntimeError("Failed to initialize application")
        
    # Create and serve dashboard
    dashboard = app.create_dashboard()
    pn.serve(dashboard, port=5006)

if __name__ == "__main__":
    main() 