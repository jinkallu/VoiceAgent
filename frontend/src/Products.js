import React, { useState, useEffect } from "react";
import Product from "./Product";

const Products = ({ token, products }) => {
    const [message, setMessage] = useState("");
    


    return (
        <div>
            <p>{message}</p>

            <ul>
                {products.length > 0 ? (
                    products.map((p, pindex) => (
                        <Product token={token} index={pindex} product={p}/>
                    )
                    )
                ) : (
                    <p>No products found</p>
                )}
            </ul>

        </div>
    );
};

export default Products;
