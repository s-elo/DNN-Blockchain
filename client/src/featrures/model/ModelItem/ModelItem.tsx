import React from "react";
import { Link } from "react-router-dom";
import { Model } from "../type";
import "./ModelItem.less";

export default function ModelItem({ model }: { model: Model }) {
  return (
    <Link className="model-item" to={`/${model.name}`}>
      <title>{`${model.name} (${(model.curAccuracy * 100).toFixed(2)}%)`}</title>
      <section>{model.desc}</section>
    </Link>
  );
}
