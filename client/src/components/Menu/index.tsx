import React from "react";
import {
  Link,
  Route,
  Switch,
  Redirect,
  withRouter,
  RouteComponentProps,
} from "react-router-dom";
import Ops from "@/components/Ops";

import "./index.less";

type Item = {
  path: string;
  name: string;
  component: React.ComponentType;
};

type Props = {
  items: Array<Item>;
  linkStyle: {
    [Props: string]: string;
  };
  menuPath: string;
  // sync the demo name
  itemChanged?: (itemName: string) => void;
};

class Menu extends React.Component<RouteComponentProps & Props> {
  state = {
    isFirstTime: true,
  };

  handleShowItem(itemName: string) {
    this.props.itemChanged && this.props.itemChanged(itemName);
  }

  toMenu() {
    const { history, menuPath } = this.props;

    history.push(menuPath);

    this.props.itemChanged && this.props.itemChanged("");
  }

  componentDidMount() {
    const {
      location: { pathname },
      history,
      items,
    } = this.props;

    // only jump if the pathname is included in the path of one of the items in this menu (level)
    // or the pathname is the next level of the path of one of the items
    const isIncluded = items.some(
      (v) => v.path === pathname || pathname.indexOf(v.path) !== -1
    );

    if (isIncluded && this.state.isFirstTime) {
      history.push(pathname);

      // sync the name if it has a name and being the up level the the pathname
      if (
        this.props.itemChanged &&
        items.some((v) => pathname.indexOf(v.path) !== -1)
      ) {
        // find that up level
        const item = items.find((v) => pathname.indexOf(v.path) !== -1);

        item && this.props.itemChanged(item.name);
      }

      this.setState({
        isFirstTime: false,
      });
    }
  }

  isMenuPath = (menuPath: string) => {
    // when it is a root path,
    // show the menu instead of the items
    return this.props.location.pathname === menuPath;
  };

  render() {
    const { items, linkStyle, menuPath } = this.props;

    return (
      <div className="body">
        {this.isMenuPath(menuPath) ? (
          <div className="menu">
            {items.map((item, index) => (
              <div
                className="menu-item"
                key={item.path}
                onClick={this.handleShowItem.bind(this, item.name)}
              >
                <div className="menu-order">{index + 1}</div>
                <Link style={linkStyle} to={item.path}>
                  {item.name}
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="demo-area">
            <div className="demo-content">
              <Switch>
                {items.map((item) => (
                  <Route
                    path={item.path}
                    component={item.component}
                    key={item.path}
                  />
                ))}
                <Route path="/ops" component={Ops} />
                {/* when the above does not match */}
                <Redirect to="/ops" />
              </Switch>
            </div>
            <div className="back-to-menu" onClick={this.toMenu.bind(this)}>
              Menu
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default withRouter(Menu);
