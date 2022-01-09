import React from "react";
import ModelItem, { Model } from "../ModelItem/ModelItem";
import './ModelList.less';

const models: Model[] = [
  {
    id: "ssss",
    name: "cifar10",
    desc: "nothing",
  },
  {
    id: "ssaasfss",
    name: "cifar100",
    desc: "nothing",
  },
  {
    id: "sssasdfs",
    name: "cifar10000",
    desc: "nothing",
  },
];

export default function ModelList() {
  const renderedModels = models.map((model) => <ModelItem model={model} />);
  return <div className="model-list-container">{renderedModels}</div>;
}
