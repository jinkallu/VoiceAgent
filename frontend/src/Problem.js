import React, { useState, useEffect } from "react";
import Solution from "./Solution";

const Problem = ({ token, index, problem }) => {
    const [message, setMessage] = useState("");
    const [product_data, setProductData] = useState("")


    useEffect(() => {

        if (!problem) {
            return
        }


    }, [problem])


    return (
        <div>

            <li key={index}>
                {problem && problem["problem"] &&
                    <strong>{index}. {problem["problem"]}</strong>
                }
            </li>
            <ul>
                {(problem && problem["solution steps"] && problem["solution steps"].length > 0) ? (
                    problem["solution steps"].map((p, pindex) => (
                        <Solution token={token} index={pindex} step={p} />
                    )
                    )
                ) : (
                    <p>No Solution found</p>
                )}

            </ul>

        </div>
    );
};

export default Problem;
