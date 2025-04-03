import { useEffect, useState } from "react";
import { IResource } from "../interfaces/generic";
import { getProductResource } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import LoadingSpinner from "./UI/loadingSpinner/LoadingSpinner";

interface props {
  productName: string;
  resource: IResource | null;
  expanded: boolean;
}

function ResourceItem({ resource, productName, expanded }: props) {
  async function getResource(
    token: string,
    productName: string,
    resource: IResource | null
  ) {
    setImageLoading(true);
    const res = await getProductResource(token, productName, resource);
    if (res?.status === 200) {
      setImageURL(res?.imageURL);
    }
    setImageLoading(false);
  }
  const [imageURL, setImageURL] = useState<string>();
  const [imageLoading, setImageLoading] = useState<boolean>(false);
  const token = useAdminStore((state) => state.token);
  useEffect(() => {
    if (expanded) getResource(token, productName, resource);
  }, [resource, productName, token, expanded]);

  return imageLoading && imageURL ? (
    <LoadingSpinner></LoadingSpinner>
  ) : (
    <img
      style={{ width: "100px", height: "100px" }}
      src={imageURL}
      alt={resource?.fileName}
    ></img>
  );
}
export default ResourceItem;
