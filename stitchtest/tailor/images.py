class IMAGE:
    def __init__(self):
        # Dictionary mapping garment names to their image paths
        self.image_paths = {
            'shirt': r"C:\Users\potup\Documents\stitchtest\tailor\static\shirt.jpg",
            'trousers': r"C:\Users\potup\Documents\stitchtest\tailor\static\trouser.jpg",
            'blazer': r"C:\Users\potup\Documents\stitchtest\tailor\static\blazer.jpg",
            'blouse': r"C:\Users\potup\Documents\stitchtest\tailor\static\blouse.jpg",
            'custom': r"C:\Users\potup\Documents\stitchtest\tailor\static\custom.jpg",
            'kurta_men': r"C:\Users\potup\Documents\stitchtest\tailor\static\kurta_men.jpg",
            'kurta_women': r"C:\Users\potup\Documents\stitchtest\tailor\static\kurta_women.jpg",
            'minor_stitches': r"C:\Users\potup\Documents\stitchtest\tailor\static\minor.jpg",
            'saree': r"C:\Users\potup\Documents\stitchtest\tailor\static\saree.jpg",
            'dhoti': r"C:\Users\potup\Documents\stitchtest\tailor\static\dhoti.jpg",
        }

    def image_to_binary(self, image_path):
        """Helper function to convert an image to binary data."""
        with open(image_path, 'rb') as file:
            binary_data = file.read()
        return binary_data

    def garment(self, garment):
        """Fetch the binary data for a given garment."""
        # Check if the garment name is in the dictionary
        if garment in self.image_paths:
            image_path = self.image_paths[garment]
            return self.image_to_binary(image_path)
        else:
            raise ValueError(f"Garment '{garment}' not found in the available garments.")
