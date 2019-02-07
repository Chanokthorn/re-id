import React from "react";
import axios from "axios";
import styled from "styled-components";
import {
  Dropdown,
  Menu,
  Grid,
  Button,
  Loader,
  Input,
  Image,
  Icon
} from "semantic-ui-react";

const HumanDetectionConsole = styled.div`
  grid-area: console;
  display: flex;
  flex-direction: column;
  justify-self: center;
  align-self: center;
`;

const GrandButton = styled(Button)`
  margin: 0.5em 1em !important;
`;

const GrandInput = styled(Input)`
  margin: 0.5em 1em !important;
`;

const VideoConsole = styled.div`
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 4fr 1fr;
  grid-template-areas:
    "frame frame frame"
    "prev detect next";
`;

const Frame = styled.div`
  grid-area: frame;
  display: flex;
  flex-direction: row;
  justify-self: center;
  align-self: center;
`;

const PrevButton = styled.div`
    align-self: start;
    grid-area: prev
    display: flex;
    flex-direction: row;
    justify-self: center;
    align-self: center;
`;
const DetectButton = styled.div`
    align-self: start;
    grid-area: detect
    display: flex;
    flex-direction: row;
    justify-self: center;
    align-self: center;
`;
const NextButton = styled.div`
    align-self: start;
    grid-area: next
    display: flex;
    flex-direction: row;
    justify-self: center;
    align-self: center;
`;

class VideoController extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      backend: props.backend,
      video: props.video,
      videoList: [],
      videoLoading: false,
      videoLoaded: false,
      videoListLoaded: false,
      frameURL: null,
      frameStep: 10
    };
  }
  componentDidMount() {
    axios
      .get(this.state.backend + "checkVideosStatus")
      .then(res => {
        this.updateVideoList(res.data.results);
      })
      .then(() => {
        this.setState({ videoListLoaded: true });
      });
  }

  updateVideoList = videosInfo => {
    let videoList = [];
    videosInfo.map(videoInfo => {
      if (videoInfo.status === "clustered") {
        videoList.push(videoInfo.video);
      }
    });
    this.setState({ videoList: videoList });
  };

  onVideoSelected = video => {
    console.log(video);
    this.setState({ video: video });
  };

  setFrameStep = () => {
    const { backend, frameStep } = this.state;
    axios.get(backend + "setFrameStep", {
      params: { frameStep: frameStep }
    });
  };

  getFrame = () => {
    const { backend } = this.state;
    this.setState({ isLoaded: false });
    axios
      .get(backend + "getFrame")
      .then(res => {
        this.setState({ frameURL: backend + "imageStorage/" + res.data.url });
        console.log("res: ", res.data.url);
      })
      .then(() => {
        this.setState({ isLoaded: true });
      });
  };
  nextFrame = () => {
    const { backend } = this.state;
    this.setState({ isLoaded: false });
    axios
      .get(backend + "getNextFrame")
      .then(res => {
        this.setState({ frameURL: backend + "imageStorage/" + res.data.url });
      })
      .then(() => {
        this.setState({ isLoaded: true });
      });
  };
  prevFrame = () => {
    const { backend } = this.state;
    this.setState({ isLoaded: false });
    axios
      .get(backend + "getPrevFrame")
      .then(res => {
        this.setState({ frameURL: backend + "imageStorage/" + res.data.url });
      })
      .then(() => {
        this.setState({ isLoaded: true });
      });
  };
  loadVideo = () => {
    const { backend, video } = this.state;
    this.setState({ videoLoading: true });
    axios
      .get(backend + "loadVideo", {
        params: { video: video }
      })
      .then(() => {
        this.setState({ videoLoading: false });
      })
      .then(() => {
        this.getFrame();
      })
      .then(() => {
        this.setState({ videoLoaded: true });
      });
  };
  detect = () => {
    console.log("detect");
  };

  renderConsole = () => {
    const {
      videoList,
      videoListLoaded,
      videoLoading,
      videoLoaded,
      frameStep,
      video,
      frameURL
    } = this.state;
    let options = [];
    if (videoList.length !== 0) {
      videoList.map((video, idx) => {
        options.push({
          key: idx,
          text: video,
          value: video
        });
      });
    }
    return (
      <HumanDetectionConsole>
        <Menu compact>
          {videoListLoaded ? (
            <Dropdown
              placeholder="select..."
              selection
              options={options}
              onChange={(e, data) => this.setState({ video: data.value })}
            />
          ) : null}
        </Menu>
        <GrandInput
          label="Frame Step"
          onChange={e => this.setState({ frameStep: e.target.value })}
          defaultValue={frameStep}
        />
        <GrandButton onClick={() => this.setFrameStep()}>
          Set Frame Step
        </GrandButton>
        {videoLoading ? (
          <Loader active inline="centered" />
        ) : (
          <GrandButton onClick={() => this.loadVideo(video)}>
            Load Video
          </GrandButton>
        )}
        {videoLoaded ? (
          <VideoConsole>
            <Frame>
              {/* <img src={frameURL} /> */}
              <Image fluid src={frameURL} size="medium" />
            </Frame>
            <PrevButton>
              <Button onClick={() => this.prevFrame()}>
                <Icon name="angle left" />
              </Button>
            </PrevButton>
            <DetectButton>
              <Button onClick={() => this.props.detectFrame()}>Detect</Button>
            </DetectButton>
            <NextButton>
              <Button onClick={() => this.nextFrame()}>
                <Icon name="angle right" />
              </Button>
            </NextButton>
          </VideoConsole>
        ) : //   <Grid width={16} centered>
        //     <Grid.Row>
        //       <Image src={frameURL} size="medium" />
        //     </Grid.Row>
        //     <Grid.Row>
        //       <Grid.Column width={6}>
        //         <Button onClick={() => this.prevFrame()}>
        //           <Icon name="angle left" />
        //         </Button>
        //       </Grid.Column>
        //       <Grid.Column width={4}>
        //         <Button onClick={() => this.props.detectFrame()}>Detect</Button>
        //       </Grid.Column>
        //       <Grid.Column width={6}>
        //         <Button onClick={() => this.nextFrame()}>
        //           <Icon name="angle right" />
        //         </Button>
        //       </Grid.Column>
        //     </Grid.Row>
        //   </Grid>
        null}
      </HumanDetectionConsole>
    );
  };

  render() {
    return <div>{this.renderConsole()}</div>;
  }
}

export default VideoController;
