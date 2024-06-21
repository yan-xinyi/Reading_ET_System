# Reading_ET_System
This reading eye movement data collection platform records the user's eye movement behavior during natural reading by embedding SearchGazer.js.
## 1.Experiment Project and Purpose:
(1) Platform Introduction:
The User Eye-Tracking Behavior Data Collection Platform utilizes the embedded SearchGazer.js to record users' eye-tracking behavior during natural reading.

(2) Experiment Purpose and Tasks:
The platform aims to collect eye-tracking data by recording high-frequency fixation point coordinates during users' reading processes. This eye-tracking data will be further processed into various eye-tracking features for analysis and use. The reading materials used by the platform are abstracts of Chinese academic papers, with each abstract constituting a reading task. Each user is required to complete a total of 330 reading tasks, and the platform will collect eye-tracking data generated during these reading sessions. The first 10 tasks are for the participants to familiarize themselves with the experimental process.

## 2. Personnel Arrangement and Grouping:
A total of 10 people are planned to participate in the experiment. Due to limitations in platform performance and accuracy, participants need to be grouped and tested at different times. The 10 people will be divided into 2 groups, each with 5 people, and different groups will conduct the experiment on different dates.
The first group includes: Yang Yukai, Li Haochuan, Hu Zile, Peng Shuyu, Chu Xinlong
The second group includes: Zeng Jiaqi, Chen Ziling, Duan Decheng, Yang Chenggang, Han Ruxue
During the experiment, each participant will receive a personal account and password for the experimental platform, which they will use to log in and conduct the experiment.

## 3. Experiment Location:
Room 301, School of Economics and Management

## 4. Time Arrangement:
(1) Experiment Date Arrangement:
The entire experiment is planned to be completed within March.
The first group's experiment is scheduled for the fourth week (March 13-17).
The second group's experiment is scheduled for the fifth week (March 20-24).
Additional experiments, if needed, are scheduled for the sixth week (March 27-31).

(2) Experiment Time Schedule:
After confirming the experiment dates, participants need to arrive at the experiment location by 8:30 AM on the scheduled day, and complete browser setup and camera check by 9:00 AM.

## 5. Experiment Process and Specific Requirements:
**Step 1:** Experiment Environment and Configuration
The experiment needs to be conducted on Google Chrome. To allow the browser to trust the experimental platform, the following settings need to be done:

① Open the link in Google Chrome: chrome://flags/#unsafely-treat-insecure-origin-as-secure

② Select the configuration as shown below, and change the content in the text box and the drop-down option on the right:

③ After completing the changes, click the “Relaunch” button at the bottom right of the interface to restart the browser.

④ Reopen Google Chrome and enter the URL of the experimental platform.

**Step 2:** Platform Login

① The URL of the experimental platform is: http://1.13.186.209:5000/index

② The page after entering the platform is as follows:

<div align=center>
<b>Figure 1: Login page</b><br>
  <img src="https://github.com/yan-xinyi/images/blob/main/ET_AKE/login.png" width="80%" alt="Table 1: Table of details of 10 subjects"><br>
</div>

③ Enter the username and password received to log in and enter the platform's homepage.

**Step 3:** Instructions for Using the Reading System
Users can refer to the “System Usage Instructions” on the left side of the homepage for unclear parts of the experiment process, or they can ask the experiment administrators.

**Step 4:** Selecting a Task for Reading
Return to the “Reading Task List,” select “Unread,” choose any task from the list, and click the reading icon on the right to start reading.

❗ Note: To ensure data validity, each task (abstract) can only be read once without interruption. Experiment participants should judge whether they have enough time to complete a task in one go based on the estimated time required and the number of sentences. Additionally, tasks that have generated reading data will be marked as read in the operation column, and the system does not support repeated reading operations.

**Step 5:** Calibration Before Reading
After clicking the reading icon, the platform will conduct two calibrations sequentially to ensure the user meets the experimental requirements.
① The first calibration page is as follows. The system needs to ensure successful camera call and accurate facial and facial feature recognition. Experiment participants need to wait for the page to show the recognized face, ensure their face is facing the camera and the green outline accurately identifies their facial features, and then click the blue button. After confirming their facial position on this page, participants should keep their head and facial positions fixed until the reading of the task (abstract) is completed.

❗ Note: If Google Chrome is not properly set up, the following warning will pop up on this step's page. Do not continue the experiment and contact the experiment administrators for adjustments.

② The second calibration page is as follows. Participants need to click on the yellow dot at the center of the circles that appear on the page. This page is for further calibration of fixation point accuracy. After clicking all nine points, the second calibration is completed.
❗ Note: If participants need to interrupt the experiment due to unmet environmental requirements during the calibration page, they can click the browser's back button or directly close the page. The system will not record any information for that task, nor will it mark the task as read. However, if the participant enters a task's reading page and then exits or closes it midway, it will be recorded as a read status.

**Step 6:** Reading the Abstract
① After completing the two calibrations, participants will click the “Start Reading” button to enter the formal reading page. During the entire reading process, the user's eye-tracking behavior will be recorded in the database.

To further improve accuracy, participants should use the mouse to follow their fixation points during reading. Participants can switch between sentences as needed during reading.
② When reaching the last sentence, clicking “Next Page” again will jump to the verification question page as follows. Participants need to select the most suitable keyword for the abstract from three options and submit their answer. After the page prompts that the save is successful, click the “Return to Task List” link at the bottom of the page to return to the homepage.

❗ Note: The verification question only has one submission opportunity, and repeated submissions will not be recorded in the database. Participants should read the abstract carefully and answer the question earnestly.
