import React from "react";
import Menu from "./components/Menu";
import SimpleStorage from "./contractComponents/SimpleStorage/SimpleStorage";
import Test from './components/test/test';
import "./App.less";

const linkStyle = {
  textDecoration: "none",
  color: "black",
  width: "100%",
  height: "100%",
  display: "inline-block",
  padding: "10px",
};

const demos = [
  {
    path: "/simpleStorage",
    name: "SimpleStorage",
    component: SimpleStorage,
  },
  {
    path: '/test',
    name: 'Test',
    component: Test
  }
];

export default class App extends React.Component {
  state = {
    currentDemoName: "",
  };

  changeDemo = (itemName: string) => {
    this.setState({
      currentDemoName: itemName,
    });
  };

  render() {
    return (
      <div className="app-body">
        <div className="app-content">
          <div className="demo-name">{this.state.currentDemoName}</div>
          <Menu
            items={demos}
            linkStyle={linkStyle}
            menuPath="/"
            itemChanged={this.changeDemo}
          ></Menu>
        </div>
      </div>
    );
  }
}
