import React from "react";
import axios from "axios";
import styled from "styled-components";
import {
  Grid,
  Loader,
  Image,
  Input,
  Button,
  Container,
  Checkbox,
  Segment
} from "semantic-ui-react";
import VideoController from "../components/VideoController";
import Timeline from "../components/Timeline2";

const HumanDetectionContainer = styled.div`
    width: 100%;
    height: 100% !important;
    display: grid;
    grid-template-columns: 40% 30% 30%
    grid-template-areas: "console persons result";
`;

const HumanDetectionPersons = styled.div`
  grid-area: persons;
  display: flex;
  flex-direction: column;
  justify-self: center;
  align-self: center;
`;

const HumanDetectionResult = styled.div`
  grid-area: result;
  display: flex;
  flex-direction: column;
  justify-self: center;
  align-self: center;
  text-align: center;
`;

const Result = styled.div`
  width: 60%;
  text-align: center;
  // opacity: ${props => (props.selected ? "0.6" : "1")};
  transition: background-color: white ease-in-out;
  -moz-transition: background-color 0.2s ease-in-out;
  -webkit-transition: background-color 0.2s ease-in-out;
  &:hover {
    background-color: gray;
    transition: background-color 0.2s ease-in-out;
    -moz-transition: background-color 0.2s ease-in-out;
    -webkit-transition: background-color 0.2s ease-in-out;
  }
`;

const GrandInput = styled(Input)`
  margin: 0.5em 1em !important;
`;

const GrandButton = styled(Button)`
  margin: 0.5em 1em !important;
`;

const GrandImage = styled(Image)`
  opacity: ${props => (props.selected ? "0.6" : "1")};
  transition: opacity 0.2s ease-in-out;
  -moz-transition: opacity 0.2s ease-in-out;
  -webkit-transition: opacity 0.2s ease-in-out;
  &:hover {
    opacity: 0.6;
    transition: opacity 0.2s ease-in-out;
    -moz-transition: opacity 0.2s ease-in-out;
    -webkit-transition: opacity 0.2s ease-in-out;
  }
`;

class HumanDetection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      backend: props.backend,
      frameLoaded: false,
      personsLoading: false,
      isFinding: false,
      findResult: [],
      personList: [],
      findResultMatch: [],
      margin: 1,
      personSelected: null,
      videoSelected: null,
      isFindingInVideo: false,
      videoPersonList: [],
      useCluster: false
    };
  }

  onFrameLoad = () => {
    this.setState({ frameLoaded: true });
  };

  detectFrame = () => {
    const { backend } = this.state;
    this.setState({ frameLoaded: true, personsLoading: true });
    axios
      .get(backend + "detectFrame")
      .then(res => {
        this.setState({ personList: res.data.results });
      })
      .then(() => {
        this.setState({ personsLoading: false });
        console.log("PERSONLIST");
        console.log(this.state.personList);
      });
  };

  searchPerson = url => {
    const { backend, useCluster } = this.state;
    this.setState({ isFinding: true, personSelected: url }, this.searchPersonWithFrame);
    console.log("searching: " + url);
    axios
      .get(backend + "findPerson", {
        params: { url: url, mode: useCluster ? "useCluster" : "full" }
      })
      .then(res => {
        this.setState({ findResult: res.data.result, isFinding: false });
        console.log("Found list");
        console.log(res.data.result);
      });
  };

  setMargin = () => {
    const { backend, margin } = this.state;
    axios
      .get(backend + "setMargin", {
        params: { margin: margin }
      })
      .then(res => {
        console.log("set margin " + res.data);
      });
  };

  observe = videoName => {
    const { backend } = this.state;
    this.setState({ isFindingInVideo: true });
    const url = backend + "observe";
    console.log("OBSERVE: ", url);
    axios
      .get(url, {
        params: { video: videoName }
      })
      .then(res => {
        this.setState({
          videoPersonList: res.data.result,
          isFindingInVideo: false
        });
      });
  };

  onModeToggled = checked => {
    if (checked === true) {
      this.setState({ videoPersonList: [] });
    }
    this.setState({ useCluster: checked });
  };
  searchPersonWithFrame = () => {
    const { backend, personSelected, useCluster } = this.state;
    axios
      .get(backend + "findPersonWithFrame", {
        params: {
          url: personSelected,
          mode: useCluster ? "useCluster" : "full"
        }
      })
      .then(res => {
        this.setState({ findResultMatch: res.data.result, isFinding: false });
        console.log("Found Match list");
        console.log(res.data.result);
      });
  };

  render() {
    const {
      backend,
      frameLoaded,
      personsLoading,
      personList,
      margin,
      findResult,
      findResultMatch,
      personSelected,
      isFindingInVideo,
      videoPersonList,
      useCluster
    } = this.state;
    return [
      <HumanDetectionContainer key="main">
        <VideoController backend={backend} detectFrame={this.detectFrame} />
        <Container>
          <HumanDetectionPersons>
            <Grid centered>
              <h3>Detected Persons</h3>
              {!frameLoaded ? (
                <h3>No frame selected</h3>
              ) : personsLoading ? (
                <Loader active inline="centered" />
              ) : (
                // <GridContainerContainer>
                //   <GridContainer>
                <Grid.Row>
                  <Grid
                    columns={4}
                    stackable
                    centered
                    padded="vertically"
                    textAlign="center"
                  >
                    {personList.map(person => {
                      const url = backend + "imageStorage/" + person;
                      console.log("image url: ", url);
                      return (
                        <Grid.Column width={4} key={person.index}>
                          <div
                            onClick={() => this.searchPerson(person)}
                            key={"div-" + person.url}
                          >
                            <GrandImage
                              size="small"
                              src={url}
                              key={"img-" + person.url}
                              selected={person === personSelected}
                            />
                          </div>
                        </Grid.Column>
                      );
                    })}
                  </Grid>
                </Grid.Row>
                //   </GridContainer>
                // </GridContainerContainer>
              )}
            </Grid>
          </HumanDetectionPersons>
        </Container>
        <Grid centered>
          <Grid.Row>
            <HumanDetectionResult>
              <h3>Detection Results</h3>
              <Segment>
                <Checkbox
                  checked={useCluster}
                  toggle
                  label="Use Cluster"
                  onChange={(e, { checked }) => this.onModeToggled(checked)}
                />
              </Segment>
              <GrandInput
                label="Margin"
                onChange={e => this.setState({ margin: e.target.value })}
                defaultValue={margin}
              />
              <GrandButton onClick={() => this.setMargin()}>
                Set Margin
              </GrandButton>
              {findResult.length === 0
                ? null
                : findResult.map(video => (
                    <GrandButton
                      color="blue"
                      onClick={() => this.observe(video.videoName)}
                    >
                      {video.videoName}
                    </GrandButton>
                  ))}
            </HumanDetectionResult>
          </Grid.Row>
          {useCluster
            ? null
            : videoPersonList.length > 0
            ? videoPersonList.map(person => (
                <Grid.Column width={4} key={person}>
                  <div
                    onClick={() => this.searchPerson(person)}
                    key={"div2-" + person}
                  >
                    <GrandImage
                      size="small"
                      src={backend + "imageStorage/" + person}
                      key={"img2-" + person}
                      selected={person === personSelected}
                    />
                  </div>
                </Grid.Column>
              ))
            : null}
        </Grid>
      </HumanDetectionContainer>,
      <Timeline
          key="timeline"
          foundList={findResultMatch}
      />
    ];
  }
}

export default HumanDetection;
