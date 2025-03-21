import React, { useState, useEffect } from "react";

const Products = ({ token, products }) => {
    const [message, setMessage] = useState("");

    return (
        <div>
            <p>{message}</p>

            <ul>
                {products.length > 0 ? (
                    products.map((p, pindex) => (
                        <li key={pindex}>
                            <strong>{p.name}</strong>
                        </li>
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
