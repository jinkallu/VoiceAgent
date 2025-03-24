import React, { useState, useEffect } from "react";
import ImageResource from "./ImageResource";

const Solution = ({ token, index, step }) => {

    return (
        <div>

            <li key={index}>
                <strong>{step}</strong>
            </li>
            <ImageResource />

        </div>
    );
};

export default Solution;
