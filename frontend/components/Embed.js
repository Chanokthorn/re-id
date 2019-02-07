import React from "react";
import axios from "axios";
import VideoItem from "../components/VideoItem";

class Embed extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      backend: props.backend,
      videosInfo: null
    };
  }
  componentDidMount() {
    axios
      .get(this.state.backend + "checkVideosStatus")
      .then(res => {
        //   console.log(res.data.results);
        this.setState({ videosInfo: res.data.results });
      })
      .then(() => {
        this.setState({ isLoaded: true });
      });
  }
  render() {
    const { videosInfo, isLoaded, backend } = this.state;

    // console.log(this.state.videosInfo);
    if (!isLoaded) {
      return <div />;
    } else {
      videosInfo.map(videoInfo => {
        console.log(videoInfo);
      });
      return (
        <div>
          {videosInfo.map(videoInfo => (
            <VideoItem
              data={videoInfo}
              key={"video-" + videoInfo.video}
              backend={backend}
            />
          ))}
        </div>
      );
    }
  }
}

export default Embed;
