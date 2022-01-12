import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import ModelList from "./components/ModelList/ModelList";
import ModelDetail from "./components/ModelDetail/ModelDetail";

import './App.less';

export default function App() {
  return (
    <div className="container">
      <header>Model List</header>
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
