import { Menu } from "semantic-ui-react";

class Layout extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activePage: props.activePage
    };
  }

  onItemClicked = pageName => {
    this.setState({ activePage: pageName });
    this.props.onPageSelected(pageName);
  };

  render() {
    const items = [
      { key: "detectHuman", active: true, name: "human identification" },
      { key: "embed", active: false, name: "video embedding" }
    ];
    const { activePage } = this.state;
    return (
      <div>
        <Menu>
          <Menu.Item
            key="detectHuman"
            active={activePage === "detectHuman"}
            name="human identification"
            onClick={() => this.onItemClicked("detectHuman")}
          />
          <Menu.Item
            key="embed"
            active={activePage === "embed"}
            name="video embedding"
            onClick={() => this.onItemClicked("embed")}
          />
        </Menu>
        <div>{this.props.children}</div>
      </div>
    );
  }
}

export default Layout;
