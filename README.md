<h2> Re-Identification in multiple videos system with platform for interaction. </h2>
<h3>Installation</h3>
<ul>
  <li>Backend
    <ol>
      <li>
        <p>Install Anaconda</p>
      </li>
      <li>
        <p>activate exported conda environment</p>
        <code>conda activate reid</code>
      </li>
      <li>
        <p>Download "HumanDetection.zip" from <nav>https://www.dropbox.com/s/3zqqwn577g9eycy/HumanDetection.zip?dl=0</nav>
          and export the file at this directory
        </p>
      </li>
      <li>
        <p>Download "best_model.pth" from <nav>https://www.dropbox.com/s/hub0mzdo1wwnz6h/best_train.pth?dl=0</nav>
      </li>
      <li>
        <code>python web_bone-Copy1.py</code>
      </li>
    </ol>
  </li>
    <li>Frontend
    <ol>
      <li>
        <code>cd frontend</code>
      </li>
      <li>
        <code>npm install</code>
      </li>
      <li>
        <code>npm run dev</code>
      </li>
      <li>
        <p>enter the page via localhost:3000</p>
      </li>
    </ol>
  </li>
</ul>
<h3>Usage</h3>
<ul>
  <li>
     <h4>storing video<h4>
       <p>store video(in .mp4 format) at folder HumanDetection/videos</p>
  </li>
  <li>
    <h4>interface usage</h4>
    <li>Human detection
       <img width="880" alt="Screen Shot 2562-03-13 at 01 23 09" src="https://user-images.githubusercontent.com/21177109/54225747-ec7df280-452e-11e9-9607-af5f1f4e71d6.png">
      <h5>videos are available after finishing decting and embedding videos in "Video Embedding" page
      and need restarting the Backend after embedding</h5>
      <ol>
        <li>
          select video
        </li>
        <li>
          scroll through frames or input index to select target frame then press "Detect"
        </li>        
        <li>
          select target to detect
        </li>
        <li>
          videos that target appears will appear on the right, each item is clickable to observe found samples
        </li>
      </ol>
      <img width="852" alt="Screen Shot 2562-03-13 at 01 23 23" src="https://user-images.githubusercontent.com/21177109/54225762-f99ae180-452e-11e9-8257-aa92e8676177.png">
      <ol>
        <li>
          yellow timeline indicates found frames
        </li>
        <li>
          click on timeline of each video to observe the frame
        </li>
        <li>
          adjust the timeline via "Pixels per second" bar
        </li>
      </ol>
     </li>
     <li>Video Embedding
       <img width="779" alt="Screen Shot 2562-03-13 at 01 23 34" src="https://user-images.githubusercontent.com/21177109/54226619-cb1e0600-4530-11e9-92b7-28fa48d6fab0.png">
       <ol>
         <li>
           press "Detect" with settings of preferred "frameSteps"(how many frames to skip) 
           and "maxFrames"(maximum amount of frames to detect)
         </li>
         <li>
           press "Embed"
         </li>
         <li><h5>* optional</h5>
           press "Cluster" with preferred hyperparameters of DBSCAN
         </li>
       </ol>
     </li>
  </li>
</ul>
