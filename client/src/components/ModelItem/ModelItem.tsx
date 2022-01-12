import React from "react";
import { Link } from "react-router-dom";
import "./ModelItem.less";

export type Model = {
  id: string;
  name: string;
  desc: string;
};

export default function ModelItem({ model }: { model: Model }) {
  return (
    <Link className="model-item" to={`/${model.name}`}>
      <title>{model.name}</title>
      <section>{model.desc}</section>
    </Link>
  );
}
