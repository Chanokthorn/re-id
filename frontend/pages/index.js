import React from "react";
import axios from "axios";
import Layout from "../components/Layout";
import HumanDetection from "../components/HumanDetection";
import Embed from "../components/Embed";

class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activePage: "detectHuman",
      // backend: "http://localhost:8890/"
      backend: "https://cgci.cp.eng.chula.ac.th/thananop/ssdfaces/"
    };
  }

  onPageSelected = pageName => {
    console.log("called");
    this.setState({ activePage: pageName });
  };

  render() {
    const { activePage, backend } = this.state;
    return (
      <Layout activePage={activePage} onPageSelected={this.onPageSelected}>
        {activePage === "detectHuman" ? (
          <HumanDetection backend={backend} />
        ) : null}
        {activePage === "embed" ? <Embed backend={backend} /> : null}
      </Layout>
    );
  }
}

export default Index;
