import React from "react";
import axios from "axios";
import styled from "styled-components";
import { Grid, Loader, Image, Input, Button } from "semantic-ui-react";
import VideoController from "../components/VideoController";

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
`;

const GrandInput = styled(Input)`
  margin: 0.5em 1em !important;
`;

const GrandButton = styled(Button)`
  margin: 0.5em 1em !important;
`;

class HumanDetection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      backend: props.backend,
      frameLoaded: false,
      personsLoading: false,
      personList: [],
      margin: 1
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

  searchPerson = index => {
    console.log("searching: " + index);
  };

  setMargin = () => {
    const { margin } = this.state;
    console.log("set margin: " + margin);
  };

  render() {
    const {
      backend,
      frameLoaded,
      personsLoading,
      personList,
      margin
    } = this.state;
    return (
      <HumanDetectionContainer>
        <VideoController backend={backend} detectFrame={this.detectFrame} />
        <HumanDetectionPersons>
          <h3>Detected Persons</h3>
          {!frameLoaded ? (
            <h3>No frame selected</h3>
          ) : personsLoading ? (
            <Loader active inline="centered" />
          ) : (
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
                      onClick={() => this.searchPerson(person.url)}
                      key={"div-" + person.url}
                    >
                      <Image size="large" src={url} key={"img-" + person.url} />
                    </div>
                  </Grid.Column>
                );
              })}
            </Grid>
          )}
        </HumanDetectionPersons>
        <HumanDetectionResult>
          <h3>Detection Results</h3>
          <GrandInput
            label="Margin"
            onChange={e => this.setState({ margin: e.target.value })}
            defaultValue={margin}
          />
          <GrandButton onClick={() => this.setMargin()}>Set Margin</GrandButton>
          <Result>- vid2.mp4</Result>
          <Result>- vid5.mp4</Result>
        </HumanDetectionResult>
      </HumanDetectionContainer>
    );
  }
}

export default HumanDetection;
