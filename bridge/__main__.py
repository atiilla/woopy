
import os

from bridge.category.woo_category_create_api import WooCategoryCreateApi


def main():
    """
    Main function
    """
    app = WooCategoryCreateApi(__name__)
    app.run(
        host=os.getenv("WOOPY_BRIDGE_HOST", "0.0.0.0"),
        port=int(os.getenv("WOOPY_BRIDGE_PORT", "5000"))
    )


if __name__ == "__main__":
    main()
    
