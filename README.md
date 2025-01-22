
# PicStream

**PicStream** is a lightweight and user-friendly command-line tool that connects to your Google Photos library to retrieve and display photos for digital photo frames. Simplify the process of syncing your favorite memories to keep your photo frame up to date.

---

## Features

- **Seamless Integration**: Access your Google Photos library with ease.
- **Customizable Photo Retrieval**: Filter photos by album, date, or tags.
- **Optimized for Digital Frames**: Automatically resize or format photos for your device.
- **Secure and Reliable**: Built with secure OAuth2 authentication for accessing Google Photos.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/PicStream.git
   cd PicStream
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure Google API credentials:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Google Photos Library API.
   - Download the `secrets.json` file and place it in the PicStream directory.

---

## Usage

1. Authenticate with your Google account:
Download the client secret json file from google api console and save it as secrets.json in the projects root directory. 
---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve PicStream.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature name"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Powered by the [Google Photos Library API](https://developers.google.com/photos).
- Inspired by the need to keep our memories alive in the digital age.

---

**PicStream** – Your memories, beautifully streamed.


# NOTES TO Revise: 

Get a static host from NGROK
add it to the google console API along with the redirectURI. 
run NGROK tunnel agent in another console.  Example: ngrok http --url=pony-safe-stag.ngrok-free.app 80 
Make sure the flask server is running in port 80
