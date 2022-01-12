import React, { ChangeEvent, useState } from "react";
import { RouteComponentProps } from "react-router-dom";

// import { Model } from "../ModelItem/ModelItem";
import "./ModelDetail.less";

const iframe = document.createElement("iframe");
iframe.style.display = "none";
const body = document.body;
body.appendChild(iframe);

export default function ModelDetail(
  props: RouteComponentProps<{ modelName: string }>
) {
  const { modelName } = props.match.params;

  const [address, setAddress] = useState("");
  const handleAddressChange = (e: ChangeEvent<HTMLInputElement>) =>
    setAddress(e.target.value);

  const getScript = () => {
    iframe.src = `http://localhost:3500/get-scripts/${modelName}-py?address=${address}`;
  };

  return (
    <>
      <title>{modelName}</title>
      <article>{`this is the desc`}</article>
      <input
        type="text"
        className="input"
        value={address}
        placeholder="please provide your account address here"
        onChange={handleAddressChange}
      />
      <button onClick={getScript} className="btn download-btn">
        Download Script
      </button>
    </>
  );
}
