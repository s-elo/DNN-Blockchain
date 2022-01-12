import React, { ChangeEvent, useState } from "react";
import { RouteComponentProps } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectModelByName } from "../modelApi";

import "./ModelDetail.less";

const iframe = document.createElement("iframe");
iframe.style.display = "none";
const body = document.body;
body.appendChild(iframe);

export default function ModelDetail(
  props: RouteComponentProps<{ modelName: string }>
) {
  const { modelName } = props.match.params;
  const model = useSelector(selectModelByName(modelName));

  const [address, setAddress] = useState("");
  const handleAddressChange = (e: ChangeEvent<HTMLInputElement>) =>
    setAddress(e.target.value);

  const getScript = () => {
    if (address.trim() === "")
      return alert("please provide your account address");
    
    iframe.src = `http://localhost:3500/get-scripts/${modelName}-py?address=${address}`;
  };

  if (!model) return <div>No such model</div>;

  return (
    <>
      <title className="detail-title">{`${model.name} (${(
        model.curAccuracy * 100
      ).toFixed(2)}%)`}</title>
      <article className="detail-desc">{model.desc}</article>
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
