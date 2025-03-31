import { useState } from "react";
import Button from "./UI/button/Button";
import { addProduct } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import { useNavigate } from "react-router-dom";

function CreateProduct() {
  const [productName, setProductName] = useState<string>("");
  const token = useAdminStore((state) => state.token);

  const navigate = useNavigate();
  const addNewProduct = async (name: string) => {
    const prodName = name.toLowerCase();
    const res = await addProduct(token, prodName);
    if (res?.status === 200 && res?.data?.result) {
      navigate(`/products/${prodName}`);
    }
    console.log(res);
  };

  return (
    <section style={{ maxHeight: "100%", overflowY: "auto" }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
          minHeight: "40vh",
        }}
      >
        <div>
          <h5>
            Enter a product name . The name should contain alphabets only
            without any space
          </h5>
        </div>
        <div
          style={{ display: "flex", marginTop: "20px", alignItems: "center" }}
        >
          <input
            name="productName"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
          ></input>
          <Button onClick={() => addNewProduct(productName)}>
            Create Product
          </Button>
        </div>
      </div>
    </section>
  );
}

export default CreateProduct;
