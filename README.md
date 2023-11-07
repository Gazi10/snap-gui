# Team 14 Project: GUI Cleanup App

## How to run:
```bash
# Node application alone
cd 326-project-repo-team-14
npm i
npm start

or
cd 326-project-repo-team-14
docker build -t app .
docker run -p80:80 app
```

```bash
# Docker compose app with db and flask (NOTE: This will be very slow since the flask backend runs some AI stuff)
cd 326-project-repo-team-14
docker compose up -d
```

The website is reachable at 127.0.0.1 or 127.0.0.1:8080 (view output/set env vars)

### Team Overview:

- Justin Fallo, jfallo
- Sergio Ly, surge119
- Abdullah Al Hamoud, AbdullahHamoud7
- Gazi Ajwad Ahbab, Gazi10

### Innovative Idea:

This application is used to remove GUI elements from images. The application can either handle mass amounts of images or a single image. If the user chooses to handle a set of images, then the application will automatically identify, remove, and inpaint all GUI elements from the images. If the user chooses to handle a single image, then the application will display the identified GUI elements to allow the user to select which they want to keep, if any. Thus, the user has the option to perform an efficient cleanup of mass amounts of images, or a personalized cleanup of a single image. The application will have a feedback and comments section to discuss performance. This application relates to current open-source projects that remove selected GUI elements from a single image.

### Data:

- Images with GUI elements: Images with GUI elements are images that contains graphical user interface objects. This data will be the input of the user that they want to clean.
- Images with highlighted GUI elements: Images with selected GUI elements are images that highlight the graphical user interface objects contained in the image. The user can interact with this data to choose which GUI elements they wants to clean.
- Images with no GUI elements: Images with no GUI elements are images that contain no graphical user interface objects. This data will be the output that the user desires.
- Comments/feedback: Comments and feedback are text posted by the user about the application.

### Functionality:

- Upload dataset: The user uploads a set of images to the application.
- Clean dataset: The user clicks a button that outputs a set of images cleaned of all GUI elements.
- Download dataset: The user downloads the set of clean images output by the application.
- Upload image: The user uploads a single image to the application.
- Identify GUI elements: The user clicks a button that outputs the single image with all GUI elements highlighted.
- Select GUI elements: The user clicks the identified GUI elements to be cleaned.
- Clean image: The user clicks a button that outputs the single image cleaned of all selected GUI elements.
- Download image: The user downloads the clean image output by the application.
- Comment: The user enters text into a text box to comment and provide feedback.
- Publish comment: The user clicks a button to post their comment to the feedback forum.

### License:

[MIT License](https://opensource.org/licenses/MIT)
