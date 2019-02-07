import axios from "axios";
import styled from "styled-components";
import { Image, Input, Loader, Button } from "semantic-ui-react";

const VideoItemContainer = styled.div`
  width: 100%;
  display: grid;
  grid-template-columns: 25% 25% 25% 25%;
  grid-template-areas: "info console plot embed";
  box-shadow: 1px 2px 6px grey;
`;

const VideoInfo = styled.div`
  grid-area: info;
  padding: 2em 1em;
`;

const VideoConsole = styled.div`
  grid-area: console;
  display: flex;
  flex-direction: column;
  justify-self: center;
  align-self: center;
`;
const VideoPlot = styled.div`
  grid-area: plot;
  display: flex;
  flex-direction: column;
  justify-self: center;
  align-self: center;
`;
const EmbedConsole = styled.div`
  grid-area: embed;
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

const Message = styled.div`
  text-align: center;
`;

class VideoItem extends React.Component {
  constructor(props) {
    super(props);
    const {
      embeddingAmount,
      eps,
      identityAmount,
      min_samples,
      status,
      video,
      projectionDim
    } = props.data;
    this.state = {
      plotInitialLoad: false,
      plotLoaded: false,
      detectLoaded: true,
      embedLoaded: true,
      clusterLoaded: true,
      plotURL: null,
      embeddingAmount: embeddingAmount ? embeddingAmount : "-",
      eps: eps ? eps : "0.5",
      identityAmount: identityAmount,
      min_samples: min_samples ? min_samples : "7",
      status: status,
      video: video,
      projectionDim: projectionDim ? projectionDim : "5",
      frameStep: 2,
      maxFrames: 30,
      backend: props.backend,
      input_eps: eps ? eps : "0.5",
      input_min_samples: min_samples ? min_samples : "7",
      input_projectionDim: projectionDim ? projectionDim : "5"
    };
  }

  componentDidMount() {
    // this.getPlotResult();
  }

  getPlotResult = () => {
    const { backend, video } = this.state;
    this.setState({ plotLoaded: false, plotInitialLoad: true });
    axios
      .get(backend + "plot", {
        params: { video: video }
      })
      .then(res => {
        console.log(res.data.url);
        this.setState({ plotURL: backend + "imageStorage/" + res.data.url });
      })
      .then(() => {
        this.setState({ plotLoaded: true, plotInitialLoad: true });
      });
  };

  getData = () => {
    const { backend, video } = this.state;
    axios
      .get(backend + "checkVideoStatus", {
        params: { video: video }
      })
      .then(res => {
        const {
          embeddingAmount,
          eps,
          identityAmount,
          min_samples,
          status,
          projectionDim
        } = res.data.result;
        this.setState({
          embeddingAmount: embeddingAmount ? embeddingAmount : "-",
          eps: eps ? eps : "0.5",
          identityAmount: identityAmount,
          min_samples: min_samples ? min_samples : "7",
          status: status,
          projectionDim: projectionDim ? projectionDim : "5"
        });
      })
      .then(() => {
        this.getPlotResult();
      });
  };

  embed = () => {
    const { backend, video } = this.state;
    this.setState({ embedLoaded: false });
    axios
      .get(backend + "embed", {
        params: { video: video }
      })
      .then(() => {
        this.setState({ embedLoaded: true });
        this.getData();
      });
  };

  detect = () => {
    const { backend, data, frameStep, maxFrames, video } = this.state;
    this.setState({ detectLoaded: false });
    axios
      .get(backend + "detect", {
        params: {
          video: video,
          frameStep: frameStep,
          maxFrames: maxFrames
        }
      })
      .then(() => {
        this.setState({ detectLoaded: true });
      });
  };

  cluster = () => {
    const {
      backend,
      video,
      input_eps,
      input_min_samples,
      input_projectionDim
    } = this.state;
    this.setState({ clusterLoaded: false });
    axios
      .get(backend + "cluster", {
        params: {
          video: video,
          eps: input_eps,
          min_samples: input_min_samples,
          projectionDim: input_projectionDim
        }
      })
      .then(() => {
        this.getData();
      })
      .then(() => {
        this.setState({ clusterLoaded: true });
      });
  };

  render() {
    const {
      video,
      status,
      identityAmount,
      eps,
      min_samples,
      plotURL,
      plotLoaded,
      plotInitialLoad,
      detectLoaded,
      embedLoaded,
      clusterLoaded,
      embeddingAmount,
      projectionDim,
      frameStep,
      maxFrames
    } = this.state;
    console.log("video: " + video + " eps: " + eps);
    return (
      <VideoItemContainer>
        <VideoInfo>
          <p>Name: {video}</p>
          <p>Status: {status}</p>
          <p>
            Embedding Amount:{" "}
            {status === "clustered" || status === "embeddingOnly"
              ? embeddingAmount
              : "-"}
          </p>
          <p>
            Identity Amount: {status === "clustered" ? identityAmount : "-"}
          </p>
          <p>eps: {status === "clustered" ? eps : "-"}</p>
          <p>min samples: {status === "clustered" ? min_samples : "-"}</p>
          <p>projection dim: {status === "clustered" ? projectionDim : "-"}</p>
        </VideoInfo>
        <VideoConsole>
          <GrandInput
            label="Eps"
            onChange={e => this.setState({ input_eps: e.target.value })}
            defaultValue={eps}
          />
          <GrandInput
            label="Min Samples"
            onChange={e => this.setState({ input_min_samples: e.target.value })}
            defaultValue={min_samples}
          />
          <GrandInput
            label="Projection Dim"
            onChange={e =>
              this.setState({ input_projectionDim: e.target.value })
            }
            defaultValue={projectionDim}
          />
          {status !== "noEmbedding" ? (
            clusterLoaded ? (
              <GrandButton onClick={() => this.cluster()}>
                Begin Clustering
              </GrandButton>
            ) : (
              <Loader active inline="centered" />
            )
          ) : (
            <Message>Need embedding before clustering</Message>
          )}
        </VideoConsole>
        <VideoPlot>
          {status === "clustered" ? (
            !plotInitialLoad ? (
              <GrandButton onClick={() => this.getPlotResult()}>
                Load Plot Result
              </GrandButton>
            ) : plotLoaded ? (
              <Image src={plotURL} size="medium" />
            ) : (
              <Loader active inline="centered" />
            )
          ) : (
            <h3>{status}</h3>
          )}
        </VideoPlot>
        <EmbedConsole>
          <GrandInput
            label="Frame Steps"
            onChange={e => this.setState({ frameStep: e.target.value })}
            defaultValue={frameStep}
          />
          <GrandInput
            label="Max Frames"
            onChange={e => this.setState({ maxFrames: e.target.value })}
            defaultValue={maxFrames}
          />
          {detectLoaded ? (
            <GrandButton onClick={() => this.detect()}>Detect</GrandButton>
          ) : (
            <Loader active inline="centered" />
          )}
          {embedLoaded ? (
            <GrandButton onClick={() => this.embed()}>Embed</GrandButton>
          ) : (
            <Loader active inline="centered" />
          )}
        </EmbedConsole>
      </VideoItemContainer>
    );
  }
}

export default VideoItem;
