# data_type_bot
## Getting Started

1. **Clone the main repository:**
    ```bash
    git clone https://github.com/work-faiz/data_type_xcel_tech
    ```

2. **Run the initial setup:**
    - Navigate to the cloned folder and double-click `start.bat`.
    - Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```
    - Install Tesseract OCR:
        - Download the Windows installer from [UB Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki).
        - Run the installer and note the installation path (e.g., `C:\Program Files\Tesseract-OCR`).
    - Download the Edge browser driver from [Microsoft Edge Developer](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and save it to `C:\path\to\`.

3. **Set up this project:**
    - Return to this directory.
    - Create a virtual environment:
      ```bash
      python -m venv venv
      ```
    - Activate the virtual environment:
      - On Windows:
         ```bash
         venv\Scripts\activate
         ```
      - On macOS/Linux:
         ```bash
         source venv/bin/activate
         ```
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```


4. **Start the application:**
    - Double-click `start.bat` in this folder.
