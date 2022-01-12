import React from "react";
import ModelItem from "../ModelItem/ModelItem";
import { useGetModelsQuery } from "../modelApi";

import "./ModelList.less";
import Spinner from "@/components/Spinner/Spinner";

export default function ModelList() {
  const {
    data: models = [],
    isLoading,
    isSuccess,
    isError,
  } = useGetModelsQuery();

  let renderedModels;
  if (isLoading) {
    renderedModels = <Spinner />;
  } else if (isSuccess) {
    renderedModels =
      models.length === 0
        ? `No any model so far`
        : models.map((model) => <ModelItem model={model} key={model.name} />);
  } else if (isError) {
    renderedModels = `can not get the models so far`;
  }

  return <div className="model-list-container">{renderedModels}</div>;
}
