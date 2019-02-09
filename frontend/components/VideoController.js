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
  grid-template-columns: 1fr 6fr;
  grid-template-rows: 7fr 1fr 1fr;
  grid-template-areas:
    "frame frame"
    "index slider"
    "detect detect";
`;

const IndexField = styled(Input)`
  margin-top: 10px;
  grid-area: index;
  height: 25px;
  width: 80px;
`;

const Frame = styled.div`
  grid-area: frame;
  display: flex;
  width: 480px;
  height: 320px;
  text-align: center;
  flex-direction: row;
  justify-self: center;
  align-self: center;
`;

const LoaderDiv = styled.div`
  display: flex;
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

// const GrandInputRange = styled(InputRange)`
//   grid-area: range;
// `;

const Slider = styled.input`
  margin-top: 10px;
  grid-area: slider
  -webkit-appearance: none;
  width: 100%;
  height: 25px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: 0.2s;
  transition: opacity 0.2s;
  &:hover {
    opacity: 1;
  }
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 25px;
    height: 25px;
    background: #4c96af;
    cursor: pointer;
  }
  &::-moz-range-thumb {
    width: 25px;
    height: 25px;
    background: #4c96af;
    cursor: pointer;
  }
`;

class VideoController extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      index: 0,
      backend: props.backend,
      video: props.video,
      videoList: [],
      videoLoading: false,
      videoLoaded: false,
      videoListLoaded: false,
      frameURL: null,
      frameStep: 10,
      length: null
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
  getFrameIndex = index => {
    const { backend } = this.state;
    this.setState({ isLoaded: false });
    axios
      .get(backend + "getFrameIndex", {
        params: { index: index }
      })
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
      .then(res => {
        this.setState({
          length: parseInt(res.data.result) - 2,
          videoLoading: false
        });
      })
      .then(() => {
        this.getFrameIndex(0);
      })
      .then(() => {
        this.setState({ videoLoaded: true });
      });
  };
  detect = () => {
    console.log("detect");
  };

  onIndexChange = e => {
    this.setState({ index: e.target.value });
    this.getFrameIndex(e.target.value);
  };

  renderConsole = () => {
    const {
      videoList,
      videoListLoaded,
      videoLoading,
      videoLoaded,
      frameStep,
      video,
      frameURL,
      index,
      isLoaded,
      length
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
        {videoLoading ? (
          <LoaderDiv>
            <Loader active inline="centered" />
          </LoaderDiv>
        ) : (
          <GrandButton onClick={() => this.loadVideo(video)}>
            Load Video
          </GrandButton>
        )}
        {videoLoaded ? (
          <VideoConsole>
            <Frame>
              {/* <img src={frameURL} /> */}
              {isLoaded ? (
                <Image centered src={frameURL} size="medium" />
              ) : (
                <Loader active inline="centered" />
              )}
            </Frame>
            <IndexField value={index} onChange={e => this.onIndexChange(e)} />
            <Slider
              type="range"
              min="1"
              max={String(length)}
              value={index}
              onChange={e => this.onIndexChange(e)}
            />
            {/* <PrevButton>
              <Button onClick={() => this.prevFrame()}>
                <Icon name="angle left" />
              </Button>
            </PrevButton> */}
            {/* <GrandInputRange>
              maxValue={20}
              minValue={0}
              value={this.state.index}
              onChange=
              {value => {
                this.setState({ index: value });
              }}
            </GrandInputRange> */}
            <DetectButton>
              <Button onClick={() => this.props.detectFrame()}>Detect</Button>
            </DetectButton>
            {/* <NextButton>
              <Button onClick={() => this.nextFrame()}>
                <Icon name="angle right" />
              </Button>
            </NextButton> */}
          </VideoConsole>
        ) : null}
      </HumanDetectionConsole>
    );
  };

  render() {
    return <div>{this.renderConsole()}</div>;
  }
}

export default VideoController;
