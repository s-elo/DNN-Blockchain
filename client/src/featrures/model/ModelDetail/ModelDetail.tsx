import React, { ChangeEvent, useState, useEffect } from "react";
import { RouteComponentProps } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectModelByName } from "../modelApi";
import getWeb3 from "@/utils/getWeb3";
import "./ModelDetail.less";
import Spinner from "@/components/Spinner/Spinner";

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
  const [hasWallet, setHasWallet] = useState(true);
  const [isLoadingWallet, setIsLoadingWallet] = useState(true);

  const handleAddressChange = (e: ChangeEvent<HTMLInputElement>) =>
    setAddress(e.target.value);

  useEffect(() => {
    const getWallet = async () => {
      try {
        const web3 = await getWeb3();
        const accounts = await web3.eth.getAccounts();

        setAddress(accounts[0]);
        setIsLoadingWallet(false);
      } catch (e) {
        setHasWallet(false);
        setIsLoadingWallet(false);
      }
    };

    getWallet();
  }, []);

  const getScript = () => {
    if (!hasWallet && address.trim() === "")
      return alert("please provide your account address");

    iframe.src = `http://localhost:3500/get-scripts/${modelName}-py?address=${address}`;
  };

  if (!model) return <div>No such model</div>;

  return (
    <>
      {isLoadingWallet ? (
        <Spinner text="Loading the wallet..." />
      ) : (
        <>
          <title className="detail-title">{`${model.name} (${(
            model.curAccuracy * 100
          ).toFixed(2)}%)`}</title>
          <article className="detail-desc">{model.desc}</article>
          {!hasWallet ? (
            <input
              type="text"
              className="input"
              value={address}
              placeholder="We can not get the wallet, you need to provide your address manually"
              onChange={handleAddressChange}
            />
          ) : (
            ""
          )}
          <button onClick={getScript} className="btn download-btn">
            Download Script
          </button>
        </>
      )}
    </>
  );
}
