import React from "react";
import {
  Link,
  Route,
  Switch,
  Redirect,
  withRouter,
  RouteComponentProps,
} from "react-router-dom";

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
    showItem: false,
    isFirstTime: true,
  };

  handleShowItem(itemName: string) {
    this.props.itemChanged && this.props.itemChanged(itemName);

    this.setState({
      showItem: true,
    });
  }

  toMenu() {
    const { history, menuPath } = this.props;

    history.push(menuPath);

    this.props.itemChanged && this.props.itemChanged("");

    this.setState({
      showItem: false,
    });
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
        showItem: true,
      });
    }
  }

  render() {
    const { items, linkStyle } = this.props;

    return (
      <div className="body">
        {!this.state.showItem ? (
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
                {/* when the above does not match */}
                <Redirect to="/" />
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
