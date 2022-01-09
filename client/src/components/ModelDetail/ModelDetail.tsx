import React from "react";
import { RouteComponentProps } from "react-router-dom";

// import { Model } from "../ModelItem/ModelItem";

export default function ModelDetail(
  props: RouteComponentProps<{ modelId: string }>
) {
  const { modelId } = props.match.params;

  return <div>{modelId}</div>;
}
