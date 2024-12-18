def get_file_names(folder_path, slug):
    try:
        # List all files in the directory
        file_names = [path.join(FAQs_DATA_FOLDER, slug, f) for f in os.listdir(
            folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return file_names
    except Exception as e:
        print(f"Error: {e}")
        return []
