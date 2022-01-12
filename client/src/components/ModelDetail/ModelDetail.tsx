import React, { useState } from "react";
import { RouteComponentProps } from "react-router-dom";

// import { Model } from "../ModelItem/ModelItem";
import "./ModelDetail.less";

const iframe = document.createElement("iframe");
iframe.style.display = 'none';
const body = document.body;
body.appendChild(iframe);

export default function ModelDetail(
  props: RouteComponentProps<{ modelName: string }>
) {
  const { modelName } = props.match.params;

  const getScript = () => {
    iframe.src = `http://localhost:3500/get-scripts/${modelName}-py`;
  };

  return (
    <>
      <title>{modelName}</title>
      <article>{`this is the desc`}</article>
      <button onClick={getScript} className="btn download-btn">
        Download Script
      </button>
    </>
  );
}
