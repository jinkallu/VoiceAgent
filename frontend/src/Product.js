import React, { useState, useEffect } from "react";
import Problem from "./Problem";

const Product = ({ token, index, product }) => {
    const [message, setMessage] = useState("");
    const [product_data, setProductData] = useState("")


    useEffect(() => {

        if (!product) {
            return
        }
        console.log(product)

        // Define your request payload
        const requestData = {
            product_name: product.json || null,  // Example data to send
        };


        fetch("http://127.0.0.1:8000/product_data/", {
            method: "POST",  // Use POST method to send data
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'  // Ensure you're sending JSON 
            },
            body: JSON.stringify(requestData),  // Convert the JavaScript object to JSON string
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data)
                setProductData(data.product_data || []);
            })
            .catch(() => setMessage("Unauthorized"));

    }, [product])


    return (
        <div>


            <li key={index}>
                <strong>{product.name}</strong>
            </li>
            <ul>
                {product_data.length > 0 ? (
                    product_data.map((p, pindex) => (
                        <Problem token={token} index={pindex} problem={p} />
                    )
                    )
                ) : (
                    <p>No Problems found</p>
                )}

            </ul>


        </div>
    );
};

export default Product;
