import { useEffect, useState } from "react";
import { IResource } from "../interfaces/generic";
import { getProductResource } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import LoadingSpinner from "./UI/loadingSpinner/LoadingSpinner";
import Modal from "./UI/modal/Modal";

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
  const [openModal, setOpenModal] = useState<boolean>(false);
  useEffect(() => {
    if (expanded) getResource(token, productName, resource);
  }, [resource, productName, token, expanded]);

  return (
    <div>
      {openModal && (
        <Modal
          title="Image"
          onConfirm={() => {
            setOpenModal(false);
          }}
        >
          <img src={imageURL} alt={resource?.fileName}></img>
        </Modal>
      )}
      {imageLoading && imageURL ? (
        <LoadingSpinner></LoadingSpinner>
      ) : (
        <img
          onClick={() => setOpenModal(true)}
          style={{ width: "40px", height: "40px", cursor: "pointer" }}
          src={imageURL}
          alt={resource?.fileName}
        ></img>
      )}
    </div>
  );
}
export default ResourceItem;
