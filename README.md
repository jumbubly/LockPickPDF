# LockPickPDF

LockPickPDF is a graphical user interface (GUI) application built using PyQt6 that attempts to decrypt password-protected PDF files using a list of potential passwords.

## Features

- Select a single PDF file or a folder containing multiple PDFs for batch processing.
- Decrypt PDF files using a list of passwords provided in a `passwords.txt` file.
- Displays progress of the decryption process.
- Uses `qpdf` for PDF decryption.

## Requirements

- `PyQt6` for building the GUI.
- `qpdf` for handling PDF decryption.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/jumbubly/LockPickPDF.git
    cd LockPickPDF
    ```

2. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    for updated or latest libraries > pip install <libraryname>
    ```

3. **Install `qpdf`:**
   - **Linux (Debian/Ubuntu):**

     ```bash
     sudo apt-get install qpdf
     ```

   - **macOS (using Homebrew):**

     ```bash
     brew install qpdf
     ```

   - **Windows:**
     Download and install `qpdf` from the [qpdf GitHub Releases](https://github.com/qpdf/qpdf/releases).

## Usage

1. **Prepare `passwords.txt`:**
   - Create a `passwords.txt` file in the same directory as the script.
   - Add potential passwords, each on a new line.

   Example `passwords.txt`:
123
password1
password2
password3

2. **Run the application:**

 ```bash
 python lockpickpdf.py
 ```

**Using the Application:**

- Click on **"Select File"** to choose a single PDF file, or **"Select Folder"** to process multiple PDFs in a folder.
- Choose the **Save Location** where the decrypted PDFs will be saved.
- Click **"Process PDFs"** to start the decryption process.

**Progress and Logs:**

- The progress bar will show the decryption progress.
- Logs will be displayed in the text area for each file processed.

## Screenshots

![LockPickPDF](https://raw.githubusercontent.com/jumbubly/GeoCipher/master/lockpickPDF.png)

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to this project.

## License

This project is protected by copyright, and all rights are reserved. Unauthorized use, reproduction, or distribution of this code or any associated materials is prohibited.

## Disclaimer

This tool is intended for educational purposes only. Decrypting PDF files without permission is illegal. Use this tool responsibly.
