import React from "react";
import { Link, Switch, Route, Redirect } from "react-router-dom";
import ModelList from "./featrures/model/ModelList/ModelList";
import ModelDetail from "./featrures/model/ModelDetail/ModelDetail";

import "./App.less";

export default function App() {
  return (
    <div className="container">
      <header>
        <Link to="/" className="to-list">
          Model List
        </Link>
      </header>
      <main className="content-area">
        <Switch>
          <Route exact path="/" component={ModelList} />
          <Route exact path="/:modelName" component={ModelDetail} />
          <Redirect to="/" />
        </Switch>
      </main>
    </div>
  );
}
